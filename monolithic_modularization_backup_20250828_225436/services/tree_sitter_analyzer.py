#!/usr/bin/env python3
"""
Tree-Sitter Analyzer - Agent Cellphone V2
==========================================

Handles Rust and JavaScript/TypeScript analysis using tree-sitter.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Any, Optional

# Optional tree-sitter for Rust/JS/TS
try:
    from tree_sitter import Language, Parser
except ImportError:
    Language = None
    Parser = None

logger = logging.getLogger(__name__)


class TreeSitterAnalyzer:
    """Handles Rust and JavaScript/TypeScript analysis using tree-sitter."""

    def __init__(self):
        """Initialize tree-sitter parsers."""
        self.rust_parser = self._init_parser("rust")
        self.js_parser = self._init_parser("javascript")

    def _init_parser(self, lang_name: str) -> Optional[Parser]:
        """Initialize tree-sitter parser for specified language."""
        if not Language or not Parser:
            logger.warning("⚠️ tree-sitter not installed. Advanced parsing disabled.")
            return None

        grammar_paths = {
            "rust": "path/to/tree-sitter-rust.so",
            "javascript": "path/to/tree-sitter-javascript.so",
        }

        if lang_name not in grammar_paths:
            logger.warning(f"⚠️ No grammar path for {lang_name}")
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
            logger.error(f"⚠️ Failed to initialize {lang_name} parser: {e}")
            return None

    def analyze_rust(self, source_code: str) -> Dict[str, Any]:
        """Analyze Rust source code using tree-sitter."""
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
                                classes[impl_name].append(
                                    method_node.text.decode("utf-8")
                                )

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

    def analyze_javascript(self, source_code: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript using tree-sitter."""
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
                # Arrow functions
                for child in node.children:
                    if child.type == "variable_declarator":
                        name_node = child.child_by_field_name("name")
                        value_node = child.child_by_field_name("value")
                        if (
                            name_node
                            and value_node
                            and value_node.type == "arrow_function"
                        ):
                            functions.append(get_node_text(name_node))
            elif node.type == "call_expression":
                self._extract_js_routes(node, routes, get_node_text)

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

    def _extract_js_routes(self, node, routes: List[Dict], get_node_text):
        """Extract JavaScript/Express.js routes from call expressions."""
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
