"""Tests for run_dry_analysis script."""

import subprocess
import sys

import pytest

SCRIPT = "run_dry_analysis.py"


@pytest.mark.parametrize(
    "mode,expected",
    [
        ("advanced_analysis", "Running advanced analysis"),
        ("advanced_elimination", "Running advanced elimination"),
        ("comprehensive_analysis", "Running comprehensive analysis"),
        ("focused_analysis", "Running focused analysis"),
        ("mass_elimination", "Running mass elimination"),
    ],
)
def test_modes(mode: str, expected: str) -> None:
    """Verify each mode prints its placeholder message."""
    result = subprocess.run(
        [sys.executable, SCRIPT, "--mode", mode],
        check=True,
        capture_output=True,
        text=True,
    )
    assert expected in result.stdout
