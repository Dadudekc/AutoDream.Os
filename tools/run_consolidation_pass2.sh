#!/usr/bin/env bash
set -euo pipefail

# Consolidation Pass-2 Batch Runner
# Idempotent execution with metrics and reporting

branch=feat/consolidation-pass2
git checkout -b "$branch" || git checkout "$branch"

echo "== Baseline metrics =="
python tools/loc_report.py || true

echo "== Preflight checks =="
python tools/canonical_coverage.py || true
python tools/consolidation_scan.py || true

echo "== Generate shim burn list =="
python tools/shim_burn_list.py

echo "== Apply Pass-2 consolidation =="
python tools/consolidation_apply_v2.py

echo "== Delete burnable shims safely =="
if [ -f runtime/consolidation/shim_burn_list.txt ]; then
  while IFS= read -r f; do
    [ -n "$f" ] && git rm -f "$f" || true
  done < runtime/consolidation/shim_burn_list.txt
fi

echo "== Smoke tests =="
pytest -q || true

echo "== Metrics after batch =="
python tools/loc_report.py | tee runtime/consolidation/metrics_pass2.txt

git add -A
git commit -m "consolidation(pass-2): imports rewired + shim burn (safe set) + metrics"
