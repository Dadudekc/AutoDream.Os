#!/usr/bin/env python3
"""
Test Utilities Module - Common Test Operations
=============================================

This module provides common test utilities extracted from the monolithic
test_todo_implementation.py file to reduce duplication and improve maintainability.

Author: Agent-2 - PHASE TRANSITION OPTIMIZATION MANAGER
License: MIT
"""

import tempfile
import shutil
from pathlib import Path
from typing import Optional, Any


class TestUtilities:
    """Common test utilities for code generation tests."""
    
    @staticmethod
    def create_temp_environment() -> Path:
        """Create a temporary test environment and return the path."""
        temp_dir = tempfile.mkdtemp()
        return Path(temp_dir)
    
    @staticmethod
    def cleanup_temp_environment(temp_dir: Path) -> None:
        """Clean up temporary test environment."""
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up temp directory: {e}")
    
    @staticmethod
    def create_test_file(temp_dir: Path, filename: str, content: str) -> Path:
        """Create a test file with specified content."""
        file_path = temp_dir / filename
        file_path.write_text(content)
        return file_path
    
    @staticmethod
    def verify_file_content(file_path: Path, expected_content: str) -> bool:
        """Verify file contains expected content."""
        try:
            actual_content = file_path.read_text()
            return actual_content == expected_content
        except Exception:
            return False
    
    @staticmethod
    def verify_file_contains(file_path: Path, expected_strings: list) -> bool:
        """Verify file contains all expected strings."""
        try:
            content = file_path.read_text()
            return all(expected in content for expected in expected_strings)
        except Exception:
            return False
    
    @staticmethod
    def verify_file_not_contains(file_path: Path, forbidden_strings: list) -> bool:
        """Verify file does not contain forbidden strings."""
        try:
            content = file_path.read_text()
            return all(forbidden not in content for forbidden in forbidden_strings)
        except Exception:
            return False
    
    @staticmethod
    def create_test_directory_structure(temp_dir: Path, structure: dict) -> None:
        """Create a test directory structure for complex tests."""
        for name, content in structure.items():
            if isinstance(content, dict):
                # Create subdirectory
                subdir = temp_dir / name
                subdir.mkdir(exist_ok=True)
                TestUtilities.create_test_directory_structure(subdir, content)
            else:
                # Create file
                TestUtilities.create_test_file(temp_dir, name, content)
    
    @staticmethod
    def assert_file_exists(file_path: Path, test_case) -> None:
        """Assert that a file exists (for use in test methods)."""
        test_case.assertTrue(file_path.exists(), f"File {file_path} should exist")
    
    @staticmethod
    def assert_file_content_matches(file_path: Path, expected_content: str, test_case) -> None:
        """Assert that file content matches expected content."""
        actual_content = file_path.read_text()
        test_case.assertEqual(actual_content, expected_content, 
                            f"File content mismatch in {file_path}")
    
    @staticmethod
    def assert_file_contains_strings(file_path: Path, expected_strings: list, test_case) -> None:
        """Assert that file contains all expected strings."""
        content = file_path.read_text()
        for expected in expected_strings:
            test_case.assertIn(expected, content, 
                             f"File {file_path} should contain '{expected}'")
    
    @staticmethod
    def assert_file_not_contains_strings(file_path: Path, forbidden_strings: list, test_case) -> None:
        """Assert that file does not contain forbidden strings."""
        content = file_path.read_text()
        for forbidden in forbidden_strings:
            test_case.assertNotIn(forbidden, content, 
                                f"File {file_path} should not contain '{forbidden}'")
