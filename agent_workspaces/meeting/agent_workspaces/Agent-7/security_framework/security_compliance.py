"""
🔒 SECURITY COMPLIANCE STANDARDS - SECURITY FRAMEWORK COMPONENT
Agent-7 - Security & Quality Assurance Manager

Security compliance standards establishment and validation.
Follows V2 coding standards: ≤300 lines per module.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from .bandit_scanner import BanditSecurityScanner
from .safety_checker import SafetyDependencyChecker
from .secure_coding_guidelines import SecureCodingGuidelines
from .security_testing import SecurityTestingFramework


@dataclass
class ComplianceStandard:
    """Security compliance standard definition."""
    standard_id: str
    name: str
    version: str
    category: str
    description: str
    requirements: List[str]
    severity_levels: Dict[str, str]
    compliance_threshold: float


@dataclass
class ComplianceCheck:
    """Individual compliance check result."""
    check_id: str
    standard_id: str
    requirement: str
    status: str  # COMPLIANT, NON_COMPLIANT, PARTIAL
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    details: Dict[str, Any]
    recommendations: List[str]


class SecurityComplianceStandards:
    """Security compliance standards establishment and validation."""
    
    def __init__(self):
        """Initialize security compliance standards."""
        self.bandit_scanner = BanditSecurityScanner()
        self.safety_checker = SafetyDependencyChecker()
        self.secure_coding_checker = SecureCodingGuidelines()
        self.security_tester = SecurityTestingFramework()
        
        # Define security compliance standards
        self.compliance_standards = {
            "OWASP_TOP_10": ComplianceStandard(
                standard_id="OWASP_TOP_10",
                name="OWASP Top 10 Web Application Security Risks",
                version="2021",
                category="Web Application Security",
                description="Industry standard for web application security risks",
                requirements=[
                    "Broken Access Control",
                    "Cryptographic Failures",
                    "Injection",
                    "Insecure Design",
                    "Security Misconfiguration",
                    "Vulnerable Components",
                    "Authentication Failures",
                    "Software and Data Integrity Failures",
                    "Security Logging Failures",
                    "Server-Side Request Forgery"
                ],
                severity_levels={
                    "Broken Access Control": "HIGH",
                    "Cryptographic Failures": "HIGH",
                    "Injection": "CRITICAL",
                    "Insecure Design": "HIGH",
                    "Security Misconfiguration": "MEDIUM",
                    "Vulnerable Components": "HIGH",
                    "Authentication Failures": "HIGH",
                    "Software and Data Integrity Failures": "HIGH",
                    "Security Logging Failures": "MEDIUM",
                    "Server-Side Request Forgery": "MEDIUM"
                },
                compliance_threshold=90.0
            ),
            "V2_CODING_STANDARDS": ComplianceStandard(
                standard_id="V2_CODING_STANDARDS",
                name="V2 Coding Standards Security Requirements",
                version="2.0",
                category="Code Quality and Security",
                description="Internal V2 coding standards for security compliance",
                requirements=[
                    "No hardcoded secrets",
                    "Input validation implemented",
                    "Secure error handling",
                    "No SQL injection vulnerabilities",
                    "No command injection vulnerabilities",
                    "Strong cryptographic algorithms",
                    "Secure random number generation",
                    "No path traversal vulnerabilities",
                    "No eval() or exec() usage",
                    "Secure dependency management"
                ],
                severity_levels={
                    "No hardcoded secrets": "CRITICAL",
                    "Input validation implemented": "HIGH",
                    "Secure error handling": "MEDIUM",
                    "No SQL injection vulnerabilities": "CRITICAL",
                    "No command injection vulnerabilities": "CRITICAL",
                    "Strong cryptographic algorithms": "HIGH",
                    "Secure random number generation": "MEDIUM",
                    "No path traversal vulnerabilities": "HIGH",
                    "No eval() or exec() usage": "HIGH",
                    "Secure dependency management": "HIGH"
                },
                compliance_threshold=95.0
            ),
            "ISO_27001": ComplianceStandard(
                standard_id="ISO_27001",
                name="ISO 27001 Information Security Management",
                version="2013",
                category="Information Security Management",
                description="International standard for information security management",
                requirements=[
                    "Information Security Policy",
                    "Asset Management",
                    "Human Resource Security",
                    "Physical and Environmental Security",
                    "Access Control",
                    "Cryptography",
                    "Operations Security",
                    "Communications Security",
                    "System Acquisition and Maintenance",
                    "Incident Management"
                ],
                severity_levels={
                    "Information Security Policy": "HIGH",
                    "Asset Management": "MEDIUM",
                    "Human Resource Security": "HIGH",
                    "Physical and Environmental Security": "MEDIUM",
                    "Access Control": "CRITICAL",
                    "Cryptography": "HIGH",
                    "Operations Security": "HIGH",
                    "Communications Security": "HIGH",
                    "System Acquisition and Maintenance": "HIGH",
                    "Incident Management": "HIGH"
                },
                compliance_threshold=85.0
            )
        }
    
    def assess_compliance(self, target_directory: str, standard_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Assess compliance with security standards.
        
        Args:
            target_directory: Path to assess for compliance
            standard_ids: List of standard IDs to assess (default: all standards)
            
        Returns:
            dict: Compliance assessment results
        """
        if standard_ids is None:
            standard_ids = list(self.compliance_standards.keys())
        
        compliance_results = {
            "assessment_id": f"COMPLIANCE_ASSESSMENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "target_directory": target_directory,
            "assessment_date": datetime.now().isoformat(),
            "standards_assessed": standard_ids,
            "overall_compliance_score": 0.0,
            "standards_compliance": {},
            "compliance_summary": {},
            "recommendations": []
        }
        
        try:
            # Run comprehensive security testing
            security_test_results = self.security_tester.run_comprehensive_security_test(target_directory)
            
            # Assess compliance for each standard
            total_compliance_score = 0.0
            for standard_id in standard_ids:
                if standard_id in self.compliance_standards:
                    standard_compliance = self._assess_standard_compliance(
                        standard_id, 
                        target_directory, 
                        security_test_results
                    )
                    compliance_results["standards_compliance"][standard_id] = standard_compliance
                    total_compliance_score += standard_compliance["compliance_score"]
            
            # Calculate overall compliance score
            if standard_ids:
                compliance_results["overall_compliance_score"] = total_compliance_score / len(standard_ids)
            
            # Generate compliance summary and recommendations
            compliance_results["compliance_summary"] = self._generate_compliance_summary(
                compliance_results["standards_compliance"]
            )
            compliance_results["recommendations"] = self._generate_compliance_recommendations(
                compliance_results["standards_compliance"]
            )
            
        except Exception as e:
            compliance_results["error"] = f"Compliance assessment error: {str(e)}"
            compliance_results["overall_compliance_score"] = 0.0
        
        return compliance_results
    
    def _assess_standard_compliance(self, standard_id: str, target_directory: str, security_test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance with a specific security standard."""
        standard = self.compliance_standards[standard_id]
        
        compliance_assessment = {
            "standard_id": standard_id,
            "standard_name": standard.name,
            "standard_version": standard.version,
            "compliance_score": 0.0,
            "compliance_status": "NON_COMPLIANT",
            "requirements_assessed": len(standard.requirements),
            "requirements_compliant": 0,
            "requirements_non_compliant": 0,
            "requirements_partial": 0,
            "compliance_checks": [],
            "critical_issues": 0,
            "high_issues": 0,
            "medium_issues": 0,
            "low_issues": 0
        }
        
        # Assess each requirement
        for requirement in standard.requirements:
            compliance_check = self._assess_requirement_compliance(
                requirement, 
                standard, 
                target_directory, 
                security_test_results
            )
            compliance_assessment["compliance_checks"].append(compliance_check)
            
            # Count compliance status
            if compliance_check.status == "COMPLIANT":
                compliance_assessment["requirements_compliant"] += 1
            elif compliance_check.status == "NON_COMPLIANT":
                compliance_assessment["requirements_non_compliant"] += 1
            else:
                compliance_assessment["requirements_partial"] += 1
            
            # Count issues by severity
            severity = compliance_check.severity
            if severity == "CRITICAL":
                compliance_assessment["critical_issues"] += 1
            elif severity == "HIGH":
                compliance_assessment["high_issues"] += 1
            elif severity == "MEDIUM":
                compliance_assessment["medium_issues"] += 1
            else:
                compliance_assessment["low_issues"] += 1
        
        # Calculate compliance score
        total_requirements = len(standard.requirements)
        if total_requirements > 0:
            compliance_score = (
                (compliance_assessment["requirements_compliant"] * 1.0) +
                (compliance_assessment["requirements_partial"] * 0.5)
            ) / total_requirements * 100.0
            compliance_assessment["compliance_score"] = round(compliance_score, 2)
        
        # Determine compliance status
        if compliance_assessment["compliance_score"] >= standard.compliance_threshold:
            compliance_assessment["compliance_status"] = "COMPLIANT"
        elif compliance_assessment["compliance_score"] >= standard.compliance_threshold * 0.8:
            compliance_assessment["compliance_status"] = "PARTIALLY_COMPLIANT"
        else:
            compliance_assessment["compliance_status"] = "NON_COMPLIANT"
        
        return compliance_assessment
    
    def _assess_requirement_compliance(self, requirement: str, standard: ComplianceStandard, target_directory: str, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Assess compliance with a specific requirement."""
        check_id = f"{standard.standard_id}_{requirement.replace(' ', '_').upper()}"
        severity = standard.severity_levels.get(requirement, "MEDIUM")
        
        compliance_check = ComplianceCheck(
            check_id=check_id,
            standard_id=standard.standard_id,
            requirement=requirement,
            status="NON_COMPLIANT",
            severity=severity,
            details={},
            recommendations=[]
        )
        
        try:
            # Map requirements to security test results
            if "hardcoded secrets" in requirement.lower():
                compliance_check = self._check_hardcoded_secrets(compliance_check, security_test_results)
            elif "sql injection" in requirement.lower():
                compliance_check = self._check_sql_injection(compliance_check, security_test_results)
            elif "command injection" in requirement.lower():
                compliance_check = self._check_command_injection(compliance_check, security_test_results)
            elif "input validation" in requirement.lower():
                compliance_check = self._check_input_validation(compliance_check, security_test_results)
            elif "error handling" in requirement.lower():
                compliance_check = self._check_error_handling(compliance_check, security_test_results)
            elif "cryptographic" in requirement.lower():
                compliance_check = self._check_cryptographic_standards(compliance_check, security_test_results)
            elif "random number generation" in requirement.lower():
                compliance_check = self._check_random_generation(compliance_check, security_test_results)
            elif "path traversal" in requirement.lower():
                compliance_check = self._check_path_traversal(compliance_check, security_test_results)
            elif "eval" in requirement.lower() or "exec" in requirement.lower():
                compliance_check = self._check_dangerous_functions(compliance_check, security_test_results)
            elif "dependency" in requirement.lower():
                compliance_check = self._check_dependency_management(compliance_check, security_test_results)
            else:
                # Generic compliance check
                compliance_check = self._generic_compliance_check(compliance_check, requirement, security_test_results)
                
        except Exception as e:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"error": str(e)}
            compliance_check.recommendations = ["Review requirement manually for compliance"]
        
        return compliance_check
    
    def _check_hardcoded_secrets(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for hardcoded secrets compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        hardcoded_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "hardcoded_secrets" in v.get("violation_type", "")
        )
        
        if hardcoded_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"hardcoded_secrets_found": 0}
            compliance_check.recommendations = ["Maintain current secure secret management practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"hardcoded_secrets_found": hardcoded_violations}
            compliance_check.recommendations = [
                f"Remove {hardcoded_violations} hardcoded secrets",
                "Implement environment variable-based secret management",
                "Use secure secret management services"
            ]
        
        return compliance_check
    
    def _check_sql_injection(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for SQL injection compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        sql_injection_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "sql_injection" in v.get("violation_type", "")
        )
        
        if sql_injection_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"sql_injection_vulnerabilities": 0}
            compliance_check.recommendations = ["Maintain current SQL injection prevention practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"sql_injection_vulnerabilities": sql_injection_violations}
            compliance_check.recommendations = [
                f"Fix {sql_injection_violations} SQL injection vulnerabilities",
                "Use parameterized queries or ORM",
                "Implement input validation and sanitization"
            ]
        
        return compliance_check
    
    def _check_command_injection(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for command injection compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        command_injection_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "command_injection" in v.get("violation_type", "")
        )
        
        if command_injection_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"command_injection_vulnerabilities": 0}
            compliance_check.recommendations = ["Maintain current command injection prevention practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"command_injection_vulnerabilities": command_injection_violations}
            compliance_check.recommendations = [
                f"Fix {command_injection_violations} command injection vulnerabilities",
                "Avoid shell=True in subprocess calls",
                "Validate and sanitize all command inputs"
            ]
        
        return compliance_check
    
    def _check_input_validation(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for input validation compliance."""
        # This is a more complex check that would require deeper analysis
        # For now, we'll use a generic approach
        compliance_check.status = "PARTIAL"
        compliance_check.details = {"input_validation_check": "Manual review required"}
        compliance_check.recommendations = [
            "Implement comprehensive input validation",
            "Use regex patterns for input validation",
            "Implement type checking and length limits",
            "Validate all user inputs before processing"
        ]
        
        return compliance_check
    
    def _check_error_handling(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for secure error handling compliance."""
        # Generic error handling check
        compliance_check.status = "PARTIAL"
        compliance_check.details = {"error_handling_check": "Manual review required"}
        compliance_check.recommendations = [
            "Implement secure error handling",
            "Avoid exposing sensitive information in error messages",
            "Use generic error messages for users",
            "Log detailed errors securely without PII"
        ]
        
        return compliance_check
    
    def _check_cryptographic_standards(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for cryptographic standards compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        weak_crypto_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "weak_crypto" in v.get("violation_type", "")
        )
        
        if weak_crypto_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"weak_crypto_violations": 0}
            compliance_check.recommendations = ["Maintain current cryptographic standards"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"weak_crypto_violations": weak_crypto_violations}
            compliance_check.recommendations = [
                f"Replace {weak_crypto_violations} weak cryptographic algorithms",
                "Use SHA-256 or stronger hashing algorithms",
                "Implement proper key management",
                "Use industry-standard cryptographic libraries"
            ]
        
        return compliance_check
    
    def _check_random_generation(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for secure random number generation compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        insecure_random_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "insecure_random" in v.get("violation_type", "")
        )
        
        if insecure_random_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"insecure_random_violations": 0}
            compliance_check.recommendations = ["Maintain current secure random generation practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"insecure_random_violations": insecure_random_violations}
            compliance_check.recommendations = [
                f"Fix {insecure_random_violations} insecure random generation issues",
                "Use secrets module for cryptographic operations",
                "Avoid random module for security-critical operations"
            ]
        
        return compliance_check
    
    def _check_path_traversal(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for path traversal vulnerability compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        path_traversal_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if "path_traversal" in v.get("violation_type", "")
        )
        
        if path_traversal_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"path_traversal_vulnerabilities": 0}
            compliance_check.recommendations = ["Maintain current path traversal prevention practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"path_traversal_vulnerabilities": path_traversal_violations}
            compliance_check.recommendations = [
                f"Fix {path_traversal_violations} path traversal vulnerabilities",
                "Validate and sanitize file paths",
                "Use pathlib for safe path operations",
                "Implement proper file access controls"
            ]
        
        return compliance_check
    
    def _check_dangerous_functions(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for dangerous function usage compliance."""
        secure_coding_results = security_test_results.get("test_results", {}).get("secure_coding", {}).get("details", {})
        
        dangerous_function_violations = sum(
            1 for v in secure_coding_results.get("violations", [])
            if any(func in v.get("violation_type", "") for func in ["eval_usage", "exec_usage"])
        )
        
        if dangerous_function_violations == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"dangerous_function_usage": 0}
            compliance_check.recommendations = ["Maintain current secure function usage practices"]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {"dangerous_function_usage": dangerous_function_violations}
            compliance_check.recommendations = [
                f"Remove {dangerous_function_violations} dangerous function usages",
                "Replace eval() and exec() with safer alternatives",
                "Use JSON parsing for data deserialization",
                "Implement proper input validation"
            ]
        
        return compliance_check
    
    def _check_dependency_management(self, compliance_check: ComplianceCheck, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Check for secure dependency management compliance."""
        dependency_results = security_test_results.get("test_results", {}).get("dependency_check", {}).get("details", {})
        
        total_vulnerabilities = dependency_results.get("total_vulnerabilities", 0)
        critical_vulns = dependency_results.get("vulnerabilities_by_severity", {}).get("CRITICAL", 0)
        high_vulns = dependency_results.get("vulnerabilities_by_severity", {}).get("HIGH", 0)
        
        if total_vulnerabilities == 0:
            compliance_check.status = "COMPLIANT"
            compliance_check.details = {"vulnerable_dependencies": 0}
            compliance_check.recommendations = ["Maintain current dependency management practices"]
        elif critical_vulns == 0 and high_vulns == 0:
            compliance_check.status = "PARTIAL"
            compliance_check.details = {"vulnerable_dependencies": total_vulnerabilities, "critical_high": 0}
            compliance_check.recommendations = [
                f"Update {total_vulnerabilities} low/medium severity vulnerable dependencies",
                "Implement automated dependency vulnerability scanning"
            ]
        else:
            compliance_check.status = "NON_COMPLIANT"
            compliance_check.details = {
                "vulnerable_dependencies": total_vulnerabilities,
                "critical_vulnerabilities": critical_vulns,
                "high_vulnerabilities": high_vulns
            }
            compliance_check.recommendations = [
                f"Update {critical_vulns} critical vulnerabilities immediately",
                f"Update {high_vulns} high severity vulnerabilities within 24 hours",
                "Implement automated dependency vulnerability scanning",
                "Set up vulnerability alerts for critical and high severity issues"
            ]
        
        return compliance_check
    
    def _generic_compliance_check(self, compliance_check: ComplianceCheck, requirement: str, security_test_results: Dict[str, Any]) -> ComplianceCheck:
        """Generic compliance check for requirements not specifically handled."""
        compliance_check.status = "PARTIAL"
        compliance_check.details = {"generic_check": f"Manual review required for: {requirement}"}
        compliance_check.recommendations = [
            f"Manually review compliance with: {requirement}",
            "Document compliance evidence",
            "Implement automated checks where possible"
        ]
        
        return compliance_check
    
    def _generate_compliance_summary(self, standards_compliance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of compliance across all standards."""
        summary = {
            "total_standards": len(standards_compliance),
            "compliant_standards": 0,
            "partially_compliant_standards": 0,
            "non_compliant_standards": 0,
            "average_compliance_score": 0.0,
            "critical_issues_total": 0,
            "high_issues_total": 0,
            "medium_issues_total": 0,
            "low_issues_total": 0
        }
        
        total_score = 0.0
        for standard_id, compliance in standards_compliance.items():
            if compliance["compliance_status"] == "COMPLIANT":
                summary["compliant_standards"] += 1
            elif compliance["compliance_status"] == "PARTIALLY_COMPLIANT":
                summary["partially_compliant_standards"] += 1
            else:
                summary["non_compliant_standards"] += 1
            
            total_score += compliance["compliance_score"]
            summary["critical_issues_total"] += compliance["critical_issues"]
            summary["high_issues_total"] += compliance["high_issues"]
            summary["medium_issues_total"] += compliance["medium_issues"]
            summary["low_issues_total"] += compliance["low_issues"]
        
        if summary["total_standards"] > 0:
            summary["average_compliance_score"] = round(total_score / summary["total_standards"], 2)
        
        return summary
    
    def _generate_compliance_recommendations(self, standards_compliance: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on compliance assessment."""
        recommendations = []
        
        # Analyze overall compliance
        total_standards = len(standards_compliance)
        non_compliant = sum(1 for c in standards_compliance.values() if c["compliance_status"] == "NON_COMPLIANT")
        partially_compliant = sum(1 for c in standards_compliance.values() if c["compliance_status"] == "PARTIALLY_COMPLIANT")
        
        if non_compliant > 0:
            recommendations.append(f"Address {non_compliant} non-compliant standards immediately")
        
        if partially_compliant > 0:
            recommendations.append(f"Improve {partially_compliant} partially compliant standards")
        
        # Specific recommendations based on standards
        for standard_id, compliance in standards_compliance.items():
            if compliance["compliance_status"] != "COMPLIANT":
                recommendations.append(f"Focus on {compliance['standard_name']} compliance improvements")
        
        # General recommendations
        if non_compliant == 0 and partially_compliant == 0:
            recommendations.append("All standards are compliant - maintain current security practices")
        
        recommendations.append("Implement automated compliance monitoring and reporting")
        recommendations.append("Conduct regular compliance audits and assessments")
        recommendations.append("Provide security compliance training for teams")
        recommendations.append("Establish compliance metrics and KPIs")
        
        return recommendations
    
    def generate_compliance_report(self, compliance_results: Dict[str, Any], output_path: str) -> bool:
        """
        Generate comprehensive compliance report.
        
        Args:
            compliance_results: Results from compliance assessment
            output_path: Path to save the report
            
        Returns:
            bool: True if report generation successful
        """
        try:
            report_content = f"""# Security Compliance Assessment Report

## Executive Summary
- **Assessment ID**: {compliance_results.get('assessment_id', 'Unknown')}
- **Target Directory**: {compliance_results.get('target_directory', 'Unknown')}
- **Assessment Date**: {compliance_results.get('assessment_date', 'Unknown')}
- **Overall Compliance Score**: {compliance_results.get('overall_compliance_score', 0):.1f}/100

## Standards Assessed
{chr(10).join(f"- {standard_id}" for standard_id in compliance_results.get('standards_assessed', []))}

## Compliance Summary
{chr(10).join(f"- **{key.replace('_', ' ').title()}**: {value}" for key, value in compliance_results.get('compliance_summary', {}).items())}

## Standards Compliance Details
{chr(10).join(f"### {standard_id}\n- **Standard**: {compliance['standard_name']} v{compliance['standard_version']}\n- **Compliance Status**: {compliance['compliance_status']}\n- **Compliance Score**: {compliance['compliance_score']:.1f}/100\n- **Requirements Compliant**: {compliance['requirements_compliant']}/{compliance['requirements_assessed']}\n- **Critical Issues**: {compliance['critical_issues']}\n- **High Issues**: {compliance['high_issues']}\n" for standard_id, compliance in compliance_results.get('standards_compliance', {}).items())}

## Recommendations
{chr(10).join(f"- {rec}" for rec in compliance_results.get('recommendations', []))}

## Next Steps
1. Address non-compliant standards immediately
2. Improve partially compliant standards
3. Implement automated compliance monitoring
4. Conduct regular compliance audits
5. Provide compliance training for teams
"""
            
            with open(output_path, 'w') as f:
                f.write(report_content)
            
            return True
            
        except Exception as e:
            print(f"Error generating compliance report: {e}")
            return False
