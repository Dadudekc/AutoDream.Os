#!/usr/bin/env python3
"""
Automated Test Reporting System - Core Module
============================================

Core test reporting functionality extracted from test_reporting.py
V2 Compliance: ≤400 lines for compliance

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize test_reporting.py for V2 compliance
License: MIT
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class CoverageReporter:
    """Comprehensive test coverage reporting system."""

    def __init__(self, report_dir: str = "test_reports"):
        """Initialize test coverage reporter."""
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now()

    def generate_coverage_report(self, coverage_data: dict[str, Any]) -> str:
        """Generate comprehensive coverage report."""
        report_path = (
            self.report_dir / f"coverage_report_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        )

        report = {
            "timestamp": self.timestamp.isoformat(),
            "coverage": coverage_data,
            "summary": self._calculate_summary(coverage_data),
            "agent_breakdown": self._calculate_agent_breakdown(coverage_data),
            "recommendations": self._generate_recommendations(coverage_data),
        }

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)

        return str(report_path)

    def generate_csv_report(self, test_results: list[dict[str, Any]]) -> str:
        """Generate CSV test results report."""
        csv_path = self.report_dir / f"test_results_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.csv"

        if test_results:
            fieldnames = test_results[0].keys()
            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(test_results)

        return str(csv_path)

    def _calculate_summary(self, coverage_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate coverage summary statistics."""
        return {
            "total_coverage": coverage_data.get("totals", {}).get("percent_covered", 0),
            "lines_covered": coverage_data.get("totals", {}).get("num_covered", 0),
            "lines_total": coverage_data.get("totals", {}).get("num_statements", 0),
            "files_covered": len(coverage_data.get("files", {})),
            "target_achieved": coverage_data.get("totals", {}).get("percent_covered", 0) >= 85,
        }

    def _calculate_agent_breakdown(self, coverage_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate coverage breakdown by agent assignment."""
        agent_coverage = {
            "agent1": {"files": [], "coverage": 0},  # Core systems
            "agent2": {"files": [], "coverage": 0},  # Architecture
            "agent3": {"files": [], "coverage": 0},  # Infrastructure
            "agent4": {"files": [], "coverage": 0},  # Quality Assurance
            "agent5": {"files": [], "coverage": 0},  # Business Intelligence
            "agent6": {"files": [], "coverage": 0},  # Coordination
            "agent7": {"files": [], "coverage": 0},  # Web Development
            "agent8": {"files": [], "coverage": 0},  # Operations
        }

        files = coverage_data.get("files", {})
        for file_path, file_data in files.items():
            file_path_str = str(file_path).lower()

            # Categorize files by agent responsibility
            if any(keyword in file_path_str for keyword in ["core", "messaging", "vector"]):
                agent_coverage["agent1"]["files"].append(file_path)
            elif any(keyword in file_path_str for keyword in ["architecture", "design", "pattern"]):
                agent_coverage["agent2"]["files"].append(file_path)
            elif any(
                keyword in file_path_str for keyword in ["infrastructure", "deployment", "config"]
            ):
                agent_coverage["agent3"]["files"].append(file_path)
            elif any(keyword in file_path_str for keyword in ["quality", "test", "validation"]):
                agent_coverage["agent4"]["files"].append(file_path)
            elif any(keyword in file_path_str for keyword in ["business", "intelligence", "data"]):
                agent_coverage["agent5"]["files"].append(file_path)
            elif any(
                keyword in file_path_str for keyword in ["coordination", "communication", "swarm"]
            ):
                agent_coverage["agent6"]["files"].append(file_path)
            elif any(keyword in file_path_str for keyword in ["web", "js", "frontend"]):
                agent_coverage["agent7"]["files"].append(file_path)
            elif any(
                keyword in file_path_str for keyword in ["operations", "monitoring", "support"]
            ):
                agent_coverage["agent8"]["files"].append(file_path)

        # Calculate coverage percentages for each agent
        for agent, data in agent_coverage.items():
            if data["files"]:
                total_lines = sum(
                    files[file].get("summary", {}).get("num_statements", 0)
                    for file in data["files"]
                )
                covered_lines = sum(
                    files[file].get("summary", {}).get("num_covered", 0) for file in data["files"]
                )
                if total_lines > 0:
                    data["coverage"] = (covered_lines / total_lines) * 100

        return agent_coverage

    def _generate_recommendations(self, coverage_data: dict[str, Any]) -> list[str]:
        """Generate coverage improvement recommendations."""
        recommendations = []
        summary = self._calculate_summary(coverage_data)
        agent_breakdown = self._calculate_agent_breakdown(coverage_data)

        # Overall coverage recommendations
        if summary["total_coverage"] < 85:
            recommendations.append(
                f"Overall coverage is {summary['total_coverage']:.1f}%. "
                "Need additional tests to reach 85% target."
            )

        # Agent-specific recommendations
        for agent, data in agent_breakdown.items():
            if data["coverage"] < 80 and data["files"]:
                recommendations.append(
                    f"{agent.upper()}: Coverage is {data['coverage']:.1f}% "
                    f"for {len(data['files'])} files. Consider adding more tests."
                )

        # Low coverage files
        low_coverage_files = []
        files = coverage_data.get("files", {})
        for file_path, file_data in files.items():
            file_coverage = file_data.get("summary", {}).get("percent_covered", 0)
            if file_coverage < 70:
                low_coverage_files.append(str(file_path))

        if low_coverage_files:
            recommendations.append(f"Focus on low-coverage files: {low_coverage_files[:5]}")

        return recommendations


class ProgressTracker:
    """Track test execution progress and provide updates."""

    def __init__(self):
        """Initialize progress tracker."""
        self.start_time = datetime.now()
        self.test_results = []
        self.coverage_reports = []

    def record_test_result(self, test_name: str, status: str, duration: float, error: str = None):
        """Record individual test result."""
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

    def get_progress_summary(self) -> dict[str, Any]:
        """Get current progress summary."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "passed"])
        failed_tests = len([r for r in self.test_results if r["status"] == "failed"])
        elapsed_time = (datetime.now() - self.start_time).total_seconds()

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "elapsed_time": elapsed_time,
            "tests_per_second": total_tests / elapsed_time if elapsed_time > 0 else 0,
        }

    def generate_progress_report(self) -> str:
        """Generate progress report."""
        summary = self.get_progress_summary()

        report = f"""
🧪 V2_SWARM Test Progress Report
================================

📊 Test Execution Summary:
- Total Tests: {summary["total_tests"]}
- Passed: {summary["passed_tests"]} ({summary["pass_rate"]:.1f}%)
- Failed: {summary["failed_tests"]}
- Elapsed Time: {summary["elapsed_time"]:.1f}s
- Tests/Second: {summary["tests_per_second"]:.1f}

📈 Recent Test Results:
"""

        # Show last 10 test results
        recent_results = self.test_results[-10:]
        for result in recent_results:
            status_emoji = "✅" if result["status"] == "passed" else "❌"
            report += f"\n{status_emoji} {result['test_name']} ({result['duration']:.3f}s)"

        return report


# Test fixtures for core functionality
@pytest.fixture(scope="session")
def coverage_reporter():
    """Provide coverage reporter fixture."""
    return CoverageReporter()


@pytest.fixture(scope="session")
def progress_tracker():
    """Provide progress tracker fixture."""
    return ProgressTracker()


@pytest.fixture(autouse=True)
def track_test_progress(request, progress_tracker):
    """Automatically track test progress."""
    start_time = datetime.now()

    def finalize():
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Record test result
        if hasattr(request.node, "rep_call"):
            outcome = request.node.rep_call.outcome
            error = str(request.node.rep_call.excinfo) if request.node.rep_call.excinfo else None
        else:
            outcome = "unknown"
            error = None

        progress_tracker.record_test_result(request.node.name, outcome, duration, error)

    request.addfinalizer(finalize)


# Test the core reporting system
class TestReportingSystemCore:
    """Test the core reporting system functionality."""

    @pytest.mark.unit
    def test_coverage_reporter_initialization(self, coverage_reporter):
        """Test coverage reporter initialization."""
        assert coverage_reporter is not None
        assert coverage_reporter.report_dir.exists()

    @pytest.mark.unit
    def test_coverage_report_generation(self, coverage_reporter):
        """Test coverage report generation."""
        mock_coverage_data = {
            "totals": {"percent_covered": 85.5, "num_covered": 1000, "num_statements": 1200},
            "files": {
                "src/core/config.py": {
                    "summary": {"percent_covered": 90.0, "num_covered": 100, "num_statements": 110}
                }
            },
        }

        report_path = coverage_reporter.generate_coverage_report(mock_coverage_data)
        assert Path(report_path).exists()

        # Verify report content
        with open(report_path) as f:
            report_data = json.load(f)

        assert "coverage" in report_data
        assert "summary" in report_data
        assert "agent_breakdown" in report_data
        assert report_data["summary"]["total_coverage"] == 85.5

    @pytest.mark.unit
    def test_progress_tracker(self, progress_tracker):
        """Test progress tracker functionality."""
        # Record some test results
        progress_tracker.record_test_result("test_1", "passed", 1.5)
        progress_tracker.record_test_result("test_2", "failed", 2.0, "AssertionError")

        summary = progress_tracker.get_progress_summary()

        assert summary["total_tests"] == 2
        assert summary["passed_tests"] == 1
        assert summary["failed_tests"] == 1
        assert summary["pass_rate"] == 50.0

    @pytest.mark.unit
    def test_progress_report_generation(self, progress_tracker):
        """Test progress report generation."""
        progress_tracker.record_test_result("test_example", "passed", 1.0)

        report = progress_tracker.generate_progress_report()

        assert "Test Progress Report" in report
        assert "test_example" in report
        assert "✅" in report


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 Automated Test Reporting System - Core Module")
    print("=" * 50)
    print("✅ Core test reporting functionality loaded successfully")
    print("✅ Coverage reporter loaded successfully")
    print("✅ Progress tracker loaded successfully")
    print("✅ Test fixtures loaded successfully")
    print("🐝 WE ARE SWARM - Core test reporting ready!")
