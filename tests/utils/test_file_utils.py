#!/usr/bin/env python3
"""Unit tests for file utilities."""

import shutil
import unittest
from pathlib import Path
from src.core.utils.io_utils import FileUtils


class TestFileUtils(unittest.TestCase):
    """Test file utilities functionality."""

    def setUp(self):
        self.file_utils = FileUtils()
        self.test_dir = Path("test_temp")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_directory_creation(self):
        """Directories are created as expected."""
        test_path = self.test_dir / "subdir" / "nested"
        result = FileUtils.ensure_directory(str(test_path))
        self.assertTrue(result)
        self.assertTrue(test_path.exists())

    def test_json_operations(self):
        """JSON files can be written and read."""
        test_file = self.test_dir / "test.json"
        test_data = {"test": "data", "number": 42}
        write_result = FileUtils.write_json(str(test_file), test_data)
        self.assertTrue(write_result)
        self.assertTrue(test_file.exists())
        read_data = FileUtils.read_json(str(test_file))
        self.assertEqual(read_data, test_data)

    def test_file_operations(self):
        """Basic file operations function correctly."""
        test_file = self.test_dir / "test.txt"
        test_file.write_text("test content")
        self.assertTrue(FileUtils.file_exists(str(test_file)))
        size = FileUtils.get_file_size(str(test_file))
        self.assertIsNotNone(size)
        self.assertGreater(size, 0)
