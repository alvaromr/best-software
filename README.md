# best-software

An agent skill that holds an engineering constitution (values, hard constraints, decision rules) and the procedures to
bootstrap a software project, raise an existing one, or score it against that constitution.

## Install
Clone it to `~/.agents/skills/best-software`:

```sh
git clone https://github.com/alvaromr/best-software.git ~/.agents/skills/best-software
```

Agents that read skills from `~/.claude/skills` find it when
that folder links to `~/.agents/skills`. Then tell the always-loaded agent instructions, such as `~/.claude/CLAUDE.md`,
to read `constitution.md` once per session in any software task.

## Use
Ask the agent to start a project, audit or raise one, or score one. The entry point is `SKILL.md`.

## Example
In a project, ask: "Score this project with the best-software skill." The agent reads the code and runs its checks
without changing anything, then reports a global score out of 10, one score per section with its main signal, and a
list of what to fix first with the points each fix recovers. Ask "Elevate this project with the best-software skill"
and it scores first, fixes in small commits with the checks green, and scores again to show the change. Each run is
recorded in a private `.best-software.json`.

## What it asks of a project
The bar does not shrink with project size, even for a small script: what never scales down is the "Never scales
down" column in `SKILL.md`, Step 1. Scores are orientative (`score.md`).

## License
MIT, in `LICENSE`.

## Contributing
Working on the skill itself: `AGENTS.md`.
