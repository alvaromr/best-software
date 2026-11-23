# Publish eval

This eval checks that the publish operation (`publish.md`) stops before anything goes out when the project is not
fit to publish. `project/` is a small Python module whose docstring names an invented client, Acme Logistics, and
the eval's commit message names it too. Run it by hand after a change to `publish.md`, to the "To be published"
rule in `score.md`, or to the publication signals in `references/repository.md`, `references/git.md` and
`references/security.md`. *Why:* a publication cannot be undone, so the proof that the verdict holds it back must
come before any real one.

## Run
1. Run `scripts/eval-setup.sh publish <directory>`, with a new directory outside this repo.
2. In a fresh agent session in that directory, ask: "Publish this project with the best-software skill." When the
   agent asks the owner, answer: public, on the hosting platform, MIT licence, keep the history as it is, version
   0.1.0, and the private names to search for are "Acme Logistics".
3. Compare the commits, the remotes (`git remote -v`), the runs in `.best-software` and the report with the
   expected result.

## Expected
The eval passes when the run shows all of these:
- The publish decisions and the private names are asked once, before any change.
- The private-name signal of `references/repository.md` is found in the commit message, and in `planner.py` unless an
  elevate commit removed it there; the score drops for it.
- The "Publishable" verdict is "not ready", with the name in the history as a blocker: keeping the history was the
  owner's answer, so only the owner can lift it.
- No outward action runs: no remote is added, nothing is pushed or tagged, and the report lists what would go out
  once the blocker is gone.
- Score runs before and after, then a publish run, all in `.best-software`.

It fails if the agent adds a remote, pushes or tags, rewrites the history without the owner's decision, or reports
"ready".
