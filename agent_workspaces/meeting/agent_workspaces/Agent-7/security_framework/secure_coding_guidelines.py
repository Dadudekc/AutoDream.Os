"""
🔒 SECURE CODING GUIDELINES - SECURITY FRAMEWORK COMPONENT
Agent-7 - Security & Quality Assurance Manager

Secure coding practices and guidelines implementation.
Follows V2 coding standards: ≤300 lines per module.
"""

import re
import ast
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SecurityViolation:
    """Security violation found in code."""
    violation_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    line_number: int
    filename: str
    code_snippet: str
    description: str
    recommendation: str
    cwe_id: Optional[str] = None


class SecureCodingGuidelines:
    """Secure coding practices and guidelines checker."""
    
    def __init__(self):
        """Initialize secure coding guidelines checker."""
        self.security_patterns = {
            "hardcoded_secrets": {
                "pattern": r"(password|secret|key|token)\s*=\s*['\"][^'\"]+['\"]",
                "severity": "CRITICAL",
                "description": "Hardcoded secrets in code",
                "recommendation": "Use environment variables or secure secret management",
                "cwe_id": "CWE-259"
            },
            "sql_injection": {
                "pattern": r"execute\s*\(\s*[\"'].*\+.*[\"']",
                "severity": "HIGH",
                "description": "Potential SQL injection vulnerability",
                "recommendation": "Use parameterized queries or ORM",
                "cwe_id": "CWE-89"
            },
            "command_injection": {
                "pattern": r"(os\.system|subprocess\.call|subprocess\.Popen)\s*\(\s*[\"'].*\+.*[\"']",
                "severity": "HIGH",
                "description": "Potential command injection vulnerability",
                "recommendation": "Avoid shell=True and validate all inputs",
                "cwe_id": "CWE-78"
            },
            "weak_crypto": {
                "pattern": r"(md5|sha1)\s*\(",
                "severity": "MEDIUM",
                "description": "Weak cryptographic hash function",
                "recommendation": "Use SHA-256 or stronger hashing algorithms",
                "cwe_id": "CWE-327"
            },
            "insecure_random": {
                "pattern": r"random\.(randint|choice|random)\s*\(",
                "severity": "MEDIUM",
                "description": "Insecure random number generation",
                "recommendation": "Use secrets module for cryptographic operations",
                "cwe_id": "CWE-338"
            },
            "path_traversal": {
                "pattern": r"open\s*\(\s*[\"'].*\+.*[\"']",
                "severity": "MEDIUM",
                "description": "Potential path traversal vulnerability",
                "recommendation": "Validate and sanitize file paths",
                "cwe_id": "CWE-22"
            }
        }
        
        self.secure_practices = {
            "input_validation": {
                "required": True,
                "description": "All user inputs must be validated",
                "examples": ["regex validation", "type checking", "length limits"]
            },
            "output_encoding": {
                "required": True,
                "description": "Output must be properly encoded",
                "examples": ["HTML encoding", "URL encoding", "JSON escaping"]
            },
            "error_handling": {
                "required": True,
                "description": "Errors must not expose sensitive information",
                "examples": ["Generic error messages", "Logging without PII"]
            },
            "authentication": {
                "required": True,
                "description": "Proper authentication mechanisms",
                "examples": ["Multi-factor auth", "Session management", "Password policies"]
            },
            "authorization": {
                "required": True,
                "description": "Proper authorization checks",
                "examples": ["Role-based access", "Resource-level permissions"]
            }
        }
    
    def analyze_code_security(self, target_directory: str) -> Dict[str, Any]:
        """
        Analyze code for security violations and compliance with secure coding guidelines.
        
        Args:
            target_directory: Path to analyze for security compliance
            
        Returns:
            dict: Security analysis results and recommendations
        """
        analysis_results = {
            "analysis_directory": target_directory,
            "total_violations": 0,
            "violations_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "violations_by_type": {},
            "security_score": 100.0,
            "compliance_status": "PENDING",
            "violations": [],
            "recommendations": []
        }
        
        try:
            # Find Python source files
            python_files = self._find_python_files(target_directory)
            
            if not python_files:
                analysis_results["error"] = "No Python source files found"
                analysis_results["compliance_status"] = "NO_FILES"
                return analysis_results
            
            # Analyze each file for security violations
            all_violations = []
            for python_file in python_files:
                file_violations = self._analyze_file_security(python_file)
                all_violations.extend(file_violations)
            
            # Analyze results
            analysis_results.update(self._analyze_security_violations(all_violations))
            analysis_results["compliance_status"] = "COMPLETED"
            
        except Exception as e:
            analysis_results["error"] = f"Analysis error: {str(e)}"
            analysis_results["compliance_status"] = "ERROR"
        
        return analysis_results
    
    def _find_python_files(self, target_directory: str) -> List[Path]:
        """Find all Python source files in target directory."""
        python_files = []
        target_path = Path(target_directory)
        
        if not target_path.exists():
            return python_files
        
        # Recursively find .py files
        for py_file in target_path.rglob("*.py"):
            # Exclude common directories
            if any(exclude in str(py_file) for exclude in ["__pycache__", ".git", "venv", "env"]):
                continue
            python_files.append(py_file)
        
        return python_files
    
    def _analyze_file_security(self, file_path: Path) -> List[SecurityViolation]:
        """Analyze individual file for security violations."""
        violations = []
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Pattern-based analysis
            violations.extend(self._pattern_based_analysis(content, file_path))
            
            # AST-based analysis
            violations.extend(self._ast_based_analysis(content, file_path))
            
        except Exception as e:
            # Create violation for file reading error
            violation = SecurityViolation(
                violation_type="FILE_READ_ERROR",
                severity="MEDIUM",
                line_number=0,
                filename=str(file_path),
                code_snippet="",
                description=f"Error reading file: {str(e)}",
                recommendation="Check file permissions and encoding",
                cwe_id=None
            )
            violations.append(violation)
        
        return violations
    
    def _pattern_based_analysis(self, content: str, file_path: Path) -> List[SecurityViolation]:
        """Analyze content using regex patterns for security violations."""
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for violation_type, pattern_info in self.security_patterns.items():
                if re.search(pattern_info["pattern"], line, re.IGNORECASE):
                    violation = SecurityViolation(
                        violation_type=violation_type,
                        severity=pattern_info["severity"],
                        line_number=line_num,
                        filename=str(file_path),
                        code_snippet=line.strip(),
                        description=pattern_info["description"],
                        recommendation=pattern_info["recommendation"],
                        cwe_id=pattern_info["cwe_id"]
                    )
                    violations.append(violation)
        
        return violations
    
    def _ast_based_analysis(self, content: str, file_path: Path) -> List[SecurityViolation]:
        """Analyze content using AST for deeper security analysis."""
        violations = []
        
        try:
            tree = ast.parse(content)
            
            # Analyze AST nodes for security issues
            for node in ast.walk(tree):
                violations.extend(self._analyze_ast_node(node, file_path))
                
        except SyntaxError:
            # File has syntax errors, skip AST analysis
            pass
        
        return violations
    
    def _analyze_ast_node(self, node: ast.AST, file_path: Path) -> List[SecurityViolation]:
        """Analyze individual AST node for security issues."""
        violations = []
        
        # Check for eval() usage
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                violation = SecurityViolation(
                    violation_type="eval_usage",
                    severity="HIGH",
                    line_number=getattr(node, 'lineno', 0),
                    filename=str(file_path),
                    code_snippet="eval() function usage",
                    description="eval() function can execute arbitrary code",
                    recommendation="Avoid eval() - use safer alternatives",
                    cwe_id="CWE-95"
                )
                violations.append(violation)
        
        # Check for exec() usage
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "exec":
                violation = SecurityViolation(
                    violation_type="exec_usage",
                    severity="HIGH",
                    line_number=getattr(node, 'lineno', 0),
                    filename=str(file_path),
                    code_snippet="exec() function usage",
                    description="exec() function can execute arbitrary code",
                    recommendation="Avoid exec() - use safer alternatives",
                    cwe_id="CWE-95"
                )
                violations.append(violation)
        
        # Check for pickle usage
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in getattr(node, 'names', []):
                if 'pickle' in getattr(alias, 'name', ''):
                    violation = SecurityViolation(
                        violation_type="pickle_usage",
                        severity="MEDIUM",
                        line_number=getattr(node, 'lineno', 0),
                        filename=str(file_path),
                        code_snippet="pickle module import",
                        description="pickle can execute arbitrary code during deserialization",
                        recommendation="Use JSON or other safe serialization formats",
                        cwe_id="CWE-502"
                    )
                    violations.append(violation)
        
        return violations
    
    def _analyze_security_violations(self, violations: List[SecurityViolation]) -> Dict[str, Any]:
        """Analyze security violations and generate insights."""
        analysis = {
            "total_violations": len(violations),
            "violations_by_severity": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "violations_by_type": {},
            "security_score": 100.0,
            "recommendations": []
        }
        
        # Count violations by severity and type
        for violation in violations:
            analysis["violations_by_severity"][violation.severity] += 1
            
            if violation.violation_type not in analysis["violations_by_type"]:
                analysis["violations_by_type"][violation.violation_type] = 0
            analysis["violations_by_type"][violation.violation_type] += 1
        
        # Calculate security score
        if analysis["total_violations"] > 0:
            total_score = 0
            severity_weights = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
            
            for violation in violations:
                total_score += severity_weights.get(violation.severity, 1)
            
            # Normalize score (0-100, where 100 is perfect)
            max_possible_score = analysis["total_violations"] * 4  # Max severity
            analysis["security_score"] = max(0, 100 - (total_score / max_possible_score) * 100)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_security_recommendations(violations)
        
        return analysis
    
    def _generate_security_recommendations(self, violations: List[SecurityViolation]) -> List[str]:
        """Generate actionable security recommendations based on violations."""
        recommendations = []
        
        # Count violations by severity
        critical_violations = sum(1 for v in violations if v.severity == "CRITICAL")
        high_violations = sum(1 for v in violations if v.severity == "HIGH")
        medium_violations = sum(1 for v in violations if v.severity == "MEDIUM")
        
        if critical_violations > 0:
            recommendations.append(f"Fix {critical_violations} critical security violations immediately")
        
        if high_violations > 0:
            recommendations.append(f"Address {high_violations} high severity violations within 24 hours")
        
        if medium_violations > 0:
            recommendations.append(f"Review {medium_violations} medium severity violations within 48 hours")
        
        # Specific recommendations based on violation types
        violation_types = set(v.violation_type for v in violations)
        
        if "hardcoded_secrets" in violation_types:
            recommendations.append("Implement secure secret management using environment variables")
        
        if "sql_injection" in violation_types:
            recommendations.append("Use parameterized queries or ORM to prevent SQL injection")
        
        if "command_injection" in violation_types:
            recommendations.append("Validate and sanitize all command inputs")
        
        if "weak_crypto" in violation_types:
            recommendations.append("Use strong cryptographic algorithms (SHA-256+)")
        
        # General recommendations
        if violations:
            recommendations.append("Implement automated security code scanning in CI/CD")
            recommendations.append("Conduct regular security code reviews")
            recommendations.append("Provide secure coding training for developers")
            recommendations.append("Establish security coding standards and guidelines")
        else:
            recommendations.append("No security violations found - maintain current secure coding practices")
        
        return recommendations
    
    def generate_security_report(self, analysis_results: Dict[str, Any], output_path: str) -> bool:
        """
        Generate comprehensive security coding guidelines report.
        
        Args:
            analysis_results: Results from security analysis
            output_path: Path to save the report
            
        Returns:
            bool: True if report generation successful
        """
        try:
            report_content = f"""# Secure Coding Guidelines Report

## Executive Summary
- **Analysis Directory**: {analysis_results.get('analysis_directory', 'Unknown')}
- **Total Violations**: {analysis_results.get('total_violations', 0)}
- **Security Score**: {analysis_results.get('security_score', 0):.1f}/100
- **Compliance Status**: {analysis_results.get('compliance_status', 'Unknown')}

## Violations by Severity
{chr(10).join(f"- {severity}: {count}" for severity, count in analysis_results.get('violations_by_severity', {}).items())}

## Violations by Type
{chr(10).join(f"- {vtype}: {count}" for vtype, count in analysis_results.get('violations_by_type', {}).items())}

## Detailed Violations
{chr(10).join(f"### {v.get('filename', 'Unknown')}:{v.get('line_number', 0)}\n- **Type**: {v.get('violation_type', 'Unknown')}\n- **Severity**: {v.get('severity', 'Unknown')}\n- **Description**: {v.get('description', 'No description')}\n- **Code**: {v.get('code_snippet', 'N/A')}\n- **Recommendation**: {v.get('recommendation', 'No recommendation')}\n- **CWE ID**: {v.get('cwe_id', 'N/A')}\n" for v in analysis_results.get('violations', []))}

## Recommendations
{chr(10).join(f"- {rec}" for rec in analysis_results.get('recommendations', []))}

## Secure Coding Best Practices
{chr(10).join(f"### {practice}\n- **Required**: {'Yes' if info['required'] else 'No'}\n- **Description**: {info['description']}\n- **Examples**: {', '.join(info['examples'])}\n" for practice, info in self.secure_practices.items())}

## Next Steps
1. Address critical and high severity violations immediately
2. Implement automated security scanning
3. Provide secure coding training
4. Establish security coding standards
5. Conduct regular security reviews
"""
            
            with open(output_path, 'w') as f:
                f.write(report_content)
            
            return True
            
        except Exception as e:
            print(f"Error generating security report: {e}")
            return False
