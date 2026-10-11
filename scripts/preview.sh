#!/usr/bin/env bash
# scripts/preview.sh — Serve the GFMR reference website for local preview.
#
# Copyright 2026 Saltfoss Energy ApS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -euo pipefail
cd -- "$(dirname -- "$0")/.."
if [[ ! -x .venv/bin/mkdocs ]]; then
  printf '%s\n' 'Set up the project first:' '  python3 -m venv .venv' '  .venv/bin/python -m pip install -r requirements.txt'
  exit 1
fi
exec .venv/bin/mkdocs serve --dev-addr 127.0.0.1:8000 "$@"
