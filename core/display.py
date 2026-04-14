"""
core/display.py
───────────────
Shared display utilities: ANSI-coloured alert rendering and Rich markdown output.
All other modules import from here to keep colour logic in one place.
"""

from rich.console import Console
from rich.markdown import Markdown

console = Console()

# Alert prefixes as they appear in .txt / .md files
ALERT_PREFIXES = [
    "[!] WARNING: ",
    "[?] REMINDER: ",
    "[+] SUGGESTION: ",
    "[+] BEST PRACTICE: ",
]

# ANSI colour code matched to each prefix
ALERT_COLORS = [
    "\033[93m",  # yellow  — WARNING
    "\033[94m",  # blue    — REMINDER
    "\033[92m",  # green   — SUGGESTION
    "\033[92m",  # green   — BEST PRACTICE
]

RESET = "\033[0m"
BOLD  = "\033[1m"


def colourise_alerts(text: str) -> str:
    """Replace plain-text alert prefixes with ANSI-coloured equivalents."""
    for prefix, colour in zip(ALERT_PREFIXES, ALERT_COLORS):
        if prefix in text:
            text = text.replace(
                prefix,
                f"{BOLD}{colour}{prefix}{RESET}{colour}",
            )
    return text + RESET


def print_alert_file(path: str) -> None:
    """Read an alert .txt file, colourise and print it."""
    try:
        with open(path) as f:
            print(colourise_alerts(f.read()))
    except FileNotFoundError:
        pass  # Several commands intentionally have empty alert files


def print_markdown_file(path: str) -> None:
    """Render a Markdown file with Rich, with coloured alerts."""
    with open(path) as f:
        content = colourise_alerts(f.read())
    console.print(Markdown(content))
