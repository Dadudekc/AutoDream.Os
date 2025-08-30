"""
🧪 FILE STRUCTURE ANALYZER - TEST-011 Modularization Implementation
Testing Framework Enhancement Manager - Agent-3

This module contains the file structure analysis and AST parsing logic.
Extracted from the monolithic testing_coverage_analysis.py file to achieve V2 compliance.
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class FileStructureAnalyzer:
    """
    Analyzes the structure of Python files for coverage analysis.
    
    This class provides:
    - File line counting and classification
    - AST parsing for code structure analysis
    - Function and class detection
    - Import statement analysis
    - Branch and complexity analysis
    """
    
    def __init__(self):
        """Initialize the file structure analyzer."""
        self.supported_extensions = {'.py', '.pyw', '.pyx'}
        self.comment_patterns = [
            r'^\s*#.*$',           # Single line comments
            r'^\s*""".*"""\s*$',   # Single line docstrings
            r'^\s*""".*$',         # Start of multi-line docstring
            r'^\s*.*"""\s*$',      # End of multi-line docstring
        ]
    
    def analyze_file_structure(self, target_file: str) -> Dict[str, Any]:
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
            "imports": [],
            "file_path": target_file,
            "file_exists": False,
            "file_size": 0,
            "error": None
        }
        
        try:
            file_path = Path(target_file)
            if not file_path.exists():
                structure["error"] = f"File does not exist: {target_file}"
                return structure
            
            if not self._is_supported_file(file_path):
                structure["error"] = f"Unsupported file type: {file_path.suffix}"
                return structure
            
            structure["file_exists"] = True
            structure["file_size"] = file_path.stat().st_size
            
            # Read file content
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
            structure["total_lines"] = len(lines)
            
            # Analyze line types
            line_analysis = self._analyze_line_types(lines)
            structure.update(line_analysis)
            
            # Parse AST for detailed analysis
            ast_analysis = self._parse_ast(content)
            structure.update(ast_analysis)
            
        except Exception as e:
            structure["error"] = str(e)
        
        return structure
    
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if the file is supported for analysis."""
        return file_path.suffix.lower() in self.supported_extensions
    
    def _analyze_line_types(self, lines: List[str]) -> Dict[str, Any]:
        """
        Analyze the types of lines in the file.
        
        Args:
            lines: List of file lines
            
        Returns:
            Dictionary with line type counts
        """
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        in_multiline_comment = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Check for blank lines
            if not stripped_line:
                blank_lines += 1
                continue
            
            # Check for multiline comment start/end
            if '"""' in stripped_line:
                if in_multiline_comment:
                    in_multiline_comment = False
                    comment_lines += 1
                else:
                    in_multiline_comment = True
                    comment_lines += 1
                continue
            
            # If we're in a multiline comment, count as comment
            if in_multiline_comment:
                comment_lines += 1
                continue
            
            # Check for single line comments
            if self._is_comment_line(stripped_line):
                comment_lines += 1
            else:
                code_lines += 1
        
        return {
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines
        }
    
    def _is_comment_line(self, line: str) -> bool:
        """Check if a line is a comment."""
        for pattern in self.comment_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _parse_ast(self, content: str) -> Dict[str, Any]:
        """
        Parse the AST of the file content.
        
        Args:
            content: The file content as a string
            
        Returns:
            Dictionary containing AST analysis results
        """
        try:
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            branches = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno),
                        "args": len(node.args.args),
                        "decorators": len(node.decorator_list),
                        "complexity": self._calculate_function_complexity(node)
                    })
                
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno),
                        "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                        "decorators": len(node.decorator_list)
                    })
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append({
                                "type": "import",
                                "module": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno
                            })
                    else:  # ImportFrom
                        module = node.module or ""
                        for alias in node.names:
                            imports.append({
                                "type": "from_import",
                                "module": module,
                                "name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno
                            })
                
                elif isinstance(node, ast.If):
                    branches.append({
                        "type": "if_statement",
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno),
                        "complexity": self._calculate_branch_complexity(node)
                    })
                
                elif isinstance(node, ast.For):
                    branches.append({
                        "type": "for_loop",
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno),
                        "complexity": self._calculate_branch_complexity(node)
                    })
                
                elif isinstance(node, ast.While):
                    branches.append({
                        "type": "while_loop",
                        "line": node.lineno,
                        "end_line": getattr(node, 'end_lineno', node.lineno),
                        "complexity": self._calculate_branch_complexity(node)
                    })
            
            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "branches": branches
            }
            
        except SyntaxError as e:
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "branches": [],
                "ast_error": f"Syntax error at line {e.lineno}: {e.text}"
            }
        except Exception as e:
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "branches": [],
                "ast_error": f"AST parsing error: {str(e)}"
            }
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate the cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_branch_complexity(self, node: ast.AST) -> int:
        """Calculate the complexity of a branch statement."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def get_file_summary(self, target_file: str) -> Dict[str, Any]:
        """
        Get a summary of the file structure.
        
        Args:
            target_file: Path to the target file
            
        Returns:
            Dictionary containing file summary
        """
        structure = self.analyze_file_structure(target_file)
        
        if structure.get("error"):
            return {"error": structure["error"]}
        
        summary = {
            "file_path": structure["file_path"],
            "file_size_bytes": structure["file_size"],
            "total_lines": structure["total_lines"],
            "code_lines": structure["code_lines"],
            "comment_lines": structure["comment_lines"],
            "blank_lines": structure["blank_lines"],
            "function_count": len(structure["functions"]),
            "class_count": len(structure["classes"]),
            "import_count": len(structure["imports"]),
            "branch_count": len(structure["branches"]),
            "code_ratio": structure["code_lines"] / structure["total_lines"] if structure["total_lines"] > 0 else 0,
            "comment_ratio": structure["comment_lines"] / structure["total_lines"] if structure["total_lines"] > 0 else 0
        }
        
        return summary
    
    def analyze_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Analyze multiple files and provide summary statistics.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dictionary containing analysis of all files
        """
        results = {
            "files_analyzed": 0,
            "files_with_errors": 0,
            "total_lines": 0,
            "total_code_lines": 0,
            "total_comment_lines": 0,
            "total_blank_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_imports": 0,
            "total_branches": 0,
            "file_details": [],
            "errors": []
        }
        
        for file_path in file_paths:
            try:
                structure = self.analyze_file_structure(file_path)
                
                if structure.get("error"):
                    results["files_with_errors"] += 1
                    results["errors"].append({
                        "file": file_path,
                        "error": structure["error"]
                    })
                else:
                    results["files_analyzed"] += 1
                    results["total_lines"] += structure["total_lines"]
                    results["total_code_lines"] += structure["code_lines"]
                    results["total_comment_lines"] += structure["comment_lines"]
                    results["total_blank_lines"] += structure["blank_lines"]
                    results["total_functions"] += len(structure["functions"])
                    results["total_classes"] += len(structure["classes"])
                    results["total_imports"] += len(structure["imports"])
                    results["total_branches"] += len(structure["branches"])
                    
                    results["file_details"].append({
                        "file": file_path,
                        "summary": self.get_file_summary(file_path)
                    })
                    
            except Exception as e:
                results["files_with_errors"] += 1
                results["errors"].append({
                    "file": file_path,
                    "error": str(e)
                })
        
        return results
