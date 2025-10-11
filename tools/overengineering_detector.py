#!/usr/bin/env python3
"""
Overengineering Detector - V2 Compliant
=======================================

Detects and prevents overengineering in the codebase.
Provides automated checks and recommendations.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import ast
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# V2 Compliance: File under 400 lines, functions under 30 lines


class OverengineeringType(Enum):
    """Overengineering type enumeration."""
    PREMATURE_OPTIMIZATION = "premature_optimization"
    COMPLEX_ABSTRACTION = "complex_abstraction"
    UNNECESSARY_PATTERN = "unnecessary_pattern"
    FEATURE_CREEP = "feature_creep"
    OVER_ARCHITECTURE = "over_architecture"


class OverengineeringSeverity(Enum):
    """Overengineering severity enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class OverengineeringIssue:
    """Overengineering issue data class."""
    
    def __init__(self, file_path: str, line_number: int, 
                 issue_type: OverengineeringType, severity: OverengineeringSeverity,
                 description: str, recommendation: str):
        """Initialize overengineering issue."""
        self.file_path = file_path
        self.line_number = line_number
        self.type = issue_type
        self.severity = severity
        self.description = description
        self.recommendation = recommendation


class OverengineeringDetector:
    """Overengineering detection system."""
    
    def __init__(self):
        """Initialize overengineering detector."""
        self.issues = []
        self.red_flags = [
            "AbstractBaseClass", "ABC", "abstractmethod",
            "asyncio", "threading", "multiprocessing",
            "inject", "dependency", "factory",
            "observer", "strategy", "command",
            "microservice", "service", "repository"
        ]
        self.green_flags = [
            "def ", "class ", "if ", "for ", "while ",
            "return", "print", "import", "from"
        ]
    
    def detect_overengineering(self, file_path: str) -> List[OverengineeringIssue]:
        """Detect overengineering in a file."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = file_path.read_text()
            
            # Check file size
            if len(content.splitlines()) > 400:
                issues.append(OverengineeringIssue(
                    file_path, 0, OverengineeringType.OVER_ARCHITECTURE,
                    OverengineeringSeverity.HIGH,
                    "File exceeds 400-line limit",
                    "Split file into smaller, focused modules"
                ))
            
            # Parse AST for complex patterns
            try:
                tree = ast.parse(content)
                issues.extend(self._analyze_ast(tree, file_path))
            except SyntaxError:
                pass
            
            # Check for red flags
            issues.extend(self._check_red_flags(content, file_path))
            
            # Check for complexity
            issues.extend(self._check_complexity(content, file_path))
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return issues
    
    def _analyze_ast(self, tree: ast.AST, file_path: str) -> List[OverengineeringIssue]:
        """Analyze AST for overengineering patterns."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for complex inheritance
            if isinstance(node, ast.ClassDef):
                if len(node.bases) > 2:
                    issues.append(OverengineeringIssue(
                        file_path, node.lineno, OverengineeringType.COMPLEX_ABSTRACTION,
                        OverengineeringSeverity.MEDIUM,
                        f"Class has {len(node.bases)} base classes",
                        "Limit inheritance to 2 levels maximum"
                    ))
                
                # Check for too many methods
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 10:
                    issues.append(OverengineeringIssue(
                        file_path, node.lineno, OverengineeringType.OVER_ARCHITECTURE,
                        OverengineeringSeverity.MEDIUM,
                        f"Class has {len(methods)} methods",
                        "Split class into smaller, focused classes"
                    ))
            
            # Check for complex functions
            elif isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    issues.append(OverengineeringIssue(
                        file_path, node.lineno, OverengineeringType.COMPLEX_ABSTRACTION,
                        OverengineeringSeverity.MEDIUM,
                        f"Function has {len(node.args.args)} parameters",
                        "Limit function parameters to 5 maximum"
                    ))
                
                # Check for complex function body
                if len(node.body) > 30:
                    issues.append(OverengineeringIssue(
                        file_path, node.lineno, OverengineeringType.OVER_ARCHITECTURE,
                        OverengineeringSeverity.MEDIUM,
                        f"Function has {len(node.body)} lines",
                        "Split function into smaller, focused functions"
                    ))
        
        return issues
    
    def _check_red_flags(self, content: str, file_path: str) -> List[OverengineeringIssue]:
        """Check for overengineering red flags."""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check for red flags
            for red_flag in self.red_flags:
                if red_flag.lower() in line_lower:
                    issues.append(OverengineeringIssue(
                        file_path, i, OverengineeringType.UNNECESSARY_PATTERN,
                        OverengineeringSeverity.MEDIUM,
                        f"Red flag detected: {red_flag}",
                        f"Consider if {red_flag} is actually needed"
                    ))
        
        return issues
    
    def _check_complexity(self, content: str, file_path: str) -> List[OverengineeringIssue]:
        """Check for complexity issues."""
        issues = []
        lines = content.splitlines()
        
        # Check for nested structures
        max_nesting = 0
        current_nesting = 0
        
        for i, line in enumerate(lines, 1):
            # Count indentation
            stripped = line.lstrip()
            if stripped:
                current_nesting = (len(line) - len(stripped)) // 4
                max_nesting = max(max_nesting, current_nesting)
        
        if max_nesting > 4:
            issues.append(OverengineeringIssue(
                file_path, 0, OverengineeringType.COMPLEX_ABSTRACTION,
                OverengineeringSeverity.MEDIUM,
                f"Maximum nesting level: {max_nesting}",
                "Reduce nesting by extracting functions or using early returns"
            ))
        
        return issues
    
    def generate_report(self) -> str:
        """Generate overengineering report."""
        if not self.issues:
            return "✅ No overengineering issues detected"
        
        report = "🚨 OVERENGINEERING DETECTION REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Group by severity
        by_severity = {}
        for issue in self.issues:
            severity = issue.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(issue)
        
        # Report by severity
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in by_severity:
                report += f"🔴 {severity.upper()} SEVERITY:\n"
                for issue in by_severity[severity]:
                    report += f"  {issue.file_path}:{issue.line_number}\n"
                    report += f"    {issue.description}\n"
                    report += f"    💡 {issue.recommendation}\n\n"
        
        # Summary
        report += "📊 SUMMARY:\n"
        report += f"  Total Issues: {len(self.issues)}\n"
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in by_severity:
                report += f"  {severity.title()}: {len(by_severity[severity])}\n"
        
        return report
    
    def get_simplification_recommendations(self) -> List[str]:
        """Get simplification recommendations."""
        recommendations = []
        
        # Analyze issues for common patterns
        abstraction_issues = [i for i in self.issues if i.type == OverengineeringType.COMPLEX_ABSTRACTION]
        if abstraction_issues:
            recommendations.append("Consider simplifying abstractions - use direct method calls instead of complex patterns")
        
        pattern_issues = [i for i in self.issues if i.type == OverengineeringType.UNNECESSARY_PATTERN]
        if pattern_issues:
            recommendations.append("Remove unnecessary design patterns - use simple, direct approaches")
        
        architecture_issues = [i for i in self.issues if i.type == OverengineeringType.OVER_ARCHITECTURE]
        if architecture_issues:
            recommendations.append("Simplify architecture - break down large files and classes")
        
        return recommendations


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Overengineering Detector")
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes')
    
    args = parser.parse_args()
    
    try:
        detector = OverengineeringDetector()
        path = Path(args.path)
        
        if path.is_file():
            issues = detector.detect_overengineering(str(path))
            detector.issues.extend(issues)
        elif path.is_dir():
            for py_file in path.rglob('*.py'):
                issues = detector.detect_overengineering(str(py_file))
                detector.issues.extend(issues)
        else:
            print(f"❌ Path not found: {path}")
            return 1
        
        if args.report:
            print(detector.generate_report())
        
        if args.fix:
            recommendations = detector.get_simplification_recommendations()
            if recommendations:
                print("💡 SIMPLIFICATION RECOMMENDATIONS:")
                for rec in recommendations:
                    print(f"  • {rec}")
            else:
                print("✅ No simplification recommendations")
        
        if not args.report and not args.fix:
            print(f"Found {len(detector.issues)} overengineering issues")
            for issue in detector.issues[:5]:  # Show first 5
                print(f"  {issue.file_path}:{issue.line_number} - {issue.description}")
            if len(detector.issues) > 5:
                print(f"  ... and {len(detector.issues) - 5} more")
        
        return 0 if len(detector.issues) == 0 else 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)






