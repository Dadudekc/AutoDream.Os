#!/usr/bin/env python3
"""
VSCode Quality Gates - V2 Compliant
===================================

Quality gates specifically for VSCode customization and extension development.
Ensures V2 compliance and VSCode-specific quality standards.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class VSCodeQualityResult:
    """VSCode quality assessment result."""

    file_path: str
    score: int
    quality_level: str
    violations: list[str]
    vscode_specific_issues: list[str]
    recommendations: list[str]


class VSCodeQualityGates:
    """VSCode-specific quality gates."""

    def __init__(self):
        self.v2_limits = {
            "max_lines": 400,
            "max_enums": 3,
            "max_classes": 5,
            "max_functions": 10,
            "max_parameters": 5,
            "max_complexity": 10,
            "max_inheritance": 2,
        }

        self.vscode_standards = {
            "required_imports": ["typing", "dataclasses", "enum"],
            "forbidden_patterns": ["asyncio", "threading", "multiprocessing"],
            "required_patterns": ["type_hints", "docstrings", "error_handling"],
        }

    def check_file(self, file_path: str) -> VSCodeQualityResult:
        """Check VSCode file quality."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Basic metrics
            line_count = len(content.splitlines())
            enums = len(
                [
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef) and self._is_enum_class(node)
                ]
            )
            classes = len(
                [
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ClassDef) and not self._is_enum_class(node)
                ]
            )
            functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])

            # Check violations
            violations = self._check_v2_violations(line_count, enums, classes, functions, tree)
            vscode_issues = self._check_vscode_issues(content, tree)
            recommendations = self._generate_recommendations(violations, vscode_issues)

            # Calculate score
            score = self._calculate_score(
                line_count, enums, classes, functions, len(violations), len(vscode_issues)
            )
            quality_level = self._get_quality_level(score)

            return VSCodeQualityResult(
                file_path=file_path,
                score=score,
                quality_level=quality_level,
                violations=violations,
                vscode_specific_issues=vscode_issues,
                recommendations=recommendations,
            )

        except Exception as e:
            return VSCodeQualityResult(
                file_path=file_path,
                score=0,
                quality_level="CRITICAL",
                violations=[f"Error parsing file: {str(e)}"],
                vscode_specific_issues=[],
                recommendations=["Fix syntax errors before quality assessment"],
            )

    def _is_enum_class(self, node: ast.ClassDef) -> bool:
        """Check if class is an enum."""
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "Enum":
                return True
        return False

    def _check_v2_violations(
        self, line_count: int, enums: int, classes: int, functions: int, tree: ast.AST
    ) -> list[str]:
        """Check V2 compliance violations."""
        violations = []

        if line_count > self.v2_limits["max_lines"]:
            violations.append(
                f"File size violation: {line_count} lines (limit: {self.v2_limits['max_lines']})"
            )

        if enums > self.v2_limits["max_enums"]:
            violations.append(f"Too many enums: {enums} (limit: {self.v2_limits['max_enums']})")

        if classes > self.v2_limits["max_classes"]:
            violations.append(
                f"Too many classes: {classes} (limit: {self.v2_limits['max_classes']})"
            )

        if functions > self.v2_limits["max_functions"]:
            violations.append(
                f"Too many functions: {functions} (limit: {self.v2_limits['max_functions']})"
            )

        # Check function complexity and parameters
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > self.v2_limits["max_parameters"]:
                    violations.append(
                        f"Too many parameters in {node.name}: {len(node.args.args)} (limit: {self.v2_limits['max_parameters']})"
                    )

                complexity = self._calculate_complexity(node)
                if complexity > self.v2_limits["max_complexity"]:
                    violations.append(
                        f"Function {node.name} too complex: {complexity} (limit: {self.v2_limits['max_complexity']})"
                    )

        return violations

    def _check_vscode_issues(self, content: str, tree: ast.AST) -> list[str]:
        """Check VSCode-specific quality issues."""
        issues = []

        # Check for forbidden patterns
        for pattern in self.vscode_standards["forbidden_patterns"]:
            if pattern in content:
                issues.append(f"Forbidden pattern found: {pattern}")

        # Check for required patterns
        if "typing" not in content:
            issues.append("Missing typing imports")

        if "dataclasses" not in content:
            issues.append("Missing dataclasses import")

        # Check for proper error handling
        has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))
        if not has_try_except:
            issues.append("No error handling found")

        # Check for docstrings
        has_docstrings = any(
            ast.get_docstring(node)
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        )
        if not has_docstrings:
            issues.append("Missing docstrings")

        return issues

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _generate_recommendations(
        self, violations: list[str], vscode_issues: list[str]
    ) -> list[str]:
        """Generate improvement recommendations."""
        recommendations = []

        if any("File size violation" in v for v in violations):
            recommendations.append("Split large file into smaller modules")

        if any("Too many functions" in v for v in violations):
            recommendations.append("Extract functions into separate modules")

        if any("Too many classes" in v for v in violations):
            recommendations.append("Split classes into focused modules")

        if any("Forbidden pattern" in i for i in vscode_issues):
            recommendations.append(
                "Remove forbidden patterns and use VSCode-compatible alternatives"
            )

        if any("Missing" in i for i in vscode_issues):
            recommendations.append("Add missing imports and documentation")

        return recommendations

    def _calculate_score(
        self,
        line_count: int,
        enums: int,
        classes: int,
        functions: int,
        violation_count: int,
        issue_count: int,
    ) -> int:
        """Calculate quality score."""
        base_score = 100

        # Deduct for violations
        base_score -= violation_count * 10

        # Deduct for VSCode issues
        base_score -= issue_count * 5

        # Bonus for good practices
        if line_count <= 200:
            base_score += 10
        if enums <= 2:
            base_score += 5
        if classes <= 3:
            base_score += 5
        if functions <= 5:
            base_score += 10

        return max(0, min(100, base_score))

    def _get_quality_level(self, score: int) -> str:
        """Get quality level based on score."""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 80:
            return "GOOD"
        elif score >= 70:
            return "ACCEPTABLE"
        elif score >= 60:
            return "POOR"
        else:
            return "CRITICAL"

    def check_directory(self, directory: str) -> list[VSCodeQualityResult]:
        """Check all Python files in directory."""
        results = []
        directory_path = Path(directory)

        for file_path in directory_path.rglob("*.py"):
            if file_path.is_file():
                result = self.check_file(str(file_path))
                results.append(result)

        return results

    def generate_report(self, results: list[VSCodeQualityResult]) -> dict[str, Any]:
        """Generate quality report."""
        if not results:
            return {"error": "No files to analyze"}

        total_files = len(results)
        excellent = sum(1 for r in results if r.quality_level == "EXCELLENT")
        good = sum(1 for r in results if r.quality_level == "GOOD")
        acceptable = sum(1 for r in results if r.quality_level == "ACCEPTABLE")
        poor = sum(1 for r in results if r.quality_level == "POOR")
        critical = sum(1 for r in results if r.quality_level == "CRITICAL")

        avg_score = sum(r.score for r in results) / total_files

        return {
            "total_files": total_files,
            "quality_distribution": {
                "excellent": excellent,
                "good": good,
                "acceptable": acceptable,
                "poor": poor,
                "critical": critical,
            },
            "average_score": round(avg_score, 2),
            "v2_compliant_files": sum(1 for r in results if not r.violations),
            "vscode_ready_files": sum(1 for r in results if not r.vscode_specific_issues),
            "files": [
                {
                    "file": r.file_path,
                    "score": r.score,
                    "quality": r.quality_level,
                    "violations": len(r.violations),
                    "issues": len(r.vscode_specific_issues),
                }
                for r in results
            ],
        }


def main():
    """Main execution function."""
    print("🎨 VSCode Quality Gates - Testing...")

    # Initialize quality gates
    gates = VSCodeQualityGates()

    # Check VSCode customization files
    results = gates.check_directory("src/team_beta")

    # Generate report
    report = gates.generate_report(results)

    print("\n📊 VSCode Quality Report:")
    print(f"   Total Files: {report['total_files']}")
    print(f"   Average Score: {report['average_score']}")
    print(f"   V2 Compliant: {report['v2_compliant_files']}/{report['total_files']}")
    print(f"   VSCode Ready: {report['vscode_ready_files']}/{report['total_files']}")

    print("\n📈 Quality Distribution:")
    for level, count in report["quality_distribution"].items():
        print(f"   {level.upper()}: {count}")

    print("\n✅ VSCode Quality Gates completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
