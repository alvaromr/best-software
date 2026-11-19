# Best software — bootstrap

Starts a new project at the bar, with the gate before any feature. The profile, the run record and the project guide
template are in `SKILL.md`.

## Procedure
1. **Agree on the profile and the shape of the core** (`SKILL.md`, "Profile the project"): the domain modules and the
   adapters at the edges.
2. **Scaffold the repository** (`references/repository.md`):
   - layout
   - root files
   - `.gitignore`, `.editorconfig`
   - toolchain pin and lockfile
   - env template if needed
3. **Install the gate, its hooks and the mutation config before any feature** (`references/tooling.md`, "The
   gate"; `references/testing.md`; `references/toolchains.md`). *Why:* quality added later means fixing a backlog;
   installed first, it means never creating one.
4. **Write a walking skeleton:** one end-to-end path through core and adapter, with its tests, and the gate green.
   *Why:* it proves the architecture and the gate before features depend on them.
5. **Write the project guide** (`SKILL.md`, "Project guide template") and the README.
6. **Make the first commit:** the skeleton, green, in the agreed convention.
7. **Build every feature test-first** (`references/testing.md`), one atomic commit per step (`references/git.md`).
   Each commit passes the coherence review (`references/docs.md`, "Content rules").
8. **Add release artifacts** (`references/release.md`) once something is distributable.
9. **Record the run** (`SKILL.md`, "Run record").
