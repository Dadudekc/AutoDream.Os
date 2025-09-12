"""
V2 Compliance Executor - Agent-4 Phase 2 Implementation
Automated V2 compliance enforcement and file modularization system.
"""

import ast
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class V2Violation:
    """V2 compliance violation data structure."""

    file_path: str
    current_lines: int
    excess_lines: int
    violation_type: str
    priority: str
    recommendations: list[str]


@dataclass
class ModularizationPlan:
    """File modularization plan data structure."""

    original_file: str
    target_files: list[str]
    line_reduction: int
    complexity_score: float
    dependencies: list[str]


class V2ComplianceExecutor:
    """Automated V2 compliance enforcement and file modularization system."""

    def __init__(self, project_root: str = "."):
        """Initialize V2 compliance executor."""
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.reports_dir = self.project_root / "v2_compliance_reports"
        self.reports_dir.mkdir(exist_ok=True)

        # V2 compliance limits
        self.max_lines = 400
        self.max_functions = 20
        self.max_classes = 10

    def execute_v2_compliance_audit(self) -> dict[str, V2Violation]:
        """Execute comprehensive V2 compliance audit."""
        print("🔍 Running V2 compliance audit...")

        violations = {}

        # Scan all Python files in src directory
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    violation = self._analyze_file_compliance(file_path)

                    if violation:
                        violations[str(file_path)] = violation

        # Generate compliance report
        self._generate_compliance_report(violations)

        return violations

    def _analyze_file_compliance(self, file_path: Path) -> V2Violation | None:
        """Analyze individual file for V2 compliance violations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                line_count = len(lines)

            # Check line count violation
            if line_count > self.max_lines:
                excess_lines = line_count - self.max_lines

                # Analyze file structure for modularization recommendations
                recommendations = self._analyze_modularization_opportunities(file_path, content)

                return V2Violation(
                    file_path=str(file_path),
                    current_lines=line_count,
                    excess_lines=excess_lines,
                    violation_type="LINE_COUNT_EXCEEDED",
                    priority="HIGH" if excess_lines > 200 else "MEDIUM",
                    recommendations=recommendations,
                )

            return None

        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")
            return None

    def _analyze_modularization_opportunities(self, file_path: Path, content: str) -> list[str]:
        """Analyze file for modularization opportunities."""
        recommendations = []

        try:
            # Parse AST to understand file structure
            tree = ast.parse(content)

            # Count functions and classes
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            # Analyze function complexity
            complex_functions = []
            for func in functions:
                func_lines = self._count_function_lines(func, content)
                if func_lines > 50:  # Functions over 50 lines
                    complex_functions.append(func.name)

            # Generate recommendations based on analysis
            if len(functions) > 15:
                recommendations.append(
                    f"Split into multiple modules - {len(functions)} functions found"
                )

            if len(classes) > 5:
                recommendations.append(
                    f"Separate classes into individual modules - {len(classes)} classes found"
                )

            if complex_functions:
                recommendations.append(
                    f"Extract complex functions: {', '.join(complex_functions[:3])}"
                )

            # Look for logical groupings
            imports = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
            ]
            if len(imports) > 20:
                recommendations.append("Consider splitting based on import dependencies")

            # Look for configuration vs logic separation
            config_functions = [
                f.name
                for f in functions
                if "config" in f.name.lower() or "setting" in f.name.lower()
            ]
            if config_functions:
                recommendations.append(
                    f"Extract configuration functions: {', '.join(config_functions)}"
                )

            # Look for utility vs business logic separation
            util_functions = [
                f.name for f in functions if "util" in f.name.lower() or "helper" in f.name.lower()
            ]
            if util_functions:
                recommendations.append(f"Extract utility functions: {', '.join(util_functions)}")

        except Exception as e:
            print(f"⚠️ Error analyzing modularization opportunities for {file_path}: {e}")
            recommendations.append("Manual analysis required - AST parsing failed")

        return recommendations

    def _count_function_lines(self, func_node: ast.FunctionDef, content: str) -> int:
        """Count lines in a function."""
        lines = content.split("\n")
        start_line = func_node.lineno - 1
        end_line = func_node.end_lineno if hasattr(func_node, "end_lineno") else start_line + 1

        # Count non-empty lines
        func_lines = lines[start_line:end_line]
        return len([line for line in func_lines if line.strip()])

    def execute_automated_modularization(
        self, violations: dict[str, V2Violation]
    ) -> dict[str, ModularizationPlan]:
        """Execute automated modularization for V2 compliance violations."""
        print("🔧 Executing automated modularization...")

        modularization_plans = {}

        for file_path, violation in violations.items():
            if violation.priority == "HIGH":
                print(f"📝 Creating modularization plan for {file_path}")
                plan = self._create_modularization_plan(file_path, violation)
                if plan:
                    modularization_plans[file_path] = plan

        # Generate modularization report
        self._generate_modularization_report(modularization_plans)

        return modularization_plans

    def _create_modularization_plan(
        self, file_path: str, violation: V2Violation
    ) -> ModularizationPlan | None:
        """Create modularization plan for a file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse file structure
            tree = ast.parse(content)

            # Identify logical modules
            modules = self._identify_logical_modules(tree, content)

            if not modules:
                return None

            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(tree, content)

            # Identify dependencies
            dependencies = self._identify_dependencies(tree)

            # Create target file names
            base_name = Path(file_path).stem
            target_files = [f"{base_name}_{module['name']}.py" for module in modules]

            return ModularizationPlan(
                original_file=file_path,
                target_files=target_files,
                line_reduction=violation.excess_lines,
                complexity_score=complexity_score,
                dependencies=dependencies,
            )

        except Exception as e:
            print(f"⚠️ Error creating modularization plan for {file_path}: {e}")
            return None

    def _identify_logical_modules(self, tree: ast.AST, content: str) -> list[dict]:
        """Identify logical modules within a file."""
        modules = []

        # Group functions by common prefixes
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        function_groups = {}

        for func in functions:
            # Extract module prefix from function name
            if "_" in func.name:
                prefix = func.name.split("_")[0]
                if prefix not in function_groups:
                    function_groups[prefix] = []
                function_groups[prefix].append(func.name)

        # Create modules from function groups
        for prefix, func_names in function_groups.items():
            if len(func_names) >= 3:  # Only create modules with 3+ functions
                modules.append({"name": prefix, "functions": func_names, "type": "function_group"})

        # Group classes
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        if len(classes) >= 2:
            modules.append(
                {"name": "models", "classes": [cls.name for cls in classes], "type": "class_group"}
            )

        # Group configuration-related code
        config_functions = [
            f for f in functions if "config" in f.name.lower() or "setting" in f.name.lower()
        ]
        if config_functions:
            modules.append(
                {
                    "name": "config",
                    "functions": [f.name for f in config_functions],
                    "type": "config_group",
                }
            )

        return modules

    def _calculate_complexity_score(self, tree: ast.AST, content: str) -> float:
        """Calculate complexity score for a file."""
        lines = content.split("\n")
        total_lines = len(lines)

        # Count various complexity indicators
        function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        import_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
            ]
        )

        # Calculate complexity score (0-100)
        complexity = (
            (function_count * 2) + (class_count * 5) + (import_count * 1) + (total_lines * 0.1)
        )

        return min(100.0, complexity)

    def _identify_dependencies(self, tree: ast.AST) -> list[str]:
        """Identify file dependencies."""
        dependencies = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencies.append(node.module)

        return list(set(dependencies))

    def _generate_compliance_report(self, violations: dict[str, V2Violation]) -> None:
        """Generate V2 compliance report."""
        print("📊 Generating V2 compliance report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"v2_compliance_report_{timestamp}.json"

        # Calculate summary statistics
        total_violations = len(violations)
        high_priority = len([v for v in violations.values() if v.priority == "HIGH"])
        medium_priority = len([v for v in violations.values() if v.priority == "MEDIUM"])
        total_excess_lines = sum(v.excess_lines for v in violations.values())

        report_data = {
            "timestamp": timestamp,
            "summary": {
                "total_violations": total_violations,
                "high_priority": high_priority,
                "medium_priority": medium_priority,
                "total_excess_lines": total_excess_lines,
            },
            "violations": {
                file_path: {
                    "current_lines": violation.current_lines,
                    "excess_lines": violation.excess_lines,
                    "violation_type": violation.violation_type,
                    "priority": violation.priority,
                    "recommendations": violation.recommendations,
                }
                for file_path, violation in violations.items()
            },
            "recommendations": self._generate_compliance_recommendations(violations),
        }

        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 V2 compliance report generated: {report_file}")

    def _generate_modularization_report(self, plans: dict[str, ModularizationPlan]) -> None:
        """Generate modularization report."""
        print("📊 Generating modularization report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"modularization_report_{timestamp}.json"

        report_data = {
            "timestamp": timestamp,
            "plans": {
                file_path: {
                    "target_files": plan.target_files,
                    "line_reduction": plan.line_reduction,
                    "complexity_score": plan.complexity_score,
                    "dependencies": plan.dependencies,
                }
                for file_path, plan in plans.items()
            },
            "summary": {
                "total_plans": len(plans),
                "total_line_reduction": sum(plan.line_reduction for plan in plans.values()),
                "avg_complexity": (
                    sum(plan.complexity_score for plan in plans.values()) / len(plans)
                    if plans
                    else 0
                ),
            },
        }

        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 Modularization report generated: {report_file}")

    def _generate_compliance_recommendations(self, violations: dict[str, V2Violation]) -> list[str]:
        """Generate compliance improvement recommendations."""
        recommendations = []

        if not violations:
            recommendations.append("✅ All files are V2 compliant!")
            return recommendations

        high_priority_count = len([v for v in violations.values() if v.priority == "HIGH"])
        if high_priority_count > 0:
            recommendations.append(
                f"🚨 Address {high_priority_count} high-priority violations immediately"
            )

        total_excess = sum(v.excess_lines for v in violations.values())
        if total_excess > 1000:
            recommendations.append(
                f"📏 Significant line reduction needed: {total_excess} excess lines"
            )

        # Group by violation type
        violation_types = {}
        for violation in violations.values():
            if violation.violation_type not in violation_types:
                violation_types[violation.violation_type] = 0
            violation_types[violation.violation_type] += 1

        for vtype, count in violation_types.items():
            recommendations.append(f"🔧 {vtype}: {count} files need attention")

        return recommendations


def main():
    """Main execution function."""
    print("🔧 Agent-4 V2 Compliance Executor - Phase 2 Implementation")
    print("=" * 60)

    executor = V2ComplianceExecutor()

    # Run compliance audit
    violations = executor.execute_v2_compliance_audit()

    print("\n📊 V2 COMPLIANCE AUDIT RESULTS")
    print("=" * 35)
    print(f"Total Violations: {len(violations)}")

    if violations:
        high_priority = len([v for v in violations.values() if v.priority == "HIGH"])
        medium_priority = len([v for v in violations.values() if v.priority == "MEDIUM"])
        total_excess = sum(v.excess_lines for v in violations.values())

        print(f"High Priority: {high_priority}")
        print(f"Medium Priority: {medium_priority}")
        print(f"Total Excess Lines: {total_excess}")

        print("\n🚨 VIOLATIONS FOUND:")
        for file_path, violation in list(violations.items())[:5]:  # Show first 5
            print(f"  {file_path}: {violation.current_lines} lines (+{violation.excess_lines})")

        if len(violations) > 5:
            print(f"  ... and {len(violations) - 5} more")

        # Execute modularization for high-priority violations
        modularization_plans = executor.execute_automated_modularization(violations)

        print(f"\n🔧 MODULARIZATION PLANS CREATED: {len(modularization_plans)}")
        for file_path, plan in modularization_plans.items():
            print(f"  {file_path} → {len(plan.target_files)} modules")
    else:
        print("✅ All files are V2 compliant!")

    print("\n✅ V2 Compliance Executor Implementation Complete!")
    print(
        "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"
    )


if __name__ == "__main__":
    main()
