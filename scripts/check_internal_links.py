#!/usr/bin/env python3
"""Check local Markdown links, empty files, and unfinished scaffold markers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
UNFINISHED_PATTERN = re.compile(r"\[(?:TODO|TBD)\]|\b(?:TODO|TBD)\b", re.IGNORECASE)
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def check_skill_frontmatter(skill: Path, expected_name: str, errors: list[str]) -> None:
    if not skill.is_file():
        errors.append(f"missing {skill.name}")
        return
    text = skill.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        errors.append(f"{skill.name}: missing or malformed YAML frontmatter")
        return
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{skill.name} frontmatter: malformed line '{line}'")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    unexpected = set(fields) - {"name", "description", "license", "allowed-tools", "metadata"}
    if unexpected:
        errors.append(f"{skill.name} frontmatter: unexpected keys {sorted(unexpected)}")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != expected_name or not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append(f"{skill.name} frontmatter: invalid name")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        errors.append(f"{skill.name} frontmatter: invalid description")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    check_skill_frontmatter(root / "SKILL.md", "cultural-event-poster", errors)
    check_skill_frontmatter(root / "SKILL.en.md", "cultural-event-poster", errors)

    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.stat().st_size == 0:
            errors.append(f"empty file: {path.relative_to(root)}")
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8-sig")
        if UNFINISHED_PATTERN.search(text):
            errors.append(f"unfinished marker: {path.relative_to(root)}")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "/")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"link escapes skill root: {path.relative_to(root)} -> {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"broken link: {path.relative_to(root)} -> {raw_target}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: links, empty files, and unfinished markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
