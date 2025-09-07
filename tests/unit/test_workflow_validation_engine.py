"""Tests for the workflow validation execution engine."""

import asyncio
import pytest

from core.workflow_validation import (
    WorkflowValidationSystem,
    ValidationLevel,
    ValidationRule,
    ValidationResult,
)


def test_engine_executes_custom_rule():
    system = WorkflowValidationSystem()

    async def quick_rule(workflow_id, target_files, workflow_data):
        return {"status": ValidationResult.PASSED, "score": 100.0}

    system.add_validation_rule(
        ValidationRule(
            rule_id="quick",
            name="Quick Rule",
            description="A fast rule for testing",
            validation_func=quick_rule,
            level=ValidationLevel.BASIC,
        )
    )

    report = asyncio.run(
        system.validate_workflow("wf1", validation_level=ValidationLevel.BASIC)
    )
    assert report.passed_rules == 1
    assert report.total_rules == 1

