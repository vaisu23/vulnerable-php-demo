#!/usr/bin/env python3
"""Local structural checks for the PHP fixture; does not mimic the crew scanner."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

composer = json.loads((ROOT / "composer.json").read_text(encoding="utf-8-sig"))
lock = json.loads((ROOT / "composer.lock").read_text(encoding="utf-8-sig"))
assert composer["name"] == "demo/dependency-fix-crew-target"
assert isinstance(lock.get("packages"), list)
assert isinstance(lock.get("packages-dev"), list)

installed = {
    package["name"]: package["version"]
    for section in ("packages", "packages-dev")
    for package in lock[section]
}
assert installed.get("psr/log") == "3.0.2"

pinned = (ROOT / ".php-version").read_text(encoding="utf-8-sig").strip()
dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8-sig")
match = re.search(r"(?im)^FROM\s+php:(\d+\.\d+\.\d+)(?:-[^\s]+)?\s*$", dockerfile)
assert match, "Expected an explicit php:X.Y.Z image tag in the root Dockerfile"
assert pinned == match.group(1) == "8.3.31"
print(f"Fixture structure OK: PHP {pinned}; packages={installed}")
print("Note: this validates the fixture structure only, not Dependency Fix Crew behavior.")
