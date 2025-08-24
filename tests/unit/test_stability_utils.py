"""Unit tests for stability management utilities."""

import warnings
from unittest.mock import patch

import pytest

from utils.stability_improvements import (
    StabilityManager,
    safe_import,
    stable_function_call,
    validate_imports,
    suppress_warnings_context,
    setup_stability_improvements,
    cleanup_stability_improvements,
)


class TestStabilityManager:
    """Verify StabilityManager behavior."""

    def test_init(self, stability_manager: StabilityManager):
        """StabilityManager initializes empty state."""
        assert stability_manager.suppressed_warnings == set()
        assert stability_manager.warning_counts == {}
        assert stability_manager.stability_metrics == {}

    def test_suppress_warning(self, stability_manager: StabilityManager):
        """Warnings can be suppressed."""
        stability_manager.suppress_warning(DeprecationWarning, "test message")
        assert len(stability_manager.suppressed_warnings) == 1
        assert (DeprecationWarning, "test message") in stability_manager.suppressed_warnings

    def test_track_warning(self, stability_manager: StabilityManager):
        """Warnings are counted and threshold alerts triggered."""
        stability_manager.track_warning("DeprecationWarning", "test_context")
        assert stability_manager.warning_counts["DeprecationWarning:test_context"] == 1
        for _ in range(10):
            stability_manager.track_warning("DeprecationWarning", "test_context")
        assert stability_manager.warning_counts["DeprecationWarning:test_context"] == 11

    def test_get_stability_report(self, stability_manager: StabilityManager):
        """Report summarizes suppressed warnings and counts."""
        stability_manager.suppress_warning(DeprecationWarning)
        stability_manager.track_warning("TestWarning", "context")
        report = stability_manager.get_stability_report()
        assert report["suppressed_warnings"] == 1
        assert "TestWarning:context" in report["warning_counts"]
        assert report["stability_metrics"] == {}


class TestSafeImport:
    """Test the safe_import utility."""

    def test_successful_import(self):
        """Modules import successfully when available."""
        result = safe_import("json")
        assert result is not None
        assert hasattr(result, "dumps")

    def test_failed_import_with_fallback(self):
        """Fallback value is returned on import failure."""
        result = safe_import("nonexistent_module", fallback="fallback_value")
        assert result == "fallback_value"

    def test_failed_import_with_custom_message(self):
        """Custom warning message is logged on failure."""
        with patch("logging.Logger.warning") as mock_warning:
            safe_import("nonexistent_module", warning_message="Custom message")
            mock_warning.assert_called_once()
            assert "Custom message" in mock_warning.call_args[0][0]


class TestStableFunctionCall:
    """Test the stable_function_call utility."""

    def test_successful_function_call(self):
        """Function executes successfully."""
        def test_func():
            return "success"

        result = stable_function_call(test_func)
        assert result == "success"

    def test_function_with_retry(self):
        """Function retries until success."""
        call_count = 0

        def failing_then_succeeding():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = stable_function_call(failing_then_succeeding, max_retries=3)
        assert result == "success"
        assert call_count == 3

    def test_function_failure_with_fallback(self):
        """Fallback value returned when retries fail."""
        def always_failing():
            raise RuntimeError("Always fails")

        result = stable_function_call(always_failing, fallback_return="fallback")
        assert result == "fallback"


class TestValidateImports:
    """Test the validate_imports utility."""

    def test_required_modules_available(self):
        """Required modules report as available."""
        result = validate_imports(["json", "os"])
        assert result["json"]["status"] == "available"
        assert result["json"]["required"] is True
        assert result["os"]["status"] == "available"
        assert result["os"]["required"] is True

    def test_required_modules_missing(self):
        """Missing required modules are reported."""
        result = validate_imports(["nonexistent_module"])
        assert result["nonexistent_module"]["status"] == "missing"
        assert result["nonexistent_module"]["required"] is True

    def test_optional_modules(self):
        """Optional modules are flagged but not required."""
        result = validate_imports(required_modules=["json"], optional_modules=["nonexistent_optional"])
        assert result["json"]["status"] == "available"
        assert result["nonexistent_optional"]["status"] == "missing"
        assert result["nonexistent_optional"]["required"] is False


class TestSuppressWarningsContext:
    """Test the suppress_warnings_context manager."""

    def test_warning_suppression(self):
        """Warnings are suppressed inside the context."""
        def generate_warning():
            warnings.warn("Test warning", DeprecationWarning)

        with warnings.catch_warnings(record=True) as w:
            generate_warning()
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)

        with suppress_warnings_context(DeprecationWarning):
            with warnings.catch_warnings(record=True) as w:
                generate_warning()
                assert len(w) == 0


class TestStabilityImprovementsSetup:
    """Test setup and cleanup helpers."""

    def test_setup_and_cleanup(self):
        """Setup and cleanup run without errors."""
        manager = setup_stability_improvements()
        assert manager is not None
        cleanup_stability_improvements()

