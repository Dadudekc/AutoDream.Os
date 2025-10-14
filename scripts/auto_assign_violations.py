#!/usr/bin/env python3
"""
Auto-Assign Violations to Agents via Gasline
Commander's directive: "Get agents working on violations"
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.gasline_integrations import GaslineHub
import json


def find_violations():
    """Find all V2 violations (files >400 lines)"""
    violations = []
    src_dir = Path("src")
    
    for py_file in src_dir.rglob("*.py"):
        try:
            lines = len(py_file.read_text(encoding='utf-8').splitlines())
            if lines > 400:
                violations.append({
                    "file": str(py_file),
                    "lines": lines,
                    "severity": "MAJOR" if lines > 600 else "MEDIUM",
                    "complexity": lines  # Approximation
                })
        except:
            pass
    
    return sorted(violations, key=lambda x: x['lines'], reverse=True)


def main():
    print("🔍 SCANNING FOR V2 VIOLATIONS...")
    
    violations = find_violations()
    
    if not violations:
        print("✅ No V2 violations found!")
        return
    
    print(f"\n📊 FOUND {len(violations)} V2 VIOLATIONS:\n")
    for v in violations[:10]:
        print(f"  • {v['file']:60} {v['lines']:4d} lines ({v['severity']})")
    
    print(f"\n⚡ AUTO-ASSIGNING TO AGENTS VIA GASLINE...")
    
    # Activate gasline integration
    hub = GaslineHub()
    success = hub.hook_violations_found(violations, auto_assign=True)
    
    if success:
        print(f"\n✅ {len(violations)} violations assigned and GAS delivered!")
        print("\nAgents will receive:")
        print("  • Violation list")
        print("  • Point values")
        print("  • Execution steps")
        print("  • PyAutoGUI activation")
    else:
        print("\n❌ Auto-assignment failed - check logs")


if __name__ == "__main__":
    main()

