#!/bin/bash
# FSM CI Script - V2 Compliant
# =============================
# 
# Finite State Machine CI validation script.
# Scans state files and runs consistency tests.
#
# Author: Agent-4 (Captain & Operations Coordinator)
# License: MIT

set -euo pipefail

echo "[FSM] Starting FSM CI validation..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "runtime/fsm/fsm_spec.yaml" ]; then
    echo "❌ Error: FSM specification not found. Run from project root."
    exit 1
fi

echo "[FSM] Scanning state files..."
python tools/fsm/fsm_scan.py
SCAN_EXIT_CODE=$?

if [ $SCAN_EXIT_CODE -ne 0 ]; then
    echo "❌ FSM scan failed with exit code $SCAN_EXIT_CODE"
    exit $SCAN_EXIT_CODE
fi

echo ""
echo "[FSM] Running consistency tests..."
if command -v pytest &> /dev/null; then
    pytest -q tests/test_fsm_consistency.py
    TEST_EXIT_CODE=$?
else
    echo "⚠️  pytest not found, running with python -m pytest"
    python -m pytest -q tests/test_fsm_consistency.py
    TEST_EXIT_CODE=$?
fi

if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "❌ FSM tests failed with exit code $TEST_EXIT_CODE"
    exit $TEST_EXIT_CODE
fi

echo ""
echo "[FSM] ✅ All FSM validations passed!"
echo "=================================="
echo "✅ State file scan: PASSED"
echo "✅ Consistency tests: PASSED"
echo "✅ FSM system: VALID"
echo ""
echo "🎉 FSM CI validation complete - system ready!"




