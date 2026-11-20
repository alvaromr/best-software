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
- **Hard constraint 3 holds on every commit, a local one included.** *Why:* a local commit gets pushed or branched
  from later, and its red spreads with it.
- **Squash WIP checkpoints before integration,** with a pre-push guard against `WIP` commits. *Why:* the integrated
  history should explain the change, not replay the process.

### Messages
- **Write messages in the imperative.** The subject is ≤72 characters and describes the observable outcome
  for whom it changes; the body explains *why* when not obvious. *Why:* history is read to understand intent, and the
  diff already shows what.
- **Use one convention per repo:**
  - New repos default to Conventional Commits (`feat(scope): …`, `fix`, `refactor`, `test`, `docs`, `perf`,
    `chore(release): vX.Y.Z`), with a ticket key when work is tracked.
  - Existing repos keep the convention their history establishes, in every part: type, ticket key, scope. A history
    without scopes gets none, so its release commit is `chore: vX.Y.Z`, not `chore(release): vX.Y.Z`. The subject
    style above applies to their new commits.
  - Past commits are never rewritten to match a convention.
  - Every script, hook and template that writes or checks messages (release script, `commit-msg` hook, changelog and
    release-note tooling) writes and accepts only that convention, and a `commit-msg` hook validates it.

  *Why:* a consistent convention enables changelog generation and scanning, and one tool that writes or accepts
  another format breaks it on every run. Rewriting old messages buys only cosmetics, at the price of breaking every
  clone and every reference to those commits.
- **Set a per-repo author identity when it differs from the global one** (for example, personal vs work email). *Why:*
  authorship and accountability belong to the right identity of the person.

### Branches and integration
- **Integrate the way the project already does.** If it integrates through pull requests, use a short-lived branch
  cut from the up-to-date default branch, and rebase before integration. Otherwise, commit to the default branch
  through the gate. History stays linear, without merge commits. *Why:* a branch exists for review and CI before
  integration, and without them it only adds steps; linear history bisects cleanly, and long branches accumulate
  conflicts.
- **Undo published work with a revert, or re-do it properly,** and never force-push a shared branch (hard
  constraint 8). *Why:* a force-push rewrites history that others pull.
- **Before rewriting any history, even unpublished, look for references to the affected commit ids.** They can live
  in tool and plugin registries, deploy configs, docs, notes and caches.
  - Rewrite only when every reference can be updated.
  - Back up first.
  - Map each old commit to its new one by tree, date and message.
  - Update the references in the same operation.

  *Why:* a commit id is a pointer that other systems hold, and rewriting leaves every holder pointing at nothing.
- **Tags are immutable and identify exactly the artifact built,** enforced by a hook. *Why:* a moved tag makes "version
  X" mean two different things.
  - Locally, a `reference-transaction` hook guards them, but it cannot tell `git update-ref -d <tag> <value>` from
    packing: `git pack-refs`, also run by `git gc`, deletes each loose tag that way once `packed-refs` holds it. So
    the hook refuses `git tag -d`, `git tag -f` and `git update-ref -d` without a value, and lets that one form
    through, since refusing it would break packing.
  - On the remote, a `pre-push` hook refuses a push that moves or deletes a remote tag.
- **Pin submodules to the last audited commit,** and move them deliberately. *Why:* a submodule is a dependency, and it
  gets reviewed like one.

### Source of truth
- **Reflect every change made on a server or device in the repo,** secrets excepted. *Why:* server drift is
  undocumented state that the next deploy destroys.
- **When a secret leaks into history, rotate it first, then purge it** (`security.md`, "Secrets"). *Why:* deleting
  the file does not delete the commit, and only rotation makes the leak harmless.
- **Before publishing, audit the full history** for secrets, personal data, third-party material and anything tied to
  one developer, which should never have entered (criterion in `repository.md`). Search with the secret scanner
  (`toolchains.md`) and with the names the owner listed as private, over every diff and every commit message, and
  check each author and committer email. Squash when the history is unfit to publish, as the owner decides. *Why:*
  publishing exposes every past commit, not just the tree, and a name in a message escapes a scan of the files.
- **Deliver code to clients as a snapshot commit, without internal history or trailers.** *Why:* internal history is
  confidential context.

## Judgment
- A ticket prefix is required only where work is tracked; never invent one. *Why:* an invented key points to no
  ticket and reads as tracked work.
- Commit times show when the author works. Say so to the owner before the first publication; rewriting the dates
  or squashing is their call. *Why:* working hours are personal, and published history cannot be recalled.

## Audit signals
- Vague subjects such as "fix", "wip" or "changes". `changeability`
- Mixed refactor and feature commits. `correctness`
- Merge spaghetti. `changeability`
- Secrets in `git log -p`. `safety`
- Moved tags. `truth`
- Assistant trailers. `truth`
- Server drift. `truth`
