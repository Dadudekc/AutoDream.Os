#!/usr/bin/env python3
"""
Test String Manager - V2 Compliance Module
=========================================

Unit tests for string manager operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import unittest
import json

from ..managers.string_manager import StringManager, StringOperationConfig, StringOperationError


class TestStringManager(unittest.TestCase):
    """Test cases for StringManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.string_manager = StringManager(StringOperationConfig(
            enable_caching=False,
            enable_validation=True
        ))

    def test_format_string_success(self):
        """Test successful string formatting."""
        template = "Hello, {name}! You have {count} messages."
        result = self.string_manager.format_string(template, name="Alice", count=5)
        expected = "Hello, Alice! You have 5 messages."
        self.assertEqual(result, expected)

    def test_sanitize_string_success(self):
        """Test successful string sanitization."""
        text = "Hello, World! This is a test@#$%^&*()"
        result = self.string_manager.sanitize_string(text, remove_special=True)
        expected = "Hello World This is a test"
        self.assertEqual(result, expected)

    def test_validate_string_success(self):
        """Test successful string validation."""
        text = "Valid string"
        result = self.string_manager.validate_string(text, min_length=5, max_length=20)
        self.assertTrue(result)

    def test_validate_string_failure(self):
        """Test string validation failure."""
        text = "Short"
        result = self.string_manager.validate_string(text, min_length=10, max_length=20)
        self.assertFalse(result)

    def test_transform_data_json_stringify(self):
        """Test JSON stringify transformation."""
        data = {"name": "Alice", "age": 30}
        result = self.string_manager.transform_data(data, "json_stringify")
        expected = json.dumps(data)
        self.assertEqual(result, expected)

    def test_transform_data_json_parse(self):
        """Test JSON parse transformation."""
        json_string = '{"name": "Alice", "age": 30}'
        result = self.string_manager.transform_data(json_string, "json_parse")
        expected = {"name": "Alice", "age": 30}
        self.assertEqual(result, expected)

    def test_transform_data_string_lower(self):
        """Test string lower transformation."""
        text = "HELLO WORLD"
        result = self.string_manager.transform_data(text, "string_lower")
        expected = "hello world"
        self.assertEqual(result, expected)

    def test_parse_json_success(self):
        """Test successful JSON parsing."""
        json_string = '{"name": "Alice", "age": 30}'
        result = self.string_manager.parse_json(json_string)
        expected = {"name": "Alice", "age": 30}
        self.assertEqual(result, expected)

    def test_stringify_json_success(self):
        """Test successful JSON stringification."""
        data = {"name": "Alice", "age": 30}
        result = self.string_manager.stringify_json(data)
        expected = json.dumps(data)
        self.assertEqual(result, expected)

    def test_extract_patterns(self):
        """Test pattern extraction."""
        text = "The quick brown fox jumps over the lazy dog"
        pattern = r'\b\w{4}\b'  # 4-letter words
        result = self.string_manager.extract_patterns(text, pattern)
        expected = ['quick', 'brown', 'jumps', 'over', 'lazy']
        self.assertEqual(result, expected)

    def test_replace_patterns(self):
        """Test pattern replacement."""
        text = "The quick brown fox"
        pattern = r'\b\w{4}\b'  # 4-letter words
        replacement = "****"
        result = self.string_manager.replace_patterns(text, pattern, replacement)
        expected = "The **** **** fox"
        self.assertEqual(result, expected)

    def test_batch_operations(self):
        """Test batch operations."""
        operations = [
            {"type": "format", "template": "Hello, {name}!", "kwargs": {"name": "Alice"}},
            {"type": "sanitize", "text": "Hello@#$%", "remove_special": True},
            {"type": "validate", "text": "Valid string", "min_length": 5, "max_length": 20}
        ]
        
        results = self.string_manager.batch_operations(operations)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], "Hello, Alice!")
        self.assertEqual(results[1], "Hello")
        self.assertTrue(results[2])


if __name__ == '__main__':
    unittest.main()
