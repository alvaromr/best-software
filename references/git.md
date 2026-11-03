# Git history and commits

**Goal:** history is a product. Every commit is a small, green, revertible, self-explaining step. The repository, not a
server or a chat, is the single source of truth. This serves truth, correctness and safety.

## Practices

### Commits
- **Make each commit atomic:** one logical change that builds and passes the gate. Keep separate:
  - refactors from behaviour changes
  - renames (`git mv`)
  - formatting churn
  - version bumps

  *Why:* an atomic commit can be reviewed, reverted and bisected alone, and a mixed one hides behaviour changes inside
  noise.
- **Commit a checkpoint before a risky or large change.** *Why:* the way back must exist before you need it.
- **Stage explicit paths,** and check the result with `git status` and `git log -1`. *Why:* blind staging commits
  secrets and scratch files, and exit codes do not show what was committed.
- **Never commit with the gate red or bypass hooks.** *Why:* a red commit breaks bisect and every branch cut from it.
- **Squash WIP checkpoints before integration,** with a pre-push guard against `WIP` commits. *Why:* the integrated
  history should explain the change, not replay the process.

### Messages
- **Write messages in English and the imperative.** The subject is ≤72 characters and describes the observable outcome
  for whom it changes; the body explains *why* when not obvious. *Why:* history is read to understand intent, and the
  diff already shows what.
- **Use one convention per repo:**
  - New repos default to Conventional Commits (`feat(scope): …`, `fix`, `refactor`, `test`, `docs`, `perf`,
    `chore(release): vX.Y.Z`), with a ticket key when work is tracked.
  - Existing repos keep their established prefix (ticket key, scope). The subject style above applies to their new
    commits.
  - Past commits are never rewritten to match a convention.
  - A `commit-msg` hook validates it.

  *Why:* a consistent convention enables changelog generation and scanning. Rewriting old messages buys only
  cosmetics, at the price of breaking every clone and every reference to those commits.
- **Set a per-repo author identity when it differs from the global one** (for example, personal vs work email). *Why:*
  authorship and accountability belong to the right identity of the person.

### Branches and integration
- **Use short-lived branches cut from the up-to-date default branch,** and rebase before integration. History stays
  linear, without merge commits. *Why:* linear history bisects cleanly, and long branches accumulate conflicts.
- **Never rewrite published history or force-push shared branches;** revert, or re-do properly. *Why:* others built on
  it, and rewriting breaks their clones silently.
- **Before rewriting any history, even unpublished, look for references to the affected commit ids.** They can live
  in tool and plugin registries, deploy configs, docs, notes and caches.
  - Rewrite only when every reference can be updated.
  - Back up first.
  - Map each old commit to its new one by tree, date and message.
  - Update the references in the same operation.

  *Why:* a commit id is a pointer that other systems hold, and rewriting leaves every holder pointing at nothing.
- **Tags are immutable and identify exactly the artifact built,** enforced by a hook. *Why:* a moved tag makes "version
  X" mean two different things.
- **Pin submodules to the last audited commit,** and move them deliberately. *Why:* a submodule is a dependency, and it
  gets reviewed like one.

### Source of truth
- **Reflect every change made on a server or device in the repo,** secrets excepted. *Why:* server drift is
  undocumented state that the next deploy destroys.
- **When a secret leaks into history, rotate it first, then purge it** (`security.md`, "Secrets"). *Why:* deleting
  the file does not delete the commit, and only rotation makes the leak harmless.
- **Before publishing, audit the full history** for secrets, personal data, third-party material and anything tied to
  one developer, which should never have entered (criterion in `repository.md`). Squash when the history is unfit to publish. *Why:*
  publishing exposes every past commit, not just the tree.
- **Deliver code to clients as a snapshot commit, without internal history or trailers.** *Why:* internal history is
  confidential context.

## Judgment
- On a solo project, direct commits to `main` are acceptable only through the same gate. For changes worth reviewing,
  branch and rebase.
- A ticket prefix is required only where work is tracked; never invent one.

## Audit signals
- Vague subjects such as "fix", "wip" or "changes".
- Mixed refactor and feature commits.
- Merge spaghetti.
- Secrets in `git log -p`.
- Moved tags.
- Assistant trailers.
- Server drift.
