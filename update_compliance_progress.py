#!/usr/bin/env python3
"""Update V2 compliance progress tracker with current metrics."""

from datetime import date

from analyze_violations import analyze_violations


def main() -> None:
    summary = analyze_violations(report=False)
    total_files = summary["total_files"]
    total_violations = len(summary["violations"])
    compliant_files = total_files - total_violations
    compliance_pct = compliant_files / total_files * 100
    non_compliant_pct = 100 - compliance_pct

    tracker = "V2_COMPLIANCE_PROGRESS_TRACKER.md"
    with open(tracker, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("**Current Compliance**"):
            lines[i] = (
                f"**Current Compliance**: {compliance_pct:.1f}% "
                f"({compliant_files}/{total_files} files)\n"
            )
        elif line.startswith("**Target Compliance**"):
            lines[i] = (
                f"**Target Compliance**: 100% " f"({total_files}/{total_files} files)\n"
            )
        elif line.startswith("**Last Updated**"):
            lines[i] = f"**Last Updated**: {date.today().isoformat()}\n"
        elif line.startswith("- **Total Files**:"):
            lines[i] = f"- **Total Files**: {total_files}\n"
        elif line.startswith("- **Compliant Files**:"):
            lines[i] = (
                f"- **Compliant Files**: {compliant_files} "
                f"({compliance_pct:.1f}%)\n"
            )
        elif line.startswith("- **Non-Compliant Files**:"):
            lines[i] = (
                f"- **Non-Compliant Files**: {total_violations} "
                f"({non_compliant_pct:.1f}%)\n"
            )

    with open(tracker, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Updated {tracker} with current metrics.")


if __name__ == "__main__":
    main()
