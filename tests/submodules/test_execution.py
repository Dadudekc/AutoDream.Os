"""Shared test execution helpers."""

import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any


def execute_command(cmd: List[str], cwd: Path, timeout: int = 300) -> Dict[str, Any]:
    """Execute a command and return execution metadata."""
    print(f"🚀 Executing: {' '.join(cmd)}")
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout
        )
        duration = time.time() - start_time
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
            "duration": duration,
            "command": " ".join(cmd),
            "timeout": True,
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command execution error: {e}",
            "duration": duration,
            "command": " ".join(cmd),
            "error": str(e),
        }


def parse_test_results(execution_result: Dict[str, Any]) -> Dict[str, Any]:
    """Parse pytest output into a standard result dictionary."""
    results = {
        "execution": execution_result,
        "tests_run": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "coverage": None,
        "summary": "UNKNOWN",
    }

    if not execution_result["success"]:
        results["summary"] = "FAILED"
        return results

    stdout = execution_result["stdout"]
    for line in stdout.split("\n"):
        line = line.strip()
        if "passed" in line or "failed" in line or "error" in line:
            parts = line.split()
            try:
                if "passed" in line:
                    idx = parts.index("passed")
                    results["passed"] = int(parts[idx - 1])
                    results["tests_run"] += results["passed"]
                if "failed" in line:
                    idx = parts.index("failed")
                    results["failed"] = int(parts[idx - 1])
                    results["tests_run"] += results["failed"]
            except (ValueError, IndexError):
                continue

    if results["failed"] > 0 or results["errors"] > 0:
        results["summary"] = "FAILED"
    elif results["passed"] > 0:
        results["summary"] = "PASSED"
    else:
        results["summary"] = "NO_TESTS"

    return results
