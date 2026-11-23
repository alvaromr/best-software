---
name: best-software
description: Procedures to bootstrap a new software project at professional quality, to audit and raise an existing one, to score one, or to publish one (architecture, tests with TDD/100 % coverage/mutation, tooling, repo, docs, git, release, security, UI). Use when asked to start a project, make it professional or publishable, review or score its quality, or apply best practices. Not for CI/CD pipeline design.
---

# Best software — procedures

The values, hard constraints and decision rules are in `constitution.md`; read it first if this session has not. The
detailed practices are in `references/` (index in the constitution). This skill adds only the end-to-end procedures.

## Operations
Called with an argument, the skill runs that operation; with none, the agent picks the one the request names.

| Argument | Procedure |
|---|---|
| `bootstrap` | `bootstrap.md`: start a new project |
| `score` | `score.md`: measure a project, changing nothing |
| `elevate` | `elevate.md`: score, fix, and score again |
| `publish` | `publish.md`: elevate for publication, release, and publish after the owner's yes |

Each operation contains the one before it: elevate starts and ends with a score, and publish is elevate with the
profile set to be published. Read only the files of the operation you run. *Why:* the skill is loaded piecemeal, and
one name per entry point keeps every run on the same procedure.

## Profile the project
Before changing anything, establish these facts and state them in one short block. *Why:* every judgment call below
depends on them.
- **Purpose and audience:** who runs it, who reads the code, whether it is public, and whether it is to be published
  or shared, and where.
- **If it is to be published or shared:** ask the owner once, before any other step, for the publish decisions
  (licence, name, visibility, whether to rewrite or squash the history, initial version) and for the names linked to
  them to search for (company, clients, people, ticket keys, domains). Keep those names in the owner's user-level
  configuration, never in the repo. *Why:* these choices are the owner's and block publication, so one question
  avoids a run that stops at each; the names are private by definition, and only the owner knows them.
- **Kind:** script or CLI, library or SDK, service or backend, app (web, mobile, desktop, extension), game or
  simulation, data or ML.
- **Stack and runtime versions.** For an existing project, also read its current gate, tests, coverage and conventions.
- **Constraints:** frozen legacy, team conventions, deadlines, platforms, compliance (privacy, data residency).
- **Previous runs:** if the repo root has `.best-software.json` (Run record, below), list this skill's commits since
  the last run's `skill_commit` (`git log --oneline <sha>..HEAD` in the skill's folder), and report those that
  require updating the project.

Then decide which practices apply, and how strictly. The right-hand column protects safety, correctness and truth,
which do not shrink with project size:

| Scales with the profile | Never scales down |
|---|---|
| number of layers and modules; DI framework or plain constructors | pure core separated from I/O |
| containers, deploy hooks, health endpoints (services only) | one source of truth; testable seams at the boundaries |
| structured logging depth, metrics | gate: format, lint, strict types, tests, 100 % coverage |
| web and authorization hardening (exposure-dependent) | mutation testing on the core |
| ADRs, runbooks, SECURITY/PRIVACY docs | no secrets in repo or history; validated input; loopback binding when local |
| i18n resources once a second language is planned | real names, typed signatures, no silent failures |
| assistive-tech verification depth | keyboard and contrast basics |
| comment density; docstrings in a public library | README + AGENTS.md, `.gitignore`, lockfile |
| folder depth | docs single-sourced and coherent |
| release channel and packaging | single version source, changelog, immutable tags |
| | scripted release, clean-environment install test |

## Run record (`.best-software.json`)
Every procedure, scoring included, appends one run to `.best-software.json` at the repository root, as its last
step before any report; only a reused score appends none (`score.md`, "Procedure"). *Why:* it marks that the skill
was applied, with which procedure and which skill version, so a later run knows what changed since.
- **Private:** add `.best-software.json` to the project's `.gitignore`, unless it is already there, in a commit of its
  own. The record stays uncommitted, and formatters, linters and scanners that read `.gitignore` skip it. When the
  project builds a package, check that the record is not in it. *Why:* the record is the skill's notes, not part of
  the project, so the project's tools should not judge it; `.gitignore` is where a project lists the files that are
  not its own, and most tools read it. A build tool may still pack files git does not track, hence the package check.
- **Not a git repo:** write it at the project root, with `commit` and `clean_tree` as `null`, and say that nothing
  excludes it.
- **History:** append each run to `runs`, newest last; never rewrite earlier runs. *Why:* later runs compare against
  them, so a rewritten run hides what changed.
- **Skill version:** the date and sha of the skill's HEAD commit, and whether its tree was clean. *Why:* the skill
  changes continuously, so a date reads at a glance where a version number would need a release process.

```json
{
  "note": "Private record of best-software runs. Scores are orientative and can vary between runs on the same code.",
  "runs": [
    {
      "date": "<ISO 8601, UTC>",
      "procedure": "bootstrap | elevate | publish | score",
      "commit": "<project HEAD sha>",
      "clean_tree": true,
      "skill_date": "<the skill's HEAD commit date, ISO 8601>",
      "skill_commit": "<the skill's HEAD sha>",
      "skill_clean_tree": true,
      "model": "<model id>",
      "summary": "<one line: what the run did>"
    }
  ]
}
```

## Reports
Every report is written in the owner's language, translating the template of its procedure. *Why:* the owner reads
the report to decide what to do next.

## Project guide template (`AGENTS.md`, with `CLAUDE.md` as a symlink)
The guide is part of the code, agnostic of the individual developer (`references/repository.md`). It is
self-contained, so teammates without this skill can follow it. It holds only what tooling
cannot express, and points to files instead of copying them. Non-negotiables carry their reason in one line, so
contributors can apply them with judgment.

```markdown
# <Project>
<One line: what it is and for whom.>

## Commands
<gate, fix, test, coverage, mutation, run, build, release — one line each, pointing to the task runner>

## Architecture
<core vs adapters, module map, the dependency rule and how it is enforced>

## Non-negotiables
<rule — why, one line each: gate before commit, TDD, coverage threshold, English, no secrets, commit convention,
everything kept coherent in the same change, …>

## Decisions
Before changing a practice, read `docs/decisions/`.

## Where things live
<pointers: docs/, runbooks, env template, changelog>
```
