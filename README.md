# best-software

An agent skill that holds an engineering constitution (values, hard constraints, decision rules) and the procedures to
bootstrap a software project, score an existing one against that constitution, raise it, or publish it.

## Install
Clone it to `~/.agents/skills/best-software`:

```sh
git clone https://github.com/alvaromr/best-software.git ~/.agents/skills/best-software
```

Agents that read skills from `~/.claude/skills` find it when
that folder links to `~/.agents/skills`. Then tell the always-loaded agent instructions, such as `~/.claude/CLAUDE.md`,
to read `constitution.md` once per session in any software task.

## Use
In a project, call the skill with the operation you want:

| Command | What it does |
|---|---|
| `/best-software score` | Scores the project out of 10, per section, and lists what to fix first. Changes nothing. |
| `/best-software elevate` | Scores it, fixes it in small commits with the checks green, and scores it again. |
| `/best-software publish` | Elevates it for publication, then releases and publishes it after your yes. |
| `/best-software bootstrap` | Starts a new project with the gate, hooks and a first working path before any feature. |

The slash form is Claude Code's; in other agents, ask in words, such as "score this project with the best-software
skill". Each run is recorded in a private `.best-software.json`.

## What it asks of a project
The bar does not shrink with project size, even for a small script: what never scales down is the "Never scales
down" column in `SKILL.md`, "Profile the project". Scores are orientative (`score.md`).

## License
MIT, in `LICENSE`.

## Contributing
Working on the skill itself: `AGENTS.md`.
