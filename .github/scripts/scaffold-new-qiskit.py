#!/usr/bin/env python3
"""Scaffold a new Qiskit minor in this repo.

Reads MINOR (e.g. "2.5") and VERSION (e.g. "2.5.1") from the env. Edits
every place that needs to know about the new minor:

- versions/<MINOR>-small/requirements.txt
- versions/<MINOR>-xl/requirements.txt (mirror of the highest existing
  -xl with the qiskit pin bumped)
- .github/workflows/build-matrix.yml: prepend matrix entries to both the
  build and manifest jobs; bump LATEST_QISKIT
- .github/dependabot.yml: point the pip ecosystem's directories at the
  new minor's small + xl dirs
- README.md: update the "today: ..." line (the per-version catalog
  lives on qubins.org, generated from versions/ — no edit needed)

Idempotent: refuses to do anything if versions/<MINOR>-small/ already
exists.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

MINOR = os.environ["MINOR"]      # e.g. "2.5"
VERSION = os.environ["VERSION"]  # e.g. "2.5.1"

REPO = Path.cwd()
VERSIONS = REPO / "versions"

small_dir = VERSIONS / f"{MINOR}-small"
xl_dir    = VERSIONS / f"{MINOR}-xl"

if small_dir.exists():
    print(f"versions/{MINOR}-small already exists; nothing to do.")
    sys.exit(0)


# --- new requirements files ------------------------------------------------

small_dir.mkdir(parents=True)
(small_dir / "requirements.txt").write_text(
    f"qiskit~={MINOR}.0\n"
    "qiskit-aer\n"
    "qiskit-ibm-runtime\n"
)

xl_candidates = sorted(
    (p for p in VERSIONS.iterdir() if re.fullmatch(r"\d+\.\d+-xl", p.name)),
    key=lambda p: tuple(int(x) for x in p.name.removesuffix("-xl").split(".")),
)
if not xl_candidates:
    sys.exit("No existing -xl directory to template from.")
template = xl_candidates[-1] / "requirements.txt"
xl_dir.mkdir(parents=True)
(xl_dir / "requirements.txt").write_text(
    re.sub(
        r"qiskit\[all\]~=\d+\.\d+\.\d+",
        f"qiskit[all]~={MINOR}.0",
        template.read_text(),
        count=1,
    )
)


# --- .github/workflows/build-matrix.yml ------------------------------------

wf_path = REPO / ".github" / "workflows" / "build-matrix.yml"
wf = wf_path.read_text()

wf = re.sub(
    r"LATEST_QISKIT: '\d+\.\d+'",
    f"LATEST_QISKIT: '{MINOR}'",
    wf,
)
# The canonical version list lives in the planner job's `ALL` bash
# array; both build and manifest matrices read from the planner's
# JSON output. Prepend the new minor as its own line so the
# scaffolder ordering convention holds (newest first).
wf = re.sub(
    r"(\n          ALL=\(\n)",
    rf"\g<1>            '{MINOR}-small' '{MINOR}-xl'\n",
    wf,
    count=1,
)

wf_path.write_text(wf)


# --- .github/dependabot.yml ------------------------------------------------

db_path = REPO / ".github" / "dependabot.yml"
db = db_path.read_text()
db = re.sub(r"(/versions/)\d+\.\d+(-small)", rf"\g<1>{MINOR}\g<2>", db)
db = re.sub(r"(/versions/)\d+\.\d+(-xl)",    rf"\g<1>{MINOR}\g<2>", db)
db_path.write_text(db)


# --- README.md -------------------------------------------------------------

readme_path = REPO / "README.md"
readme = readme_path.read_text()
# The per-version catalog now lives on qubins.org (generated from
# versions/ at deploy time). Only the "today: <minor>" hint needs
# bumping in README.
readme = re.sub(
    r"\(today: `\d+\.\d+`\)",
    f"(today: `{MINOR}`)",
    readme,
)
readme_path.write_text(readme)

print(f"Scaffolded Qiskit {MINOR} (qiskit {VERSION}).")
