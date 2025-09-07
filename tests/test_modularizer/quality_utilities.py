"""
🧪 QUALITY ASSURANCE UTILITIES - MODULARIZED COMPONENT
Testing Framework Enhancement Manager - Agent-3

This module contains utility functions for the quality assurance system.
Extracted from quality_assurance_protocols.py for better modularity.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any


def calculate_cyclomatic_complexity(tree: ast.AST) -> float:
    """Calculate cyclomatic complexity from AST."""
    complexity = 1  # Base complexity
    
    try:
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.AsyncWith):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
            elif isinstance(node, ast.Return):
                complexity += 1
                
    except Exception as e:
        print(f"Error calculating cyclomatic complexity: {e}")
        
    return float(complexity)


def is_interface_file(content: str) -> bool:
    """Check if a file is an interface file."""
    # Simple heuristic: interface files typically have many function/class definitions
    # but few implementations
    lines = content.splitlines()
    function_defs = len(re.findall(r'^def\s+', content, re.MULTILINE))
    class_defs = len(re.findall(r'^class\s+', content, re.MULTILINE))
    
    # Interface files have more definitions than implementation lines
    return function_defs + class_defs > len(lines) * 0.3


def extract_imports(content: str) -> List[str]:
    """Extract import statements from file content."""
    imports = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
    except:
        pass
    return imports


def build_dependency_graph(import_structure: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Build dependency graph from import structure."""
    graph = {}
    for file_path, imports in import_structure.items():
        file_name = Path(file_path).stem
        graph[file_name] = imports
    return graph


def analyze_file_structure(file_path: Path) -> Dict[str, Any]:
    """Analyze basic file structure and statistics."""
    analysis = {
        "file_size": 0,
        "line_count": 0,
        "function_count": 0,
        "class_count": 0,
        "complexity_score": 0.0,
        "import_count": 0
    }
    
    try:
        if file_path.exists():
            # File size
            analysis["file_size"] = file_path.stat().st_size
            
            # Line count
            content = file_path.read_text()
            lines = content.splitlines()
            analysis["line_count"] = len(lines)
            
            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                analysis["function_count"] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                analysis["class_count"] = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                analysis["import_count"] = len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
                
                # Calculate cyclomatic complexity
                analysis["complexity_score"] = calculate_cyclomatic_complexity(tree)
                
            except SyntaxError:
                # File might not be valid Python
                pass
                
    except Exception as e:
        analysis["error"] = str(e)
        
    return analysis
