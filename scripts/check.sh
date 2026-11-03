#!/bin/sh
# The gate: the mechanical checks over the skill. The pre-commit hook runs it.
exec python3 "$(dirname "$0")/check.py"
