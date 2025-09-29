#!/usr/bin/env python3
"""
Dependency Scanner - Comprehensive Dependency Vulnerability Analysis
===================================================================

Advanced dependency scanning tool that checks for known vulnerabilities
in Python dependencies and provides remediation recommendations.

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


class DependencyScanner:
    """Comprehensive dependency vulnerability scanner."""

    def __init__(self, project_root: str = "."):
        """Initialize dependency scanner."""
        self.project_root = Path(project_root).resolve()
        self.results: dict[str, Any] = {}
        self.vulnerability_databases = ["safety", "pip-audit", "osv-scanner"]

    def run_comprehensive_scan(self) -> dict[str, Any]:
        """Run comprehensive dependency vulnerability scan."""
        logger.info("🔍 Starting comprehensive dependency vulnerability scan...")

        scan_results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "tools": {},
            "summary": {},
        }

        # Run individual dependency scanning tools
        scan_results["tools"]["safety"] = self._run_safety_scan()
        scan_results["tools"]["pip_audit"] = self._run_pip_audit_scan()
        scan_results["tools"]["osv_scanner"] = self._run_osv_scanner()
        scan_results["tools"]["manual_check"] = self._run_manual_dependency_check()

        # Generate summary
        scan_results["summary"] = self._generate_dependency_summary(scan_results["tools"])

        self.results = scan_results
        return scan_results

    def _run_safety_scan(self) -> dict[str, Any]:
        """Run Safety dependency vulnerability scanner."""
        logger.info("🔍 Running Safety scan...")

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

    def _run_pip_audit_scan(self) -> dict[str, Any]:
        """Run pip-audit vulnerability scanner."""
        logger.info("🔍 Running pip-audit scan...")

        try:
            # Check if pip-audit is available
            subprocess.run(["pip-audit", "--version"], capture_output=True, check=True)

            cmd = ["pip-audit", "--format=json", "--desc"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            pip_audit_data = []
            if result.stdout:
                try:
                    pip_audit_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pip_audit_data = [{"raw_output": result.stdout}]

            return {"status": "success", "data": pip_audit_data, "command": " ".join(cmd)}

        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("pip-audit not available, skipping...")
            return {"status": "skipped", "reason": "pip-audit not installed", "data": []}
        except Exception as e:
            logger.error(f"pip-audit scan failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _run_osv_scanner(self) -> dict[str, Any]:
        """Run OSV (Open Source Vulnerabilities) scanner."""
        logger.info("🔍 Running OSV scanner...")

        try:
            # Check if osv-scanner is available
            subprocess.run(["osv-scanner", "--version"], capture_output=True, check=True)

            cmd = ["osv-scanner", "--json", str(self.project_root)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            osv_data = []
            if result.stdout:
                try:
                    osv_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    osv_data = [{"raw_output": result.stdout}]

            return {"status": "success", "data": osv_data, "command": " ".join(cmd)}

        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("osv-scanner not available, skipping...")
            return {"status": "skipped", "reason": "osv-scanner not installed", "data": []}
        except Exception as e:
            logger.error(f"OSV scanner failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _run_manual_dependency_check(self) -> dict[str, Any]:
        """Run manual dependency check against known vulnerable packages."""
        logger.info("🔍 Running manual dependency check...")

        try:
            # Find all requirements files
            requirements_files = list(self.project_root.glob("requirements*.txt"))
            requirements_files.extend(list(self.project_root.glob("pyproject.toml")))

            if not requirements_files:
                return {"status": "skipped", "reason": "No requirements files found", "data": []}

            vulnerabilities = []
            for req_file in requirements_files:
                file_vulns = self._check_file_vulnerabilities(req_file)
                vulnerabilities.extend(file_vulns)

            return {"status": "success", "data": vulnerabilities, "command": "manual_check"}

        except Exception as e:
            logger.error(f"Manual dependency check failed: {e}")
            return {"status": "error", "error": str(e), "data": []}

    def _check_file_vulnerabilities(self, file_path: Path) -> list[dict[str, Any]]:
        """Check a single requirements file for vulnerabilities."""
        vulnerabilities = []

        try:
            with open(file_path) as f:
                content = f.read()

            # Known vulnerable packages with minimum safe versions
            vulnerable_packages = {
                "django": {"min_version": "2.2.0", "severity": "HIGH"},
                "flask": {"min_version": "1.1.0", "severity": "MEDIUM"},
                "requests": {"min_version": "2.25.0", "severity": "HIGH"},
                "urllib3": {"min_version": "1.26.0", "severity": "HIGH"},
                "jinja2": {"min_version": "2.11.0", "severity": "MEDIUM"},
                "pyyaml": {"min_version": "5.4.0", "severity": "HIGH"},
                "cryptography": {"min_version": "3.4.0", "severity": "HIGH"},
                "pillow": {"min_version": "8.2.0", "severity": "MEDIUM"},
                "numpy": {"min_version": "1.21.0", "severity": "MEDIUM"},
                "pandas": {"min_version": "1.3.0", "severity": "MEDIUM"},
            }

            for line in content.split("\n"):
                line = line.strip()
                if line and not line.startswith("#"):
                    for package, info in vulnerable_packages.items():
                        if package.lower() in line.lower():
                            vulnerabilities.append(
                                {
                                    "file": str(file_path),
                                    "package": package,
                                    "line": line,
                                    "severity": info["severity"],
                                    "min_safe_version": info["min_version"],
                                    "issue": f"Potentially vulnerable version of {package}",
                                    "recommendation": f'Upgrade {package} to >= {info["min_version"]}',
                                }
                            )

        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")

        return vulnerabilities

    def _generate_dependency_summary(self, tools_results: dict[str, Any]) -> dict[str, Any]:
        """Generate dependency vulnerability summary."""
        summary = {
            "total_vulnerabilities": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "packages_checked": 0,
            "tools_status": {},
            "recommendations": [],
        }

        # Analyze each tool's results
        for tool_name, tool_result in tools_results.items():
            summary["tools_status"][tool_name] = tool_result["status"]

            if tool_result["status"] == "success":
                data = tool_result["data"]

                if tool_name == "safety":
                    summary["total_vulnerabilities"] += len(data)
                    summary["high_severity"] += len(
                        data
                    )  # Safety issues are typically high severity

                elif tool_name == "pip_audit":
                    for vuln in data:
                        summary["total_vulnerabilities"] += 1
                        severity = vuln.get("severity", "MEDIUM").upper()
                        summary[f"{severity.lower()}_severity"] += 1

                elif tool_name == "osv_scanner":
                    for vuln in data:
                        summary["total_vulnerabilities"] += 1
                        severity = vuln.get("severity", "MEDIUM").upper()
                        summary[f"{severity.lower()}_severity"] += 1

                elif tool_name == "manual_check":
                    for vuln in data:
                        summary["total_vulnerabilities"] += 1
                        severity = vuln.get("severity", "MEDIUM").upper()
                        summary[f"{severity.lower()}_severity"] += 1

        # Generate recommendations
        if summary["high_severity"] > 0:
            summary["recommendations"].append(
                "🚨 CRITICAL: Address high-severity vulnerabilities immediately"
            )

        if summary["medium_severity"] > 5:
            summary["recommendations"].append(
                "⚠️  WARNING: Multiple medium-severity vulnerabilities detected"
            )

        if summary["total_vulnerabilities"] == 0:
            summary["recommendations"].append("✅ No known vulnerabilities detected")
        else:
            summary["recommendations"].append("📋 RECOMMENDATION: Update vulnerable dependencies")

        return summary

    def generate_remediation_report(self) -> str:
        """Generate remediation report with specific upgrade commands."""
        if not self.results:
            self.run_comprehensive_scan()

        report_content = "# Dependency Vulnerability Remediation Report\n\n"
        report_content += f"**Generated:** {self.results['timestamp']}\n"
        report_content += f"**Project:** {self.results['project_root']}\n\n"

        summary = self.results["summary"]
        report_content += "## Summary\n"
        report_content += f"- **Total Vulnerabilities:** {summary['total_vulnerabilities']}\n"
        report_content += f"- **High Severity:** {summary['high_severity']}\n"
        report_content += f"- **Medium Severity:** {summary['medium_severity']}\n"
        report_content += f"- **Low Severity:** {summary['low_severity']}\n\n"

        # Add remediation commands
        report_content += "## Remediation Commands\n\n"
        report_content += "```bash\n"

        # Generate pip install commands for upgrades
        upgrade_commands = set()
        for tool_name, tool_result in self.results["tools"].items():
            if tool_result["status"] == "success":
                for vuln in tool_result["data"]:
                    if "recommendation" in vuln:
                        upgrade_commands.add(vuln["recommendation"])

        for cmd in sorted(upgrade_commands):
            report_content += f"# {cmd}\n"

        report_content += "```\n\n"

        # Add recommendations
        if summary["recommendations"]:
            report_content += "## Recommendations\n\n"
            for rec in summary["recommendations"]:
                report_content += f"- {rec}\n"

        return report_content

    def generate_report(self, output_file: str | None = None) -> str:
        """Generate dependency vulnerability report."""
        if not self.results:
            self.run_comprehensive_scan()

        report_file = output_file or self.project_root / "dependency_vulnerability_report.json"

        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"📄 Dependency vulnerability report generated: {report_file}")
        return str(report_file)


def main():
    """Main entry point for dependency scanner."""
    parser = argparse.ArgumentParser(description="Comprehensive Dependency Vulnerability Scanner")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output file for vulnerability report")
    parser.add_argument("--remediation", action="store_true", help="Generate remediation report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    scanner = DependencyScanner(args.project_root)
    results = scanner.run_comprehensive_scan()

    # Print summary
    summary = results["summary"]
    print("\n🔍 Dependency Vulnerability Scan Summary:")
    print(f"Total Vulnerabilities: {summary['total_vulnerabilities']}")
    print(f"High Severity: {summary['high_severity']}")
    print(f"Medium Severity: {summary['medium_severity']}")
    print(f"Low Severity: {summary['low_severity']}")

    if summary["recommendations"]:
        print("\n📋 Recommendations:")
        for rec in summary["recommendations"]:
            print(f"  {rec}")

    # Generate reports
    report_file = scanner.generate_report(args.output)
    print(f"\n📄 Detailed report saved to: {report_file}")

    if args.remediation:
        remediation_report = scanner.generate_remediation_report()
        remediation_file = Path(args.output or "dependency_remediation_report.md")
        with open(remediation_file, "w") as f:
            f.write(remediation_report)
        print(f"📄 Remediation report saved to: {remediation_file}")

    return 0 if summary["high_severity"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
