"""Tests for the :mod:`tests.submodules.cleanup` module."""

import pytest

from tests.submodules.cleanup import cleanup_artifacts
from tests.testing_config import COVERAGE_DIR, RESULTS_DIR


@pytest.fixture()
def artifact_dirs() -> None:
    """Create temporary files in the results and coverage directories."""

    for directory in (RESULTS_DIR, COVERAGE_DIR):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "temp.txt").write_text("data", encoding="utf-8")
    yield
    for directory in (RESULTS_DIR, COVERAGE_DIR):
        if directory.exists():
            for item in directory.iterdir():
                if item.is_file():
                    item.unlink()
            directory.rmdir()


def test_cleanup_artifacts_removes_files(artifact_dirs: None) -> None:
    """Ensure cleanup removes files from configured directories."""

    for directory in (RESULTS_DIR, COVERAGE_DIR):
        assert any(directory.iterdir())

    cleanup_artifacts()

    for directory in (RESULTS_DIR, COVERAGE_DIR):
        assert list(directory.iterdir()) == []

