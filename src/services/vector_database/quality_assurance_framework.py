"""
Quality Assurance Framework - V2 Compliant (Simplified)
======================================================

Core quality assurance with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class QualityGate(Enum):
    """Quality gate enumeration."""

    ARCHITECTURE = "architecture"
    TESTING = "testing"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"


class QualityLevel(Enum):
    """Quality level enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXCELLENT = "excellent"


@dataclass
class QualityMetric:
    """Quality metric structure."""

    gate: QualityGate
    name: str
    value: float
    threshold: float
    level: QualityLevel
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class QualityResult:
    """Quality result structure."""

    gate: QualityGate
    passed: bool
    score: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)


class QualityChecker:
    """Core quality checker."""

    def __init__(self):
        self._metrics: dict[str, QualityMetric] = {}
        self._results: list[QualityResult] = []
        self._lock = threading.Lock()

    def add_metric(
        self, gate: QualityGate, name: str, value: float, threshold: float, level: QualityLevel
    ) -> None:
        """Add a quality metric."""
        with self._lock:
            metric = QualityMetric(
                gate=gate, name=name, value=value, threshold=threshold, level=level
            )
            self._metrics.append(metric)

    def update_metric(self, gate: QualityGate, name: str, value: float) -> None:
        """Update a quality metric."""
        with self._lock:
            for metric in self._metrics:
                if metric.gate == gate and metric.name == name:
                    metric.value = value
                    break

    def get_metric(self, gate: QualityGate, name: str) -> QualityMetric | None:
        """Get a quality metric."""
        with self._lock:
            for metric in self._metrics:
                if metric.gate == gate and metric.name == name:
                    return metric
            return None

    def get_metrics_by_gate(self, gate: QualityGate) -> dict[str, QualityMetric]:
        """Get metrics by gate."""
        with self._lock:
            return {metric.name: metric for metric in self._metrics if metric.gate == gate}

    def check_quality_gate(self, gate: QualityGate) -> QualityResult:
        """Check a quality gate."""
        with self._lock:
            gate_metrics = self.get_metrics_by_gate(gate)
            if not gate_metrics:
                result = QualityResult(
                    gate=gate,
                    passed=False,
                    score=0.0,
                    message=f"No metrics found for gate: {gate.value}",
                )
                self._results.append(result)
                return result

            total_score = 0.0
            passed_metrics = 0
            total_metrics = len(gate_metrics)

            for metric in gate_metrics.values():
                if metric.value >= metric.threshold:
                    passed_metrics += 1
                    total_score += metric.value

            average_score = total_score / total_metrics if total_metrics > 0 else 0.0
            passed = passed_metrics >= (total_metrics * 0.8)  # 80% threshold

            result = QualityResult(
                gate=gate,
                passed=passed,
                score=average_score,
                message=f"Gate {gate.value}: {passed_metrics}/{total_metrics} metrics passed",
            )

            self._results.append(result)
            logger.info(f"Quality gate checked: {gate.value} - {'PASSED' if passed else 'FAILED'}")
            return result

    def get_quality_results(self) -> list[QualityResult]:
        """Get all quality results."""
        return self._results.copy()

    def get_failed_gates(self) -> list[QualityGate]:
        """Get failed quality gates."""
        return [result.gate for result in self._results if not result.passed]


class QualityManager:
    """Quality management system."""

    def __init__(self):
        self._checker = QualityChecker()
        self._enabled = True

    def enable(self) -> None:
        """Enable quality management."""
        self._enabled = True
        logger.info("Quality management enabled")

    def disable(self) -> None:
        """Disable quality management."""
        self._enabled = False
        logger.info("Quality management disabled")

    def is_enabled(self) -> bool:
        """Check if quality management is enabled."""
        return self._enabled

    def get_checker(self) -> QualityChecker:
        """Get quality checker."""
        return self._checker

    def run_quality_check(self) -> dict[str, Any]:
        """Run complete quality check."""
        if not self._enabled:
            return {"success": False, "message": "Quality management disabled"}

        results = {
            "success": True,
            "timestamp": datetime.now(),
            "gates_checked": [],
            "overall_score": 0.0,
            "passed_gates": 0,
            "failed_gates": 0,
        }

        total_score = 0.0
        gate_count = 0

        # Check all quality gates
        for gate in QualityGate:
            result = self._checker.check_quality_gate(gate)
            results["gates_checked"].append(
                {
                    "gate": gate.value,
                    "passed": result.passed,
                    "score": result.score,
                    "message": result.message,
                }
            )

            total_score += result.score
            gate_count += 1

            if result.passed:
                results["passed_gates"] += 1
            else:
                results["failed_gates"] += 1

        results["overall_score"] = total_score / gate_count if gate_count > 0 else 0.0

        logger.info(f"Quality check completed: {results['passed_gates']}/{gate_count} gates passed")
        return results

    def get_quality_summary(self) -> dict[str, Any]:
        """Get quality summary."""
        results = self._checker.get_quality_results()
        if not results:
            return {"message": "No quality checks performed"}

        total_gates = len(results)
        passed_gates = len([r for r in results if r.passed])
        failed_gates = total_gates - passed_gates

        return {
            "total_gates": total_gates,
            "passed_gates": passed_gates,
            "failed_gates": failed_gates,
            "success_rate": (passed_gates / total_gates * 100) if total_gates > 0 else 0,
            "last_check": results[-1].timestamp if results else None,
        }


class ComplianceChecker:
    """V2 compliance checker."""

    def __init__(self):
        self._compliance_rules: dict[str, dict[str, Any]] = {}
        self._violations: list[dict[str, Any]] = []
        self._lock = threading.Lock()

    def add_compliance_rule(self, rule_name: str, rule_config: dict[str, Any]) -> None:
        """Add a compliance rule."""
        with self._lock:
            self._compliance_rules[rule_name] = rule_config
            logger.debug(f"Compliance rule added: {rule_name}")

    def check_compliance(self, rule_name: str, data: dict[str, Any]) -> bool:
        """Check compliance for a rule."""
        if rule_name not in self._compliance_rules:
            logger.warning(f"Compliance rule not found: {rule_name}")
            return False

        rule = self._compliance_rules[rule_name]

        # Simple compliance checks
        if "max_lines" in rule:
            if "lines" in data and data["lines"] > rule["max_lines"]:
                violation = {
                    "rule": rule_name,
                    "type": "line_count_exceeded",
                    "value": data["lines"],
                    "limit": rule["max_lines"],
                    "timestamp": datetime.now(),
                }
                self._violations.append(violation)
                return False

        if "max_classes" in rule:
            if "classes" in data and data["classes"] > rule["max_classes"]:
                violation = {
                    "rule": rule_name,
                    "type": "class_count_exceeded",
                    "value": data["classes"],
                    "limit": rule["max_classes"],
                    "timestamp": datetime.now(),
                }
                self._violations.append(violation)
                return False

        return True

    def get_violations(self) -> list[dict[str, Any]]:
        """Get compliance violations."""
        return self._violations.copy()

    def clear_violations(self) -> None:
        """Clear compliance violations."""
        with self._lock:
            self._violations.clear()
            logger.info("Compliance violations cleared")


# Global quality management
quality_manager = QualityManager()
compliance_checker = ComplianceChecker()


def get_quality_manager() -> QualityManager:
    """Get the global quality manager."""
    return quality_manager


def get_compliance_checker() -> ComplianceChecker:
    """Get the global compliance checker."""
    return compliance_checker


def run_quality_check() -> dict[str, Any]:
    """Run quality check."""
    return quality_manager.run_quality_check()
