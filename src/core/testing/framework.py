"""Lightweight orchestration for discovery, execution, and reporting."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import List

from .discovery import discover_test_files
from .executor import TestExecutor
from .reporting import print_execution_summary
from .testing_utils import BaseTest, TestResult


def _load_tests(paths: List[Path]) -> List[BaseTest]:
    """Load ``BaseTest`` subclasses from file paths."""
    tests: List[BaseTest] = []
    for path in paths:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[path.stem] = module
            spec.loader.exec_module(module)
            for obj in module.__dict__.values():
                if isinstance(obj, type) and issubclass(obj, BaseTest) and obj is not BaseTest:
                    tests.append(obj())
    return tests


def run_tests(start_dir: str, pattern: str = "test_*.py") -> List[TestResult]:
    """Discover, execute, and report tests under ``start_dir``."""
    files = discover_test_files(start_dir, pattern)
    tests = _load_tests(files)
    executor = TestExecutor()
    executor.add_tests_to_queue(tests)
    results = executor.execute_queue()
    print_execution_summary(results)
    return results
