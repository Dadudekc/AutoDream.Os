"""Reporting utilities for V2 standards checker.

The reporter receives result dictionaries from the core module and prints
human friendly summaries. Keeping printing separate from validation makes
it easy to reuse the checker in automated environments where plain data
structures are preferred.
"""

from typing import Dict, Any


def _percent(part: int, whole: int) -> float:
    return (part / whole * 100) if whole else 0.0


def print_summary(results: Dict[str, Any]) -> None:
    """Print overall compliance summary."""
    total = results.get("total_files", 0)
    compliant = results.get("compliant_files", 0)
    rate = _percent(compliant, total)
    print("V2 CODING STANDARDS SUMMARY")
    print("=" * 32)
    print(f"Total Files: {total}")
    print(f"Compliant Files: {compliant}")
    print(f"Compliance: {rate:.1f}%")

    for key in ["loc", "oop", "cli", "srp"]:
        violations = results.get(f"{key}_violations", 0)
        if violations:
            print(f"- {key.upper()} Violations: {violations}")


def print_loc_details(results: Dict[str, Any]) -> None:
    """Print LOC specific violations."""
    violations = results.get("violations", [])
    if not violations:
        print("No LOC violations detected.")
        return
    print("LOC Violations:")
    for v in violations:
        msg = v.get("message", "")
        print(f"- {v['file']}: {msg}")
