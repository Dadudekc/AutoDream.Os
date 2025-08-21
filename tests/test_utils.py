"""
Test Utilities for Agent_Cellphone_V2_Repository
Foundation & Testing Specialist - TDD Integration Project

This module provides utility functions and helpers for testing,
including V2 standards compliance validation and common testing patterns.
"""

import ast
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from unittest.mock import Mock, patch, MagicMock
import pytest


class V2StandardsChecker:
    """Checker for V2 coding standards compliance."""
    
    # V2 Standards Constants
    MAX_LOC_STANDARD = 300
    MAX_LOC_GUI = 500
    MAX_LOC_CORE = 200
    
    def __init__(self):
        """Initialize the V2 standards checker."""
        self.violations = []
    
    def check_file_compliance(self, file_path: Path) -> Dict[str, Any]:
        """
        Check if a file complies with V2 coding standards.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            Dictionary with compliance results
        """
        if not file_path.exists():
            return {
                "compliant": False,
                "error": "File does not exist",
                "violations": ["File not found"]
            }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = f.readlines()
        except Exception as e:
            return {
                "compliant": False,
                "error": f"Could not read file: {e}",
                "violations": [f"File read error: {e}"]
            }
        
        # Reset violations for this file
        self.violations = []
        
        # Check each standard
        loc_compliant = self._check_line_count(file_path, lines)
        oop_compliant = self._check_oop_design(content)
        cli_compliant = self._check_cli_interface(content)
        srp_compliant = self._check_single_responsibility(content)
        
        # Determine overall compliance
        overall_compliant = all([
            loc_compliant,
            oop_compliant,
            cli_compliant,
            srp_compliant
        ])
        
        return {
            "compliant": overall_compliant,
            "file_path": str(file_path),
            "line_count": len(lines),
            "standards": {
                "line_count": loc_compliant,
                "oop_design": oop_compliant,
                "cli_interface": cli_compliant,
                "single_responsibility": srp_compliant
            },
            "violations": self.violations.copy(),
            "recommendations": self._generate_recommendations()
        }
    
    def _check_line_count(self, file_path: Path, lines: List[str]) -> bool:
        """Check if file meets LOC requirements."""
        # Count non-empty, non-comment lines
        code_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                code_lines.append(line)
        
        line_count = len(code_lines)
        
        # Determine appropriate limit based on file type
        if 'gui' in file_path.name.lower() or 'ui' in file_path.name.lower():
            max_lines = self.MAX_LOC_GUI
            limit_type = "GUI"
        elif file_path.parent.name in ['core', 'src']:
            max_lines = self.MAX_LOC_CORE
            limit_type = "Core"
        else:
            max_lines = self.MAX_LOC_STANDARD
            limit_type = "Standard"
        
        if line_count > max_lines:
            self.violations.append(
                f"Line count ({line_count}) exceeds {limit_type} limit ({max_lines})"
            )
            return False
        
        return True
    
    def _check_oop_design(self, content: str) -> bool:
        """Check if file follows OOP design principles."""
        try:
            tree = ast.parse(content)
            
            # Check for class definitions
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            if not classes:
                self.violations.append("No class definitions found (OOP requirement)")
                return False
            
            # Check for functions outside classes
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            functions_outside_classes = []
            
            for func in functions:
                # Check if function is defined at module level
                if not any(func in ast.walk(cls) for cls in classes):
                    functions_outside_classes.append(func.name)
            
            # Allow main function and CLI interface functions
            allowed_functions = ['main', 'cli', 'run', 'execute']
            functions_outside_classes = [
                f for f in functions_outside_classes 
                if f not in allowed_functions
            ]
            
            if functions_outside_classes:
                self.violations.append(
                    f"Functions outside classes: {', '.join(functions_outside_classes)}"
                )
                return False
            
            return True
            
        except SyntaxError as e:
            self.violations.append(f"Syntax error in file: {e}")
            return False
    
    def _check_cli_interface(self, content: str) -> bool:
        """Check if file has CLI interface for testing."""
        # Check for argparse usage
        if 'argparse' not in content:
            self.violations.append("No argparse import found (CLI requirement)")
            return False
        
        # Check for main function or CLI entry point
        if 'def main(' not in content and 'if __name__' not in content:
            self.violations.append("No main function or entry point found (CLI requirement)")
            return False
        
        # Check for argument parsing
        if 'add_argument' not in content:
            self.violations.append("No argument parsing found (CLI requirement)")
            return False
        
        # Check for help documentation
        if 'help=' not in content:
            self.violations.append("No help documentation found (CLI requirement)")
            return False
        
        return True
    
    def _check_single_responsibility(self, content: str) -> bool:
        """Check if classes follow single responsibility principle."""
        try:
            tree = ast.parse(content)
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            for cls in classes:
                # Count methods in class
                methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
                
                # Check if class has too many methods (potential SRP violation)
                if len(methods) > 15:  # Arbitrary threshold
                    self.violations.append(
                        f"Class '{cls.name}' has {len(methods)} methods (potential SRP violation)"
                    )
                    return False
                
                # Check method names for mixed responsibilities
                method_names = [method.name.lower() for method in methods]
                responsibility_groups = {
                    'data': ['get', 'set', 'save', 'load', 'store', 'retrieve'],
                    'validation': ['validate', 'check', 'verify', 'ensure'],
                    'processing': ['process', 'transform', 'convert', 'format'],
                    'communication': ['send', 'receive', 'connect', 'disconnect'],
                    'management': ['start', 'stop', 'init', 'cleanup']
                }
                
                # Count methods per responsibility group
                responsibility_counts = {}
                for group, keywords in responsibility_groups.items():
                    count = sum(1 for name in method_names if any(kw in name for kw in keywords))
                    if count > 0:
                        responsibility_counts[group] = count
                
                # If class has methods from too many responsibility groups, flag it
                if len(responsibility_counts) > 3:
                    self.violations.append(
                        f"Class '{cls.name}' handles multiple responsibilities: {list(responsibility_counts.keys())}"
                    )
                    return False
            
            return True
            
        except SyntaxError as e:
            self.violations.append(f"Syntax error in SRP check: {e}")
            return False
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for fixing violations."""
        recommendations = []
        
        for violation in self.violations:
            if "Line count" in violation:
                recommendations.append("Consider refactoring into smaller, focused modules")
            elif "No class definitions" in violation:
                recommendations.append("Restructure code to use proper OOP design with classes")
            elif "Functions outside classes" in violation:
                recommendations.append("Move functions into appropriate classes or create utility classes")
            elif "No argparse" in violation:
                recommendations.append("Add argparse import and CLI interface for testing")
            elif "No main function" in violation:
                recommendations.append("Add main function or entry point for CLI testing")
            elif "No argument parsing" in violation:
                recommendations.append("Implement argument parsing with add_argument calls")
            elif "No help documentation" in violation:
                recommendations.append("Add help text to all CLI arguments")
            elif "SRP violation" in violation:
                recommendations.append("Split class into smaller, focused classes with single responsibilities")
            elif "multiple responsibilities" in violation:
                recommendations.append("Refactor class to focus on a single, well-defined responsibility")
        
        return recommendations


class TestDataFactory:
    """Factory for creating test data and mock objects."""
    
    @staticmethod
    def create_mock_agent(agent_id: str = "test_agent_001", **kwargs) -> Mock:
        """Create a mock agent with realistic data."""
        agent = Mock()
        agent.agent_id = agent_id
        agent.name = kwargs.get('name', f"Test Agent {agent_id}")
        agent.type = kwargs.get('type', 'testing')
        agent.status = kwargs.get('status', 'active')
        agent.health_score = kwargs.get('health_score', 95)
        agent.capabilities = kwargs.get('capabilities', ['testing', 'validation'])
        agent.last_heartbeat = kwargs.get('last_heartbeat', '2025-08-20T12:00:00Z')
        
        # Mock methods
        agent.initialize.return_value = True
        agent.get_status.return_value = agent.status
        agent.get_health_score.return_value = agent.health_score
        agent.execute_task.return_value = {"success": True, "task_id": "test_task_001"}
        
        return agent
    
    @staticmethod
    def create_mock_workflow(workflow_id: str = "test_workflow_001", **kwargs) -> Mock:
        """Create a mock workflow with realistic data."""
        workflow = Mock()
        workflow.workflow_id = workflow_id
        workflow.name = kwargs.get('name', f"Test Workflow {workflow_id}")
        workflow.status = kwargs.get('status', 'running')
        workflow.steps = kwargs.get('steps', [
            {"id": 1, "name": "Initialize", "status": "completed"},
            {"id": 2, "name": "Process", "status": "running"},
            {"id": 3, "name": "Validate", "status": "pending"}
        ])
        
        # Mock methods
        workflow.get_status.return_value = workflow.status
        workflow.get_current_step.return_value = workflow.steps[1]
        workflow.execute_step.return_value = {"success": True, "step_id": 2}
        
        return workflow
    
    @staticmethod
    def create_mock_performance_metrics(**kwargs) -> Dict[str, Any]:
        """Create mock performance metrics."""
        return {
            "cpu_usage": kwargs.get('cpu_usage', 45.2),
            "memory_usage": kwargs.get('memory_usage', 67.8),
            "response_time": kwargs.get('response_time', 125),
            "error_rate": kwargs.get('error_rate', 0.02),
            "throughput": kwargs.get('throughput', 1500),
            "timestamp": kwargs.get('timestamp', '2025-08-20T12:00:00Z')
        }


class TestAssertions:
    """Custom assertion methods for testing."""
    
    @staticmethod
    def assert_v2_compliance(file_path: Path, max_loc: int = V2StandardsChecker.MAX_LOC_CORE):
        """Assert that a file complies with V2 standards."""
        checker = V2StandardsChecker()
        result = checker.check_file_compliance(file_path)
        
        assert result["compliant"], (
            f"File {file_path} does not comply with V2 standards:\n"
            f"Violations: {result['violations']}\n"
            f"Recommendations: {result['recommendations']}"
        )
    
    @staticmethod
    def assert_cli_interface(file_path: Path):
        """Assert that a file has a CLI interface."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'argparse' in content, f"File {file_path} must import argparse"
        assert 'def main(' in content or 'if __name__' in content, f"File {file_path} must have main function or entry point"
        assert 'add_argument' in content, f"File {file_path} must have argument parsing"
        assert 'help=' in content, f"File {file_path} must have help documentation"
    
    @staticmethod
    def assert_oop_design(file_path: Path):
        """Assert that a file follows OOP design principles."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'class ' in content, f"File {file_path} must contain class definitions"
        
        # Check for functions outside classes (excluding main and CLI functions)
        lines = content.split('\n')
        in_class = False
        functions_outside_classes = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('class '):
                in_class = True
            elif stripped.startswith('def ') and not in_class:
                func_name = stripped.split('(')[0].split()[-1]
                if func_name not in ['main', 'cli', 'run', 'execute']:
                    functions_outside_classes.append(func_name)
            elif stripped == '' or stripped.startswith('#'):
                continue
            elif stripped.startswith('if __name__'):
                break
        
        assert not functions_outside_classes, (
            f"File {file_path} has functions outside classes: {functions_outside_classes}"
        )


# Pytest fixtures for common testing patterns
@pytest.fixture
def v2_checker():
    """Provide V2 standards checker for testing."""
    return V2StandardsChecker()


@pytest.fixture
def test_data_factory():
    """Provide test data factory for testing."""
    return TestDataFactory()


@pytest.fixture
def test_assertions():
    """Provide custom test assertions for testing."""
    return TestAssertions()


# Utility functions for testing
def create_temp_test_file(content: str, filename: str = "test_file.py") -> Path:
    """Create a temporary test file with specified content."""
    import tempfile
    temp_dir = tempfile.mkdtemp()
    file_path = Path(temp_dir) / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def cleanup_temp_files(*file_paths: Path):
    """Clean up temporary test files."""
    import shutil
    for file_path in file_paths:
        if file_path.exists():
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)


def mock_environment_variables(**env_vars):
    """Context manager for mocking environment variables."""
    original_env = os.environ.copy()
    
    try:
        os.environ.update(env_vars)
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)


def assert_file_structure(directory: Path, expected_structure: Dict[str, Any]):
    """
    Assert that a directory has the expected file structure.
    
    Args:
        directory: Directory to check
        expected_structure: Dictionary describing expected structure
            Example: {
                "src": {"__init__.py": "file", "core": "dir"},
                "tests": {"test_*.py": "pattern"}
            }
    """
    for path, expected_type in expected_structure.items():
        full_path = directory / path
        
        if expected_type == "file":
            assert full_path.is_file(), f"Expected file: {full_path}"
        elif expected_type == "dir":
            assert full_path.is_dir(), f"Expected directory: {full_path}"
        elif expected_type == "pattern":
            # Pattern matching (e.g., "test_*.py")
            matching_files = list(directory.glob(path))
            assert matching_files, f"Expected files matching pattern: {path}"
        else:
            raise ValueError(f"Unknown expected type: {expected_type}")


# CLI testing utilities
def run_cli_command(script_path: Path, args: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """
    Run a CLI script with arguments and capture output.

    Args:
        script_path: Path to the script to run
        args: List of command line arguments
        cwd: Working directory for execution

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    import subprocess
    
    cmd = [sys.executable, str(script_path)] + args
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or script_path.parent
    )
    
    return result.returncode, result.stdout, result.stderr


def assert_cli_help(script_path: Path, expected_help_text: List[str] = None):
    """Assert that a CLI script provides help information."""
    return_code, stdout, stderr = run_cli_command(script_path, ["--help"])
    
    assert return_code == 0, f"Help command failed with return code {return_code}"
    assert "usage:" in stdout.lower() or "help" in stdout.lower(), "Help output not found"
    
    if expected_help_text:
        for text in expected_help_text:
            assert text in stdout, f"Expected help text not found: {text}"


def assert_cli_version(script_path: Path, expected_version: str = None):
    """Assert that a CLI script provides version information."""
    return_code, stdout, stderr = run_cli_command(script_path, ["--version"])
    
    # Version command should succeed or fail gracefully
    assert return_code in [0, 1], f"Version command failed unexpectedly with return code {return_code}"
