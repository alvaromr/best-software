"""Mechanical coherence tests over the skill's Markdown files. The gate, `scripts/check.sh`, runs them."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_BLOCK = re.compile(r"^```json\n(.*?)^```$", re.MULTILINE | re.DOTALL)
REFERENCE_PATH = re.compile(r"references/([a-z-]+\.md)")
INDEX_ROW = re.compile(r"^\|.*\| `([a-z-]+\.md)` \|$", re.MULTILINE)
MAX_LINE_LENGTH = 120


def markdown_files() -> list[Path]:
    return sorted([*ROOT.glob("*.md"), *ROOT.glob("references/*.md")])


class SkillTest(unittest.TestCase):
    def test_every_json_block_parses(self) -> None:
        errors = []
        for path in markdown_files():
            for block in JSON_BLOCK.findall(path.read_text()):
                try:
                    json.loads(block)
                except json.JSONDecodeError as error:
                    errors.append(f"{path.relative_to(ROOT)}: {error}")
        self.assertEqual(errors, [])

    def test_every_named_reference_exists(self) -> None:
        missing = [
            f"{path.relative_to(ROOT)}: references/{name}"
            for path in markdown_files()
            for name in sorted(set(REFERENCE_PATH.findall(path.read_text())))
            if not (ROOT / "references" / name).is_file()
        ]
        self.assertEqual(missing, [])

    def test_the_constitution_indexes_exactly_the_references(self) -> None:
        indexed = set(INDEX_ROW.findall((ROOT / "constitution.md").read_text()))
        present = {path.name for path in ROOT.glob("references/*.md")}
        self.assertEqual(indexed, present)

    def test_no_markdown_line_passes_the_maximum_length(self) -> None:
        too_long = []
        for path in markdown_files():
            lines = path.read_text().splitlines()
            # The YAML frontmatter is not Markdown, so it is exempt.
            start = lines.index("---", 1) + 1 if lines[:1] == ["---"] else 0
            too_long += [
                f"{path.relative_to(ROOT)}:{number}"
                for number, line in enumerate(lines[start:], start + 1)
                if len(line) > MAX_LINE_LENGTH
            ]
        self.assertEqual(too_long, [])

    def test_claude_md_is_a_symlink_to_agents_md(self) -> None:
        link = ROOT / "CLAUDE.md"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.readlink(), Path("AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
