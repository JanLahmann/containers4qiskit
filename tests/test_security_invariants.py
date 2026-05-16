#!/usr/bin/env python3
"""Regression guard for the security invariants added in PR #77.

Deliberately small and dependency-free (stdlib unittest only — no
pytest, no network). Run with:  python3 -m unittest discover tests

Covers exactly the three hardening behaviors so a future refactor
that weakens them fails CI instead of shipping silently:

  1. scaffold-new-qiskit.py rejects malformed MINOR/VERSION before
     touching the filesystem (subprocess, since the script acts at
     import time and has no main() guard).
  2. _SafeRedirectHandler in build-pages-data.py and build-admin-stats.py
     keeps same-host auth, strips Authorization on host change, and
     refuses an HTTPS->HTTP downgrade.
  3. The launch.js `image`-tag regex accepts real tags and rejects
     traversal / scheme / over-length inputs (kept in sync with
     docs/launch/launch.js by an explicit source check).
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import unittest
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / ".github" / "scripts"


def _load(mod_name: str, path: Path):
    """Import a main()-guarded script as a module (no side effects)."""
    spec = importlib.util.spec_from_file_location(mod_name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ScaffolderInputValidation(unittest.TestCase):
    """scaffold-new-qiskit.py must reject bad MINOR/VERSION and make
    no filesystem changes when it does."""

    SCRIPT = SCRIPTS / "scaffold-new-qiskit.py"

    def _run(self, minor: str, version: str):
        env = {**os.environ, "MINOR": minor, "VERSION": version}
        return subprocess.run(
            [sys.executable, str(self.SCRIPT)],
            env=env, capture_output=True, text=True,
            cwd=str(REPO_ROOT),
        )

    def test_rejects_path_traversal_minor(self):
        r = self._run("2.5/../../tmp/evil", "2.5.0")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MINOR must be X.Y", r.stderr + r.stdout)
        # No stray directory created from the traversal attempt.
        self.assertFalse((REPO_ROOT / "tmp").exists())

    def test_rejects_prerelease_version(self):
        r = self._run("2.5", "2.5.0rc1")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("VERSION must be X.Y.Z", r.stderr + r.stdout)

    def test_rejects_version_minor_mismatch(self):
        r = self._run("2.5", "3.0.0")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not within MINOR", r.stderr + r.stdout)

    def test_rejects_yaml_breaking_minor(self):
        r = self._run("2.5'\n  evil: x", "2.5.0")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MINOR must be X.Y", r.stderr + r.stdout)


class _FakeFP:
    def read(self, *_):
        return b""

    def close(self):
        pass


class SafeRedirectHandler(unittest.TestCase):
    """Both scripts' _SafeRedirectHandler must not leak the bearer
    across hosts and must refuse a scheme downgrade."""

    def _cases(self, handler_cls):
        h = handler_cls()

        def mk(url):
            return urllib.request.Request(
                url, headers={"Authorization": "Bearer SECRET", "Accept": "x"}
            )

        # same-host https: keep credential
        new = h.redirect_request(
            mk("https://ghcr.io/v2/x"), _FakeFP(), 302, "Found", {},
            "https://ghcr.io/v2/y",
        )
        self.assertIsNotNone(new)
        self.assertTrue(new.has_header("Authorization"))

        # cross-host https: strip credential
        new = h.redirect_request(
            mk("https://ghcr.io/v2/x"), _FakeFP(), 302, "Found", {},
            "https://evil.example/blob",
        )
        self.assertIsNotNone(new)
        self.assertFalse(new.has_header("Authorization"))

        # https -> http downgrade: refuse to follow at all
        new = h.redirect_request(
            mk("https://ghcr.io/v2/x"), _FakeFP(), 302, "Found", {},
            "http://ghcr.io/v2/y",
        )
        self.assertIsNone(new)

    def test_build_pages_data_handler(self):
        m = _load("_bpd", SCRIPTS / "build-pages-data.py")
        self._cases(m._SafeRedirectHandler)

    def test_build_admin_stats_handler(self):
        m = _load("_bas", SCRIPTS / "build-admin-stats.py")
        self._cases(m._SafeRedirectHandler)


class LaunchJsTagRegex(unittest.TestCase):
    """The image-tag allowlist in launch.js must accept real tags and
    reject hostile values. The pattern is duplicated here from the JS
    on purpose; a guard test asserts the JS still contains it so the
    two can't silently drift."""

    # Mirror of TAG_RE in docs/launch/launch.js
    TAG_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,40}$")
    LAUNCH_JS = REPO_ROOT / "docs" / "launch" / "launch.js"

    def test_regex_still_present_in_source(self):
        src = self.LAUNCH_JS.read_text()
        self.assertIn(
            r"/^[a-z0-9][a-z0-9._-]{0,40}$/", src,
            "launch.js TAG_RE changed — update this test to match, "
            "then re-verify the accept/reject cases below.",
        )

    def test_accepts_real_tags(self):
        for tag in ("latest-xl", "latest-small", "2.4-xxl",
                    "2.4-small", "1.4-xl", "a" * 41):
            self.assertRegex(tag, self.TAG_RE)

    def test_rejects_hostile_values(self):
        for bad in ("../../../@evil.example.com/", "foo/bar",
                    "javascript:alert(1)", "", "-leadingdash",
                    "a" * 42, "UPPER", "tag with space"):
            self.assertNotRegex(bad, self.TAG_RE)


if __name__ == "__main__":
    unittest.main()
