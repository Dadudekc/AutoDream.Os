import tempfile
from pathlib import Path

import pytest

from .code_crafter_support import CodeCrafter


@pytest.fixture
def temp_code_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    import shutil

    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_python_code():
    return '''"""
Sample Python code for testing
"""

def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    """Main function."""
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")

if __name__ == "__main__":
    main()
'''


class TestCodeCrafterValidation:
    """Tests for code analysis and helper methods."""

    @pytest.mark.unit
    def test_analyze_code(self, temp_code_dir, sample_python_code):
        code_file = temp_code_dir / "test_code.py"
        code_file.write_text(sample_python_code)

        crafter = CodeCrafter()
        analysis = crafter.analyze_code(str(code_file))

        assert analysis.file_path == str(code_file)
        assert analysis.complexity_score > 0
        assert analysis.maintainability_index > 0
        assert isinstance(analysis.code_smells, list)
        assert isinstance(analysis.suggestions, list)
        assert isinstance(analysis.security_issues, list)
        assert isinstance(analysis.performance_issues, list)
        assert analysis.documentation_coverage >= 0
        assert analysis.test_coverage == 0.0

    @pytest.mark.unit
    def test_analyze_code_file_not_found(self):
        crafter = CodeCrafter()
        with pytest.raises(FileNotFoundError):
            crafter.analyze_code("nonexistent_file.py")

    @pytest.mark.unit
    def test_calculate_complexity(self):
        crafter = CodeCrafter()
        code = "def test():\n    if True:\n        for i in range(10):\n            pass"
        complexity = crafter._calculate_complexity(code)
        assert complexity > 0
        assert isinstance(complexity, float)

    @pytest.mark.unit
    def test_extract_dependencies_python(self):
        crafter = CodeCrafter()
        code = "import os\nimport sys\nfrom flask import Flask"
        dependencies = crafter._extract_dependencies(code, "python")
        assert "os" in dependencies
        assert "sys" in dependencies
        assert "flask" in dependencies

    @pytest.mark.unit
    def test_extract_dependencies_javascript(self):
        crafter = CodeCrafter()
        code = "const express = require('express');\nconst fs = require('fs');"
        dependencies = crafter._extract_dependencies(code, "javascript")
        assert "express" in dependencies
        assert "fs" in dependencies

    @pytest.mark.unit
    def test_detect_code_smells(self):
        crafter = CodeCrafter()
        code = "def very_long_function():\n" + "\n".join(["    pass"] * 60)
        smells = crafter._detect_code_smells(code)
        assert "Long function detected" in str(smells)

    @pytest.mark.unit
    def test_check_security_issues(self):
        crafter = CodeCrafter()
        code = "password = 'secret123'"
        issues = crafter._check_security_issues(code)
        assert "hardcoded secrets" in str(issues).lower()

    @pytest.mark.unit
    def test_check_performance_issues(self):
        crafter = CodeCrafter()
        code = "for i in range(100):\n    for j in range(100):\n        pass"
        issues = crafter._check_performance_issues(code)
        assert "Nested loops" in str(issues)

    @pytest.mark.unit
    def test_calculate_documentation_coverage(self):
        crafter = CodeCrafter()
        code = '"""Docstring"""\ndef test():\n    # Comment\n    pass'
        coverage = crafter._calculate_documentation_coverage(code)
        assert coverage > 0
        assert coverage <= 100
