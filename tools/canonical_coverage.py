#!/usr/bin/env python3
"""
Canonical Coverage Asserter
===========================

Asserts that canonical modules expose the expected unified APIs.
Failing this means we shouldn't delete alts yet.

V2 Compliance: ≤400 lines, focused coverage validation
Author: Agent-4 (Captain) - Strategic Oversight & Emergency Intervention
"""

from __future__ import annotations

import importlib

CANON = {
    "services.discord_commander.discord_post_client": [
        "DiscordPostClient",
    ],
    "services.agent_hard_onboarding": [
        "AgentHardOnboarder",
    ],
}


def check(module: str, symbols: list[str]) -> list[str]:
    """Check if module exposes required symbols."""
    try:
        # Add src to path for imports
        import sys
        from pathlib import Path

        src_path = Path(__file__).parent.parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        m = importlib.import_module(module)
    except Exception as e:
        return [f"import failed: {module} ({e})"]
    missing = [s for s in symbols if not hasattr(m, s)]
    return [f"{module} missing: {', '.join(missing)}"] if missing else []


def main() -> int:
    """Validate canonical coverage."""
    errs = []
    for mod, syms in CANON.items():
        errs += check(mod, syms)
    if errs:
        print("❌ canonical coverage errors:")
        for e in errs:
            print(" -", e)
        return 2
    print("✅ canonical coverage OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
