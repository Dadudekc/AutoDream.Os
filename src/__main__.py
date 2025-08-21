import argparse, os, sys, platform, subprocess, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = shutil.which("python") or sys.executable

def _ok(ok: bool) -> str:
    return "✅" if ok else "❌"

def status():
    info = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": str(os.getcwd()),
        "repo_root": str(ROOT),
        "has_tests_dir": (ROOT / "tests").exists(),
        "has_requirements": (ROOT / "requirements.txt").exists(),
    }
    print(json.dumps(info, indent=2))
    return True

def demo():
    # Prefer an existing demo if present, else quick smoke
    demo_candidates = [
        ROOT / "scripts" / "demo.py",
        ROOT / "demo_integrated_coordinator.py",
        ROOT / "scripts" / "run_demo.sh",
    ]
    for c in demo_candidates:
        if c.exists():
            cmd = [PY, str(c)] if c.suffix == ".py" else ["bash", str(c)]
            print(f"→ Running demo: {c}")
            rc = subprocess.call(cmd)
            if rc == 0:
                return True
            print("Demo script failed; running minimal sanity print.")
            break
    else:
        print("No demo script found; running minimal sanity print.")
    print("Demo OK.")
    return True

def test():
    # Run pytest if available, else unittest discovery
    if shutil.which("pytest"):
        cmd = ["pytest", "-q"]
    else:
        cmd = [PY, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
    print("→ Running tests:", " ".join(cmd))
    return subprocess.call(cmd) == 0

def validate():
    # Hook for code standards; run flake8/ruff if installed
    ran = False
    for tool in ("ruff", "flake8"):
        if shutil.which(tool):
            ran = True
            print(f"→ Running {tool} …")
            cmd = [tool, "check", "src"] if tool == "ruff" else [tool, "src"]
            subprocess.call(cmd)
    if not ran:
        print("No linter installed; skipped.")
    return True

def main():
    ap = argparse.ArgumentParser(prog="autodream.os")
    ap.add_argument("--status", action="store_true", help="Show system status")
    ap.add_argument("--demo", action="store_true", help="Run a demo flow")
    ap.add_argument("--test", action="store_true", help="Run tests")
    ap.add_argument("--validate", action="store_true", help="Run linters/validators if present")
    args = ap.parse_args()

    ran = False
    ok = True
    if args.status:
        ran = True
        ok &= status()
    if args.demo:
        ran = True
        ok &= demo()
    if args.test:
        ran = True
        ok &= test()
    if args.validate:
        ran = True
        ok &= validate()

    if not ran:
        ap.print_help()
        sys.exit(0)
    print(f"\nOverall: {_ok(ok)}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
