#!/usr/bin/env python3
"""
Security Integration Script
===========================

Automated security integration for CI/CD pipelines.
Runs comprehensive security checks and generates reports.

V2 Compliance: ≤400 lines, single responsibility
Author: Security Implementation Team
License: MIT
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.security.security_manager import SecurityManager
from core.validation.enhanced_security_validator import EnhancedSecurityValidator


class SecurityIntegration:
    """Security integration for CI/CD pipelines."""

    def __init__(self, project_path: str = ".", output_dir: str = "security_reports"):
        """Initialize security integration."""
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize security tools
        self.security_manager = SecurityManager()
        self.security_validator = EnhancedSecurityValidator()

        # Results storage
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "checks": {},
        }

    def run_static_analysis(self) -> dict[str, Any]:
        """Run static code analysis."""
        print("🔍 Running static code analysis...")

        try:
            result = self.security_validator.validate()

            # Generate report
            report_file = self.output_dir / "static_analysis_report.json"
            with open(report_file, "w") as f:
                json.dump(result, f, indent=2)

            check_result = {
                "status": result["status"],
                "total_files": result["results"]["total_files_scanned"],
                "total_findings": result["results"]["total_findings"],
                "real_violations": result["results"]["real_violations"],
                "false_positives": result["results"]["false_positives"],
                "report_file": str(report_file),
            }

            print(
                f"✅ Static analysis completed: {result['results']['real_violations']} real violations"
            )
            return check_result

        except Exception as e:
            print(f"❌ Static analysis failed: {e}")
            return {"status": "ERROR", "error": str(e)}

    def run_dependency_scan(self) -> dict[str, Any]:
        """Run dependency security scan using safety."""
        print("📦 Running dependency security scan...")

        try:
            import subprocess

            result = subprocess.run(
                ["safety", "check", "--json"], capture_output=True, text=True, timeout=60
            )

            # Generate report
            report_file = self.output_dir / "dependency_scan_report.json"
            with open(report_file, "w") as f:
                f.write(result.stdout)

            # Parse safety output
            if result.returncode == 0:
                vulnerabilities = 0
                status = "PASSED"
            else:
                try:
                    safety_data = json.loads(result.stdout)
                    vulnerabilities = len(safety_data.get("vulnerabilities", []))
                    status = "FAILED" if vulnerabilities > 0 else "PASSED"
                except:
                    vulnerabilities = 0
                    status = "ERROR"

            check_result = {
                "status": status,
                "vulnerable_dependencies": vulnerabilities,
                "report_file": str(report_file),
            }

            print(f"✅ Dependency scan completed: {vulnerabilities} vulnerabilities")
            return check_result

        except Exception as e:
            print(f"❌ Dependency scan failed: {e}")
            return {"status": "ERROR", "error": str(e)}

    def run_input_validation_tests(self) -> dict[str, Any]:
        """Run input validation tests."""
        print("🛡️ Running input validation tests...")

        test_cases = [
            ("admin", "username"),
            ("password123!", "password"),
            ("user@example.com", "email"),
            ("https://example.com", "url"),
            ("192.168.1.1", "ip_address"),
        ]

        passed_tests = 0
        failed_tests = 0
        test_results = []

        for value, input_type in test_cases:
            try:
                result = self.security_validator.validate_input(value, input_type)

                test_result = {
                    "input_type": input_type,
                    "value": value,
                    "is_valid": result["is_valid"],
                    "errors": result.get("errors", []),
                }

                test_results.append(test_result)

                if result["is_valid"]:
                    passed_tests += 1
                else:
                    failed_tests += 1

            except Exception as e:
                test_result = {
                    "input_type": input_type,
                    "value": value,
                    "is_valid": False,
                    "error": str(e),
                }
                test_results.append(test_result)
                failed_tests += 1

        check_result = {
            "status": "PASSED" if failed_tests == 0 else "FAILED",
            "total_tests": len(test_cases),
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "test_results": test_results,
        }

        print(f"✅ Input validation tests completed: {passed_tests}/{len(test_cases)} passed")
        return check_result

    def run_password_security_tests(self) -> dict[str, Any]:
        """Run password security tests."""
        print("🔑 Running password security tests...")

        test_passwords = [
            "password123",  # Weak
            "Password123!",  # Medium
            "SecureP@ssw0rd2024!",  # Strong
            "123456",  # Very weak
            "MySecurePassword123!@#",  # Strong
        ]

        test_results = []
        passed_tests = 0

        for password in test_passwords:
            try:
                # Test password hashing
                password_hash, salt = self.security_manager.hash_password(password)

                # Test password verification
                is_valid = self.security_manager.verify_password(password, password_hash, salt)

                test_result = {
                    "password": password,
                    "hash_generated": bool(password_hash),
                    "verification_success": is_valid,
                    "algorithm": salt,
                }

                test_results.append(test_result)

                if password_hash and is_valid:
                    passed_tests += 1

            except Exception as e:
                test_result = {"password": password, "error": str(e)}
                test_results.append(test_result)

        check_result = {
            "status": "PASSED" if passed_tests >= len(test_passwords) * 0.8 else "FAILED",
            "total_tests": len(test_passwords),
            "passed_tests": passed_tests,
            "test_results": test_results,
        }

        print(f"✅ Password security tests completed: {passed_tests}/{len(test_passwords)} passed")
        return check_result

    def run_comprehensive_audit(self) -> dict[str, Any]:
        """Run comprehensive security audit."""
        print("🚀 Starting comprehensive security audit...")

        # Run all security checks
        self.results["checks"]["static_analysis"] = self.run_static_analysis()
        self.results["checks"]["dependency_scan"] = self.run_dependency_scan()
        self.results["checks"]["input_validation"] = self.run_input_validation_tests()
        self.results["checks"]["password_security"] = self.run_password_security_tests()

        # Calculate overall security score
        overall_score = self._calculate_overall_score()
        self.results["overall_score"] = overall_score

        # Generate recommendations
        recommendations = self._generate_recommendations()
        self.results["recommendations"] = recommendations

        # Save comprehensive report
        report_file = self.output_dir / "comprehensive_security_report.json"
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print("\n📊 Comprehensive Security Audit Complete!")
        print(f"Overall Security Score: {overall_score}/100")
        print(f"Report saved to: {report_file}")

        return self.results

    def _calculate_overall_score(self) -> int:
        """Calculate overall security score."""
        score = 100

        # Static analysis scoring
        static_result = self.results["checks"].get("static_analysis", {})
        if static_result.get("status") == "PASSED":
            score -= 0
        elif static_result.get("status") == "FAILED":
            critical_findings = static_result.get("findings_by_severity", {}).get("critical", 0)
            high_findings = static_result.get("findings_by_severity", {}).get("high", 0)
            score -= critical_findings * 20 + high_findings * 10

        # Dependency scan scoring
        dep_result = self.results["checks"].get("dependency_scan", {})
        if dep_result.get("status") == "PASSED":
            score -= 0
        elif dep_result.get("status") == "FAILED":
            vulnerable_deps = dep_result.get("vulnerable_dependencies", 0)
            outdated_deps = dep_result.get("outdated_dependencies", 0)
            score -= vulnerable_deps * 15 + outdated_deps * 5

        # Input validation scoring
        input_result = self.results["checks"].get("input_validation", {})
        if input_result.get("status") == "FAILED":
            failed_tests = input_result.get("failed_tests", 0)
            score -= failed_tests * 5

        # Password security scoring
        password_result = self.results["checks"].get("password_security", {})
        if password_result.get("status") == "FAILED":
            failed_tests = password_result.get("failed_tests", 0)
            score -= failed_tests * 3

        return max(0, score)

    def _generate_recommendations(self) -> list[str]:
        """Generate security recommendations."""
        recommendations = []

        # Static analysis recommendations
        static_result = self.results["checks"].get("static_analysis", {})
        if static_result.get("status") == "FAILED":
            critical_findings = static_result.get("findings_by_severity", {}).get("critical", 0)
            if critical_findings > 0:
                recommendations.append(f"Address {critical_findings} critical security findings")

        # Dependency recommendations
        dep_result = self.results["checks"].get("dependency_scan", {})
        if dep_result.get("status") == "FAILED":
            vulnerable_deps = dep_result.get("vulnerable_dependencies", 0)
            if vulnerable_deps > 0:
                recommendations.append(f"Update {vulnerable_deps} vulnerable dependencies")

            outdated_deps = dep_result.get("outdated_dependencies", 0)
            if outdated_deps > 0:
                recommendations.append(f"Update {outdated_deps} outdated dependencies")

        # Input validation recommendations
        input_result = self.results["checks"].get("input_validation", {})
        if input_result.get("status") == "FAILED":
            recommendations.append("Review and fix input validation test failures")

        # Password security recommendations
        password_result = self.results["checks"].get("password_security", {})
        if password_result.get("status") == "FAILED":
            recommendations.append("Improve password security policies and validation")

        return recommendations

    def check_security_gates(self, min_score: int = 80) -> bool:
        """Check if security gates are passed."""
        overall_score = self.results.get("overall_score", 0)

        if overall_score < min_score:
            print(f"❌ Security gates failed: Score {overall_score} < {min_score}")
            return False

        # Check individual gate requirements
        static_result = self.results["checks"].get("static_analysis", {})
        if static_result.get("status") == "FAILED":
            critical_findings = static_result.get("findings_by_severity", {}).get("critical", 0)
            if critical_findings > 0:
                print(f"❌ Security gates failed: {critical_findings} critical findings")
                return False

        dep_result = self.results["checks"].get("dependency_scan", {})
        if dep_result.get("status") == "FAILED":
            vulnerable_deps = dep_result.get("vulnerable_dependencies", 0)
            if vulnerable_deps > 0:
                print(f"❌ Security gates failed: {vulnerable_deps} vulnerable dependencies")
                return False

        print(f"✅ Security gates passed: Score {overall_score} >= {min_score}")
        return True


def main():
    """Main function for security integration."""
    parser = argparse.ArgumentParser(description="Security Integration Script")
    parser.add_argument("--project-path", default=".", help="Project path to scan")
    parser.add_argument(
        "--output-dir", default="security_reports", help="Output directory for reports"
    )
    parser.add_argument("--min-score", type=int, default=80, help="Minimum security score")
    parser.add_argument(
        "--check-only", action="store_true", help="Only run checks, don't generate reports"
    )

    args = parser.parse_args()

    # Initialize security integration
    security_integration = SecurityIntegration(args.project_path, args.output_dir)

    # Run comprehensive audit
    results = security_integration.run_comprehensive_audit()

    # Check security gates
    gates_passed = security_integration.check_security_gates(args.min_score)

    # Exit with appropriate code
    if gates_passed:
        print("🎉 Security integration completed successfully!")
        sys.exit(0)
    else:
        print("💥 Security integration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
