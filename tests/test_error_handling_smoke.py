#!/usr/bin/env python3
"""
Error Handling Smoke Tests
===========================

Quick validation tests for error handling models.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import importlib.util

import pytest

pytestmark = pytest.mark.smoke


def load_error_models():
    """Load error models directly (bypass broken __init__)."""
    spec = importlib.util.spec_from_file_location(
        "error_handling_models", "src/core/error_handling/error_handling_models.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.smoke
def test_error_classifier_init():
    """Smoke test: ErrorClassifier initializes."""
    models = load_error_models()
    classifier = models.ErrorClassifier()
    assert classifier is not None


@pytest.mark.smoke
def test_error_severity_classification():
    """Smoke test: Severity classification works."""
    models = load_error_models()
    classifier = models.ErrorClassifier()

    # Critical error
    exc = ValueError("test")
    severity = classifier.classify_severity(exc)
    assert severity == models.ErrorSeverity.HIGH


@pytest.mark.smoke
def test_error_decision_engine():
    """Smoke test: Decision engine works."""
    models = load_error_models()
    engine = models.ErrorDecisionEngine()

    exc = FileNotFoundError("test")
    decision = engine.decide_action(exc, attempt=1)

    assert decision["action"] in ["retry", "fail", "escalate"]
    assert "severity" in decision


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "smoke"])
