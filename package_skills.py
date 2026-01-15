#!/usr/bin/env python3
"""
Package skill folders under ./skills into .skill files in ./mindm/skills.

Usage:
  python package_skills.py
  python package_skills.py --output-dir mindm/skills --skills-dir skills
  python package_skills.py --only mindm-export mindm-mindmap
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

IGNORED_NAMES = {".DS_Store", "__pycache__", ".git", ".pytest_cache"}


def should_ignore(path: Path) -> bool:
    return any(part in IGNORED_NAMES for part in path.parts)


def find_skill_dirs(skills_dir: Path, only: list[str]) -> list[Path]:
    if not skills_dir.exists():
        raise FileNotFoundError(f"skills directory not found: {skills_dir}")

    skill_dirs = []
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        if only and child.name not in only:
            continue
        if (child / "SKILL.md").exists():
            skill_dirs.append(child)
    return skill_dirs


def package_skill(skill_dir: Path, output_dir: Path, quiet: bool) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{skill_dir.name}.skill"

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if should_ignore(file_path):
                continue
            arcname = file_path.relative_to(skill_dir.parent)
            zipf.write(file_path, arcname)

    if not quiet:
        print(f"Packaged {skill_dir.name} -> {output_path}")

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Package skills into .skill files.",
    )
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Directory containing skill folders (default: skills).",
    )
    parser.add_argument(
        "--output-dir",
        default="mindm/skills",
        help="Output directory for .skill files (default: mindm/skills).",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Optional list of skill folder names to package.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-skill output.",
    )
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    output_dir = Path(args.output_dir)
    only = [name.strip() for name in args.only if name.strip()]

    try:
        skill_dirs = find_skill_dirs(skills_dir, only)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    found_names = {skill_dir.name for skill_dir in skill_dirs}
    missing = sorted(set(only) - found_names)
    if missing:
        print(f"Error: skill(s) not found: {', '.join(missing)}", file=sys.stderr)
        return 1

    if not skill_dirs:
        print(f"Error: no skills found in {skills_dir}", file=sys.stderr)
        return 1

    for skill_dir in skill_dirs:
        package_skill(skill_dir, output_dir, args.quiet)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
