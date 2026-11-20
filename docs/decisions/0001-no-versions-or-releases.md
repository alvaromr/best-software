# No version numbers, tags or releases

- **Date:** 2026-11-19
- **Decided by:** the owner
- **Practices set aside:** a single version source, SemVer, immutable tags and a scripted release
  (`references/release.md`, "Versioning" and "Build").

## Context
The skill is installed by cloning the repository, and the installed copy is the working tree, so users take whatever
`main` holds. Nothing is built or packaged.

## Why the value is not at stake
A version exists so that one name identifies exactly one artifact (correctness and truth). Here the artifact is the
commit: every run record names the skill's commit sha and date (`SKILL.md`, "Run record"), and `CHANGELOG.md` lists
what changed for agents under each date. A version number would add a release process without identifying anything
the sha does not.

## Rejected alternative
GitHub releases with SemVer tags, as some published skills use. They help users who pin a version, which no one does
yet. Revisit when someone asks to pin one, or when the skill is packaged.
