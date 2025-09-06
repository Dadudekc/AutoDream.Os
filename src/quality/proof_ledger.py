# src/quality/proof_ledger.py
from __future__ import annotations
import json, os, subprocess, time
from datetime import datetime
from typing import Dict, List, Tuple


def _git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def run_tdd_proof(mode: str, role_map: Dict[str, str]) -> str:
    """Executes pytest if available and writes a JSON proof artifact.

    Returns path to the proof file.
    """
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    outdir = os.path.join("runtime", "quality", "proofs", "tdd")
    os.makedirs(outdir, exist_ok=True)
    proof_path = os.path.join(outdir, f"proof-{ts}.json")

    pytest_available = True
    start = time.time()
    result = {
        "schema": "tdd_proof/v1",
        "timestamp_utc": ts,
        "git_commit": _git_head(),
        "mode": mode,
        "roles": role_map,
        "pytest_available": True,
        "pytest_exit_code": None,
        "tests": {
            "collected": None,
            "passed": None,
            "failed": None,
            "errors": None,
            "skipped": None,
        },
        "duration_sec": None,
        "notes": "",
    }

    try:
        # Use -q for quiet summary; users may expand later
        proc = subprocess.run(["pytest", "-q"], capture_output=True, text=True)
        result["pytest_exit_code"] = proc.returncode
        # Lightweight parse: look for last line like "X passed, Y failed, Z skipped in Ns"
        tail = (proc.stdout or "") + "\n" + (proc.stderr or "")
        # naive parse (robust enough for proof artifact)
        import re

        m = re.search(r"(\d+)\s+passed.*?(\d+)\s+failed|(\d+)\s+failed", tail)
        passed = None
        failed = None
        if m:
            groups = [g for g in m.groups() if g]
            if len(groups) == 2:
                passed = int(groups[0])
                failed = int(groups[1])
            elif len(groups) == 1:
                failed = int(groups[0])
        result["tests"]["passed"] = passed
        result["tests"]["failed"] = failed
        result["duration_sec"] = round(time.time() - start, 3)
    except FileNotFoundError:
        pytest_available = False
        result["pytest_available"] = False
        result["notes"] = "pytest not installed or not on PATH"
        result["duration_sec"] = round(time.time() - start, 3)
    except Exception as e:
        result["pytest_exit_code"] = 1
        result["notes"] = f"pytest run error: {e}"
        result["duration_sec"] = round(time.time() - start, 3)

    with open(proof_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return proof_path
