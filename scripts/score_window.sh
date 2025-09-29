#!/bin/bash
set -euo pipefail
WINDOW="${1:-runtime/windows/current}"
OUT="${2:-captain_progress_data/latest_progress.json}"
python -m analytics.score_window --window "$WINDOW" --out "$OUT"
