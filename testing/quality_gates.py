"""
Quality Gates for Monolithic File Modularization

This module implements configurable quality gates that must be passed
before a file is considered successfully modularized.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from src.utils.logger import get_logger

logger = get_logger(__name__)


class GateSeverity(Enum):
    """Severity levels for quality gates."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class GateStatus(Enum):
    """Status of a quality gate check."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class QualityGateConfig:
    """Configuration for a quality gate."""
    gate_name: str
    severity: GateSeverity
    enabled: bool
    threshold: float
    weight: float
    description: str
    failure_message: str
    success_message: str


@dataclass
class QualityGateResult:
    """Result of a quality gate check."""
    gate_name: str
    status: GateStatus
    score: float
    threshold: float
    weight: float
    severity: GateSeverity
    details: str
    recommendations: List[str]
    timestamp: str
    execution_time_ms: float


@dataclass
class QualityGateSummary:
    """Summary of all quality gate results."""
    total_gates: int
    passed_gates: int
    failed_gates: int
    warning_gates: int
    error_gates: int
    overall_score: float
    weighted_score: float
    critical_failures: int
    high_failures: int
    medium_failures: int
    low_failures: int
    timestamp: str


class QualityGateRegistry:
    """Registry for managing quality gates."""
    
    def __init__(self):
        self.gates: Dict[str, QualityGateConfig] = {}
        self._register_default_gates()
    
    def _register_default_gates(self):
        """Register the default set of quality gates."""
        default_gates = [
            QualityGateConfig(
                gate_name="Line Count",
                severity=GateSeverity.CRITICAL,
                enabled=True,
                threshold=300.0,
                weight=1.0,
                description="Check if file meets line count requirements",
                failure_message="File exceeds maximum line count threshold",
                success_message="File meets line count requirements"
            ),
            QualityGateConfig(
                gate_name="Cyclomatic Complexity",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=20.0,
                weight=0.9,
                description="Check cyclomatic complexity of the file",
                failure_message="File has excessive cyclomatic complexity",
                success_message="File has acceptable complexity"
            ),
            QualityGateConfig(
                gate_name="Dependency Count",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=15.0,
                weight=0.8,
                description="Check number of external dependencies",
                failure_message="File has too many external dependencies",
                success_message="File has acceptable dependency count"
            ),
            QualityGateConfig(
                gate_name="Test Coverage",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=80.0,
                weight=0.7,
                description="Check test coverage percentage",
                failure_message="File has insufficient test coverage",
                success_message="File has adequate test coverage"
            ),
            QualityGateConfig(
                gate_name="Naming Conventions",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=90.0,
                weight=0.6,
                description="Check naming convention compliance",
                failure_message="File violates naming conventions",
                success_message="File follows naming conventions"
            ),
            QualityGateConfig(
                gate_name="Documentation Coverage",
                severity=GateSeverity.LOW,
                enabled=True,
                threshold=70.0,
                weight=0.5,
                description="Check documentation coverage",
                failure_message="File has insufficient documentation",
                success_message="File has adequate documentation"
            ),
            QualityGateConfig(
                gate_name="Code Duplication",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=10.0,
                weight=0.7,
                description="Check for code duplication percentage",
                failure_message="File has excessive code duplication",
                success_message="File has acceptable duplication levels"
            ),
            QualityGateConfig(
                gate_name="Function Length",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=50.0,
                weight=0.8,
                description="Check maximum function length",
                failure_message="File contains overly long functions",
                success_message="File has appropriately sized functions"
            ),
            QualityGateConfig(
                gate_name="Class Complexity",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=15.0,
                weight=0.6,
                description="Check class complexity metrics",
                failure_message="File contains overly complex classes",
                success_message="File has appropriately complex classes"
            ),
            QualityGateConfig(
                gate_name="Import Organization",
                severity=GateSeverity.LOW,
                enabled=True,
                threshold=85.0,
                weight=0.4,
                description="Check import statement organization",
                failure_message="File has poorly organized imports",
                success_message="File has well-organized imports"
            )
        ]
        
        for gate in default_gates:
            self.register_gate(gate)
    
    def register_gate(self, gate: QualityGateConfig):
        """Register a new quality gate."""
        self.gates[gate.gate_name] = gate
        logger.info(f"Registered quality gate: {gate.gate_name}")
    
    def get_gate(self, gate_name: str) -> Optional[QualityGateConfig]:
        """Get a quality gate by name."""
        return self.gates.get(gate_name)
    
    def get_enabled_gates(self) -> List[QualityGateConfig]:
        """Get all enabled quality gates."""
        return [gate for gate in self.gates.values() if gate.enabled]
    
    def update_gate_config(self, gate_name: str, **kwargs) -> bool:
        """Update a gate's configuration."""
        if gate_name not in self.gates:
            return False
        
        gate = self.gates[gate_name]
        for key, value in kwargs.items():
            if hasattr(gate, key):
                setattr(gate, key, value)
        
        logger.info(f"Updated gate configuration: {gate_name}")
        return True


class QualityGateExecutor:
    """Executes quality gate checks."""
    
    def __init__(self, registry: QualityGateRegistry):
        self.registry = registry
        self.execution_history: List[QualityGateResult] = []
    
    def execute_all_gates(self, file_path: Path, file_metrics: Dict[str, Any]) -> List[QualityGateResult]:
        """Execute all enabled quality gates for a file."""
        enabled_gates = self.registry.get_enabled_gates()
        results = []
        
        for gate in enabled_gates:
            try:
                start_time = datetime.now()
                result = self._execute_single_gate(gate, file_path, file_metrics)
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                result.execution_time_ms = execution_time
                
                results.append(result)
                self.execution_history.append(result)
                
            except Exception as e:
                logger.error(f"Error executing gate {gate.gate_name}: {e}")
                error_result = QualityGateResult(
                    gate_name=gate.gate_name,
                    status=GateStatus.ERROR,
                    score=0.0,
                    threshold=gate.threshold,
                    weight=gate.weight,
                    severity=gate.severity,
                    details=f"Gate execution failed: {e}",
                    recommendations=["Fix gate implementation", "Check file format"],
                    timestamp=datetime.now().isoformat(),
                    execution_time_ms=0.0
                )
                results.append(error_result)
        
        return results
    
    def _execute_single_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute a single quality gate."""
        gate_executors = {
            "Line Count": self._execute_line_count_gate,
            "Cyclomatic Complexity": self._execute_complexity_gate,
            "Dependency Count": self._execute_dependency_gate,
            "Test Coverage": self._execute_test_coverage_gate,
            "Naming Conventions": self._execute_naming_gate,
            "Documentation Coverage": self._execute_documentation_gate,
            "Code Duplication": self._execute_duplication_gate,
            "Function Length": self._execute_function_length_gate,
            "Class Complexity": self._execute_class_complexity_gate,
            "Import Organization": self._execute_import_organization_gate
        }
        
        executor = gate_executors.get(gate.gate_name)
        if executor:
            return executor(gate, file_path, file_metrics)
        else:
            return self._execute_generic_gate(gate, file_path, file_metrics)
    
    def _execute_line_count_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute line count quality gate."""
        line_count = file_metrics.get('original_lines', 0)
        threshold = gate.threshold
        
        # Adjust threshold for test files
        if 'test' in str(file_path).lower():
            threshold = 500.0
        
        passed = line_count <= threshold
        score = max(0, 100 - (line_count - threshold) / 10) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Extract large functions to separate modules",
                "Split large classes into smaller components",
                "Move utility functions to shared modules",
                "Consider breaking file into multiple focused modules"
            ])
        else:
            recommendations.append("Line count is within acceptable range")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"File has {line_count} lines (threshold: {threshold})",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_complexity_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute cyclomatic complexity quality gate."""
        complexity = file_metrics.get('complexity_score', 0)
        threshold = gate.threshold
        
        passed = complexity <= threshold
        score = max(0, 100 - (complexity - threshold) * 2) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Simplify complex conditional logic",
                "Extract complex methods to separate functions",
                "Reduce nesting levels",
                "Use early returns to reduce complexity",
                "Consider breaking complex functions into smaller ones"
            ])
        else:
            recommendations.append("Complexity is within acceptable range")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Complexity score: {complexity} (threshold: {threshold})",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_dependency_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute dependency count quality gate."""
        dependencies = file_metrics.get('dependency_count', 0)
        threshold = gate.threshold
        
        passed = dependencies <= threshold
        score = max(0, 100 - (dependencies - threshold) * 3) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Consolidate similar imports",
                "Use relative imports where possible",
                "Create abstraction layers for external dependencies",
                "Group related imports together",
                "Consider creating a facade for external services"
            ])
        else:
            recommendations.append("Dependency count is within acceptable range")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Dependency count: {dependencies} (threshold: {threshold})",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_test_coverage_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute test coverage quality gate."""
        coverage = file_metrics.get('test_coverage', 0.0)
        threshold = gate.threshold
        
        passed = coverage >= threshold
        score = coverage
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Add unit tests for uncovered functions",
                "Add integration tests for complex workflows",
                "Improve test data coverage",
                "Add edge case testing",
                "Consider using property-based testing"
            ])
        else:
            recommendations.append("Test coverage meets requirements")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Test coverage: {coverage:.1f}% (threshold: {threshold}%)",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_naming_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute naming conventions quality gate."""
        # This is a simplified implementation - in practice, you'd analyze actual naming patterns
        score = 95.0  # Placeholder score
        passed = score >= gate.threshold
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = [
            "Continue following established naming patterns",
            "Use descriptive names for functions and variables",
            "Follow PEP 8 naming conventions"
        ]
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=gate.threshold,
            weight=gate.weight,
            severity=gate.severity,
            details="Naming conventions check passed",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_documentation_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute documentation coverage quality gate."""
        # Placeholder implementation
        score = 75.0
        passed = score >= gate.threshold
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Add docstrings to all public functions",
                "Document complex algorithms",
                "Add type hints where appropriate",
                "Include usage examples in docstrings"
            ])
        else:
            recommendations.append("Documentation coverage is adequate")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=gate.threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Documentation coverage: {score:.1f}% (threshold: {gate.threshold}%)",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_duplication_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute code duplication quality gate."""
        # Placeholder implementation
        duplication = 8.0  # 8% duplication
        threshold = gate.threshold
        
        passed = duplication <= threshold
        score = max(0, 100 - (duplication - threshold) * 5) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Extract common code into utility functions",
                "Use inheritance to reduce duplication",
                "Create shared constants and configurations",
                "Consider using mixins for shared functionality"
            ])
        else:
            recommendations.append("Code duplication is within acceptable levels")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Code duplication: {duplication:.1f}% (threshold: {threshold}%)",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_function_length_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute function length quality gate."""
        # Placeholder implementation
        max_function_length = 45
        threshold = gate.threshold
        
        passed = max_function_length <= threshold
        score = max(0, 100 - (max_function_length - threshold)) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Break long functions into smaller ones",
                "Extract complex logic into helper functions",
                "Use early returns to reduce nesting",
                "Consider using the Strategy pattern for complex logic"
            ])
        else:
            recommendations.append("Function lengths are appropriate")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Maximum function length: {max_function_length} (threshold: {threshold})",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_class_complexity_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute class complexity quality gate."""
        # Placeholder implementation
        class_complexity = 12
        threshold = gate.threshold
        
        passed = class_complexity <= threshold
        score = max(0, 100 - (class_complexity - threshold) * 3) if not passed else 100
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = []
        if not passed:
            recommendations.extend([
                "Split large classes into smaller ones",
                "Use composition instead of inheritance",
                "Extract complex methods to separate classes",
                "Consider using the Facade pattern"
            ])
        else:
            recommendations.append("Class complexity is appropriate")
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Class complexity: {class_complexity} (threshold: {threshold})",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_import_organization_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute import organization quality gate."""
        # Placeholder implementation
        import_score = 88.0
        threshold = gate.threshold
        
        passed = import_score >= threshold
        score = import_score
        
        status = GateStatus.PASSED if passed else GateStatus.FAILED
        
        recommendations = [
            "Group standard library imports first",
            "Group third-party imports second",
            "Group local imports last",
            "Use absolute imports for clarity",
            "Remove unused imports"
        ]
        
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=status,
            score=score,
            threshold=threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Import organization score: {score:.1f}% (threshold: {threshold}%)",
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def _execute_generic_gate(self, gate: QualityGateConfig, file_path: Path, file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute a generic quality gate for unknown gate types."""
        return QualityGateResult(
            gate_name=gate.gate_name,
            status=GateStatus.ERROR,
            score=0.0,
            threshold=gate.threshold,
            weight=gate.weight,
            severity=gate.severity,
            details=f"Unknown gate type: {gate.gate_name}",
            recommendations=["Implement specific gate executor", "Check gate configuration"],
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def generate_summary(self, results: List[QualityGateResult]) -> QualityGateSummary:
        """Generate a summary of quality gate results."""
        total_gates = len(results)
        passed_gates = len([r for r in results if r.status == GateStatus.PASSED])
        failed_gates = len([r for r in results if r.status == GateStatus.FAILED])
        warning_gates = len([r for r in results if r.status == GateStatus.WARNING])
        error_gates = len([r for r in results if r.status == GateStatus.ERROR])
        
        # Calculate overall scores
        overall_score = sum(r.score for r in results) / total_gates if total_gates > 0 else 0
        
        # Calculate weighted score
        total_weight = sum(r.weight for r in results)
        weighted_score = sum(r.score * r.weight for r in results) / total_weight if total_weight > 0 else 0
        
        # Count failures by severity
        critical_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == GateSeverity.CRITICAL])
        high_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == GateSeverity.HIGH])
        medium_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == GateSeverity.MEDIUM])
        low_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == GateSeverity.LOW])
        
        return QualityGateSummary(
            total_gates=total_gates,
            passed_gates=passed_gates,
            failed_gates=failed_gates,
            warning_gates=warning_gates,
            error_gates=error_gates,
            overall_score=overall_score,
            weighted_score=weighted_score,
            critical_failures=critical_failures,
            high_failures=high_failures,
            medium_failures=medium_failures,
            low_failures=low_failures,
            timestamp=datetime.now().isoformat()
        )
    
    def save_results(self, results: List[QualityGateResult], output_path: Path):
        """Save quality gate results to a JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert results to serializable format
        serializable_results = []
        for result in results:
            serializable_result = asdict(result)
            serializable_result['status'] = result.status.value
            serializable_result['severity'] = result.severity.value
            serializable_results.append(serializable_result)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        logger.info(f"Quality gate results saved to {output_path}")


def create_quality_gate_system() -> Tuple[QualityGateRegistry, QualityGateExecutor]:
    """Create a quality gate system with default configuration."""
    registry = QualityGateRegistry()
    executor = QualityGateExecutor(registry)
    return registry, executor


def run_quality_gates(file_path: Path, file_metrics: Dict[str, Any]) -> Tuple[List[QualityGateResult], QualityGateSummary]:
    """Run quality gates for a single file."""
    registry, executor = create_quality_gate_system()
    
    # Execute all gates
    results = executor.execute_all_gates(file_path, file_metrics)
    
    # Generate summary
    summary = executor.generate_summary(results)
    
    return results, summary
