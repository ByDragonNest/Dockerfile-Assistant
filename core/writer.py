"""
core/writer.py
──────────────
Low-level helpers that append content to the Dockerfile being built.
Replaces the original instructions.py with cleaner separation of concerns.
"""

import time
from pathlib import Path
from termcolor import colored

from core.display import print_alert_file, print_markdown_file

ALERTS_DIR   = Path("alerts")
COMMANDS_DIR = Path("commands")
DOCKERFILE   = Path("Dockerfile")


def append_to_dockerfile(line: str) -> None:
    """Append *line* (plus a newline) to the current Dockerfile."""
    with DOCKERFILE.open("a") as f:
        f.write(line + "\n")


def read_alerts(instruction: str) -> None:
    """Print the alert file for *instruction* (if it exists and is non-empty)."""
    print_alert_file(str(ALERTS_DIR / f"{instruction}.txt"))


def write_instruction(instruction: str) -> None:
    """
    Show the full documentation page for *instruction*, optionally add a
    comment, then prompt the user to type the instruction body and persist
    it to the Dockerfile.  Supports multi-line continuation with '\\'.
    """
    print_markdown_file(str(COMMANDS_DIR / f"{instruction}.md"))

    # Optional inline comment
    if input("Would you like to add a comment above this instruction (y/n)? ").lower() == "y":
        comment = input("Comment (remember to start with '#'): ")
        append_to_dockerfile(comment)

    # Main instruction body
    print("  Tip: end a line with '\\' to continue writing on the next line.")
    body = input(f"  Instruction body (omit the '{instruction}' keyword): ").strip()
    full_line = f"{instruction} {body}"
    append_to_dockerfile(full_line)

    # Multi-line continuation loop
    while full_line.rstrip().endswith("\\"):
        continuation = input("  Next line: ").strip()
        append_to_dockerfile(continuation)
        full_line = continuation

    print(colored(f"[+] Added: {instruction} …", "green", attrs=["bold"]))
    time.sleep(0.6)
