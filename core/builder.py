"""
core/builder.py
───────────────
Guides the user through interactive Dockerfile creation.

Key design changes vs the original:

  • The monolithic main() has been split into small, single-purpose functions.
  • The verbose match/case block is replaced by a data-driven dispatch table
    (INSTRUCTION_CONFIG). Adding a new Dockerfile instruction now requires
    only a one-line entry in the dict.
  • Base-image validation (latest tag, missing colon) is in its own function.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from termcolor import colored

from core.display import colourise_alerts, console
from core.scanner import vulnerability_scan
from core.writer import append_to_dockerfile, read_alerts, write_instruction
from rich.markdown import Markdown

INSTRUCTIONS_MD = Path("instructions.md")

# ── Instruction configuration ─────────────────────────────────────────────────

@dataclass(frozen=True)
class InstructionConfig:
    """Declares how each Dockerfile instruction should be handled."""
    show_alerts:      bool = True
    ask_confirmation: bool = False  # prompt "still want to use it?" after alerts


# One entry per supported Dockerfile keyword.
# To add a new instruction: one line here, plus alerts/ and commands/ files.
INSTRUCTION_CONFIG: dict[str, InstructionConfig] = {
    "ADD":         InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "ARG":         InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "CMD":         InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "COPY":        InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "ENTRYPOINT":  InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "ENV":         InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "EXPOSE":      InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "FROM":        InstructionConfig(show_alerts=False, ask_confirmation=False),
    "HEALTHCHECK": InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "LABEL":       InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "MAINTAINER":  InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "ONBUILD":     InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "RUN":         InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "SHELL":       InstructionConfig(show_alerts=True,  ask_confirmation=True),
    "STOPSIGNAL":  InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "USER":        InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "VOLUME":      InstructionConfig(show_alerts=True,  ask_confirmation=False),
    "WORKDIR":     InstructionConfig(show_alerts=True,  ask_confirmation=False),
}

_KNOWN_INSTRUCTIONS = set(INSTRUCTION_CONFIG.keys())

_BASE_IMAGE_BEST_PRACTICE = (
    "[+] BEST PRACTICE: Use current official images as your base. "
    "Alpine is recommended — it is small (< 6 MB) yet a full Linux distribution. "
    "Always pin an explicit version tag; never rely on 'latest'."
)


# ── Base-image selection ───────────────────────────────────────────────────────

def _validate_image_syntax(image: str) -> str | None:
    """
    Return an error message if the image string is invalid, else None.
    Checks enforced:
      - Must use  image:tag  syntax (colon required)
      - 'latest' tag is explicitly discouraged
    """
    if "latest" in image:
        return (
            '[!] WARNING: Avoid the "latest" tag — it makes builds '
            "non-reproducible. Specify an exact version."
        )
    if ":" not in image:
        return "[!] WARNING: Use the correct syntax:  image:tag  (e.g. python:3.12-slim)."
    return None


def _select_base_image() -> None:
    """Prompt for a base image, optionally scan it, then write the FROM line."""
    print("\n" + colored("── Step 1: Base image ──────────────────────────", "cyan", attrs=["bold"]))
    print(colored(_BASE_IMAGE_BEST_PRACTICE, "green"))

    while True:
        image = input("\nBase image (image:tag): ").strip()

        error = _validate_image_syntax(image)
        if error:
            print(colored(error, "yellow", attrs=["bold"]))
            continue

        if input("Scan this image for known vulnerabilities before proceeding (y/n)? ").lower() == "y":
            vulnerability_scan(image)
            if input("Continue with this image anyway (y/n)? ").lower() == "n":
                print("Choose a different image.\n")
                continue

        append_to_dockerfile(f"FROM {image}")
        print(colored("[+] Base image selected.", "green", attrs=["bold"]))
        time.sleep(0.6)
        return


# ── Instruction loop ───────────────────────────────────────────────────────────

def _print_instruction_menu() -> None:
    """Print instructions.md with coloured alerts using Rich."""
    try:
        content = colourise_alerts(INSTRUCTIONS_MD.read_text())
        console.print(Markdown(content))
    except FileNotFoundError:
        print(colored("[!] instructions.md not found.", "red"))


def _handle_instruction(instruction: str) -> None:
    """
    Dispatch a single instruction through its configured flow:
      1. Show alerts (if configured)
      2. Ask for confirmation (if configured)
      3. Invoke the instruction writer
    """
    config = INSTRUCTION_CONFIG.get(instruction)
    if config is None:
        print(colored(
            f"[!] Unknown instruction '{instruction}'. "
            f"Supported: {', '.join(sorted(_KNOWN_INSTRUCTIONS))}",
            "red",
        ))
        return

    if config.show_alerts:
        read_alerts(instruction)
        time.sleep(0.4)

    if config.ask_confirmation:
        answer = input("Would you still like to add this instruction (y/n)? ").lower()
        if answer != "y":
            return

    write_instruction(instruction)


# ── Public entry point ────────────────────────────────────────────────────────

def build_dockerfile() -> None:
    """
    Full interactive Dockerfile creation flow:
      1. Select base image (with optional Grype scan)
      2. Add instructions one at a time until the user types 'quit'
    """
    _select_base_image()

    print("\n" + colored("── Step 2: Add instructions ────────────────────", "cyan", attrs=["bold"]))
    print("Type an instruction name (e.g. RUN, COPY, ENV) or 'quit' to finish.\n")

    while True:
        _print_instruction_menu()
        raw = input("\nInstruction (or 'quit'): ").strip().upper()

        if raw == "QUIT":
            break
        if raw == "":
            continue

        _handle_instruction(raw)

    print(colored("\n[+] Dockerfile creation complete.", "green", attrs=["bold"]))
