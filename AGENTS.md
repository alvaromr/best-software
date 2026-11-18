# best-software
An agent skill: the engineering constitution and the procedures that apply it, for agents and their owners.

## Commands
- Gate: `scripts/check.sh`. It runs the mechanical tests over the Markdown; Python 3 standard library only, on any
  supported version. Adding a test: `references/testing.md`.
- Hooks: the pre-commit hook runs the gate on the staged files, the commit-msg hook checks the subject
  (`references/git.md`), and the gate's first run in a clone installs both.
- The gate cannot judge meaning. A change to a procedure is verified by running it on a real project.

## Architecture
- `SKILL.md`: the entry point and the bootstrap and elevate procedures.
- `constitution.md`: values, hard constraints, decision rules and the index of references.
- `score.md`: the scoring procedure.
- `references/`: one practice file per topic, each practice with its *Why*; `toolchains.md` holds the concrete tools.
- `tests/test_skill.py`: the mechanical tests.
- The installed skill is this working tree, so uncommitted edits are live for every agent at once.

## Non-negotiables
- The constitution governs this repo too — the skill must meet the bar it sets.
- English in every file — the agent translates the report templates into the owner's language.
- Each practice states its *Why* — agents apply it with judgment only when they know the reason.
- Tools and their versions appear only in `references/toolchains.md` — tools change faster than practices.
- One term per concept across all files — two names for one thing read as two things.
- A change updates every file it affects in the same commit — the skill is loaded piecemeal, so any stale file
  misleads.
- A change to what the skill asks of agents adds a line to `CHANGELOG.md` under its date — users learn what changed
  for their agents without reading the history.

## Decisions
Before changing a practice, read `docs/decisions/` (none yet).

## Where things live
- Install and use: `README.md`.
