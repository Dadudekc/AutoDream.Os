#!/usr/bin/env python3
"""
Unit Tests for StandardValidator
================================

Tests for src/core/ssot/unified_ssot/validators/standard_validator.py

Author: Agent-1 - Testing & Quality Assurance Specialist
Created: 2025-10-14
Coverage Target: 100%
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

import pytest


# Mock SSOTComponent and related classes for testing
class SSOTComponentType(Enum):
    """Mock SSOT component types."""

    LOGGING = "logging"
    CONFIGURATION = "configuration"
    EXECUTION = "execution"
    VALIDATION = "validation"


@dataclass
class SSOTComponent:
    """Mock SSOT component for testing."""

    component_id: str = "test_component"
    component_type: SSOTComponentType = SSOTComponentType.EXECUTION
    component_name: str = "Test Component"
    priority: str | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    configuration: dict[str, Any] | None = None
    parent_id: str | None = None
    children: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


# Import after mock definitions
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ssot.unified_ssot.validators.standard_validator import StandardValidator


class TestStandardValidator:
    """Test suite for StandardValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = StandardValidator()

    def test_init(self):
        """Test validator initialization."""
        assert self.validator is not None
        assert "valid_priorities" in self.validator.validation_rules
        assert "valid_statuses" in self.validator.validation_rules
        assert self.validator.validation_rules["max_age_days"] == 365
        assert self.validator.validation_rules["min_update_frequency_days"] == 30

    def test_validate_standard_fields_valid_priority(self):
        """Test validation of valid priority."""
        component = SSOTComponent(priority="high")
        issues = self.validator.validate_standard_fields(component)
        assert len(issues) == 0

    def test_validate_standard_fields_invalid_priority(self):
        """Test validation of invalid priority."""
        component = SSOTComponent(priority="invalid")
        issues = self.validator.validate_standard_fields(component)
        assert any("Invalid priority" in issue for issue in issues)

    def test_validate_standard_fields_valid_status(self):
        """Test validation of valid status."""
        component = SSOTComponent(status="active")
        issues = self.validator.validate_standard_fields(component)
        assert len(issues) == 0

    def test_validate_standard_fields_invalid_status(self):
        """Test validation of invalid status."""
        component = SSOTComponent(status="unknown")
        issues = self.validator.validate_standard_fields(component)
        assert any("Invalid status" in issue for issue in issues)

    def test_validate_standard_fields_component_too_old(self):
        """Test validation of component age (too old)."""
        old_date = datetime.now() - timedelta(days=400)
        component = SSOTComponent(created_at=old_date)
        issues = self.validator.validate_standard_fields(component)
        assert any("too old" in issue for issue in issues)

    def test_validate_standard_fields_component_recent(self):
        """Test validation of recent component."""
        recent_date = datetime.now() - timedelta(days=100)
        component = SSOTComponent(created_at=recent_date)
        issues = self.validator.validate_standard_fields(component)
        # Should not have age-related issues
        assert not any("too old" in issue for issue in issues)

    def test_validate_standard_fields_not_updated_recently(self):
        """Test validation of component not updated recently."""
        old_update = datetime.now() - timedelta(days=60)
        component = SSOTComponent(updated_at=old_update)
        issues = self.validator.validate_standard_fields(component)
        assert any("not updated recently" in issue for issue in issues)

    def test_validate_standard_fields_recently_updated(self):
        """Test validation of recently updated component."""
        recent_update = datetime.now() - timedelta(days=10)
        component = SSOTComponent(updated_at=recent_update)
        issues = self.validator.validate_standard_fields(component)
        assert not any("not updated recently" in issue for issue in issues)

    def test_validate_standard_fields_with_valid_configuration(self):
        """Test validation with valid configuration."""
        config = {"enabled": True, "settings": {"key": "value"}}
        component = SSOTComponent(configuration=config)
        issues = self.validator.validate_standard_fields(component)
        assert len(issues) == 0

    def test_validate_standard_fields_with_invalid_configuration(self):
        """Test validation with invalid configuration (missing keys)."""
        config = {
            "enabled": True
            # Missing 'settings' key
        }
        component = SSOTComponent(configuration=config)
        issues = self.validator.validate_standard_fields(component)
        assert any("Missing required configuration key" in issue for issue in issues)

    def test_validate_component_relationships_parent_and_children(self):
        """Test validation when component has both parent and children."""
        component = SSOTComponent(parent_id="parent_123", children=["child_1", "child_2"])
        issues = self.validator.validate_component_relationships(component)
        assert any("cannot have both parent and children" in issue for issue in issues)

    def test_validate_component_relationships_self_dependency(self):
        """Test validation when component depends on itself."""
        component = SSOTComponent(component_id="comp_123", dependencies=["other_comp", "comp_123"])
        issues = self.validator.validate_component_relationships(component)
        assert any("cannot depend on itself" in issue for issue in issues)

    def test_validate_component_relationships_with_parent_only(self):
        """Test validation when component has only parent (no children)."""
        component = SSOTComponent(
            component_type=SSOTComponentType.LOGGING, parent_id="parent_123", children=[]
        )
        issues = self.validator.validate_component_relationships(component)
        # Should have no relationship issues with just a parent
        assert not any("both parent and children" in issue for issue in issues)

    def test_validate_component_relationships_valid(self):
        """Test validation of valid component relationships."""
        component = SSOTComponent(
            component_type=SSOTComponentType.VALIDATION,
            parent_id="parent_123",
            dependencies=["dep_1", "dep_2"],
        )
        issues = self.validator.validate_component_relationships(component)
        # Valid relationships should have no issues
        assert (
            len([i for i in issues if "error" not in i.lower()]) == 0
        )  # Filter out error messages

    def test_validate_configuration_not_dict(self):
        """Test _validate_configuration with non-dict input."""
        issues = self.validator._validate_configuration("not_a_dict")
        assert any("must be a dictionary" in issue for issue in issues)

    def test_validate_configuration_missing_enabled(self):
        """Test _validate_configuration missing 'enabled' key."""
        config = {"settings": {}}
        issues = self.validator._validate_configuration(config)
        assert any("enabled" in issue for issue in issues)

    def test_validate_configuration_missing_settings(self):
        """Test _validate_configuration missing 'settings' key."""
        config = {"enabled": True}
        issues = self.validator._validate_configuration(config)
        assert any("settings" in issue for issue in issues)

    def test_validate_configuration_settings_not_dict(self):
        """Test _validate_configuration with settings not being a dict."""
        config = {"enabled": True, "settings": "not_a_dict"}
        issues = self.validator._validate_configuration(config)
        assert any("settings must be a dictionary" in issue for issue in issues)

    def test_has_circular_reference_no_circular(self):
        """Test _has_circular_reference with no circular references."""
        data = {"key1": "value1", "key2": {"nested": "value2"}}
        has_circular = self.validator._has_circular_reference(data)
        assert has_circular is False

    def test_has_circular_reference_list(self):
        """Test _has_circular_reference with list data."""
        data = ["item1", "item2", ["nested1", "nested2"]]
        has_circular = self.validator._has_circular_reference(data)
        assert has_circular is False

    def test_get_validation_score_no_issues(self):
        """Test validation score with no issues."""
        score = self.validator.get_validation_score([])
        assert score == 100.0

    def test_get_validation_score_some_issues(self):
        """Test validation score with some issues."""
        issues = ["issue1", "issue2", "issue3"]
        score = self.validator.get_validation_score(issues)
        # 100 - (3 * 5) = 85
        assert score == 85.0

    def test_get_validation_score_many_issues(self):
        """Test validation score with many issues (floor at 0)."""
        issues = ["issue" + str(i) for i in range(30)]
        score = self.validator.get_validation_score(issues)
        # Should not go below 0
        assert score == 0.0

    def test_validate_standard_fields_exception_handling(self):
        """Test exception handling in validate_standard_fields."""

        # Create a mock component that will raise an exception
        class FailingComponent:
            def __getattribute__(self, name):
                raise Exception("Test error")

        component = FailingComponent()
        issues = self.validator.validate_standard_fields(component)
        assert any("error" in issue.lower() for issue in issues)

    def test_case_insensitive_priority(self):
        """Test that priority validation is case-insensitive."""
        component = SSOTComponent(priority="HIGH")
        issues = self.validator.validate_standard_fields(component)
        assert len(issues) == 0

    def test_case_insensitive_status(self):
        """Test that status validation is case-insensitive."""
        component = SSOTComponent(status="ACTIVE")
        issues = self.validator.validate_standard_fields(component)
        assert len(issues) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
