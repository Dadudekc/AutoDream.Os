#!/usr/bin/env python3
"""
Security Scanner - Comprehensive Security Analysis Tool
======================================================

Advanced security scanning tool that combines multiple security analysis tools
to provide comprehensive vulnerability detection and security assessment.

Author: Agent-2 (Security & Quality Specialist)
License: MIT
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class SecurityScanner:
    """Comprehensive security scanner for Python projects."""

    def __init__(self, project_root: str = "."):
        """Initialize security scanner."""
        self.project_root = Path(project_root).resolve()
        self.results: dict[str, Any] = {}
        self.severity_levels = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "INFO": 0}

    def run_comprehensive_scan(self) -> dict[str, Any]:
        """Run comprehensive security scan using multiple tools."""
        logger.info("🔒 Starting comprehensive security scan...")

        scan_results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "tools": {},
        }

        # Run individual security tools
        scan_results["tools"]["bandit"] = self._run_bandit_scan()
        scan_results["tools"]["safety"] = self._run_safety_scan()
        scan_results["tools"]["semgrep"] = self._run_semgrep_scan()
        scan_results["tools"]["dependency_check"] = self._run_dependency_check()

        # Generate summary
        scan_results["summary"] = self._generate_security_summary(scan_results["tools"])

        self.results = scan_results
        return scan_results

    def _run_bandit_scan(self) -> dict[str, Any]:
        """Run Bandit security linter."""
        logger.info("🔍 Running Bandit security scan...")

        try:
            cmd = [
                "bandit",
                "-r",
                str(self.project_root / "src"),
                "-f",
                "json",
                "-ll",
                "--skip",
                "B101,B601",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            if result.returncode == 0:
                bandit_data = json.loads(result.stdout) if result.stdout else {"results": []}
            else:
                bandit_data = {"results": [], "error": result.stderr}

            return {
                "status": "success" if result.returncode == 0 else "warning",
                "data": bandit_data,
                "command": " ".join(cmd),
            }

        except Exception as e:
            logger.error(f"Bandit scan failed: {e}")
            return {"status": "error", "error": str(e), "data": {"results": []}}

    def _run_safety_scan(self) -> dict[str, Any]:
        """Run Safety dependency vulnerability scanner."""
        logger.info("🔍 Running Safety dependency scan...")

        try:
            cmd = ["safety", "check", "--json", "--short-report"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            safety_data = []
            if result.stdout:
                try:
                    safety_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Safety might return non-JSON output
                    safety_data = [{"raw_output": result.stdout}]

            return {"status": "success", "data": safety_data, "command": " ".join(cmd)}

        except Exception as e:
            logger.error(f"Safety scan failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _run_semgrep_scan(self) -> dict[str, Any]:
        """Run Semgrep static analysis (if available)."""
        logger.info("🔍 Running Semgrep static analysis...")

        try:
            # Check if semgrep is available
            subprocess.run(["semgrep", "--version"], capture_output=True, check=True)

            cmd = [
                "semgrep",
                "--config=auto",
                "--json",
                "--exclude-rule",
                "python.lang.security.audit.weak-cryptographic-key.weak-cryptographic-key",
                str(self.project_root / "src"),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            semgrep_data = []
            if result.stdout:
                try:
                    semgrep_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    semgrep_data = [{"raw_output": result.stdout}]

            return {"status": "success", "data": semgrep_data, "command": " ".join(cmd)}

        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Semgrep not available, skipping...")
            return {"status": "skipped", "reason": "Semgrep not installed", "data": []}
        except Exception as e:
            logger.error(f"Semgrep scan failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _run_dependency_check(self) -> dict[str, Any]:
        """Run dependency vulnerability check."""
        logger.info("🔍 Running dependency vulnerability check...")

        try:
            # Check requirements.txt for known vulnerable packages
            requirements_file = self.project_root / "requirements.txt"
            if not requirements_file.exists():
                return {"status": "skipped", "reason": "No requirements.txt found", "data": []}

            # Read requirements and check for common vulnerable packages
            with open(requirements_file) as f:
                requirements = f.read()

            vulnerable_packages = self._check_vulnerable_packages(requirements)

            return {"status": "success", "data": vulnerable_packages, "command": "manual_check"}

        except Exception as e:
            logger.error(f"Dependency check failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _check_vulnerable_packages(self, requirements: str) -> list[dict[str, str]]:
        """Check for known vulnerable packages in requirements."""
        # Common vulnerable packages (this should be updated regularly)
        vulnerable_packages = {
            "django": "<2.2.0",
            "flask": "<1.1.0",
            "requests": "<2.25.0",
            "urllib3": "<1.26.0",
            "jinja2": "<2.11.0",
            "pyyaml": "<5.4.0",
        }

        issues = []
        for line in requirements.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                for package, min_version in vulnerable_packages.items():
                    if package in line.lower():
                        issues.append(
                            {
                                "package": package,
                                "issue": f"Potentially vulnerable version (min: {min_version})",
                                "severity": "MEDIUM",
                            }
                        )

        return issues

    def _generate_security_summary(self, tools_results: dict[str, Any]) -> dict[str, Any]:
        """Generate security summary from all tool results."""
        summary = {
            "total_issues": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "info_issues": 0,
            "tools_status": {},
            "recommendations": [],
        }

        # Analyze each tool's results
        for tool_name, tool_result in tools_results.items():
            summary["tools_status"][tool_name] = tool_result["status"]

            if tool_name == "bandit" and tool_result["status"] == "success":
                bandit_data = tool_result["data"]
                if "results" in bandit_data:
                    for issue in bandit_data["results"]:
                        summary["total_issues"] += 1
                        severity = issue.get("issue_severity", "INFO").upper()
                        summary[f"{severity.lower()}_severity"] += 1

            elif tool_name == "safety" and tool_result["status"] == "success":
                safety_data = tool_result["data"]
                for issue in safety_data:
                    summary["total_issues"] += 1
                    summary["high_severity"] += 1  # Safety issues are typically high severity

            elif tool_name == "semgrep" and tool_result["status"] == "success":
                semgrep_data = tool_result["data"]
                for issue in semgrep_data:
                    summary["total_issues"] += 1
                    severity = issue.get("extra", {}).get("severity", "INFO").upper()
                    summary[f"{severity.lower()}_severity"] += 1

        # Generate recommendations
        if summary["high_severity"] > 0:
            summary["recommendations"].append(
                "🚨 CRITICAL: Address high-severity security issues immediately"
            )

        if summary["medium_severity"] > 5:
            summary["recommendations"].append(
                "⚠️  WARNING: Multiple medium-severity issues detected"
            )

        if summary["total_issues"] == 0:
            summary["recommendations"].append("✅ No security issues detected")

        return summary

    def generate_report(self, output_file: str | None = None) -> str:
        """Generate security report."""
        if not self.results:
            self.run_comprehensive_scan()

        report_file = output_file or self.project_root / "security_report.json"

        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"📄 Security report generated: {report_file}")
        return str(report_file)


def main():
    """Main entry point for security scanner."""
    parser = argparse.ArgumentParser(description="Comprehensive Security Scanner")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output file for security report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    scanner = SecurityScanner(args.project_root)
    results = scanner.run_comprehensive_scan()

    # Print summary
    summary = results["summary"]
    print("\n🔒 Security Scan Summary:")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"High Severity: {summary['high_severity']}")
    print(f"Medium Severity: {summary['medium_severity']}")
    print(f"Low Severity: {summary['low_severity']}")

    if summary["recommendations"]:
        print("\n📋 Recommendations:")
        for rec in summary["recommendations"]:
            print(f"  {rec}")

    # Generate report
    report_file = scanner.generate_report(args.output)
    print(f"\n📄 Detailed report saved to: {report_file}")

    return 0 if summary["high_severity"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
