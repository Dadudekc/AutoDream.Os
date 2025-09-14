"""Language-specific code analysis for different programming languages."""

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
    """Handles language-specific code analysis for different programming languages."""

    def __init__(self):
        """Initialize language analyzers and parsers."""
        self.rust_parser = self._init_tree_sitter_language("rust")
        self.js_parser = self._init_tree_sitter_language("javascript")

    def _init_tree_sitter_language(self, lang_name: str) -> Parser | None:
        """
        Initializes and returns a Parser for the given language name (rust, javascript).
        Adjust grammar_paths to point at your compiled .so files if using tree-sitter.
        """
        if not Language or not Parser:
            logger.warning(
                "⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled."
            )
            return None

        grammar_paths = {
            "rust": "path/to/tree-sitter-rust.so",  # <-- Adjust as needed
            "javascript": "path/to/tree-sitter-javascript.so",  # <-- Adjust as needed
        }
        if lang_name not in grammar_paths:
            logger.warning(f"⚠️ No grammar path for {lang_name}. Skipping.")
            return None

        grammar_path = grammar_paths[lang_name]
        if not Path(grammar_path).exists():
            logger.warning(f"⚠️ {lang_name} grammar not found at {grammar_path}")
            return None

        try:
            lang_lib = Language(grammar_path, lang_name)
            parser = Parser()
            parser.set_language(lang_lib)
            return parser
        except Exception as e:
            logger.error(f"⚠️ Failed to initialize tree-sitter {lang_name} parser: {e}")
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
                            routes.append({"path": path_arg, "methods": methods, "function": node.name})

            elif isinstance(node, ast.ClassDef):
                class_methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_methods.append(item.name)
                classes[node.name] = class_methods

        return {
            "language": "python",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": len(functions) + len(classes) * 2,
        }

    def _analyze_rust(self, source_code: str) -> dict:
        """Analyzes Rust source code using tree-sitter."""
        if not self.rust_parser:
            return {"language": "rust", "functions": [], "classes": {}, "routes": [], "complexity": 0}

        tree = self.rust_parser.parse(bytes(source_code, "utf8"))
        functions = []
        classes = {}

        # Basic tree-sitter query for functions and structs
        # This is a simplified example - you'd want more sophisticated queries
        def traverse_node(node):
            if node.type == "function_item":
                # Extract function name
                for child in node.children:
                    if child.type == "identifier":
                        functions.append(child.text.decode("utf8"))
                        break
            elif node.type == "struct_item":
                # Extract struct name
                for child in node.children:
                    if child.type == "type_identifier":
                        classes[child.text.decode("utf8")] = []
                        break

        traverse_node(tree.root_node)

        return {
            "language": "rust",
            "functions": functions,
            "classes": classes,
            "routes": [],  # Rust web frameworks would need specific detection
            "complexity": len(functions) + len(classes) * 2,
        }

    def _analyze_javascript(self, source_code: str) -> dict:
        """Analyzes JavaScript/TypeScript source code using tree-sitter."""
        if not self.js_parser:
            return {"language": "javascript", "functions": [], "classes": {}, "routes": [], "complexity": 0}

        tree = self.js_parser.parse(bytes(source_code, "utf8"))
        functions = []
        classes = {}

        # Basic tree-sitter query for functions and classes
        def traverse_node(node):
            if node.type in ["function_declaration", "arrow_function", "method_definition"]:
                # Extract function name
                for child in node.children:
                    if child.type == "identifier":
                        functions.append(child.text.decode("utf8"))
                        break
            elif node.type == "class_declaration":
                # Extract class name
                for child in node.children:
                    if child.type == "type_identifier":
                        classes[child.text.decode("utf8")] = []
                        break

        traverse_node(tree.root_node)

        return {
            "language": "javascript",
            "functions": functions,
            "classes": classes,
            "routes": [],  # JS frameworks would need specific detection
            "complexity": len(functions) + len(classes) * 2,
        }