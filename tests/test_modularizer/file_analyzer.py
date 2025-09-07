#!/usr/bin/env python3
"""
File Analyzer - File structure analysis for testing coverage.

This module handles file structure analysis including AST parsing,
line counting, and complexity analysis.
V2 COMPLIANT: Focused module under 150 lines
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Optional


class FileStructureAnalyzer:
    """
    Analyzer for file structure and complexity.
    
    This class handles:
    - File structure analysis
    - AST parsing and analysis
    - Line counting and classification
    - Complexity scoring
    """
    
    def __init__(self):
        """Initialize the file structure analyzer."""
        pass
    
    def analyze_file_structure(self, target_file: str) -> Dict[str, Any]:
        """
        Analyze the structure of a target file.
        
        Args:
            target_file: Path to the target file
            
        Returns:
            Dictionary containing file structure analysis
        """
        try:
            file_path = Path(target_file)
            if not file_path.exists():
                return {"error": "File not found"}
            
            content = file_path.read_text()
            lines = content.splitlines()
            
            # Basic line analysis
            line_analysis = self._analyze_lines(lines)
            
            # AST analysis
            ast_analysis = self._analyze_ast(content)
            
            # Combine results
            structure = {
                "total_lines": line_analysis["total_lines"],
                "code_lines": line_analysis["code_lines"],
                "comment_lines": line_analysis["comment_lines"],
                "blank_lines": line_analysis["blank_lines"],
                "functions": ast_analysis["functions"],
                "classes": ast_analysis["classes"],
                "branches": ast_analysis["branches"],
                "imports": ast_analysis["imports"],
                "complexity_score": self._calculate_complexity_score(ast_analysis)
            }
            
            return structure
            
        except Exception as e:
            return {"error": f"File structure analysis failed: {e}"}
    
    def _analyze_lines(self, lines: List[str]) -> Dict[str, int]:
        """Analyze lines for code, comments, and blanks."""
        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                comment_lines += 1
            else:
                code_lines += 1
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines
        }
    
    def _analyze_ast(self, content: str) -> Dict[str, Any]:
        """Analyze file using AST parsing."""
        try:
            tree = ast.parse(content)
            
            functions = []
            classes = []
            branches = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno)
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno)
                    })
                elif isinstance(node, ast.If) or isinstance(node, ast.For) or isinstance(node, ast.While):
                    branches.append({
                        "type": type(node).__name__,
                        "line": node.lineno
                    })
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}")
            
            return {
                "functions": functions,
                "classes": classes,
                "branches": branches,
                "imports": imports
            }
            
        except SyntaxError as e:
            return {
                "functions": [],
                "classes": [],
                "branches": [],
                "imports": [],
                "syntax_error": str(e)
            }
        except Exception as e:
            return {
                "functions": [],
                "classes": [],
                "branches": [],
                "imports": [],
                "error": str(e)
            }
    
    def _calculate_complexity_score(self, ast_analysis: Dict[str, Any]) -> int:
        """Calculate complexity score based on AST analysis."""
        try:
            function_count = len(ast_analysis.get("functions", []))
            class_count = len(ast_analysis.get("classes", []))
            branch_count = len(ast_analysis.get("branches", []))
            import_count = len(ast_analysis.get("imports", []))
            
            # Weighted complexity calculation
            complexity = (
                function_count * 2 +      # Functions are moderately complex
                class_count * 3 +         # Classes are more complex
                branch_count * 1 +        # Branches add some complexity
                import_count * 0.5        # Imports add minimal complexity
            )
            
            return int(complexity)
            
        except Exception:
            return 0
