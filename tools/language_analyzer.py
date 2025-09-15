"""Language analyzer for project scanning."""

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Optional: If tree-sitter grammars are present for Rust/JS/TS
try:
    from tree_sitter import Language, Parser
except ImportError:
    Language = None
    Parser = None
    logger.warning(
        "⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled."
    )


class LanguageAnalyzer:
    """Language analyzer for project scanning."""
    
    def __init__(self):
        """Initialize the language analyzer."""
        # Disable tree-sitter parsers for now - focus on Python analysis
        self.rust_parser = None
        self.js_parser = None

    def analyze_language(self, file_path: str, content: str) -> dict:
        """Handles language-specific code analysis for different programming languages."""
        return {}

    def _init_tree_sitter_language(self, lang_name: str) -> Parser | None:
        """
        Initializes and returns a Parser for the given language name (rust, javascript).
        Returns None if tree-sitter is not available or grammars are missing.
        """
        if not Language or not Parser:
            # Silently return None - tree-sitter is optional
            return None

        # Skip tree-sitter initialization for now - focus on Python analysis
        logger.info(f"Tree-sitter {lang_name} parsing disabled - focusing on Python analysis")
        return None

    def analyze_file(self, file_path: Path, source_code: str) -> dict:
        """
        Analyzes source code based on file extension.

        Args:
            file_path: Path to the source file
            source_code: Contents of the source file

        Returns:
            Dict with structure {language, functions, classes, routes, complexity}
        """
        suffix = file_path.suffix.lower()
        if suffix == ".py":
            return self._analyze_python(source_code)
        elif suffix == ".rs" and self.rust_parser:
            return self._analyze_rust(source_code)
        elif suffix in [".js", ".ts"] and self.js_parser:
            return self._analyze_javascript(source_code)
        else:
            return {
                "language": suffix,
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
            }

    def _analyze_python(self, source_code: str) -> dict:
        """
        Analyzes Python source code using the builtin `ast` module.
        Extracts a naive list of function defs, classes, routes, complexity, etc.
        """
        tree = ast.parse(source_code)
        functions = []
        classes = {}
        routes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

                # Route detection (Flask/FastAPI style) from existing logic
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and hasattr(decorator.func, "attr"):
                        func_attr = decorator.func.attr.lower()
                        if func_attr in {"route", "get", "post", "put", "delete", "patch"}:
                            path_arg = "/unknown"
                            methods = [func_attr.upper()]
                            if decorator.args:
                                arg0 = decorator.args[0]
                                if isinstance(arg0, ast.Str):
                                    path_arg = arg0.s
                            # Check for "methods" kwarg
                            for kw in decorator.keywords:
                                if kw.arg == "methods" and isinstance(kw.value, ast.List):
                                    extracted_methods = []
                                    for elt in kw.value.elts:
                                        if isinstance(elt, ast.Str):
                                            extracted_methods.append(elt.s.upper())
                                    if extracted_methods:
                                        methods = extracted_methods
                            for m in methods:
                                routes.append(
                                    {"function": node.name, "method": m, "path": path_arg}
                                )

            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                method_names = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
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
                classes[node.name] = {
                    "methods": method_names,
                    "docstring": docstring,
                    "base_classes": base_classes,
                }

        # Complexity = function count + sum of class methods
        complexity = len(functions) + sum(len(c["methods"]) for c in classes.values())
        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": complexity,
        }

    def _analyze_rust(self, source_code: str) -> dict:
        """Analyzes Rust source code using tree-sitter (if available)."""
        if not self.rust_parser:
            return {
                "language": ".rs",
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
            }

        tree = self.rust_parser.parse(bytes(source_code, "utf-8"))
        functions = []
        classes = {}

        def _traverse(node):
            if node.type == "function_item":
                fn_name_node = node.child_by_field_name("name")
                if fn_name_node:
                    functions.append(fn_name_node.text.decode("utf-8"))
            elif node.type == "struct_item":
                struct_name_node = node.child_by_field_name("name")
                if struct_name_node:
                    classes[struct_name_node.text.decode("utf-8")] = []
            elif node.type == "impl_item":
                impl_type_node = node.child_by_field_name("type")
                if impl_type_node:
                    impl_name = impl_type_node.text.decode("utf-8")
                    if impl_name not in classes:
                        classes[impl_name] = []
                    for child in node.children:
                        if child.type == "function_item":
                            method_node = child.child_by_field_name("name")
                            if method_node:
                                classes[impl_name].append(method_node.text.decode("utf-8"))
            for child in node.children:
                _traverse(child)

        _traverse(tree.root_node)
        complexity = len(functions) + sum(len(m) for m in classes.values())
        return {
            "language": ".rs",
            "functions": functions,
            "classes": classes,
            "routes": [],
            "complexity": complexity,
        }

    def _analyze_javascript(self, source_code: str) -> dict:
        """Analyzes JS/TS using tree-sitter (if available)."""
        if not self.js_parser:
            return {
                "language": ".js",
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
            }

        tree = self.js_parser.parse(bytes(source_code, "utf-8"))
        root = tree.root_node
        functions = []
        classes = {}
        routes = []

        def get_node_text(node):
            return node.text.decode("utf-8")

        def _traverse(node):
            if node.type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    functions.append(get_node_text(name_node))
            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    cls_name = get_node_text(name_node)
                    classes[cls_name] = []
            elif node.type == "lexical_declaration":
                # arrow functions, etc.
                for child in node.children:
                    if child.type == "variable_declarator":
                        name_node = child.child_by_field_name("name")
                        value_node = child.child_by_field_name("value")
                        if name_node and value_node and value_node.type == "arrow_function":
                            functions.append(get_node_text(name_node))
            elif node.type == "call_expression":
                if node.child_count >= 2:
                    callee_node = node.child_by_field_name("function")
                    args_node = node.child_by_field_name("arguments")
                    if callee_node:
                        callee_text = get_node_text(callee_node)
                        parts = callee_text.split(".")
                        if len(parts) == 2:
                            obj, method = parts
                            if method.lower() in {"get", "post", "put", "delete", "patch"}:
                                path_str = "/unknown"
                                if args_node and args_node.child_count > 0:
                                    first_arg = args_node.child(0)
                                    if first_arg.type == "string":
                                        path_str = get_node_text(first_arg).strip("\"'")
                                routes.append(
                                    {"object": obj, "method": method.upper(), "path": path_str}
                                )
            for child in node.children:
                _traverse(child)

        _traverse(root)
        complexity = len(functions) + sum(len(v) for v in classes.values())
        return {
            "language": ".js",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": complexity,
        }
