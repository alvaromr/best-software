# best-software
An agent skill: the engineering constitution and the procedures that apply it, for agents and their owners.

## Commands
- Gate: `scripts/check.sh`. It runs the mechanical tests over the Markdown; Python 3 standard library only. A new
  test proves itself by failing once on a known violation (`references/testing.md`).
- Hook: the pre-commit hook runs the gate, and the gate's first run in a clone installs the hook.
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
- English in every file except the Spanish report templates — they are user-facing copy for the owner.
- Each practice states its *Why* — agents apply it with judgment only when they know the reason.
- Tools and their versions appear only in `references/toolchains.md` — tools change faster than practices.
- One term per concept across all files — two names for one thing read as two things.
- A change updates every file it affects in the same commit — the skill is loaded piecemeal, so any stale file
  misleads.

## Decisions
Before changing a practice, read `docs/decisions/` (none yet).

## Where things live
- Install and use: `README.md`.
