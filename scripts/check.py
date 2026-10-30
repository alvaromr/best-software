"""Mechanical coherence checks over the skill's Markdown files.

Run through the gate, `scripts/check.sh`. Exits 1 and lists every failure when a check fails.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

JSON_BLOCK = re.compile(r"^```json\n(.*?)^```$", re.MULTILINE | re.DOTALL)
REFERENCE_PATH = re.compile(r"references/([a-z-]+\.md)")
INDEX_ROW = re.compile(r"^\|.*\| `([a-z-]+\.md)` \|$", re.MULTILINE)


def markdown_files(root: Path) -> list[Path]:
    return sorted([*root.glob("*.md"), *root.glob("references/*.md")])


def invalid_json_blocks(root: Path) -> list[str]:
    errors = []
    for path in markdown_files(root):
        for block in JSON_BLOCK.findall(path.read_text()):
            try:
                json.loads(block)
            except json.JSONDecodeError as error:
                errors.append(f"{path.relative_to(root)}: JSON block does not parse: {error}")
    return errors


def missing_references(root: Path) -> list[str]:
    errors = []
    for path in markdown_files(root):
        for name in sorted(set(REFERENCE_PATH.findall(path.read_text()))):
            if not (root / "references" / name).is_file():
                errors.append(f"{path.relative_to(root)}: names references/{name}, which does not exist")
    return errors


def index_mismatches(root: Path) -> list[str]:
    indexed = set(INDEX_ROW.findall((root / "constitution.md").read_text()))
    present = {path.name for path in root.glob("references/*.md")}
    return [f"constitution.md: the reference index lacks {name}" for name in sorted(present - indexed)] + [
        f"constitution.md: the reference index lists {name}, which does not exist" for name in sorted(indexed - present)
    ]


def broken_guide_link(root: Path) -> list[str]:
    link = root / "CLAUDE.md"
    if link.is_symlink() and link.readlink() == Path("AGENTS.md"):
        return []
    return ["CLAUDE.md: must be a symlink to AGENTS.md"]


CHECKS = (invalid_json_blocks, missing_references, index_mismatches, broken_guide_link)


def main(root: Path = Path(__file__).resolve().parent.parent) -> int:
    errors = [error for check in CHECKS for error in check(root)]
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
