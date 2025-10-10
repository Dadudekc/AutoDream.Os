#!/usr/bin/env python3
"""
Refactoring Suggestion Engine - Intelligent Quality Automation
===============================================================

AST-based analyzer that suggests split points and refactoring strategies
for V2 compliance violations. Provides actionable recommendations with
code snippets and impact estimates.

Features:
- AST analysis to identify logical split points
- Intelligent module extraction suggestions
- Class/function grouping recommendations
- Import statement generation
- Impact estimation and preview

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class CodeEntity:
    """Represents a code entity (class, function, etc.)."""

    entity_type: str  # "class", "function", "import", "constant"
    name: str
    start_line: int
    end_line: int
    line_count: int
    dependencies: List[str] = field(default_factory=list)
    complexity: int = 0
    category: str = "general"  # "model", "util", "service", "repository", etc.


@dataclass
class ModuleSuggestion:
    """Suggested module extraction."""

    module_name: str
    purpose: str
    entities: List[CodeEntity]
    estimated_lines: int
    priority: int  # 1=high, 2=medium, 3=low


@dataclass
class RefactoringSuggestion:
    """Complete refactoring suggestion for a file."""

    file_path: str
    violation_type: str
    current_lines: int
    target_lines: int
    suggested_modules: List[ModuleSuggestion]
    import_changes: List[str]
    estimated_main_file_lines: int
    estimated_total_lines: int  # Across all modules
    confidence: float  # 0.0 to 1.0
    reasoning: str


class ASTAnalyzer:
    """AST analyzer for code structure analysis."""

    def __init__(self):
        """Initialize AST analyzer."""
        self.entities: List[CodeEntity] = []

    def analyze_file(self, file_path: Path) -> List[CodeEntity]:
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

    def _extract_entities(self, tree: ast.AST, lines: List[str]) -> None:
        """Extract entities from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._extract_class(node, lines)
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                self._extract_function(node, lines)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self._extract_import(node)

    def _extract_class(self, node: ast.ClassDef, lines: List[str]) -> None:
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

    def _extract_function(self, node: ast.FunctionDef, lines: List[str]) -> None:
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

    def _extract_class_methods(self, class_node: ast.ClassDef, lines: List[str], class_name: str) -> None:
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

    def _categorize_class(self, node: ast.ClassDef, lines: List[str]) -> str:
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

    def _categorize_function(self, node: ast.FunctionDef, lines: List[str]) -> str:
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


class RefactoringSuggestionEngine:
    """Generates intelligent refactoring suggestions."""

    def __init__(self):
        """Initialize suggestion engine."""
        self.analyzer = ASTAnalyzer()

    def suggest_refactoring(
        self, file_path: str, current_lines: int, target_lines: int = 400
    ) -> Optional[RefactoringSuggestion]:
        """Generate refactoring suggestions for a file."""
        path = Path(file_path)
        if not path.exists():
            return None

        # Analyze file structure
        entities = self.analyzer.analyze_file(path)
        if not entities:
            return None

        # Group entities by category
        grouped = self._group_entities_by_category(entities)

        # Generate module suggestions
        suggested_modules = self._generate_module_suggestions(
            file_path, grouped, current_lines, target_lines
        )

        # Calculate estimates
        estimated_main = self._estimate_main_file_size(entities, suggested_modules)
        estimated_total = estimated_main + sum(m.estimated_lines for m in suggested_modules)

        # Generate import changes
        import_changes = self._generate_import_changes(file_path, suggested_modules)

        # Calculate confidence
        confidence = self._calculate_confidence(current_lines, estimated_main, target_lines)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            current_lines, estimated_main, suggested_modules, target_lines
        )

        return RefactoringSuggestion(
            file_path=file_path,
            violation_type="FILE_SIZE",
            current_lines=current_lines,
            target_lines=target_lines,
            suggested_modules=suggested_modules,
            import_changes=import_changes,
            estimated_main_file_lines=estimated_main,
            estimated_total_lines=estimated_total,
            confidence=confidence,
            reasoning=reasoning,
        )

    def _group_entities_by_category(
        self, entities: List[CodeEntity]
    ) -> Dict[str, List[CodeEntity]]:
        """Group entities by their category."""
        grouped: Dict[str, List[CodeEntity]] = {}

        for entity in entities:
            if entity.category not in grouped:
                grouped[entity.category] = []
            grouped[entity.category].append(entity)

        return grouped

    def _generate_module_suggestions(
        self,
        file_path: str,
        grouped: Dict[str, List[CodeEntity]],
        current_lines: int,
        target_lines: int,
    ) -> List[ModuleSuggestion]:
        """Generate module extraction suggestions."""
        suggestions = []
        base_name = Path(file_path).stem

        # Priority order for extraction
        extraction_priority = [
            ("model", "models", "Data models and entities", 1),
            ("config", "config", "Configuration classes", 1),
            ("enum", "enums", "Enumeration definitions", 2),
            ("repository", "repository", "Repository operations", 1),
            ("operations", "operations", "Operation handlers", 2),
            ("utility", "utils", "Utility functions", 2),
            ("factory", "factories", "Factory functions", 3),
            ("validation", "validators", "Validation logic", 2),
            ("formatting", "formatters", "Formatting functions", 3),
            ("validation_helper", "validation_helpers", "Validation helper methods", 2),
            ("formatting_helper", "formatting_helpers", "Formatting helper methods", 2),
            ("processing_helper", "processing_helpers", "Processing helper methods", 2),
            ("factory_helper", "factory_helpers", "Factory helper methods", 3),
            ("helper", "helpers", "Helper methods", 3),
        ]

        for category, suffix, purpose, priority in extraction_priority:
            if category in grouped and grouped[category]:
                entities = grouped[category]
                total_lines = sum(e.line_count for e in entities)

                # Only suggest extraction if it's meaningful
                if total_lines >= 30:  # Minimum size to justify extraction
                    module_name = f"{base_name}_{suffix}.py"

                    suggestion = ModuleSuggestion(
                        module_name=module_name,
                        purpose=purpose,
                        entities=entities,
                        estimated_lines=total_lines + 20,  # Add overhead for imports/docs
                        priority=priority,
                    )

                    suggestions.append(suggestion)

        # Sort by priority
        suggestions.sort(key=lambda x: x.priority)

        return suggestions

    def _estimate_main_file_size(
        self, all_entities: List[CodeEntity], suggested_modules: List[ModuleSuggestion]
    ) -> int:
        """Estimate main file size after extraction."""
        extracted_entities = set()
        extracted_lines = 0
        
        for module in suggested_modules:
            for entity in module.entities:
                extracted_entities.add(entity.name)
                extracted_lines += entity.line_count

        # Get total current lines (including non-entity lines like comments, docstrings)
        # Estimate non-entity lines as ~20% of file
        entity_lines = sum(e.line_count for e in all_entities if e.entity_type != "import")
        
        # Calculate total file lines from largest entity end line
        max_line = max((e.end_line for e in all_entities), default=0)
        total_file_lines = max_line

        # Remaining = total - extracted + import overhead
        import_overhead = 20 + (len(suggested_modules) * 2)  # Header + imports
        remaining_lines = total_file_lines - extracted_lines + import_overhead

        return max(remaining_lines, 50)  # Minimum 50 lines for basic structure

    def _generate_import_changes(
        self, file_path: str, modules: List[ModuleSuggestion]
    ) -> List[str]:
        """Generate import statements for suggested modules."""
        imports = []
        base_dir = Path(file_path).parent.name

        for module in modules:
            # Generate relative import
            module_base = module.module_name.replace(".py", "")
            entity_names = [e.name for e in module.entities[:5]]  # First 5 entities

            if len(entity_names) <= 3:
                import_stmt = f"from .{module_base} import {', '.join(entity_names)}"
            else:
                import_stmt = f"from .{module_base} import ("
                for name in entity_names:
                    import_stmt += f"\n    {name},"
                import_stmt += "\n)"

            imports.append(import_stmt)

        return imports

    def _calculate_confidence(
        self, current: int, estimated_main: int, target: int
    ) -> float:
        """Calculate confidence score for suggestion."""
        if estimated_main <= target:
            # Will achieve compliance
            margin = target - estimated_main
            confidence = min(1.0, 0.7 + (margin / target) * 0.3)
        else:
            # Won't fully achieve compliance
            improvement = current - estimated_main
            confidence = max(0.3, (improvement / current) * 0.7)

        return round(confidence, 2)

    def _generate_reasoning(
        self,
        current: int,
        estimated_main: int,
        modules: List[ModuleSuggestion],
        target: int,
    ) -> str:
        """Generate human-readable reasoning for suggestions."""
        lines = []

        reduction = current - estimated_main
        reduction_pct = (reduction / current * 100) if current > 0 else 0

        lines.append(f"Current file: {current} lines (target: ≤{target} lines)")
        lines.append(
            f"Suggested extraction: {len(modules)} modules ({reduction} lines, {reduction_pct:.0f}% reduction)"
        )
        lines.append(f"Estimated main file: {estimated_main} lines")

        if estimated_main <= target:
            lines.append(f"✅ Result: V2 COMPLIANT (within {target - estimated_main} lines of limit)")
        else:
            lines.append(
                f"⚠️ Result: Still {estimated_main - target} lines over (may need additional refactoring)"
            )

        lines.append("\nSuggested modules:")
        for i, module in enumerate(modules, 1):
            entity_count = len(module.entities)
            lines.append(
                f"{i}. {module.module_name} ({module.estimated_lines} lines, {entity_count} entities)"
            )
            lines.append(f"   Purpose: {module.purpose}")
            entity_preview = ", ".join([e.name for e in module.entities[:3]])
            if len(module.entities) > 3:
                entity_preview += f", ... (+{len(module.entities) - 3} more)"
            lines.append(f"   Contains: {entity_preview}")

        return "\n".join(lines)

    def format_suggestion(self, suggestion: RefactoringSuggestion, detailed: bool = True) -> str:
        """Format refactoring suggestion as readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append(f"REFACTORING SUGGESTION: {Path(suggestion.file_path).name}")
        lines.append("=" * 80)
        lines.append(f"Violation: {suggestion.violation_type}")
        lines.append(
            f"Current: {suggestion.current_lines} lines → Target: ≤{suggestion.target_lines} lines"
        )
        lines.append(f"Confidence: {suggestion.confidence * 100:.0f}%")
        lines.append("")
        lines.append("REASONING:")
        lines.append(suggestion.reasoning)
        lines.append("")

        if detailed and suggestion.suggested_modules:
            lines.append("SUGGESTED IMPLEMENTATION:")
            lines.append("")

            for i, module in enumerate(suggestion.suggested_modules, 1):
                lines.append(f"{i}. CREATE: {module.module_name}")
                lines.append(f"   Purpose: {module.purpose}")
                lines.append(f"   Estimated size: {module.estimated_lines} lines")
                lines.append(f"   Entities to extract ({len(module.entities)}):")

                for entity in module.entities:
                    lines.append(
                        f"      - {entity.entity_type.title()} '{entity.name}' ({entity.line_count} lines, lines {entity.start_line}-{entity.end_line})"
                    )

                lines.append("")

            lines.append("IMPORT CHANGES:")
            lines.append("Add to main file:")
            for import_stmt in suggestion.import_changes:
                lines.append(f"  {import_stmt}")
            lines.append("")

            lines.append("ESTIMATED RESULT:")
            lines.append(
                f"  - Main file: {suggestion.estimated_main_file_lines} lines"
            )
            lines.append(
                f"  - Total (all modules): {suggestion.estimated_total_lines} lines"
            )
            lines.append(
                f"  - V2 Compliant: {'✅ YES' if suggestion.estimated_main_file_lines <= suggestion.target_lines else '⚠️  NO (needs more refactoring)'}"
            )

        lines.append("=" * 80)

        return "\n".join(lines)


class RefactoringSuggestionService:
    """Main service for refactoring suggestions."""

    def __init__(self):
        """Initialize refactoring suggestion service."""
        self.engine = RefactoringSuggestionEngine()

    def analyze_and_suggest(self, file_path: str) -> Optional[RefactoringSuggestion]:
        """Analyze file and generate suggestions."""
        path = Path(file_path)

        # Check file size
        if not path.exists():
            return None

        content = path.read_text(encoding="utf-8")
        current_lines = len(content.split("\n"))

        # Only suggest if violation exists
        if current_lines <= 400:
            return None

        # Generate suggestions
        return self.engine.suggest_refactoring(file_path, current_lines)

    def analyze_directory(
        self, directory: str, pattern: str = "**/*.py"
    ) -> List[RefactoringSuggestion]:
        """Analyze directory and generate suggestions for all violations."""
        suggestions = []
        dir_path = Path(directory)

        for file_path in dir_path.glob(pattern):
            if self._should_skip_file(file_path):
                continue

            suggestion = self.analyze_and_suggest(str(file_path))
            if suggestion:
                suggestions.append(suggestion)

        # Sort by current line count (worst first)
        suggestions.sort(key=lambda x: x.current_lines, reverse=True)

        return suggestions

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            "__pycache__",
            ".venv",
            "venv",
            "env",
            ".git",
            "migrations",
            ".pytest_cache",
        ]

        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Refactoring Suggestion Engine - Intelligent Quality Automation"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to analyze (default: current directory)",
    )
    parser.add_argument(
        "--pattern", default="**/*.py", help="File pattern for directory scan"
    )
    parser.add_argument(
        "--detailed", "-d", action="store_true", help="Show detailed suggestions"
    )
    parser.add_argument(
        "--limit", "-l", type=int, default=10, help="Limit number of suggestions shown"
    )

    args = parser.parse_args()

    service = RefactoringSuggestionService()
    path = Path(args.path)

    if path.is_file():
        # Analyze single file
        suggestion = service.analyze_and_suggest(str(path))
        if suggestion:
            print(service.engine.format_suggestion(suggestion, args.detailed))
        else:
            print(f"✅ {path.name} is V2 compliant or couldn't be analyzed")

    elif path.is_dir():
        # Analyze directory
        suggestions = service.analyze_directory(str(path), args.pattern)

        if not suggestions:
            print(f"✅ All files in {path} are V2 compliant!")
        else:
            print(f"\nFound {len(suggestions)} files requiring refactoring:")
            print("")

            for i, suggestion in enumerate(suggestions[: args.limit], 1):
                print(f"\n{'=' * 80}")
                print(f"#{i}: {Path(suggestion.file_path).name}")
                print(f"{'=' * 80}")
                print(service.engine.format_suggestion(suggestion, args.detailed))

            if len(suggestions) > args.limit:
                print(f"\n... and {len(suggestions) - args.limit} more files")

    else:
        print(f"❌ Path not found: {path}")


if __name__ == "__main__":
    main()

