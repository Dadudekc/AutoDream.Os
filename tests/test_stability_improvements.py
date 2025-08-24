"""
Test Stability Improvements

This module tests the stability improvements and warning management utilities.
"""

import pytest
import warnings
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.stability_improvements import (
    StabilityManager,
    safe_import,
    stable_function_call,
    validate_imports,
    suppress_warnings_context,
    setup_stability_improvements,
    cleanup_stability_improvements
)


class TestStabilityManager:
    """Test the StabilityManager class"""
    
    def test_init(self):
        """Test StabilityManager initialization"""
        manager = StabilityManager()
        assert manager.suppressed_warnings == set()
        assert manager.warning_counts == {}
        assert manager.stability_metrics == {}
    
    def test_suppress_warning(self):
        """Test warning suppression"""
        manager = StabilityManager()
        manager.suppress_warning(DeprecationWarning, "test message")
        
        assert len(manager.suppressed_warnings) == 1
        assert (DeprecationWarning, "test message") in manager.suppressed_warnings
    
    def test_track_warning(self):
        """Test warning tracking"""
        manager = StabilityManager()
        manager.track_warning("DeprecationWarning", "test_context")
        
        assert manager.warning_counts["DeprecationWarning:test_context"] == 1
        
        # Test threshold alert
        for _ in range(10):
            manager.track_warning("DeprecationWarning", "test_context")
        
        # Should trigger alert at >10
        assert manager.warning_counts["DeprecationWarning:test_context"] == 11
    
    def test_get_stability_report(self):
        """Test stability report generation"""
        manager = StabilityManager()
        manager.suppress_warning(DeprecationWarning)
        manager.track_warning("TestWarning", "context")
        
        report = manager.get_stability_report()
        
        assert report["suppressed_warnings"] == 1
        assert "TestWarning:context" in report["warning_counts"]
        assert report["stability_metrics"] == {}


class TestSafeImport:
    """Test the safe_import function"""
    
    def test_successful_import(self):
        """Test successful module import"""
        result = safe_import("json")
        assert result is not None
        assert hasattr(result, "dumps")
    
    def test_failed_import_with_fallback(self):
        """Test failed import with fallback"""
        result = safe_import("nonexistent_module", fallback="fallback_value")
        assert result == "fallback_value"
    
    def test_failed_import_with_custom_message(self):
        """Test failed import with custom warning message"""
        with patch("logging.Logger.warning") as mock_warning:
            safe_import("nonexistent_module", warning_message="Custom message")
            mock_warning.assert_called_once()
            assert "Custom message" in mock_warning.call_args[0][0]


class TestStableFunctionCall:
    """Test the stable_function_call function"""
    
    def test_successful_function_call(self):
        """Test successful function execution"""
        def test_func():
            return "success"
        
        result = stable_function_call(test_func)
        assert result == "success"
    
    def test_function_with_retry(self):
        """Test function execution with retry logic"""
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
        """Test function failure with fallback return"""
        def always_failing():
            raise RuntimeError("Always fails")
        
        result = stable_function_call(always_failing, fallback_return="fallback")
        assert result == "fallback"


class TestValidateImports:
    """Test the validate_imports function"""
    
    def test_required_modules_available(self):
        """Test validation of available required modules"""
        result = validate_imports(["json", "os"])
        
        assert result["json"]["status"] == "available"
        assert result["json"]["required"] is True
        assert result["os"]["status"] == "available"
        assert result["os"]["required"] is True
    
    def test_required_modules_missing(self):
        """Test validation of missing required modules"""
        result = validate_imports(["nonexistent_module"])
        
        assert result["nonexistent_module"]["status"] == "missing"
        assert result["nonexistent_module"]["required"] is True
    
    def test_optional_modules(self):
        """Test validation of optional modules"""
        result = validate_imports(
            required_modules=["json"],
            optional_modules=["nonexistent_optional"]
        )
        
        assert result["json"]["status"] == "available"
        assert result["nonexistent_optional"]["status"] == "missing"
        assert result["nonexistent_optional"]["required"] is False


class TestSuppressWarningsContext:
    """Test the suppress_warnings_context context manager"""
    
    def test_warning_suppression(self):
        """Test that warnings are suppressed within context"""
        def generate_warning():
            warnings.warn("Test warning", DeprecationWarning)
        
        # Warning should be generated outside context
        with warnings.catch_warnings(record=True) as w:
            generate_warning()
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
        
        # Warning should be suppressed within context
        with suppress_warnings_context(DeprecationWarning):
            with warnings.catch_warnings(record=True) as w:
                generate_warning()
                assert len(w) == 0


class TestStabilityImprovementsSetup:
    """Test stability improvements setup and cleanup"""
    
    def test_setup_and_cleanup(self):
        """Test setup and cleanup of stability improvements"""
        # Setup
        manager = setup_stability_improvements()
        assert manager is not None
        
        # Cleanup
        cleanup_stability_improvements()
        # Should not raise any errors


class TestIntegration:
    """Integration tests for stability improvements"""
    
    def test_end_to_end_stability_management(self):
        """Test end-to-end stability management workflow"""
        manager = StabilityManager()
        
        # Suppress a warning
        manager.suppress_warning(DeprecationWarning, "test pattern")
        
        # Track some warnings
        manager.track_warning("DeprecationWarning", "test_context")
        manager.track_warning("UserWarning", "another_context")
        
        # Generate report
        report = manager.get_stability_report()
        
        assert report["suppressed_warnings"] == 1
        assert len(report["warning_counts"]) == 2
        
        # Cleanup
        manager.restore_warnings()
        assert len(manager.suppressed_warnings) == 0
    
    def test_safe_import_with_stability_manager(self):
        """Test safe_import integration with stability manager"""
        manager = StabilityManager()
        
        # Track import attempts
        result = safe_import("nonexistent_module", fallback="test_fallback")
        manager.track_warning("ImportError", "nonexistent_module")
        
        assert result == "test_fallback"
        assert manager.warning_counts["ImportError:nonexistent_module"] == 1


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
