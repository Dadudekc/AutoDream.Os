#!/usr/bin/env python3
"""
OSS CLI Smoke Tests
===================

Quick validation tests for OSS contribution system.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.smoke
def test_oss_cli_help():
    """Smoke test: CLI help command works."""
    result = subprocess.run(
        [sys.executable, "-m", "src.opensource.oss_cli", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


@pytest.mark.smoke
def test_oss_cli_status():
    """Smoke test: Status command works."""
    result = subprocess.run(
        [sys.executable, "-m", "src.opensource.oss_cli", "status"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "OSS Contribution Status" in result.stdout


@pytest.mark.smoke
def test_oss_cli_list():
    """Smoke test: List command works."""
    result = subprocess.run(
        [sys.executable, "-m", "src.opensource.oss_cli", "list"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Registered OSS Projects" in result.stdout


@pytest.mark.smoke
def test_project_manager_init():
    """Smoke test: Project manager initializes."""
    import tempfile

    from src.opensource.project_manager import OpenSourceProjectManager

    with tempfile.TemporaryDirectory() as tmpdir:
        pm = OpenSourceProjectManager(tmpdir)
        assert pm.projects_root.exists()
        assert pm.registry_file.exists()


@pytest.mark.smoke
def test_contribution_tracker_init():
    """Smoke test: Contribution tracker initializes."""
    import tempfile

    from src.opensource.contribution_tracker import ContributionTracker

    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = ContributionTracker(f"{tmpdir}/portfolio.json")
        assert tracker.portfolio_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "smoke"])
