"""Tests for validation rule definitions."""

import asyncio
import pytest

from core.workflow_validation.system.rules import (
    initialize_validation_rules,
    ValidationRule,
    ValidationResult,
)


def test_initialize_validation_rules_returns_rules():
    rules = initialize_validation_rules()
    assert isinstance(rules, dict)
    assert "code_quality_srp_compliance" in rules
    assert isinstance(rules["code_quality_srp_compliance"], ValidationRule)


def test_rule_execution_produces_status():
    rules = initialize_validation_rules()
    rule = rules["code_quality_srp_compliance"]
    result = asyncio.run(rule.validation_func("wf", None, None))
    assert "status" in result
    assert isinstance(result["status"], ValidationResult)

