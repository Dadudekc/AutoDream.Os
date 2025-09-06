# tests/test_hard_onboarding.py
import os
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

CLI = ["python", "-m", "src.services.messaging_cli"]


def run_cli(tmp, *args):
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    cwd = tmp
    return subprocess.run(
        CLI + list(args), cwd=cwd, env=env, capture_output=True, text=True
    )


def setup_agents(root, n=3):
    for i in range(1, n + 1):
        d = Path(root) / f"runtime/agent_state/Agent-{i}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "status.json").write_text("{}", encoding="utf-8")
        (d / "onboarding.json").write_text("{}", encoding="utf-8")


def test_dry_run_success(tmp_path):
    setup_agents(tmp_path, n=2)
    r = run_cli(tmp_path, "--hard-onboarding", "--dry-run", "--yes")
    assert r.returncode == 0
    assert "DRY-RUN" in r.stdout
    assert "Hard onboarding complete: 2/2" in r.stdout


def test_subset_and_exit_codes(tmp_path):
    setup_agents(tmp_path, n=3)
    # Limit to Agent-1
    r = run_cli(tmp_path, "--hard-onboarding", "--yes", "--agents", "Agent-1")
    assert r.returncode == 0
    assert "Hard onboarding complete: 1/1" in r.stdout


def test_backup_created(tmp_path):
    setup_agents(tmp_path, n=1)
    r = run_cli(tmp_path, "--hard-onboarding", "--yes")
    assert "Backup created:" in r.stdout


def test_confirmation_abort(tmp_path, monkeypatch):
    setup_agents(tmp_path, n=1)
    # Simulate user pressing Enter (default No)
    monkeypatch.setenv("NONINTERACTIVE_YES", "")
    p = subprocess.Popen(
        CLI + ["--hard-onboarding"],
        cwd=tmp_path,
        env=os.environ | {"PYTHONPATH": "."},
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = p.communicate("\n", timeout=5)
    assert "Aborted" in out
    assert p.returncode == 1
