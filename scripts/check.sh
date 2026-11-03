#!/bin/sh
# The gate: the mechanical tests over the skill. The pre-commit hook runs it; in a clone without the hooks, it
# installs them first, since git never runs a repo's hooks until core.hooksPath points to them.
cd "$(dirname "$0")/.." || exit 1
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ "$(git config --get core.hooksPath)" != .githooks ]; then
  git config core.hooksPath .githooks && echo "Installed the hooks: core.hooksPath = .githooks" >&2
fi
exec python3 -B -m unittest discover --quiet --start-directory tests
