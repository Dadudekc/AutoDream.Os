"""
Runs the ProjectScanner from repo root and stages snapshot artifacts.
- Safe to call from pre-commit.
- If files change, pre-commit will halt; commit again to include updates.
"""

import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
try:
    from tools.projectscanner import ProjectScanner
except Exception:
    logger.info(
        "ERROR: Unable to import ProjectScanner. Update import path in tools/run_project_scan.py."
    )
    sys.exit(2)


def run() -> None:
    repo_root = REPO_ROOT
    try:
        import os

        os.chdir(repo_root)
    except Exception:
        pass
    scanner = ProjectScanner(project_root=".")
    scanner.scan_project()
    scanner.generate_init_files(overwrite=True)
    scanner.categorize_agents()
    scanner.report_generator.save_report()
    scanner.export_chatgpt_context()
    scanner.modular_reporter.generate_modular_reports()
    artifacts = [
        "project_analysis.json",
        "test_analysis.json",
        "chatgpt_project_context.json",
        "dependency_cache.json",
        "analysis/agent_analysis.json",
        "analysis/module_analysis.json",
        "analysis/file_type_analysis.json",
        "analysis/complexity_analysis.json",
        "analysis/dependency_analysis.json",
        "analysis/architecture_overview.json",
    ]
    existing = [p for p in artifacts if Path(p).exists()]
    if existing:
        try:
            subprocess.run(["git", "add", *existing], check=False)
        except Exception:
            pass


if __name__ == "__main__":
    run()
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
