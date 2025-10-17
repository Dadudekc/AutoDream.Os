#!/usr/bin/env python3
"""
Tests for Consolidated Validation Utilities
============================================

Tests for consolidated validation functions (DUP-Validation mission).

Author: Agent-5
Date: 2025-10-17
"""

import pytest
from pathlib import Path
from src.core.validation.consolidated_validation_utils import (
    validate_config,
    validate_config_value,
    validate_session,
    validate_session_active,
    validate_import_syntax,
    validate_import_pattern,
    validate_module_path,
    validate_file_path,
    validate_file_extension,
    validate_type,
    validate_not_none,
    validate_not_empty,
    validate_hasattr,
    validate_range,
    validate_coordinates,
    validate_forecast_accuracy,
    validate_regex,
    validate_custom,
)


class TestConfigValidation:
    """Tests for config validation functions."""
    
    def test_validate_config_valid_dict(self):
        """Test valid config dictionary."""
        config = {'key1': 'value1', 'key2': 'value2'}
        assert validate_config(config) is True
    
    def test_validate_config_empty_dict(self):
        """Test empty config fails."""
        assert validate_config({}) is False
    
    def test_validate_config_none(self):
        """Test None config fails."""
        assert validate_config(None) is False
    
    def test_validate_config_required_keys(self):
        """Test required keys validation."""
        config = {'api_key': 'test', 'endpoint': 'http://test'}
        assert validate_config(config, ['api_key', 'endpoint']) is True
        assert validate_config(config, ['api_key', 'missing']) is False
    
    def test_validate_config_value_correct_type(self):
        """Test config value type validation."""
        assert validate_config_value('test', str) is True
        assert validate_config_value(123, int) is True
        assert validate_config_value('test', int) is False
    
    def test_validate_config_value_none_handling(self):
        """Test None value handling."""
        assert validate_config_value(None, str, allow_none=True) is True
        assert validate_config_value(None, str, allow_none=False) is False


class TestSessionValidation:
    """Tests for session validation functions."""
    
    def test_validate_session_valid(self):
        """Test valid session object."""
        class MockSession:
            cookies = {}
            headers = {}
        
        assert validate_session(MockSession()) is True
    
    def test_validate_session_none(self):
        """Test None session fails."""
        assert validate_session(None) is False
    
    def test_validate_session_active_with_cookies(self):
        """Test active session with cookies."""
        class MockSession:
            cookies = {'session_id': 'test'}
            headers = {}
        
        assert validate_session_active(MockSession()) is True
    
    def test_validate_session_active_no_cookies(self):
        """Test session with no cookies fails active check."""
        class MockSession:
            cookies = {}
            headers = {}
        
        assert validate_session_active(MockSession()) is False


class TestImportValidation:
    """Tests for import validation functions."""
    
    def test_validate_import_syntax_simple(self):
        """Test simple import syntax."""
        assert validate_import_syntax('import os') is True
        assert validate_import_syntax('import sys') is True
    
    def test_validate_import_syntax_from(self):
        """Test from import syntax."""
        assert validate_import_syntax('from os import path') is True
        assert validate_import_syntax('from pathlib import Path') is True
    
    def test_validate_import_syntax_as(self):
        """Test import as syntax."""
        assert validate_import_syntax('import numpy as np') is True
    
    def test_validate_import_syntax_invalid(self):
        """Test invalid import syntax."""
        assert validate_import_syntax('not_an_import') is False
        assert validate_import_syntax('') is False
        assert validate_import_syntax(None) is False
    
    def test_validate_import_pattern_module(self):
        """Test module pattern validation."""
        assert validate_import_pattern('src.core.config') is True
        assert validate_import_pattern('os.path') is True
    
    def test_validate_import_pattern_wildcard(self):
        """Test wildcard pattern."""
        assert validate_import_pattern('src.core.*') is True
        assert validate_import_pattern('*.utils') is True
    
    def test_validate_module_path_valid(self):
        """Test valid module paths."""
        assert validate_module_path('src.core.config') is True
        assert validate_module_path('my_module') is True
        assert validate_module_path('_private') is True
    
    def test_validate_module_path_invalid(self):
        """Test invalid module paths."""
        assert validate_module_path('123invalid') is False
        assert validate_module_path('has-dash') is False


class TestFilePathValidation:
    """Tests for file path validation functions."""
    
    def test_validate_file_path_string(self):
        """Test string path validation."""
        assert validate_file_path('test/path/file.py') is True
        assert validate_file_path('') is False
        assert validate_file_path(None) is False
    
    def test_validate_file_path_exists(self):
        """Test path existence check."""
        # This file should exist
        assert validate_file_path(__file__, must_exist=True) is True
        # Non-existent file
        assert validate_file_path('nonexistent/file.py', must_exist=True) is False
    
    def test_validate_file_extension_allowed(self):
        """Test file extension validation."""
        assert validate_file_extension('test.py', ['.py', '.md']) is True
        assert validate_file_extension('test.md', ['.py', '.md']) is True
        assert validate_file_extension('test.txt', ['.py', '.md']) is False
    
    def test_validate_file_extension_empty(self):
        """Test empty inputs."""
        assert validate_file_extension('', ['.py']) is False
        assert validate_file_extension('test.py', []) is False


class TestTypeValidation:
    """Tests for type validation functions."""
    
    def test_validate_type_correct(self):
        """Test correct type validation."""
        assert validate_type('test', str) is True
        assert validate_type(123, int) is True
        assert validate_type([], list) is True
    
    def test_validate_type_incorrect(self):
        """Test incorrect type."""
        assert validate_type('test', int) is False
        assert validate_type(123, str) is False
    
    def test_validate_not_none_valid(self):
        """Test not None validation."""
        assert validate_not_none('test') is True
        assert validate_not_none(0) is True
        assert validate_not_none([]) is True
    
    def test_validate_not_none_invalid(self):
        """Test None fails."""
        assert validate_not_none(None) is False
    
    def test_validate_not_empty_string(self):
        """Test non-empty string."""
        assert validate_not_empty('test') is True
        assert validate_not_empty('') is False
    
    def test_validate_not_empty_collections(self):
        """Test non-empty collections."""
        assert validate_not_empty([1, 2, 3]) is True
        assert validate_not_empty([]) is False
        assert validate_not_empty({'key': 'value'}) is True
        assert validate_not_empty({}) is False
    
    def test_validate_hasattr_present(self):
        """Test hasattr when attribute exists."""
        class TestObj:
            test_attr = 'value'
        
        assert validate_hasattr(TestObj(), 'test_attr') is True
    
    def test_validate_hasattr_missing(self):
        """Test hasattr when attribute missing."""
        class TestObj:
            pass
        
        assert validate_hasattr(TestObj(), 'missing_attr') is False
    
    def test_validate_range_within(self):
        """Test value within range."""
        assert validate_range(5, min_val=0, max_val=10) is True
        assert validate_range(0, min_val=0, max_val=10) is True
        assert validate_range(10, min_val=0, max_val=10) is True
    
    def test_validate_range_outside(self):
        """Test value outside range."""
        assert validate_range(-1, min_val=0, max_val=10) is False
        assert validate_range(11, min_val=0, max_val=10) is False
    
    def test_validate_range_no_bounds(self):
        """Test range with no bounds."""
        assert validate_range(999999) is True
        assert validate_range(-999999) is True


class TestSpecializedValidation:
    """Tests for specialized validation functions."""
    
    def test_validate_coordinates_valid(self):
        """Test valid screen coordinates."""
        assert validate_coordinates(100, 100) is True
        assert validate_coordinates(1920, 1080) is True
    
    def test_validate_coordinates_invalid(self):
        """Test invalid coordinates."""
        assert validate_coordinates(9999, 9999) is False
        assert validate_coordinates(-9999, -9999) is False
    
    def test_validate_forecast_accuracy_within_tolerance(self):
        """Test forecast within tolerance."""
        assert validate_forecast_accuracy(100.0, 105.0, tolerance=10.0) is True
        assert validate_forecast_accuracy(100.0, 100.0, tolerance=0.1) is True
    
    def test_validate_forecast_accuracy_outside_tolerance(self):
        """Test forecast outside tolerance."""
        assert validate_forecast_accuracy(100.0, 120.0, tolerance=10.0) is False


class TestUtilityValidation:
    """Tests for utility validation functions."""
    
    def test_validate_regex_match(self):
        """Test regex pattern matching."""
        assert validate_regex('test123', r'^test\d+$') is True
        assert validate_regex('test', r'^test\d+$') is False
    
    def test_validate_regex_invalid_pattern(self):
        """Test invalid regex pattern."""
        assert validate_regex('test', '[invalid(') is False
    
    def test_validate_custom_success(self):
        """Test custom validator success."""
        validator = lambda x: x > 10
        assert validate_custom(15, validator) is True
        assert validate_custom(5, validator) is False
    
    def test_validate_custom_exception(self):
        """Test custom validator that raises exception."""
        def bad_validator(x):
            raise ValueError("Test error")
        
        assert validate_custom('test', bad_validator) is False

