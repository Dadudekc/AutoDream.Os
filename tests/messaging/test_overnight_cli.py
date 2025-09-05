"""Tests for overnight flag in messaging CLI."""

import sys
from pathlib import Path
import subprocess

from src.services import messaging_cli


def test_overnight_flag_runs_overnight_system(monkeypatch):
    """Ensure --overnight dispatches the overnight system script."""
    from unittest.mock import MagicMock

    mock_run = MagicMock()
    monkeypatch.setattr(subprocess, "run", mock_run)
    monkeypatch.setattr(sys, "argv", ["messaging_cli", "--overnight"])

    messaging_cli.main()

    mock_run.assert_called_once()
    called_cmd = mock_run.call_args.args[0]
    assert Path(called_cmd[1]).name == "overnight_autonomous_system.py"
