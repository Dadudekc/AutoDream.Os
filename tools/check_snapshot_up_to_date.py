import logging
logger = logging.getLogger(__name__)
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
try:
    from tools.projectscanner import ProjectScanner
except Exception:
    logger.info(
        'ERROR: Unable to import ProjectScanner. Update import path in tools/check_snapshot_up_to_date.py.'
        )
    sys.exit(2)
ARTIFACTS = ['project_analysis.json', 'test_analysis.json',
    'chatgpt_project_context.json', 'dependency_cache.json',
    'analysis/agent_analysis.json', 'analysis/module_analysis.json',
    'analysis/file_type_analysis.json', 'analysis/complexity_analysis.json',
    'analysis/dependency_analysis.json', 'analysis/architecture_overview.json']


def git_diff_has_changes(paths: list[str]) ->bool:
    cmd = ['git', 'diff', '--quiet', '--'] + paths
    result = subprocess.run(cmd)
    return result.returncode != 0


def main() ->None:
    repo_root = REPO_ROOT
    try:
        import os
        os.chdir(repo_root)
    except Exception:
        pass
    scanner = ProjectScanner(project_root='.')
    scanner.scan_project()
    scanner.generate_init_files(overwrite=True)
    scanner.categorize_agents()
    scanner.report_generator.save_report()
    scanner.export_chatgpt_context()
    scanner.generate_modular_reports()
    existing = [p for p in ARTIFACTS if Path(p).exists()]
    if not existing:
        sys.exit(0)
    if git_diff_has_changes(existing):
        logger.info(
            """
❌ Snapshots out of date.
   I just regenerated snapshots and they differ from HEAD.
   ➜ Action: `git add project_analysis.json test_analysis.json chatgpt_project_context.json dependency_cache.json`
             `git commit -m "chore(snapshots): refresh project analysis"`
             Then push again.
"""
            )
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
