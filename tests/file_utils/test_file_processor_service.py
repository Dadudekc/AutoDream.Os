#!/usr/bin/env python3
"""
Test File Processor Service - Agent Cellphone V2
================================================

TDD tests for FileProcessorService implementation.
Follows V2 standards: Test-First Development, 90% coverage minimum.
"""

import pytest
import tempfile

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from unittest.mock import Mock, patch
import json

# Import will be created after tests pass (TDD RED phase)
# from src.services.file_processor_service import FileProcessorService


class TestFileProcessorService:
    """Test suite for FileProcessorService following TDD principles."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_service_initialization(self):
        """Test FileProcessorService can be initialized."""
        # RED: This will fail until service is implemented
        processor = FileProcessorService()
        assert processor is not None
        assert hasattr(processor, "process_file")
        assert hasattr(processor, "get_file_stats")

    def test_process_python_file(self):
        """Test processing Python source files."""
        processor = FileProcessorService()

        # Create test Python file
        python_file = self.test_dir / "test.py"
        python_file.write_text(
            '''
def test_function():
    """Test function."""
    return "hello"

class TestClass:
    def method(self):
        pass
'''
        )

        result = processor.process_file(python_file)

        assert result["file_path"] == str(python_file)
        assert result["file_type"] == "python"
        assert result["functions_count"] >= 1
        assert result["classes_count"] >= 1
        assert result["lines_count"] > 0
        assert result["size_bytes"] > 0

    def test_process_javascript_file(self):
        """Test processing JavaScript source files."""
        processor = FileProcessorService()

        # Create test JavaScript file
        js_file = self.test_dir / "test.js"
        js_file.write_text(
            """
function testFunction() {
    return "hello";
}

class TestClass {
    constructor() {
        this.value = 42;
    }
}
"""
        )

        result = processor.process_file(js_file)

        assert result["file_path"] == str(js_file)
        assert result["file_type"] == "javascript"
        assert result["functions_count"] >= 1
        assert result["classes_count"] >= 1
        assert result["lines_count"] > 0

    def test_process_rust_file(self):
        """Test processing Rust source files."""
        processor = FileProcessorService()

        # Create test Rust file
        rust_file = self.test_dir / "test.rs"
        rust_file.write_text(
            """
fn test_function() -> String {
    "hello".to_string()
}

struct TestStruct {
    value: i32,
}

impl TestStruct {
    fn new() -> Self {
        TestStruct { value: 42 }
    }
}
"""
        )

        result = processor.process_file(rust_file)

        assert result["file_path"] == str(rust_file)
        assert result["file_type"] == "rust"
        assert result["functions_count"] >= 1
        assert result["structs_count"] >= 1
        assert result["lines_count"] > 0

    def test_process_unsupported_file(self):
        """Test processing unsupported file types."""
        processor = FileProcessorService()

        # Create unsupported file type
        text_file = self.test_dir / "test.txt"
        text_file.write_text("This is a plain text file.")

        result = processor.process_file(text_file)

        assert result["file_path"] == str(text_file)
        assert result["file_type"] == "text"
        assert result["functions_count"] == 0
        assert result["classes_count"] == 0
        assert result["lines_count"] > 0

    def test_process_nonexistent_file(self):
        """Test processing non-existent files."""
        processor = FileProcessorService()

        nonexistent_file = self.test_dir / "nonexistent.py"

        with pytest.raises(FileNotFoundError):
            processor.process_file(nonexistent_file)

    def test_process_empty_file(self):
        """Test processing empty files."""
        processor = FileProcessorService()

        empty_file = self.test_dir / "empty.py"
        empty_file.touch()

        result = processor.process_file(empty_file)

        assert result["file_path"] == str(empty_file)
        assert result["lines_count"] == 0
        assert result["size_bytes"] == 0
        assert result["functions_count"] == 0
        assert result["classes_count"] == 0

    def test_process_file_with_syntax_errors(self):
        """Test processing files with syntax errors."""
        processor = FileProcessorService()

        # Create file with syntax errors
        error_file = self.test_dir / "error.py"
        error_file.write_text(
            """
def broken_function(
    # Missing closing parenthesis and colon
    pass
"""
        )

        result = processor.process_file(error_file)

        assert result["file_path"] == str(error_file)
        assert result["has_syntax_errors"] is True
        assert "error_details" in result

    def test_get_file_stats(self):
        """Test getting comprehensive file statistics."""
        processor = FileProcessorService()

        # Create multiple test files
        files = []
        for i in range(3):
            test_file = self.test_dir / f"test_{i}.py"
            test_file.write_text(f"def function_{i}():\n    pass\n")
            files.append(test_file)

        stats = processor.get_file_stats(files)

        assert stats["total_files"] == 3
        assert stats["total_lines"] >= 6
        assert stats["total_functions"] >= 3
        assert stats["file_types"]["python"] == 3

    def test_calculate_complexity_score(self):
        """Test complexity score calculation."""
        processor = FileProcessorService()

        # Create complex Python file
        complex_file = self.test_dir / "complex.py"
        complex_file.write_text(
            """
def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                try:
                    result = i * 2
                except Exception:
                    continue
            else:
                while i > 0:
                    i -= 1
        return result
    else:
        return 0
"""
        )

        result = processor.process_file(complex_file)

        assert "complexity_score" in result
        assert result["complexity_score"] > 1
        assert result["complexity_level"] in ["low", "medium", "high", "very_high"]

    def test_extract_imports(self):
        """Test import extraction functionality."""
        processor = FileProcessorService()

        # Create file with imports
        import_file = self.test_dir / "imports.py"
        import_file.write_text(
            """
import os
import sys
from pathlib import Path
from typing import Dict, List
import json as js
"""
        )

        result = processor.process_file(import_file)

        assert "imports" in result
        assert len(result["imports"]) >= 5
        assert "os" in [imp["module"] for imp in result["imports"]]
        assert "pathlib.Path" in [imp["name"] for imp in result["imports"]]

    def test_detect_todo_fixme_comments(self):
        """Test detection of TODO and FIXME comments."""
        processor = FileProcessorService()

        # Create file with TODO/FIXME comments
        todo_file = self.test_dir / "todo.py"
        todo_file.write_text(
            """
def function():
    # TODO: Implement this function
    pass

def another_function():
    # FIXME: This has a bug
    # BUG: Another issue here
    return None
"""
        )

        result = processor.process_file(todo_file)

        assert "work_items" in result
        assert len(result["work_items"]) >= 3
        todo_types = [item["type"] for item in result["work_items"]]
        assert "TODO" in todo_types
        assert "FIXME" in todo_types
        assert "BUG" in todo_types

    def test_process_file_with_encoding_issues(self):
        """Test processing files with encoding issues."""
        processor = FileProcessorService()

        # Create file with special characters
        encoding_file = self.test_dir / "encoding.py"
        encoding_file.write_text(
            '# -*- coding: utf-8 -*-\ndef função():\n    return "café"\n',
            encoding="utf-8",
        )

        result = processor.process_file(encoding_file)

        assert result["file_path"] == str(encoding_file)
        assert result["encoding"] == "utf-8"
        assert result["functions_count"] >= 1

    def test_batch_processing(self):
        """Test batch processing of multiple files."""
        processor = FileProcessorService()

        # Create multiple files
        files = []
        for i in range(5):
            test_file = self.test_dir / f"batch_{i}.py"
            test_file.write_text(f"def function_{i}():\n    return {i}\n")
            files.append(test_file)

        results = processor.process_files_batch(files)

        assert len(results) == 5
        for result in results:
            assert "file_path" in result
            assert "functions_count" in result
            assert result["functions_count"] >= 1

    def test_performance_metrics(self):
        """Test performance metrics collection."""
        processor = FileProcessorService()

        test_file = self.test_dir / "perf.py"
        test_file.write_text("def test():\n    pass\n")

        result = processor.process_file(test_file)

        assert "processing_time_ms" in result
        assert result["processing_time_ms"] >= 0
        assert "memory_usage_bytes" in result

    def test_file_caching(self):
        """Test file processing caching mechanism."""
        processor = FileProcessorService()

        test_file = self.test_dir / "cache.py"
        test_file.write_text("def cached_function():\n    pass\n")

        # First processing
        result1 = processor.process_file(test_file)

        # Second processing (should use cache)
        result2 = processor.process_file(test_file, use_cache=True)

        assert result1["file_path"] == result2["file_path"]
        assert result1["functions_count"] == result2["functions_count"]
        assert result2["from_cache"] is True
