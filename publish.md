# Best software — publish

Publishes a project, or shares it beyond its owner: elevate (`elevate.md`) with the profile set to be published,
then the release when the project distributes an artifact, the verdict, and the publication itself after the owner's
yes. This file holds only what publishing adds; every other step is elevate's. *Why:* publishing is elevate plus a
point of no return, so the steps before that point stay in one place.

## Procedure
1. **Profile the project as to be published** (`SKILL.md`, "Profile the project"), and ask the owner its one
   upfront question: the publish decisions and the names linked to them. *Why:* with every decision known at the
   start, the run can reach the verdict without stopping.
2. **Elevate the project** (`elevate.md`). Its scores count every public-repo practice and end in the "Publishable"
   verdict (`score.md`, "Rules"). Apply the owner's decisions as elevate's fixes, such as the licence file or a
   history squash, each in its own commit.
3. **Prepare the release** when the project distributes an artifact: the version, the changelog entry and the
   scripted release with its dry run, as `references/release.md` asks in "Versioning" and "Build". *Why:* the
   release is part of what goes out, so it is ready before the verdict that lets anything out.
4. **State the verdict.** If it is "not ready", report the blockers and stop. *Why:* a publication cannot be undone,
   so it starts only from a verdict with no blockers.
5. **List every outward action** and wait for the owner's yes over the whole list: create or reconfigure the
   repository, push, tag, release, and the platform settings the project needs, such as its description, topics and
   private vulnerability reporting (`references/toolchains.md`). *Why:* each of these reaches people outside the
   repo; one explicit yes over the complete list is the owner's informed decision, and a yes to a partial list is not.
6. **Run the list** with the project's release script, or else the hosting platform's tool
   (`references/toolchains.md`). Stop at the first failure and report it. *Why:* the script is the project's own
   verified way to publish, and continuing after a failure publishes something the owner did not approve.
7. **Verify the publication:** install a fresh copy from the remote, as a user would, and run its smoke test; then
   read back each platform setting from the platform. *Why:* what was pushed is not proof of what the public gets,
   and a setting such as private vulnerability reporting can silently stay off.
8. **Record the run** (`SKILL.md`, "Run record") and **report** in elevate's format, with a final "Published"
   section: what went out, where, and what the verification showed.
