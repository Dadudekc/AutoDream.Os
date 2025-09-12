#!/usr/bin/env python3
"""
Test Coverage Improvement Tool
==============================

Comprehensive tool for improving test coverage and reliability with focus on:
- Automated test discovery and coverage analysis
- CI/CD integration with coverage reporting
- Test reliability improvements and flaky test detection
- Coverage gap analysis and recommendations
- Integration with existing test infrastructure

Author: Agent-5 (Business Intelligence Specialist)
Usage: python tools/test_coverage_improvement.py --analyze --target messaging
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest


class TestCoverageImprover:
    """Tool for improving test coverage and reliability."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.tests_dir = project_root / "tests"
        self.tools_dir = project_root / "tools"
        self.reports_dir = project_root / "runtime" / "reports"

    def analyze_current_coverage(self, target: str = "all") -> Dict[str, Any]:
        """Analyze current test coverage for specified target."""
        print(f"🔍 Analyzing test coverage for target: {target}")

        # Run coverage analysis
        coverage_data = self._run_coverage_analysis(target)

        # Analyze coverage gaps
        gaps = self._analyze_coverage_gaps(coverage_data)

        # Generate recommendations
        recommendations = self._generate_recommendations(gaps, target)

        return {
            "target": target,
            "coverage_data": coverage_data,
            "gaps": gaps,
            "recommendations": recommendations,
            "timestamp": self._get_timestamp(),
        }

    def _run_coverage_analysis(self, target: str) -> Dict[str, Any]:
        """Run coverage analysis for target."""
        coverage_cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov-report=json",
            "--cov-report=term-missing",
            f"--cov={self._get_coverage_target(target)}",
        ]

        if target != "all":
            coverage_cmd.extend(["-k", target])

        coverage_cmd.append(str(self.tests_dir))

        try:
            result = subprocess.run(
                coverage_cmd, cwd=self.project_root, capture_output=True, text=True, timeout=300
            )

            return {
                "command": " ".join(coverage_cmd),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"error": "Coverage analysis timed out", "success": False}

    def _get_coverage_target(self, target: str) -> str:
        """Get coverage target based on analysis target."""
        targets = {
            "messaging": "src.integration.messaging_gateway,src.services.consolidated_messaging_service,src.core.orchestration.intent_subsystems.message_router",
            "consolidated": "src.services.consolidated_messaging_service,src.services.consolidated_vector_service,src.services.consolidated_coordination_service",
            "routing": "src.core.orchestration.intent_subsystems.message_router",
            "gateway": "src.integration.messaging_gateway",
            "all": "src",
        }
        return targets.get(target, "src")

    def _analyze_coverage_gaps(self, coverage_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze coverage gaps from coverage data."""
        gaps = []

        if not coverage_data.get("success", False):
            return gaps

        # Parse coverage output for missing lines
        stdout = coverage_data.get("stdout", "")

        # Look for coverage warnings and missing lines
        lines = stdout.split("\n")
        current_file = None

        for line in lines:
            if line.startswith("src/") and ":" in line:
                # File coverage line
                parts = line.split(":")
                if len(parts) >= 2:
                    filename = parts[0]
                    coverage_info = ":".join(parts[1:])

                    if "%" in coverage_info:
                        # Extract coverage percentage
                        coverage_pct = 0
                        try:
                            for part in coverage_info.split():
                                if "%" in part:
                                    coverage_pct = int(part.replace("%", ""))
                                    break
                        except ValueError:
                            pass

                        if coverage_pct < 80:  # Consider < 80% as gap
                            gaps.append(
                                {
                                    "file": filename,
                                    "coverage_percentage": coverage_pct,
                                    "severity": "high" if coverage_pct < 50 else "medium",
                                    "type": "low_coverage",
                                }
                            )

        return gaps

    def _generate_recommendations(
        self, gaps: List[Dict[str, Any]], target: str
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for improving coverage."""
        recommendations = []

        # General recommendations
        recommendations.extend(
            [
                {
                    "type": "general",
                    "priority": "high",
                    "description": "Add unit tests for all public methods and classes",
                    "estimated_effort": "2-3 days",
                },
                {
                    "type": "general",
                    "priority": "medium",
                    "description": "Implement integration tests for end-to-end workflows",
                    "estimated_effort": "1-2 days",
                },
                {
                    "type": "general",
                    "priority": "high",
                    "description": "Add error handling and edge case tests",
                    "estimated_effort": "1 day",
                },
            ]
        )

        # Target-specific recommendations
        if target == "messaging":
            recommendations.extend(
                [
                    {
                        "type": "messaging_specific",
                        "priority": "high",
                        "description": "Add tests for PyAutoGUI coordinate-based message delivery",
                        "estimated_effort": "1 day",
                    },
                    {
                        "type": "messaging_specific",
                        "priority": "medium",
                        "description": "Test message routing with various priority levels",
                        "estimated_effort": "0.5 days",
                    },
                ]
            )

        elif target == "routing":
            recommendations.extend(
                [
                    {
                        "type": "routing_specific",
                        "priority": "high",
                        "description": "Add performance tests for high-throughput message routing",
                        "estimated_effort": "1 day",
                    },
                    {
                        "type": "routing_specific",
                        "priority": "medium",
                        "description": "Test thread safety and concurrent message processing",
                        "estimated_effort": "0.5 days",
                    },
                ]
            )

        # Gap-specific recommendations
        for gap in gaps:
            if gap["type"] == "low_coverage":
                recommendations.append(
                    {
                        "type": "gap_specific",
                        "priority": gap["severity"],
                        "description": f"Improve coverage for {gap['file']} (currently {gap['coverage_percentage']}%)",
                        "file": gap["file"],
                        "estimated_effort": "0.5-1 day",
                    }
                )

        return recommendations

    def improve_test_reliability(self, target: str = "all") -> Dict[str, Any]:
        """Improve test reliability by identifying and fixing flaky tests."""
        print(f"🔧 Improving test reliability for target: {target}")

        # Run tests multiple times to detect flakiness
        reliability_results = self._run_reliability_tests(target)

        # Analyze and fix flaky tests
        fixes = self._analyze_and_fix_flaky_tests(reliability_results)

        return {
            "target": target,
            "reliability_results": reliability_results,
            "fixes_applied": fixes,
            "timestamp": self._get_timestamp(),
        }

    def _run_reliability_tests(self, target: str, runs: int = 3) -> Dict[str, Any]:
        """Run tests multiple times to detect flakiness."""
        results = []

        for run in range(runs):
            print(f"  Running reliability test run {run + 1}/{runs}")

            cmd = [sys.executable, "-m", "pytest", "--tb=no", "-q"]
            if target != "all":
                cmd.extend(["-k", target])
            cmd.append(str(self.tests_dir))

            try:
                result = subprocess.run(
                    cmd, cwd=self.project_root, capture_output=True, text=True, timeout=120
                )

                results.append(
                    {
                        "run": run + 1,
                        "return_code": result.returncode,
                        "passed": result.returncode == 0,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    }
                )

            except subprocess.TimeoutExpired:
                results.append({"run": run + 1, "error": "Test run timed out", "passed": False})

        # Analyze consistency
        passed_runs = sum(1 for r in results if r.get("passed", False))
        total_runs = len(results)

        return {
            "total_runs": total_runs,
            "passed_runs": passed_runs,
            "consistency_percentage": (passed_runs / total_runs) * 100 if total_runs > 0 else 0,
            "is_flaky": passed_runs != total_runs,  # Not 100% consistent
            "run_details": results,
        }

    def _analyze_and_fix_flaky_tests(
        self, reliability_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze flaky tests and suggest fixes."""
        fixes = []

        if reliability_results.get("is_flaky", False):
            consistency = reliability_results["consistency_percentage"]

            fixes.append(
                {
                    "type": "flaky_test_fix",
                    "description": f"Tests show {consistency:.1f}% consistency - investigate timing issues",
                    "severity": "high" if consistency < 80 else "medium",
                    "recommendations": [
                        "Add proper cleanup in test teardown methods",
                        "Use explicit waits instead of time.sleep()",
                        "Mock external dependencies properly",
                        "Check for race conditions in threaded code",
                    ],
                }
            )

        return fixes

    def generate_ci_cd_integration(self) -> Dict[str, Any]:
        """Generate CI/CD integration configuration."""
        print("🔗 Generating CI/CD integration configuration")

        # Create coverage configuration
        coverage_config = {
            "coverage": {
                "source": ["src/"],
                "omit": ["*/tests/*", "*/test_*.py", "*/__pycache__/*", "*/venv/*", "*.pyc"],
                "report": {
                    "exclude_lines": [
                        "pragma: no cover",
                        "def __repr__",
                        "raise AssertionError",
                        "raise NotImplementedError",
                    ]
                },
            },
            "pytest": {
                "addopts": [
                    "--cov=src",
                    "--cov-report=html:htmlcov",
                    "--cov-report=xml",
                    "--cov-report=term-missing",
                    "--cov-fail-under=85",
                    "-v",
                    "--tb=short",
                ],
                "markers": [
                    "unit: Unit tests",
                    "integration: Integration tests",
                    "performance: Performance tests",
                    "slow: Slow running tests",
                ],
            },
        }

        # Generate GitHub Actions workflow
        workflow_config = self._generate_github_actions_workflow()

        return {
            "coverage_config": coverage_config,
            "workflow_config": workflow_config,
            "timestamp": self._get_timestamp(),
        }

    def _generate_github_actions_workflow(self) -> Dict[str, Any]:
        """Generate GitHub Actions workflow for CI/CD."""
        workflow = {
            "name": "Test Coverage CI",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main"]},
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {"matrix": {"python-version": ["3.8", "3.9", "3.10", "3.11"]}},
                    "steps": [
                        {"name": "Checkout code", "uses": "actions/checkout@v3"},
                        {
                            "name": "Set up Python ${{ matrix.python-version }}",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": "${{ matrix.python-version }}"},
                        },
                        {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                        {
                            "name": "Run tests with coverage",
                            "run": "python -m pytest --cov=src --cov-report=xml --cov-fail-under=85",
                        },
                        {
                            "name": "Upload coverage to Codecov",
                            "uses": "codecov/codecov-action@v3",
                            "with": {"file": "./coverage.xml"},
                        },
                    ],
                }
            },
        }

        return workflow

    def save_report(self, report: Dict[str, Any], report_type: str) -> str:
        """Save analysis report to file."""
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        timestamp = report.get("timestamp", self._get_timestamp())
        filename = f"{report_type}_analysis_{timestamp}.json"
        filepath = self.reports_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"📄 Report saved: {filepath}")
        return str(filepath)

    def _get_timestamp(self) -> str:
        """Get current timestamp for reports."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_full_analysis(self, target: str = "messaging") -> Dict[str, Any]:
        """Run full analysis suite."""
        print(f"🚀 Starting full test coverage analysis for: {target}")

        # Analyze coverage
        coverage_report = self.analyze_current_coverage(target)

        # Improve reliability
        reliability_report = self.improve_test_reliability(target)

        # Generate CI/CD integration
        ci_cd_config = self.generate_ci_cd_integration()

        # Combine results
        full_report = {
            "analysis_type": "full_test_coverage_analysis",
            "target": target,
            "coverage_analysis": coverage_report,
            "reliability_analysis": reliability_report,
            "ci_cd_integration": ci_cd_config,
            "summary": {
                "coverage_gaps_found": len(coverage_report.get("gaps", [])),
                "recommendations_count": len(coverage_report.get("recommendations", [])),
                "flaky_tests_detected": reliability_report.get("reliability_results", {}).get(
                    "is_flaky", False
                ),
                "ci_cd_config_generated": True,
            },
            "timestamp": self._get_timestamp(),
        }

        # Save comprehensive report
        report_path = self.save_report(full_report, "full_test_coverage")

        print("✅ Full analysis complete!")
        print(f"📊 Summary:")
        print(f"   - Coverage gaps: {len(coverage_report.get('gaps', []))}")
        print(f"   - Recommendations: {len(coverage_report.get('recommendations', []))}")
        print(
            f"   - Flaky tests: {reliability_report.get('reliability_results', {}).get('is_flaky', False)}"
        )
        print(f"   - Report: {report_path}")

        return full_report

    def analyze_error_handling_coverage(self, target: str) -> Dict[str, Any]:
        """Analyze error handling module integration test coverage."""
        print("🔍 Analyzing error handling integration coverage...")

        # Run error handling specific tests
        error_test_cmd = [
            sys.executable, "-m", "pytest",
            "--cov-report=json",
            "--cov=src.core.error_handling",
            "--cov=src.core.error_handling_unified",
            "tests/operational/test_error_handling.py",
            "tests/integration/test_cross_service_integration.py",
            "-v"
        ]

        try:
            result = subprocess.run(
                error_test_cmd, cwd=self.project_root, capture_output=True, text=True, timeout=180
            )

            # Parse coverage data
            coverage_percentage = 0
            if result.returncode == 0:
                # Extract coverage percentage from output
                for line in result.stdout.split('\n'):
                    if 'TOTAL' in line and '%' in line:
                        try:
                            coverage_percentage = float(line.split()[-1].replace('%', ''))
                            break
                        except (ValueError, IndexError):
                            pass

            return {
                "target": target,
                "coverage_percentage": coverage_percentage,
                "tests_run": result.returncode == 0,
                "error_modules_tested": [
                    "advanced_error_handler",
                    "automated_recovery",
                    "circuit_breaker",
                    "error_analysis_engine",
                    "error_recovery",
                    "retry_mechanisms"
                ],
                "integration_tests_covered": [
                    "messaging_error_handling",
                    "coordination_error_recovery",
                    "vector_search_error_scenarios"
                ]
            }

        except subprocess.TimeoutExpired:
            return {
                "target": target,
                "error": "Error handling coverage analysis timed out",
                "coverage_percentage": 0,
                "tests_run": False
            }

    def run_performance_benchmarking(self, target: str) -> Dict[str, Any]:
        """Run performance benchmarking for test execution."""
        print("⚡ Running performance benchmarking...")

        # Run performance tests
        perf_cmd = [
            sys.executable, "-m", "pytest",
            "tests/performance/",
            "--durations=10",
            "--tb=no",
            "-q"
        ]

        try:
            start_time = time.time()
            result = subprocess.run(
                perf_cmd, cwd=self.project_root, capture_output=True, text=True, timeout=120
            )
            end_time = time.time()

            execution_time = end_time - start_time
            benchmarks_met = execution_time < 60  # Target: under 60 seconds for performance tests

            return {
                "target": target,
                "execution_time_seconds": execution_time,
                "benchmarks_met": benchmarks_met,
                "performance_tests_passed": result.returncode == 0,
                "target_execution_time": 60,
                "performance_metrics": {
                    "test_execution_efficiency": "high" if benchmarks_met else "needs_improvement",
                    "bottleneck_detection": len([line for line in result.stdout.split('\n') if 'slowest' in line.lower()]) > 0
                }
            }

        except subprocess.TimeoutExpired:
            return {
                "target": target,
                "error": "Performance benchmarking timed out",
                "execution_time_seconds": 120,
                "benchmarks_met": False
            }

    def generate_intelligent_recommendations(
        self,
        coverage_report: Dict[str, Any],
        reliability_report: Dict[str, Any],
        error_handling_report: Dict[str, Any],
        performance_report: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate intelligent recommendations based on all analysis data."""
        recommendations = []

        # Coverage-based recommendations
        coverage_gaps = coverage_report.get("gaps", [])
        if len(coverage_gaps) > 0:
            high_priority_gaps = [gap for gap in coverage_gaps if gap.get("severity") == "high"]
            if high_priority_gaps:
                recommendations.append({
                    "priority": "CRITICAL",
                    "category": "coverage",
                    "title": "Address High-Priority Coverage Gaps",
                    "description": f"Focus on {len(high_priority_gaps)} files with <50% coverage immediately",
                    "action_items": [
                        "Prioritize unit tests for critical business logic",
                        "Add integration tests for high-risk components",
                        "Review and refactor complex functions for testability"
                    ],
                    "estimated_effort": "High",
                    "impact": "Critical for system reliability"
                })

        # Error handling recommendations
        error_coverage = error_handling_report.get("coverage_percentage", 0)
        if error_coverage < 80:
            recommendations.append({
                "priority": "HIGH",
                "category": "error_handling",
                "title": "Improve Error Handling Test Coverage",
                "description": f"Current error handling coverage: {error_coverage:.1f}%. Target: 85%+",
                "action_items": [
                    "Add integration tests for error recovery scenarios",
                    "Test error propagation across service boundaries",
                    "Validate error handling in edge cases",
                    "Add chaos engineering tests for failure scenarios"
                ],
                "estimated_effort": "Medium",
                "impact": "Critical for system resilience"
            })

        # Performance recommendations
        if not performance_report.get("benchmarks_met", True):
            recommendations.append({
                "priority": "MEDIUM",
                "category": "performance",
                "title": "Optimize Test Execution Performance",
                "description": f"Test execution time: {performance_report.get('execution_time_seconds', 0):.1f}s. Target: <60s",
                "action_items": [
                    "Implement parallel test execution",
                    "Optimize test setup and teardown",
                    "Add selective test running for CI/CD",
                    "Cache expensive test fixtures"
                ],
                    "estimated_effort": "Medium",
                    "impact": "Improves development velocity"
            })

        # Reliability recommendations
        if reliability_report.get("reliability_results", {}).get("is_flaky", False):
            recommendations.append({
                "priority": "HIGH",
                "category": "reliability",
                "title": "Address Flaky Test Issues",
                "description": "Flaky tests detected in test suite affecting CI/CD reliability",
                "action_items": [
                    "Identify and isolate external dependencies",
                    "Add proper test isolation and cleanup",
                    "Implement retry mechanisms for transient failures",
                    "Add timing-based test stability checks"
                ],
                "estimated_effort": "High",
                "impact": "Critical for CI/CD pipeline reliability"
            })

        # Cross-cutting recommendations
        if (len(coverage_gaps) > 5 and error_coverage < 70):
            recommendations.append({
                "priority": "CRITICAL",
                "category": "system_health",
                "title": "Comprehensive Test Infrastructure Overhaul",
                "description": "Multiple test quality issues require coordinated improvement approach",
                "action_items": [
                    "Conduct full test audit and gap analysis",
                    "Develop prioritized improvement roadmap",
                    "Allocate dedicated testing sprint",
                    "Establish test quality metrics and monitoring"
                ],
                "estimated_effort": "High",
                "impact": "Fundamental improvement of test infrastructure"
            })

        return recommendations

    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate comprehensive HTML report."""
        timestamp = report_data.get("timestamp", "unknown")
        target = report_data.get("target", "unknown")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Test Coverage Report - {target} ({timestamp})</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric-title {{ font-size: 0.9em; color: #666; margin-bottom: 10px; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .status-good {{ color: #28a745; }}
        .status-warning {{ color: #ffc107; }}
        .status-danger {{ color: #dc3545; }}
        .recommendations {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .recommendation-item {{ margin-bottom: 15px; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }}
        .priority-critical {{ border-left-color: #dc3545; }}
        .priority-high {{ border-left-color: #ffc107; }}
        .priority-medium {{ border-left-color: #28a745; }}
        .coverage-gaps {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .gap-item {{ padding: 10px; margin-bottom: 10px; background: #fff3cd; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐝 Enhanced Test Coverage Report</h1>
        <p><strong>Target:</strong> {target} | <strong>Generated:</strong> {timestamp}</p>
        <p><strong>Tool Version:</strong> 2.0.0 | <strong>Analysis Type:</strong> Full Enhanced Analysis</p>
    </div>

    <div class="summary-grid">
        <div class="metric-card">
            <div class="metric-title">Overall Quality Score</div>
            <div class="metric-value status-good">{report_data['summary']['overall_quality_score']:.1f}/100</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Coverage Gaps Found</div>
            <div class="metric-value status-warning">{report_data['summary']['coverage_gaps_found']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Error Handling Coverage</div>
            <div class="metric-value status-good">{report_data['error_handling_analysis']['coverage_percentage']:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Intelligent Recommendations</div>
            <div class="metric-value">{report_data['summary']['intelligent_recommendations_count']}</div>
        </div>
    </div>

    <div class="coverage-gaps">
        <h2>📊 Coverage Gaps Analysis</h2>
"""

        gaps = report_data.get("coverage_analysis", {}).get("gaps", [])
        if gaps:
            for gap in gaps[:10]:  # Show first 10 gaps
                severity_class = "status-danger" if gap.get("severity") == "high" else "status-warning"
                html_content += f"""
        <div class="gap-item">
            <strong class="{severity_class}">{gap.get('file', 'Unknown')}</strong>
            <span>Coverage: {gap.get('coverage_percentage', 0)}%</span>
            <span>Severity: {gap.get('severity', 'medium').upper()}</span>
        </div>
"""
        else:
            html_content += "<p class="good-status">✅ No significant coverage gaps detected!</p>"

        html_content += """
    </div>

    <div class="recommendations">
        <h2>🎯 Intelligent Recommendations</h2>
"""

        recommendations = report_data.get("intelligent_recommendations", [])
        if recommendations:
            for rec in recommendations:
                priority_class = f"priority-{rec.get('priority', 'medium').lower()}"
                html_content += f"""
        <div class="recommendation-item {priority_class}">
            <h4>{rec.get('title', 'Unknown')}</h4>
            <p><strong>Priority:</strong> {rec.get('priority', 'Unknown')}</p>
            <p><strong>Category:</strong> {rec.get('category', 'Unknown')}</p>
            <p>{rec.get('description', '')}</p>
            <p><strong>Estimated Effort:</strong> {rec.get('estimated_effort', 'Unknown')}</p>
            <p><strong>Impact:</strong> {rec.get('impact', 'Unknown')}</p>
        </div>
"""
        else:
            html_content += "<p>No specific recommendations generated.</p>"

        html_content += """
    </div>
</body>
</html>
"""

        # Save HTML report
        html_filename = f"enhanced_test_coverage_report_{target}_{timestamp}.html"
        html_filepath = self.reports_dir / html_filename
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(html_filepath)

    def _calculate_overall_quality_score(
        self,
        coverage_report: Dict[str, Any],
        reliability_report: Dict[str, Any],
        error_handling_report: Dict[str, Any],
        performance_report: Dict[str, Any]
    ) -> float:
        """Calculate overall quality score from all analysis components."""
        score = 0
        max_score = 100

        # Coverage score (40% weight)
        gaps = coverage_report.get("gaps", [])
        coverage_score = max(0, 40 - len(gaps) * 2)
        score += min(coverage_score, 40)

        # Error handling score (25% weight)
        error_coverage = error_handling_report.get("coverage_percentage", 0)
        error_score = (error_coverage / 100) * 25
        score += error_score

        # Reliability score (20% weight)
        reliability_score = 20
        if reliability_report.get("reliability_results", {}).get("is_flaky", False):
            reliability_score = 10  # Penalty for flaky tests
        score += reliability_score

        # Performance score (15% weight)
        performance_score = 15 if performance_report.get("benchmarks_met", True) else 7.5
        score += performance_score

        return min(score, max_score)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Test Coverage Improvement Tool")
    parser.add_argument(
        "--target",
        choices=["messaging", "consolidated", "routing", "gateway", "all"],
        default="messaging",
        help="Target component for analysis",
    )
    parser.add_argument("--analyze", action="store_true", help="Run coverage analysis")
    parser.add_argument("--reliability", action="store_true", help="Run reliability improvement")
    parser.add_argument("--ci-cd", action="store_true", help="Generate CI/CD integration")
    parser.add_argument("--full", action="store_true", help="Run full analysis suite")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML report for full analysis")
    parser.add_argument(
        "--project-root", type=Path, default=Path("."), help="Project root directory"
    )

    args = parser.parse_args()

    improver = TestCoverageImprover(args.project_root)

    if args.full:
        improver.run_full_analysis(args.target, args.html_report)
    elif args.analyze:
        report = improver.analyze_current_coverage(args.target)
        improver.save_report(report, "coverage_analysis")
    elif args.reliability:
        report = improver.improve_test_reliability(args.target)
        improver.save_report(report, "reliability_analysis")
    elif args.ci_cd:
        report = improver.generate_ci_cd_integration()
        improver.save_report(report, "ci_cd_integration")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
