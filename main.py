#!/usr/bin/env python3
"""
Dockerfile Assistant
────────────────────
A CLI tool that guides developers through writing secure Dockerfiles.

Features
  • Interactive, step-by-step Dockerfile creation with inline documentation
  • Grype integration — scan base images and final images for CVEs
  • Hadolint integration — static analysis of the generated Dockerfile
  • docker run auditor — checks hardening flags on run commands
  • Qualys VMDR module — analyse scan exports from a Dockerised environment

Usage
  python main.py                 # guided creation + security scans
  python main.py --scan-only     # skip creation, jump to scans
  python main.py --qualys        # launch the Qualys analysis module
"""

import argparse
import sys

from core.builder  import build_dockerfile
from core.scanner  import dockerfile_scan, dockerrun_scan


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="dockerfile-assistant",
        description="Guided Dockerfile creation with integrated security scanning.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py                 # full interactive workflow\n"
            "  python main.py --scan-only     # scan an existing Dockerfile\n"
            "  python main.py --qualys        # Qualys VMDR analysis module\n"
        ),
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Skip Dockerfile creation and go directly to the scanning phase.",
    )
    parser.add_argument(
        "--qualys",
        action="store_true",
        help="Launch the Qualys VMDR scan analysis module.",
    )
    return parser.parse_args()


# ── Scanning phase ────────────────────────────────────────────────────────────

def _run_scan_phase() -> None:
    """Post-creation scanning: Hadolint + docker run audit."""
    if input("\nScan the Dockerfile with Hadolint (y/n)? ").lower() == "y":
        dockerfile_scan()

    if input("\nAudit a 'docker run' command (y/n)? ").lower() == "y":
        while True:
            command = input("Paste the 'docker run' command: ").strip()
            if command:
                dockerrun_scan(command)
            if input("\nAudit another command (y/n)? ").lower() != "y":
                break


# ── Banner ────────────────────────────────────────────────────────────────────

def _print_banner() -> None:
    print(
        "\n"
        "╔══════════════════════════════════════════╗\n"
        "║       Welcome to Dockerfile Assistant    ║\n"
        "║  Guided creation + Docker security scans ║\n"
        "╚══════════════════════════════════════════╝\n"
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    if args.qualys:
        from qualys.menu import run as run_qualys
        run_qualys()
        return

    _print_banner()

    if not args.scan_only:
        build_dockerfile()

    _run_scan_phase()


if __name__ == "__main__":
    main()
