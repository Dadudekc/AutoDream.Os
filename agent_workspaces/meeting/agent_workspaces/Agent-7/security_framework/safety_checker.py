"""
🔒 SAFETY DEPENDENCY CHECKER - SECURITY FRAMEWORK COMPONENT
Agent-7 - Security & Quality Assurance Manager

Safety dependency vulnerability checker for Python packages.
Follows V2 coding standards: ≤300 lines per module.
"""

import subprocess
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class VulnerabilityInfo:
    """Vulnerability information for a package."""
    package_name: str
    installed_version: str
    vulnerable_spec: str
    vulnerability_id: str
    advisory: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    cve_id: Optional[str] = None


class SafetyDependencyChecker:
    """Safety dependency vulnerability checker for Python packages."""
    
    def __init__(self):
        """Initialize Safety dependency checker."""
        self.safety_config = {
            "output_format": "json",
            "severity_threshold": "LOW",  # Minimum severity to report
            "timeout": 120,  # 2 minute timeout
            "exclude_packages": []  # Packages to exclude from checking
        }
        
        self.severity_levels = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4
        }
    
    def check_dependencies(self, requirements_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Check Python dependencies for known vulnerabilities using Safety.
        
        Args:
            requirements_file: Path to requirements.txt file (optional)
            
        Returns:
            dict: Vulnerability check results and analysis
        """
        check_results = {
            "check_type": "dependency_vulnerability_scan",
            "total_vulnerabilities": 0,
            "vulnerabilities_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "affected_packages": [],
            "security_score": 100.0,
            "check_status": "PENDING",
            "recommendations": []
        }
        
        try:
            # Check if Safety is installed
            if not self._is_safety_installed():
                check_results["error"] = "Safety not installed. Install with: pip install safety"
                check_results["check_status"] = "FAILED"
                return check_results
            
            # Run Safety check
            safety_output = self._run_safety_check(requirements_file)
            
            if safety_output["success"]:
                # Parse Safety output
                vulnerabilities = self._parse_safety_output(safety_output["output"])
                
                # Analyze results
                check_results.update(self._analyze_vulnerability_results(vulnerabilities))
                check_results["check_status"] = "COMPLETED"
            else:
                check_results["error"] = f"Safety check failed: {safety_output['error']}"
                check_results["check_status"] = "FAILED"
                
        except Exception as e:
            check_results["error"] = f"Check error: {str(e)}"
            check_results["check_status"] = "ERROR"
        
        return check_results
    
    def _is_safety_installed(self) -> bool:
        """Check if Safety is installed and available."""
        try:
            result = subprocess.run(
                ["safety", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _run_safety_check(self, requirements_file: Optional[str] = None) -> Dict[str, Any]:
        """Run Safety vulnerability check on dependencies."""
        try:
            # Build Safety command
            cmd = [
                "safety",
                "check",
                "--output", self.safety_config["output_format"]
            ]
            
            # Add requirements file if specified
            if requirements_file and os.path.exists(requirements_file):
                cmd.extend(["--file", requirements_file])
            
            # Run check
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.safety_config["timeout"]
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "output": None,
                    "error": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": None,
                "error": "Check timeout - too many dependencies or network issues"
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    def _parse_safety_output(self, safety_output: str) -> List[VulnerabilityInfo]:
        """Parse Safety JSON output into structured vulnerability information."""
        vulnerabilities = []
        
        try:
            # Parse JSON output
            safety_data = json.loads(safety_output)
            
            # Extract vulnerabilities from results
            for vuln in safety_data:
                vulnerability = VulnerabilityInfo(
                    package_name=vuln.get("package", "unknown"),
                    installed_version=vuln.get("installed_version", "unknown"),
                    vulnerable_spec=vuln.get("vulnerable_spec", "unknown"),
                    vulnerability_id=vuln.get("vulnerability_id", "unknown"),
                    advisory=vuln.get("advisory", "No advisory available"),
                    severity=vuln.get("severity", "MEDIUM"),
                    description=vuln.get("description", "No description available"),
                    cve_id=vuln.get("cve_id")
                )
                vulnerabilities.append(vulnerability)
                
        except json.JSONDecodeError:
            # Fallback parsing for non-JSON output
            vulnerabilities = self._parse_text_output(safety_output)
        
        return vulnerabilities
    
    def _parse_text_output(self, text_output: str) -> List[VulnerabilityInfo]:
        """Fallback parsing for text-based Safety output."""
        vulnerabilities = []
        lines = text_output.split('\n')
        
        for line in lines:
            if 'Vulnerability found in' in line:
                # Parse vulnerability line
                parts = line.split('Vulnerability found in')
                if len(parts) == 2:
                    package_info = parts[1].strip()
                    
                    # Create basic vulnerability object
                    vulnerability = VulnerabilityInfo(
                        package_name="unknown",
                        installed_version="unknown",
                        vulnerable_spec="unknown",
                        vulnerability_id="unknown",
                        advisory="No advisory available",
                        severity="MEDIUM",
                        description=package_info,
                        cve_id=None
                    )
                    vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _analyze_vulnerability_results(self, vulnerabilities: List[VulnerabilityInfo]) -> Dict[str, Any]:
        """Analyze vulnerability check results and generate insights."""
        analysis = {
            "total_vulnerabilities": len(vulnerabilities),
            "vulnerabilities_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "affected_packages": [self._vulnerability_to_dict(vuln) for vuln in vulnerabilities],
            "security_score": 100.0,
            "recommendations": []
        }
        
        # Count vulnerabilities by severity
        for vuln in vulnerabilities:
            analysis["vulnerabilities_by_severity"][vuln.severity] += 1
        
        # Calculate security score
        if analysis["total_vulnerabilities"] > 0:
            total_score = 0
            for vuln in vulnerabilities:
                severity_score = self.severity_levels.get(vuln.severity, 1)
                total_score += severity_score
            
            # Normalize score (0-100, where 100 is perfect)
            max_possible_score = analysis["total_vulnerabilities"] * 4  # Max severity
            analysis["security_score"] = max(0, 100 - (total_score / max_possible_score) * 100)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_vulnerability_recommendations(vulnerabilities)
        
        return analysis
    
    def _vulnerability_to_dict(self, vuln: VulnerabilityInfo) -> Dict[str, Any]:
        """Convert VulnerabilityInfo to dictionary for JSON serialization."""
        return {
            "package_name": vuln.package_name,
            "installed_version": vuln.installed_version,
            "vulnerable_spec": vuln.vulnerable_spec,
            "vulnerability_id": vuln.vulnerability_id,
            "advisory": vuln.advisory,
            "severity": vuln.severity,
            "description": vuln.description,
            "cve_id": vuln.cve_id
        }
    
    def _generate_vulnerability_recommendations(self, vulnerabilities: List[VulnerabilityInfo]) -> List[str]:
        """Generate actionable recommendations based on vulnerability results."""
        recommendations = []
        
        # Count critical and high severity vulnerabilities
        critical_vulns = sum(1 for vuln in vulnerabilities if vuln.severity == "CRITICAL")
        high_vulns = sum(1 for vuln in vulnerabilities if vuln.severity == "HIGH")
        
        if critical_vulns > 0:
            recommendations.append(f"Update {critical_vulns} critical vulnerabilities immediately")
        
        if high_vulns > 0:
            recommendations.append(f"Update {high_vulns} high severity vulnerabilities within 24 hours")
        
        # Medium and low severity
        medium_vulns = sum(1 for vuln in vulnerabilities if vuln.severity == "MEDIUM")
        low_vulns = sum(1 for vuln in vulnerabilities if vuln.severity == "LOW")
        
        if medium_vulns > 0:
            recommendations.append(f"Review {medium_vulns} medium severity vulnerabilities within 48 hours")
        
        if low_vulns > 0:
            recommendations.append(f"Plan updates for {low_vulns} low severity vulnerabilities")
        
        # Specific recommendations
        if vulnerabilities:
            recommendations.append("Implement automated dependency vulnerability scanning in CI/CD")
            recommendations.append("Set up vulnerability alerts for critical and high severity issues")
            recommendations.append("Regularly update dependencies to latest secure versions")
            recommendations.append("Consider using dependency pinning for critical packages")
        else:
            recommendations.append("No vulnerabilities found - maintain current dependency update practices")
        
        return recommendations
    
    def generate_vulnerability_report(self, check_results: Dict[str, Any], output_path: str) -> bool:
        """
        Generate comprehensive vulnerability report.
        
        Args:
            check_results: Results from vulnerability check
            output_path: Path to save the report
            
        Returns:
            bool: True if report generation successful
        """
        try:
            report_content = f"""# Dependency Vulnerability Report - Safety Analysis

## Executive Summary
- **Check Type**: {check_results.get('check_type', 'Unknown')}
- **Total Vulnerabilities**: {check_results.get('total_vulnerabilities', 0)}
- **Security Score**: {check_results.get('security_score', 0):.1f}/100
- **Check Status**: {check_results.get('check_status', 'Unknown')}

## Vulnerabilities by Severity
{chr(10).join(f"- {severity}: {count}" for severity, count in check_results.get('vulnerabilities_by_severity', {}).items())}

## Affected Packages
{chr(10).join(f"### {vuln.get('package_name', 'Unknown')} {vuln.get('installed_version', 'Unknown')}\n- **Vulnerability ID**: {vuln.get('vulnerability_id', 'Unknown')}\n- **Severity**: {vuln.get('severity', 'Unknown')}\n- **Description**: {vuln.get('description', 'No description')}\n- **Advisory**: {vuln.get('advisory', 'No advisory')}\n- **CVE ID**: {vuln.get('cve_id', 'N/A')}\n" for vuln in check_results.get('affected_packages', []))}

## Recommendations
{chr(10).join(f"- {rec}" for rec in check_results.get('recommendations', []))}

## Next Steps
1. Update critical and high severity vulnerabilities immediately
2. Review medium severity vulnerabilities within 48 hours
3. Plan updates for low severity vulnerabilities
4. Implement automated vulnerability scanning
5. Set up vulnerability alerts
"""
            
            with open(output_path, 'w') as f:
                f.write(report_content)
            
            return True
            
        except Exception as e:
            print(f"Error generating vulnerability report: {e}")
            return False
    
    def check_specific_package(self, package_name: str, version: str) -> Dict[str, Any]:
        """
        Check specific package for vulnerabilities.
        
        Args:
            package_name: Name of the package to check
            version: Version of the package to check
            
        Returns:
            dict: Vulnerability check results for specific package
        """
        try:
            # Create temporary requirements content
            temp_requirements = f"{package_name}=={version}"
            
            # Run Safety check on specific package
            cmd = [
                "safety",
                "check",
                "--output", self.safety_config["output_format"]
            ]
            
            result = subprocess.run(
                cmd,
                input=temp_requirements,
                text=True,
                capture_output=True,
                timeout=60
            )
            
            if result.returncode == 0:
                vulnerabilities = self._parse_safety_output(result.stdout)
                return {
                    "package": package_name,
                    "version": version,
                    "vulnerabilities_found": len(vulnerabilities),
                    "vulnerabilities": [self._vulnerability_to_dict(v) for v in vulnerabilities],
                    "check_status": "COMPLETED"
                }
            else:
                return {
                    "package": package_name,
                    "version": version,
                    "error": result.stderr,
                    "check_status": "FAILED"
                }
                
        except Exception as e:
            return {
                "package": package_name,
                "version": version,
                "error": str(e),
                "check_status": "ERROR"
            }
