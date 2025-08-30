"""
🔒 BANDIT SECURITY SCANNER - SECURITY FRAMEWORK COMPONENT
Agent-7 - Security & Quality Assurance Manager

Bandit security linter integration for Python code security analysis.
Follows V2 coding standards: ≤300 lines per module.
"""

import subprocess
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SecurityIssue:
    """Security issue detected by Bandit."""
    issue_id: str
    severity: str  # LOW, MEDIUM, HIGH
    confidence: str  # LOW, MEDIUM, HIGH
    issue_text: str
    line_number: int
    filename: str
    code: str
    more_info: str


class BanditSecurityScanner:
    """Bandit security scanner integration for Python code."""
    
    def __init__(self):
        """Initialize Bandit security scanner."""
        self.bandit_config = {
            "exclude_dirs": ["tests", "test_", "__pycache__", ".git"],
            "skips": ["B101", "B601"],  # Skip specific test-related warnings
            "severity_levels": ["LOW", "MEDIUM", "HIGH"],
            "confidence_levels": ["LOW", "MEDIUM", "HIGH"]
        }
        
        self.severity_scores = {
            "LOW": 1,
            "MEDIUM": 3,
            "HIGH": 5
        }
        
        self.confidence_scores = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3
        }
    
    def scan_directory(self, target_directory: str) -> Dict[str, Any]:
        """
        Scan directory for security issues using Bandit.
        
        Args:
            target_directory: Path to scan for security issues
            
        Returns:
            dict: Security scan results and analysis
        """
        scan_results = {
            "scan_directory": target_directory,
            "total_issues": 0,
            "issues_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "issues_by_confidence": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "security_score": 100.0,
            "issues": [],
            "recommendations": [],
            "scan_status": "PENDING"
        }
        
        try:
            # Check if Bandit is installed
            if not self._is_bandit_installed():
                scan_results["error"] = "Bandit not installed. Install with: pip install bandit"
                scan_results["scan_status"] = "FAILED"
                return scan_results
            
            # Run Bandit scan
            bandit_output = self._run_bandit_scan(target_directory)
            
            if bandit_output["success"]:
                # Parse Bandit output
                issues = self._parse_bandit_output(bandit_output["output"])
                
                # Analyze results
                scan_results.update(self._analyze_security_results(issues))
                scan_results["scan_status"] = "COMPLETED"
            else:
                scan_results["error"] = f"Bandit scan failed: {bandit_output['error']}"
                scan_results["scan_status"] = "FAILED"
                
        except Exception as e:
            scan_results["error"] = f"Scan error: {str(e)}"
            scan_results["scan_status"] = "ERROR"
        
        return scan_results
    
    def _is_bandit_installed(self) -> bool:
        """Check if Bandit is installed and available."""
        try:
            result = subprocess.run(
                ["bandit", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _run_bandit_scan(self, target_directory: str) -> Dict[str, Any]:
        """Run Bandit security scan on target directory."""
        try:
            # Build Bandit command
            cmd = [
                "bandit",
                "-r",  # Recursive scan
                "-f", "json",  # JSON output format
                "-x", ",".join(self.bandit_config["exclude_dirs"]),  # Exclude directories
                "-s", ",".join(self.bandit_config["skips"]),  # Skip specific tests
                target_directory
            ]
            
            # Run scan
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
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
                "error": "Scan timeout - directory too large or complex"
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e)
            }
    
    def _parse_bandit_output(self, bandit_output: str) -> List[SecurityIssue]:
        """Parse Bandit JSON output into structured security issues."""
        issues = []
        
        try:
            # Parse JSON output
            scan_data = json.loads(bandit_output)
            
            # Extract issues from results
            for result in scan_data.get("results", []):
                issue = SecurityIssue(
                    issue_id=result.get("issue_id", "UNKNOWN"),
                    severity=result.get("issue_severity", "LOW"),
                    confidence=result.get("issue_confidence", "LOW"),
                    issue_text=result.get("issue_text", "Unknown issue"),
                    line_number=result.get("line_number", 0),
                    filename=result.get("filename", "unknown"),
                    code=result.get("code", ""),
                    more_info=result.get("more_info", "")
                )
                issues.append(issue)
                
        except json.JSONDecodeError:
            # Fallback parsing for non-JSON output
            issues = self._parse_text_output(bandit_output)
        
        return issues
    
    def _parse_text_output(self, text_output: str) -> List[SecurityIssue]:
        """Fallback parsing for text-based Bandit output."""
        issues = []
        lines = text_output.split('\n')
        
        for line in lines:
            if '>> Issue:' in line:
                # Parse issue line
                parts = line.split('>> Issue:')
                if len(parts) == 2:
                    issue_text = parts[1].strip()
                    
                    # Create basic issue object
                    issue = SecurityIssue(
                        issue_id="UNKNOWN",
                        severity="MEDIUM",
                        confidence="MEDIUM",
                        issue_text=issue_text,
                        line_number=0,
                        filename="unknown",
                        code="",
                        more_info=""
                    )
                    issues.append(issue)
        
        return issues
    
    def _analyze_security_results(self, issues: List[SecurityIssue]) -> Dict[str, Any]:
        """Analyze security scan results and generate insights."""
        analysis = {
            "total_issues": len(issues),
            "issues_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "issues_by_confidence": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "security_score": 100.0,
            "issues": [self._issue_to_dict(issue) for issue in issues],
            "recommendations": []
        }
        
        # Count issues by severity and confidence
        for issue in issues:
            analysis["issues_by_severity"][issue.severity] += 1
            analysis["issues_by_confidence"][issue.confidence] += 1
        
        # Calculate security score
        if analysis["total_issues"] > 0:
            total_score = 0
            for issue in issues:
                severity_score = self.severity_scores.get(issue.severity, 1)
                confidence_score = self.confidence_scores.get(issue.confidence, 1)
                total_score += severity_score * confidence_score
            
            # Normalize score (0-100, where 100 is perfect)
            max_possible_score = analysis["total_issues"] * 15  # Max severity * max confidence
            analysis["security_score"] = max(0, 100 - (total_score / max_possible_score) * 100)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_security_recommendations(issues)
        
        return analysis
    
    def _issue_to_dict(self, issue: SecurityIssue) -> Dict[str, Any]:
        """Convert SecurityIssue to dictionary for JSON serialization."""
        return {
            "issue_id": issue.issue_id,
            "severity": issue.severity,
            "confidence": issue.confidence,
            "issue_text": issue.issue_text,
            "line_number": issue.line_number,
            "filename": issue.filename,
            "code": issue.code,
            "more_info": issue.more_info
        }
    
    def _generate_security_recommendations(self, issues: List[SecurityIssue]) -> List[str]:
        """Generate actionable security recommendations based on scan results."""
        recommendations = []
        
        # Count high severity issues
        high_severity = sum(1 for issue in issues if issue.severity == "HIGH")
        if high_severity > 0:
            recommendations.append(f"Address {high_severity} high severity security issues immediately")
        
        # Count medium severity issues
        medium_severity = sum(1 for issue in issues if issue.severity == "MEDIUM")
        if medium_severity > 0:
            recommendations.append(f"Review and fix {medium_severity} medium severity issues within 48 hours")
        
        # Specific recommendations based on issue types
        issue_types = set(issue.issue_id for issue in issues)
        if "B101" in issue_types:
            recommendations.append("Implement proper input validation for all user inputs")
        if "B102" in issue_types:
            recommendations.append("Use secure random number generation for cryptographic operations")
        if "B103" in issue_types:
            recommendations.append("Avoid hardcoded passwords and secrets in code")
        
        # General recommendations
        if not recommendations:
            recommendations.append("No critical security issues found - maintain current security practices")
        else:
            recommendations.append("Implement automated security scanning in CI/CD pipeline")
            recommendations.append("Conduct regular security code reviews")
        
        return recommendations
    
    def generate_security_report(self, scan_results: Dict[str, Any], output_path: str) -> bool:
        """
        Generate comprehensive security report.
        
        Args:
            scan_results: Results from security scan
            output_path: Path to save the report
            
        Returns:
            bool: True if report generation successful
        """
        try:
            report_content = f"""# Security Scan Report - Bandit Analysis

## Executive Summary
- **Scan Directory**: {scan_results.get('scan_directory', 'Unknown')}
- **Total Issues Found**: {scan_results.get('total_issues', 0)}
- **Security Score**: {scan_results.get('security_score', 0):.1f}/100
- **Scan Status**: {scan_results.get('scan_status', 'Unknown')}

## Issues by Severity
{chr(10).join(f"- {severity}: {count}" for severity, count in scan_results.get('issues_by_severity', {}).items())}

## Issues by Confidence
{chr(10).join(f"- {confidence}: {count}" for confidence, count in scan_results.get('issues_by_confidence', {}).items())}

## Detailed Issues
{chr(10).join(f"### {issue.get('filename', 'Unknown')}:{issue.get('line_number', 0)}\n- **Issue**: {issue.get('issue_text', 'Unknown')}\n- **Severity**: {issue.get('severity', 'Unknown')}\n- **Confidence**: {issue.get('confidence', 'Unknown')}\n- **Code**: {issue.get('code', 'N/A')}\n" for issue in scan_results.get('issues', []))}

## Recommendations
{chr(10).join(f"- {rec}" for rec in scan_results.get('recommendations', []))}

## Next Steps
1. Address high severity issues immediately
2. Review medium severity issues within 48 hours
3. Implement automated security scanning
4. Conduct regular security code reviews
"""
            
            with open(output_path, 'w') as f:
                f.write(report_content)
            
            return True
            
        except Exception as e:
            print(f"Error generating security report: {e}")
            return False
