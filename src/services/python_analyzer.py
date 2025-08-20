#!/usr/bin/env python3
"""
Python Analyzer - Agent Cellphone V2
====================================

Handles Python-specific AST analysis.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import ast
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PythonAnalyzer:
    """Handles Python source code analysis using AST module."""
    
    def analyze(self, source_code: str) -> Dict[str, Any]:
        """
        Analyze Python source code using AST module.
        
        Args:
            source_code: Python source code string
            
        Returns:
            Dict with structure {language, functions, classes, routes, complexity}
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            logger.warning("Python syntax error, returning empty analysis")
            return {"language": ".py", "functions": [], "classes": {}, "routes": [], "complexity": 0}
        
        functions = []
        classes = {}
        routes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
                routes.extend(self._extract_routes(node))
            elif isinstance(node, ast.ClassDef):
                classes[node.name] = self._extract_class_info(node)
        
        # Complexity = function count + sum of class methods
        complexity = len(functions) + sum(len(c["methods"]) for c in classes.values())
        
        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": complexity
        }
    
    def _extract_routes(self, func_node: ast.FunctionDef) -> List[Dict[str, str]]:
        """Extract route information from function decorators."""
        routes = []
        
        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'attr'):
                func_attr = decorator.func.attr.lower()
                if func_attr in {"route", "get", "post", "put", "delete", "patch"}:
                    path_arg = "/unknown"
                    methods = [func_attr.upper()]
                    
                    if decorator.args and isinstance(decorator.args[0], ast.Str):
                        path_arg = decorator.args[0].s
                    
                    # Check for "methods" kwarg
                    for kw in decorator.keywords:
                        if kw.arg == "methods" and isinstance(kw.value, ast.List):
                            extracted_methods = []
                            for elt in kw.value.elts:
                                if isinstance(elt, ast.Str):
                                    extracted_methods.append(elt.s.upper())
                            if extracted_methods:
                                methods = extracted_methods
                    
                    for method in methods:
                        routes.append({
                            "function": func_node.name,
                            "method": method,
                            "path": path_arg
                        })
        
        return routes
    
    def _extract_class_info(self, class_node: ast.ClassDef) -> Dict[str, Any]:
        """Extract class information including methods, docstring, and base classes."""
        docstring = ast.get_docstring(class_node)
        method_names = [n.name for n in class_node.body if isinstance(n, ast.FunctionDef)]
        base_classes = []
        
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_parts = []
                attr_node = base
                while isinstance(attr_node, ast.Attribute):
                    base_parts.append(attr_node.attr)
                    attr_node = attr_node.value
                if isinstance(attr_node, ast.Name):
                    base_parts.append(attr_node.id)
                base_classes.append(".".join(reversed(base_parts)))
            else:
                base_classes.append(None)
        
        return {
            "methods": method_names,
            "docstring": docstring,
            "base_classes": base_classes
        }
