"""Mechanical coherence tests over the skill's Markdown files. The gate, `scripts/check.sh`, runs them."""

from __future__ import annotations

import json
import re
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_BLOCK = re.compile(r"^```json\n(.*?)^```$", re.MULTILINE | re.DOTALL)
REFERENCE_PATH = re.compile(r"references/([a-z-]+\.md)")
INDEX_ROW = re.compile(r"^\|.*\| `([a-z-]+\.md)` \|$", re.MULTILINE)
MAX_LINE_LENGTH = 120
AUDIT_SIGNALS = re.compile(r"^## Audit signals\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
DEFAULT_VALUE = re.compile(r" `(safety|correctness|truth|changeability|simplicity|efficiency)`$")
SECTION_POINTER = re.compile(r'(?:`(?:references/)?([a-zA-Z-]+\.md)`, |\b(constitution)(?:\'s|,) )"([^"]+)"')
PRACTICES = re.compile(r"^## (?!Judgment|Audit signals).*?\n(.*?)(?=^## Judgment|\Z)", re.MULTILINE | re.DOTALL)
PRACTICE = re.compile(r"^- \*\*.*?(?=^- \*\*|^#|\Z)", re.MULTILINE | re.DOTALL)
TOOL_VERSION = re.compile(r"\b([A-Za-z][\w-]*) v?\d+\.\d+|\b[\w-]+@\d")
NOT_A_TOOL = {"at", "most", "below", "WCAG"}
SPANISH = re.compile(r"[áéíóúñü¿¡ÁÉÍÓÚÑÜ]")
DATED_HEADING = re.compile(r"^## (.*)$", re.MULTILINE)


def markdown_files() -> list[Path]:
    return sorted([*ROOT.glob("*.md"), *ROOT.glob("references/*.md"), *ROOT.glob("evals/**/*.md")])


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

    def test_every_audit_signal_ends_with_its_default_value(self) -> None:
        missing = [
            f"{path.relative_to(ROOT)}: {line}"
            for path in sorted(ROOT.glob("references/*.md"))
            for section in AUDIT_SIGNALS.findall(path.read_text())
            for line in section.splitlines()
            if line.startswith("- ") and not DEFAULT_VALUE.search(line)
        ]
        self.assertEqual(missing, [])

    def test_every_named_section_exists(self) -> None:
        missing = []
        for path in markdown_files():
            for file, _, section in SECTION_POINTER.findall(path.read_text()):
                # A pointer names a file next to the one that holds it, or else one at the root.
                nearby = path.parent / file
                target = nearby if file and nearby.is_file() else ROOT / (file or "constitution.md")
                lines = target.read_text().splitlines()
                headings = [line.lstrip("#").strip() for line in lines if line.startswith("#")]
                section = " ".join(section.split())
                if not any(heading.startswith(section) for heading in headings):
                    missing.append(f"{path.relative_to(ROOT)}: {target.name}, {section!r}")
        self.assertEqual(missing, [])

    def test_each_audit_signal_is_listed_in_one_reference_only(self) -> None:
        owners: dict[str, list[str]] = {}
        for path in sorted(ROOT.glob("references/*.md")):
            for section in AUDIT_SIGNALS.findall(path.read_text()):
                for line in section.splitlines():
                    if line.startswith("- "):
                        owners.setdefault(DEFAULT_VALUE.sub("", line).lower(), []).append(path.name)
        self.assertEqual({signal: files for signal, files in owners.items() if len(files) > 1}, {})

    def test_every_practice_states_its_why(self) -> None:
        missing = [
            f"{path.relative_to(ROOT)}: {practice.splitlines()[0][:60]}"
            for path in sorted(ROOT.glob("references/*.md"))
            if path.name != "toolchains.md"
            for body in PRACTICES.findall(path.read_text())
            for practice in PRACTICE.findall(body)
            if "*Why:*" not in practice
        ]
        self.assertEqual(missing, [])

    def test_tool_versions_appear_only_in_the_toolchains_reference(self) -> None:
        found = [
            f"{path.relative_to(ROOT)}:{number}: {match.group(0)}"
            for path in markdown_files()
            if path.name != "toolchains.md"
            for number, line in enumerate(path.read_text().splitlines(), 1)
            for match in TOOL_VERSION.finditer(line)
            if match.group(1) not in NOT_A_TOOL
        ]
        self.assertEqual(found, [])

    def test_every_file_is_in_english(self) -> None:
        found = [
            f"{path.relative_to(ROOT)}:{number}"
            for path in markdown_files()
            for number, line in enumerate(path.read_text().splitlines(), 1)
            if SPANISH.search(line)
        ]
        self.assertEqual(found, [])

    def test_the_changelog_is_dated_newest_first(self) -> None:
        headings = DATED_HEADING.findall((ROOT / "CHANGELOG.md").read_text())
        for heading in headings:
            date.fromisoformat(heading)
        self.assertEqual(headings, sorted(set(headings), reverse=True))

    def test_claude_md_is_a_symlink_to_agents_md(self) -> None:
        link = ROOT / "CLAUDE.md"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.readlink(), Path("AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
