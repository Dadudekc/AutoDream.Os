#!/usr/bin/env python
"""
Pre-push enforcement:
- Re-run scanner
- If any snapshot artifacts differ from HEAD, fail with actionable message.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Adjust import like in run_project_scan.py
try:
    from tools.projectscanner import ProjectScanner
except Exception:  # pragma: no cover - import failure path
    print(
        "ERROR: Unable to import ProjectScanner. Update import path in tools/check_snapshot_up_to_date.py.",
        file=sys.stderr,
    )
    sys.exit(2)

ARTIFACTS = [
    "project_analysis.json",
    "test_analysis.json",
    "chatgpt_project_context.json",
    "dependency_cache.json",
]

def git_diff_has_changes(paths: list[str]) -> bool:
    # Check index vs HEAD after regeneration
    cmd = ["git", "diff", "--quiet", "--"] + paths
    result = subprocess.run(cmd)
    return result.returncode != 0

def main() -> None:
    repo_root = REPO_ROOT
    try:
        import os
        os.chdir(repo_root)
    except Exception:
        pass

    # Re-generate snapshots
    scanner = ProjectScanner(project_root=".")
    scanner.scan_project()
    scanner.generate_init_files(overwrite=True)
    scanner.categorize_agents()
    scanner.report_generator.save_report()
    scanner.export_chatgpt_context()

    # If artifacts changed relative to HEAD, block push.
    existing = [p for p in ARTIFACTS if Path(p).exists()]
    if not existing:
        # Nothing to enforce
        sys.exit(0)

    if git_diff_has_changes(existing):
        print(
            "\n❌ Snapshots out of date.\n"
            "   I just regenerated snapshots and they differ from HEAD.\n"
            "   ➜ Action: `git add project_analysis.json test_analysis.json chatgpt_project_context.json dependency_cache.json`\n"
            "             `git commit -m \"chore(snapshots): refresh project analysis\"`\n"
            "             Then push again.\n",
            file=sys.stderr,
        )
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
