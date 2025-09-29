"""
Enhanced Project Scanner Python Analyzer
=======================================

Python-specific analysis functionality.
"""

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PythonAnalyzer:
    """Python-specific analysis functionality."""

    def analyze_python_file(self, source_code: str, file_path: Path) -> dict[str, Any]:
        """Enhanced Python analysis with route detection and agent categorization."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            return {
                "language": ".py",
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
                "maturity": "Syntax Error",
                "agent_type": "Error",
            }

        functions = []
        classes = {}
        routes = []
        imports = []
        decorators = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "args": len(node.args.args),
                    "decorators": [self._get_decorator_name(dec) for dec in node.decorator_list],
                }
                functions.append(func_info)

                # Enhanced route detection for Flask/FastAPI/Django
                route_info = self._extract_route_info(node)
                if route_info:
                    routes.extend(route_info)

            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]

                # Extract base classes with full path resolution
                base_classes = []
                for base in node.bases:
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

                # Enhanced class analysis
                classes[node.name] = {
                    "methods": method_names,
                    "docstring": docstring,
                    "base_classes": base_classes,
                    "line": node.lineno,
                    "maturity": self._assess_class_maturity(node, docstring, method_names),
                    "agent_type": self._categorize_agent_type(node.name, docstring, method_names),
                }

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._extract_import_info(node)
                imports.append(import_info)

        # Calculate enhanced complexity score
        complexity = self._calculate_complexity(functions, classes, routes)

        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "imports": imports,
            "complexity": complexity,
            "file_size": len(source_code.splitlines()),
            "maturity": self._assess_file_maturity(classes, functions),
            "agent_type": self._categorize_file_type(file_path, classes, functions),
        }

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        return "unknown"

    def _extract_route_info(self, func_node: ast.FunctionDef) -> list[dict[str, str]]:
        """Extract route information from function decorators."""
        routes = []

        for decorator in func_node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    func_attr = decorator.func.attr.lower()
                    if func_attr in {"route", "get", "post", "put", "delete", "patch"}:
                        path_arg = "/unknown"
                        methods = [func_attr.upper()]

                        # Extract path from arguments
                        if decorator.args:
                            arg0 = decorator.args[0]
                            if isinstance(arg0, ast.Str):
                                path_arg = arg0.s
                            elif isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                                path_arg = arg0.value

                        # Extract methods from keywords
                        for kw in decorator.keywords:
                            if kw.arg == "methods" and isinstance(kw.value, ast.List):
                                extracted_methods = []
                                for elt in kw.value.elts:
                                    if isinstance(elt, ast.Str):
                                        extracted_methods.append(elt.s.upper())
                                    elif isinstance(elt, ast.Constant) and isinstance(
                                        elt.value, str
                                    ):
                                        extracted_methods.append(elt.value.upper())
                                if extracted_methods:
                                    methods = extracted_methods

                        for method in methods:
                            routes.append(
                                {
                                    "function": func_node.name,
                                    "method": method,
                                    "path": path_arg,
                                    "line": func_node.lineno,
                                }
                            )

        return routes

    def _extract_import_info(self, node: ast.AST) -> dict[str, Any]:
        """Extract import information from AST node."""
        if isinstance(node, ast.Import):
            return {
                "type": "import",
                "module": None,
                "names": [alias.name for alias in node.names],
                "line": node.lineno,
            }
        elif isinstance(node, ast.ImportFrom):
            return {
                "type": "from_import",
                "module": node.module,
                "names": [alias.name for alias in node.names],
                "level": node.level,
                "line": node.lineno,
            }
        return {}

    def _calculate_complexity(
        self, functions: list[dict], classes: dict, routes: list[dict]
    ) -> int:
        """Calculate enhanced complexity score."""
        base_complexity = len(functions) + sum(len(c.get("methods", [])) for c in classes.values())

        # Add complexity for routes (API endpoints are typically complex)
        route_complexity = len(routes) * 2

        # Add complexity for decorators and imports
        decorator_complexity = sum(len(f.get("decorators", [])) for f in functions)

        return base_complexity + route_complexity + decorator_complexity

    def _assess_class_maturity(
        self, class_node: ast.ClassDef, docstring: str, methods: list[str]
    ) -> str:
        """Assess class maturity level."""
        score = 0

        if docstring:
            score += 2
        if len(methods) > 3:
            score += 2
        if any(
            base
            for base in class_node.bases
            if not isinstance(base, ast.Name) or base.id not in ("object",)
        ):
            score += 1
        if class_node.name and class_node.name[0].isupper():
            score += 1

        if score >= 5:
            return "Core Asset"
        elif score >= 3:
            return "Prototype"
        else:
            return "Kiddie Script"

    def _categorize_agent_type(self, class_name: str, docstring: str, methods: list[str]) -> str:
        """Categorize class as agent type."""
        doc = (docstring or "").lower()

        # Check for agent-specific methods
        if "run" in methods or "execute" in methods:
            return "ActionAgent"
        if "transform" in doc or "parse" in doc or "process" in doc:
            return "DataAgent"
        if any(m in methods for m in ["predict", "analyze", "classify"]):
            return "SignalAgent"
        if "communicate" in doc or "message" in doc or "send" in methods:
            return "CommunicationAgent"
        if "scan" in doc or "monitor" in doc or "check" in methods:
            return "MonitoringAgent"

        return "UtilityAgent"

    def _assess_file_maturity(self, classes: dict, functions: list[dict]) -> str:
        """Assess overall file maturity."""
        if not classes and not functions:
            return "Empty"

        total_methods = sum(len(c.get("methods", [])) for c in classes.values())
        total_functions = len(functions)

        if total_methods + total_functions > 10:
            return "Core Asset"
        elif total_methods + total_functions > 5:
            return "Prototype"
        else:
            return "Kiddie Script"

    def _categorize_file_type(self, file_path: Path, classes: dict, functions: list[dict]) -> str:
        """Categorize file type based on content and location."""
        path_str = str(file_path).lower()

        if "test" in path_str:
            return "TestAgent"
        elif "agent" in path_str:
            return "AgentCore"
        elif "service" in path_str:
            return "ServiceAgent"
        elif "tool" in path_str:
            return "ToolAgent"
        elif any(cls.get("agent_type") == "CommunicationAgent" for cls in classes.values()):
            return "CommunicationAgent"
        elif any(cls.get("agent_type") == "MonitoringAgent" for cls in classes.values()):
            return "MonitoringAgent"
        else:
            return "UtilityAgent"
