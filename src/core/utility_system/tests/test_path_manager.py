#!/usr/bin/env python3
"""
Test Path Manager - V2 Compliance Module
=======================================

Unit tests for path manager operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import unittest
import tempfile
from pathlib import Path

from ..managers.path_manager import PathManager, PathOperationConfig, PathOperationError


class TestPathManager(unittest.TestCase):
    """Test cases for PathManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.path_manager = PathManager(PathOperationConfig(
            enable_validation=True,
            project_root=Path(self.temp_dir)
        ))

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_resolve_path_absolute(self):
        """Test resolving absolute path."""
        absolute_path = Path(self.temp_dir) / "test.txt"
        result = self.path_manager.resolve_path(absolute_path)
        self.assertEqual(result, absolute_path)

    def test_resolve_path_relative(self):
        """Test resolving relative path."""
        relative_path = "test.txt"
        result = self.path_manager.resolve_path(relative_path)
        expected = Path(self.temp_dir) / "test.txt"
        self.assertEqual(result, expected)

    def test_normalize_path(self):
        """Test path normalization."""
        test_path = Path(self.temp_dir) / ".." / "test.txt"
        result = self.path_manager.normalize_path(test_path)
        self.assertIsInstance(result, str)
        self.assertIn("test.txt", result)

    def test_get_relative_path(self):
        """Test getting relative path."""
        file_path = Path(self.temp_dir) / "subdir" / "test.txt"
        file_path.parent.mkdir(exist_ok=True)
        file_path.touch()
        
        result = self.path_manager.get_relative_path(file_path, self.temp_dir)
        expected = "subdir/test.txt"
        self.assertEqual(result, expected)

    def test_get_file_extension(self):
        """Test getting file extension."""
        test_file = Path(self.temp_dir) / "test.txt"
        result = self.path_manager.get_file_extension(test_file)
        self.assertEqual(result, ".txt")

    def test_path_exists(self):
        """Test path existence check."""
        existing_file = Path(self.temp_dir) / "existing.txt"
        existing_file.touch()
        
        self.assertTrue(self.path_manager.path_exists(existing_file))
        self.assertFalse(self.path_manager.path_exists(Path(self.temp_dir) / "nonexistent.txt"))

    def test_is_file(self):
        """Test file check."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.touch()
        
        self.assertTrue(self.path_manager.is_file(test_file))
        self.assertFalse(self.path_manager.is_file(Path(self.temp_dir)))

    def test_is_directory(self):
        """Test directory check."""
        test_dir = Path(self.temp_dir) / "test_dir"
        test_dir.mkdir()
        
        self.assertTrue(self.path_manager.is_directory(test_dir))
        self.assertFalse(self.path_manager.is_directory(Path(self.temp_dir) / "nonexistent.txt"))

    def test_create_directory(self):
        """Test directory creation."""
        test_dir = Path(self.temp_dir) / "new_dir"
        result = self.path_manager.create_directory(test_dir)
        self.assertTrue(result)
        self.assertTrue(test_dir.exists())
        self.assertTrue(test_dir.is_dir())

    def test_get_directory_contents(self):
        """Test getting directory contents."""
        # Create test files
        (Path(self.temp_dir) / "file1.txt").touch()
        (Path(self.temp_dir) / "file2.txt").touch()
        (Path(self.temp_dir) / "subdir").mkdir()
        
        contents = self.path_manager.get_directory_contents(self.temp_dir)
        self.assertGreaterEqual(len(contents), 3)  # At least 2 files + 1 directory

    def test_get_path_info(self):
        """Test getting path information."""
        test_file = Path(self.temp_dir) / "info_test.txt"
        test_file.touch()
        
        info = self.path_manager.get_path_info(test_file)
        self.assertEqual(info["name"], "info_test.txt")
        self.assertEqual(info["stem"], "info_test")
        self.assertEqual(info["suffix"], ".txt")
        self.assertTrue(info["exists"])
        self.assertTrue(info["is_file"])
        self.assertFalse(info["is_directory"])

    def test_batch_operations(self):
        """Test batch operations."""
        test_file = Path(self.temp_dir) / "batch_test.txt"
        test_file.touch()
        
        operations = [
            {"type": "exists", "path": test_file},
            {"type": "extension", "file_path": test_file},
            {"type": "normalize", "path": test_file}
        ]
        
        results = self.path_manager.batch_operations(operations)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0])  # File exists
        self.assertEqual(results[1], ".txt")  # Extension
        self.assertIsInstance(results[2], str)  # Normalized path


if __name__ == '__main__':
    unittest.main()
