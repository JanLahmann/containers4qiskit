#!/usr/bin/env python3
"""Scaffold a new Qiskit minor in this repo.

Reads MINOR (e.g. "2.5") and VERSION (e.g. "2.5.1") from the env. Edits
every place that needs to know about the new minor:

- versions/<MINOR>-small/requirements.txt
- versions/<MINOR>-xl/requirements.txt (mirror of the highest existing
  -xl with the qiskit pin bumped)
- versions/<MINOR>-xxl/requirements.txt (mirror of the highest existing
  -xxl, with its `-r ../<old>-xl/...` include repointed at this minor's
  -xl and the qiskit pin bumped) — only if an -xxl template exists;
  xxl was introduced at 2.4, so older minors that never had one are
  left two-flavor.
- .github/workflows/build-matrix.yml: prepend matrix entries to both the
  build and manifest jobs; bump LATEST_QISKIT
- .github/dependabot.yml: point the pip ecosystem's directories at the
  new minor's small + xl + xxl dirs
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

# Schema-gate the inputs at startup. The detector workflow already
# validates the PyPI string, but this script is also runnable by hand
# and writes filesystem paths + does regex substitutions into
# build-matrix.yml / dependabot.yml from MINOR. Anchoring the shape
# here means a malformed value (path traversal via "../", YAML-breaking
# characters, pre-release junk) fails loudly before any file is
# written rather than corrupting tracked files.
if not re.fullmatch(r"\d+\.\d+", MINOR):
    sys.exit(f"MINOR must be X.Y (got {MINOR!r}); refusing to scaffold.")
if not re.fullmatch(r"\d+\.\d+\.\d+", VERSION):
    sys.exit(f"VERSION must be X.Y.Z (got {VERSION!r}); refusing to scaffold.")
if not VERSION.startswith(f"{MINOR}."):
    sys.exit(f"VERSION {VERSION!r} is not within MINOR {MINOR!r}.")

REPO = Path.cwd()
VERSIONS = REPO / "versions"

small_dir = VERSIONS / f"{MINOR}-small"
xl_dir    = VERSIONS / f"{MINOR}-xl"
xxl_dir   = VERSIONS / f"{MINOR}-xxl"

if small_dir.exists():
    print(f"versions/{MINOR}-small already exists; nothing to do.")
    sys.exit(0)


def latest_template(suffix: str) -> Path | None:
    """Highest existing versions/<minor>-<suffix>/requirements.txt, or
    None if no minor has that flavor yet."""
    cands = sorted(
        (p for p in VERSIONS.iterdir()
         if re.fullmatch(rf"\d+\.\d+-{suffix}", p.name)),
        key=lambda p: tuple(
            int(x) for x in p.name.removesuffix(f"-{suffix}").split(".")
        ),
    )
    return (cands[-1] / "requirements.txt") if cands else None


# --- new requirements files ------------------------------------------------

small_dir.mkdir(parents=True)
(small_dir / "requirements.txt").write_text(
    f"qiskit~={MINOR}.0\n"
    "qiskit-aer\n"
    "qiskit-ibm-runtime\n"
)

xl_template = latest_template("xl")
if xl_template is None:
    sys.exit("No existing -xl directory to template from.")
xl_dir.mkdir(parents=True)
(xl_dir / "requirements.txt").write_text(
    re.sub(
        r"qiskit\[all\]~=\d+\.\d+\.\d+",
        f"qiskit[all]~={MINOR}.0",
        xl_template.read_text(),
        count=1,
    )
)

# xxl mirrors the highest existing xxl. It includes its sibling xl via
# `-r ../<minor>-xl/requirements.txt`, so that include must be repointed
# from the template's minor to this one. xxl was introduced at 2.4;
# minors that predate it (no xxl template) stay two-flavor.
xxl_template = latest_template("xxl")
if xxl_template is not None:
    xxl_text = xxl_template.read_text()
    xxl_text = re.sub(
        r"-r \.\./\d+\.\d+-xl/requirements\.txt",
        f"-r ../{MINOR}-xl/requirements.txt",
        xxl_text,
    )
    # Bump every prose reference to the template's minor — the header
    # comment names the minor and both the ../<m>-xl and ../<m>-xxl
    # paths in explanatory text, not just on the `-r` line.
    old_minor = xxl_template.parent.name.removesuffix("-xxl")
    xxl_text = xxl_text.replace(f"Qiskit {old_minor} ", f"Qiskit {MINOR} ")
    xxl_text = xxl_text.replace(f"../{old_minor}-xl", f"../{MINOR}-xl")
    xxl_text = xxl_text.replace(f"../{old_minor}-xxl", f"../{MINOR}-xxl")
    xxl_dir.mkdir(parents=True)
    (xxl_dir / "requirements.txt").write_text(xxl_text)


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
# scaffolder ordering convention holds (newest first). Include the
# xxl entry only if we actually scaffolded an xxl dir for this minor.
matrix_entries = f"'{MINOR}-small' '{MINOR}-xl'"
if xxl_dir.exists():
    matrix_entries += f" '{MINOR}-xxl'"
wf = re.sub(
    r"(\n          ALL=\(\n)",
    rf"\g<1>            {matrix_entries}\n",
    wf,
    count=1,
)

wf_path.write_text(wf)


# --- .github/dependabot.yml ------------------------------------------------

db_path = REPO / ".github" / "dependabot.yml"
db = db_path.read_text()
# `-small` / `-xl` / `-xxl` are anchored at end-of-line so the `-xl`
# pattern can't also chew the `-xl` prefix of an `-xxl` entry.
db = re.sub(r"(/versions/)\d+\.\d+(-small)$", rf"\g<1>{MINOR}\g<2>",
            db, flags=re.M)
db = re.sub(r"(/versions/)\d+\.\d+(-xl)$", rf"\g<1>{MINOR}\g<2>",
            db, flags=re.M)
if xxl_dir.exists():
    if re.search(r"/versions/\d+\.\d+-xxl$", db, flags=re.M):
        # Some minor already had an xxl line — just repoint it.
        db = re.sub(r"(/versions/)\d+\.\d+(-xxl)$", rf"\g<1>{MINOR}\g<2>",
                    db, flags=re.M)
    else:
        # First minor to gain xxl: append an xxl line right after this
        # minor's xl line, matching its indentation.
        m = re.search(
            rf"^(?P<indent>[ \t]*)-(?P<gap>[ \t]+)/versions/{re.escape(MINOR)}-xl$",
            db, flags=re.M,
        )
        if m:
            xl_line = m.group(0)
            xxl_line = f"{m.group('indent')}-{m.group('gap')}/versions/{MINOR}-xxl"
            db = db.replace(xl_line, f"{xl_line}\n{xxl_line}", 1)
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
