---
name: best-software
description: Procedures to bootstrap a new software project at professional quality, or to audit and raise an existing one (architecture, tests with TDD/100 % coverage/mutation, tooling, repo, docs, git, release, security, UI). Use when asked to start a project, make it professional or publishable, review its quality, or apply best practices. Not for CI/CD pipeline design.
---

# Best software — procedures

The values, hard constraints and decision rules are in `constitution.md`; read it first if this session has not. The detailed
practices are in `references/` (index in the constitution). This skill adds only the end-to-end procedures.

## Step 1 — Profile the project
Before changing anything, establish these facts and state them in one short block. *Why:* every judgment call below
depends on them.
- **Purpose and audience:** who runs it, who reads the code, and whether it is public.
- **Kind:** script or CLI, library or SDK, service or backend, app (web, mobile, desktop, extension), game or
  simulation, data or ML.
- **Stack and runtime versions.** For an existing project, also read its current gate, tests, coverage and conventions.
- **Constraints:** frozen legacy, team conventions, deadlines, platforms, compliance (privacy, data residency).

Then decide which practices apply, and how strictly. The right-hand column protects safety, correctness and truth,
which do not shrink with project size:

| Scales with the profile | Never scales down |
|---|---|
| number of layers and modules; DI framework or plain constructors | pure core separated from I/O |
| containers, deploy hooks, health endpoints (services only) | gate: format, lint, strict types, tests, 100 % coverage |
| structured logging depth, metrics | mutation testing on the core |
| web hardening (exposure-dependent) | no secrets in repo or history; validated input |
| ADRs, runbooks, SECURITY/PRIVACY docs | README + AGENTS.md; docs single-sourced and coherent |
| i18n: strings in resources once a second language is planned; assistive-tech verification depth | keyboard and contrast basics |
| release channel and packaging | single version source, changelog, immutable tags |

## Step 2a — Bootstrap a new project
1. **Agree on the profile and the shape of the core:** the domain modules and the adapters at the edges.
2. **Scaffold the repository** (`references/repository.md`):
   - layout
   - root files
   - `.gitignore`, `.editorconfig`
   - toolchain pin and lockfile
   - env template if needed
3. **Install the gate before any feature** (`references/tooling.md`, `references/toolchains.md`):
   - formatter
   - strict linter
   - strict type checker
   - test runner with the 100 % threshold
   - mutation config
   - architecture rule
   - automatically installed hooks
   - one `check` task

   *Why:* quality added later means fixing a backlog; installed first, it means never creating one.
4. **Write a walking skeleton:** one end-to-end path through core and adapter, with its tests, and the gate green.
   *Why:* it proves the architecture and the gate before features depend on them.
5. **Write the project guide** (template below) and the README.
6. **Make the first commit:** the skeleton, green, in the agreed convention.
7. **Build every feature test-first** (`references/testing.md`), one atomic commit per step (`references/git.md`).
   Each commit passes the coherence review: does anything here lie, contradict another part, or describe what no
   longer exists?
8. **Add release artifacts** (`references/release.md`) once something is distributable.

## Step 2b — Elevate an existing project
1. **Prepare the branch:**
   - **If the project is a git repo:** check that the tree is clean. If it is dirty, stop and ask (hard constraint 7).
     Then update the default branch and create a clean branch from it (`chore/engineering-baseline`, or one per topic).
   - **If the project is not a git repo:** ask whether to initialise one before changing anything. Otherwise, deliver
     the assessment only.
2. **Measure the baseline.** *Why:* without a "before" there is no proof of improvement, and no way to spot a regression.
   - Run the existing build and tests.
   - Record coverage, lint and type findings, and the dependency audit.
   - Note what is unknown.
3. **Assess every topic** against its reference's audit signals. Rank the findings by the value order: safety first,
   then correctness, truth, changeability, simplicity and efficiency.
4. **Fix directly, in this order.** Each step is its own atomic commit with the gate green. *Why:* the order builds the
   safety net before anything that could break.
   1. Safety net: characterization tests around anything you will touch.
   2. Gate and hooks. On legacy code, baseline the findings as a ratchet.
   3. Secrets and security fixes. A leaked secret is reported to the owner at once, for rotation.
   4. Repository hygiene and toolchain pin.
   5. Structure and code refactors, under tests, with no behaviour change.
   6. Tests up to the coverage and mutation targets.
   7. Docs and the project guide.
   8. Release artifacts.
5. **Behaviour is frozen during the pass** (hard constraint 6). When you find a real bug:
   - **If the fix is safe:** fix it in its own `fix:` commit with a reproducing test.
   - **Otherwise:** report it.

   Ask before any change that alters public API, data, or the deploy.
6. **Verify:**
   1. Run the full gate.
   2. Run the app, CLI or package as a user would.
   3. Review coherence across every part of the repo, and fix whatever disagrees.
7. **Report** in the format below.

## Project guide template (`AGENTS.md`, with `CLAUDE.md` as a symlink)
The guide is part of the code. It is self-contained, so teammates without this skill can follow it, and agnostic of
the individual developer, so it works the same for everyone (`references/repository.md`). It holds only what tooling cannot express,
and points to files instead of copying them. Non-negotiables carry their reason in one line, so contributors can apply
them with judgment.

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

## Report format (elevate mode, in Spanish)

```markdown
## Perfil
<tipo · stack · audiencia · restricciones>

## Punto de partida
<estado del gate, cobertura, nº de hallazgos, auditorías — antes → después>

## Hecho
1. <asunto del commit> — <tema>

## Aplazado
1. <hallazgo> — <por qué se aplaza> — <arreglo propuesto>

## Decisiones para el dueño
1. <decisión> — <opciones> — <recomendación>
```
