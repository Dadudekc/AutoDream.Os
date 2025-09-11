#!/usr/bin/env python3
"""
V2_SWARM Comprehensive Test Runner - Agent-4 Coordination
========================================================

Comprehensive test execution script that runs all agent-specific tests,
generates coverage reports, and coordinates the testing mission.

Author: Agent-4 (Quality Assurance Captain)
License: MIT
"""

import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime
import argparse

class ComprehensiveTestRunner:
    """Comprehensive test runner for V2_SWARM."""

    def __init__(self):
        """Initialize test runner."""
        self.project_root = Path(__file__).parent
        self.test_reports_dir = self.project_root / "test_reports"
        self.test_reports_dir.mkdir(exist_ok=True)
        self.start_time = datetime.now()

        # Test configuration
        self.coverage_threshold = 85
        self.test_timeout = 3600  # 1 hour timeout

    def run_pytest_with_coverage(self, markers: str = None, verbose: bool = True) -> dict:
        """Run pytest with coverage analysis."""
        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=src",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--cov-report=xml:coverage.xml",
            "--cov-fail-under=85",
            "--durations=10",
            "-v" if verbose else "-q"
        ]

        if markers:
            cmd.extend(["-m", markers])

        # Add test paths
        cmd.append("tests/")

        print(f"🚀 Running pytest with command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=self.test_timeout
            )

            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": ' '.join(cmd)
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Test execution timed out",
                "command": ' '.join(cmd)
            }

    def run_agent_specific_tests(self, agent: str) -> dict:
        """Run tests specific to an agent."""
        marker = f"agent{agent[-1]}"  # Extract number from agent name
        print(f"\n🎯 Running {agent.upper()} specific tests...")

        return self.run_pytest_with_coverage(f"agent{agent[-1]}", verbose=False)

    def run_all_tests_by_category(self) -> dict:
        """Run all tests organized by category."""
        categories = {
            "unit": "Unit Tests",
            "integration": "Integration Tests",
            "system": "System Tests",
            "slow": "Slow Tests"
        }

        results = {}

        for category, description in categories.items():
            print(f"\n📊 Running {description}...")
            result = self.run_pytest_with_coverage(category, verbose=False)
            results[category] = result

            if result["success"]:
                print(f"✅ {description}: PASSED")
            else:
                print(f"❌ {description}: FAILED")

        return results

    def run_agent_coordinated_tests(self) -> dict:
        """Run tests coordinated by agent assignments."""
        agents = {
            "agent1": "Core Systems Integration",
            "agent2": "Architecture & Design Patterns",
            "agent3": "Infrastructure & Deployment",
            "agent4": "Quality Assurance & Coordination",
            "agent5": "Business Intelligence & Data",
            "agent6": "Coordination & Communication",
            "agent7": "Web Development & APIs",
            "agent8": "Operations & Support"
        }

        results = {}

        for agent, description in agents.items():
            print(f"\n🤖 {agent.upper()}: {description}")
            result = self.run_agent_specific_tests(agent)
            results[agent] = result

            if result["success"]:
                print(f"✅ {agent.upper()}: PASSED")
            else:
                print(f"❌ {agent.upper()}: FAILED - {result.get('stderr', '')[:100]}...")

        return results

    def generate_comprehensive_report(self, test_results: dict) -> str:
        """Generate comprehensive test report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.test_reports_dir / f"comprehensive_test_report_{timestamp}.json"

        # Analyze coverage if available
        coverage_data = self._analyze_coverage_report()

        report = {
            "timestamp": datetime.now().isoformat(),
            "execution_time": (datetime.now() - self.start_time).total_seconds(),
            "test_results": test_results,
            "coverage_analysis": coverage_data,
            "summary": self._calculate_overall_summary(test_results, coverage_data),
            "recommendations": self._generate_test_recommendations(test_results, coverage_data)
        }

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        return str(report_file)

    def _analyze_coverage_report(self) -> dict:
        """Analyze coverage report data."""
        coverage_file = self.project_root / "coverage.xml"

        if not coverage_file.exists():
            return {"error": "Coverage report not found"}

        try:
            # Simple XML parsing for coverage data
            with open(coverage_file) as f:
                content = f.read()

            # Extract basic coverage information
            if 'line-rate=' in content:
                # Parse coverage percentage from XML
                import re
                rate_match = re.search(r'line-rate="([^"]*)"', content)
                if rate_match:
                    coverage_percent = float(rate_match.group(1)) * 100
                    return {
                        "overall_coverage": coverage_percent,
                        "target_achieved": coverage_percent >= self.coverage_threshold,
                        "status": "success"
                    }

        except Exception as e:
            return {"error": f"Failed to parse coverage report: {e}"}

        return {"error": "Could not extract coverage data"}

    def _calculate_overall_summary(self, test_results: dict, coverage_data: dict) -> dict:
        """Calculate overall test summary."""
        total_runs = 0
        successful_runs = 0

        # Count successful test runs
        for category, result in test_results.items():
            if isinstance(result, dict) and result.get("success"):
                successful_runs += 1
            total_runs += 1

        coverage_achieved = coverage_data.get("overall_coverage", 0)
        target_met = coverage_achieved >= self.coverage_threshold

        return {
            "total_test_categories": total_runs,
            "successful_categories": successful_runs,
            "success_rate": (successful_runs / total_runs * 100) if total_runs > 0 else 0,
            "coverage_percentage": coverage_achieved,
            "coverage_target_met": target_met,
            "overall_status": "SUCCESS" if successful_runs == total_runs and target_met else "NEEDS_IMPROVEMENT"
        }

    def _generate_test_recommendations(self, test_results: dict, coverage_data: dict) -> list:
        """Generate test improvement recommendations."""
        recommendations = []

        # Analyze failed tests
        failed_categories = [
            category for category, result in test_results.items()
            if isinstance(result, dict) and not result.get("success", False)
        ]

        if failed_categories:
            recommendations.append(f"Focus on failed categories: {', '.join(failed_categories)}")

        # Analyze coverage
        coverage = coverage_data.get("overall_coverage", 0)
        if coverage < self.coverage_threshold:
            gap = self.coverage_threshold - coverage
            recommendations.append(f"Improve coverage by {gap:.1f}% to reach {self.coverage_threshold}% target")

        # General recommendations
        recommendations.extend([
            "Add more integration tests for cross-component interactions",
            "Implement performance benchmarks for critical paths",
            "Add error handling tests for edge cases",
            "Create system-level tests for end-to-end scenarios"
        ])

        return recommendations

    def print_execution_summary(self, test_results: dict, coverage_data: dict):
        """Print execution summary to console."""
        summary = self._calculate_overall_summary(test_results, coverage_data)

        print("\n" + "="*60)
        print("🎯 V2_SWARM COMPREHENSIVE TEST EXECUTION SUMMARY")
        print("="*60)

        print("📊 Test Results:")
        print(f"   Categories Run: {summary['total_test_categories']}")
        print(f"   Successful: {summary['successful_categories']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")

        print("
📈 Coverage Analysis:"        print(f"   Overall Coverage: {summary['coverage_percentage']:.1f}%")
        print(f"   Target (85%): {'✅ MET' if summary['coverage_target_met'] else '❌ NOT MET'}")

        print("
🏆 Overall Status:"        status_emoji = "✅" if summary['overall_status'] == "SUCCESS" else "⚠️"
        print(f"   {status_emoji} {summary['overall_status']}")

        print("
💡 Key Recommendations:"        recommendations = self._generate_test_recommendations(test_results, coverage_data)
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")

        print("\n📁 Reports Generated:")
        print(f"   HTML Coverage: htmlcov/index.html")
        print(f"   XML Coverage: coverage.xml")
        print(f"   Comprehensive Report: test_reports/comprehensive_test_report_*.json")

        execution_time = (datetime.now() - self.start_time).total_seconds()
        print(".1f"
    def run_full_test_suite(self) -> dict:
        """Run the complete test suite."""
        print("🚀 STARTING V2_SWARM COMPREHENSIVE TEST SUITE")
        print("="*60)
        print("🎯 Target: 85%+ Coverage | All Agent Tests | Full Integration")
        print("="*60)

        # Run all tests by category
        print("\n📊 PHASE 1: Running Tests by Category")
        category_results = self.run_all_tests_by_category()

        # Run agent-specific tests
        print("\n🤖 PHASE 2: Running Agent-Coordinated Tests")
        agent_results = self.run_agent_coordinated_tests()

        # Run full integration test
        print("\n🔗 PHASE 3: Running Full Integration Test")
        integration_result = self.run_pytest_with_coverage("integration or system", verbose=True)

        # Combine all results
        all_results = {
            "categories": category_results,
            "agents": agent_results,
            "integration": integration_result
        }

        # Generate comprehensive report
        report_file = self.generate_comprehensive_report(all_results)

        # Print final summary
        coverage_data = self._analyze_coverage_report()
        self.print_execution_summary(all_results, coverage_data)

        print(f"\n📄 Detailed Report: {report_file}")

        return all_results

def main():
    """Main entry point for comprehensive test execution."""
    parser = argparse.ArgumentParser(description="V2_SWARM Comprehensive Test Runner")
    parser.add_argument("--category", choices=["unit", "integration", "system", "slow"],
                       help="Run specific test category")
    parser.add_argument("--agent", choices=[f"agent{i}" for i in range(1, 9)],
                       help="Run specific agent tests")
    parser.add_argument("--quick", action="store_true",
                       help="Run quick test summary only")
    parser.add_argument("--coverage-only", action="store_true",
                       help="Run coverage analysis only")

    args = parser.parse_args()

    runner = ComprehensiveTestRunner()

    if args.category:
        print(f"🎯 Running {args.category} tests only...")
        result = runner.run_pytest_with_coverage(args.category)
        print("✅ PASSED" if result["success"] else "❌ FAILED")

    elif args.agent:
        print(f"🤖 Running {args.agent.upper()} tests only...")
        result = runner.run_agent_specific_tests(args.agent)
        print("✅ PASSED" if result["success"] else "❌ FAILED")

    elif args.coverage_only:
        print("📊 Running coverage analysis...")
        coverage_data = runner._analyze_coverage_report()
        print(f"Coverage: {coverage_data.get('overall_coverage', 0):.1f}%")
        print(f"Target Met: {'✅' if coverage_data.get('target_achieved', False) else '❌'}")

    elif args.quick:
        print("⚡ Running quick test summary...")
        # Run a subset of critical tests
        result = runner.run_pytest_with_coverage("unit and not slow", verbose=False)
        coverage_data = runner._analyze_coverage_report()

        print(f"Quick Test: {'✅ PASSED' if result['success'] else '❌ FAILED'}")
        print(".1f"
    else:
        # Run full comprehensive test suite
        runner.run_full_test_suite()

if __name__ == "__main__":
    main()
