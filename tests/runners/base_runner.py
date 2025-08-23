"""
Base Test Runner - Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - Unified Test Runner System

Common functionality for all test runners, eliminating duplication
across the previous 3 separate test runners.
"""

import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod


class BaseTestRunner(ABC):
    """Base class for all test runners with common functionality."""

    def __init__(self, repo_root: Path):
        """Initialize the base test runner."""
        self.repo_root = repo_root
        self.tests_dir = repo_root / "tests"
        self.src_dir = repo_root / "src"
        self.results_dir = repo_root / "test_results"
        self.coverage_dir = repo_root / "htmlcov"

        # Ensure required directories exist
        self.results_dir.mkdir(exist_ok=True)
        self.coverage_dir.mkdir(exist_ok=True)

        self.results = {}
        self.start_time = None
        self.end_time = None

    def discover_tests(
        self, test_type: Optional[str] = None, pattern: str = "test_*.py"
    ) -> List[Path]:
        """Discover test files based on type and pattern."""
        if not self.tests_dir.exists():
            print(f"❌ Test directory not found: {self.tests_dir}")
            return []

        test_files = []

        if test_type:
            # Specific test type directory
            type_dir = self.tests_dir / test_type
            if type_dir.exists():
                test_files.extend(type_dir.rglob(pattern))
            else:
                print(f"⚠️ Test type directory not found: {type_dir}")
        else:
            # All test files
            test_files.extend(self.tests_dir.rglob(pattern))
            # Also include root-level test files
            test_files.extend(self.repo_root.glob(pattern))

        return sorted(set(test_files))  # Remove duplicates and sort

    def build_pytest_command(
        self,
        test_paths: List[Path],
        coverage: bool = True,
        parallel: bool = False,
        verbose: bool = True,
        markers: Optional[List[str]] = None,
    ) -> List[str]:
        """Build pytest command with specified options."""
        cmd = ["python", "-m", "pytest"]

        # Add test paths
        for test_path in test_paths:
            cmd.append(str(test_path))

        # Add options
        if verbose:
            cmd.append("-v")

        if coverage:
            cmd.extend(
                [
                    "--cov=src",
                    "--cov-report=html",
                    "--cov-report=term-missing",
                    "--cov-report=json",
                ]
            )

        if parallel:
            cmd.extend(["-n", "auto"])

        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])

        # Standard pytest options
        cmd.extend(
            [
                "--tb=short",
                "--strict-markers",
                "--disable-warnings",
                f"--html={self.results_dir}/report.html",
                "--self-contained-html",
            ]
        )

        return cmd

    def execute_command(self, cmd: List[str], timeout: int = 300) -> Dict[str, Any]:
        """Execute command and return results."""
        print(f"🚀 Executing: {' '.join(cmd)}")

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.repo_root, timeout=timeout
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

        except subprocess.TimeoutExpired as e:
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
                "stderr": f"Command execution error: {str(e)}",
                "duration": duration,
                "command": " ".join(cmd),
                "error": str(e),
            }

    def parse_test_results(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
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

        # Parse pytest output
        stdout = execution_result["stdout"]

        # Look for test summary line
        for line in stdout.split("\n"):
            line = line.strip()
            if "passed" in line or "failed" in line or "error" in line:
                # Parse various pytest output formats
                if " passed" in line:
                    try:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if "passed" in part and i > 0:
                                results["passed"] = int(parts[i - 1])
                                results["tests_run"] += results["passed"]
                    except (ValueError, IndexError):
                        pass

                if " failed" in line:
                    try:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if "failed" in part and i > 0:
                                results["failed"] = int(parts[i - 1])
                                results["tests_run"] += results["failed"]
                    except (ValueError, IndexError):
                        pass

        # Determine summary
        if results["failed"] > 0 or results["errors"] > 0:
            results["summary"] = "FAILED"
        elif results["passed"] > 0:
            results["summary"] = "PASSED"
        else:
            results["summary"] = "NO_TESTS"

        return results

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"

        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"📊 Results saved to: {filepath}")
        return filepath

    def print_summary(self, results: Dict[str, Any]):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 70)

        execution = results.get("execution", {})
        print(f"Duration: {execution.get('duration', 0):.2f}s")
        print(f"Command: {execution.get('command', 'Unknown')}")
        print(f"Return Code: {execution.get('returncode', 'Unknown')}")

        print(f"\n📈 Test Results:")
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

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Abstract method for running tests."""
        pass
