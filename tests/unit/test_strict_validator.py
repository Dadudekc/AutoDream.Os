#!/usr/bin/env python3
"""
Unit Tests for StrictValidator
===============================

Tests for src/core/ssot/unified_ssot/validators/strict_validator.py

Author: Agent-1 - Testing & Quality Assurance Specialist
Created: 2025-10-14
Coverage Target: 100%
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import pytest


# Mock SSOT classes for testing
class SSOTComponentType(Enum):
    """Mock SSOT component types."""

    EXECUTION = "execution"
    VALIDATION = "validation"


@dataclass
class SSOTExecutionPhase:
    """Mock SSOT execution phase."""

    name: str = "test_phase"
    description: str = ""


@dataclass
class SSOTComponent:
    """Mock SSOT component for testing."""

    component_id: str = "test_component"
    component_type: SSOTComponentType = SSOTComponentType.EXECUTION
    component_name: str = "Test Component"
    description: str | None = None
    usage_examples: str | None = None
    author: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    version: str | None = None
    performance_metrics: dict[str, Any] | None = None
    configuration: dict[str, Any] | None = None
    execution_phases: list[SSOTExecutionPhase] = field(default_factory=list)
    resource_requirements: dict[str, Any] | None = None
    access_controls: dict[str, Any] | None = None


# Import after mock definitions
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ssot.unified_ssot.validators.strict_validator import StrictValidator


class TestStrictValidator:
    """Test suite for StrictValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = StrictValidator()

    def test_init(self):
        """Test validator initialization."""
        assert self.validator is not None
        assert "required_documentation" in self.validator.validation_rules
        assert "min_description_length" in self.validator.validation_rules
        assert "required_metadata" in self.validator.validation_rules
        assert "performance_thresholds" in self.validator.validation_rules
        assert self.validator.validation_rules["min_description_length"] == 50

    def test_validate_strict_requirements_all_present(self):
        """Test validation with all strict requirements present."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement for strict validation testing purposes.",
            usage_examples="Example 1: How to use this component",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
        )
        issues = self.validator.validate_strict_requirements(component)
        assert len(issues) == 0

    def test_validate_strict_requirements_missing_description(self):
        """Test validation with missing description."""
        component = SSOTComponent(
            usage_examples="Example 1", author="Agent-1", created_at=datetime.now(), version="1.0.0"
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Missing required documentation: description" in issue for issue in issues)

    def test_validate_strict_requirements_description_too_short(self):
        """Test validation with description too short."""
        component = SSOTComponent(
            description="Short",  # Less than 50 characters
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Description too short" in issue for issue in issues)

    def test_validate_strict_requirements_missing_usage_examples(self):
        """Test validation with missing usage_examples."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Missing required documentation: usage_examples" in issue for issue in issues)

    def test_validate_strict_requirements_missing_author(self):
        """Test validation with missing author metadata."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            created_at=datetime.now(),
            version="1.0.0",
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Missing required metadata: author" in issue for issue in issues)

    def test_validate_strict_requirements_missing_created_at(self):
        """Test validation with missing created_at metadata."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            version="1.0.0",
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Missing required metadata: created_at" in issue for issue in issues)

    def test_validate_strict_requirements_missing_version(self):
        """Test validation with missing version metadata."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Missing required metadata: version" in issue for issue in issues)

    def test_validate_strict_requirements_with_performance_metrics_ok(self):
        """Test validation with acceptable performance metrics."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
            performance_metrics={
                "execution_time": 15.0,  # Within 30s threshold
                "memory_usage": 256,  # Within 512MB threshold
            },
        )
        issues = self.validator.validate_strict_requirements(component)
        assert len(issues) == 0

    def test_validate_strict_requirements_execution_time_exceeds(self):
        """Test validation with execution time exceeding threshold."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
            performance_metrics={"execution_time": 45.0},  # Exceeds 30s threshold
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Execution time exceeds threshold" in issue for issue in issues)

    def test_validate_strict_requirements_memory_exceeds(self):
        """Test validation with memory usage exceeding threshold."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
            performance_metrics={"memory_usage": 1024},  # Exceeds 512MB threshold
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("Memory usage exceeds threshold" in issue for issue in issues)

    def test_validate_strict_requirements_security_sensitive_data(self):
        """Test validation detecting sensitive data in configuration."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
            configuration={"database_password": "secret123", "api_key": "abc123"},
        )
        issues = self.validator.validate_strict_requirements(component)
        assert any("sensitive data exposure" in issue for issue in issues)

    def test_validate_component_integrity_updated_before_created(self):
        """Test integrity validation when updated_at is before created_at."""
        component = SSOTComponent(
            created_at=datetime.now(),
            updated_at=datetime.now() - timedelta(days=1),  # Before created
        )
        issues = self.validator.validate_component_integrity(component)
        assert any(
            "Updated timestamp cannot be before created timestamp" in issue for issue in issues
        )

    def test_validate_component_integrity_valid_timestamps(self):
        """Test integrity validation with valid timestamps."""
        now = datetime.now()
        component = SSOTComponent(created_at=now, updated_at=now + timedelta(hours=1))
        issues = self.validator.validate_component_integrity(component)
        assert not any("timestamp" in issue.lower() for issue in issues)

    def test_validate_component_integrity_execution_phases(self):
        """Test integrity validation with execution phases."""
        component = SSOTComponent(
            execution_phases=[SSOTExecutionPhase(name="phase1"), SSOTExecutionPhase(name="phase2")]
        )
        issues = self.validator.validate_component_integrity(component)
        assert len(issues) == 0

    def test_validate_component_integrity_duplicate_phase_names(self):
        """Test integrity validation with duplicate phase names."""
        component = SSOTComponent(
            execution_phases=[
                SSOTExecutionPhase(name="phase1"),
                SSOTExecutionPhase(name="phase1"),  # Duplicate
            ]
        )
        issues = self.validator.validate_component_integrity(component)
        assert any("Duplicate phase name" in issue for issue in issues)

    def test_validate_component_integrity_phase_missing_name(self):
        """Test integrity validation with phase missing name."""
        component = SSOTComponent(execution_phases=[SSOTExecutionPhase(name="")])
        issues = self.validator.validate_component_integrity(component)
        assert any("Phase" in issue and "missing name" in issue for issue in issues)

    def test_validate_component_integrity_resource_requirements_valid(self):
        """Test integrity validation with valid resource requirements."""
        component = SSOTComponent(
            resource_requirements={"cpu": 2.0, "memory": 4096, "storage": 10000}
        )
        issues = self.validator.validate_component_integrity(component)
        assert len(issues) == 0

    def test_validate_component_integrity_missing_cpu_requirement(self):
        """Test integrity validation with missing CPU requirement."""
        component = SSOTComponent(resource_requirements={"memory": 4096, "storage": 10000})
        issues = self.validator.validate_component_integrity(component)
        assert any("Missing resource requirement: cpu" in issue for issue in issues)

    def test_validate_component_integrity_invalid_memory_requirement(self):
        """Test integrity validation with invalid memory requirement."""
        component = SSOTComponent(
            resource_requirements={
                "cpu": 2.0,
                "memory": -100,  # Invalid negative value
                "storage": 10000,
            }
        )
        issues = self.validator.validate_component_integrity(component)
        assert any("Invalid memory requirement" in issue for issue in issues)

    def test_validate_security_requirements_access_controls_not_dict(self):
        """Test security validation with access_controls not being dict."""
        component = SSOTComponent(access_controls="not_a_dict")
        issues = self.validator._validate_security_requirements(component)
        assert any("Access controls must be a dictionary" in issue for issue in issues)

    def test_validate_security_requirements_empty_access_controls(self):
        """Test security validation with empty access_controls."""
        component = SSOTComponent(access_controls={})
        issues = self.validator._validate_security_requirements(component)
        assert any("Access controls cannot be empty" in issue for issue in issues)

    def test_validate_security_requirements_valid_access_controls(self):
        """Test security validation with valid access_controls."""
        component = SSOTComponent(
            access_controls={"role": "admin", "permissions": ["read", "write"]}
        )
        issues = self.validator._validate_security_requirements(component)
        assert len(issues) == 0

    def test_validate_performance_metrics_valid(self):
        """Test _validate_performance_metrics with valid metrics."""
        metrics = {"execution_time": 10.0, "memory_usage": 200}
        issues = self.validator._validate_performance_metrics(metrics)
        assert len(issues) == 0

    def test_validate_execution_phases_not_list(self):
        """Test _validate_execution_phases with non-list input."""
        issues = self.validator._validate_execution_phases("not_a_list")
        assert any("must be a list" in issue for issue in issues)

    def test_validate_resource_requirements_all_valid(self):
        """Test _validate_resource_requirements with all valid values."""
        requirements = {"cpu": 4.0, "memory": 8192, "storage": 50000}
        issues = self.validator._validate_resource_requirements(requirements)
        assert len(issues) == 0

    def test_get_validation_score_no_issues(self):
        """Test validation score with no issues."""
        score = self.validator.get_validation_score([])
        assert score == 100.0

    def test_get_validation_score_some_issues(self):
        """Test validation score with some issues."""
        issues = ["issue1", "issue2", "issue3", "issue4"]
        score = self.validator.get_validation_score(issues)
        # 100 - (4 * 3) = 88
        assert score == 88.0

    def test_get_validation_score_many_issues(self):
        """Test validation score with many issues (floor at 0)."""
        issues = ["issue" + str(i) for i in range(50)]
        score = self.validator.get_validation_score(issues)
        # Should not go below 0
        assert score == 0.0

    def test_validate_strict_requirements_exception_handling(self):
        """Test exception handling in validate_strict_requirements."""
        component = SSOTComponent()
        component.__getattribute__ = lambda self, name: (_ for _ in ()).throw(
            Exception("Test error")
        )

        issues = self.validator.validate_strict_requirements(component)
        assert any("Strict validation error" in issue for issue in issues)

    def test_validate_component_integrity_exception_handling(self):
        """Test exception handling in validate_component_integrity."""
        component = SSOTComponent()
        component.__getattribute__ = lambda self, name: (_ for _ in ()).throw(
            Exception("Test error")
        )

        issues = self.validator.validate_component_integrity(component)
        assert any("Integrity validation error" in issue for issue in issues)

    def test_sensitive_key_detection_case_insensitive(self):
        """Test that sensitive key detection is case-insensitive."""
        component = SSOTComponent(
            description="This is a comprehensive description that meets the minimum length requirement.",
            usage_examples="Example 1",
            author="Agent-1",
            created_at=datetime.now(),
            version="1.0.0",
            configuration={
                "DATABASE_PASSWORD": "secret",
                "Api_Token": "token123",
                "Secret_KEY": "key123",
            },
        )
        issues = self.validator.validate_strict_requirements(component)
        # Should detect all three sensitive keys
        sensitive_issues = [i for i in issues if "sensitive data exposure" in i]
        assert len(sensitive_issues) >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
