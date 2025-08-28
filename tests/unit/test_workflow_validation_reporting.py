"""Tests for reporting utilities."""

from datetime import datetime

from core.workflow_validation.system.reporting import (
    WorkflowValidationReport,
    calculate_validation_scores,
    generate_recommendations,
)
from core.workflow_validation.system.rules import (
    ValidationRule,
    ValidationLevel,
    ValidationResult,
    RuleResult,
)


def test_calculate_scores_and_recommendations():
    rule = ValidationRule(
        rule_id="r1",
        name="Rule1",
        description="test",
        validation_func=lambda *args, **kwargs: {},
        level=ValidationLevel.BASIC,
        weight=1.0,
    )
    result = RuleResult(
        rule_id="r1",
        rule_name="Rule1",
        result=ValidationResult.PASSED,
        score=100.0,
        execution_time=0.1,
    )
    report = WorkflowValidationReport(
        workflow_id="wf",
        validation_level=ValidationLevel.BASIC,
        start_time=datetime.now(),
        rule_results=[result],
        total_rules=1,
        passed_rules=1,
    )

    report = calculate_validation_scores(report, {"r1": rule})
    recs = generate_recommendations(report)

    assert report.overall_score == 100.0
    assert recs

