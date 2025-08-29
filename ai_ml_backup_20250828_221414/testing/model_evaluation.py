from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
import logging
import subprocess
import sys

    import coverage  # type: ignore


logger = logging.getLogger(__name__)

try:
    COVERAGE_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    COVERAGE_AVAILABLE = False
    logger.warning("coverage package not available")


class ModelEvaluator:
    """Evaluate models by running test suites."""

    def __init__(self, project_path: str = ".", test_dir: str = "tests"):
        self.project_path = Path(project_path)
        self.test_dir = Path(test_dir)

    def run_tests(self, test_path: Optional[str] = None) -> Dict[str, Optional[str]]:
        """Execute pytest on the given path and return raw results."""
        cmd = [sys.executable, "-m", "pytest"]
        if test_path:
            cmd.append(test_path)
        else:
            cmd.append(str(self.test_dir))
        logger.info("Running tests with command: %s", " ".join(cmd))
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=self.project_path
        )
        output = {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timestamp": datetime.now().isoformat(),
        }
        output.update(self._parse_pytest_output(result.stdout))
        return output

    def run_coverage_analysis(self, source_dir: str = "src") -> Dict[str, Any]:
        """Run coverage analysis for the test suite."""
        if not COVERAGE_AVAILABLE:
            logger.error("coverage package not available")
            return {"error": "coverage package not available"}

        cmd = [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--source",
            source_dir,
            "-m",
            "pytest",
            str(self.test_dir),
        ]
        logger.info("Running coverage analysis: %s", " ".join(cmd))
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=self.project_path
        )

        report_cmd = [sys.executable, "-m", "coverage", "report"]
        report_result = subprocess.run(
            report_cmd, capture_output=True, text=True, cwd=self.project_path
        )

        html_cmd = [sys.executable, "-m", "coverage", "html"]
        html_result = subprocess.run(
            html_cmd, capture_output=True, text=True, cwd=self.project_path
        )

        return {
            "coverage_run": {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
            "coverage_report": {
                "return_code": report_result.returncode,
                "stdout": report_result.stdout,
                "stderr": report_result.stderr,
            },
            "html_report": {
                "return_code": html_result.returncode,
                "stdout": html_result.stdout,
                "stderr": html_result.stderr,
            },
            "timestamp": datetime.now().isoformat(),
        }

    def _parse_pytest_output(self, output: str) -> Dict[str, int]:
        """Parse pytest output to extract statistics."""
        stats: Dict[str, int] = {}
        for line in output.splitlines():
            if "collected" in line and "items" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "collected" and i + 1 < len(parts):
                        stats["total"] = int(parts[i + 1])
            if "passed" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            stats["passed"] = int(parts[i - 1])
                        except ValueError:
                            pass
            if "failed" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "failed" and i > 0:
                        try:
                            stats["failed"] = int(parts[i - 1])
                        except ValueError:
                            pass
        return stats
