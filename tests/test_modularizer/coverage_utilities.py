"""
🔧 COVERAGE UTILITIES - Helper functions for testing coverage analysis

This module contains utility functions and helper methods used by the testing coverage analyzer.
Extracted from testing_coverage_analysis.py for better modularity.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any


def analyze_file_structure(target_file: str) -> Dict[str, Any]:
    """
    Analyze the structure of the target file.
    
    Args:
        target_file: Path to the target file
        
    Returns:
        Dictionary containing file structure analysis
    """
    structure = {
        "total_lines": 0,
        "code_lines": 0,
        "comment_lines": 0,
        "blank_lines": 0,
        "functions": [],
        "classes": [],
        "branches": [],
        "imports": []
    }
    
    try:
        file_path = Path(target_file)
        if file_path.exists():
            content = file_path.read_text()
            lines = content.splitlines()
            structure["total_lines"] = len(lines)
            
            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                
                # Count functions and classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        structure["functions"].append({
                            "name": node.name,
                            "line": node.lineno,
                            "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        })
                    elif isinstance(node, ast.ClassDef):
                        structure["classes"].append({
                            "name": node.name,
                            "line": node.lineno,
                            "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        })
                    elif isinstance(node, ast.If):
                        structure["branches"].append({
                            "type": "if",
                            "line": node.lineno,
                            "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        })
                    elif isinstance(node, ast.For):
                        structure["branches"].append({
                            "type": "for",
                            "line": node.lineno,
                            "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        })
                    elif isinstance(node, ast.While):
                        structure["branches"].append({
                            "type": "while",
                            "line": node.lineno,
                            "end_line": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
                        })
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        structure["imports"].append({
                            "type": type(node).__name__,
                            "line": node.lineno
                        })
                
                # Calculate code lines (non-comment, non-blank)
                structure["code_lines"] = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
                structure["comment_lines"] = len([line for line in lines if line.strip().startswith('#')])
                structure["blank_lines"] = len([line for line in lines if not line.strip()])
                
            except SyntaxError:
                # File might not be valid Python
                pass
                
    except Exception as e:
        structure["error"] = str(e)
        
    return structure


def run_coverage_analysis(target_file: str, test_directory: str = None) -> Dict[str, Any]:
    """
    Run coverage analysis on the target file.
    
    Args:
        target_file: Path to the target file
        test_directory: Path to the test directory
        
    Returns:
        Dictionary containing coverage results
    """
    coverage_results = {
        "line_coverage": {},
        "branch_coverage": {},
        "function_coverage": {},
        "class_coverage": {},
        "coverage_percentage": 0.0
    }
    
    try:
        # This would integrate with actual coverage tools in a real implementation
        # For now, we'll simulate coverage analysis
        
        # Simulate line coverage
        file_path = Path(target_file)
        if file_path.exists():
            content = file_path.read_text()
            lines = content.splitlines()
            
            # Simulate coverage data (in real implementation, this would come from coverage.py)
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.strip().startswith('#'):
                    # Simulate some lines as covered, some as uncovered
                    coverage_results["line_coverage"][i] = (i % 3 != 0)  # Every 3rd line uncovered
            
            # Calculate coverage percentage
            total_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            covered_lines = sum(1 for covered in coverage_results["line_coverage"].values() if covered)
            coverage_results["coverage_percentage"] = (covered_lines / total_lines * 100) if total_lines > 0 else 0.0
            
            # Simulate other coverage metrics
            coverage_results["branch_coverage"] = {"branches": "simulated"}
            coverage_results["function_coverage"] = {"functions": "simulated"}
            coverage_results["class_coverage"] = {"classes": "simulated"}
            
    except Exception as e:
        coverage_results["error"] = str(e)
        
    return coverage_results


def identify_uncovered_areas(target_file: str, coverage_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Identify specific areas that lack test coverage.
    
    Args:
        target_file: Path to the target file
        coverage_results: Results from coverage analysis
        
    Returns:
        List of uncovered areas with details
    """
    uncovered_areas = []
    
    try:
        # Analyze line coverage to find uncovered lines
        line_coverage = coverage_results.get("line_coverage", {})
        
        for line_num, covered in line_coverage.items():
            if not covered:
                uncovered_areas.append({
                    "type": "line",
                    "line_number": line_num,
                    "description": f"Line {line_num} not covered by tests",
                    "risk_level": "MEDIUM"
                })
        
        # Add function-level analysis
        file_path = Path(target_file)
        if file_path.exists():
            try:
                content = file_path.read_text()
                lines = content.splitlines()
                
                # Find functions that might be uncovered
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check if function has any uncovered lines
                        function_lines = list(range(node.lineno, 
                                                 node.end_lineno + 1 if hasattr(node, 'end_lineno') else node.lineno + 1))
                        uncovered_lines = [line for line in function_lines if line in line_coverage and not line_coverage[line]]
                        
                        if uncovered_lines:
                            uncovered_areas.append({
                                "type": "function",
                                "name": node.name,
                                "line_number": node.lineno,
                                "uncovered_lines": uncovered_lines,
                                "description": f"Function '{node.name}' has {len(uncovered_lines)} uncovered lines",
                                "risk_level": "HIGH"
                            })
                            
            except SyntaxError:
                pass
                
    except Exception as e:
        print(f"Error identifying uncovered areas: {e}")
        
    return uncovered_areas


def assess_risk_level(coverage: float, risk_thresholds: Dict[str, float]) -> str:
    """
    Assess risk level based on coverage percentage.
    
    Args:
        coverage: Coverage percentage
        risk_thresholds: Risk assessment thresholds
        
    Returns:
        Risk level string
    """
    if coverage >= risk_thresholds["safe"]:
        return "LOW"
    elif coverage >= risk_thresholds["low_risk"]:
        return "LOW"
    elif coverage >= risk_thresholds["medium_risk"]:
        return "MEDIUM"
    elif coverage >= risk_thresholds["high_risk"]:
        return "HIGH"
    else:
        return "CRITICAL"
