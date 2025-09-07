"""Reporting utilities for workflow validation."""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

from .rules import ValidationLevel, ValidationResult, RuleResult, ValidationRule

logger = logging.getLogger(__name__)


@dataclass
class WorkflowValidationReport:
    """Complete workflow validation report."""

    workflow_id: str
    validation_level: ValidationLevel
    start_time: datetime
    end_time: Optional[datetime] = None
    total_rules: int = 0
    passed_rules: int = 0
    failed_rules: int = 0
    warning_rules: int = 0
    error_rules: int = 0
    skipped_rules: int = 0
    overall_score: float = 0.0
    reliability_score: float = 0.0
    quality_score: float = 0.0
    performance_score: float = 0.0
    rule_results: List[RuleResult] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def calculate_validation_scores(
    report: WorkflowValidationReport, validation_rules: Dict[str, ValidationRule]
) -> WorkflowValidationReport:
    """Calculate comprehensive validation scores."""

    if not report.rule_results:
        return report

    total_weight = 0.0
    weighted_score = 0.0
    for result in report.rule_results:
        rule = validation_rules.get(result.rule_id)
        if rule:
            weight = rule.weight
            total_weight += weight
            weighted_score += result.score * weight

    if total_weight > 0:
        report.overall_score = weighted_score / total_weight

    if report.total_rules > 0:
        reliability_factors = {
            ValidationResult.PASSED: 1.0,
            ValidationResult.WARNING: 0.8,
            ValidationResult.FAILED: 0.3,
            ValidationResult.ERROR: 0.0,
            ValidationResult.SKIPPED: 0.5,
        }

        reliability_score = 0.0
        for result in report.rule_results:
            factor = reliability_factors.get(result.result, 0.0)
            reliability_score += factor

        report.reliability_score = (reliability_score / report.total_rules) * 100

    valid_scores = [r.score for r in report.rule_results if r.result != ValidationResult.ERROR]
    if valid_scores:
        report.quality_score = statistics.mean(valid_scores)

    execution_times = [r.execution_time for r in report.rule_results if r.execution_time > 0]
    if execution_times:
        avg_time = statistics.mean(execution_times)
        report.performance_score = max(0, 100 - (avg_time * 10))

    return report


def generate_recommendations(report: WorkflowValidationReport) -> List[str]:
    """Generate actionable recommendations based on validation results."""

    recommendations: List[str] = []

    failed_rules = [r for r in report.rule_results if r.result == ValidationResult.FAILED]
    if failed_rules:
        recommendations.append(
            f"Address {len(failed_rules)} failed validation rules to improve overall score"
        )
        for rule in failed_rules[:3]:
            recommendations.append(
                f"Fix {rule.rule_name}: {rule.error_message or 'Review implementation'}"
            )

    warning_rules = [r for r in report.rule_results if r.result == ValidationResult.WARNING]
    if warning_rules:
        recommendations.append(
            f"Review {len(warning_rules)} warning validation rules for potential improvements"
        )

    if report.performance_score < 70:
        recommendations.append(
            "Optimize validation rule execution times for better performance"
        )

    if report.reliability_score < 80:
        recommendations.append(
            "Improve error handling and consistency for better reliability"
        )

    if report.quality_score < 85:
        recommendations.append(
            "Enhance individual rule implementations for higher quality scores"
        )

    if report.overall_score < 90:
        recommendations.append(
            "Consider implementing additional validation rules for comprehensive coverage"
        )

    if not recommendations:
        recommendations.append(
            "Excellent validation results! Maintain current quality standards."
        )

    return recommendations


def export_validation_report(
    report: WorkflowValidationReport, output_path: str
) -> bool:
    """Export a validation report to JSON."""

    try:
        export_data = {
            "workflow_id": report.workflow_id,
            "validation_level": report.validation_level.value,
            "start_time": report.start_time.isoformat(),
            "end_time": report.end_time.isoformat() if report.end_time else None,
            "scores": {
                "overall_score": report.overall_score,
                "reliability_score": report.reliability_score,
                "quality_score": report.quality_score,
                "performance_score": report.performance_score,
            },
            "rule_results": [
                {
                    "rule_id": r.rule_id,
                    "rule_name": r.rule_name,
                    "result": r.result.value,
                    "score": r.score,
                    "details": r.details,
                    "execution_time": r.execution_time,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp.isoformat(),
                }
                for r in report.rule_results
            ],
            "recommendations": report.recommendations,
            "metadata": report.metadata,
        }

        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2, default=str)

        logger.info("Validation report exported to: %s", output_path)
        return True

    except Exception as e:  # pragma: no cover - defensive programming
        logger.error("Failed to export validation report: %s", str(e))
        return False


def get_reliability_trends(reliability_history: List[float]) -> Dict[str, Any]:
    """Get reliability trends and statistics."""

    if not reliability_history:
        return {"message": "No reliability data available"}

    return {
        "current_reliability": reliability_history[-1],
        "average_reliability": statistics.mean(reliability_history),
        "reliability_trend": (
            "improving"
            if len(reliability_history) >= 2
            and reliability_history[-1] > reliability_history[-2]
            else "stable"
        ),
        "total_validations": len(reliability_history),
        "reliability_history": reliability_history[-10:],
    }


__all__ = [
    "WorkflowValidationReport",
    "calculate_validation_scores",
    "generate_recommendations",
    "export_validation_report",
    "get_reliability_trends",
]

