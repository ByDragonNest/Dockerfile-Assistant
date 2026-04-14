# Dockerfile Assistant

A CLI tool that guides developers through writing secure Dockerfiles —
from base-image selection to final container hardening.

---

## Features

| Feature | Description |
|---|---|
| **Guided creation** | Step-by-step Dockerfile authoring with inline documentation for every instruction |
| **Grype integration** | CVE scan of the base image before you commit to it, and again after the build |
| **Hadolint integration** | Static analysis of the generated Dockerfile against best-practice rules |
| **`docker run` auditor** | Checks hardening flags (`--security-opt`, `--read-only`, `--pids-limit`, …) on any run command |

---

## Project structure

```
dockerfile-assistant/
├── main.py                  # Entry point (argparse)
├── core/
│   ├── builder.py           # Interactive Dockerfile creation flow
│   ├── scanner.py           # Grype / Hadolint / docker run auditor
│   ├── writer.py            # Low-level Dockerfile I/O helpers
│   └── display.py           # Shared colour/Rich display utilities
├── Qualys_scan/             # Qualys data processing scripts & scan exports
├── alerts/                  # Per-instruction warning text files
├── commands/                # Per-instruction full documentation (Markdown)
├── instructions.md          # Instruction reference shown during creation
├── Dockerfile               # Example intentionally-flawed Dockerfile (for demo)
└── requirements.txt
```

---

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| Python ≥ 3.10 | Runtime | [python.org](https://www.python.org/) |
| [Grype](https://github.com/anchore/grype) | Image vulnerability scanning | `brew install grype` / see docs |
| [Hadolint](https://github.com/hadolint/hadolint) | Dockerfile linting | `brew install hadolint` / see docs |

---

## Installation

```bash
git clone https://github.com/<your-handle>/dockerfile-assistant.git
cd dockerfile-assistant
pip install -r requirements.txt
```

---

## Usage

```bash
# Full interactive workflow: create a Dockerfile, then scan it
python main.py

# Skip creation — scan an existing Dockerfile + audit a docker run command
python main.py --scan-only

### Example session

```
╔══════════════════════════════════════════╗
║       Welcome to Dockerfile Assistant    ║
║  Guided creation + Docker security scans ║
╚══════════════════════════════════════════╝

── Step 1: Base image ──────────────────────────
[+] BEST PRACTICE: Use current official images …

Base image (image:tag): python:3.12-slim
Scan this image for known vulnerabilities before proceeding (y/n)? y
[+] Scanning image with Grype …

[!] Total vulnerabilities: 12
    Critical:   0
    High:       1
    …
```
---

## Origin
 
This tool started as a Master's thesis project with a specific goal: building a 
script that could actively assist developers in crafting secure Dockerfiles.
The conceptual roadmap also envisioned applying the same principles to Docker Compose configurations, 
expanding the scope of security guidance.

---

## The example Dockerfile

`Dockerfile` is intentionally full of security anti-patterns — it is used by
the tool itself as a **demo target** for Hadolint. Do not use it in production.
Issues it demonstrates:

- Running as `root` throughout
- Copying a `secret_keys.txt` into the image
- Bind-mounting the Docker socket via `VOLUME`
- Installing a known-vulnerable dependency (`flask==0.12`)
- `RUN cd /app/src` — a no-op (each `RUN` starts a fresh shell)

---

## License

MIT
