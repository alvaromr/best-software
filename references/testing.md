# Testing

**Goal:** the test suite is the executable specification. A green gate means the behaviour works, and any regression
turns it red. Feedback arrives in seconds. This serves correctness, truth and changeability.

## Practices

### Method
- **Use TDD:** red, green, refactor. Write the failing test first for every feature, behaviour change and bug. *Why:* a
  test seen failing is proven to test something, and test-first design yields testable, decoupled code.
- **Reproduce a bug before fixing it.** The reproduction becomes the regression test, and a report's claims are never
  trusted unverified. *Why:* without a reproduction you cannot know the fix fixed it, nor that it stays fixed.
- **Refactor only under a safety net:**
  - On untested legacy, write characterization tests first.
  - To prove an equivalence, a disposable test is fine; delete it afterwards.

  *Why:* refactoring means unchanged behaviour, and only tests can show that.
- **Every security fix ships with a test that fails if the fix is removed.** *Why:* security regressions are silent
  until exploited.
- **Every bug found in the field becomes a regression case,** kept in a growing scenario suite. *Why:* a bug that
  escaped once has proven that the suite had a hole there.

### Coverage and mutation
- **Gate on 100 % line and branch coverage,** plus functions in JS/TS, measured on the full suite.
  - A new branch ships with its test.
  - Never lower the threshold.

  *Why:* below 100 % nobody can tell which uncovered lines matter. At 100 %, any new gap is visible and blocks.
- **Keep exclusions explicit, rare and justified** in the coverage config:
  - An unreachable defensive branch is provoked in a test, or deleted.
  - Generated code and a thin entry point covered by e2e may be excluded, with the reason recorded.

  *Why:* an exclusion is a claim that the code needs no proof, so it must be stated and defended.
- **Measure production code only.** Tests, test helpers and the gate's own checks are verification code: they get no
  coverage target, mutation run or tests of their own. A new check proves itself by failing once on a known violation.
  They run on the toolchain production code pins and need no pin of their own. *Why:* testing the tests never ends, a
  check seen catching a real violation has already shown it works, and a check that cannot run fails loudly.
- **Add mutation testing on the core,** or on everything when it is cheap:
  - Run it outside the pre-commit hook.
  - Its command runs only the unit suite. Prefer a runner that executes only the tests covering each mutant, and set
    low concurrency and a timeout close to the suite's real time as safety limits.
  - Start small, with one module or a sample, before the full run.
  - Triage every survivor: a real hole gets a test, an equivalent mutant gets a recorded reason.
  - Improve the tests before touching production code.
  - Target zero unexplained survivors in the core.

  *Why:* coverage proves the code ran, while mutation proves the tests would notice if it were wrong. Mutation runs
  the tests once per mutant, so it multiplies their cost and side effects by hundreds. Only fast, in-process unit
  tests stay safe at that scale.

### Test design
- **Write tests as specification.**
  - Names state the rule in domain language.
  - Use arrange-act-assert, one behaviour per test.
  - Use parameterized tables for variants, including near-miss negatives.

  *Why:* the suite becomes documentation that cannot go stale, because it runs.
- **Assert exact observable outputs:** whole messages, exact log lines, full rendered output. A test fails when a field
  or behaviour disappears. *Why:* weak assertions such as "not null" pass on broken code.
- **Avoid tautological tests;** condense repetitive tests into parameterized ones and check that nothing was lost.
  *Why:* a test that re-implements the code shares its bugs.
- **Test domain invariants,** not just examples (physical, mathematical and game rules, round-trips). Cross-check
  against references, and never approximate silently. *Why:* invariants catch whole classes of bugs, while examples
  catch one each.
- **Validate shipped data in tests:** every fixture, preset or content file parses and meets its schema. *Why:* data is
  code that no compiler checks.
- **Use realistic, coherent fixtures** loaded by name, plus an edge-case dataset (empty, many, overlapping, missing).
  *Why:* unrealistic fixtures prove behaviour on inputs that never occur.
- **Lint and type-check test code with the tools that check production code;** verification code alone never justifies
  adding a tool. *Why:* sloppy tests produce false confidence, but a toolchain kept only for the tests costs more than
  it catches.

### Isolation and speed
- **Keep the suite overwhelmingly unit tests on the pure core.** Higher levels exist only for what units cannot reach.
  *Why:* unit tests are fast, precise and stable, and they make TDD and the pre-commit gate usable.
- **Treat speed as a requirement:**
  - A unit test runs in milliseconds, with no I/O, sleeps or real time.
  - The unit suite runs in seconds, in the pre-commit hook.
  - A slow test is a defect: move its logic into the core, or move the test down a level.

  *Why:* a slow suite stops being run, and an unrun test proves nothing.
- **Keep tests hermetic:**
  - No real network; the build blocks it.
  - Use a fake backend or mock transport that asserts method, path, headers, query and body.
  - Use a temporary HOME and temporary directories.
  - Pin the clock, timezone, locale and random seed.
  - Make no test depend on another test's order.
  - A test terminates every process it starts, even when the code under test fails to stop it. Kill the process
    group in teardown, and bound it with a timeout in the harness.

  *Why:* a test that depends on the world fails for reasons unrelated to the code. A process left alive by a failing
  test keeps consuming the machine, and repeated runs exhaust it.
- **Mock only system boundaries;** project code runs for real, and fakes beat mocks. A test needing many mocks sits at
  the wrong level. *Why:* mocking project code tests the mocks and freezes the implementation.
- **Test a module through its interface,** not its internals: its private helpers, its constants or the text of its
  source. *Why:* a test tied to the structure breaks on every refactor yet can pass on broken behaviour, so it checks
  the shape of the code, not what it does.
- **Never trigger real-world side effects from tests:** payments, real accounts, paid APIs, production writes. *Why:*
  tests run often and unattended.

### Levels
- **Integration tests are few.** They cover only the adapters (database, HTTP, filesystem, platform) against real or
  contract-faithful dependencies, and never re-test business rules. They run outside the pre-commit hook. *Why:* they
  catch wiring and contract errors, which units cannot see, but they are slow.
- **Contract tests guard fragile third parties** and come before infrastructure migrations. *Why:* they pin the
  behaviour you depend on, so an upgrade fails loudly.
- **Live checks** verify real responses and stay out of the default run:
  - Reads go to a non-production environment. They may go to production only when no non-production environment
    is faithful to it, for example because of different configuration.
  - Writes never go to production. Destructive ones need the owner's permission.
  - Mark every datum they create with a fixed label, and at the end report what was left behind, and where.
  - Never run them in the owner's running app, account or session; use a separate process, profile or test account.

  *Why:* a check against an unfaithful environment proves nothing, a production read risks nothing, unlabelled
  leftovers become someone else's mystery data, and a check in the owner's own app interrupts their work and acts as
  them.
- **Keep a few end-to-end smoke tests on the real artifact,** plus a short manual plan for what automation cannot reach.
  *Why:* green units do not prove that the packaged thing starts.
- **Automate UI behaviour checks:** a headless DOM when no browser is needed, config-change and process-death survival,
  accessibility, the release build. *Why:* manual checks are skipped under pressure.
- **Run the gate on every supported runtime version.** *Why:* behaviour differs between versions.
- **Use the platform's official test runner when it suffices.** *Why:* it is one dependency less.

### After green
- **Verify in the real runtime before declaring done:**
  - Run the app or CLI, isolated from the owner's as live checks are.
  - Exercise the failure path.
  - Check the affected variants.
  - Repeat flaky-prone checks.

  *Why:* the gate proves what you thought to test, and the real run catches what you did not.
- **Root-cause flaky tests;** never re-run them into green. *Why:* a flaky test either hides a real race or teaches
  everyone to ignore red.

## Judgment
- 100 % coverage and mutation testing are the default bar. Lower them only by a recorded decision, for example UI glue
  proven by e2e, or a prototype explicitly marked throwaway.
- Scale mutation runs to cost: run them per module or incrementally on large codebases.
- Exploratory spikes are deleted, or re-done test-first before they land.

## Audit signals
- No coverage threshold, or one below 100 with no reason. `correctness`
- More integration or e2e tests than unit tests, or tests that re-test rules at high level. `changeability`
- A unit suite that takes minutes; sleeps or real timers in tests. `changeability`
- Tests named after methods. `changeability`
- `isNotNull`-only assertions. `correctness`
- Network or wall-clock in unit tests. `correctness`
- Mocks of project classes. `changeability`
- Tests that assert private helpers, constants or the source text of the code under test. `changeability`
- No regression test next to a fix. `correctness`
- Skipped or retried tests. `correctness`
- No e2e smoke. `correctness`
