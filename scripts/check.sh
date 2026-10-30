#!/bin/sh
# The gate: the tests of the checks, then the checks over the skill. The pre-commit hook runs it.
set -e
cd "$(dirname "$0")/.."
python3 -m unittest discover --quiet --start-directory tests
python3 scripts/check.py
