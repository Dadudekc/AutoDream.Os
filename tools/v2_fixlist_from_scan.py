#!/usr/bin/env python3
"""
Reads Project Scanner JSON and produces:
- v2_fixlist.md: 9 violating files with LOC/class/func counts (if present)
- v2_fixlist.json: machine-readable list for automation
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = [
  ROOT/"project_analysis.json",
  ROOT/"runtime/projectscan/project_analysis.json",
  ROOT/"runtime/analysis/project_analysis.json",
  ROOT/"runtime/reports/project_analysis.json",
]

def load_report()->dict:
    for p in CANDIDATES:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    print("❌ project_analysis.json not found in known locations", file=sys.stderr)
    sys.exit(2)

def main()->int:
    data = load_report()
    v2 = data.get("v2_compliance", {})
    violations = v2.get("violations") or v2.get("non_compliant_files") or []
    # Normalize into list of dicts with path + metrics if present
    items = []
    for it in violations:
        if isinstance(it, str):
            items.append({"path": it})
        else:
            items.append(it)

    outdir = ROOT/"runtime"/"pass3"/"reports"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir/"v2_fixlist.json").write_text(json.dumps(items, indent=2), encoding="utf-8")

    lines = ["# V2 Fixlist (from Project Scanner)", f"Count: {len(items)}", ""]
    for i, it in enumerate(items, 1):
        p = it.get("path", "unknown")
        loc = it.get("loc", "?")
        classes = it.get("classes", "?")
        funcs = it.get("functions", "?")
        lines.append(f"{i}. `{p}`  — LOC:{loc}  classes:{classes}  funcs:{funcs}")
        lines.append(f"   - Action: split or refactor to ≤400 LOC / ≤5 classes / ≤10 funcs")

    (outdir/"v2_fixlist.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ wrote {outdir/'v2_fixlist.md'} and {outdir/'v2_fixlist.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
