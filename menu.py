"""
qualys/menu.py
──────────────
Entry point for the Qualys VMDR scan analysis module.
Provides a simple interactive menu to choose between image-level and
container-level scan result processing.
"""

from termcolor import colored


def _print_banner() -> None:
    print(
        "\n"
        "╔══════════════════════════════════════════╗\n"
        "║       Qualys Scan Analysis Module        ║\n"
        "║  Container & Image vulnerability reports ║\n"
        "╚══════════════════════════════════════════╝\n"
    )


def run() -> None:
    """Interactive menu for the Qualys scan analysis sub-module."""
    _print_banner()

    options = {
        "1": ("Image scan results",     _run_image_scan),
        "2": ("Container scan results", _run_container_scan),
        "q": ("Quit",                   None),
    }

    while True:
        print("Select an option:")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")

        choice = input("\nChoice: ").strip().lower()

        if choice == "q":
            break
        if choice not in options:
            print(colored("[!] Invalid choice.", "red"))
            continue

        _, action = options[choice]
        if action:
            action()


# ── Sub-actions ───────────────────────────────────────────────────────────────

def _run_image_scan() -> None:
    try:
        from Qualys_scan import image_qualys_results as img  # type: ignore
        img.main()
    except ImportError:
        print(colored(
            "[!] Could not import Qualys_scan.image_qualys_results. "
            "Make sure the Qualys_scan directory is on your PYTHONPATH.",
            "red",
        ))


def _run_container_scan() -> None:
    try:
        from Qualys_scan import container_qualys_results as cont  # type: ignore
        cont.main()
    except ImportError:
        print(colored(
            "[!] Could not import Qualys_scan.container_qualys_results. "
            "Make sure the Qualys_scan directory is on your PYTHONPATH.",
            "red",
        ))
