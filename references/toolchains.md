# Toolchains: current defaults per stack

These are means, not goals. Each line names the outcome first, then today's best-known tool. Replace a tool when a
better one reaches the same outcome. Before adopting a tool, check its current version and status with the docs MCP
(context7) or the registry. This file is the only one in the skill that names tools or their versions; the others
name only standards, such as SemVer or WCAG.

Last reviewed: 2026-10-29.

## Agnostic
- **Hooks installed from the repo:** `lefthook` or `pre-commit`, or a build-installed hook script.
- **Secret scanning:** `gitleaks`.
- **Container lint and scan:** `hadolint`, `trivy`.
- **Dependency update PRs:** Renovate (`config:best-practices`, `rangeStrategy: pin`), configured as a repo file.
- **Diagrams:** Mermaid.
- **Private vulnerability reporting:** GitHub Private Vulnerability Reporting, or the hosting platform's equivalent.
- **Editor settings:** `.editorconfig`.

## Kotlin / Android / JVM
- **Build:** Gradle Kotlin DSL, the version catalog (`gradle/libs.versions.toml`) and convention plugins in an included
  build. Commit the wrapper, set a JDK toolchain, and enable the configuration cache where plugins allow it.
- **Static analysis:** detekt with `warningsAsErrors`, Compose rules where Compose is used, and formatting via
  ktlint/detekt-formatting. Run Android Lint with `abortOnError` and `warningsAsErrors`. Set Kotlin `allWarningsAsErrors`
  and `extraWarnings`.
- **Library surface:** `explicitApi()` and binary-compatibility-validator.
- **Dependency hygiene:** dependency-analysis plugin, and `implementation` over `api`.
- **Tests:** JUnit 5 or kotest, MockK only at boundaries, Turbine for flows, `kotlinx-coroutines-test` with injected
  dispatchers, Robolectric for JVM Android tests, Compose UI tests, and Roborazzi or Paparazzi for screenshots.
- **Coverage:** Kover with verification rules (line and branch), or JaCoCo.
- **Mutation:** PIT (pitest) with the Kotlin plugin, or Arcmutate.
- **Architecture rules:** Konsist, or detekt `ForbiddenImport`.
- **Release:** R8 full mode, consumer ProGuard rules in libraries, and a `resourcePrefix` in library modules.

## TypeScript / Node / Web
- **Package manager:** pnpm, with hardening in `pnpm-workspace.yaml`: `minimumReleaseAge: 10080`, `trustPolicy:
  no-downgrade`, `verifyDepsBeforeRun: error`, `allowBuilds: {}`. Pin `packageManager`, use frozen-lockfile installs,
  and pin the runtime (`.node-version`, `engines`).
- **Types:** TypeScript `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`,
  `noUnusedLocals` and `noUnusedParameters`. Type plain JS with JSDoc and `checkJs`.
- **Lint and format:** Biome, or ESLint (`typescript-eslint` strict-type-checked) with Prettier.
- **Dead code:** knip.
- **Architecture rules:** dependency-cruiser, or `noRestrictedImports` in Biome/ESLint.
- **Tests:** Vitest with V8 coverage thresholds at 100. It is the default, because it enables per-test mutation
  runs. Use `node --test` with coverage flags only when the project must stay dependency-free; mutation then needs
  the command runner. Use happy-dom for headless DOM and Playwright for e2e.
- **Network block in unit tests:** a Vitest setup file, loaded only by the unit project, that makes
  `net.Socket.prototype.connect` throw. It blocks `fetch`, `http` and raw sockets with no dependency; integration
  tests run in a separate Vitest project without it. MSW (`onUnhandledFrame: 'error'` in v3) and nock
  (`disableNetConnect()`) also reject unmatched HTTP requests, but not raw sockets.
- **Mutation:** StrykerJS. Prefer a runner plugin with per-test coverage, such as `@stryker-mutator/vitest-runner`,
  which always uses `perTest`: each mutant runs only the tests that cover it. The command runner (the only option
  for `node --test`) reports no coverage and re-runs its whole command per mutant. With it, point
  `commandRunner.command` at the unit test files only, and keep `concurrency` low. Add
  `@stryker-mutator/typescript-checker` to discard mutants that do not compile before running tests, and run with
  `--incremental` so each run re-tests only what changed.
- **Audit:** `pnpm audit`.

## Python
- **Environment and packaging:** uv, with hatch where named env scripts help. Use a `src/` layout and keep all config in
  `pyproject.toml`.
- **Lint and format:**
  - ruff with a broad rule set: `E,F,W,I,N,UP,B,SIM,ARG,PERF,PL,TID,ERA,C4,DTZ,LOG,TC,S,D` plus framework rules.
  - `ban-relative-imports = "all"`.
  - pydocstyle with `convention = "google"`, off for tests and scripts, with each ignored `D` rule annotated.
  - `ruff format` with `docstring-code-format = true`.
- **Types:** mypy `--strict` (`warn_unreachable`, `warn_unused_ignores`, framework plugins), or pyright strict.
- **Tests:** pytest with pytest-cov (`branch = true`, `fail_under = 100`), hypothesis for property tests, an
  `httpx.MockTransport`/`respx`-style transport mock, and a version matrix via nox or hatch. Add a test that resolves
  the type hints of every public callable (`typing.get_type_hints`) on each matrix version, because annotation
  evaluation differs between versions (lazy since 3.14).
- **Network block in unit tests:** an autouse fixture in `conftest.py` that makes `socket.socket.connect` and
  `socket.getaddrinfo` raise, skipped for tests with the project's integration marker. It needs no dependency;
  `pytest-socket` (`--disable-socket`, `@pytest.mark.enable_socket`) is the packaged equivalent. Drivers with native
  network code, such as libpq, bypass both, so real databases stay in integration tests.
- **Mutation:** mutmut, or cosmic-ray. mutmut adds methods to classes, so tests that introspect classes (generated
  docs, per-method docstring checks) fail under it. Leave those tests out of the mutation command, with the reason
  recorded. On macOS, run mutmut ≥ 3.8 with `NO_PROXY=*`. It forks one child per mutant, and a child that calls
  CoreFoundation crashes at random, which mutmut reports as a segfault. urllib's system proxy lookup makes that call,
  and so did setproctitle before mutmut 3.8.
- **Architecture rules:** import-linter.
- **Security:** ruff's `S` rules, which reimplement bandit's checks inside the gate, so bandit itself is not needed.
  Use pip-audit for vulnerable dependencies.
- **Schema:** Alembic migrations as the only schema owner.

## Containers / services
- Use a multi-stage Dockerfile, base images pinned by digest, a non-root user and a `HEALTHCHECK`. Compose with layered
  env files and `${VAR:?}` guards. Put a reverse proxy (Caddy or nginx) in front, serving static files.
