#!/usr/bin/env python3
"""
Unified Test Configuration System - Agent Cellphone V2
=====================================================

Consolidated test configuration system that eliminates duplication across
multiple configuration files. Provides unified configuration management,
standards checking, and environment-specific settings for all test types.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
import json
import yaml
from pathlib import Path


# ============================================================================
# UNIFIED TEST CONFIGURATION ENUMS AND DATA CLASSES
# ============================================================================

class TestEnvironment(Enum):
    """Test environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI = "ci"
    LOCAL = "local"


class TestLevel(Enum):
    """Test level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestType(Enum):
    """Test type enumeration."""
    UNIT = "unit"
    INTEGRATION = "integration"
    SMOKE = "smoke"
    PERFORMANCE = "performance"
    SECURITY = "security"
    API = "api"
    BEHAVIOR = "behavior"
    DECISION = "decision"
    COORDINATION = "coordination"
    LEARNING = "learning"


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
    fail_under: float = 70.0
    report_formats: List[str] = field(default_factory=lambda: ["html", "term", "xml"])
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*/tests/*",
        "*/test_*",
        "*/__pycache__/*",
        "*/migrations/*",
        "*/venv/*",
        "*/env/*"
    ])
    include_patterns: List[str] = field(default_factory=lambda: [
        "src/**/*.py",
        "tests/**/*.py"
    ])


@dataclass
class PerformanceConfig:
    """Test performance configuration."""
    timeout_multiplier: float = 1.0
    max_workers: int = 4
    parallel_threshold: int = 10
    memory_limit_mb: int = 1024
    cpu_limit_percent: int = 80
    enable_profiling: bool = False
    profiling_interval: float = 5.0


@dataclass
class ReportingConfig:
    """Test reporting configuration."""
    enabled: bool = True
    output_formats: List[str] = field(default_factory=lambda: ["text", "json", "html"])
    output_directory: str = "test_results"
    detailed_output: bool = True
    include_coverage: bool = True
    include_performance: bool = True
    include_standards: bool = True
    email_notifications: bool = False
    slack_notifications: bool = False


# ============================================================================
# UNIFIED TEST CONFIGURATION SYSTEM
# ============================================================================

class UnifiedTestConfig:
    """Unified test configuration system consolidating all configurations."""
    
    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize the unified test configuration system."""
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent
        self.environment = self._detect_environment()
        
        # Initialize configurations
        self.test_categories = self._initialize_test_categories()
        self.standards = StandardsConfig()
        self.coverage = CoverageConfig()
        self.performance = PerformanceConfig()
        self.reporting = ReportingConfig()
        
        # Setup paths
        self._setup_paths()
        
        # Load environment-specific overrides
        self._load_environment_overrides()
    
    def _detect_environment(self) -> TestEnvironment:
        """Detect the current test environment."""
        env = os.getenv("TEST_ENVIRONMENT", "").lower()
        
        if env == "ci" or os.getenv("CI"):
            return TestEnvironment.CI
        elif env == "staging":
            return TestEnvironment.STAGING
        elif env == "production":
            return TestEnvironment.PRODUCTION
        elif env == "local":
            return TestEnvironment.LOCAL
        else:
            return TestEnvironment.DEVELOPMENT
    
    def _setup_paths(self):
        """Setup important directory paths."""
        self.paths = {
            "repo_root": self.repo_root,
            "tests_dir": self.repo_root / "tests",
            "src_dir": self.repo_root / "src",
            "results_dir": self.repo_root / "test_results",
            "coverage_dir": self.repo_root / "htmlcov",
            "config_dir": self.repo_root / "config",
            "logs_dir": self.repo_root / "logs"
        }
        
        # Ensure important directories are on the import path
        for path in (self.repo_root, self.paths["tests_dir"]):
            path_str = str(path)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)
        
        # Create necessary directories
        for path in [self.paths["results_dir"], self.paths["coverage_dir"], self.paths["logs_dir"]]:
            path.mkdir(parents=True, exist_ok=True)
    
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
                coverage_required=True,
                min_coverage=70.0
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
                min_coverage=80.0
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
                coverage_required=False,
                min_coverage=50.0
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
                coverage_required=True,
                min_coverage=90.0
            ),
            "api": TestCategoryConfig(
                name="api",
                description="API endpoint testing",
                marker="api",
                timeout=240,
                level=TestLevel.HIGH,
                directory="api",
                enabled=True,
                parallel=True,
                coverage_required=True,
                min_coverage=80.0
            ),
            "behavior": TestCategoryConfig(
                name="behavior",
                description="Behavior tree tests",
                marker="behavior",
                timeout=120,
                level=TestLevel.MEDIUM,
                directory="behavior_trees",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=75.0
            ),
            "decision": TestCategoryConfig(
                name="decision",
                description="Decision engine tests",
                marker="decision",
                timeout=120,
                level=TestLevel.MEDIUM,
                directory="decision_engines",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=75.0
            ),
            "coordination": TestCategoryConfig(
                name="coordination",
                description="Multi-agent coordination tests",
                marker="coordination",
                timeout=180,
                level=TestLevel.MEDIUM,
                directory="multi_agent",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=70.0
            ),
            "learning": TestCategoryConfig(
                name="learning",
                description="Learning component tests",
                marker="learning",
                timeout=180,
                level=TestLevel.MEDIUM,
                directory="learning",
                enabled=True,
                parallel=False,
                coverage_required=True,
                min_coverage=70.0
            )
        }
    
    def _load_environment_overrides(self):
        """Load environment-specific configuration overrides."""
        config_file = self.paths["config_dir"] / f"test_config_{self.environment.value}.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    overrides = json.load(f)
                self._apply_overrides(overrides)
            except Exception as e:
                print(f"Warning: Could not load environment config {config_file}: {e}")
    
    def _apply_overrides(self, overrides: Dict[str, Any]):
        """Apply configuration overrides."""
        # Override test categories
        if "test_categories" in overrides:
            for cat_name, cat_overrides in overrides["test_categories"].items():
                if cat_name in self.test_categories:
                    for key, value in cat_overrides.items():
                        if hasattr(self.test_categories[cat_name], key):
                            setattr(self.test_categories[cat_name], key, value)
        
        # Override other configurations
        for config_name in ["standards", "coverage", "performance", "reporting"]:
            if config_name in overrides:
                config_obj = getattr(self, config_name)
                for key, value in overrides[config_name].items():
                    if hasattr(config_obj, key):
                        setattr(config_obj, key, value)
    
    def get_test_category(self, name: str) -> Optional[TestCategoryConfig]:
        """Get test category configuration by name."""
        return self.test_categories.get(name)
    
    def get_enabled_categories(self) -> List[str]:
        """Get list of enabled test categories."""
        return [name for name, config in self.test_categories.items() if config.enabled]
    
    def get_critical_categories(self) -> List[str]:
        """Get list of critical test categories."""
        return [name for name, config in self.test_categories.items() 
                if config.level == TestLevel.CRITICAL and config.enabled]
    
    def get_parallel_categories(self) -> List[str]:
        """Get list of test categories that support parallel execution."""
        return [name for name, config in self.test_categories.items() 
                if config.parallel and config.enabled]
    
    def get_category_timeout(self, category: str) -> int:
        """Get timeout for a specific test category."""
        cat_config = self.get_test_category(category)
        if cat_config:
            return int(cat_config.timeout * self.performance.timeout_multiplier)
        return 300  # Default timeout
    
    def get_standards_limit(self, component_type: str) -> int:
        """Get line count limit for a component type."""
        if component_type == "web":
            return self.standards.max_loc_gui
        elif component_type in ["core", "services", "launchers"]:
            return self.standards.max_loc_core
        elif component_type == "utils":
            return self.standards.max_loc_utils
        else:
            return self.standards.max_loc_standard
    
    def get_coverage_requirements(self, category: str) -> Tuple[bool, float]:
        """Get coverage requirements for a test category."""
        cat_config = self.get_test_category(category)
        if cat_config:
            return cat_config.coverage_required, cat_config.min_coverage
        return self.coverage.enabled, self.coverage.min_coverage
    
    def validate_configuration(self) -> List[str]:
        """Validate the current configuration and return any issues."""
        issues = []
        
        # Validate test categories
        for name, config in self.test_categories.items():
            if config.enabled and not (self.paths["tests_dir"] / config.directory).exists():
                issues.append(f"Test category '{name}' enabled but directory '{config.directory}' not found")
            
            if config.timeout <= 0:
                issues.append(f"Test category '{name}' has invalid timeout: {config.timeout}")
            
            if config.min_coverage < 0 or config.min_coverage > 100:
                issues.append(f"Test category '{name}' has invalid coverage: {config.min_coverage}%")
        
        # Validate paths
        for path_name, path in self.paths.items():
            if not path.exists() and path_name not in ["results_dir", "coverage_dir", "logs_dir"]:
                issues.append(f"Required path not found: {path_name} = {path}")
        
        # Validate performance settings
        if self.performance.max_workers <= 0:
            issues.append(f"Invalid max_workers: {self.performance.max_workers}")
        
        if self.performance.memory_limit_mb <= 0:
            issues.append(f"Invalid memory_limit_mb: {self.performance.memory_limit_mb}")
        
        return issues
    
    def export_configuration(self, format: str = "json") -> str:
        """Export current configuration in specified format."""
        config_data = {
            "environment": self.environment.value,
            "test_categories": {
                name: {
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
            "standards": {
                "max_loc_standard": self.standards.max_loc_standard,
                "max_loc_gui": self.standards.max_loc_gui,
                "max_loc_core": self.standards.max_loc_core,
                "max_loc_services": self.standards.max_loc_services,
                "max_loc_utils": self.standards.max_loc_utils,
                "max_loc_launchers": self.standards.max_loc_launchers,
                "components": self.standards.components
            },
            "coverage": {
                "enabled": self.coverage.enabled,
                "min_coverage": self.coverage.min_coverage,
                "fail_under": self.coverage.fail_under,
                "report_formats": self.coverage.report_formats,
                "exclude_patterns": self.coverage.exclude_patterns,
                "include_patterns": self.coverage.include_patterns
            },
            "performance": {
                "timeout_multiplier": self.performance.timeout_multiplier,
                "max_workers": self.performance.max_workers,
                "parallel_threshold": self.performance.parallel_threshold,
                "memory_limit_mb": self.performance.memory_limit_mb,
                "cpu_limit_percent": self.performance.cpu_limit_percent,
                "enable_profiling": self.performance.enable_profiling,
                "profiling_interval": self.performance.profiling_interval
            },
            "reporting": {
                "enabled": self.reporting.enabled,
                "output_formats": self.reporting.output_formats,
                "output_directory": self.reporting.output_directory,
                "detailed_output": self.reporting.detailed_output,
                "include_coverage": self.reporting.include_coverage,
                "include_performance": self.reporting.include_performance,
                "include_standards": self.reporting.include_standards,
                "email_notifications": self.reporting.email_notifications,
                "slack_notifications": self.reporting.slack_notifications
            },
            "paths": {
                name: str(path) for name, path in self.paths.items()
            }
        }
        
        if format.lower() == "json":
            return json.dumps(config_data, indent=2)
        elif format.lower() == "yaml":
            return yaml.dump(config_data, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def save_configuration(self, file_path: Path, format: str = "json"):
        """Save current configuration to file."""
        content = self.export_configuration(format)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"Configuration saved to: {file_path}")


# ============================================================================
# GLOBAL INSTANCE AND CONVENIENCE FUNCTIONS
# ============================================================================

# Global configuration instance
UNIFIED_TEST_CONFIG = UnifiedTestConfig()

# Convenience functions for backward compatibility
def get_test_category(name: str) -> Optional[TestCategoryConfig]:
    """Get test category configuration by name."""
    return UNIFIED_TEST_CONFIG.get_test_category(name)

def get_enabled_categories() -> List[str]:
    """Get list of enabled test categories."""
    return UNIFIED_TEST_CONFIG.get_enabled_categories()

def get_critical_categories() -> List[str]:
    """Get list of critical test categories."""
    return UNIFIED_TEST_CONFIG.get_critical_categories()

def get_category_timeout(category: str) -> int:
    """Get timeout for a specific test category."""
    return UNIFIED_TEST_CONFIG.get_category_timeout(category)

def get_standards_limit(component_type: str) -> int:
    """Get line count limit for a component type."""
    return UNIFIED_TEST_CONFIG.get_standards_limit(component_type)

def get_coverage_requirements(category: str) -> Tuple[bool, float]:
    """Get coverage requirements for a test category."""
    return UNIFIED_TEST_CONFIG.get_coverage_requirements(category)

# Path constants for backward compatibility
REPO_ROOT = UNIFIED_TEST_CONFIG.paths["repo_root"]
TESTS_DIR = UNIFIED_TEST_CONFIG.paths["tests_dir"]
SRC_DIR = UNIFIED_TEST_CONFIG.paths["src_dir"]
RESULTS_DIR = UNIFIED_TEST_CONFIG.paths["results_dir"]
COVERAGE_DIR = UNIFIED_TEST_CONFIG.paths["coverage_dir"]


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Main classes
    "UnifiedTestConfig",
    "TestCategoryConfig",
    "StandardsConfig",
    "CoverageConfig",
    "PerformanceConfig",
    "ReportingConfig",
    
    # Enums
    "TestEnvironment",
    "TestLevel",
    "TestType",
    
    # Global instance
    "UNIFIED_TEST_CONFIG",
    
    # Convenience functions
    "get_test_category",
    "get_enabled_categories",
    "get_critical_categories",
    "get_category_timeout",
    "get_standards_limit",
    "get_coverage_requirements",
    
    # Path constants
    "REPO_ROOT",
    "TESTS_DIR",
    "SRC_DIR",
    "RESULTS_DIR",
    "COVERAGE_DIR"
]
