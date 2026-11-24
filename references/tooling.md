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
- **Keep code where the gate checks it.** Code with logic (several statements, branches or loops) lives in its own
  file, with its language's extension, and the gate lints every language of the production code, and verification
  code with those same tools only (`testing.md`, "Test design"). A string is fine for a one-line command, or when a
  check in the gate verifies that code, such as a test that runs the query or a tool that validates it. *Why:* the
  gate checks only what its tools can parse. Code in a string escapes format, lint and type-check, needs escaping, and
  editors show it as text, so its bugs surface only when it runs.
- **Provide a `fix` companion** that formats, autofixes and re-runs the gate. *Why:* fixing mechanical findings by hand
  wastes attention.
- **Version the hooks in the repo and install them automatically:**
  - The pre-commit hook is fast, runs on staged files, and is skipped when no relevant file is staged.
  - Heavy checks (full matrix, mutation scoped as `testing.md` says, integration tests, audits) run before push or
    integration.

  *Why:* manual installation means some clones run no hooks, and a slow hook gets bypassed.
- **Expose every routine action as a named, described task:** run, test, gate, fix, coverage, mutation, audit, build,
  release, logs, smoke. *Why:* nobody should have to remember a command, and a forgotten step is a skipped step.

### Static analysis
- **Commit the formatter config and an `.editorconfig`.** *Why:* style decided by a machine ends style debates.
- **Run the linter strict, with warnings as errors;** its config is the single source of truth for style. *Why:* a
  warning that does not fail is ignored forever.
- **Treat baselines as a ratchet:**
  - Generate them with the tool; never edit them by hand.
  - Let them only shrink.
  - Enable stricter rules one at a time.

  *Why:* the baseline makes adoption possible on legacy code, and the ratchet makes it converge.
- **After a tool or plugin bump, verify that the rules actually load:** the provider is registered and a known
  violation is caught. *Why:* a rule set that silently fails to load produces a green build that proves nothing.
- **Keep the analyzer and its rule sets current,** reading changelogs and enabling new applicable rules. *Why:* new
  rules encode new knowledge of bugs, for free.
- **Turn a correction made twice into a check:** a lint rule or a test in the gate, when the tools can express it.
  *Why:* a rule kept only in reviews holds while someone remembers it, while a check holds on every change at no cost.

### Dependencies
- **Keep dependencies minimal by default:** stdlib and platform first. Review every new dependency for:
  - maintenance and provenance
  - transitive tree
  - licence
  - install and build scripts
  - whether it reaches production

  *Why:* each dependency is code you run but did not write, review or control.
- **Prefer a small own implementation over a large framework for a narrow need,** but never hand-roll complex standard
  formats, nor crypto (`security.md`, "AuthN, AuthZ, transport"). *Why:* a small own module removes a trust and
  upgrade burden, while security code needs the scrutiny only mature libraries get.
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
  only. That report lists only the declared dependencies, so the agent checks each toolchain pin (`packageManager`,
  version files, wrapper scripts) against its latest stable by hand. *Why:* an exact pin that no report lists stays
  behind silently, release after release. For each update:
  1. Read the changelog from the current version to the target.
  2. List the impact.
  3. Flag every major jump to the owner.
  4. Verify by building, running the gate and exercising the affected features.

  Never revert a risky upgrade blindly. *Why:* staying current keeps security fixes cheap, and verification keeps
  upgrades safe.
- **Harden the supply chain:**
  - Wait a minimum release age before installing a new release. If the fix for an advisory that reaches the project
    is younger than that age, weigh the advisory's severity and reachability against the risk of a fresh release.
    When the fix cannot wait, review its release (publisher, provenance, install scripts, new dependencies,
    changelog), exempt that exact version with the reason next to the exemption, and remove the exemption once the
    age has passed.
  - Block install scripts, except an allow-list.
  - Use frozen-lockfile installs.
  - Refuse trust downgrades.
  - Run audits (dependencies, SAST, secrets) as tasks.
  - Read third-party code that touches private data before installing or updating it.

  *Why:* compromised releases are usually caught within days, and install scripts run with your privileges. The wait
  guards against an unknown compromise, so it must not keep a known one.
- **Pin the toolchain as exactly as the project kind requires:**
  - Services and apps: the exact runtime patch that production runs; for a container, the base image by digest.
  - Libraries and SDKs tested across a version matrix: each supported minor, tested on its latest patch, with the gate
    printing the patch each environment used.
  - Build tools, package managers, installers and compilers: the exact version, always, through wrapper scripts,
    `packageManager` or a version file.
  - No dev tool raises the oldest runtime or OS version the project supports.
  - A project that declares no oldest supported version gets the oldest one its code runs on, checked by running the
    tests there; raising it is the owner's choice (constitution, "How to decide").

  *Why:* "works on my machine" is usually a toolchain difference, so the gate runs what production runs. A library's
  users pick the patch, and the latest one carries the security fixes, so a frozen old patch keeps fixed bugs; the
  printed patch makes a difference between machines visible instead of silent. A supported version dropped for a dev
  tool locks users out for nothing they use, and an undeclared floor already includes every version the code runs on,
  so declaring a higher one drops users silently.

## Judgment
- On legacy code, introduce the gate in report-only mode, baseline the existing findings, then enforce it on new code at
  once.
- Code kept in a string usually buys isolation, such as running against the installed package instead of the source.
  A separate file, run with the interpreter's isolation option, buys the same and stays checked.

## Audit signals
- No single gate. `correctness`
- Code kept in strings or config, out of the gate's reach. `correctness`
- Hooks that are manual or absent. `correctness`
- No formatter config. `changeability`
- Warnings allowed. `correctness`
- A hand-edited baseline. `truth`
- Floating versions. `correctness`
- No lockfile, or one that is uncommitted. `correctness`
- Unused dependencies. `simplicity`
- No audit task. `correctness`
- A toolchain pinned less exactly than its project kind requires. `correctness`
- A dependency or toolchain pin behind its latest stable past the release-age wait, without a reason. `changeability`
