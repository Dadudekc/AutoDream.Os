"""Tests for overnight flag in messaging CLI."""

import sys
from pathlib import Path
import subprocess

from src.services import messaging_cli


def test_overnight_flag_runs_overnight_system(monkeypatch):
    """Ensure --overnight dispatches the overnight system script."""
    called = {}

    def fake_run(cmd, *args, **kwargs):
        called["cmd"] = cmd

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["messaging_cli", "--overnight"])

    messaging_cli.main()

    assert Path(called["cmd"][1]).name == "overnight_autonomous_system.py"
