"""Execution engine for running tests with coverage."""

import io
from pathlib import Path
from typing import Any, Dict, List

import coverage
import pytest

from src.utils.logger import get_logger

from .config import COVERAGE_REPORT_PRECISION

logger = get_logger(__name__)


def run_tests(test_files: List[Path], source_dir: Path) -> Dict[str, Any]:
    """Execute ``test_files`` and return pass status and coverage percentage."""
    cov = coverage.Coverage(source=[str(source_dir)])
    cov.start()
    exit_code = pytest.main([str(f) for f in test_files])
    cov.stop()
    cov.save()
    stream = io.StringIO()
    coverage_pct = round(cov.report(file=stream), COVERAGE_REPORT_PRECISION)
    logger.info(
        "Test execution finished with exit code %s and coverage %.2f",
        exit_code,
        coverage_pct,
    )
    return {"passed": exit_code == 0, "coverage": coverage_pct}
