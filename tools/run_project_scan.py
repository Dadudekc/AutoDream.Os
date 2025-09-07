#!/usr/bin/env python
"""
Runs the ProjectScanner from repo root and stages snapshot artifacts.
- Safe to call from pre-commit.
- If files change, pre-commit will halt; commit again to include updates.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import your scanner implementation from its module location.
try:
    from tools.projectscanner import ProjectScanner
except Exception:  # pragma: no cover - import failure path
    # Fallback: try relative import if the class is defined in this same file.
    print(
        "ERROR: Unable to import ProjectScanner. Update import path in tools/run_project_scan.py.",
        file=sys.stderr,
    )
    sys.exit(2)

def run() -> None:
    repo_root = REPO_ROOT
    # Ensure we execute from repo root (so output lands at project root)
    try:
        import os
        os.chdir(repo_root)
    except Exception:
        pass

    scanner = ProjectScanner(project_root=".")
    scanner.scan_project()
    # Optional: turn on features by default; flags are kept to mirror CLI behavior
    scanner.generate_init_files(overwrite=True)
    scanner.categorize_agents()
    scanner.report_generator.save_report()
    scanner.export_chatgpt_context()

    # Stage artifacts so a single re-commit includes them.
    artifacts = [
        "project_analysis.json",
        "test_analysis.json",
        "chatgpt_project_context.json",
        "dependency_cache.json",
    ]
    # Only stage files that exist
    existing = [p for p in artifacts if Path(p).exists()]
    if existing:
        try:
            subprocess.run(["git", "add", *existing], check=False)
        except Exception:  # pragma: no cover - staging is best effort
            # Staging is best-effort; pre-commit will still stop if working tree changed
            pass

if __name__ == "__main__":
    run()
