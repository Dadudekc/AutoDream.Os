import logging

logger = logging.getLogger(__name__)
"""
Runs the ProjectScanner from repo root and stages snapshot artifacts.
- Safe to call from pre-commit.
- If files change, pre-commit will halt; commit again to include updates.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
try:
    from tools.projectscanner.enhanced_scanner import EnhancedProjectScanner
except Exception:
    logger.info(
        "ERROR: Unable to import EnhancedProjectScanner. Update import path in tools/run_project_scan.py."
    )
    sys.exit(2)


def run() -> None:
    repo_root = REPO_ROOT
    try:
        import os

        os.chdir(repo_root)
    except Exception:
        pass
    scanner = EnhancedProjectScanner(project_root=".")
    
    # Progress callback for enhanced scanning
    def progress_callback(percent: int):
        if percent % 20 == 0:  # Log every 20%
            logger.info(f"📊 Enhanced scan progress: {percent}%")
    
    # Run enhanced scan with all features
    scanner.scan_project(progress_callback=progress_callback)
    
    # Generate additional outputs
    scanner.generate_init_files(overwrite=True)
    scanner.export_chatgpt_context()
    artifacts = [
        "project_analysis.json",
        "test_analysis.json", 
        "chatgpt_project_context.json",
        "dependency_cache.json",
        "analysis/enhanced_agent_analysis.json",
        "analysis/enhanced_architecture_overview.json",
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
