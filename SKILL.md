---
name: best-software
description: Procedures to bootstrap a new software project at professional quality, to audit and raise an existing one, or to score one (architecture, tests with TDD/100 % coverage/mutation, tooling, repo, docs, git, release, security, UI). Use when asked to start a project, make it professional or publishable, review or score its quality, or apply best practices. Not for CI/CD pipeline design.
---

# Best software — procedures

The values, hard constraints and decision rules are in `constitution.md`; read it first if this session has not. The
detailed practices are in `references/` (index in the constitution). This skill adds only the end-to-end procedures.
To score a project, follow `score.md`.

## Step 1 — Profile the project
Before changing anything, establish these facts and state them in one short block. *Why:* every judgment call below
depends on them.
- **Purpose and audience:** who runs it, who reads the code, and whether it is public.
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

## Step 2a — Bootstrap a new project
1. **Agree on the profile and the shape of the core:** the domain modules and the adapters at the edges.
2. **Scaffold the repository** (`references/repository.md`):
   - layout
   - root files
   - `.gitignore`, `.editorconfig`
   - toolchain pin and lockfile
   - env template if needed
3. **Install the gate, its hooks and the mutation config before any feature** (`references/tooling.md`, "The
   gate"; `references/testing.md`; `references/toolchains.md`). *Why:* quality added later means fixing a backlog;
   installed first, it means never creating one.
4. **Write a walking skeleton:** one end-to-end path through core and adapter, with its tests, and the gate green.
   *Why:* it proves the architecture and the gate before features depend on them.
5. **Write the project guide** (template below) and the README.
6. **Make the first commit:** the skeleton, green, in the agreed convention.
7. **Build every feature test-first** (`references/testing.md`), one atomic commit per step (`references/git.md`).
   Each commit passes the coherence review (`references/docs.md`, "Content rules").
8. **Add release artifacts** (`references/release.md`) once something is distributable.
9. **Record the run** (Run record, below).

## Step 2b — Elevate an existing project
1. **Prepare the branch:**
   - **If the project is a git repo:** check that the tree is clean. If it is dirty, stop and ask (hard constraint 7).
     Then update the default branch. If the project integrates through pull requests (`references/git.md`), create
     a clean branch from it (`chore/engineering-baseline`, or one per topic).
   - **If the project is not a git repo:** ask whether to initialise one before changing anything. Otherwise, deliver
     the assessment only.
2. **Measure the baseline.** *Why:* without a "before" there is no proof of improvement, and no way to spot a
   regression.
   - Run the existing build and tests. Record each failure they already have as the baseline: until it is fixed,
     the gate fails only on new failures (hard constraint 3).
   - Record coverage, lint and type findings, the dependency audit, and the outdated dependencies and
     toolchain pins.
   - Note what is unknown.
3. **Assess every topic** against its reference's practices, its audit signals first. Rank the findings by the
   constitution's value order.
4. **Fix directly, in this order.** Each step is its own atomic commit with the gate green. *Why:* the order builds the
   safety net before anything that could break.
   1. Safety net: characterization tests around anything you will touch.
   2. Gate and hooks, as a ratchet on legacy code (`references/tooling.md`).
   3. Secrets and security fixes. A leaked secret is reported to the owner at once, for rotation.
   4. Repository hygiene and toolchain pin.
   5. Structure and code refactors, under tests, with no behaviour change.
   6. Tests up to the coverage and mutation targets.
   7. Docs and the project guide.
   8. Release artifacts.
5. **Behaviour is frozen during the pass** (hard constraint 6). When you find a real bug:
   - **If the fix is safe:** fix it in its own `fix:` commit with a reproducing test.
   - **Otherwise:** report it.

   Ask before any change the constitution's "How to decide" leaves to the owner.
6. **Verify:**
   1. Run the full gate.
   2. Run the app, CLI or package as a user would.
   3. Run the coherence review over the whole repo, and fix whatever disagrees.
7. **Record the run** (below).
8. **Report** in the format below.

## Run record (`.best-software.json`)
Every procedure, scoring included, appends one run to `.best-software.json` at the repository root, as its last
step before any report; only a reused score appends none (`score.md`, "Procedure"). *Why:* it marks that the skill
was applied, with which procedure and which skill version, so a later run knows what changed since.
- **Private:** add `.best-software.json` to the file that `git rev-parse --git-path info/exclude` names, unless it is
  already there. The record stays uncommittable without touching the project's `.gitignore`.
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
      "procedure": "bootstrap | elevate | score",
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

## Report format (elevate mode)
Every report is written in the owner's language, translating the templates here and in `score.md`. *Why:* the owner
reads the report to decide what to do next.

```markdown
## Profile
<kind · stack · audience · constraints>

## Baseline
<gate state, coverage, number of findings, audits — before → after>

## Done
1. <commit subject> — <topic>

## Deferred
1. <finding> — <why it is deferred> — <proposed fix>

## Decisions for the owner
1. <decision> — <options> — <recommendation>
```
