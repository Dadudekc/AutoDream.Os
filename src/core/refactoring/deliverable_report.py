"""Generate reports for contract deliverable validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class RuleResult:
    """Result of a single validation rule."""

    rule_id: str
    description: str
    passed: bool


@dataclass
class DeliverableReport:
    """Summary of contract validation results."""

    contract_id: str
    validation_date: datetime
    total_tests: int
    passed_tests: int
    failed_tests: int
    overall_score: float
    requirements_met: int
    total_requirements: int
    test_results: List[RuleResult] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


def create_report(contract_id: str, results: List[RuleResult]) -> DeliverableReport:
    """Create a deliverable validation report from rule results."""
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    overall = (passed / total * 100) if total else 0.0
    recommendations: List[str] = []
    if failed:
        recommendations.append(f"Address {failed} failing validation rules")
    else:
        recommendations.append("All validation rules passed")
    return DeliverableReport(
        contract_id=contract_id,
        validation_date=datetime.now(),
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        overall_score=overall,
        requirements_met=passed,
        total_requirements=total,
        test_results=results,
        recommendations=recommendations,
    )
