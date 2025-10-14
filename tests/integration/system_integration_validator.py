#!/usr/bin/env python3
"""
System Integration Validator - C-048-5
======================================

Comprehensive integration validation suite for Agent Cellphone V2.
Validates imports, dependencies, circular dependencies, and system health.

Author: Agent-2 - Architecture & Design Specialist
Date: 2025-10-12
License: MIT
"""

import ast
import json
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation check."""

    module_path: str
    status: str  # "PASS", "FAIL", "WARNING"
    message: str
    details: dict = field(default_factory=dict)


@dataclass
class IntegrationHealthReport:
    """Comprehensive integration health report."""

    total_modules: int = 0
    importable_modules: int = 0
    failed_imports: list[ValidationResult] = field(default_factory=list)
    circular_dependencies: list[tuple[str, str]] = field(default_factory=list)
    missing_dependencies: list[ValidationResult] = field(default_factory=list)
    warnings: list[ValidationResult] = field(default_factory=list)
    success_rate: float = 0.0


class SystemIntegrationValidator:
    """Comprehensive system integration validation."""

    def __init__(self, project_root: Path = None):
        """Initialize validator with project root."""
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.results: list[ValidationResult] = []
        self.dependency_graph: dict[str, set[str]] = defaultdict(set)

    def validate_imports(self, file_pattern: str = "**/*.py") -> list[ValidationResult]:
        """
        Validate all Python imports in the project.

        Args:
            file_pattern: Glob pattern for files to validate

        Returns:
            List of validation results
        """
        logger.info("🔍 Validating imports...")
        import_results = []

        python_files = list(self.project_root.glob(file_pattern))
        # Filter out venv, node_modules, .git
        python_files = [
            f
            for f in python_files
            if not any(x in f.parts for x in ["venv", "node_modules", ".git", "__pycache__"])
        ]

        total = len(python_files)
        passed = 0

        for py_file in python_files:
            try:
                # Try to compile the file
                with open(py_file, encoding="utf-8") as f:
                    code = f.read()
                    compile(code, str(py_file), "exec")

                # Extract imports for dependency graph
                imports = self._extract_imports(code)
                rel_path = str(py_file.relative_to(self.project_root))
                self.dependency_graph[rel_path] = imports

                result = ValidationResult(
                    module_path=rel_path, status="PASS", message="Import validation passed"
                )
                passed += 1

            except SyntaxError as e:
                result = ValidationResult(
                    module_path=str(py_file.relative_to(self.project_root)),
                    status="FAIL",
                    message=f"Syntax error: {e}",
                    details={"line": e.lineno, "error": str(e)},
                )
            except Exception as e:
                result = ValidationResult(
                    module_path=str(py_file.relative_to(self.project_root)),
                    status="FAIL",
                    message=f"Validation error: {e}",
                )

            import_results.append(result)

        logger.info(f"✅ Import validation: {passed}/{total} passed ({passed/total*100:.1f}%)")
        return import_results

    def _extract_imports(self, code: str) -> set[str]:
        """Extract import statements from Python code."""
        imports = set()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
        except:
            pass
        return imports

    def detect_circular_dependencies(self) -> list[tuple[str, str]]:
        """
        Detect circular dependencies in the dependency graph.

        Returns:
            List of circular dependency pairs
        """
        logger.info("🔄 Detecting circular dependencies...")
        circular_deps = []

        visited = set()
        rec_stack = set()

        def dfs(module: str, path: list[str]):
            visited.add(module)
            rec_stack.add(module)

            for dep in self.dependency_graph.get(module, []):
                # Try to find the module in our codebase
                dep_path = self._resolve_module_path(dep)

                if dep_path and dep_path in rec_stack:
                    circular_deps.append((module, dep_path))
                elif dep_path and dep_path not in visited:
                    dfs(dep_path, path + [module])

            rec_stack.remove(module)

        for module in self.dependency_graph:
            if module not in visited:
                dfs(module, [])

        logger.info(f"🔄 Found {len(circular_deps)} circular dependencies")
        return circular_deps

    def _resolve_module_path(self, module_name: str) -> str:
        """Resolve module name to file path."""
        # Simple resolution: convert module name to path
        if module_name.startswith("src."):
            path = module_name.replace(".", "/") + ".py"
            if (self.project_root / path).exists():
                return path
        return ""

    def check_missing_dependencies(self) -> list[ValidationResult]:
        """
        Check for missing dependencies (imports that don't exist).

        Returns:
            List of validation results for missing dependencies
        """
        logger.info("📦 Checking for missing dependencies...")
        missing_deps = []

        for module, imports in self.dependency_graph.items():
            for imp in imports:
                # Check if it's a local import
                if imp.startswith("src.") or imp.startswith("tests."):
                    resolved = self._resolve_module_path(imp)
                    if not resolved:
                        missing_deps.append(
                            ValidationResult(
                                module_path=module,
                                status="WARNING",
                                message=f"Potentially missing local import: {imp}",
                                details={"import": imp},
                            )
                        )

        logger.info(f"📦 Found {len(missing_deps)} potential missing dependencies")
        return missing_deps

    def generate_health_report(self) -> IntegrationHealthReport:
        """
        Generate comprehensive integration health report.

        Returns:
            IntegrationHealthReport with all metrics
        """
        logger.info("📊 Generating integration health report...")

        # Run all validations
        import_results = self.validate_imports()
        circular_deps = self.detect_circular_dependencies()
        missing_deps = self.check_missing_dependencies()

        # Calculate metrics
        total_modules = len(import_results)
        passed_imports = sum(1 for r in import_results if r.status == "PASS")
        failed_imports = [r for r in import_results if r.status == "FAIL"]
        warnings = [r for r in import_results if r.status == "WARNING"] + missing_deps

        success_rate = (passed_imports / total_modules * 100) if total_modules > 0 else 0

        report = IntegrationHealthReport(
            total_modules=total_modules,
            importable_modules=passed_imports,
            failed_imports=failed_imports,
            circular_dependencies=circular_deps,
            missing_dependencies=missing_deps,
            warnings=warnings,
            success_rate=success_rate,
        )

        return report

    def save_report(self, report: IntegrationHealthReport, output_path: Path):
        """Save health report to file."""
        report_dict = {
            "total_modules": report.total_modules,
            "importable_modules": report.importable_modules,
            "success_rate": f"{report.success_rate:.2f}%",
            "failed_imports_count": len(report.failed_imports),
            "circular_dependencies_count": len(report.circular_dependencies),
            "missing_dependencies_count": len(report.missing_dependencies),
            "warnings_count": len(report.warnings),
            "failed_imports": [
                {"module": r.module_path, "message": r.message, "details": r.details}
                for r in report.failed_imports
            ],
            "circular_dependencies": [
                {"from": src, "to": dst} for src, dst in report.circular_dependencies
            ],
            "missing_dependencies": [
                {"module": r.module_path, "import": r.details.get("import", "")}
                for r in report.missing_dependencies
            ],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report_dict, f, indent=2)

        logger.info(f"📄 Report saved to: {output_path}")

    def print_summary(self, report: IntegrationHealthReport):
        """Print human-readable summary."""
        print("\n" + "=" * 70)
        print("🏥 SYSTEM INTEGRATION HEALTH REPORT")
        print("=" * 70)
        print("\n📊 Overall Metrics:")
        print(f"  Total Modules: {report.total_modules}")
        print(f"  Importable Modules: {report.importable_modules}")
        print(f"  Success Rate: {report.success_rate:.2f}%")
        print(f"\n❌ Failed Imports: {len(report.failed_imports)}")
        print(f"🔄 Circular Dependencies: {len(report.circular_dependencies)}")
        print(f"📦 Missing Dependencies: {len(report.missing_dependencies)}")
        print(f"⚠️  Warnings: {len(report.warnings)}")

        if report.failed_imports:
            print("\n❌ Failed Import Details:")
            for result in report.failed_imports[:10]:  # Show first 10
                print(f"  • {result.module_path}: {result.message}")

        if report.circular_dependencies:
            print("\n🔄 Circular Dependency Details:")
            for src, dst in report.circular_dependencies[:10]:  # Show first 10
                print(f"  • {src} ↔ {dst}")

        print("\n" + "=" * 70)


def main():
    """Main entry point for C-048-5 validation."""
    print("🚀 Starting System Integration Validation (C-048-5)")
    print("Agent-2 - Architecture & Design Specialist\n")

    # Initialize validator
    validator = SystemIntegrationValidator()

    # Generate health report
    report = validator.generate_health_report()

    # Print summary
    validator.print_summary(report)

    # Save detailed report
    output_path = Path("tests/integration/integration_health_report.json")
    validator.save_report(report, output_path)

    print(f"\n✅ Validation complete! Detailed report: {output_path}")

    # Return exit code based on success
    return 0 if report.success_rate >= 95 else 1


if __name__ == "__main__":
    sys.exit(main())
