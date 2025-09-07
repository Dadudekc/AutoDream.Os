#!/usr/bin/env python3
"""
Unified Test Configuration System V2 - Agent Cellphone V2
=======================================================

V2-compliant test configuration system (under 500 lines).
Uses modular components from tests/core/ to achieve compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
import json
import yaml

# Import modular components
from .core import TestEnvironment, TestLevel, TestType


@dataclass
class TestCategoryConfig:
    """Test category configuration."""
    name: str
    description: str
    marker: str
    timeout: int
    level: TestLevel
    directory: str
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    parallel: bool = False
    retry_count: int = 0
    coverage_required: bool = True
    min_coverage: float = 80.0


@dataclass
class StandardsConfig:
    """V2 standards configuration."""
    max_loc_standard: int = 400
    max_loc_gui: int = 600
    max_loc_core: int = 400
    max_loc_services: int = 400
    max_loc_utils: int = 300
    max_loc_launchers: int = 400
    
    components: Dict[str, str] = field(default_factory=lambda: {
        "core": "Core system components",
        "services": "Service layer components",
        "launchers": "Launcher components",
        "utils": "Utility components",
        "web": "Web interface components",
        "interfaces": "Interface components",
        "types": "Type system components"
    })


@dataclass
class CoverageConfig:
    """Test coverage configuration."""
    enabled: bool = True
    min_coverage: float = 80.0
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*/tests/*",
        "*/test_*",
        "*/__pycache__/*",
        "*/migrations/*",
        "*/venv/*",
        "*/env/*"
    ])
    include_patterns: List[str] = field(default_factory=lambda: [
        "*.py"
    ])
    report_formats: List[str] = field(default_factory=lambda: [
        "html",
        "xml",
        "term-missing"
    ])
    fail_under: float = 80.0


@dataclass
class PerformanceConfig:
    """Performance testing configuration."""
    enabled: bool = True
    timeout: int = 300
    max_memory: int = 1024  # MB
    max_cpu: float = 80.0  # percentage
    parallel_workers: int = 4
    load_test_duration: int = 60  # seconds
    stress_test_duration: int = 300  # seconds


@dataclass
class ReportingConfig:
    """Test reporting configuration."""
    enabled: bool = True
    output_formats: List[str] = field(default_factory=lambda: [
        "text",
        "json",
        "html",
        "xml"
    ])
    output_directory: str = "test_reports"
    include_timestamps: bool = True
    include_coverage: bool = True
    include_performance: bool = True
    color_output: bool = True


class UnifiedTestConfigV2:
    """V2-compliant unified test configuration system."""
    
    def __init__(self, repo_root: Path = None):
        """Initialize the unified test configuration."""
        self.repo_root = repo_root or Path.cwd()
        self.environment = self._detect_environment()
        self.test_categories = self._initialize_test_categories()
        self.standards = StandardsConfig()
        self.coverage = CoverageConfig()
        self.performance = PerformanceConfig()
        self.reporting = ReportingConfig()
        
        # Load environment-specific overrides
        self._load_environment_overrides()
    
    def _detect_environment(self) -> TestEnvironment:
        """Detect the current test environment."""
        env_vars = {
            "CI": TestEnvironment.CI,
            "STAGING": TestEnvironment.STAGING,
            "PRODUCTION": TestEnvironment.PRODUCTION,
            "DEVELOPMENT": TestEnvironment.DEVELOPMENT
        }
        
        for var, env in env_vars.items():
            if os.getenv(var):
                return env
        
        return TestEnvironment.LOCAL
    
    def _initialize_test_categories(self) -> Dict[str, TestCategoryConfig]:
        """Initialize test categories with configuration."""
        return {
            "smoke": TestCategoryConfig(
                name="smoke",
                description="Smoke tests for basic functionality validation",
                marker="smoke",
                timeout=60,
                level=TestLevel.CRITICAL,
                directory="smoke",
                enabled=True,
                parallel=False,
                coverage_required=False
            ),
            "unit": TestCategoryConfig(
                name="unit",
                description="Unit tests for individual components",
                marker="unit",
                timeout=120,
                level=TestLevel.CRITICAL,
                directory="unit",
                enabled=True,
                parallel=True,
                coverage_required=True,
                min_coverage=85.0
            ),
            "integration": TestCategoryConfig(
                name="integration",
                description="Integration tests for component interaction",
                marker="integration",
                timeout=300,
                level=TestLevel.HIGH,
                directory="integration",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=75.0
            ),
            "performance": TestCategoryConfig(
                name="performance",
                description="Performance and load testing",
                marker="performance",
                timeout=600,
                level=TestLevel.MEDIUM,
                directory="performance",
                enabled=True,
                parallel=False,
                coverage_required=False
            ),
            "security": TestCategoryConfig(
                name="security",
                description="Security and vulnerability testing",
                marker="security",
                timeout=180,
                level=TestLevel.CRITICAL,
                directory="security",
                enabled=True,
                parallel=False,
                coverage_required=False
            ),
            "api": TestCategoryConfig(
                name="api",
                description="API endpoint testing",
                marker="api",
                timeout=240,
                level=TestLevel.HIGH,
                directory="api",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=80.0
            )
        }
    
    def _load_environment_overrides(self):
        """Load environment-specific configuration overrides."""
        env_config_file = self.repo_root / f"test_config_{self.environment.value}.json"
        
        if env_config_file.exists():
            try:
                with open(env_config_file, 'r') as f:
                    overrides = json.load(f)
                
                # Apply overrides to test categories
                for category_name, config in overrides.get("categories", {}).items():
                    if category_name in self.test_categories:
                        for key, value in config.items():
                            if hasattr(self.test_categories[category_name], key):
                                setattr(self.test_categories[category_name], key, value)
                
                # Apply other overrides
                if "coverage" in overrides:
                    for key, value in overrides["coverage"].items():
                        if hasattr(self.coverage, key):
                            setattr(self.coverage, key, value)
                
                if "performance" in overrides:
                    for key, value in overrides["performance"].items():
                        if hasattr(self.performance, key):
                            setattr(self.performance, key, value)
                            
            except Exception as e:
                print(f"Warning: Failed to load environment config: {e}")
    
    def get_test_paths(self) -> Dict[str, Path]:
        """Get test directory paths."""
        return {
            category: self.repo_root / "tests" / config.directory
            for category, config in self.test_categories.items()
        }
    
    def get_category_config(self, category: str) -> Optional[TestCategoryConfig]:
        """Get configuration for a specific test category."""
        return self.test_categories.get(category)
    
    def is_category_enabled(self, category: str) -> bool:
        """Check if a test category is enabled."""
        config = self.get_category_config(category)
        return config.enabled if config else False
    
    def get_coverage_config(self) -> CoverageConfig:
        """Get coverage configuration."""
        return self.coverage
    
    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration."""
        return self.performance
    
    def get_reporting_config(self) -> ReportingConfig:
        """Get reporting configuration."""
        return self.reporting
    
    def validate_standards(self, file_path: Path) -> Dict[str, Any]:
        """Validate file against V2 standards."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            file_type = self._get_file_type(file_path)
            max_lines = self._get_max_lines_for_type(file_type)
            
            return {
                "file_path": str(file_path),
                "line_count": line_count,
                "file_type": file_type,
                "max_lines": max_lines,
                "compliant": line_count <= max_lines,
                "excess_lines": max(0, line_count - max_lines)
            }
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": str(e),
                "compliant": False
            }
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type based on path."""
        path_str = str(file_path)
        
        if "gui" in path_str or "frontend" in path_str:
            return "gui"
        elif "core" in path_str:
            return "core"
        elif "services" in path_str:
            return "services"
        elif "utils" in path_str:
            return "utils"
        elif "launchers" in path_str:
            return "launchers"
        else:
            return "standard"
    
    def _get_max_lines_for_type(self, file_type: str) -> int:
        """Get maximum lines for file type."""
        max_lines_map = {
            "gui": self.standards.max_loc_gui,
            "core": self.standards.max_loc_core,
            "services": self.standards.max_loc_services,
            "utils": self.standards.max_loc_utils,
            "launchers": self.standards.max_loc_launchers,
            "standard": self.standards.max_loc_standard
        }
        return max_lines_map.get(file_type, self.standards.max_loc_standard)
    
    def export_config(self, format: str = "json") -> str:
        """Export configuration to specified format."""
        config_data = {
            "environment": self.environment.value,
            "test_categories": {
                name: {
                    "name": config.name,
                    "description": config.description,
                    "marker": config.marker,
                    "timeout": config.timeout,
                    "level": config.level.value,
                    "directory": config.directory,
                    "enabled": config.enabled,
                    "parallel": config.parallel,
                    "coverage_required": config.coverage_required,
                    "min_coverage": config.min_coverage
                }
                for name, config in self.test_categories.items()
            },
            "coverage": {
                "enabled": self.coverage.enabled,
                "min_coverage": self.coverage.min_coverage,
                "exclude_patterns": self.coverage.exclude_patterns,
                "include_patterns": self.coverage.include_patterns,
                "report_formats": self.coverage.report_formats,
                "fail_under": self.coverage.fail_under
            },
            "performance": {
                "enabled": self.performance.enabled,
                "timeout": self.performance.timeout,
                "max_memory": self.performance.max_memory,
                "max_cpu": self.performance.max_cpu,
                "parallel_workers": self.performance.parallel_workers
            },
            "reporting": {
                "enabled": self.reporting.enabled,
                "output_formats": self.reporting.output_formats,
                "output_directory": self.reporting.output_directory,
                "color_output": self.reporting.color_output
            }
        }
        
        if format.lower() == "yaml":
            return yaml.dump(config_data, default_flow_style=False)
        else:
            return json.dumps(config_data, indent=2)


# Global instance for convenience
UNIFIED_TEST_CONFIG = UnifiedTestConfigV2()


def get_test_config() -> UnifiedTestConfigV2:
    """Get the global test configuration instance."""
    return UNIFIED_TEST_CONFIG


def get_category_config(category: str) -> Optional[TestCategoryConfig]:
    """Get configuration for a specific test category."""
    return UNIFIED_TEST_CONFIG.get_category_config(category)


def is_category_enabled(category: str) -> bool:
    """Check if a test category is enabled."""
    return UNIFIED_TEST_CONFIG.is_category_enabled(category)
