#!/usr/bin/env python3
"""
Integration Testing Suite Runner
=================================

Orchestrates execution of comprehensive integration testing framework:
- End-to-end tests
- API testing suites
- Cross-service integration tests
- Deployment verification

Usage:
    python tests/run_integration_tests.py [options]

Options:
    --e2e-only          Run only end-to-end tests
    --api-only          Run only API tests
    --integration-only  Run only cross-service integration tests
    --deployment-only   Run only deployment verification
    --environment ENV   Target environment (development/staging/production)
    --verbose           Enable verbose output
    --report FORMAT     Report format (json/html/summary)

Author: Agent-7 (Web Development Specialist)
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tests.integration_testing_framework import IntegrationTestFramework, TestResult, TestStatus, TestType


class IntegrationTestRunner:
    """Orchestrates execution of all integration test suites."""

    def __init__(self, base_url: str = "http://localhost:8000", environment: str = "development"):
        self.base_url = base_url
        self.environment = environment
        self.framework = IntegrationTestFramework(base_url=base_url)
        self.test_results = []
        self.execution_summary = {}

    def run_all_tests(self) -> Dict[str, Any]:
        """Run complete integration test suite."""
        print("🐝 Starting Swarm Intelligence Integration Test Suite")
        print("=" * 60)

        start_time = time.time()

        # Execute test suites
        test_suites = [
            ("End-to-End Tests", self.run_e2e_tests),
            ("API Tests", self.run_api_tests),
            ("Cross-Service Integration", self.run_integration_tests),
            ("Deployment Verification", self.run_deployment_tests)
        ]

        all_results = []

        for suite_name, suite_func in test_suites:
            print(f"\n📋 Running {suite_name}...")
            try:
                results = suite_func()
                all_results.extend(results)
                passed = len([r for r in results if r.status == TestStatus.PASSED])
                failed = len([r for r in results if r.status == TestStatus.FAILED])
                print(f"   ✅ {passed} passed, ❌ {failed} failed")
            except Exception as e:
                print(f"   ❌ Suite failed: {e}")
                # Create error result
                error_result = TestResult(
                    test_id=f"suite_error_{suite_name.lower().replace(' ', '_')}",
                    test_name=f"Suite Error: {suite_name}",
                    test_type=TestType.INTEGRATION,
                    status=TestStatus.ERROR,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    duration=0.0,
                    error_message=str(e)
                )
                all_results.append(error_result)

        end_time = time.time()
        total_duration = end_time - start_time

        # Generate summary
        summary = self._generate_summary(all_results, total_duration)

        print("\n" + "=" * 60)
        print("🐝 INTEGRATION TEST SUITE COMPLETED")
        print("=" * 60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(".2f")
        print(f"Success Rate: {summary['success_rate']:.1%}")

        if summary['failed'] > 0:
            print(f"\n❌ Failed Tests: {', '.join(summary['failed_tests'])}")

        print(f"\nEnvironment: {self.environment}")
        print(f"Base URL: {self.base_url}")

        self.test_results = all_results
        self.execution_summary = summary

        return {
            "summary": summary,
            "results": [self._result_to_dict(r) for r in all_results],
            "metadata": {
                "environment": self.environment,
                "base_url": self.base_url,
                "execution_time": datetime.now().isoformat(),
                "total_duration": total_duration
            }
        }

    def run_e2e_tests(self) -> List[TestResult]:
        """Run end-to-end test suite."""
        results = []

        # Import and run E2E tests
        try:
            from tests.e2e.test_agent_lifecycle_e2e import run_e2e_test_suite
            results = run_e2e_test_suite()
        except ImportError:
            print("   ⚠️  E2E test suite not available")
        except Exception as e:
            print(f"   ❌ E2E test execution failed: {e}")

        return results

    def run_api_tests(self) -> List[TestResult]:
        """Run API testing suite."""
        results = []

        # Import and run API tests
        try:
            from tests.api.test_agent_api_suite import run_agent_api_test_suite
            results = run_agent_api_test_suite()
        except ImportError:
            print("   ⚠️  API test suite not available")
        except Exception as e:
            print(f"   ❌ API test execution failed: {e}")

        return results

    def run_integration_tests(self) -> List[TestResult]:
        """Run cross-service integration tests."""
        results = []

        # Import and run integration tests
        try:
            from tests.integration.test_cross_service_integration import run_cross_service_integration_suite
            results = run_cross_service_integration_suite()
        except ImportError:
            print("   ⚠️  Integration test suite not available")
        except Exception as e:
            print(f"   ❌ Integration test execution failed: {e}")

        return results

    def run_deployment_tests(self) -> List[TestResult]:
        """Run deployment verification tests."""
        results = []

        try:
            from tests.deployment.test_deployment_verification import DeploymentVerificationSystem

            verifier = DeploymentVerificationSystem(
                environment=self.environment,
                base_url=self.base_url
            )

            # Run verification and convert to TestResult format
            verification_results = verifier.run_full_deployment_verification()

            # Convert to TestResult
            result = TestResult(
                test_id="deployment_verification",
                test_name="Deployment Verification Suite",
                test_type=TestType.DEPLOYMENT,
                status=TestStatus.PASSED if verification_results["overall_status"] == "passed" else TestStatus.FAILED,
                start_time=datetime.fromisoformat(verification_results["verification_start"]),
                end_time=datetime.fromisoformat(verification_results["verification_end"]),
                duration=verification_results["total_duration"],
                metadata={
                    "verification_results": verification_results,
                    "failed_checks": verification_results.get("failed_checks", [])
                }
            )

            results.append(result)

        except ImportError:
            print("   ⚠️  Deployment verification not available")
        except Exception as e:
            print(f"   ❌ Deployment verification failed: {e}")
            # Create error result
            error_result = TestResult(
                test_id="deployment_error",
                test_name="Deployment Verification Error",
                test_type=TestType.DEPLOYMENT,
                status=TestStatus.ERROR,
                start_time=datetime.now(),
                end_time=datetime.now(),
                duration=0.0,
                error_message=str(e)
            )
            results.append(error_result)

        return results

    def _generate_summary(self, results: List[TestResult], total_duration: float) -> Dict[str, Any]:
        """Generate execution summary."""
        total_tests = len(results)
        passed = len([r for r in results if r.status == TestStatus.PASSED])
        failed = len([r for r in results if r.status == TestStatus.FAILED])
        errors = len([r for r in results if r.status == TestStatus.ERROR])
        skipped = len([r for r in results if r.status == TestStatus.SKIPPED])

        failed_tests = [r.test_name for r in results if r.status in [TestStatus.FAILED, TestStatus.ERROR]]

        success_rate = passed / total_tests if total_tests > 0 else 0

        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "success_rate": success_rate,
            "total_duration": total_duration,
            "failed_tests": failed_tests,
            "test_types": {
                test_type.value: len([r for r in results if r.test_type == test_type])
                for test_type in TestType
            }
        }

    def _result_to_dict(self, result: TestResult) -> Dict[str, Any]:
        """Convert TestResult to dictionary."""
        return {
            "test_id": result.test_id,
            "test_name": result.test_name,
            "test_type": result.test_type.value if result.test_type else None,
            "status": result.status.value if result.status else None,
            "duration": result.duration,
            "start_time": result.start_time.isoformat() if result.start_time else None,
            "end_time": result.end_time.isoformat() if result.end_time else None,
            "error_message": result.error_message,
            "metadata": result.metadata
        }

    def save_report(self, filename: str, format: str = "json") -> None:
        """Save test execution report."""
        report_data = {
            "integration_test_report": {
                "generated_at": datetime.now().isoformat(),
                "runner_version": "2.0.0",
                **self.execution_summary,
                "results": [self._result_to_dict(r) for r in self.test_results]
            }
        }

        if format == "json":
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
        elif format == "html":
            self._save_html_report(filename, report_data)
        else:
            raise ValueError(f"Unsupported report format: {format}")

        print(f"Report saved to: {filename}")

    def _save_html_report(self, filename: str, report_data: Dict[str, Any]) -> None:
        """Save HTML formatted report."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Intelligence Integration Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 4px; text-align: center; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .error {{ color: #ffc107; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .test-result.passed {{ border-left-color: #28a745; background: #f8fff8; }}
        .test-result.failed {{ border-left-color: #dc3545; background: #fff8f8; }}
        .test-result.error {{ border-left-color: #ffc107; background: #fffef8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐝 Swarm Intelligence Integration Test Report</h1>
        <p>Generated: {report_data['integration_test_report']['generated_at']}</p>
        <p>Environment: {self.environment} | Base URL: {self.base_url}</p>
    </div>

    <div class="summary">
        <h2>Test Summary</h2>
        <div class="metric">
            <div style="font-size: 2em; font-weight: bold;">{report_data['integration_test_report']['total_tests']}</div>
            <div>Total Tests</div>
        </div>
        <div class="metric passed">
            <div style="font-size: 2em; font-weight: bold;">{report_data['integration_test_report']['passed']}</div>
            <div>Passed</div>
        </div>
        <div class="metric failed">
            <div style="font-size: 2em; font-weight: bold;">{report_data['integration_test_report']['failed']}</div>
            <div>Failed</div>
        </div>
        <div class="metric error">
            <div style="font-size: 2em; font-weight: bold;">{report_data['integration_test_report']['errors']}</div>
            <div>Errors</div>
        </div>
        <div class="metric">
            <div style="font-size: 2em; font-weight: bold;">{report_data['integration_test_report']['success_rate']:.1%}</div>
            <div>Success Rate</div>
        </div>
    </div>

    <h2>Test Results</h2>
"""

        for result in report_data['integration_test_report']['results']:
            status_class = result['status'].lower()
            html_content += f"""
    <div class="test-result {status_class}">
        <h4>{result['test_name']}</h4>
        <p><strong>Status:</strong> {result['status']} | <strong>Duration:</strong> {result['duration']:.2f}s</p>
        <p><strong>Type:</strong> {result['test_type']}</p>
        {"<p><strong>Error:</strong> " + result['error_message'] + "</p>" if result.get('error_message') else ""}
    </div>
"""

        html_content += """
</body>
</html>
"""

        with open(filename, 'w') as f:
            f.write(html_content)


def main():
    """Main entry point for integration test runner."""
    parser = argparse.ArgumentParser(description="Swarm Intelligence Integration Test Runner")
    parser.add_argument("--e2e-only", action="store_true", help="Run only end-to-end tests")
    parser.add_argument("--api-only", action="store_true", help="Run only API tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only cross-service integration tests")
    parser.add_argument("--deployment-only", action="store_true", help="Run only deployment verification")
    parser.add_argument("--environment", choices=["development", "staging", "production"],
                       default="development", help="Target environment")
    parser.add_argument("--base-url", help="Base URL for API endpoints")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--report", choices=["json", "html", "summary"],
                       default="summary", help="Report format")

    args = parser.parse_args()

    # Determine base URL
    base_url = args.base_url
    if not base_url:
        if args.environment == "production":
            base_url = "https://api.swarm.intelligence"
        elif args.environment == "staging":
            base_url = "https://staging.swarm.intelligence"
        else:
            base_url = "http://localhost:8000"

    # Create test runner
    runner = IntegrationTestRunner(base_url=base_url, environment=args.environment)

    # Determine which tests to run
    if args.e2e_only:
        print("Running E2E tests only...")
        results = runner.run_e2e_tests()
    elif args.api_only:
        print("Running API tests only...")
        results = runner.run_api_tests()
    elif args.integration_only:
        print("Running integration tests only...")
        results = runner.run_integration_tests()
    elif args.deployment_only:
        print("Running deployment verification only...")
        results = runner.run_deployment_tests()
    else:
        # Run all tests
        report_data = runner.run_all_tests()

        # Save report if requested
        if args.report != "summary":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"integration_test_report_{timestamp}.{args.report}"
            runner.save_report(filename, args.report)
            print(f"📊 Detailed report saved: {filename}")

        # Exit with appropriate code
        summary = runner.execution_summary
        if summary["success_rate"] >= 0.8:  # 80% success rate required
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
