#!/usr/bin/env python3
"""
Testing Infrastructure Manager - Agent Cellphone V2

Consolidates all testing infrastructure setup, configuration, and
management into a single system that eliminates duplication.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3G - Testing Infrastructure Cleanup
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .output_formatter import OutputFormatter


class DependencyStatus(Enum):
    """Dependency installation status"""
    INSTALLED = "installed"
    NOT_INSTALLED = "not_installed"
    FAILED = "failed"
    CHECKING = "checking"


@dataclass
class TestingDependency:
    """Testing dependency information"""
    name: str
    package_name: str
    version_constraint: str
    description: str
    critical: bool = True
    status: DependencyStatus = DependencyStatus.CHECKING
    installed_version: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TestDirectory:
    """Test directory configuration"""
    path: Path
    description: str
    required: bool = True
    exists: bool = False
    created: bool = False


class TestingInfrastructureManager:
    """
    Testing Infrastructure Manager - TASK 3G
    
    Consolidates all testing infrastructure setup and configuration,
    eliminating duplication across multiple setup scripts.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.output_formatter = OutputFormatter()
        
        # Core directories
        self.test_dir = project_root / "tests"
        self.src_dir = project_root / "src"
        self.results_dir = project_root / "test_results"
        self.coverage_dir = project_root / "htmlcov"
        self.fixtures_dir = project_root / "tests" / "fixtures"
        self.mocks_dir = project_root / "tests" / "mocks"
        
        # Dependencies
        self.testing_dependencies = self._initialize_dependencies()
        
        # Directory structure
        self.test_directories = self._initialize_directories()

    def _initialize_dependencies(self) -> List[TestingDependency]:
        """Initialize testing dependencies list"""
        return [
            TestingDependency(
                name="pytest",
                package_name="pytest",
                version_constraint=">=7.0.0",
                description="Core testing framework"
            ),
            TestingDependency(
                name="pytest-cov",
                package_name="pytest-cov",
                version_constraint=">=4.0.0",
                description="Coverage plugin for pytest"
            ),
            TestingDependency(
                name="pytest-mock",
                package_name="pytest-mock",
                version_constraint=">=3.10.0",
                description="Mocking support for pytest"
            ),
            TestingDependency(
                name="pytest-asyncio",
                package_name="pytest-asyncio",
                version_constraint=">=0.21.0",
                description="Async support for pytest"
            ),
            TestingDependency(
                name="pytest-html",
                package_name="pytest-html",
                version_constraint=">=3.1.0",
                description="HTML reporting for pytest"
            ),
            TestingDependency(
                name="pytest-xdist",
                package_name="pytest-xdist",
                version_constraint=">=3.0.0",
                description="Parallel test execution"
            ),
            TestingDependency(
                name="coverage",
                package_name="coverage",
                version_constraint=">=7.0.0",
                description="Code coverage measurement"
            ),
            TestingDependency(
                name="coverage-badge",
                package_name="coverage-badge",
                version_constraint=">=1.1.0",
                description="Coverage badge generation"
            ),
            TestingDependency(
                name="black",
                package_name="black",
                version_constraint=">=23.0.0",
                description="Code formatting"
            ),
            TestingDependency(
                name="flake8",
                package_name="flake8",
                version_constraint=">=6.0.0",
                description="Code linting"
            ),
            TestingDependency(
                name="mypy",
                package_name="mypy",
                version_constraint=">=1.0.0",
                description="Type checking"
            ),
            TestingDependency(
                name="isort",
                package_name="isort",
                version_constraint=">=5.12.0",
                description="Import sorting"
            ),
            TestingDependency(
                name="factory-boy",
                package_name="factory-boy",
                version_constraint=">=3.2.0",
                description="Test data factories"
            ),
            TestingDependency(
                name="faker",
                package_name="faker",
                version_constraint=">=18.0.0",
                description="Fake data generation"
            ),
            TestingDependency(
                name="responses",
                package_name="responses",
                version_constraint=">=0.23.0",
                description="HTTP response mocking"
            ),
            TestingDependency(
                name="freezegun",
                package_name="freezegun",
                version_constraint=">=1.2.0",
                description="Time mocking for tests"
            ),
            TestingDependency(
                name="pytest-benchmark",
                package_name="pytest-benchmark",
                version_constraint=">=4.0.0",
                description="Performance benchmarking"
            ),
            TestingDependency(
                name="bandit",
                package_name="bandit",
                version_constraint=">=1.7.0",
                description="Security linting"
            ),
            TestingDependency(
                name="safety",
                package_name="safety",
                version_constraint=">=2.3.0",
                description="Security vulnerability checking"
            )
        ]

    def _initialize_directories(self) -> List[TestDirectory]:
        """Initialize test directory configurations"""
        return [
            TestDirectory(
                path=self.test_dir,
                description="Main test directory"
            ),
            TestDirectory(
                path=self.test_dir / "smoke",
                description="Smoke tests"
            ),
            TestDirectory(
                path=self.test_dir / "unit",
                description="Unit tests"
            ),
            TestDirectory(
                path=self.test_dir / "integration",
                description="Integration tests"
            ),
            TestDirectory(
                path=self.test_dir / "performance",
                description="Performance tests"
            ),
            TestDirectory(
                path=self.test_dir / "security",
                description="Security tests"
            ),
            TestDirectory(
                path=self.fixtures_dir,
                description="Test fixtures"
            ),
            TestDirectory(
                path=self.mocks_dir,
                description="Test mocks"
            ),
            TestDirectory(
                path=self.results_dir,
                description="Test results"
            ),
            TestDirectory(
                path=self.coverage_dir,
                description="Coverage reports"
            )
        ]

    def setup_infrastructure(self) -> bool:
        """Setup complete testing infrastructure"""
        self.output_formatter.print_banner(str(self.project_root))
        self.output_formatter.print_info("Setting up testing infrastructure...")
        
        try:
            # Check current status
            self._check_current_status()
            
            # Install dependencies
            if not self._install_dependencies():
                return False
            
            # Create directory structure
            if not self._create_directory_structure():
                return False
            
            # Create configuration files
            if not self._create_configuration_files():
                return False
            
            # Validate setup
            if not self._validate_setup():
                return False
            
            self.output_formatter.print_success("Testing infrastructure setup completed successfully!")
            return True
            
        except Exception as e:
            self.output_formatter.print_error(f"Infrastructure setup failed: {e}")
            return False

    def _check_current_status(self) -> None:
        """Check current infrastructure status"""
        self.output_formatter.print_info("Checking current infrastructure status...")
        
        # Check dependencies
        self._check_dependencies()
        
        # Check directories
        self._check_directories()
        
        # Display status summary
        self._display_status_summary()

    def _check_dependencies(self) -> None:
        """Check dependency installation status"""
        self.output_formatter.print_info("Checking dependencies...")
        
        for dependency in self.testing_dependencies:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "show", dependency.package_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # Extract version from output
                    lines = result.stdout.split('\n')
                    version = None
                    for line in lines:
                        if line.startswith('Version:'):
                            version = line.split(':', 1)[1].strip()
                            break
                    
                    dependency.status = DependencyStatus.INSTALLED
                    dependency.installed_version = version
                    
                else:
                    dependency.status = DependencyStatus.NOT_INSTALLED
                    
            except Exception as e:
                dependency.status = DependencyStatus.FAILED
                dependency.error_message = str(e)

    def _check_directories(self) -> None:
        """Check directory existence"""
        for directory in self.test_directories:
            directory.exists = directory.path.exists()

    def _display_status_summary(self) -> None:
        """Display current status summary"""
        installed_deps = sum(1 for d in self.testing_dependencies if d.status == DependencyStatus.INSTALLED)
        total_deps = len(self.testing_dependencies)
        
        existing_dirs = sum(1 for d in self.test_directories if d.exists)
        total_dirs = len(self.test_directories)
        
        self.output_formatter.print_info(f"Dependencies: {installed_deps}/{total_deps} installed")
        self.output_formatter.print_info(f"Directories: {existing_dirs}/{total_dirs} exist")

    def _install_dependencies(self) -> bool:
        """Install missing dependencies"""
        missing_deps = [d for d in self.testing_dependencies if d.status != DependencyStatus.INSTALLED]
        
        if not missing_deps:
            self.output_formatter.print_success("All dependencies already installed!")
            return True
        
        self.output_formatter.print_info(f"Installing {len(missing_deps)} missing dependencies...")
        
        for dependency in missing_deps:
            if not self._install_dependency(dependency):
                if dependency.critical:
                    self.output_formatter.print_error(f"Critical dependency {dependency.name} failed to install")
                    return False
                else:
                    self.output_formatter.print_warning(f"Non-critical dependency {dependency.name} failed to install")
        
        return True

    def _install_dependency(self, dependency: TestingDependency) -> bool:
        """Install a single dependency"""
        self.output_formatter.print_info(f"Installing {dependency.name}...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", f"{dependency.package_name}{dependency.version_constraint}"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300
            )
            
            if result.returncode == 0:
                dependency.status = DependencyStatus.INSTALLED
                self.output_formatter.print_success(f"✅ {dependency.name} installed successfully")
                return True
            else:
                dependency.status = DependencyStatus.FAILED
                dependency.error_message = result.stderr
                self.output_formatter.print_error(f"❌ Failed to install {dependency.name}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            dependency.status = DependencyStatus.FAILED
            dependency.error_message = "Installation timed out"
            self.output_formatter.print_error(f"❌ {dependency.name} installation timed out")
            return False
        except Exception as e:
            dependency.status = DependencyStatus.FAILED
            dependency.error_message = str(e)
            self.output_formatter.print_error(f"❌ Error installing {dependency.name}: {e}")
            return False

    def _create_directory_structure(self) -> bool:
        """Create test directory structure"""
        self.output_formatter.print_info("Creating directory structure...")
        
        try:
            for directory in self.test_directories:
                if not directory.exists:
                    directory.path.mkdir(parents=True, exist_ok=True)
                    directory.created = True
                    self.output_formatter.print_success(f"✅ Created directory: {directory.path}")
                else:
                    self.output_formatter.print_info(f"📁 Directory exists: {directory.path}")
            
            return True
            
        except Exception as e:
            self.output_formatter.print_error(f"Failed to create directories: {e}")
            return False

    def _create_configuration_files(self) -> bool:
        """Create essential configuration files"""
        self.output_formatter.print_info("Creating configuration files...")
        
        try:
            # Create conftest.py
            conftest_file = self.test_dir / "conftest.py"
            if not conftest_file.exists():
                self._create_conftest_file(conftest_file)
            
            # Create pytest.ini
            pytest_ini = self.project_root / "pytest.ini"
            if not pytest_ini.exists():
                self._create_pytest_ini(pytest_ini)
            
            # Create .coveragerc
            coverage_rc = self.project_root / ".coveragerc"
            if not coverage_rc.exists():
                self._create_coverage_rc(coverage_rc)
            
            return True
            
        except Exception as e:
            self.output_formatter.print_error(f"Failed to create configuration files: {e}")
            return False

    def _create_conftest_file(self, conftest_path: Path) -> None:
        """Create conftest.py file"""
        conftest_content = '''#!/usr/bin/env python3
"""
Test configuration and fixtures for Agent Cellphone V2

This file provides shared test configuration, fixtures, and utilities
for all tests in the project.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

@pytest.fixture(scope="session")
def project_root():
    """Provide project root directory"""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def src_directory():
    """Provide src directory"""
    return Path(__file__).parent.parent / "src"

@pytest.fixture(scope="session")
def tests_directory():
    """Provide tests directory"""
    return Path(__file__).parent
'''
        conftest_path.write_text(conftest_content)
        self.output_formatter.print_success(f"✅ Created conftest.py")

    def _create_pytest_ini(self, pytest_ini_path: Path) -> None:
        """Create pytest.ini file"""
        pytest_ini_content = '''[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    security: Security tests
    slow: Slow running tests
'''
        pytest_ini_path.write_text(pytest_ini_content)
        self.output_formatter.print_success(f"✅ Created pytest.ini")

    def _create_coverage_rc(self, coverage_rc_path: Path) -> None:
        """Create .coveragerc file"""
        coverage_rc_content = '''[run]
source = src
omit = 
    */tests/*
    */test_*
    */__pycache__/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\\bProtocol\\):
    @(abc\\.)?abstractmethod
'''
        coverage_rc_path.write_text(coverage_rc_content)
        self.output_formatter.print_success(f"✅ Created .coveragerc")

    def _validate_setup(self) -> bool:
        """Validate the complete setup"""
        self.output_formatter.print_info("Validating setup...")
        
        # Check dependencies again
        self._check_dependencies()
        
        # Check directories again
        self._check_directories()
        
        # Run basic validation
        if not self._run_basic_validation():
            return False
        
        self.output_formatter.print_success("Setup validation completed successfully!")
        return True

    def _run_basic_validation(self) -> bool:
        """Run basic validation tests"""
        try:
            # Test pytest import
            result = subprocess.run(
                [sys.executable, "-c", "import pytest; print('pytest available')"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.output_formatter.print_error("pytest import validation failed")
                return False
            
            # Test coverage import
            result = subprocess.run(
                [sys.executable, "-c", "import coverage; print('coverage available')"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.output_formatter.print_warning("coverage import validation failed")
            
            return True
            
        except Exception as e:
            self.output_formatter.print_error(f"Basic validation failed: {e}")
            return False

    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        return {
            "project_root": str(self.project_root),
            "dependencies": {
                "total": len(self.testing_dependencies),
                "installed": sum(1 for d in self.testing_dependencies if d.status == DependencyStatus.INSTALLED),
                "failed": sum(1 for d in self.testing_dependencies if d.status == DependencyStatus.FAILED),
                "missing": sum(1 for d in self.testing_dependencies if d.status == DependencyStatus.NOT_INSTALLED)
            },
            "directories": {
                "total": len(self.test_directories),
                "existing": sum(1 for d in self.test_directories if d.exists),
                "created": sum(1 for d in self.test_directories if d.created)
            },
            "setup_complete": all(d.status == DependencyStatus.INSTALLED for d in self.testing_dependencies if d.critical)
        }

    def cleanup(self) -> None:
        """Clean up testing infrastructure"""
        self.output_formatter.print_info("Cleaning up testing infrastructure...")
        
        try:
            # Clear any temporary files
            # Note: We don't remove installed dependencies or created directories
            # as they are part of the permanent infrastructure
            
            self.output_formatter.print_success("Cleanup completed")
            
        except Exception as e:
            self.output_formatter.print_error(f"Cleanup failed: {e}")


def main():
    """Main entry point for testing infrastructure manager"""
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Initialize manager
    manager = TestingInfrastructureManager(project_root)
    
    try:
        # Setup infrastructure
        success = manager.setup_infrastructure()
        
        if success:
            # Display final status
            status = manager.get_status_report()
            print(f"\n📊 Final Status:")
            print(f"   Dependencies: {status['dependencies']['installed']}/{status['dependencies']['total']} installed")
            print(f"   Directories: {status['directories']['existing']}/{status['directories']['total']} exist")
            print(f"   Setup Complete: {status['setup_complete']}")
            
            return 0
        else:
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

