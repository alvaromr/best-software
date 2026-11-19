# Scoring eval

The gate checks the form of the skill; this eval checks that the scoring procedure finds what it should. `project/`
is a tiny Python project with known flaws. Run the eval by hand after a change to `score.md` or to a reference's
audit signals. *Why:* only an agent can judge meaning, so the proof that the prose works is an agent applying it to
a project whose flaws are known.

## Run
1. Copy `project/` into a new empty directory outside this repo, then run `git init`, `git add -A` and
   `git commit -m "Add the example"` there.
2. In a fresh agent session in that directory, ask: "Score this project with the best-software skill."
3. Compare the report and the run in `.best-software.json` with the expected result below.
4. Repeat steps 1 to 3 once, and compare the two runs with each other.

## Expected
The eval passes when each run shows all of these:
- Hard constraint 2 broken, with `app.py`, `load_settings` as evidence: the broad catch returns `{}`, a silent
  fallback.
- A global score of at most 4.0, with the cap line in the report.
- `code`: "Empty or broad catches", at `app.py`.
- `testing`: "`isNotNull`-only assertions", at `test_app.py`, and "No coverage threshold".
- `tooling`: "No single gate".
- `repository`: no README and no `AGENTS.md`, from its root-files table; `docs` judges only what existing docs say.
- `ui`: not applicable, since the project has no interface.

It fails if a run misses any of these, reports a secret or personal datum, or scores `ui`. The two runs must also
agree on the global score and on the expected signals; any other difference between them is noted, not a failure.
