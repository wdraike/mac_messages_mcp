# Copyright (c) 2023 Carter Lasalle
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    match = re.search(r'^version = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M)
    assert match
    return match.group(1)


def test_manifest_matches_pyproject() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["version"] == _project_version()


def test_memory_bank_current_version_matches_pyproject() -> None:
    text = (ROOT / "memory-bank" / "activecontext.md").read_text()
    match = re.search(r"\*\*Current Version\*\*: (\d+\.\d+\.\d+)", text)
    assert match, "activecontext.md has no Current Version line"
    assert match.group(1) == _project_version()


def test_memory_bank_has_no_known_stale_release_strings() -> None:
    version = _project_version()
    for name in ("activecontext.md", "techcontext.md"):
        text = (ROOT / "memory-bank" / name).read_text()
        assert "(version 0.7.3)" not in text, name
        assert "Updated to 0.7.3" not in text, name


def test_techcontext_has_current_version_section() -> None:
    text = (ROOT / "memory-bank" / "techcontext.md").read_text()
    match = re.search(r"## Current Version\n- \*\*(\d+\.\d+\.\d+)\*\*", text)
    assert match, "techcontext.md has no Current Version section"
    assert match.group(1) == _project_version()
