#!/usr/bin/env python3
"""
Test Coverage Analysis - Agent Cellphone V2
==========================================

Analyzes test coverage for the repository and identifies components that need testing.
"""

import os
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class TestCoverageAnalyzer:
    """Analyzes test coverage for the repository"""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.src_dir = self.repo_root / "src"
        self.tests_dir = self.repo_root / "tests"

        # Track components and their test status
        self.components = {}
        self.tests = {}
        self.imports = defaultdict(set)
        self.test_coverage = {}

    def analyze_component(self, file_path: Path) -> Dict:
        """Analyze a single component file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse AST to find classes and functions
            tree = ast.parse(content)

            classes = []
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            # Count lines
            line_count = len(content.splitlines())

            return {
                "path": str(file_path.relative_to(self.repo_root)),
                "line_count": line_count,
                "classes": classes,
                "functions": functions,
                "complexity": self._assess_complexity(
                    line_count, len(classes), len(functions)
                ),
            }

        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.repo_root)),
                "error": str(e),
                "line_count": 0,
                "classes": [],
                "functions": [],
                "complexity": "UNKNOWN",
            }

    def _assess_complexity(self, lines: int, classes: int, functions: int) -> str:
        """Assess component complexity"""
        if lines > 500 or classes > 10 or functions > 20:
            return "HIGH"
        elif lines > 200 or classes > 5 or functions > 10:
            return "MEDIUM"
        else:
            return "LOW"

    def scan_components(self):
        """Scan all component files in src directory"""
        print("🔍 Scanning components...")

        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    file_path = Path(root) / file
                    component = self.analyze_component(file_path)
                    self.components[component["path"]] = component

        print(f"✅ Found {len(self.components)} components")

    def scan_tests(self):
        """Scan all test files"""
        print("🧪 Scanning tests...")

        for root, dirs, files in os.walk(self.tests_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    file_path = Path(root) / file
                    test_info = self._analyze_test_file(file_path)
                    self.tests[test_info["path"]] = test_info

        print(f"✅ Found {len(self.tests)} test files")

    def _analyze_test_file(self, file_path: Path) -> Dict:
        """Analyze a test file to find what it tests"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for import statements and test class/function names
            tree = ast.parse(content)

            imports = []
            test_classes = []
            test_functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
                elif isinstance(node, ast.ClassDef):
                    if node.name.startswith("Test") or "test" in node.name.lower():
                        test_classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    if node.name.startswith("test_"):
                        test_functions.append(node.name)

            return {
                "path": str(file_path.relative_to(self.repo_root)),
                "imports": imports,
                "test_classes": test_classes,
                "test_functions": test_functions,
                "test_count": len(test_functions),
            }

        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.repo_root)),
                "error": str(e),
                "imports": [],
                "test_classes": [],
                "test_functions": [],
                "test_count": 0,
            }

    def analyze_coverage(self):
        """Analyze test coverage for components"""
        print("📊 Analyzing test coverage...")

        for component_path, component in self.components.items():
            # Check if component has tests
            has_tests = self._component_has_tests(component_path)

            self.test_coverage[component_path] = {
                "component": component,
                "has_tests": has_tests,
                "test_files": self._find_test_files(component_path),
                "coverage_status": "TESTED" if has_tests else "UNTESTED",
            }

    def _component_has_tests(self, component_path: str) -> bool:
        """Check if a component has corresponding tests"""
        # Extract component name from path
        component_name = Path(component_path).stem

        # Look for test files that might test this component
        for test_path, test_info in self.tests.items():
            if component_name.lower() in test_path.lower():
                return True

            # Check imports in test file
            for import_name in test_info["imports"]:
                if component_name.lower() in import_name.lower():
                    return True

        return False

    def _find_test_files(self, component_path: str) -> List[str]:
        """Find test files that might test a component"""
        component_name = Path(component_path).stem
        test_files = []

        for test_path, test_info in self.tests.items():
            if component_name.lower() in test_path.lower():
                test_files.append(test_path)
            else:
                # Check imports
                for import_name in test_info["imports"]:
                    if component_name.lower() in import_name.lower():
                        test_files.append(test_path)
                        break

        return test_files

    def generate_report(self) -> str:
        """Generate comprehensive test coverage report"""
        report = []
        report.append("# Test Coverage Analysis Report")
        report.append("## Agent Cellphone V2 Repository")
        report.append("")

        # Summary statistics
        total_components = len(self.components)
        tested_components = sum(
            1 for coverage in self.test_coverage.values() if coverage["has_tests"]
        )
        untested_components = total_components - tested_components

        coverage_percentage = (
            (tested_components / total_components * 100) if total_components > 0 else 0
        )

        report.append("## 📊 Summary Statistics")
        report.append("")
        report.append(f"- **Total Components:** {total_components}")
        report.append(f"- **Tested Components:** {tested_components}")
        report.append(f"- **Untested Components:** {untested_components}")
        report.append(f"- **Test Coverage:** {coverage_percentage:.1f}%")
        report.append("")

        # Untested components by priority
        report.append("## 🚨 Untested Components (High Priority)")
        report.append("")

        high_priority = []
        medium_priority = []
        low_priority = []

        for component_path, coverage in self.test_coverage.items():
            if not coverage["has_tests"]:
                component = coverage["component"]
                priority = component.get("complexity", "UNKNOWN")

                if priority == "HIGH":
                    high_priority.append((component_path, component))
                elif priority == "MEDIUM":
                    medium_priority.append((component_path, component))
                else:
                    low_priority.append((component_path, component))

        # High priority components
        report.append("### 🔴 High Complexity (Critical)")
        for component_path, component in high_priority:
            report.append(f"- **{component_path}** ({component['line_count']} lines)")
            report.append(f"  - Classes: {len(component['classes'])}")
            report.append(f"  - Functions: {len(component['functions'])}")
            report.append("")

        # Medium priority components
        if medium_priority:
            report.append("### 🟡 Medium Complexity (High)")
            for component_path, component in medium_priority:
                report.append(
                    f"- **{component_path}** ({component['line_count']} lines)"
                )
                report.append(f"  - Classes: {len(component['classes'])}")
                report.append(f"  - Functions: {len(component['functions'])}")
                report.append("")

        # Low priority components
        if low_priority:
            report.append("### 🟢 Low Complexity (Medium)")
            for component_path, component in low_priority:
                report.append(
                    f"- **{component_path}** ({component['line_count']} lines)"
                )
                report.append(f"  - Classes: {len(component['classes'])}")
                report.append(f"  - Functions: {len(component['functions'])}")
                report.append("")

        # Test files summary
        report.append("## 🧪 Test Files Summary")
        report.append("")
        report.append(f"- **Total Test Files:** {len(self.tests)}")
        report.append(
            f"- **Total Test Functions:** {sum(test['test_count'] for test in self.tests.values())}"
        )
        report.append("")

        for test_path, test_info in self.tests.items():
            report.append(f"- **{test_path}**")
            report.append(f"  - Test Functions: {test_info['test_count']}")
            report.append(f"  - Test Classes: {len(test_info['test_classes'])}")
            report.append("")

        # Recommendations
        report.append("## 🎯 Recommendations")
        report.append("")
        report.append("### Immediate Actions (Priority 1)")
        report.append(
            f"1. **Create tests for {len(high_priority)} high-complexity components**"
        )
        report.append("   - These represent the highest risk if untested")
        report.append("   - Focus on core functionality and edge cases")
        report.append("")

        report.append("### Short-term Actions (Priority 2)")
        report.append(
            f"1. **Create tests for {len(medium_priority)} medium-complexity components**"
        )
        report.append("   - These represent moderate risk")
        report.append("   - Ensure basic functionality is covered")
        report.append("")

        report.append("### Long-term Actions (Priority 3)")
        report.append(
            f"1. **Create tests for {len(low_priority)} low-complexity components**"
        )
        report.append("   - These represent lower risk")
        report.append("   - Focus on integration and edge cases")
        report.append("")

        report.append("### Testing Strategy")
        report.append("1. **Use existing test patterns** from well-tested components")
        report.append("2. **Prioritize by complexity and risk**")
        report.append("3. **Implement integration tests** for critical workflows")
        report.append("4. **Set minimum coverage requirements** for new components")

        return "\n".join(report)

    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting Test Coverage Analysis")
        print("=" * 50)

        self.scan_components()
        self.scan_tests()
        self.analyze_coverage()

        # Generate and save report
        report = self.generate_report()
        report_file = self.repo_root / "TEST_COVERAGE_ANALYSIS_REPORT.md"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Analysis complete! Report saved to: {report_file}")

        # Print summary
        total_components = len(self.components)
        tested_components = sum(
            1 for coverage in self.test_coverage.values() if coverage["has_tests"]
        )
        coverage_percentage = (
            (tested_components / total_components * 100) if total_components > 0 else 0
        )

        print(f"\n📊 QUICK SUMMARY:")
        print(f"Components: {total_components}")
        print(f"Tested: {tested_components}")
        print(f"Untested: {total_components - tested_components}")
        print(f"Coverage: {coverage_percentage:.1f}%")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze test coverage for Agent Cellphone V2"
    )
    parser.add_argument("--repo-root", default=".", help="Repository root directory")

    args = parser.parse_args()

    analyzer = TestCoverageAnalyzer(args.repo_root)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
