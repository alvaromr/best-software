#!/bin/sh
# The gate: the mechanical tests over the skill. The pre-commit hook runs it.
cd "$(dirname "$0")/.." && exec python3 -B -m unittest discover --quiet --start-directory tests
