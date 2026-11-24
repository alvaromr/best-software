# Best software — elevate

Raises an existing project to the bar: it scores the project, fixes it in a fixed order, and scores it again. The
profile, the run record and the project guide template are in `SKILL.md`.

## Procedure
1. **Prepare the branch:**
   - **If the project is a git repo:** check that the tree is clean. If it is dirty, stop and ask (hard constraint 7).
     Then update the default branch. If the project integrates through pull requests (`references/git.md`), create
     a clean branch from it (`chore/engineering-baseline`, or one per topic).
   - **If the project is not a git repo:** ask whether to initialise one before changing anything. Otherwise, deliver
     the score only.
2. **Score the project** (`score.md`), recording its own score run. That run is the "before", and its signals are
   the findings to fix, ranked by what each fix recovers. Record each failure the existing build or tests already
   have as the baseline: until it is fixed, the gate fails only on new failures (hard constraint 3). A failing test
   stays as written: whether the test or the code is right is an owner decision, and characterization tests pin only
   what no test already states.
   *Why:* without a "before" there is no proof of improvement, and one assessment, in one place, keeps elevate and
   scoring from judging the same project differently; a failing test may be the only record of what the code was
   meant to do.
3. **Fix directly, in this order.** Each step is its own atomic commit with the gate green. *Why:* the order builds the
   safety net before anything that could break.
   1. Safety net: characterization tests around anything you will touch.
   2. Gate and hooks, as a ratchet on legacy code (`references/tooling.md`).
   3. Secrets and security fixes. A leaked secret is reported to the owner at once, for rotation.
   4. Repository hygiene and toolchain pin.
   5. Structure and code refactors, under tests, with no behaviour change.
   6. Tests up to the coverage target (`references/testing.md`, "Coverage").
   7. Docs and the project guide (`SKILL.md`, "Project guide template").
   8. Release artifacts.
4. **Behaviour is frozen during the pass** (hard constraint 6). When you find a real bug:
   - **If the fix is safe:** fix it in its own `fix:` commit with a reproducing test.
   - **Otherwise:** report it.

   Ask before any change the constitution's "How to decide" leaves to the owner.
5. **Verify:**
   1. Run the full gate.
   2. Run the app, CLI or package as a user would.
   3. Run the coherence review over the whole repo, and fix whatever disagrees.
   4. Score the project again, recording a second score run. Its comparison with the first is the "after".
6. **Record the run** (`SKILL.md`, "Run record").
7. **Report** in the format below.

## Report format

```markdown
## Profile
<kind · stack · audience · constraints>

## Baseline
<global score, gate state, coverage, number of signals — before → after>

## Done
1. <commit subject> — <topic>

## Deferred
1. <finding> — <why it is deferred> — <proposed fix>

## Decisions for the owner
1. <decision> — <options> — <recommendation>
```
