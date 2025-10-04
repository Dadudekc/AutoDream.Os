#!/usr/bin/env python3
"""
Consolidation Scanner (Scoped)
===============================

Finds exact + near duplicates in onboarding/ and discord/ systems.
Outputs JSON report + human md summary.

V2 Compliance: ≤400 lines, focused duplicate detection
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [
    ROOT / "src" / "services",
    ROOT / "tools",
]
FOCUS_KEYWORDS = ["onboard", "onboarding", "discord", "devlog", "webhook", "post", "messaging"]


def is_focus_file(p: Path) -> bool:
    """Check if file matches focus keywords."""
    s = str(p).lower()
    return any(k in s for k in FOCUS_KEYWORDS) and p.suffix in {".py", ".md"}


def normalize_text(txt: str) -> str:
    """Remove comments/blank lines, collapse whitespace."""
    lines = []
    for line in txt.splitlines():
        if line.strip().startswith("#"):
            continue
        lines.append(re.sub(r"\s+", " ", line.strip()))
    return "\n".join(lines).strip()


def sha256_norm(p: Path) -> str:
    """Calculate normalized SHA256 hash of file content."""
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
        norm = normalize_text(t)
        return hashlib.sha256(norm.encode()).hexdigest()
    except Exception:
        return ""


def ast_signature(p: Path) -> tuple[int, int, list[str]]:
    """Extract AST signature: function count, class count, symbols."""
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(t)
        funcs = sorted({n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)})
        classes = sorted({n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)})
        return (len(funcs), len(classes), funcs + classes)
    except Exception:
        return (0, 0, [])


def near_similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two texts."""
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def scan() -> dict:
    """Main scanning function."""
    files: list[Path] = []

    # Collect focus files
    for base in SCAN_DIRS:
        if base.exists():
            for p in base.rglob("*.py"):
                if is_focus_file(p):
                    files.append(p)

    # Also scan root level for discord files
    for p in ROOT.glob("*.py"):
        if is_focus_file(p):
            files.append(p)

    exact: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}
    texts: dict[str, str] = {}

    # Process each file
    for p in files:
        try:
            h = sha256_norm(p)
            if h:  # Only process if hash calculation succeeded
                rel_path = str(p.relative_to(ROOT))
                exact.setdefault(h, []).append(rel_path)

                raw = p.read_text(encoding="utf-8", errors="ignore")
                texts[rel_path] = normalize_text(raw)

                fcount, ccount, sig = ast_signature(p)
                meta[rel_path] = {
                    "functions": fcount,
                    "classes": ccount,
                    "symbols": sig,
                    "size": len(raw),
                    "lines": len(raw.splitlines()),
                }
        except Exception as e:
            print(f"Warning: Error processing {p}: {e}")

    # Find near-duplicate pairs
    near = []
    rels = list(texts.keys())
    for i in range(len(rels)):
        for j in range(i + 1, len(rels)):
            a, b = rels[i], rels[j]
            sim = near_similarity(texts[a], texts[b])
            if sim >= 0.86:  # Moderate threshold
                near.append({"a": a, "b": b, "similarity": round(sim, 4)})

    # Summarize results
    exact_groups = [v for v in exact.values() if len(v) > 1]

    report = {
        "root": str(ROOT),
        "focus_keywords": FOCUS_KEYWORDS,
        "scan_dirs": [str(d) for d in SCAN_DIRS],
        "exact_groups": exact_groups,
        "near_pairs": near,
        "meta": meta,
        "totals": {
            "files_scanned": len(files),
            "exact_dup_groups": len(exact_groups),
            "near_dup_pairs": len(near),
            "total_duplicates": len(exact_groups) + len(near),
        },
    }

    # Write output files
    outdir = ROOT / "runtime" / "consolidation"
    outdir.mkdir(parents=True, exist_ok=True)

    # JSON report
    json_file = outdir / "dup_report.json"
    json_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Markdown summary
    md_lines = [
        "# Consolidation Scan Report (Scoped: onboarding + discord)",
        "",
        f"- **Files scanned**: {len(files)}",
        f"- **Exact duplicate groups**: {len(exact_groups)}",
        f"- **Near-duplicate pairs**: {len(near)}",
        f"- **Total duplicates found**: {len(exact_groups) + len(near)}",
        "",
        "## Exact Duplicate Groups:",
        "",
    ]

    for i, group in enumerate(exact_groups[:20], 1):
        md_lines.append(f"{i}. {', '.join(group)}")

    if len(exact_groups) > 20:
        md_lines.append(f"... and {len(exact_groups) - 20} more groups")

    md_lines.extend(["", "## Top Near-Duplicate Pairs (similarity ≥ 86%):", ""])

    for i, pair in enumerate(near[:20], 1):
        md_lines.append(f"{i}. **{pair['similarity']:.1%}** similarity:")
        md_lines.append(f"   - `{pair['a']}`")
        md_lines.append(f"   - `{pair['b']}`")
        md_lines.append("")

    if len(near) > 20:
        md_lines.append(f"... and {len(near) - 20} more pairs")

    md_lines.extend(
        [
            "",
            "## Consolidation Recommendations:",
            "",
            "### High Priority (Exact Duplicates):",
            "- Remove duplicate files, keep canonical versions",
            "- Update imports to point to canonical modules",
            "",
            "### Medium Priority (Near Duplicates):",
            "- Review similar files for merge opportunities",
            "- Consider creating shim modules for backward compatibility",
            "",
            "### Canonical Modules Identified:",
            "- **Onboarding**: `src/services/agent_hard_onboarding.py`",
            "- **Discord**: `src/services/discord_commander/discord_post_client.py`",
            "",
        ]
    )

    md_file = outdir / "dup_report.md"
    md_file.write_text("\n".join(md_lines), encoding="utf-8")

    print("✅ Scan complete!")
    print(f"   Files scanned: {len(files)}")
    print(f"   Exact duplicates: {len(exact_groups)} groups")
    print(f"   Near duplicates: {len(near)} pairs")
    print("   Reports written:")
    print(f"     - {json_file}")
    print(f"     - {md_file}")

    return report


if __name__ == "__main__":
    scan()
