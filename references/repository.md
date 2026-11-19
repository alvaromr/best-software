# Repository structure and hygiene

**Goal:** anyone can clone the repo and, from the README alone, build, test and run it on another machine. The repo
could be published at any moment without leaking anything. This serves safety, truth and changeability.

## Practices

### Layout
- **Follow the stack's conventional layout,** with tests mirroring the source and a predictable home per concern:
  - source (core, adapters, UI)
  - `tests/`
  - `scripts/`, `bin/`
  - `docs/`
  - data or fixtures
  - per-environment config, in one folder

  Keep the root lean. *Why:* convention is free documentation, and newcomers and tools know where to look.
- **Modularize by feature** once there are several features: a shared core, a UI/design-system module, a test-support
  module, and build logic shared instead of copied. *Why:* modules make boundaries enforceable, and shared build logic
  keeps modules consistent.
- **Use one deliverable per top-level folder** in multi-package repos, each with the same layout, all listed in one
  root manifest. *Why:* uniform packages can be audited and changed uniformly.
- **Keep one canonical home for agent guidance:** `AGENTS.md`, with `CLAUDE.md` as a symlink, and project skills in one
  directory that other tools symlink to. A project-owned skill or CLI lives in its repo. *Why:* two copies of
  instructions diverge (truth), and a tool outside its repo goes stale.

### Root files

| File | When | Why |
|---|---|---|
| `README.md` | always | the entry point for every reader |
| `AGENTS.md` + `CLAUDE.md` symlink | always | how to work on the repo, in one place |
| `.gitignore`, `.editorconfig` | always | hygiene and consistent editors |
| formatter/linter/type-checker config | the repo has production code | the gate needs it |
| lockfile + toolchain pin | the repo has production code | reproducible builds |
| `.env.example` / template | the app reads env | documents every variable without secrets |
| `CHANGELOG.md` | versioned or released | users learn what changed |
| `LICENSE` | public or shared code; ask the owner which | without it, nobody may legally use the code |
| security policy | as `security.md`, "Reporting channel" says | how to report issues |
| `PRIVACY.md` | software handling user data | what happens to data |
| `docs/` | beyond small tools | decisions, operations, limitations |

### Hygiene
- **`.gitignore` covers** build outputs, dependency folders, caches, coverage and mutation dirs, IDE state, local
  config, local agent settings, secrets and OS junk. Use generic patterns, and never version files the program
  rewrites at runtime. *Why:* noise in `git status` hides real changes, and runtime files cause endless churn.
- **Track every config file the build needs,** such as `tsconfig`, wrappers, lint configs and the version catalog.
  *Why:* an untracked build input makes the build unreproducible.
- **Never commit generated artifacts:** `dist/`, `build/`, installers, coverage, test output. *Why:* they are derived,
  stale on the next change, and bloat history.
- **Keep the repo publishable at all times:**
  - No personal, company or machine-specific data.
  - Cross-platform paths.
  - Everything user-specific is configuration.

  *Why:* repos get shared or published sooner than planned, and history keeps whatever leaked.
- **Every versioned artifact is agnostic of the individual developer from the start.** It is never cleaned up before
  publishing. `AGENTS.md`, hooks, scripts, project skills and commit messages are part of the code. They describe how
  *anyone* works on this project.
  - The developer's own setup and habits never enter the repo, not even as a gitignored `.local` file. That covers
    personal tools, permissions, memories, workflow rules, handoff notes and process narration. They live in the
    developer's user-level configuration.
  - **Test each item:** would every contributor need it, and would it work the same for them? Would it tell a stranger
    something about you, your team or your clients that they have no reason to know?

  *Why:*
  - The project behaves the same for everyone who clones it.
  - Publishing needs no cleanup step that can be forgotten.
  - No private and public versions drift apart.
  - Nothing exposes context (tools, clients, habits, internal names) that may be confidential or useful to an attacker.
- **Keep private inputs out of git** via `.gitignore` or `.git/info/exclude`. *Why:* once committed, a private
  document is in history for good.
- **Keep experiments out of production code:** delete them, or archive them clearly with their lessons. *Why:* dead
  experiments mislead readers about what the system does.
- **Update the env template in the same change that adds or renames a variable.** *Why:* a stale template breaks the
  next setup (coherence).
- **Prefer vectors and modern compressed formats for assets,** with extensions matching the real format. Keep assets
  homogeneous across variants and remove unused ones with a task. *Why:* the app gets smaller, and variants stay
  coherent.
- **After integration, delete merged branches and orphaned worktrees,** and report anything unintegrated before
  deleting it. *Why:* stale branches hide which work is real.

## Judgment
- Folder depth grows with the codebase, not ahead of it.
- Keep a personal-data repo local, without a remote, when its content must never leave the machine. Record the reason.
- **Relaxing the developer-agnostic rule:** relax it only when the owner asks, and only for a repo that will never be
  published or shared. The repo may then hold the owner's own workflow and setup. Record the decision in
  `docs/decisions/`, so that before any change of plan the cleanup is a known task, not a surprise. Secrets
  stay out regardless (hard constraint 1). *Why:* the rule's value is consistency for others and safe publication;
  with no others and no publication, that value is not at stake, but a leaked secret still is.

## Audit signals
- A cluttered root. `changeability`
- Tests that do not mirror the source. `changeability`
- Committed `build/`, IDE files or OS junk. `simplicity`
- Untracked build config. `correctness`
- Absolute or personal paths. `correctness`
- A stale env template. `truth`
- Duplicate agent instructions. `changeability`
- Stale branches. `simplicity`
- A published package that links to a private repository: its "Repository" link is a 404 for the public. `truth`
