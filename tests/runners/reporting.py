"""Functions for parsing and reporting test execution results."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def parse_test_results(execution_result: Dict[str, Any]) -> Dict[str, Any]:
    """Parse test execution results."""
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
            for i, part in enumerate(parts):
                if part.startswith("passed") and i > 0:
                    try:
                        results["passed"] = int(parts[i - 1])
                        results["tests_run"] += results["passed"]
                    except ValueError:
                        pass
                if part.startswith("failed") and i > 0:
                    try:
                        results["failed"] = int(parts[i - 1])
                        results["tests_run"] += results["failed"]
                    except ValueError:
                        pass
    if results["failed"] > 0 or results["errors"] > 0:
        results["summary"] = "FAILED"
    elif results["passed"] > 0:
        results["summary"] = "PASSED"
    else:
        results["summary"] = "NO_TESTS"
    return results


def save_results(
    results: Dict[str, Any], results_dir: Path, filename: str | None = None
) -> Path:
    """Save test results to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
    filepath = results_dir / filename
    with open(filepath, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"📊 Results saved to: {filepath}")
    return filepath


def print_summary(results: Dict[str, Any]) -> None:
    """Print a summary of the test results."""
    print("\n" + "=" * 70)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 70)
    execution = results.get("execution", {})
    print(f"Duration: {execution.get('duration', 0):.2f}s")
    print(f"Command: {execution.get('command', 'Unknown')}")
    print(f"Return Code: {execution.get('returncode', 'Unknown')}")
    print("\n📈 Test Results:")
    print(f"  Tests Run: {results.get('tests_run', 0)}")
    print(f"  Passed: {results.get('passed', 0)}")
    print(f"  Failed: {results.get('failed', 0)}")
    print(f"  Skipped: {results.get('skipped', 0)}")
    print(f"  Errors: {results.get('errors', 0)}")
    summary = results.get("summary", "UNKNOWN")
    if summary == "PASSED":
        print(f"\n✅ Overall Status: {summary}")
    elif summary == "FAILED":
        print(f"\n❌ Overall Status: {summary}")
    else:
        print(f"\n⚠️ Overall Status: {summary}")
