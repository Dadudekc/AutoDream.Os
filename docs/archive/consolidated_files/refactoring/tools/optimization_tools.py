"""
Refactoring Optimization Tools - V2 Compliance Module
====================================================

Optimization functionality for refactoring tools.

V2 Compliance: < 300 lines, single responsibility, optimization tools.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import pathlib
from dataclasses import dataclass


@dataclass
class OptimizationPlan:
    """Plan for optimizing code structure."""

    optimization_targets: list[str]
    optimization_rules: list[str]
    performance_improvements: list[str]
    v2_compliance_improvements: list[str]


class OptimizationTools:
    """Optimization tools for refactoring."""

    def __init__(self):
        """Initialize optimization tools."""
        # Use standard pathlib instead of unified import system
        self.path_class = pathlib.Path

    def create_optimization_plan(self, file_path: str) -> OptimizationPlan:
        """Create an optimization plan for a file."""
        try:
            # Analyze file for optimization opportunities
            source_path = self.path_class(file_path)
            source_content = source_path.read_text(encoding="utf-8")

            optimization_targets = self._identify_optimization_targets(source_content)
            optimization_rules = self._generate_optimization_rules(source_content)
            performance_improvements = self._identify_performance_improvements(source_content)
            v2_compliance_improvements = self._identify_v2_compliance_improvements(source_content)

            return OptimizationPlan(
                optimization_targets=optimization_targets,
                optimization_rules=optimization_rules,
                performance_improvements=performance_improvements,
                v2_compliance_improvements=v2_compliance_improvements,
            )
        except Exception:
            return OptimizationPlan(
                optimization_targets=[],
                optimization_rules=[],
                performance_improvements=[],
                v2_compliance_improvements=[],
            )

    def execute_optimization(self, plan: OptimizationPlan, file_path: str) -> bool:
        """Execute optimization plan."""
        try:
            source_path = self.path_class(file_path)
            source_content = source_path.read_text(encoding="utf-8")

            # Apply optimizations
            optimized_content = self._apply_optimizations(source_content, plan)

            # Write optimized content
            source_path.write_text(optimized_content, encoding="utf-8")

            return True
        except Exception:
            return False

    def _identify_optimization_targets(self, content: str) -> list[str]:
        """Identify optimization targets in content."""
        targets = []

        lines = content.split("\n")
        for i, line in enumerate(lines):
            if len(line) > 100:  # Long lines
                targets.append(f"Line {i + 1}: Long line ({len(line)} chars)")
            elif line.strip().startswith("#"):  # Comment lines
                targets.append(f"Line {i + 1}: Comment line")
            elif "import" in line and "," in line:  # Multiple imports
                targets.append(f"Line {i + 1}: Multiple imports")

        return targets[:10]  # Limit to 10 targets

    def _generate_optimization_rules(self, content: str) -> list[str]:
        """Generate optimization rules based on content."""
        rules = []

        if len(content.split("\n")) > 300:
            rules.append("Split large file into smaller modules")

        if content.count("class ") > 5:
            rules.append("Extract classes into separate modules")

        if content.count("def ") > 10:
            rules.append("Extract functions into utility modules")

        if content.count("import ") > 20:
            rules.append("Consolidate import statements")

        return rules

    def _identify_performance_improvements(self, content: str) -> list[str]:
        """Identify performance improvement opportunities."""
        improvements = []

        if "for " in content and "range(" in content:
            improvements.append("Consider using list comprehensions")

        if "if " in content and "else" in content:
            improvements.append("Consider using ternary operators")

        if "try:" in content and "except:" in content:
            improvements.append("Optimize exception handling")

        return improvements

    def _identify_v2_compliance_improvements(self, content: str) -> list[str]:
        """Identify V2 compliance improvement opportunities."""
        improvements = []

        lines = content.split("\n")
        if len(lines) > 300:
            improvements.append("Reduce file size to under 300 lines")

        if content.count("class ") > 3:
            improvements.append("Extract classes to separate modules")

        if content.count("def ") > 8:
            improvements.append("Extract functions to utility modules")

        return improvements

    def _apply_optimizations(self, content: str, plan: OptimizationPlan) -> str:
        """Apply optimizations to content."""
        optimized_content = content
        lines = content.split("\n")

        # Apply structural optimizations
        for rule in plan.optimization_rules:
            if "Split large file" in rule:
                # Add file split markers for large files
                optimized_content = self._apply_file_splitting(optimized_content, lines)
            elif "Extract classes" in rule:
                optimized_content = self._apply_class_extraction(optimized_content, lines)
            elif "Extract functions" in rule:
                optimized_content = self._apply_function_extraction(optimized_content, lines)
            elif "Consolidate import" in rule:
                optimized_content = self._apply_import_consolidation(optimized_content, lines)

        # Apply performance optimizations
        for improvement in plan.performance_improvements:
            if "list comprehensions" in improvement:
                optimized_content = self._apply_list_comprehension_optimization(
                    optimized_content, lines
                )
            elif "ternary operators" in improvement:
                optimized_content = self._apply_ternary_operator_optimization(
                    optimized_content, lines
                )
            elif "exception handling" in improvement:
                optimized_content = self._apply_exception_handling_optimization(
                    optimized_content, lines
                )

        # Apply V2 compliance improvements
        for improvement in plan.v2_compliance_improvements:
            if "reduce file size" in improvement:
                optimized_content = self._apply_file_size_reduction(optimized_content, lines)
            elif "extract classes" in improvement:
                optimized_content = self._apply_class_extraction(optimized_content, lines)
            elif "extract functions" in improvement:
                optimized_content = self._apply_function_extraction(optimized_content, lines)

        return optimized_content

    def _apply_file_splitting(self, content: str, lines: list[str]) -> str:
        """Apply file splitting optimizations."""
        # Add section markers for better organization
        sections = []

        # Find class definitions
        class_indices = []
        for i, line in enumerate(lines):
            if line.strip().startswith("class "):
                class_indices.append(i)

        # Find function definitions
        function_indices = []
        for i, line in enumerate(lines):
            if line.strip().startswith("def ") and not line.strip().startswith("    "):
                function_indices.append(i)

        # Add section markers
        if class_indices:
            sections.append(f"# Classes ({len(class_indices)} found)")
        if function_indices:
            sections.append(f"# Functions ({len(function_indices)} found)")

        if sections:
            content = "\n".join(sections) + "\n\n" + content

        return content

    def _apply_class_extraction(self, content: str, lines: list[str]) -> str:
        """Apply class extraction optimizations."""
        # Add comments suggesting class extractions
        class_count = sum(1 for line in lines if line.strip().startswith("class "))
        if class_count > 3:
            content = f"# OPTIMIZATION: Consider extracting {class_count} classes into separate modules\n{content}"
        return content

    def _apply_function_extraction(self, content: str, lines: list[str]) -> str:
        """Apply function extraction optimizations."""
        # Add comments suggesting function extractions
        function_count = sum(
            1
            for line in lines
            if line.strip().startswith("def ") and not line.strip().startswith("    ")
        )
        if function_count > 8:
            content = f"# OPTIMIZATION: Consider extracting {function_count} functions into utility modules\n{content}"
        return content

    def _apply_import_consolidation(self, content: str, lines: list[str]) -> str:
        """Apply import consolidation optimizations."""
        # Group and optimize imports
        import_lines = []
        other_lines = []

        for line in lines:
            if line.strip().startswith("import ") or line.strip().startswith("from "):
                import_lines.append(line)
            else:
                other_lines.append(line)

        if len(import_lines) > 10:
            # Add consolidation suggestion
            import_lines.insert(
                0, "# OPTIMIZATION: Consider consolidating imports into __init__.py"
            )

        return "\n".join(import_lines + [""] + other_lines)

    def _apply_list_comprehension_optimization(self, content: str, lines: list[str]) -> str:
        """Apply list comprehension optimizations."""
        # Look for for loops that could be list comprehensions
        optimized_lines = []
        for line in lines:
            # Simple pattern: for x in list: result.append(func(x))
            if "for " in line and "append(" in line:
                optimized_lines.append(
                    f"# OPTIMIZATION: Consider converting to list comprehension: {line.strip()}"
                )
            optimized_lines.append(line)

        return "\n".join(optimized_lines)

    def _apply_ternary_operator_optimization(self, content: str, lines: list[str]) -> str:
        """Apply ternary operator optimizations."""
        # Look for simple if-else assignments that could use ternary
        optimized_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith("if ") and i + 2 < len(lines):
                next_line = lines[i + 1].strip()
                if "else:" in next_line and i + 3 < len(lines):
                    then_line = lines[i + 2].strip()
                    else_line = lines[i + 4].strip() if i + 4 < len(lines) else ""
                    if "=" in then_line and "=" in else_line:
                        optimized_lines.append(
                            f"# OPTIMIZATION: Consider ternary operator for: {line.strip()}"
                        )
            optimized_lines.append(line)

        return "\n".join(optimized_lines)

    def _apply_exception_handling_optimization(self, content: str, lines: list[str]) -> str:
        """Apply exception handling optimizations."""
        # Look for bare except clauses
        optimized_lines = []
        for line in lines:
            if line.strip() == "except:" or line.strip().startswith("except:"):
                optimized_lines.append(
                    f"# OPTIMIZATION: Specify exception types instead of bare except: {line.strip()}"
                )
            optimized_lines.append(line)

        return "\n".join(optimized_lines)

    def _apply_file_size_reduction(self, content: str, lines: list[str]) -> str:
        """Apply file size reduction optimizations."""
        if len(lines) > 300:
            content = f"# OPTIMIZATION: File has {len(lines)} lines - consider splitting into smaller modules\n{content}"
        return content
