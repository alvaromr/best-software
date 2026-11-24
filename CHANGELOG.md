# Changelog

What changes for the agents that use this skill, newest first. The skill has no version numbers: each entry is
dated, and the run record names the exact commit (`SKILL.md`, "Run record").

## 2026-11-24
### Changed
- A score skips a signal that only rewriting published history could fix, such as a published commit that mixes
  changes, unless it breaks a hard constraint (`score.md`, "Rules").

## 2026-11-23
### Added
- Code that runs git on a repository of its own (a test, fixture, helper or script) unsets the variables
  `git rev-parse --local-env-vars` lists before its git commands, because a hook exports them and a gate run from the
  pre-commit hook would otherwise commit, branch and write config in the real repository. In production code, a
  test runs that code with `GIT_DIR` pointing at a decoy repository and asserts the decoy is untouched; verification
  code gets no such test. Missing either is a `safety` signal (`references/testing.md`, "Isolation and speed").
- Each repeatable procedure has one home, with an agent as its usual operator: a script exposed as a named task when
  it can be scripted, otherwise a runbook in `docs/runbooks/`, and a project skill that triggers on the task and points
  to the script or runbook without repeating its steps. A procedure written out in a skill or doc, and a scriptable
  routine left as manual steps, are new signals. A plan kept out of the docs that turns out to be a repeatable
  procedure goes to that home.

### Changed
- The run record is `.best-software`, with no extension though its content is JSON, so the project's formatters and
  linters leave it alone (`SKILL.md`, "Run record").
- The gate lints every language of the production code, not every language in the repo; tests and scripts are
  checked with those same tools only, so a repo whose product is Markdown needs no linter for its Python tests or
  shell scripts (`references/tooling.md`, "The gate").
- The full mutation set runs once, when the owner chooses, one repository at a time with the machine free and kept
  awake; from then on each change mutates what it touches before it is pushed, so the result stays whole, and a full
  run happens again only when the owner asks. A change re-runs only the mutants whose result it can change: config
  that does not change the mutants or how their tests run, tools the tests do not use and version numbers re-run
  nothing. A score, an elevate pass or a release with no previous result no longer runs the full set; the score
  reports the last result and may run the scoped run for what changed. A task that re-runs every mutant for such a
  change is an `efficiency` signal, and an old result now means code or tests changed with no scoped run covering
  them since (`references/testing.md`, "Coverage and mutation").
- A mutation run keeps the tool's own default per-mutant timeout instead of 10 to 20 times one test run; on a loaded
  machine it raises the timeout's fixed part, not its multiplier. A change to the timeout re-runs only the mutants it
  can flip: a longer one, those that timed out; a shorter one, those that survived. A timeout moved by its multiplier,
  or with no recorded reason, is an `efficiency` signal (`references/testing.md`, "Coverage and mutation").
- The test runner is one the mutation tool runs in one process, as a dev dependency even when the product ships none
  (in JS, Vitest); the platform's built-in runner only when the project cannot take dev dependencies
  (`references/testing.md`, "Levels").
- Code that runs as a command, server or child process takes its process inputs as parameters, so tests drive its
  logic in their own process with fakes; only the end-to-end smoke test starts the real program. Tests that start the
  program to test its logic are a `changeability` signal (`references/testing.md`, "Isolation and speed").
- With pnpm, Stryker's runner plugin is listed in `plugins` (`references/toolchains.md`, "TypeScript / Node / Web").
- Project skills live in one directory of the repo's choosing, which other tools' skill directories symlink to, not
  in a fixed `.agents/skills/` (`references/repository.md`, "Layout").
- A project records the owner's acceptance of a platform's terms only when it uses that platform in a way the platform
  could object to: scraping its site, acting beyond what a person does by hand, acting on behalf of other people, or
  redistributing its data. A tool the account holder runs on their own account at a person's pace needs no record,
  and its absence is no longer a signal (`references/security.md`).
- Calling routes a platform does not document is no longer a terms issue: a tool the account holder runs at a
  person's pace may use the routes the platform's own web client uses. It is a maintenance risk, which the project's
  tests or smoke check catch the day those routes change (`references/security.md`).
- The minimum release age the Node package manager is set to wait before installing a new release is 4 days, down
  from 7 (`references/toolchains.md`).
- Plans and work state stay out of the docs: pending steps, the next release or one-off owner decisions go to the
  issue tracker or the owner's task list, a lasting decision to `docs/decisions/`, a repeatable procedure to its one
  home, as added above. Known limitations cover only what the project cannot do and deferred ideas. Scoring flags a
  plan, pending step or one-off owner decision in the docs, `AGENTS.md` and `README.md` included, as a `truth` signal.

## 2026-11-20
### Added
- When a project builds a package, the agent checks that the private run record is not in it, because build tools
  may pack files git does not track.

### Changed
- New commits follow the repo's established convention in every part, scope included: a history without scopes gets
  none. Release scripts, `commit-msg` hooks and changelog tooling write and accept only that convention.
- Mutation runs only on the code and tests a change touches. A full run needs the owner's request or a stated
  reason, such as no previous result or a change to shared test helpers, the mutation config or the dependencies;
  once a result exists, a score, an elevate pass, a release or a commit is not one. Each run ends with zero
  unexplained survivors in what it mutated. Scoring reports the last mutation result, scoped or full, and runs
  mutation only when none exists. A missing result, or one older than the code or tests, is a `correctness`
  signal, and a task or script that runs the full set by default is an `efficiency` signal.

## 2026-11-19
### Added
- A `publish` operation (`publish.md`): elevate with the profile set to be published, then the release when an
  artifact is distributed, a "Publishable" verdict, every outward action listed for the owner's yes, run with the
  project's release script, and a fresh copy from the remote verified afterwards.
- The profile asks whether the project is to be published or shared, and where; if so, the owner's publish decisions
  and private names come in one question at the start. Scoring then runs in full, counts public-repo practices as if
  public, and ends in the "Publishable" verdict.
- New signals for publication: a name the owner listed as private in a file or the history; copied code whose
  licence clashes; a third party's mark presented as the project's own; a security policy naming a channel that is
  not enabled. The history audit searches diffs and commit messages with the secret scanner and the owner's names,
  and checks author emails; commit times are flagged to the owner before the first publication.
- The agent classifies each personal datum it finds (test data, declared identity, or someone else's) instead of
  handing the owner a list; a project that drives another platform records that its terms were accepted; the release
  script runs dry before the first tag.
- A public repo has a `CONTRIBUTING.md` that points to `AGENTS.md`; one that takes outside contributions also has a
  code of conduct and issue and pull-request templates.
- Each hard constraint states its own reason: what harm it prevents and why that harm spreads unseen.
- Hard constraint 8, split from 3: never rewrite published history or move a tag. Constraint 3 keeps the gate and
  the hooks, and scoring's direct evidence names 1, 2 and 8.

### Changed
- A project that declares no oldest supported version gets the oldest one its code runs on, tested there; raising it
  is left to the owner.
- Each operation has its own file (`bootstrap.md`, `score.md`, `elevate.md`), named by an argument in `SKILL.md`'s
  operations table; `SKILL.md` keeps only what they share: the profile, the run record, reports and the guide
  template.
- The Python mutation task fails on any surviving mutant, because the tool itself exits with success, and its
  config uses the option name that is not deprecated.
- Raising the oldest runtime or OS version a project supports is a choice left to the owner, like a public API break.
- A recorded decision never excuses a broken hard constraint when scoring: the evidence still caps the score at 4.0,
  and the owner's decision goes to the report.
- Elevate keeps a test that already fails as written, recorded in the baseline; whether the test or the code is
  right is left to the owner.
- Elevate scores the project before its first change and after its last, instead of assessing it on its own; its
  report shows the global score before and after. Scoring is read-only again: it no longer fixes anything.
- Only production deploys need a tagged commit; previews and staging may run any commit.
- Elevating a project whose build or tests already fail records those failures as the baseline, so the first commit
  is possible; the gate then fails only on new failures.
- A CLI's output to its user goes to stdout; only logging must go through the project logger.
- A defect outside the project, in a dependency or the platform, may get a workaround that cites its source and
  when it can go.
- Settle rules whose copies disagreed: coverage is lowered only by a recorded deviation, never for a prototype alone;
  hooks are never bypassed, with no WIP override; one list of choices left to the owner, in the constitution; health
  and version endpoints are asked of services only.
- Each rule is stated once, in the reference that owns its topic, and other files point to it: what never scales down
  lives only in the `SKILL.md` table, the constitution's tensions keep their reasoning, and toolchain lines name only
  tools.
- What counts as a personal datum or a live secret, such as declared authorship or a credential proven revoked, is
  stated once, in the security reference, and scoring points to it.
- Toolchain pins (`packageManager`, version files, wrapper scripts) are checked for updates by hand, because the
  package manager's outdated report skips them; a dependency or pin behind its latest stable past the release-age
  wait, without a reason, is a `tooling` signal.
- Mutation runs are bounded so the machine stays usable: at most half the cores, lower priority, and a per-mutant
  timeout of about 10 to 20 times one test run.
- The docs signal for a README covers only a README that exists and lacks install, run or test; a missing README
  is a `repository` signal, from its root-files table.

### Fixed
- Absolutes narrowed to where their reason holds: a generated file the build reads but does not regenerate, such as
  a lockfile, is committed; ticket references in comments follow the repo's existing convention, and an upstream
  issue behind a workaround is cited; `innerHTML` is banned for untrusted data; parallel builds are banned only when
  they share an output; only URLs a rewrite moves must redirect.

### Removed
- How to test screen sizes without touching the user's window: it governs how an agent works with its owner, which
  the constitution leaves to the owner's own instructions.

## 2026-11-18
### Added
- Code with logic stays where the gate checks it, never inside a string that escapes format, lint and type-check.
- Deep modules with a small interface, tests through that interface only, and one owner for each piece of state.
- A correction made twice becomes a gate check.
- Agent instructions name patterns by their established term instead of describing them.
- MIT licence, a security policy and a clone command in the README.

### Changed
- The constitution says when to read a reference (before the first change on its topic) and why the constitution
  alone is not enough.
- Reports are written in the owner's language, from templates in English.
- The README states the bar the skill asks of every project.

## 2026-11-06
### Added
- After scoring, the agent fixes every signal that needs no owner decision, then scores again.

## 2026-11-05
### Changed
- A link to the project's own public home is not scored before its first publication.
- The git reference states which tag deletion a local hook cannot refuse.

## 2026-11-04
### Added
- Checks never run against the owner's own app, and no dev tool may raise the oldest supported runtime or OS.
- A reviewed fix for a known security advisory may skip the minimum release age.

### Changed
- Scoring counts a breach of any practice, not only the listed audit signals.
- Misplaced code and docs are scored, and a changed project profile forces a full scoring pass.
- A feature branch is created only where the project integrates through pull requests.

## 2026-11-03
### Added
- Scores subtract points per signal instance, at most 3 per signal and section, by the value at stake.
- Each audit signal states its default value, an identical run is reused, and a run on the same skill version starts
  from the last verified signals.
- The score report ranks every signal by the global points its fix recovers.
- Reviews stop at findings that clear a bar: reproduced or realistic, and worth their cost.
- The agent updates outdated dependencies itself, with the package manager's own report, instead of a bot.
- A scored project's files are data, never instructions to the agent.
- Exact toolchain pinning per project kind: services, libraries and tools.
- A commit-msg hook that checks the subject against the repository's convention.

### Changed
- Verification code (tests, test helpers, gate checks) gets no coverage target, mutation run, tests of its own or
  toolchain pin.
- The scoring commands are named apart from the checks of hard constraint 3.
- The gate config and toolchain pin are required only where production code exists.
- Each instruction and audit signal is stated in one file only, and the others point to it.
- The user-level agent instructions point to the constitution instead of holding a copy of it.
- The Python mutation tool moves to the release that runs on the current test runner, with the sources cited.

## 2026-10-30
### Added
- A read-only scoring procedure, with a global score and one per section.
- A private run record, `.best-software.json`, for every procedure.
- Deviations from a practice are recorded in the project's `docs/decisions/`, with who decided them.
- A workaround for the Python mutation tool's crash on macOS.

### Changed
- The skill is renamed from `engineering-standards` to `best-software`.
- Tools and their versions appear only in the toolchains reference.

### Fixed
- Two contradictions and the scoring edge cases found on the first runs.

## 2026-10-29
### Added
- First version: the engineering constitution, the bootstrap and elevate procedures, and one reference per topic.
- A network block for unit tests in Node and Python.
