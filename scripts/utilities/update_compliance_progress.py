#!/usr/bin/env python3
"""Update ``V2_COMPLIANCE_PROGRESS_TRACKER.md`` with current metrics."""

from datetime import date
from pathlib import Path

from analyze_violations import analyze_violations


def main(tracker: Path = Path("V2_COMPLIANCE_PROGRESS_TRACKER.md")) -> None:
    """Update the compliance tracker with fresh statistics.

    Args:
        tracker: Path to the Markdown file to update.
    """

    summary = analyze_violations(report=False)
    total_files = summary["total_files"]
    total_violations = len(summary["violations"])
    compliant_files = total_files - total_violations
    compliance_pct = (compliant_files / total_files * 100) if total_files else 0
    non_compliant_pct = (total_violations / total_files * 100) if total_files else 0

    lines = tracker.read_text(encoding="utf-8").splitlines(keepends=True)

    replacements = {
        "**Current Compliance**": (
            f"**Current Compliance**: {compliance_pct:.1f}% "
            f"({compliant_files}/{total_files} files)\n"
        ),
        "**Target Compliance**": (
            f"**Target Compliance**: 100% ({total_files}/{total_files} files)\n"
        ),
        "**Last Updated**": f"**Last Updated**: {date.today().isoformat()}\n",
        "- **Total Files**:": f"- **Total Files**: {total_files}\n",
        "- **Compliant Files**:": (
            f"- **Compliant Files**: {compliant_files} "
            f"({compliance_pct:.1f}%)\n"
        ),
        "- **Non-Compliant Files**:": (
            f"- **Non-Compliant Files**: {total_violations} "
            f"({non_compliant_pct:.1f}%)\n"
        ),
    }

    for i, line in enumerate(lines):
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                lines[i] = replacement
                break

    tracker.write_text("".join(lines), encoding="utf-8")
    print(f"Updated {tracker} with current metrics.")


if __name__ == "__main__":
    main()
