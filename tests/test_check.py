from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check  # noqa: E402 — the module lives in scripts/, which is not a package

INDEX = "| topic | Read |\n|---|---|\n| writing code | `code.md` |\n"


class CheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "references").mkdir()
        (self.root / "references" / "code.md").write_text("# Code\n")
        (self.root / "constitution.md").write_text(INDEX)
        (self.root / "AGENTS.md").write_text("# Guide\n")
        (self.root / "CLAUDE.md").symlink_to("AGENTS.md")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, text: str) -> None:
        (self.root / name).write_text(text)

    def test_a_coherent_tree_passes_every_check(self) -> None:
        self.write("SKILL.md", 'See `references/code.md`.\n\n```json\n{"a": 1}\n```\n')
        self.assertEqual([error for c in check.CHECKS for error in c(self.root)], [])

    def test_a_json_block_that_does_not_parse_fails(self) -> None:
        self.write("SKILL.md", '```json\n{"a": }\n```\n')
        [error] = check.invalid_json_blocks(self.root)
        self.assertIn("SKILL.md: JSON block does not parse", error)

    def test_a_path_to_a_missing_reference_fails(self) -> None:
        self.write("SKILL.md", "See `references/gone.md`.\n")
        self.assertEqual(
            check.missing_references(self.root), ["SKILL.md: names references/gone.md, which does not exist"]
        )

    def test_a_reference_missing_from_the_index_fails(self) -> None:
        (self.root / "references" / "docs.md").write_text("# Docs\n")
        self.assertEqual(check.index_mismatches(self.root), ["constitution.md: the reference index lacks docs.md"])

    def test_an_indexed_reference_that_does_not_exist_fails(self) -> None:
        (self.root / "references" / "code.md").unlink()
        self.assertEqual(
            check.index_mismatches(self.root), ["constitution.md: the reference index lists code.md, which does not exist"]
        )

    def test_a_guide_link_that_is_not_a_symlink_fails(self) -> None:
        (self.root / "CLAUDE.md").unlink()
        self.write("CLAUDE.md", "# Guide\n")
        self.assertEqual(check.broken_guide_link(self.root), ["CLAUDE.md: must be a symlink to AGENTS.md"])

    def test_main_exits_0_when_every_check_passes(self) -> None:
        self.assertEqual(check.main(self.root), 0)

    def test_main_prints_each_failure_and_exits_1(self) -> None:
        self.write("SKILL.md", "See `references/gone.md`.\n")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(check.main(self.root), 1)
        self.assertEqual(stderr.getvalue(), "SKILL.md: names references/gone.md, which does not exist\n")


if __name__ == "__main__":
    unittest.main()
