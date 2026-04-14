"""
core/scanner.py
───────────────
Three independent scanning functions:

  vulnerability_scan(image)   — Grype scan of a Docker image
  dockerfile_scan(path)       — Hadolint static analysis of a Dockerfile
  dockerrun_scan(command)     — Security audit of a 'docker run' command

All bugs present in the original implementation are fixed here and marked
with a  # BUG FIX  comment so the changes are easy to trace.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from termcolor import colored

# ── Output artefacts ──────────────────────────────────────────────────────────

GRYPE_OUTPUT    = Path("grype_results.json")
HADOLINT_OUTPUT = Path("hadolint_results.json")


# ─────────────────────────────────────────────────────────────────────────────
# Grype — image vulnerability scanning
# ─────────────────────────────────────────────────────────────────────────────

def vulnerability_scan(image: str) -> None:
    """Run Grype against *image* and print a severity summary."""
    print(
        colored("[+] Scanning image with Grype:", "green", attrs=["bold"])
        + " https://github.com/anchore/grype/\n"
        + f"    Target: {image} (may take a moment…)"
    )
    try:
        result = subprocess.run(
            ["grype", "-o", "json", image],
            capture_output=True,
            text=True,
            check=False,
        )
        GRYPE_OUTPUT.write_text(result.stdout)
        _print_grype_summary()
        print(
            "Full results saved to"
            + colored(f" {GRYPE_OUTPUT}", "white", attrs=["bold"])
        )
    except FileNotFoundError:
        print(colored(
            "[!] Grype not found. Install it from https://github.com/anchore/grype/",
            "red",
        ))
    except Exception as exc:
        print(colored(f"[!] Grype error: {exc}", "red"))


def _print_grype_summary() -> None:
    try:
        data = json.loads(GRYPE_OUTPUT.read_text())
    except (json.JSONDecodeError, FileNotFoundError) as exc:
        print(colored(f"[!] Could not parse Grype output: {exc}", "red"))
        return

    counts: dict[str, int] = {
        k: 0 for k in ("critical", "high", "medium", "low", "negligible", "unknown")
    }
    for match in data.get("matches", []):
        sev = match.get("vulnerability", {}).get("severity", "unknown").lower()
        counts[sev] = counts.get(sev, 0) + 1

    total = sum(counts.values())
    print(colored(f"\n[!] Total vulnerabilities: {total}", "dark_grey", attrs=["bold"]))
    print(colored(f"    Critical:   {counts['critical']}",   "red",       attrs=["bold"]))
    print(colored(f"    High:       {counts['high']}",       "light_red", attrs=["bold"]))
    print(colored(f"    Medium:     {counts['medium']}",     "yellow",    attrs=["bold"]))
    print(colored(f"    Low:        {counts['low']}",        "blue",      attrs=["bold"]))
    print(colored(f"    Negligible: {counts['negligible']}", "white",     attrs=["bold"]))
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Hadolint — Dockerfile static analysis
# ─────────────────────────────────────────────────────────────────────────────

def dockerfile_scan(dockerfile: str = "Dockerfile") -> None:
    """
    Run Hadolint against *dockerfile*.

    Human-readable output goes to stdout; a JSON copy is saved to
    hadolint_results.json for downstream processing.
    """
    print(
        colored("[+] Analysing Dockerfile with Hadolint:", "green", attrs=["bold"])
        + " https://github.com/hadolint/hadolint"
    )
    try:
        # Human-readable pass — output goes directly to the terminal
        subprocess.run(["hadolint", dockerfile], check=False)

        # BUG FIX: original code was
        #   ["hadolint", "-f", "json" "Dockerfile"]
        # The missing comma between "json" and "Dockerfile" caused Python's
        # implicit string concatenation to produce the single token
        # "jsonDockerfile", so Hadolint never received a valid -f argument
        # and the JSON output file was always empty / malformed.
        result = subprocess.run(
            ["hadolint", "-f", "json", dockerfile],   # <-- comma added
            capture_output=True,
            text=True,
            check=False,
        )
        HADOLINT_OUTPUT.write_text(result.stdout)
        print(
            "JSON results saved to"
            + colored(f" {HADOLINT_OUTPUT}", "white", attrs=["bold"])
        )
    except FileNotFoundError:
        print(colored(
            "[!] Hadolint not found. Install it from https://github.com/hadolint/hadolint",
            "red",
        ))
    except Exception as exc:
        print(colored(f"[!] Hadolint error: {exc}", "red"))


# ─────────────────────────────────────────────────────────────────────────────
# docker run — command security analysis
# ─────────────────────────────────────────────────────────────────────────────

def dockerrun_scan(command: str) -> None:
    """
    Audit a 'docker run' command string and print categorised findings:
    ERRORs (must fix), WARNINGs (should fix), BEST PRACTICEs (consider).

    Bug fixes vs original implementation
    ─────────────────────────────────────
    1. `("--cpus" or "--memory") not in command`
       Python evaluates `"--cpus" or "--memory"` to `"--cpus"` (first truthy
       operand), so the --memory branch was never checked independently.
       Fixed to:  `"--cpus" not in command and "--memory" not in command`

    2. `"--memor-swap"` (typo) → `"--memory-swap"`
       The original typo meant this check never triggered.

    3. `if "-p" or "-P" in command`
       `"-p"` is a non-empty string → always truthy → warning always fired.
       Fixed to:  `"-p" in command or "-P" in command`

    4. `if ("-v" or "--mount" in command) and ...`
       Same short-circuit issue as #3.
       Fixed to:  `("-v" in command or "--mount" in command) and ...`
    """
    errors:         list[str] = []
    warnings:       list[str] = []
    best_practices: list[str] = []

    # ── Hard errors ───────────────────────────────────────────────────────────

    if "--security-opt=no-new-privileges" not in command:
        errors.append(_err(
            "Always add '--security-opt=no-new-privileges' to block privilege "
            "escalation attempts from inside the container."
        ))

    if "--privileged" in command:
        errors.append(_err(
            "'--privileged' grants ALL Linux kernel capabilities to the container "
            "— effectively giving it root access on the host. Remove it."
        ))
        best_practices.append(_bp(
            "Drop all capabilities first ('--cap-drop all'), then re-add only "
            "those your application genuinely needs ('--cap-add <CAP>')."
        ))

    if "/var/run/docker.sock" in command:
        errors.append(_err(
            "Do not bind-mount /var/run/docker.sock into a container. It grants "
            "full control over the Docker daemon and is a classic host-escape vector."
        ))

    if "--device" in command:
        errors.append(_err(
            "'--device' exposes host hardware to the container. "
            "This is a high-risk privilege escalation surface — remove it."
        ))

    # ── Warnings ──────────────────────────────────────────────────────────────

    if "--read-only" not in command:
        warnings.append(_warn(
            "Run with a read-only root filesystem ('--read-only'). "
            "Use '--tmpfs /tmp' for writable scratch space when needed."
        ))

    # BUG FIX #1 — independent checks for --cpus and --memory
    if "--cpus" not in command and "--memory" not in command:
        warnings.append(_warn(
            "Set resource limits to prevent runaway containers / DoS: "
            "e.g. '--cpus=1.5 --memory=512m'. "
            "See: https://docs.docker.com/engine/containers/resource_constraints/"
        ))

    if "--restart" not in command:
        warnings.append(_warn(
            "Define an explicit restart policy for predictable lifecycle management: "
            "e.g. '--restart=unless-stopped' or '--restart=on-failure:3'."
        ))

    if "--network=host" in command:
        warnings.append(_warn(
            "'--network=host' removes all network isolation. "
            "Use a user-defined bridge network for container-to-container communication: "
            "https://docs.docker.com/network/#communication-between-containers"
        ))

    if "--pids-limit" not in command:
        warnings.append(_warn(
            "Set '--pids-limit' to cap the number of processes and prevent "
            "fork-bomb style DoS attacks: "
            "https://docs.docker.com/engine/containers/resource_constraints/"
        ))

    # BUG FIX #2 — corrected spelling: --memor-swap → --memory-swap
    if "--memory-swap" not in command:
        warnings.append(_warn(
            "Consider '--memory-swap' to control swap usage: "
            "https://docs.docker.com/engine/containers/resource_constraints/"
        ))

    # BUG FIX #3 — explicit membership check instead of `"-p" or "-P" in command`
    if "-p" in command or "-P" in command:
        warnings.append(_warn(
            "When publishing ports, bind explicitly to a specific interface "
            "rather than 0.0.0.0: e.g. '-p 127.0.0.1:8080:80'. "
            "See: https://docs.docker.com/engine/reference/commandline/dockerd/"
            "#daemon-socket-option"
        ))

    # BUG FIX #4 — correct short-circuit on the -v / --mount check
    if ("-v" in command or "--mount" in command) and (
        ":ro" not in command and ",readonly" not in command
    ):
        warnings.append(_warn(
            "If this volume should be read-only, append ':ro' to '-v' "
            "(e.g. '-v vol:/data:ro') or add ',readonly' to '--mount …'."
        ))

    # ── Best practices (always shown) ─────────────────────────────────────────

    best_practices.extend([
        _bp("Keep the host OS and Docker Engine up to date."),
        _bp(
            "Do not disable the default seccomp profile. Consider AppArmor as an "
            "additional MAC layer: https://docs.docker.com/engine/security/apparmor/"
        ),
        _bp("Verify daemon log level is 'info' in /etc/docker/daemon.json."),
        _bp(
            "Run the Docker daemon in rootless mode where possible: "
            "https://docs.docker.com/engine/security/rootless/"
        ),
        _bp(
            "Manage secrets with Docker Secrets, not environment variables: "
            "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
        ),
    ])

    # ── Output ────────────────────────────────────────────────────────────────

    if not errors and not warnings:
        print(colored("[+] No critical issues detected.", "green", attrs=["bold"]))

    for msg in errors + warnings + best_practices:
        print(msg)


# ── Private helpers ───────────────────────────────────────────────────────────

def _err(msg: str) -> str:
    return colored("[!] ERROR: ",         "red",    attrs=["bold"]) + colored(msg, "red")

def _warn(msg: str) -> str:
    return colored("[!] WARNING: ",       "yellow", attrs=["bold"]) + colored(msg, "yellow")

def _bp(msg: str) -> str:
    return colored("[+] BEST PRACTICE: ", "green",  attrs=["bold"]) + colored(msg, "green")
