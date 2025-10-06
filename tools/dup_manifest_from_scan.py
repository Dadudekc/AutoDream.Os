#!/usr/bin/env python3
"""
Reads Project Scanner JSON for duplicate hints (if present) and creates:
- runtime/pass3/dup_manifest.json (actions: delete|merge review)
- runtime/pass3/dup_review.md (human checklist)
Safe to run even if duplicates are not present; produces empty manifest.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT/"runtime"/"pass3"
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
    return {}

def main()->int:
    data = load()
    dup_groups = data.get("duplicates") or data.get("duplicate_groups") or []

    manifest = {"version": 1, "actions": []}
    md = ["# Duplicate Consolidation Review", f"Groups: {len(dup_groups)}", ""]
    for g in dup_groups:
        files = g.get("files", g)  # support simple list form
        md.append("- " + " | ".join(files))
        # Draft action (review-first; not auto-delete)
        manifest["actions"].append({"files": files, "action": "review"})

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR/"dup_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUTDIR/"dup_review.md").write_text("\n".join(md), encoding="utf-8")
    print(f"✅ wrote {OUTDIR/'dup_manifest.json'} and {OUTDIR/'dup_review.md'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

