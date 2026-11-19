# Elevate eval

This eval checks that the elevate procedure (`SKILL.md`, "Step 2b") raises an existing project without breaking the
hard constraints. `project/` is a tiny Python project with a test that already fails, a swallowed error and no gate.
Run it by hand after a change to Step 2b, to the hard constraints, or to a reference's practices that Step 2b fixes.
*Why:* elevate changes a project more than any other procedure, and only an agent applying it shows whether it keeps
behaviour frozen and every commit green.

## Run
1. Copy `project/` into a new empty directory outside this repo, then run `git init`, `git add -A` and
   `git commit -m "Add the example"` there.
2. In a fresh agent session in that directory, ask: "Elevate this project with the best-software skill." When the
   agent asks the owner, answer: private project, no remote, no licence, keep the current behaviour.
3. Compare the commits, the working tree, the run in `.best-software.json` and the report with the expected result.

## Expected
The eval passes when the run shows all of these:
- The baseline records `test_average_of_nothing` as failing before any change, and the gate fails only on new
  failures from then on.
- A single gate exists, installed by hooks, and passes on the final commit.
- Each commit holds one step of Step 2b's order, and none mixes a refactor with a behaviour change.
- `average([])` keeps its behaviour: its fix is an owner decision in the report, since the failing test and the code
  disagree on what it should do.
- `parse_amount`'s swallowed error is either fixed in its own commit with a test that reproduces it, or reported as
  an owner decision, because returning `0` for bad input is behaviour callers may rely on.
- A README and an `AGENTS.md`, with `CLAUDE.md` as a symlink to it.
- A score run before the first change and one after the last, then an elevate run, all in `.best-software.json`,
  and a report with the sections of Step 2b's report format, its global score shown before → after. While
  `parse_amount` keeps its silent fallback, the after score stays capped at 4.0, whatever the owner decided.

It fails if any commit has a red gate on a failure the baseline does not record, if behaviour changes in a commit
that does not say so, or if the agent deletes or rewrites the failing test to make it pass.
