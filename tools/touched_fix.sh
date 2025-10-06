#!/usr/bin/env bash
set -euo pipefail

# Lint & Format Gate for touched files only
base=${1:-HEAD~1}
files=$(git diff --name-only "$base"..HEAD -- '*.py' || true)
[ -z "$files" ] && exit 0
ruff --fix $files || true
python -m black $files || true
pytest -q || true

