#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
if [[ ! -x .venv/bin/mkdocs ]]; then
  printf '%s\n' 'Set up the project first:' '  python3 -m venv .venv' '  .venv/bin/python -m pip install -r requirements.txt'
  exit 1
fi
exec .venv/bin/mkdocs serve --dev-addr 127.0.0.1:8000 "$@"
