#!/usr/bin/env python3
"""
Shim Burn Detector
==================

Find shim files safe to delete (no imports reference their module path).
Looks for 'Deprecated shim' signature and checks import graph by grep-like scan.

V2 Compliance: ≤400 lines, focused shim detection
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIG = "DEPRECATED: Use the canonical module directly"


def module_name(p: Path) -> str:
    """Convert file path to module name."""
    rel = p.relative_to(ROOT).as_posix().removesuffix(".py")
    return rel.replace("/", ".")


def main() -> int:
    """Find burnable shims."""
    shims = []
    for p in ROOT.rglob("*.py"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
            if SIG in t:
                shims.append(p)
        except Exception:
            pass

    py_files = [p for p in ROOT.rglob("*.py")]
    burn = []
    for shim in shims:
        mod = module_name(shim)
        imported = False
        for f in py_files:
            if f == shim:
                continue
            try:
                t = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if re.search(rf"\bfrom\s+{re.escape(mod)}\s+import\b", t) or re.search(
                rf"\bimport\s+{re.escape(mod)}\b", t
            ):
                imported = True
                break
        if not imported:
            burn.append(shim)

    out = ROOT / "runtime" / "consolidation" / "shim_burn_list.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(str(p) for p in burn), encoding="utf-8")
    print(f"🧯 burnable shims: {len(burn)} → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
