"""Tests for validation executor module."""
from src.services.validation_executor import ValidationExecutor
from src.services.validation_rules import ValidationRuleManager


def test_deadline_rule_failure():
    manager = ValidationRuleManager()
    executor = ValidationExecutor(manager)
    contract = {
        "contract_id": "c1",
        "deadline": "2024-01-01",
        "delivery_date": "2024-02-01",
    }
    results = executor.execute(contract)
    deadline = next(r for r in results if r.rule_id == "deadline_check")
    assert deadline.passed is False
