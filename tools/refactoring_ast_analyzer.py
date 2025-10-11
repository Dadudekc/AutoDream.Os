#!/usr/bin/env python3
"""
Refactoring AST Analyzer - Code Structure Analysis
===================================================

AST-based analyzer for identifying code entities and categorization.
Extracted from refactoring_suggestion_engine.py for V2 compliance.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import ast
from pathlib import Path

try:
    from .refactoring_models import CodeEntity
except ImportError:
    from refactoring_models import CodeEntity


class ASTAnalyzer:
    """AST analyzer for code structure analysis."""

    def __init__(self):
        """Initialize AST analyzer."""
        self.entities: list[CodeEntity] = []

    def analyze_file(self, file_path: Path) -> list[CodeEntity]:
        """Analyze file and extract code entities."""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
            lines = content.split("\n")

            self.entities = []
            self._extract_entities(tree, lines)

            return self.entities

        except SyntaxError as e:
            print(f"❌ Syntax error in {file_path}: {e}")
            return []
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return []

    def _extract_entities(self, tree: ast.AST, lines: list[str]) -> None:
        """Extract entities from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._extract_class(node, lines)
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                self._extract_function(node, lines)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self._extract_import(node)

    def _extract_class(self, node: ast.ClassDef, lines: list[str]) -> None:
        """Extract class entity."""
        end_line = node.end_lineno if hasattr(node, "end_lineno") else node.lineno
        line_count = end_line - node.lineno + 1

        # Categorize class
        category = self._categorize_class(node, lines)

        entity = CodeEntity(
            entity_type="class",
            name=node.name,
            start_line=node.lineno,
            end_line=end_line,
            line_count=line_count,
            category=category,
        )

        self.entities.append(entity)

        # If class is large (>200 lines), extract methods as separate entities
        if line_count > 200:
            self._extract_class_methods(node, lines, node.name)

    def _extract_function(self, node: ast.FunctionDef, lines: list[str]) -> None:
        """Extract top-level function entity."""
        end_line = node.end_lineno if hasattr(node, "end_lineno") else node.lineno
        line_count = end_line - node.lineno + 1

        category = self._categorize_function(node, lines)

        entity = CodeEntity(
            entity_type="function",
            name=node.name,
            start_line=node.lineno,
            end_line=end_line,
            line_count=line_count,
            category=category,
        )

        self.entities.append(entity)

    def _extract_import(self, node) -> None:
        """Extract import entity."""
        entity = CodeEntity(
            entity_type="import",
            name="imports",
            start_line=node.lineno,
            end_line=node.lineno,
            line_count=1,
            category="import",
        )

        self.entities.append(entity)

    def _extract_class_methods(
        self, class_node: ast.ClassDef, lines: list[str], class_name: str
    ) -> None:
        """Extract methods from large classes as extractable entities."""
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                end_line = node.end_lineno if hasattr(node, "end_lineno") else node.lineno
                line_count = end_line - node.lineno + 1

                # Categorize method
                category = self._categorize_method(node, class_name)

                # Only add if method is substantial enough to extract
                if line_count >= 10:
                    entity = CodeEntity(
                        entity_type="method",
                        name=f"{class_name}.{node.name}",
                        start_line=node.lineno,
                        end_line=end_line,
                        line_count=line_count,
                        category=category,
                    )
                    self.entities.append(entity)

    def _categorize_method(self, node: ast.FunctionDef, class_name: str) -> str:
        """Categorize class method by purpose."""
        name_lower = node.name.lower()

        if name_lower.startswith("_") and not name_lower.startswith("__"):
            if "validate" in name_lower or "check" in name_lower:
                return "validation_helper"
            elif "format" in name_lower or "render" in name_lower:
                return "formatting_helper"
            elif "process" in name_lower or "handle" in name_lower:
                return "processing_helper"
            elif "create" in name_lower or "generate" in name_lower:
                return "factory_helper"
            else:
                return "helper"

        return "method"

    def _categorize_class(self, node: ast.ClassDef, lines: list[str]) -> str:
        """Categorize class by purpose."""
        name_lower = node.name.lower()

        # Check inheritance for categorization
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_name = base.id.lower()
                if "repository" in base_name or "repo" in base_name:
                    return "repository"
                elif "service" in base_name:
                    return "service"
                elif "manager" in base_name:
                    return "manager"
                elif "adapter" in base_name:
                    return "adapter"
                elif "enum" in base_name:
                    return "enum"

        # Check name patterns
        if "config" in name_lower:
            return "config"
        elif "model" in name_lower or node.name.endswith("Model"):
            return "model"
        elif "repository" in name_lower or "repo" in name_lower:
            return "repository"
        elif "service" in name_lower:
            return "service"
        elif "manager" in name_lower:
            return "manager"
        elif "adapter" in name_lower:
            return "adapter"
        elif "operations" in name_lower or "ops" in name_lower:
            return "operations"
        elif "coordinator" in name_lower:
            return "coordinator"
        elif "monitor" in name_lower:
            return "monitor"
        elif "handler" in name_lower:
            return "handler"

        # Check decorators
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                return "model"

        return "general"

    def _categorize_function(self, node: ast.FunctionDef, lines: list[str]) -> str:
        """Categorize function by purpose."""
        name_lower = node.name.lower()

        if name_lower.startswith("create_") or name_lower.startswith("make_"):
            return "factory"
        elif name_lower.startswith("get_") or name_lower.startswith("find_"):
            return "query"
        elif name_lower.startswith("validate_") or name_lower.startswith("check_"):
            return "validation"
        elif name_lower.startswith("format_") or name_lower.startswith("render_"):
            return "formatting"
        elif "helper" in name_lower or "util" in name_lower:
            return "utility"

        return "general"
