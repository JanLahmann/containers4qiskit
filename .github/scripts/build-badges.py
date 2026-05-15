#!/usr/bin/env python3
"""Generate shields.io-style "launch on QuBins" badges as static SVGs.

Outputs to docs/badges/:
  - launch-on-qubins.svg                    (generic, no image label)
  - launch-on-qubins-<tag>.svg              (one per image, e.g. 2.4-xl)
  - launch-on-qubins-latest-{small,xl}.svg  (aliases of the latest minor)

Each SVG is hand-laid-out (no rsvg dependency) so anyone can read the
output. Width is calculated from text length using an approximate
character-width constant tuned for the Verdana family that shields.io
uses; renderers are tolerant of a few px of slack.

Re-run after every change to versions/ or LATEST_QISKIT.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VERSIONS_JSON = REPO_ROOT / "docs" / "versions.json"
OUT_DIR = REPO_ROOT / "docs" / "badges"

# Approximate width per character at font-size=11 in DejaVu Sans / Verdana.
# Slight overestimate to ensure no clipping.
CHAR_W = 6.0
PAD_X = 6  # horizontal padding inside each half
LEFT_BG = "#555"
RIGHT_BG = "#2da44e"  # QuBins green (matches the "latest" tag pill on the page)
TEXT = "#fff"


def text_width(s: str) -> int:
    # Round up so we never clip; minimum 30 to fit short labels neatly.
    return max(30, int(len(s) * CHAR_W + 2 * PAD_X))


def render(left: str, right: str) -> str:
    lw = text_width(left)
    rw = text_width(right)
    total = lw + rw
    # shields.io trick: render text twice with a slight Y-offset (and
    # 70%-opacity black shadow first) for a subtle drop-shadow.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20" role="img" aria-label="{left}: {right}">
  <title>{left}: {right}</title>
  <linearGradient id="g" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{lw}" height="20" fill="{LEFT_BG}"/>
    <rect x="{lw}" width="{rw}" height="20" fill="{RIGHT_BG}"/>
    <rect width="{total}" height="20" fill="url(#g)"/>
  </g>
  <g fill="{TEXT}" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{lw / 2}" y="15" fill="#010101" fill-opacity=".3">{left}</text>
    <text x="{lw / 2}" y="14">{left}</text>
    <text x="{lw + rw / 2}" y="15" fill="#010101" fill-opacity=".3">{right}</text>
    <text x="{lw + rw / 2}" y="14">{right}</text>
  </g>
</svg>
"""


def write(filename: str, content: str) -> None:
    path = OUT_DIR / filename
    path.write_text(content)
    print(f"  {path.relative_to(REPO_ROOT)}  ({len(content)} bytes)")


def main() -> None:
    if not VERSIONS_JSON.exists():
        sys.exit(
            f"{VERSIONS_JSON.relative_to(REPO_ROOT)} not found; "
            "run build-pages-data.py first."
        )
    data = json.loads(VERSIONS_JSON.read_text())
    images = data["images"]
    latest_minor = data["latest_qiskit"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Writing badges to {OUT_DIR.relative_to(REPO_ROOT)}/ ...")
    # Generic "Launch on QuBins" — for the use case where the embedder
    # doesn't want to pin a specific image (e.g. a "tap to launch
    # latest-xl" badge in a tutorial README).
    write("launch-on-qubins.svg", render("launch on", "QuBins"))

    # One per image: "launch on | QuBins 2.4-xl"
    for img in images:
        tag = img["binder_tag"]
        write(f"launch-on-qubins-{tag}.svg", render("launch on", f"QuBins {tag}"))

    # latest-* aliases of the current minor
    for flavor in ("small", "xl"):
        tag = f"latest-{flavor}"
        write(f"launch-on-qubins-{tag}.svg", render("launch on", f"QuBins {tag}"))

    print(f"Done. latest minor = {latest_minor}.")


if __name__ == "__main__":
    main()
