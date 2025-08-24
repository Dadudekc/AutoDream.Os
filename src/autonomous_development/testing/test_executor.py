"""Utilities for executing tests."""
import subprocess
from typing import Any, Dict, List

from .result_collation import TestResult


def run_tests(test_files: List[str], config: Dict[str, Any]) -> List[TestResult]:
    """Execute ``test_files`` using pytest and return their results."""
    results: List[TestResult] = []
    timeout = config.get("timeout", 30)
    for file in test_files:
        cmd = ["python", "-m", "pytest", file, "-q"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        results.append(
            TestResult(
                file=file,
                returncode=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
            )
        )
    return results
