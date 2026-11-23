# Bootstrap eval

This eval checks that the bootstrap procedure (`bootstrap.md`) starts a project with the gate before any feature.
There is no example project: the agent starts from an empty directory. Run it by hand after a change to
`bootstrap.md`, to the project guide template, or to the gate's practices in `references/tooling.md`. *Why:* the
order of bootstrap is its whole point, and only the commits an agent makes show whether it kept that order.

## Run
1. Create a new empty directory outside this repo.
2. In a fresh agent session in that directory, ask: "Bootstrap a Python command-line tool that converts Celsius to
   Fahrenheit, with the best-software skill." When the agent asks the owner, answer: private project, no remote, no
   licence.
3. Compare the commits, the files, the run in `.best-software` and the agent's messages with the expected result.

## Expected
The eval passes when the run shows all of these:
- The profile is stated before any file is written.
- The first commit holds the gate, its hooks and a walking skeleton, with the gate green; no later commit adds
  either for the first time.
- The conversion rule lives in a pure core module, apart from the command-line adapter that reads arguments and
  prints.
- The gate runs format, lint, strict types and tests with a 100 % coverage threshold, and mutation is configured on
  the core.
- The feature is built test-first: its test lands in the same commit as its code, or before it.
- A README with install, run and test, and an `AGENTS.md` that follows the template, with `CLAUDE.md` as a symlink.
- A bootstrap run appended to `.best-software`.

It fails if any commit has a red gate, if a feature lands before the gate, or if the agent picks a licence or makes
the project public without asking.
