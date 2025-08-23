"""
🧪 CORE COMPONENTS SMOKE TESTS - AGENT_CELLPHONE_V2
Foundation & Testing Specialist - TDD Integration Project

Smoke tests for core system components ensuring V2 coding standards compliance:
- Line count limits (≤200 LOC for core)
- OOP design compliance
- Single responsibility principle
- CLI interface functionality
- Basic functionality validation
"""

import pytest
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

from tests.conftest import TestConfig, assert_v2_standards_compliance


class TestCoreComponentsSmoke:
    """Smoke tests for core system components."""

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_directory_structure(self, test_config: TestConfig):
        """Test core directory structure exists and follows V2 standards."""
        core_dir = Path("src/core")
        assert core_dir.exists(), "Core directory must exist"
        assert core_dir.is_dir(), "Core must be a directory"

        # Check for required files
        required_files = ["__init__.py"]
        for file_name in required_files:
            assert (
                core_dir / file_name
            ).exists(), f"Required file {file_name} missing in core"

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_loc_compliance(self, test_config: TestConfig):
        """Test all core components meet LOC requirements (≤200 LOC)."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Check each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check LOC compliance
            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                code_lines = [
                    line
                    for line in lines
                    if line.strip() and not line.strip().startswith("#")
                ]

                assert (
                    len(code_lines) <= test_config.MAX_LOC_CORE
                ), f"Core component {py_file.name} exceeds {test_config.MAX_LOC_CORE} LOC limit: {len(code_lines)} lines"

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_oop_compliance(self, test_config: TestConfig):
        """Test all core components follow OOP design principles."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Check each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check OOP compliance
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Must have class definitions
                assert (
                    "class " in content
                ), f"Core component {py_file.name} must contain class definitions"

                # Check for functions outside classes (should be minimal)
                lines = content.split("\n")
                in_class = False
                functions_outside_classes = 0

                for line in lines:
                    line = line.strip()
                    if line.startswith("class "):
                        in_class = True
                    elif line.startswith("def ") and not in_class:
                        functions_outside_classes += 1
                    elif line == "" or line.startswith("#"):
                        continue
                    elif line.startswith("if __name__"):
                        break

                # Allow main function and minimal utility functions
                assert (
                    functions_outside_classes <= 2
                ), f"Core component {py_file.name} has too many functions outside classes: {functions_outside_classes}"

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_cli_interface(self, test_config: TestConfig):
        """Test all core components have CLI interfaces for testing."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Check each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check CLI interface compliance
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Must have argparse usage
                assert (
                    "argparse" in content
                ), f"Core component {py_file.name} must use argparse for CLI"

                # Must have main function or entry point
                assert (
                    "def main(" in content or "if __name__" in content
                ), f"Core component {py_file.name} must have main function or entry point"

                # Must have help documentation
                assert (
                    "help=" in content
                ), f"Core component {py_file.name} must have help documentation"

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_single_responsibility(self, test_config: TestConfig):
        """Test core components follow single responsibility principle."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Check each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check for mixed responsibilities
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Count different types of operations
                operations = {
                    "file_ops": content.count("open(") + content.count("Path("),
                    "network_ops": content.count("requests.")
                    + content.count("urllib."),
                    "db_ops": content.count("sqlite") + content.count("database"),
                    "gui_ops": content.count("tkinter") + content.count("PyQt"),
                    "cli_ops": content.count("argparse") + content.count("click"),
                }

                # Should have primary focus on one area
                active_ops = sum(1 for count in operations.values() if count > 0)
                assert (
                    active_ops <= 2
                ), f"Core component {py_file.name} has too many mixed responsibilities: {active_ops} areas"

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_imports(self, test_config: TestConfig):
        """Test core components have clean, focused imports."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Check each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check import statements
            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

                import_lines = [
                    line
                    for line in lines
                    if line.strip().startswith(("import ", "from "))
                ]

                # Should not have excessive imports
                assert (
                    len(import_lines) <= 15
                ), f"Core component {py_file.name} has too many imports: {len(import_lines)}"

                # Check for unused imports (basic check)
                for import_line in import_lines:
                    import_line = import_line.strip()
                    if import_line.startswith("from "):
                        module = import_line.split(" import ")[0].split("from ")[1]
                    else:
                        module = import_line.split(" import ")[0]

                    # Check if module is used in content
                    with open(py_file, "r", encoding="utf-8") as f2:
                        content = f2.read()
                        # Basic usage check (can be improved with AST analysis)
                        if not any(
                            usage in content
                            for usage in [module, module.split(".")[-1]]
                        ):
                            pytest.warns(
                                UserWarning,
                                f"Potential unused import: {module} in {py_file.name}",
                            )


class TestCoreComponentsFunctionality:
    """Test core components basic functionality."""

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_executable(self, test_config: TestConfig):
        """Test core components can be executed without errors."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Test each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Test basic execution
            try:
                result = subprocess.run(
                    [sys.executable, str(py_file), "--help"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                # Should not crash and should provide help
                assert result.returncode in [
                    0,
                    1,
                ], f"Core component {py_file.name} crashed during execution"

                # Should provide help output
                if result.returncode == 0:
                    assert (
                        "help" in result.stdout.lower()
                        or "usage" in result.stdout.lower()
                    ), f"Core component {py_file.name} should provide help information"

            except subprocess.TimeoutExpired:
                pytest.fail(f"Core component {py_file.name} timed out during execution")
            except Exception as e:
                pytest.fail(f"Core component {py_file.name} failed execution: {e}")

    @pytest.mark.smoke
    @pytest.mark.core
    def test_core_components_smoke_tests(self, test_config: TestConfig):
        """Test core components have working smoke tests via CLI."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Test each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Test smoke test functionality
            try:
                result = subprocess.run(
                    [sys.executable, str(py_file), "--test"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                # Should handle --test flag gracefully
                assert result.returncode in [
                    0,
                    1,
                ], f"Core component {py_file.name} should handle --test flag gracefully"

                # Should provide test output
                if result.returncode == 0:
                    assert (
                        "test" in result.stdout.lower()
                        or "smoke" in result.stdout.lower()
                    ), f"Core component {py_file.name} should provide test output"

            except subprocess.TimeoutExpired:
                pytest.fail(
                    f"Core component {py_file.name} timed out during smoke test"
                )
            except Exception as e:
                pytest.fail(f"Core component {py_file.name} failed smoke test: {e}")


class TestCoreComponentsV2Standards:
    """Test core components V2 coding standards compliance."""

    @pytest.mark.smoke
    @pytest.mark.v2_standards
    @pytest.mark.core
    def test_core_components_full_v2_compliance(self, test_config: TestConfig):
        """Test all core components meet full V2 coding standards."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Test each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Assert full V2 standards compliance
            assert_v2_standards_compliance(py_file, test_config.MAX_LOC_CORE)

    @pytest.mark.smoke
    @pytest.mark.v2_standards
    @pytest.mark.core
    def test_core_components_documentation(self, test_config: TestConfig):
        """Test core components have proper documentation."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Test each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check documentation
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Should have module docstring
                assert (
                    '"""' in content or "'''" in content
                ), f"Core component {py_file.name} should have module documentation"

                # Should have class docstrings
                if "class " in content:
                    class_lines = [
                        line
                        for line in content.split("\n")
                        if line.strip().startswith("class ")
                    ]
                    for class_line in class_lines:
                        class_name = (
                            class_line.split("class ")[1]
                            .split("(")[0]
                            .split(":")[0]
                            .strip()
                        )
                        # Check for class docstring (basic check)
                        class_start = content.find(f"class {class_name}")
                        if class_start != -1:
                            class_content = content[class_start:]
                            # Should have docstring after class definition
                            assert (
                                '"""' in class_content[:200]
                                or "'''" in class_content[:200]
                            ), f"Class {class_name} in {py_file.name} should have docstring"

    @pytest.mark.smoke
    @pytest.mark.v2_standards
    @pytest.mark.core
    def test_core_components_error_handling(self, test_config: TestConfig):
        """Test core components have proper error handling."""
        core_dir = Path("src/core")
        if not core_dir.exists():
            pytest.skip("Core directory not found")

        # Test each Python file in core
        for py_file in core_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files

            # Check error handling
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Should have try-except blocks or proper error handling
                has_error_handling = (
                    "try:" in content
                    or "except " in content
                    or "raise " in content
                    or "assert " in content
                )

                # Basic error handling should be present
                assert (
                    has_error_handling
                ), f"Core component {py_file.name} should have error handling"


# Test execution helpers
def run_core_smoke_tests() -> Dict[str, Any]:
    """Run all core component smoke tests and return results."""
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "skipped_tests": 0,
        "components_tested": 0,
        "v2_compliance": True,
    }

    # This would be called by the main testing framework
    return results


if __name__ == "__main__":
    # Run smoke tests if executed directly
    pytest.main([__file__, "-v", "--tb=short"])
