# best-software

An agent skill that holds an engineering constitution (values, hard constraints, decision rules) and the procedures to
bootstrap a software project, raise an existing one, or score it against that constitution.

## Install
Place this folder at `~/.agents/skills/best-software`. Agents that read skills from `~/.claude/skills` find it when
that folder links to `~/.agents/skills`. Then tell the always-loaded agent instructions, such as `~/.claude/CLAUDE.md`,
to read `constitution.md` once per session in any software task.

## Use
Ask the agent to start a project, audit or raise one, or score one. The entry point is `SKILL.md`.

## What it asks of a project
The bar does not shrink with project size. Even a small script gets a pure core apart from its I/O, a gate with
strict types and 100 % coverage, mutation testing on the core, and features built test-first. The full list is the
"Never scales down" column in `SKILL.md`, Step 1. Scores are orientative: an agent assigns them, so two runs on the
same code can differ. Reports follow templates in Spanish, which the agent translates into the owner's language.

## Next
Working on the skill itself: `AGENTS.md`.
