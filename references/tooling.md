# Tooling, static analysis and dependencies

**Goal:** quality is enforced by machines, identically everywhere. Every dependency is deliberate, minimal, pinned and
trusted. This serves correctness and safety, at no cost to the author's attention.

## Practices

### The gate
- **Make one command the gate** (`check`). It runs:
  - format check
  - lint
  - type-check
  - tests with the coverage threshold
  - project guards: architecture rules, file-size cap, secret scan, docs-sync tests

  Its exit code is the verdict, and the same command runs locally, in the hook and in CI. *Why:* one command means one
  definition of "done" that nobody can partially forget.
- **Provide a `fix` companion** that formats, autofixes and re-runs the gate. *Why:* fixing mechanical findings by hand
  wastes attention.
- **Version the hooks in the repo and install them automatically:**
  - The pre-commit hook is fast, runs on staged files, and is skipped when no relevant file is staged.
  - Heavy checks (full matrix, mutation, audits) run before push or integration.
  - Hooks are never bypassed; a skip is a narrow, documented env override for local WIP only.

  *Why:* manual installation means some clones run no hooks, and a slow hook gets bypassed.
- **Expose every routine action as a named, described task:** run, test, gate, fix, coverage, mutation, audit, build,
  release, logs, smoke. *Why:* nobody should have to remember a command, and a forgotten step is a skipped step.

### Static analysis
- **Commit the formatter config and an `.editorconfig`;** docs point to them and never restate their values. *Why:*
  style decided by a machine ends style debates, and restated values drift (truth).
- **Run the linter strict, with warnings as errors;** its config is the single source of truth for style. *Why:* a
  warning that does not fail is ignored forever.
- **Treat baselines as a ratchet:**
  - Generate them with the tool; never edit them by hand.
  - Let them only shrink.
  - Enable stricter rules one at a time.

  *Why:* the baseline makes adoption possible on legacy code, and the ratchet makes it converge.
- **After a tool or plugin bump, verify that the rules actually load:** the provider is registered and a known
  violation is caught. *Why:* a rule set that silently fails to load produces a green build that proves nothing.
- **Keep the analyzer and its rule sets current,** reading changelogs and enabling new applicable rules. *Why:* new rules
  encode new knowledge of bugs, for free.
- **Take facts from tools** (build tasks, compiler, resolver), not from ad-hoc parsing scripts. *Why:* the tool knows
  the real configuration; a parser knows a guess.

### Dependencies
- **Keep dependencies minimal by default:** stdlib and platform first. Review every new dependency for:
  - maintenance and provenance
  - transitive tree
  - licence
  - install and build scripts
  - whether it reaches production

  *Why:* each dependency is code you run but did not write, review or control.
- **Prefer a small own implementation over a large framework for a narrow need,** but never hand-roll crypto, complex
  standard formats or security primitives. *Why:* a small own module removes a trust and upgrade burden, while
  security code needs the scrutiny only mature libraries get.
- **Pin reproducibly:**
  - Commit the lockfile, and keep one place for versions.
  - Use exact versions for tools and applications, and compatible ranges for a library's runtime dependencies.
  - Annotate every pin or hold with its reason.
  - Pin installers and binaries by version and checksum.

  *Why:* the same inputs must produce the same build, and a pin without a reason cannot be safely removed.
- **Declare what you import directly.** *Why:* a transitive dependency can vanish in any upgrade.
- **Remove unused and wrongly scoped dependencies** (`api` vs `implementation`, dev vs runtime), and verify each
  removal by building and running. *Why:* unused dependencies still carry vulnerabilities and slow builds, and a
  "false positive" may be loaded reflectively.
- **Track the latest stable versions.** For runtimes and operating systems with an LTS line, use the latest
  LTS. *Why:* LTS gets security fixes for years without forced upgrades, and plain stable releases of
  a runtime expire within months. The agent working on the project finds what is outdated with the package manager's
  own report and updates it; no update bot. *Why:* a bot needs a hosted remote, and many repos live on one machine
  only. For each update:
  1. Read the changelog from the current version to the target.
  2. List the impact.
  3. Flag every major jump to the owner.
  4. Verify by building, running the gate and exercising the affected features.

  Never revert a risky upgrade blindly. *Why:* staying current keeps security fixes cheap, and verification keeps
  upgrades safe.
- **Harden the supply chain:**
  - Wait a minimum release age before installing a new release.
  - Block install scripts, except an allow-list.
  - Use frozen-lockfile installs.
  - Refuse trust downgrades.
  - Run audits (dependencies, SAST, secrets) as tasks.
  - Read third-party code that touches private data before installing or updating it.

  *Why:* compromised releases are usually caught within days, and install scripts run with your privileges.
- **Pin the toolchain:** wrapper scripts, a runtime version file, `packageManager`, the compiler toolchain. *Why:*
  "works on my machine" is usually a toolchain difference.

## Judgment
- Tool choice follows the goal and stays open. `toolchains.md` lists today's defaults; verify their status before
  adopting.
- On legacy code, introduce the gate in report-only mode, baseline the existing findings, then enforce it on new code at
  once.

## Audit signals
- No single gate.
- Hooks that are manual or absent.
- No formatter config.
- Warnings allowed.
- A hand-edited baseline.
- Floating versions.
- No lockfile, or one that is uncommitted.
- Unused dependencies.
- No audit task.
- An unpinned toolchain.
