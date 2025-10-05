#!/usr/bin/env python3
"""
Loads scanner metrics and enforces pass-3 gates:
- Max Python files threshold (moving target)
- 0 V2 violations gate (optional: warn-only)
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THRESHOLDS = {"py_files": 600, "v2_violations": 0}
CANDIDATES = [
  ROOT/"project_analysis.json",
  ROOT/"runtime/projectscan/project_analysis.json",
  ROOT/"runtime/analysis/project_analysis.json",
  ROOT/"runtime/reports/project_analysis.json",
]

def load():
    for p in CANDIDATES:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    print("❌ analysis report not found", file=sys.stderr); sys.exit(2)

def main()->int:
    data = load()
    file_stats = data.get("file_statistics", {})
    py = file_stats.get("python_files", 0)
    v2 = data.get("v2_compliance", {})
    noncompliant = v2.get("violation_files", 0)
    ok = True
    if py > THRESHOLDS["py_files"]:
        print(f"❌ Gate fail: py_files {py} > {THRESHOLDS['py_files']}"); ok=False
    else:
        print(f"✅ py_files {py} ≤ {THRESHOLDS['py_files']}")
    if noncompliant > THRESHOLDS["v2_violations"]:
        print(f"❌ Gate fail: V2 violations {noncompliant} > {THRESHOLDS['v2_violations']}")
        # non-blocking for first pass; exit 0 but print warning. Flip to blocking later.
    else:
        print("✅ V2 violations == 0")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
