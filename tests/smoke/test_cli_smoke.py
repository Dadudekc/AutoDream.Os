import subprocess, sys

def run(args):
    return subprocess.run([sys.executable, "-m", "src"] + args, capture_output=True, text=True)

def test_status_runs():
    p = run(["--status"])
    assert p.returncode == 0
    assert "python" in p.stdout.lower()

def test_validate_runs():
    p = run(["--validate"])
    assert p.returncode == 0

def test_demo_runs():
    p = run(["--demo"])
    assert p.returncode == 0
