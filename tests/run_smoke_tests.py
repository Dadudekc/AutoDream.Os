#!/usr/bin/env python3
"""
Smoke Test Runner - Agent Cellphone V2
=====================================

Comprehensive smoke test runner for all major features.
Runs all smoke tests in sequence and provides consolidated reporting.

Author: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    """Result of a test suite execution."""
    name: str
    passed: int
    failed: int
    skipped: int
    duration: float
    error_message: str = ""


class SmokeTestRunner:
    """Comprehensive smoke test runner for Agent Cellphone V2."""

    def __init__(self):
        """Initialize the smoke test runner."""
        self.project_root = Path(__file__).resolve().parent.parent
        self.test_results: List[TestResult] = []
        self.start_time = None

    def run_command(self, command: List[str], cwd: Path = None) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out after 300 seconds"
        except Exception as e:
            return -1, "", f"Command execution failed: {e}"

    def parse_pytest_output(self, output: str) -> Tuple[int, int, int]:
        """Parse pytest output to extract passed/failed/skipped counts."""
        passed = failed = skipped = 0

        lines = output.split('\n')
        for line in lines:
            if 'passed' in line and 'failed' in line and 'skipped' in line:
                # Parse summary line like "5 passed, 0 failed, 2 skipped"
                parts = line.strip().split(',')
                for part in parts:
                    part = part.strip()
                    if 'passed' in part:
                        try:
                            passed = int(part.split()[0])
                        except (ValueError, IndexError):
                            pass
                    elif 'failed' in part:
                        try:
                            failed = int(part.split()[0])
                        except (ValueError, IndexError):
                            pass
                    elif 'skipped' in part:
                        try:
                            skipped = int(part.split()[0])
                        except (ValueError, IndexError):
                            pass
                break

        return passed, failed, skipped

    def run_messaging_smoke_tests(self) -> TestResult:
        """Run messaging system smoke tests."""
        print("🚀 Running Messaging Smoke Tests...")
        start_time = time.time()

        command = [
            sys.executable, "-m", "pytest",
            "tests/test_messaging_smoke.py",
            "-v", "--tb=short"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time
        passed, failed, skipped = self.parse_pytest_output(stdout)

        error_msg = stderr if exit_code != 0 else ""

        return TestResult(
            name="Messaging System",
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            error_message=error_msg
        )

    def run_vector_db_smoke_tests(self) -> TestResult:
        """Run vector database smoke tests."""
        print("🚀 Running Vector Database Smoke Tests...")
        start_time = time.time()

        command = [
            sys.executable, "-m", "pytest",
            "tests/vector_database/",
            "-v", "--tb=short"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time
        passed, failed, skipped = self.parse_pytest_output(stdout)

        error_msg = stderr if exit_code != 0 else ""

        return TestResult(
            name="Vector Database",
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            error_message=error_msg
        )

    def run_agent_management_smoke_tests(self) -> TestResult:
        """Run agent management smoke tests."""
        print("🚀 Running Agent Management Smoke Tests...")
        start_time = time.time()

        command = [
            sys.executable, "-m", "pytest",
            "tests/test_agent_management_smoke.py",
            "-v", "--tb=short"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time
        passed, failed, skipped = self.parse_pytest_output(stdout)

        error_msg = stderr if exit_code != 0 else ""

        return TestResult(
            name="Agent Management",
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            error_message=error_msg
        )

    def run_contract_system_smoke_tests(self) -> TestResult:
        """Run contract system smoke tests."""
        print("🚀 Running Contract System Smoke Tests...")
        start_time = time.time()

        command = [
            sys.executable, "-m", "pytest",
            "tests/test_contract_system_smoke.py",
            "-v", "--tb=short"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time
        passed, failed, skipped = self.parse_pytest_output(stdout)

        error_msg = stderr if exit_code != 0 else ""

        return TestResult(
            name="Contract System",
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            error_message=error_msg
        )

    def run_web_interface_smoke_tests(self) -> TestResult:
        """Run web interface smoke tests."""
        print("🚀 Running Web Interface Smoke Tests...")
        start_time = time.time()

        command = [
            sys.executable, "-m", "pytest",
            "tests/ui-common.test.js",
            "-v", "--tb=short"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time
        passed, failed, skipped = self.parse_pytest_output(stdout)

        error_msg = stderr if exit_code != 0 else ""

        return TestResult(
            name="Web Interface",
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            error_message=error_msg
        )

    def run_code_quality_checks(self) -> TestResult:
        """Run code quality checks."""
        print("🚀 Running Code Quality Checks...")
        start_time = time.time()

        # Check for large files (V2 compliance)
        command = [
            "powershell", "-Command",
            "Get-ChildItem -Path src -Recurse -Include '*.py' | ForEach-Object { $lineCount = (Get-Content $_.FullName | Measure-Object -Line).Lines; Write-Output \"$lineCount $($_.FullName)\" } | Sort-Object -Descending { [int]$_.Split()[0] } | Select-Object -First 20"
        ]

        exit_code, stdout, stderr = self.run_command(command)

        duration = time.time() - start_time

        # Parse results to check for violations
        lines = stdout.split('\n')
        violations = []

        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        line_count = int(parts[0])
                        file_path = ' '.join(parts[1:])

                        if line_count > 600:
                            violations.append(f"🚨 CRITICAL: {file_path} ({line_count} lines)")
                        elif line_count > 400:
                            violations.append(f"⚠️ MAJOR: {file_path} ({line_count} lines)")
                    except (ValueError, IndexError):
                        continue

        passed = 1 if len(violations) == 0 else 0
        failed = len(violations)

        error_msg = "\n".join(violations) if violations else ""

        return TestResult(
            name="Code Quality",
            passed=passed,
            failed=failed,
            skipped=0,
            duration=duration,
            error_message=error_msg
        )

    def generate_report(self) -> str:
        """Generate a comprehensive test report."""
        total_passed = sum(result.passed for result in self.test_results)
        total_failed = sum(result.failed for result in self.test_results)
        total_skipped = sum(result.skipped for result in self.test_results)
        total_duration = sum(result.duration for result in self.test_results)

        report = []
        report.append("=" * 80)
        report.append("🧪 AGENT CELLPHONE V2 - SMOKE TEST REPORT")
        report.append("=" * 80)
        report.append(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {total_duration:.2f} seconds")
        report.append("")

        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 40)
        report.append(f"✅ Passed: {total_passed}")
        report.append(f"❌ Failed: {total_failed}")
        report.append(f"⏭️ Skipped: {total_skipped}")
        report.append(f"📈 Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "N/A")
        report.append("")

        # Detailed results
        report.append("📋 DETAILED RESULTS")
        report.append("-" * 40)

        for result in self.test_results:
            status_icon = "✅" if result.failed == 0 else "❌" if result.failed > 0 else "⏭️"
            report.append(f"{status_icon} {result.name}")
            report.append(f"   Duration: {result.duration:.2f}s")
            report.append(f"   Passed: {result.passed}, Failed: {result.failed}, Skipped: {result.skipped}")

            if result.error_message:
                report.append(f"   Error: {result.error_message[:100]}{'...' if len(result.error_message) > 100 else ''}")

            report.append("")

        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)

        if total_failed > 0:
            report.append("❌ Some tests failed. Please review the detailed error messages above.")
            report.append("   - Check for missing dependencies")
            report.append("   - Verify configuration files")
            report.append("   - Ensure all services are running")
        else:
            report.append("✅ All smoke tests passed! The system is in good health.")

        if total_skipped > 0:
            report.append(f"⏭️ {total_skipped} tests were skipped. This may indicate missing optional components.")

        report.append("")
        report.append("🔧 V2 COMPLIANCE STATUS")
        report.append("-" * 40)

        code_quality_result = next((r for r in self.test_results if r.name == "Code Quality"), None)
        if code_quality_result and code_quality_result.failed == 0:
            report.append("✅ Code quality checks passed - V2 compliance maintained")
        else:
            report.append("⚠️ Code quality issues detected - review file sizes and structure")

        report.append("=" * 80)

        return "\n".join(report)

    def run_all_smoke_tests(self) -> bool:
        """Run all smoke tests and return success status."""
        print("🚀 Starting Agent Cellphone V2 Smoke Test Suite")
        print("=" * 60)

        self.start_time = time.time()
        self.test_results = []

        # Run all test suites
        test_suites = [
            self.run_messaging_smoke_tests,
            self.run_vector_db_smoke_tests,
            self.run_agent_management_smoke_tests,
            self.run_contract_system_smoke_tests,
            self.run_web_interface_smoke_tests,
            self.run_code_quality_checks,
        ]

        for test_suite in test_suites:
            try:
                result = test_suite()
                self.test_results.append(result)
            except Exception as e:
                # Handle test suite failures
                error_result = TestResult(
                    name=test_suite.__name__.replace('run_', '').replace('_smoke_tests', '').replace('_', ' ').title(),
                    passed=0,
                    failed=1,
                    skipped=0,
                    duration=0,
                    error_message=f"Test suite execution failed: {e}"
                )
                self.test_results.append(error_result)

        # Generate and display report
        report = self.generate_report()
        print(report)

        # Save report to file
        report_file = self.project_root / "smoke_test_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📄 Detailed report saved to: {report_file}")

        # Return overall success status
        total_failed = sum(result.failed for result in self.test_results)
        return total_failed == 0


def main():
    """Main entry point for smoke test runner."""
    runner = SmokeTestRunner()
    success = runner.run_all_smoke_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
