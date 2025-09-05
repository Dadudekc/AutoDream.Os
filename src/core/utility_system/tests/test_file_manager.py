#!/usr/bin/env python3
"""
Test File Manager - V2 Compliance Module
=======================================

Unit tests for file manager operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import unittest
import tempfile
import os
from pathlib import Path

from ..managers.file_manager import FileManager, FileOperationConfig, FileOperationError


class TestFileManager(unittest.TestCase):
    """Test cases for FileManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(FileOperationConfig(
            enable_caching=False,
            backup_before_write=False,
            validate_checksums=False
        ))

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_read_file_success(self):
        """Test successful file read."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = "Hello, World!"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        result = self.file_manager.read_file(test_file)
        self.assertEqual(result, test_content)

    def test_read_file_not_found(self):
        """Test file read with non-existent file."""
        non_existent_file = Path(self.temp_dir) / "nonexistent.txt"
        
        with self.assertRaises(FileOperationError):
            self.file_manager.read_file(non_existent_file)

    def test_write_file_success(self):
        """Test successful file write."""
        test_file = Path(self.temp_dir) / "write_test.txt"
        test_content = "Test content"
        
        result = self.file_manager.write_file(test_file, test_content)
        self.assertTrue(result)
        
        with open(test_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_content)

    def test_copy_file_success(self):
        """Test successful file copy."""
        source_file = Path(self.temp_dir) / "source.txt"
        dest_file = Path(self.temp_dir) / "dest.txt"
        test_content = "Copy test content"
        
        with open(source_file, 'w') as f:
            f.write(test_content)
        
        result = self.file_manager.copy_file(source_file, dest_file)
        self.assertTrue(result)
        self.assertTrue(dest_file.exists())
        
        with open(dest_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_content)

    def test_get_file_size(self):
        """Test get file size."""
        test_file = Path(self.temp_dir) / "size_test.txt"
        test_content = "Size test"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        size = self.file_manager.get_file_size(test_file)
        self.assertEqual(size, len(test_content.encode('utf-8')))

    def test_get_file_hash(self):
        """Test get file hash."""
        test_file = Path(self.temp_dir) / "hash_test.txt"
        test_content = "Hash test content"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        hash_value = self.file_manager.get_file_hash(test_file)
        self.assertIsInstance(hash_value, str)
        self.assertGreater(len(hash_value), 0)

    def test_batch_operations(self):
        """Test batch operations."""
        test_file = Path(self.temp_dir) / "batch_test.txt"
        test_content = "Batch test content"
        
        operations = [
            {"type": "write", "file_path": test_file, "content": test_content},
            {"type": "read", "file_path": test_file},
            {"type": "copy", "source": test_file, "destination": Path(self.temp_dir) / "copy.txt"}
        ]
        
        results = self.file_manager.batch_operations(operations)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0])  # Write should succeed
        self.assertEqual(results[1], test_content)  # Read should return content
        self.assertTrue(results[2])  # Copy should succeed


if __name__ == '__main__':
    unittest.main()
