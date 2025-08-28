#!/usr/bin/env python3
"""
Advanced Code Analysis Tools - Agent Cellphone V2
================================================

Advanced code analysis and pattern recognition tools for refactoring.
Part of SPRINT ACCELERATION mission to reach INNOVATION PLANNING MODE.

Follows V2 coding standards: ≤300 lines per module, OOP design, SRP.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict, Counter

from src.core.base_manager import BaseManager


class CodePatternAnalyzer(BaseManager):
    """
    Advanced code pattern analyzer for refactoring.
    
    Analyzes code structure, identifies patterns, detects duplication,
    and provides insights for refactoring decisions.
    """
    
    def __init__(self):
        """Initialize Code Pattern Analyzer."""
        super().__init__(
            manager_id="code_pattern_analyzer",
            name="Advanced Code Pattern Analyzer",
            description="Advanced code analysis and pattern recognition for refactoring"
        )
        
        self.patterns = self._initialize_patterns()
        self.analysis_cache = {}
        
    def _initialize_patterns(self) -> Dict[str, Any]:
        """Initialize common code patterns for analysis."""
        return {
            "duplication_patterns": {
                "function_duplication": r"def\s+\w+\s*\([^)]*\)\s*:",
                "class_duplication": r"class\s+\w+",
                "import_duplication": r"(?:from|import)\s+\w+",
                "variable_duplication": r"\w+\s*=",
                "comment_duplication": r"#.*"
            },
            "complexity_patterns": {
                "nested_loops": r"for.*for|while.*while",
                "deep_nesting": r"if.*if.*if",
                "long_functions": r"def\s+\w+[^}]*{",
                "large_classes": r"class\s+\w+[^}]*{"
            },
            "quality_patterns": {
                "magic_numbers": r"\b\d{2,}\b",
                "hardcoded_strings": r'"[^"]{20,}"',
                "unused_imports": r"import\s+\w+(?:\s+as\s+\w+)?",
                "missing_docstrings": r"def\s+\w+[^:]*:\s*(?!\s*[\"'])"
            }
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single file for code patterns and quality issues.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Analysis results dictionary
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"error": f"File not found: {file_path}"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "file_path": str(file_path),
                "file_size": len(content),
                "lines": len(content.splitlines()),
                "patterns": self._analyze_patterns(content),
                "ast_analysis": self._analyze_ast(content),
                "complexity_metrics": self._calculate_complexity(content),
                "quality_issues": self._identify_quality_issues(content),
                "refactoring_suggestions": []
            }
            
            # Generate refactoring suggestions
            analysis["refactoring_suggestions"] = self._generate_refactoring_suggestions(analysis)
            
            self.logger.info(f"File analysis completed: {file_path}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze file {file_path}: {e}")
            return {"error": str(e)}
    
    def _analyze_patterns(self, content: str) -> Dict[str, List[str]]:
        """Analyze content for common code patterns."""
        patterns = {}
        
        for pattern_type, pattern_regex in self.patterns["duplication_patterns"].items():
            matches = re.findall(pattern_regex, content, re.MULTILINE)
            patterns[pattern_type] = matches
        
        return patterns
    
    def _analyze_ast(self, content: str) -> Dict[str, Any]:
        """Analyze code using Abstract Syntax Tree."""
        try:
            tree = ast.parse(content)
            
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "variables": [],
                "complexity": 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args),
                        "has_docstring": ast.get_docstring(node) is not None
                    })
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                        "has_docstring": ast.get_docstring(node) is not None
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    analysis["imports"].append(f"{node.module}.{node.names[0].name}")
            
            return analysis
            
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}"}
        except Exception as e:
            return {"error": f"AST analysis failed: {e}"}
    
    def _calculate_complexity(self, content: str) -> Dict[str, int]:
        """Calculate code complexity metrics."""
        metrics = {
            "cyclomatic_complexity": 0,
            "nesting_depth": 0,
            "function_count": 0,
            "class_count": 0,
            "line_count": len(content.splitlines())
        }
        
        lines = content.splitlines()
        current_nesting = 0
        max_nesting = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Count nesting
            if stripped.startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif stripped.startswith(('elif ', 'else:')):
                pass  # Same nesting level
            elif stripped and not stripped.startswith(('#', '"', "'")):
                # Check for closing braces/statements
                if stripped in ('pass', 'break', 'continue', 'return') or stripped.endswith(':'):
                    current_nesting = max(0, current_nesting - 1)
            
            # Count functions and classes
            if stripped.startswith('def '):
                metrics["function_count"] += 1
            elif stripped.startswith('class '):
                metrics["class_count"] += 1
        
        metrics["nesting_depth"] = max_nesting
        metrics["cyclomatic_complexity"] = metrics["function_count"] + metrics["class_count"] + max_nesting
        
        return metrics
    
    def _identify_quality_issues(self, content: str) -> List[Dict[str, Any]]:
        """Identify code quality issues."""
        issues = []
        
        for issue_type, pattern in self.patterns["quality_patterns"].items():
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                issues.append({
                    "type": issue_type,
                    "line": content[:match.start()].count('\n') + 1,
                    "match": match.group(),
                    "severity": self._assess_issue_severity(issue_type, match.group())
                })
        
        return issues
    
    def _assess_issue_severity(self, issue_type: str, match: str) -> str:
        """Assess the severity of a quality issue."""
        severity_map = {
            "magic_numbers": "MEDIUM" if len(match) > 2 else "LOW",
            "hardcoded_strings": "HIGH" if len(match) > 30 else "MEDIUM",
            "unused_imports": "LOW",
            "missing_docstrings": "MEDIUM"
        }
        return severity_map.get(issue_type, "LOW")
    
    def _generate_refactoring_suggestions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate refactoring suggestions based on analysis."""
        suggestions = []
        
        # Function-related suggestions
        if analysis["complexity_metrics"]["function_count"] > 10:
            suggestions.append({
                "type": "function_consolidation",
                "priority": "HIGH",
                "description": "Consider consolidating similar functions",
                "impact": "Reduce code duplication and improve maintainability"
            })
        
        # Complexity suggestions
        if analysis["complexity_metrics"]["nesting_depth"] > 4:
            suggestions.append({
                "type": "complexity_reduction",
                "priority": "HIGH",
                "description": "Reduce nesting depth by extracting methods",
                "impact": "Improve readability and reduce cognitive load"
            })
        
        # Quality issue suggestions
        quality_issues = analysis.get("quality_issues", [])
        if any(issue["severity"] == "HIGH" for issue in quality_issues):
            suggestions.append({
                "type": "quality_improvement",
                "priority": "HIGH",
                "description": "Address high-severity quality issues",
                "impact": "Improve code quality and reduce technical debt"
            })
        
        return suggestions
    
    def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Analyze all Python files in a directory.
        
        Args:
            directory_path: Path to directory to analyze
            
        Returns:
            Directory analysis results
        """
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return {"error": f"Directory not found: {directory_path}"}
            
            python_files = list(directory.rglob("*.py"))
            analysis_results = []
            
            for file_path in python_files:
                file_analysis = self.analyze_file(str(file_path))
                if "error" not in file_analysis:
                    analysis_results.append(file_analysis)
            
            # Aggregate results
            directory_analysis = {
                "directory_path": str(directory),
                "total_files": len(python_files),
                "analyzed_files": len(analysis_results),
                "files": analysis_results,
                "summary": self._generate_directory_summary(analysis_results)
            }
            
            self.logger.info(f"Directory analysis completed: {directory_path}")
            return directory_analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze directory {directory_path}: {e}")
            return {"error": str(e)}
    
    def _generate_directory_summary(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for directory analysis."""
        if not file_analyses:
            return {}
        
        total_lines = sum(f.get("lines", 0) for f in file_analyses)
        total_functions = sum(f.get("ast_analysis", {}).get("function_count", 0) for f in file_analyses)
        total_classes = sum(f.get("ast_analysis", {}).get("class_count", 0) for f in file_analyses)
        
        # Aggregate quality issues
        all_issues = []
        for analysis in file_analyses:
            all_issues.extend(analysis.get("quality_issues", []))
        
        issue_counts = Counter(issue["type"] for issue in all_issues)
        
        return {
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": sum(f.get("complexity_metrics", {}).get("cyclomatic_complexity", 0) for f in file_analyses) / len(file_analyses),
            "quality_issues": dict(issue_counts),
            "refactoring_priority": self._assess_refactoring_priority(file_analyses)
        }
    
    def _assess_refactoring_priority(self, file_analyses: List[Dict[str, Any]]) -> str:
        """Assess overall refactoring priority for directory."""
        high_priority_files = 0
        total_issues = 0
        
        for analysis in file_analyses:
            if analysis.get("complexity_metrics", {}).get("nesting_depth", 0) > 4:
                high_priority_files += 1
            total_issues += len(analysis.get("quality_issues", []))
        
        if high_priority_files > len(file_analyses) * 0.3 or total_issues > len(file_analyses) * 5:
            return "HIGH"
        elif high_priority_files > len(file_analyses) * 0.1 or total_issues > len(file_analyses) * 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    # BaseManager abstract method implementations
    def _on_start(self) -> bool:
        """Start the code pattern analyzer."""
        try:
            self.logger.info("Starting Advanced Code Pattern Analyzer...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start analyzer: {e}")
            return False
    
    def _on_stop(self):
        """Stop the code pattern analyzer."""
        try:
            self.logger.info("Advanced Code Pattern Analyzer stopped")
        except Exception as e:
            self.logger.error(f"Error during analyzer shutdown: {e}")
    
    def _on_heartbeat(self):
        """Analyzer heartbeat."""
        try:
            cache_size = len(self.analysis_cache)
            self.logger.debug(f"Analyzer heartbeat - cache size: {cache_size}")
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
    
    def _on_initialize_resources(self) -> bool:
        """Initialize analyzer resources."""
        try:
            self.analysis_cache.clear()
            return True
        except Exception as e:
            self.logger.error(f"Resource initialization failed: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup analyzer resources."""
        try:
            self.analysis_cache.clear()
        except Exception as e:
            self.logger.error(f"Resource cleanup error: {e}")


def main():
    """CLI interface for Advanced Code Analysis Tools."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Code Analysis Tools")
    parser.add_argument("--file", help="Analyze single file")
    parser.add_argument("--directory", help="Analyze directory")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    analyzer = CodePatternAnalyzer()
    
    if args.file:
        results = analyzer.analyze_file(args.file)
        print(f"File Analysis Results: {results}")
    elif args.directory:
        results = analyzer.analyze_directory(args.directory)
        print(f"Directory Analysis Results: {results}")
    else:
        print("Advanced Code Analysis Tools - Agent Cellphone V2")
        print("Use --file or --directory to analyze code")


if __name__ == "__main__":
    main()
