"""Tests of `scripts/eval-setup.sh`, the task that prepares an eval's example project."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "eval-setup.sh"
# A fixed identity, so the commit does not depend on the git config of whoever runs the gate.
IDENTITY = {
    "GIT_AUTHOR_NAME": "Eval", "GIT_AUTHOR_EMAIL": "eval@example.invalid",
    "GIT_COMMITTER_NAME": "Eval", "GIT_COMMITTER_EMAIL": "eval@example.invalid",
}
MESSAGES = {
    "elevate": "Add the example",
    "publish": "Add the route planner for Acme Logistics",
    "score": "Add the example",
}


# The variables that point git at one repo, such as GIT_DIR and GIT_INDEX_FILE, which a hook running the gate sets.
REPO_VARIABLES = subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True, text=True).stdout.split()
CLEAN_ENV = {key: value for key, value in os.environ.items() if key not in REPO_VARIABLES}


def run(
    *args: str | Path, cwd: Path | None = None, env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(arg) for arg in args], cwd=cwd, env={**CLEAN_ENV, **IDENTITY, **(env or {})}, capture_output=True,
        text=True,
    )


def git(directory: Path, *args: str) -> str:
    return run("git", *args, cwd=directory).stdout.strip()


class EvalSetupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parent = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.parent)

    def test_each_eval_with_a_project_gets_it_committed_alone_with_its_message(self) -> None:
        self.assertEqual(sorted(path.parent.name for path in ROOT.glob("evals/*/project")), sorted(MESSAGES))
        for name, message in MESSAGES.items():
            with self.subTest(name):
                target = self.parent / name
                result = run(SCRIPT, name, target)
                self.assertEqual(result.returncode, 0, result.stderr)
                project = sorted(path.name for path in (ROOT / "evals" / name / "project").iterdir())
                self.assertEqual(git(target, "ls-files").splitlines(), project)
                self.assertEqual(git(target, "log", "--format=%s"), message)
                self.assertEqual(git(target, "status", "--porcelain"), "")
                self.assertEqual(git(target, "remote"), "")

    def test_git_variables_inherited_from_another_repo_leave_that_repo_untouched(self) -> None:
        other = self.parent / "other"
        other.mkdir()
        run("git", "init", "--quiet", cwd=other)
        run("git", "commit", "--quiet", "--allow-empty", "-m", "Keep this history", cwd=other)
        inherited = {"GIT_DIR": str(other / ".git"), "GIT_INDEX_FILE": str(other / ".git" / "index")}
        result = run(SCRIPT, "score", self.parent / "score", env=inherited)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git(other, "log", "--format=%s"), "Keep this history")
        self.assertEqual(git(self.parent / "score", "log", "--format=%s"), "Add the example")

    def test_a_directory_that_is_not_empty_is_refused(self) -> None:
        (self.parent / "kept").write_text("owner's work\n")
        result = run(SCRIPT, "score", self.parent)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not empty", result.stderr)
        self.assertEqual(sorted(path.name for path in self.parent.iterdir()), ["kept"])

    def test_a_directory_inside_this_repo_is_refused(self) -> None:
        target = ROOT / "evals" / "score" / "eval-setup-test"
        result = run(SCRIPT, "score", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside this repo", result.stderr)
        self.assertFalse(target.exists())

    def test_an_eval_without_a_project_is_refused(self) -> None:
        for name in ("bootstrap", "missing"):
            with self.subTest(name):
                result = run(SCRIPT, name, self.parent / name)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("no example project", result.stderr)
                self.assertFalse((self.parent / name).exists())


if __name__ == "__main__":
    unittest.main()
