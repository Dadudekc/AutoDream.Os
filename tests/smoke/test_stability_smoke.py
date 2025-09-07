"""Smoke tests for stability utilities."""

import pytest

from utils.stability_improvements import StabilityManager, safe_import


@pytest.mark.smoke
def test_stability_manager_basic(stability_manager: StabilityManager):
    """StabilityManager suppresses warnings and reports them."""
    stability_manager.suppress_warning(DeprecationWarning, "test")
    report = stability_manager.get_stability_report()
    assert report["suppressed_warnings"] == 1


@pytest.mark.smoke
def test_safe_import_smoke():
    """safe_import returns fallback for missing module."""
    assert safe_import("nonexistent_module", fallback="x") == "x"

