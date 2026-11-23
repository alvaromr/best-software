#!/bin/sh
# Prepares an eval's example project: copies evals/<eval>/project/ into a new empty directory outside this repo and
# commits it there as the only commit, with no remote, so the agent under test starts from a clean history.
# Usage: scripts/eval-setup.sh <eval> <directory>
fail() { echo "eval-setup: $1" >&2; exit 1; }
[ $# -eq 2 ] || fail "usage: scripts/eval-setup.sh <eval> <directory>"
repo=$(cd "$(dirname "$0")/.." && pwd -P) || exit 1
project="$repo/evals/$1/project"
[ -d "$project" ] || fail "$1 has no example project in evals/$1/project/"
# The publish eval checks that the private name in its history is found, so its message carries that name.
case $1 in
  publish) message="Add the route planner for Acme Logistics" ;;
  *) message="Add the example" ;;
esac
parent=$(cd "$(dirname "$2")" 2>/dev/null && pwd -P) || fail "the parent of $2 must exist"
case $parent/ in "$repo"/*) fail "$2 must be outside this repo" ;; esac
[ ! -e "$2" ] || [ -z "$(ls -A "$2")" ] || fail "$2 is not empty"
mkdir -p "$2" || exit 1
target="$parent/$(basename "$2")"
cp -R "$project/." "$target/" || exit 1
cd "$target" || exit 1
# Variables such as GIT_DIR, set when a hook runs this, would point git at another repo and commit there.
unset $(git rev-parse --local-env-vars)
git init --quiet && git add -A && git commit --quiet -m "$message" || exit 1
echo "eval-setup: $1 is ready in $target" >&2
