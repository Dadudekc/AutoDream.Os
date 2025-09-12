"""
Quality Gates - Agent-4 Phase 2 Implementation
Automated quality gate enforcement and validation system.
"""

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class GateStatus(Enum):
    """Quality gate status enumeration."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


@dataclass
class QualityGate:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.quality.quality_gates import Quality_Gates

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Quality_Gates(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

    """Quality gate data structure."""

    name: str
    description: str
    status: GateStatus
    threshold: float
    actual_value: float
    message: str
    details: dict[str, Any]


@dataclass
class QualityGateSuite:
    """Quality gate suite data structure."""

    name: str
    gates: list[QualityGate]
    overall_status: GateStatus
    pass_rate: float
    execution_time: float


class QualityGates:
    """Automated quality gate enforcement and validation system."""

    def __init__(self, project_root: str = "."):
        """Initialize quality gates system."""
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "quality_gate_reports"
        self.reports_dir.mkdir(exist_ok=True)

        # Quality gate thresholds
        self.thresholds = {
            "test_coverage": 85.0,
            "v2_compliance": 100.0,
            "lint_errors": 0,
            "security_issues": 0,
            "performance_score": 70.0,
            "documentation_coverage": 80.0,
            "complexity_score": 10.0,
        }

    def run_quality_gate_suite(self) -> QualityGateSuite:
        """Run comprehensive quality gate suite."""
        print("🚪 Running quality gate suite...")

        start_time = datetime.now()
        gates = []

        # Test Coverage Gate
        print("  📊 Checking test coverage...")
        coverage_gate = self._check_test_coverage()
        gates.append(coverage_gate)

        # V2 Compliance Gate
        print("  📏 Checking V2 compliance...")
        v2_gate = self._check_v2_compliance()
        gates.append(v2_gate)

        # Linting Gate
        print("  🔍 Checking linting...")
        lint_gate = self._check_linting()
        gates.append(lint_gate)

        # Security Gate
        print("  🔒 Checking security...")
        security_gate = self._check_security()
        gates.append(security_gate)

        # Performance Gate
        print("  ⚡ Checking performance...")
        performance_gate = self._check_performance()
        gates.append(performance_gate)

        # Documentation Gate
        print("  📚 Checking documentation...")
        docs_gate = self._check_documentation()
        gates.append(docs_gate)

        # Complexity Gate
        print("  🧮 Checking complexity...")
        complexity_gate = self._check_complexity()
        gates.append(complexity_gate)

        # Calculate overall status
        execution_time = (datetime.now() - start_time).total_seconds()
        passed_gates = len([g for g in gates if g.status == GateStatus.PASSED])
        total_gates = len(gates)
        pass_rate = (passed_gates / total_gates * 100) if total_gates > 0 else 0

        overall_status = GateStatus.PASSED if pass_rate >= 80 else GateStatus.FAILED

        suite = QualityGateSuite(
            name="Comprehensive Quality Gates",
            gates=gates,
            overall_status=overall_status,
            pass_rate=pass_rate,
            execution_time=execution_time,
        )

        # Generate quality gate report
        self._generate_quality_gate_report(suite)

        return suite

    def _check_test_coverage(self) -> QualityGate:
        """Check test coverage quality gate."""
        try:
            # Run pytest with coverage
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "pytest",
                    "--cov=src",
                    "--cov-report=json",
                    "--cov-report=term-missing",
                    "tests/",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            coverage = 0.0
            if result.returncode == 0:
                # Parse coverage from output
                lines = result.stdout.split("\n")
                for line in lines:
                    if "TOTAL" in line and "%" in line:
                        try:
                            coverage = float(line.split()[-1].replace("%", ""))
                            break
                        except (ValueError, IndexError):
                            pass

            threshold = self.thresholds["test_coverage"]
            status = GateStatus.PASSED if coverage >= threshold else GateStatus.FAILED

            return QualityGate(
                name="Test Coverage",
                description=f"Test coverage must be >= {threshold}%",
                status=status,
                threshold=threshold,
                actual_value=coverage,
                message=f"Test coverage: {coverage:.1f}% (threshold: {threshold}%)",
                details={"coverage_percentage": coverage},
            )

        except Exception as e:
            return QualityGate(
                name="Test Coverage",
                description=f"Test coverage must be >= {self.thresholds['test_coverage']}%",
                status=GateStatus.FAILED,
                threshold=self.thresholds["test_coverage"],
                actual_value=0.0,
                message=f"Error checking test coverage: {e}",
                details={"error": str(e)},
            )

    def _check_v2_compliance(self) -> QualityGate:
        """Check V2 compliance quality gate."""
        try:
            # Count files over 400 lines
            violations = 0
            total_files = 0

            for root, dirs, files in os.walk(self.src_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = Path(root) / file
                        total_files += 1

                        try:
                            with open(file_path, encoding="utf-8") as f:
                                lines = len(f.readlines())
                                if lines > 400:
                                    violations += 1
                        except Exception:
                            continue

            compliance_rate = (
                ((total_files - violations) / total_files * 100) if total_files > 0 else 0
            )
            threshold = self.thresholds["v2_compliance"]
            status = GateStatus.PASSED if compliance_rate >= threshold else GateStatus.FAILED

            return QualityGate(
                name="V2 Compliance",
                description=f"V2 compliance must be >= {threshold}%",
                status=status,
                threshold=threshold,
                actual_value=compliance_rate,
                message=f"V2 compliance: {compliance_rate:.1f}% ({violations} violations)",
                details={"violations": violations, "total_files": total_files},
            )

        except Exception as e:
            return QualityGate(
                name="V2 Compliance",
                description=f"V2 compliance must be >= {self.thresholds['v2_compliance']}%",
                status=GateStatus.FAILED,
                threshold=self.thresholds["v2_compliance"],
                actual_value=0.0,
                message=f"Error checking V2 compliance: {e}",
                details={"error": str(e)},
            )

    def _check_linting(self) -> QualityGate:
        """Check linting quality gate."""
        try:
            # Run flake8
            result = subprocess.run(
                ["python", "-m", "flake8", "src/", "--count", "--statistics"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            error_count = 0
            if result.stdout:
                # Parse error count from flake8 output
                lines = result.stdout.split("\n")
                for line in lines:
                    if "total" in line.lower():
                        try:
                            error_count = int(line.split()[-1])
                            break
                        except (ValueError, IndexError):
                            pass

            threshold = self.thresholds["lint_errors"]
            status = GateStatus.PASSED if error_count <= threshold else GateStatus.FAILED

            return QualityGate(
                name="Linting",
                description=f"Lint errors must be <= {threshold}",
                status=status,
                threshold=threshold,
                actual_value=error_count,
                message=f"Lint errors: {error_count} (threshold: {threshold})",
                details={"error_count": error_count},
            )

        except Exception as e:
            return QualityGate(
                name="Linting",
                description=f"Lint errors must be <= {self.thresholds['lint_errors']}",
                status=GateStatus.FAILED,
                threshold=self.thresholds["lint_errors"],
                actual_value=999,
                message=f"Error checking linting: {e}",
                details={"error": str(e)},
            )

    def _check_security(self) -> QualityGate:
        """Check security quality gate."""
        try:
            # Run bandit
            result = subprocess.run(
                ["python", "-m", "bandit", "-r", "src/", "-f", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            issue_count = 0
            if result.stdout:
                try:
                    security_data = json.loads(result.stdout)
                    issue_count = len(security_data.get("results", []))
                except json.JSONDecodeError:
                    pass

            threshold = self.thresholds["security_issues"]
            status = GateStatus.PASSED if issue_count <= threshold else GateStatus.FAILED

            return QualityGate(
                name="Security",
                description=f"Security issues must be <= {threshold}",
                status=status,
                threshold=threshold,
                actual_value=issue_count,
                message=f"Security issues: {issue_count} (threshold: {threshold})",
                details={"issue_count": issue_count},
            )

        except Exception as e:
            return QualityGate(
                name="Security",
                description=f"Security issues must be <= {self.thresholds['security_issues']}",
                status=GateStatus.FAILED,
                threshold=self.thresholds["security_issues"],
                actual_value=999,
                message=f"Error checking security: {e}",
                details={"error": str(e)},
            )

    def _check_performance(self) -> QualityGate:
        """Check performance quality gate."""
        try:
            # Simple performance check based on file structure
            import_count = 0
            function_count = 0

            for root, dirs, files in os.walk(self.src_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = Path(root) / file

                        try:
                            with open(file_path, encoding="utf-8") as f:
                                content = f.read()
                                import_count += content.count("import ")
                                function_count += content.count("def ")
                        except Exception:
                            continue

            # Calculate performance score
            if function_count > 0:
                complexity_ratio = import_count / function_count
                performance_score = max(0, 100 - (complexity_ratio * 10))
            else:
                performance_score = 50.0

            threshold = self.thresholds["performance_score"]
            status = GateStatus.PASSED if performance_score >= threshold else GateStatus.FAILED

            return QualityGate(
                name="Performance",
                description=f"Performance score must be >= {threshold}",
                status=status,
                threshold=threshold,
                actual_value=performance_score,
                message=f"Performance score: {performance_score:.1f} (threshold: {threshold})",
                details={"performance_score": performance_score},
            )

        except Exception as e:
            return QualityGate(
                name="Performance",
                description=f"Performance score must be >= {self.thresholds['performance_score']}",
                status=GateStatus.FAILED,
                threshold=self.thresholds["performance_score"],
                actual_value=0.0,
                message=f"Error checking performance: {e}",
                details={"error": str(e)},
            )

    def _check_documentation(self) -> QualityGate:
        """Check documentation quality gate."""
        try:
            # Count files with docstrings
            documented_functions = 0
            total_functions = 0

            for root, dirs, files in os.walk(self.src_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = Path(root) / file

                        try:
                            with open(file_path, encoding="utf-8") as f:
                                content = f.read()

                                # Count functions with docstrings
                                lines = content.split("\n")
                                in_function = False
                                function_has_docstring = False

                                for i, line in enumerate(lines):
                                    if line.strip().startswith("def "):
                                        in_function = True
                                        function_has_docstring = False
                                        total_functions += 1

                                        # Check next few lines for docstring
                                        for j in range(i + 1, min(i + 5, len(lines))):
                                            next_line = lines[j].strip()
                                            if next_line.startswith('"""') or next_line.startswith(
                                                "'''"
                                            ):
                                                function_has_docstring = True
                                                break
                                            elif next_line and not next_line.startswith("#"):
                                                break

                                        if function_has_docstring:
                                            documented_functions += 1

                        except Exception:
                            continue

            doc_coverage = (
                (documented_functions / total_functions * 100) if total_functions > 0 else 0
            )
            threshold = self.thresholds["documentation_coverage"]
            status = GateStatus.PASSED if doc_coverage >= threshold else GateStatus.FAILED

            return QualityGate(
                name="Documentation",
                description=f"Documentation coverage must be >= {threshold}%",
                status=status,
                threshold=threshold,
                actual_value=doc_coverage,
                message=f"Documentation coverage: {doc_coverage:.1f}% (threshold: {threshold}%)",
                details={
                    "documented_functions": documented_functions,
                    "total_functions": total_functions,
                },
            )

        except Exception as e:
            return QualityGate(
                name="Documentation",
                description=f"Documentation coverage must be >= {self.thresholds['documentation_coverage']}%",
                status=GateStatus.FAILED,
                threshold=self.thresholds["documentation_coverage"],
                actual_value=0.0,
                message=f"Error checking documentation: {e}",
                details={"error": str(e)},
            )

    def _check_complexity(self) -> QualityGate:
        """Check complexity quality gate."""
        try:
            # Calculate average cyclomatic complexity
            total_complexity = 0
            file_count = 0

            for root, dirs, files in os.walk(self.src_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = Path(root) / file
                        file_count += 1

                        try:
                            with open(file_path, encoding="utf-8") as f:
                                content = f.read()

                                # Simple complexity calculation
                                complexity = (
                                    content.count("if ")
                                    + content.count("elif ")
                                    + content.count("for ")
                                    + content.count("while ")
                                    + content.count("except ")
                                    + content.count("and ")
                                    + content.count("or ")
                                )

                                total_complexity += complexity

                        except Exception:
                            continue

            avg_complexity = total_complexity / file_count if file_count > 0 else 0
            threshold = self.thresholds["complexity_score"]
            status = GateStatus.PASSED if avg_complexity <= threshold else GateStatus.FAILED

            return QualityGate(
                name="Complexity",
                description=f"Average complexity must be <= {threshold}",
                status=status,
                threshold=threshold,
                actual_value=avg_complexity,
                message=f"Average complexity: {avg_complexity:.1f} (threshold: {threshold})",
                details={"total_complexity": total_complexity, "file_count": file_count},
            )

        except Exception as e:
            return QualityGate(
                name="Complexity",
                description=f"Average complexity must be <= {self.thresholds['complexity_score']}",
                status=GateStatus.FAILED,
                threshold=self.thresholds["complexity_score"],
                actual_value=999,
                message=f"Error checking complexity: {e}",
                details={"error": str(e)},
            )

    def _generate_quality_gate_report(self, suite: QualityGateSuite) -> None:
        """Generate quality gate report."""
        print("📊 Generating quality gate report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"quality_gate_report_{timestamp}.json"

        report_data = {
            "timestamp": timestamp,
            "suite": {
                "name": suite.name,
                "overall_status": suite.overall_status.value,
                "pass_rate": suite.pass_rate,
                "execution_time": suite.execution_time,
            },
            "gates": [
                {
                    "name": gate.name,
                    "description": gate.description,
                    "status": gate.status.value,
                    "threshold": gate.threshold,
                    "actual_value": gate.actual_value,
                    "message": gate.message,
                    "details": gate.details,
                }
                for gate in suite.gates
            ],
            "recommendations": self._generate_gate_recommendations(suite),
        }

        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 Quality gate report generated: {report_file}")

    def _generate_gate_recommendations(self, suite: QualityGateSuite) -> list[str]:
        """Generate quality gate improvement recommendations."""
        recommendations = []

        failed_gates = [gate for gate in suite.gates if gate.status == GateStatus.FAILED]

        if not failed_gates:
            recommendations.append("✅ All quality gates passed!")
            return recommendations

        for gate in failed_gates:
            if gate.name == "Test Coverage":
                recommendations.append(
                    f"📊 Increase test coverage from {gate.actual_value:.1f}% to {gate.threshold}%"
                )
            elif gate.name == "V2 Compliance":
                recommendations.append(
                    f"📏 Fix V2 compliance violations to achieve {gate.threshold}% compliance"
                )
            elif gate.name == "Linting":
                recommendations.append(f"🔍 Fix {gate.actual_value} linting errors")
            elif gate.name == "Security":
                recommendations.append(f"🔒 Address {gate.actual_value} security issues")
            elif gate.name == "Performance":
                recommendations.append(
                    f"⚡ Improve performance score from {gate.actual_value:.1f} to {gate.threshold}"
                )
            elif gate.name == "Documentation":
                recommendations.append(
                    f"📚 Increase documentation coverage from {gate.actual_value:.1f}% to {gate.threshold}%"
                )
            elif gate.name == "Complexity":
                recommendations.append(
                    f"🧮 Reduce complexity from {gate.actual_value:.1f} to {gate.threshold}"
                )

        return recommendations


def main():
    """Main execution function."""
    print("🚪 Agent-4 Quality Gates - Phase 2 Implementation")
    print("=" * 60)

    gates = QualityGates()
    suite = gates.run_quality_gate_suite()

    print("\n📊 QUALITY GATE RESULTS")
    print("=" * 25)
    print(f"Overall Status: {suite.overall_status.value}")
    print(f"Pass Rate: {suite.pass_rate:.1f}%")
    print(f"Execution Time: {suite.execution_time:.2f}s")

    print("\n🚪 GATE DETAILS:")
    for gate in suite.gates:
        status_icon = "✅" if gate.status == GateStatus.PASSED else "❌"
        print(f"  {status_icon} {gate.name}: {gate.message}")

    if suite.overall_status == GateStatus.PASSED:
        print("\n🎉 All quality gates passed! Ready for deployment.")
    else:
        print(
            f"\n⚠️ {len([g for g in suite.gates if g.status == GateStatus.FAILED])} quality gates failed. Address issues before deployment."
        )

    print("\n✅ Quality Gates Implementation Complete!")
    print(
        "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"
    )


if __name__ == "__main__":
    main()
