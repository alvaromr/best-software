# best-software

An agent skill that holds an engineering constitution (values, hard constraints, decision rules) and the procedures to
bootstrap a software project, raise an existing one, or score it against that constitution.

## Install
Place this folder at `~/.agents/skills/best-software`. Agents that read skills from `~/.claude/skills` find it when
that folder links to `~/.agents/skills`. Then tell the always-loaded agent instructions, such as `~/.claude/CLAUDE.md`,
to read `constitution.md` once per session in any software task.

## Use
Ask the agent to start a project, audit or raise one, or score one. The entry point is `SKILL.md`.

## Next
Working on the skill itself: `AGENTS.md`.
