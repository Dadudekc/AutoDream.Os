"""Tests for validation reporter module."""
from src.services.validation_reporter import ValidationReporter
from src.services.validation_rules import ValidationResult, ValidationSeverity


def test_summary_counts_pass_fail():
    reporter = ValidationReporter()
    results = [
        ValidationResult(
            contract_id="c1",
            rule_id="r1",
            passed=True,
            severity=ValidationSeverity.INFO,
            message="",
            details={},
            timestamp=0.0,
        ),
        ValidationResult(
            contract_id="c1",
            rule_id="r2",
            passed=False,
            severity=ValidationSeverity.ERROR,
            message="",
            details={},
            timestamp=0.0,
        ),
    ]
    summary = reporter.summarize(results)
    assert summary == {"passed": 1, "failed": 1}
