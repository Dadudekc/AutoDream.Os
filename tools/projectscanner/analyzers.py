"""
Project Scanner Language Analyzers
=================================

Language-specific analyzers for different programming languages.
"""

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
        """Initialize tree-sitter parser for given language."""
        if not Language or not Parser:
            logger.warning(
                "⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled."
            )
            return None

        grammar_paths = {
            "rust": "path/to/tree-sitter-rust.so",
            "javascript": "path/to/tree-sitter-javascript.so",
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

    def analyze_python_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze a Python file using AST parsing."""
        try:
            with open(file_path, encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source, filename=str(file_path))

            analysis = {
                "file": str(file_path),
                "language": "python",
                "lines": len(source.splitlines()),
                "classes": [],
                "functions": [],
                "imports": [],
                "complexity": 0,
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["classes"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "methods": len(
                                [n for n in node.body if isinstance(n, ast.FunctionDef)]
                            ),
                        }
                    )
                elif isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(
                        {"name": node.name, "line": node.lineno, "args": len(node.args.args)}
                    )
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            analysis["imports"].append(f"{module}.{alias.name}")

            # Calculate basic complexity
            analysis["complexity"] = len(analysis["classes"]) + len(analysis["functions"])

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing Python file {file_path}: {e}")
            return {"file": str(file_path), "language": "python", "error": str(e)}

    def analyze_rust_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze a Rust file using tree-sitter if available."""
        try:
            with open(file_path, encoding="utf-8") as f:
                source = f.read()

            analysis = {
                "file": str(file_path),
                "language": "rust",
                "lines": len(source.splitlines()),
                "functions": [],
                "structs": [],
                "impls": [],
                "complexity": 0,
            }

            if self.rust_parser:
                tree = self.rust_parser.parse(bytes(source, "utf8"))
                # Tree-sitter analysis would go here
                # For now, just basic line counting
                analysis["complexity"] = (
                    source.count("fn ") + source.count("struct ") + source.count("impl ")
                )
            else:
                # Fallback to basic text analysis
                analysis["functions"] = [{"name": "unknown", "line": 0}]
                analysis["complexity"] = source.count("fn ")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing Rust file {file_path}: {e}")
            return {"file": str(file_path), "language": "rust", "error": str(e)}

    def analyze_javascript_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze a JavaScript/TypeScript file using tree-sitter if available."""
        try:
            with open(file_path, encoding="utf-8") as f:
                source = f.read()

            analysis = {
                "file": str(file_path),
                "language": "javascript",
                "lines": len(source.splitlines()),
                "functions": [],
                "classes": [],
                "imports": [],
                "complexity": 0,
            }

            if self.js_parser:
                tree = self.js_parser.parse(bytes(source, "utf8"))
                # Tree-sitter analysis would go here
                # For now, just basic text analysis
                analysis["complexity"] = source.count("function ") + source.count("class ")
            else:
                # Fallback to basic text analysis
                analysis["functions"] = [{"name": "unknown", "line": 0}]
                analysis["complexity"] = source.count("function ")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing JavaScript file {file_path}: {e}")
            return {"file": str(file_path), "language": "javascript", "error": str(e)}

    def analyze_other_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze other file types with basic information."""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            return {
                "file": str(file_path),
                "language": "other",
                "lines": len(content.splitlines()),
                "size": len(content),
                "extension": file_path.suffix,
                "complexity": 0,
            }

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return {"file": str(file_path), "language": "other", "error": str(e)}
