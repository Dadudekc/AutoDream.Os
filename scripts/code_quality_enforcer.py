#!/usr/bin/env python3
"""
Code Quality Enforcer - V2 Compliance System.

Enforces comprehensive code quality standards across the repository.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class CodeQualityEnforcer:
    """Comprehensive code quality enforcement system for V2 compliance."""
    def __init__(self):
        """Initialize the code quality enforcer with tools and thresholds."""
        self.quality_tools = {
            "black": "black --check --diff",
            "isort": "isort --check-only --diff",
            "flake8": "flake8",
            "pylint": "pylint",
            "mypy": "mypy",
            "bandit": "bandit -r . -f json",
            "safety": "safety check --json",
        }

        self.quality_thresholds = {
            "black": 100.0,  # Must pass completely
            "isort": 100.0,  # Must pass completely
            "flake8": 95.0,  # 95% compliance required
            "pylint": 8.0,  # Score 8.0+ required
            "mypy": 90.0,  # 90% type coverage required
            "bandit": 0,  # No security issues allowed
            "safety": 0,  # No vulnerabilities allowed
        }

        self.exclude_patterns = [
            "*/__pycache__/*",
            "*/venv/*",
            "*/.venv/*",
            "*/build/*",
            "*/dist/*",
            "*/.git/*",
            "*/node_modules/*",
            "*.pyc",
            "*.pyo",
            "*.pyd",
        ]

    def run_quality_check(self, tool: str, args: str = "") -> Dict[str, Any]:
        """Run a specific quality check tool."""
        try:
            command = f"{self.quality_tools[tool]} {args}".strip()
            result = subprocess.run(
                command.split(), capture_output=True, text=True, cwd=Path.cwd()
            )

            return {
                "tool": tool,
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "tool": tool,
                "command": command,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def run_all_quality_checks(self) -> Dict[str, Any]:
        """Run all quality checks and generate comprehensive report."""
        print("🚀 Starting comprehensive code quality checks...")

        start_time = datetime.now()
        results = {}
        overall_score = 0.0
        total_tools = len(self.quality_tools)

        for tool in self.quality_tools:
            print(f"🔍 Running {tool}...")
            result = self.run_quality_check(tool)
            results[tool] = result

            # Calculate score for this tool
            if result["success"]:
                tool_score = 100.0
            else:
                tool_score = self._calculate_partial_score(tool, result)

            overall_score += tool_score
            status = '✅ PASS' if result['success'] else '❌ FAIL'
            print(f"   {tool}: {status} ({tool_score:.1f}%)")

        overall_score /= total_tools

        # Generate comprehensive report
        report = {
            "timestamp": start_time.isoformat(),
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
            "overall_score": overall_score,
            "compliance_level": self._get_compliance_level(overall_score),
            "tools_checked": total_tools,
            "tools_passed": sum(
                1 for r in results.values() if r["success"]
            ),
            "tools_failed": sum(
                1 for r in results.values() if not r["success"]
            ),
            "detailed_results": results,
            "recommendations": self._generate_recommendations(
                results, overall_score
            ),
            "next_actions": self._generate_next_actions(
                results, overall_score
            ),
        }

        return report

    def _calculate_partial_score(self, tool: str, result: Dict[str, Any]) -> float:
        """Calculate partial score for failed tools based on output analysis."""
        if tool == "black":
            # Count lines that need formatting
            lines_to_format = len([
                line for line in result["stdout"].split("\n") if line.strip()
            ])
            return max(0, 100 - (lines_to_format * 2))

        elif tool == "flake8":
            # Count linting errors
            error_lines = [
                line for line in result["stderr"].split("\n") if ":" in line
            ]
            return max(0, 100 - (len(error_lines) * 5))

        elif tool == "pylint":
            # Extract score from output
            try:
                search_text = "Your code has been rated at"
                score_match = [
                    line
                    for line in result["stdout"].split("\n")
                    if search_text in line
                ]
                if score_match:
                    score_text = score_match[0]
                    score = float(score_text.split()[-2])
                    return min(100, score * 10)
            except Exception:
                pass
            return 50.0

        elif tool == "mypy":
            # Count type errors
            error_lines = [
                line for line in result["stderr"].split("\n") 
                if "error:" in line
            ]
            return max(0, 100 - (len(error_lines) * 3))

        else:
            return 50.0

    def _get_compliance_level(self, score: float) -> str:
        """Determine compliance level based on overall score."""
        if score >= 95.0:
            return "V2 COMPLIANT - EXCELLENT"
        elif score >= 90.0:
            return "V2 COMPLIANT - GOOD"
        elif score >= 80.0:
            return "V2 COMPLIANT - ACCEPTABLE"
        elif score >= 70.0:
            return "V2 COMPLIANT - NEEDS IMPROVEMENT"
        else:
            return "V2 NON-COMPLIANT - CRITICAL ISSUES"

    def _generate_recommendations(
        self, results: Dict[str, Any], overall_score: float
    ) -> List[str]:
        """Generate actionable recommendations based on results."""
        recommendations = []

        if overall_score < 95.0:
            msg = ("IMMEDIATE: Address all critical quality issues "
                   "to achieve V2 compliance")
            recommendations.append(msg)

        for tool, result in results.items():
            if not result["success"]:
                if tool == "black":
                    recommendations.append(
                        "FORMATTING: Run 'black .' to fix code formatting issues"
                    )
                elif tool == "isort":
                    recommendations.append(
                        "IMPORTS: Run 'isort .' to fix import sorting issues"
                    )
                elif tool == "flake8":
                    recommendations.append(
                        "LINTING: Fix flake8 violations to improve code quality"
                    )
                elif tool == "pylint":
                    recommendations.append(
                        "ANALYSIS: Address pylint warnings to improve code structure"
                    )
                elif tool == "mypy":
                    recommendations.append(
                        "TYPES: Add type hints to improve code reliability"
                    )
                elif tool == "bandit":
                    recommendations.append(
                        "SECURITY: Address security issues identified by bandit"
                    )
                elif tool == "safety":
                    msg = ("DEPENDENCIES: Update vulnerable dependencies "
                   "identified by safety")
                    recommendations.append(msg)

        if not recommendations:
            msg = ("MAINTENANCE: Schedule regular quality checks "
                   "to maintain V2 compliance")
            recommendations.append(msg)
            msg = ("OPTIMIZATION: Consider implementing additional quality tools "
                   "for enhanced compliance")
            recommendations.append(msg)

        return recommendations

    def _generate_next_actions(
        self, results: Dict[str, Any], overall_score: float
    ) -> List[str]:
        """Generate next actions based on quality check results."""
        actions = []

        if overall_score < 95.0:
            msg = ("URGENT: Fix all quality issues "
                   "to achieve V2 compliance")
            actions.append(msg)
            msg = ("PRIORITY: Address critical failures first")
            actions.append(msg)

        # Tool-specific actions
        for tool, result in results.items():
            if not result["success"]:
                if tool in ["black", "isort"]:
                    actions.append(f"Run '{tool} .' to automatically fix {tool} issues")
                elif tool == "flake8":
                    msg = "Review and fix flake8 violations manually"
                    actions.append(msg)
                elif tool == "pylint":
                    msg = "Address pylint warnings to improve code quality"
                    actions.append(msg)
                elif tool == "mypy":
                    msg = "Add type hints to resolve mypy errors"
                    actions.append(msg)
                elif tool in ["bandit", "safety"]:
                    actions.append(f"Investigate and resolve {tool} security issues")

        if overall_score >= 95.0:
            msg = "Maintain current quality standards"
            actions.append(msg)
            msg = "Schedule regular quality audits"
            actions.append(msg)
            msg = "Consider implementing additional quality tools"
            actions.append(msg)

        return actions

    def save_report(
        self, report: Dict[str, Any], output_file: Optional[Path] = None
    ) -> None:
        """Save quality report to file."""
        if output_file is None:
            output_file = Path("reports/code_quality_report.json")

        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📊 Quality report saved to: {output_file}")

    def print_summary(self, report: Dict[str, Any]) -> None:
        """Print a formatted summary of the quality check results."""
        print("\n" + "=" * 80)
        print("🚀 CODE QUALITY CHECK SUMMARY - V2 COMPLIANCE")
        print("=" * 80)

        print(f"📅 Timestamp: {report['timestamp']}")
        print(f"⏱️  Duration: {report['duration_seconds']:.2f} seconds")
        print(f"🎯 Overall Score: {report['overall_score']:.1f}%")
        print(f"🏆 Compliance Level: {report['compliance_level']}")
        print(f"🔧 Tools Checked: {report['tools_checked']}")
        print(f"✅ Tools Passed: {report['tools_passed']}")
        print(f"❌ Tools Failed: {report['tools_failed']}")

        print("\n📋 DETAILED RESULTS:")
        print("-" * 40)

        for tool, result in report["detailed_results"].items():
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{tool:12} : {status}")

        print("\n💡 RECOMMENDATIONS:")
        print("-" * 40)
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"{i:2}. {rec}")

        print("\n🎯 NEXT ACTIONS:")
        print("-" * 40)
        for i, action in enumerate(report["next_actions"], 1):
            print(f"{i:2}. {action}")

        print("\n" + "=" * 80)

        if report["overall_score"] >= 95.0:
            print("🎉 CONGRATULATIONS! V2 COMPLIANCE ACHIEVED! 🎉")
        else:
            print("⚠️  V2 COMPLIANCE NOT YET ACHIEVED - ACTION REQUIRED ⚠️")

        print("=" * 80)


def main():
    """Main entry point for code quality enforcer."""
    parser = argparse.ArgumentParser(
        description="Code Quality Enforcer - V2 Compliance System"
    )
    parser.add_argument("--tool", help="Run specific quality tool only")
    parser.add_argument("--output", help="Output file for quality report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="Automatically fix issues where possible"
    )

    args = parser.parse_args()

    enforcer = CodeQualityEnforcer()

    if args.tool:
        # Run specific tool only
        if args.tool in enforcer.quality_tools:
            result = enforcer.run_quality_check(args.tool)
            print(f"Tool: {args.tool}")
            print(f"Success: {result['success']}")
            if args.verbose:
                print(f"Output: {result['stdout']}")
                if result["stderr"]:
                    print(f"Errors: {result['stderr']}")
        else:
            print(f"Unknown tool: {args.tool}")
            print(f"Available tools: {', '.join(enforcer.quality_tools.keys())}")
            sys.exit(1)
    else:
        # Run all quality checks
        report = enforcer.run_all_quality_checks()

        # Save report
        output_file = Path(args.output) if args.output else None
        enforcer.save_report(report, output_file)

        # Print summary
        enforcer.print_summary(report)

        # Exit with appropriate code
        if report["overall_score"] >= 95.0:
            print("✅ Quality check passed - V2 compliance achieved")
            sys.exit(0)
        else:
            print("❌ Quality check failed - V2 compliance not achieved")
            sys.exit(1)


if __name__ == "__main__":
    main()
