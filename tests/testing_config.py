
# MIGRATED: This file has been migrated to the centralized configuration system
from pathlib import Path
import sys

# Repository root
REPO_ROOT = Path(__file__).resolve().parent.parent

# Common paths
TESTS_DIR = REPO_ROOT / "tests"
SRC_DIR = REPO_ROOT / "src"
RESULTS_DIR = REPO_ROOT / "test_results"
COVERAGE_DIR = REPO_ROOT / "htmlcov"

# Ensure important directories are on the import path
for path in (REPO_ROOT, TESTS_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
