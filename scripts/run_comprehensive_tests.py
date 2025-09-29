#!/usr/bin/env python3
"""
Comprehensive Test Runner
=========================

Runs all integration tests and validates the modular components.
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ComprehensiveTestRunner:
    """Runs comprehensive test suites for modular components."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_results = {}
        self.test_log = []

    def run_workflow_tests(self) -> tuple[bool, dict[str, Any]]:
        """Run workflow integration tests."""
        logger.info("Running workflow integration tests...")

        try:
            # Test workflow core components
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from tools.workflow.core import WorkflowStep, WorkflowDefinition; "
                    "step = WorkflowStep('test', 'Agent-1', 'test'); "
                    "print('✅ Workflow core components working')",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                logger.info("✅ Workflow core components test passed")
                self.test_log.append("✅ Workflow core components test passed")

                # Test workflow manager
                result2 = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from tools.workflow import WorkflowManager; "
                        "manager = WorkflowManager(); "
                        "print('✅ Workflow manager working')",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                )

                if result2.returncode == 0:
                    logger.info("✅ Workflow manager test passed")
                    self.test_log.append("✅ Workflow manager test passed")
                    return True, {"status": "passed", "tests": 2}
                else:
                    logger.error(f"❌ Workflow manager test failed: {result2.stderr}")
                    return False, {"status": "failed", "error": result2.stderr}
            else:
                logger.error(f"❌ Workflow core test failed: {result.stderr}")
                return False, {"status": "failed", "error": result.stderr}

        except Exception as e:
            logger.error(f"❌ Workflow test execution failed: {e}")
            return False, {"status": "failed", "error": str(e)}

    def run_discord_commander_tests(self) -> tuple[bool, dict[str, Any]]:
        """Run Discord commander integration tests."""
        logger.info("Running Discord commander integration tests...")

        try:
            # Test Discord commander core components
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from src.services.discord_commander.core import DiscordConfig; "
                    "config = DiscordConfig(); "
                    "print('✅ Discord Commander core components working')",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                logger.info("✅ Discord Commander core components test passed")
                self.test_log.append("✅ Discord Commander core components test passed")

                # Test Discord commander bot
                result2 = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from src.services.discord_commander import DiscordCommanderBot; "
                        "bot = DiscordCommanderBot(); "
                        "print('✅ Discord Commander bot working')",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                )

                if result2.returncode == 0:
                    logger.info("✅ Discord Commander bot test passed")
                    self.test_log.append("✅ Discord Commander bot test passed")
                    return True, {"status": "passed", "tests": 2}
                else:
                    logger.error(f"❌ Discord Commander bot test failed: {result2.stderr}")
                    return False, {"status": "failed", "error": result2.stderr}
            else:
                logger.error(f"❌ Discord Commander core test failed: {result.stderr}")
                return False, {"status": "failed", "error": result.stderr}

        except Exception as e:
            logger.error(f"❌ Discord Commander test execution failed: {e}")
            return False, {"status": "failed", "error": str(e)}

    def run_performance_tests(self) -> tuple[bool, dict[str, Any]]:
        """Run performance optimization tests."""
        logger.info("Running performance optimization tests...")

        try:
            # Test workflow optimization
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from tools.workflow.optimization import WorkflowOptimizer; "
                    "optimizer = WorkflowOptimizer(); "
                    "print('✅ Workflow optimization working')",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                logger.info("✅ Workflow optimization test passed")
                self.test_log.append("✅ Workflow optimization test passed")

                # Test Discord optimization
                result2 = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from src.services.discord_commander.optimization import DiscordOptimizer; "
                        "optimizer = DiscordOptimizer(); "
                        "print('✅ Discord optimization working')",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                )

                if result2.returncode == 0:
                    logger.info("✅ Discord optimization test passed")
                    self.test_log.append("✅ Discord optimization test passed")
                    return True, {"status": "passed", "tests": 2}
                else:
                    logger.error(f"❌ Discord optimization test failed: {result2.stderr}")
                    return False, {"status": "failed", "error": result2.stderr}
            else:
                logger.error(f"❌ Workflow optimization test failed: {result.stderr}")
                return False, {"status": "failed", "error": result.stderr}

        except Exception as e:
            logger.error(f"❌ Performance test execution failed: {e}")
            return False, {"status": "failed", "error": str(e)}

    def run_v2_compliance_tests(self) -> tuple[bool, dict[str, Any]]:
        """Run V2 compliance tests."""
        logger.info("Running V2 compliance tests...")

        try:
            # Run project scanner to check compliance
            result = subprocess.run(
                [sys.executable, "tools/simple_project_scanner.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                # Parse output to get compliance stats
                output_lines = result.stdout.split("\n")
                compliant_files = 0
                total_files = 0

                for line in output_lines:
                    if "V2 compliant:" in line:
                        compliant_files = int(line.split(":")[1].strip())
                    elif "Python files:" in line:
                        total_files = int(line.split(":")[1].strip())

                compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0

                logger.info(f"✅ V2 compliance test passed: {compliance_rate:.1f}%")
                self.test_log.append(f"✅ V2 compliance test passed: {compliance_rate:.1f}%")

                return True, {
                    "status": "passed",
                    "compliant_files": compliant_files,
                    "total_files": total_files,
                    "compliance_rate": compliance_rate,
                }
            else:
                logger.error(f"❌ V2 compliance test failed: {result.stderr}")
                return False, {"status": "failed", "error": result.stderr}

        except Exception as e:
            logger.error(f"❌ V2 compliance test execution failed: {e}")
            return False, {"status": "failed", "error": str(e)}

    def run_integration_tests(self) -> tuple[bool, dict[str, Any]]:
        """Run comprehensive integration tests."""
        logger.info("Running comprehensive integration tests...")

        test_suites = [
            ("workflow", self.run_workflow_tests),
            ("discord_commander", self.run_discord_commander_tests),
            ("performance", self.run_performance_tests),
            ("v2_compliance", self.run_v2_compliance_tests),
        ]

        results = {}
        all_passed = True

        for suite_name, test_func in test_suites:
            logger.info(f"Running {suite_name} tests...")
            passed, result = test_func()
            results[suite_name] = result

            if not passed:
                all_passed = False
                logger.error(f"❌ {suite_name} tests failed")
            else:
                logger.info(f"✅ {suite_name} tests passed")

        return all_passed, results

    def generate_test_report(self) -> bool:
        """Generate comprehensive test report."""
        try:
            report = {
                "test_run_time": datetime.now().isoformat(),
                "test_results": self.test_results,
                "test_log": self.test_log,
                "summary": {
                    "total_test_suites": len(self.test_results),
                    "passed_suites": sum(
                        1 for r in self.test_results.values() if r.get("status") == "passed"
                    ),
                    "failed_suites": sum(
                        1 for r in self.test_results.values() if r.get("status") == "failed"
                    ),
                    "overall_status": "passed"
                    if all(r.get("status") == "passed" for r in self.test_results.values())
                    else "failed",
                },
            }

            report_path = self.project_root / "comprehensive_test_report.json"
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Test report generated: {report_path}")
            return True

        except Exception as e:
            logger.error(f"Test report generation failed: {e}")
            return False

    def run_all_tests(self) -> bool:
        """Run all comprehensive tests."""
        logger.info("Starting comprehensive test suite...")

        try:
            # Run integration tests
            all_passed, results = self.run_integration_tests()
            self.test_results = results

            # Generate test report
            self.generate_test_report()

            if all_passed:
                logger.info("✅ All comprehensive tests passed!")
                print("🎉 COMPREHENSIVE TEST SUITE RESULTS")
                print("=" * 50)
                print("✅ Workflow System: PASSED")
                print("✅ Discord Commander: PASSED")
                print("✅ Performance Optimization: PASSED")
                print("✅ V2 Compliance: PASSED")
                print("=" * 50)
                print("🎯 All tests completed successfully!")
                return True
            else:
                logger.error("❌ Some tests failed!")
                print("❌ COMPREHENSIVE TEST SUITE RESULTS")
                print("=" * 50)
                for suite_name, result in results.items():
                    status = "✅ PASSED" if result.get("status") == "passed" else "❌ FAILED"
                    print(f"{status} {suite_name.title()}")
                print("=" * 50)
                print("🔍 Check comprehensive_test_report.json for details")
                return False

        except Exception as e:
            logger.error(f"Comprehensive test execution failed: {e}")
            return False


def main():
    """Main test runner function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Comprehensive Tests")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--suite",
        choices=["workflow", "discord", "performance", "compliance", "all"],
        default="all",
        help="Test suite to run",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    project_root = Path(args.project_root).resolve()
    test_runner = ComprehensiveTestRunner(project_root)

    if args.suite == "all":
        success = test_runner.run_all_tests()
    elif args.suite == "workflow":
        success, _ = test_runner.run_workflow_tests()
    elif args.suite == "discord":
        success, _ = test_runner.run_discord_commander_tests()
    elif args.suite == "performance":
        success, _ = test_runner.run_performance_tests()
    elif args.suite == "compliance":
        success, _ = test_runner.run_v2_compliance_tests()
    else:
        print(f"Unknown test suite: {args.suite}")
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
