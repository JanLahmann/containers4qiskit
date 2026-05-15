#!/usr/bin/env python3
"""Generate docs/versions.json from the versions/ directory.

Walks versions/<minor>-<flavor>/ and emits an ordered list (newest minor
first, matching the build-matrix planner convention). The page JS
consumes this at runtime to render the catalog table and to populate
the URL generator's image dropdown.

Schema (one entry per published image):

    {
      "qiskit_minor": "2.4",
      "flavor":       "small" | "xl",
      "is_latest":    true,      # current LATEST_QISKIT minor
      "binder_tag":   "2.4-small",
      "docker_tag":   "ghcr.io/qubins/images:2.4-small",
      "notes":        "reduced set: ..."   # optional
    }

LATEST_QISKIT is read from build-matrix.yml's env block so we don't
need a second source of truth.

`notes` overrides live in NOTES below; keep that in sync with the
README footnotes when a flavor changes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Hand-maintained notes per image (mirrors the README footnotes).
# Empty if no special note applies.
NOTES: dict[tuple[str, str], str] = {
    ("1.4", "xl"): (
        "Reduced package set: qiskit-addon-*, qiskit-serverless, "
        "qiskit-ibm-catalog, and qiskit-ibm-transpiler are 2.x-only "
        "and not included."
    ),
}

REPO_ROOT = Path(__file__).resolve().parents[2]
VERSIONS_DIR = REPO_ROOT / "versions"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "build-matrix.yml"
DOCKER_PREFIX = "ghcr.io/qubins/images"


def latest_qiskit() -> str:
    text = WORKFLOW_PATH.read_text()
    m = re.search(r"LATEST_QISKIT:\s*'([0-9.]+)'", text)
    if not m:
        sys.exit("LATEST_QISKIT not found in build-matrix.yml")
    return m.group(1)


def discover_versions() -> list[dict]:
    pattern = re.compile(r"^(\d+\.\d+)-(small|xl)$")
    entries: list[tuple[tuple[int, int], str, str]] = []
    for child in VERSIONS_DIR.iterdir():
        if not child.is_dir():
            continue
        m = pattern.match(child.name)
        if not m:
            continue
        minor, flavor = m.group(1), m.group(2)
        sort_key = tuple(int(p) for p in minor.split("."))
        entries.append((sort_key, minor, flavor))
    # newest minor first, small before xl within a minor
    entries.sort(key=lambda x: (-x[0][0], -x[0][1], 0 if x[2] == "small" else 1))
    return [
        {"qiskit_minor": minor, "flavor": flavor}
        for _, minor, flavor in entries
    ]


def main() -> None:
    latest = latest_qiskit()
    out: list[dict] = []
    for entry in discover_versions():
        minor = entry["qiskit_minor"]
        flavor = entry["flavor"]
        tag = f"{minor}-{flavor}"
        item = {
            "qiskit_minor": minor,
            "flavor": flavor,
            "is_latest": minor == latest,
            "binder_tag": tag,
            "docker_tag": f"{DOCKER_PREFIX}:{tag}",
        }
        note = NOTES.get((minor, flavor))
        if note:
            item["notes"] = note
        out.append(item)

    payload = {
        "latest_qiskit": latest,
        "images": out,
    }
    target = REPO_ROOT / "docs" / "versions.json"
    target.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {target.relative_to(REPO_ROOT)} ({len(out)} images, latest={latest})")


if __name__ == "__main__":
    main()
