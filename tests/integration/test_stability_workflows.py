"""Integration tests for stability management workflows."""

import pytest

from utils.stability_improvements import StabilityManager, safe_import


class TestStabilityIntegration:
    """Ensure stability utilities work together."""

    def test_end_to_end_stability_management(self, stability_manager: StabilityManager):
        """End-to-end stability management workflow."""
        stability_manager.suppress_warning(DeprecationWarning, "test pattern")
        stability_manager.track_warning("DeprecationWarning", "test_context")
        stability_manager.track_warning("UserWarning", "another_context")
        report = stability_manager.get_stability_report()
        assert report["suppressed_warnings"] == 1
        assert len(report["warning_counts"]) == 2
        stability_manager.restore_warnings()
        assert len(stability_manager.suppressed_warnings) == 0

    def test_safe_import_with_stability_manager(self, stability_manager: StabilityManager):
        """safe_import integrates with warning tracking."""
        result = safe_import("nonexistent_module", fallback="test_fallback")
        stability_manager.track_warning("ImportError", "nonexistent_module")
        assert result == "test_fallback"
        assert stability_manager.warning_counts["ImportError:nonexistent_module"] == 1

