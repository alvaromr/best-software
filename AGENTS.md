# best-software
An agent skill: the engineering constitution and the procedures that apply it, for agents and their owners.

## Commands
- Gate: `scripts/check.sh`. It runs the mechanical tests over the Markdown; Python 3 standard library only, on
  any supported version. Adding a test: `references/testing.md`.
- Hooks: the pre-commit hook runs the gate on the staged files, the commit-msg hook checks the subject
  (`references/git.md`), and the gate's first run in a clone installs both.
- The gate cannot judge meaning. A change to a procedure is verified by running it on a real project, and by the
  evals in `evals/`, each when its README says it applies.
- Eval setup: `scripts/eval-setup.sh <eval> <directory>` commits an eval's example project in a new directory.

## Architecture
- `SKILL.md`: the entry point: the operations, and what they share (profile, run record, reports, guide template).
- `bootstrap.md`, `score.md`, `elevate.md`, `publish.md`: one file per operation.
- `constitution.md`: values, hard constraints, decision rules and the index of references.
- `references/`: one practice file per topic, each practice with its *Why*; `toolchains.md` holds the concrete tools.
- `tests/`: the mechanical tests, in `test_skill.py`, over the Markdown.
- `evals/`: one folder per operation (`bootstrap`, `elevate`, `publish`, `score`), each with its example project where
  it needs one, and what running the procedure must produce.
- The installed skill is this working tree, so uncommitted edits are live for every agent at once.

## Non-negotiables
- The constitution governs this repo too — the skill must meet the bar it sets.
- English in every file, report templates included — the constitution's "Language of artifacts".
- Each practice states its *Why* — agents apply it with judgment only when they know the reason.
- "Never" and "always" only where no exception holds, with a *Why* that says why none does (the gate checks it) —
  an absolute without its reason is applied where it no longer fits, or dropped as arbitrary.
- Tools and their versions appear only in `references/toolchains.md` — tools change faster than practices.
- One term per concept across all files — two names for one thing read as two things.
- A change updates every file it affects in the same commit — the skill is loaded piecemeal, so any stale file
  misleads.
- A change to what the skill asks of agents adds a line to `CHANGELOG.md` under its date — users learn what changed
  for their agents without reading the history.

## Decisions
Before changing a practice, read `docs/decisions/`.

## Where things live
- Install and use: `README.md`.
- Issue and pull-request templates: `.github/`.
