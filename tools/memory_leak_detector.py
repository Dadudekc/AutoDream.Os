#!/usr/bin/env python3
"""
Memory Leak Detector & Analyzer
===============================

Comprehensive memory leak detection and analysis tool for the V2_SWARM project.
Identifies potential memory sinks, leaks, and optimization opportunities.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, focused analysis, comprehensive detection
"""

import ast
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


@dataclass
class MemoryIssue:
    """Represents a potential memory issue."""
    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    code_snippet: str
    recommendation: str


class MemoryLeakDetector:
    """Detects memory leaks and optimization opportunities."""

    def __init__(self, project_root: Path):
        """Initialize the memory leak detector."""
        self.project_root = project_root
        self.issues: List[MemoryIssue] = []
        
        # Memory leak patterns to detect
        self.memory_patterns = {
            "threading_thread": {
                "pattern": r"threading\.Thread\(",
                "severity": "HIGH",
                "description": "Thread creation without proper cleanup",
                "recommendation": "Ensure threads are properly joined or use daemon threads"
            },
            "multiprocessing_process": {
                "pattern": r"multiprocessing\.Process\(",
                "severity": "HIGH", 
                "description": "Process creation without proper cleanup",
                "recommendation": "Ensure processes are properly terminated"
            },
            "queue_without_limit": {
                "pattern": r"queue\.Queue\(\)",
                "severity": "MEDIUM",
                "description": "Unbounded queue can cause memory growth",
                "recommendation": "Consider using maxsize parameter"
            },
            "deque_without_limit": {
                "pattern": r"collections\.deque\(\)",
                "severity": "MEDIUM",
                "description": "Unbounded deque can cause memory growth",
                "recommendation": "Consider using maxlen parameter"
            },
            "sqlite_without_close": {
                "pattern": r"sqlite3\.connect\(",
                "severity": "HIGH",
                "description": "SQLite connection without explicit close",
                "recommendation": "Use context manager or ensure connection.close()"
            },
            "file_without_context": {
                "pattern": r"open\([^)]+\)(?!\s*as)",
                "severity": "HIGH",
                "description": "File opened without context manager",
                "recommendation": "Use 'with open() as f:' context manager"
            },
            "global_variables": {
                "pattern": r"^[a-zA-Z_][a-zA-Z0-9_]*\s*=",
                "severity": "LOW",
                "description": "Global variable that may accumulate data",
                "recommendation": "Consider using local variables or cleanup mechanisms"
            },
            "circular_references": {
                "pattern": r"self\.[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*self",
                "severity": "MEDIUM",
                "description": "Potential circular reference",
                "recommendation": "Use weakref or break the circular reference"
            },
            "large_data_structures": {
                "pattern": r"(list|dict|set)\(\)",
                "severity": "LOW",
                "description": "Large data structure that may grow indefinitely",
                "recommendation": "Consider size limits or cleanup mechanisms"
            },
            "event_handlers": {
                "pattern": r"addEventListener|on\w+\s*=",
                "severity": "MEDIUM",
                "description": "Event handler that may not be removed",
                "recommendation": "Ensure event handlers are properly removed"
            }
        }

    def analyze_file(self, file_path: Path) -> List[MemoryIssue]:
        """Analyze a single file for memory issues."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Check for memory leak patterns
            for line_num, line in enumerate(lines, 1):
                for pattern_name, pattern_info in self.memory_patterns.items():
                    if re.search(pattern_info["pattern"], line):
                        issue = MemoryIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            issue_type=pattern_name,
                            severity=pattern_info["severity"],
                            description=pattern_info["description"],
                            code_snippet=line.strip(),
                            recommendation=pattern_info["recommendation"]
                        )
                        issues.append(issue)
            
            # AST-based analysis for more complex issues
            try:
                tree = ast.parse(content)
                ast_issues = self._analyze_ast(tree, file_path)
                issues.extend(ast_issues)
            except SyntaxError:
                logger.warning(f"Could not parse {file_path} as Python code")
                
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        return issues

    def _analyze_ast(self, tree: ast.AST, file_path: Path) -> List[MemoryIssue]:
        """Analyze AST for complex memory issues."""
        issues = []
        
        class MemoryVisitor(ast.NodeVisitor):
            def __init__(self, file_path: Path):
                self.file_path = file_path
                self.issues = []
                self.current_class = None
                
            def visit_ClassDef(self, node: ast.ClassDef):
                old_class = self.current_class
                self.current_class = node.name
                self.generic_visit(node)
                self.current_class = old_class
                
            def visit_FunctionDef(self, node: ast.FunctionDef):
                # Check for functions that create resources
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Attribute):
                            if child.func.attr in ['Thread', 'Process', 'Queue']:
                                issue = MemoryIssue(
                                    file_path=str(self.file_path),
                                    line_number=child.lineno,
                                    issue_type="resource_creation",
                                    severity="HIGH",
                                    description=f"Resource creation in function {node.name}",
                                    code_snippet=f"{child.func.attr}()",
                                    recommendation="Ensure proper cleanup in finally block"
                                )
                                self.issues.append(issue)
                self.generic_visit(node)
                
            def visit_Assign(self, node: ast.Assign):
                # Check for assignments that might cause memory issues
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id in ['self', 'cls']:
                            # Check for circular references
                            if isinstance(node.value, ast.Name) and node.value.id == target.id:
                                issue = MemoryIssue(
                                    file_path=str(self.file_path),
                                    line_number=node.lineno,
                                    issue_type="circular_reference",
                                    severity="MEDIUM",
                                    description="Potential circular reference",
                                    code_snippet=f"{target.id} = {node.value.id}",
                                    recommendation="Use weakref or break the circular reference"
                                )
                                self.issues.append(issue)
                self.generic_visit(node)
        
        visitor = MemoryVisitor(file_path)
        visitor.visit(tree)
        return visitor.issues

    def analyze_project(self) -> Dict[str, Any]:
        """Analyze the entire project for memory issues."""
        logger.info("Starting memory leak analysis...")
        
        # Find all Python files
        python_files = list(self.project_root.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files to analyze")
        
        total_issues = 0
        files_with_issues = 0
        
        for file_path in python_files:
            # Skip test files and __pycache__
            if "test" in str(file_path) or "__pycache__" in str(file_path):
                continue
                
            issues = self.analyze_file(file_path)
            if issues:
                files_with_issues += 1
                total_issues += len(issues)
                self.issues.extend(issues)
        
        # Generate summary
        summary = {
            "total_files_analyzed": len(python_files),
            "files_with_issues": files_with_issues,
            "total_issues": total_issues,
            "issues_by_severity": self._count_by_severity(),
            "issues_by_type": self._count_by_type(),
            "top_files_with_issues": self._get_top_files_with_issues(),
            "recommendations": self._generate_recommendations()
        }
        
        logger.info(f"Analysis complete: {total_issues} issues found in {files_with_issues} files")
        return summary

    def _count_by_severity(self) -> Dict[str, int]:
        """Count issues by severity."""
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in self.issues:
            counts[issue.severity] += 1
        return counts

    def _count_by_type(self) -> Dict[str, int]:
        """Count issues by type."""
        counts = {}
        for issue in self.issues:
            counts[issue.issue_type] = counts.get(issue.issue_type, 0) + 1
        return counts

    def _get_top_files_with_issues(self) -> List[Dict[str, Any]]:
        """Get top files with most issues."""
        file_counts = {}
        for issue in self.issues:
            file_counts[issue.file_path] = file_counts.get(issue.file_path, 0) + 1
        
        # Sort by issue count
        sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"file": file_path, "issue_count": count}
            for file_path, count in sorted_files[:10]
        ]

    def _generate_recommendations(self) -> List[str]:
        """Generate high-level recommendations."""
        recommendations = []
        
        severity_counts = self._count_by_severity()
        
        if severity_counts["HIGH"] > 0:
            recommendations.append(f"🚨 URGENT: {severity_counts['HIGH']} HIGH severity issues require immediate attention")
        
        if severity_counts["MEDIUM"] > 5:
            recommendations.append(f"⚠️ WARNING: {severity_counts['MEDIUM']} MEDIUM severity issues should be addressed")
        
        # Check for specific patterns
        threading_issues = sum(1 for issue in self.issues if issue.issue_type == "threading_thread")
        if threading_issues > 0:
            recommendations.append(f"🧵 Thread Management: {threading_issues} threading issues detected - ensure proper cleanup")
        
        sqlite_issues = sum(1 for issue in self.issues if issue.issue_type == "sqlite_without_close")
        if sqlite_issues > 0:
            recommendations.append(f"🗄️ Database: {sqlite_issues} SQLite connection issues - use context managers")
        
        file_issues = sum(1 for issue in self.issues if issue.issue_type == "file_without_context")
        if file_issues > 0:
            recommendations.append(f"📁 File Handling: {file_issues} file handling issues - use context managers")
        
        return recommendations

    def generate_report(self, output_file: Path = None) -> str:
        """Generate a comprehensive memory leak report."""
        if not output_file:
            output_file = self.project_root / "memory_leak_report.json"
        
        report = {
            "timestamp": str(Path().cwd()),
            "project_root": str(self.project_root),
            "summary": self.analyze_project(),
            "detailed_issues": [
                {
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "code": issue.code_snippet,
                    "recommendation": issue.recommendation
                }
                for issue in self.issues
            ]
        }
        
        # Write report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Memory leak report saved to: {output_file}")
        return str(output_file)


def main():
    """Main function for memory leak detection."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Leak Detector")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output report file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    project_root = Path(args.project_root)
    detector = MemoryLeakDetector(project_root)
    
    # Generate report
    report_file = detector.generate_report(Path(args.output) if args.output else None)
    
    # Print summary
    summary = detector.analyze_project()
    print(f"\n🔍 Memory Leak Analysis Summary:")
    print(f"📊 Files analyzed: {summary['total_files_analyzed']}")
    print(f"⚠️ Files with issues: {summary['files_with_issues']}")
    print(f"🚨 Total issues: {summary['total_issues']}")
    print(f"📈 Issues by severity: {summary['issues_by_severity']}")
    
    print(f"\n💡 Recommendations:")
    for rec in summary['recommendations']:
        print(f"  {rec}")
    
    print(f"\n📄 Detailed report: {report_file}")


if __name__ == "__main__":
    main()
