#!/usr/bin/env python3
"""
Unit Tests for BasicValidator
==============================

Tests for src/core/ssot/unified_ssot/validators/basic_validator.py

Author: Agent-1 - Testing & Quality Assurance Specialist
Created: 2025-10-14
Coverage Target: 100%
"""

import pytest
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# Mock SSOTComponent for testing
class SSOTComponentType(Enum):
    """Mock SSOT component types."""
    EXECUTION = "execution"
    VALIDATION = "validation"


@dataclass
class SSOTComponent:
    """Mock SSOT component for testing."""
    component_id: str | None = None
    component_type: SSOTComponentType | None = None
    component_name: str | None = None
    description: str | None = None
    version: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_validated: datetime | None = None
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


# Import after mock definitions
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ssot.unified_ssot.validators.basic_validator import BasicValidator


class TestBasicValidator:
    """Test suite for BasicValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = BasicValidator()

    def test_init(self):
        """Test validator initialization."""
        assert self.validator is not None
        assert "required_fields" in self.validator.validation_rules
        assert "field_length_limits" in self.validator.validation_rules
        assert "component_id" in self.validator.validation_rules["required_fields"]
        assert "component_type" in self.validator.validation_rules["required_fields"]
        assert "component_name" in self.validator.validation_rules["required_fields"]

    def test_validate_basic_fields_all_required_present(self):
        """Test validation with all required fields present."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test Component"
        )
        issues = self.validator.validate_basic_fields(component)
        assert len(issues) == 0

    def test_validate_basic_fields_missing_component_id(self):
        """Test validation with missing component_id."""
        component = SSOTComponent(
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test Component"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("Missing required field: component_id" in issue for issue in issues)

    def test_validate_basic_fields_empty_component_id(self):
        """Test validation with empty component_id."""
        component = SSOTComponent(
            component_id="   ",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test Component"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("Empty required field: component_id" in issue for issue in issues)

    def test_validate_basic_fields_missing_component_type(self):
        """Test validation with missing component_type."""
        component = SSOTComponent(
            component_id="test_id",
            component_name="Test Component"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("Missing required field: component_type" in issue for issue in issues)

    def test_validate_basic_fields_missing_component_name(self):
        """Test validation with missing component_name."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("Missing required field: component_name" in issue for issue in issues)

    def test_validate_basic_fields_component_name_exceeds_limit(self):
        """Test validation with component_name exceeding length limit."""
        long_name = "x" * 150  # Limit is 100
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name=long_name
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("exceeds length limit" in issue and "component_name" in issue for issue in issues)

    def test_validate_basic_fields_description_exceeds_limit(self):
        """Test validation with description exceeding length limit."""
        long_desc = "x" * 600  # Limit is 500
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            description=long_desc
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("exceeds length limit" in issue and "description" in issue for issue in issues)

    def test_validate_basic_fields_version_exceeds_limit(self):
        """Test validation with version exceeding length limit."""
        long_version = "1.0.0" * 10  # Limit is 20
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            version=long_version
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("exceeds length limit" in issue and "version" in issue for issue in issues)

    def test_validate_basic_fields_component_id_not_string(self):
        """Test validation with component_id not being a string."""
        component = SSOTComponent(
            component_id=123,  # Should be string
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("component_id must be a string" in issue for issue in issues)

    def test_validate_basic_fields_component_id_too_short(self):
        """Test validation with component_id too short."""
        component = SSOTComponent(
            component_id="ab",  # Less than 3 characters
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("at least 3 characters" in issue for issue in issues)

    def test_validate_basic_fields_component_id_invalid_chars(self):
        """Test validation with component_id containing invalid characters."""
        component = SSOTComponent(
            component_id="test@#$",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test"
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("invalid characters" in issue for issue in issues)

    def test_validate_basic_fields_component_id_with_underscore(self):
        """Test validation with component_id containing valid underscore."""
        component = SSOTComponent(
            component_id="test_component_123",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test"
        )
        issues = self.validator.validate_basic_fields(component)
        # Should not have component_id issues
        assert not any("component_id" in issue for issue in issues)

    def test_validate_basic_fields_component_id_with_dash(self):
        """Test validation with component_id containing valid dash."""
        component = SSOTComponent(
            component_id="test-component-123",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test"
        )
        issues = self.validator.validate_basic_fields(component)
        # Should not have component_id issues
        assert not any("component_id" in issue for issue in issues)

    def test_validate_basic_fields_created_at_not_datetime(self):
        """Test validation with created_at not being datetime."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            created_at="2025-01-01"  # String instead of datetime
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("created_at" in issue and "datetime object" in issue for issue in issues)

    def test_validate_basic_fields_updated_at_not_datetime(self):
        """Test validation with updated_at not being datetime."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            updated_at="2025-01-01"  # String instead of datetime
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("updated_at" in issue and "datetime object" in issue for issue in issues)

    def test_validate_basic_fields_last_validated_not_datetime(self):
        """Test validation with last_validated not being datetime."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            last_validated="2025-01-01"  # String instead of datetime
        )
        issues = self.validator.validate_basic_fields(component)
        assert any("last_validated" in issue and "datetime object" in issue for issue in issues)

    def test_validate_basic_fields_valid_timestamps(self):
        """Test validation with valid datetime timestamps."""
        component = SSOTComponent(
            component_id="test_id",
            component_type=SSOTComponentType.EXECUTION,
            component_name="Test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_validated=datetime.now()
        )
        issues = self.validator.validate_basic_fields(component)
        assert len(issues) == 0

    def test_validate_component_metadata_version_not_string(self):
        """Test metadata validation with version not being string."""
        component = SSOTComponent(
            version=123  # Should be string
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("version must be a string" in issue for issue in issues)

    def test_validate_component_metadata_version_no_digits(self):
        """Test metadata validation with version containing no digits."""
        component = SSOTComponent(
            version="release"  # No digits
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("version must contain at least one digit" in issue for issue in issues)

    def test_validate_component_metadata_version_valid(self):
        """Test metadata validation with valid version."""
        component = SSOTComponent(
            version="v1.2.3"
        )
        issues = self.validator.validate_component_metadata(component)
        assert len(issues) == 0

    def test_validate_component_metadata_tags_not_list(self):
        """Test metadata validation with tags not being list."""
        component = SSOTComponent(
            tags="tag1,tag2"  # Should be list
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("tags must be a list" in issue for issue in issues)

    def test_validate_component_metadata_tag_not_string(self):
        """Test metadata validation with tag not being string."""
        component = SSOTComponent(
            tags=["tag1", 123, "tag3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("Tag at index 1 must be a string" in issue for issue in issues)

    def test_validate_component_metadata_empty_tag(self):
        """Test metadata validation with empty tag."""
        component = SSOTComponent(
            tags=["tag1", "   ", "tag3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("Tag at index 1 cannot be empty" in issue for issue in issues)

    def test_validate_component_metadata_valid_tags(self):
        """Test metadata validation with valid tags."""
        component = SSOTComponent(
            tags=["tag1", "tag2", "tag3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert len(issues) == 0

    def test_validate_component_metadata_dependencies_not_list(self):
        """Test metadata validation with dependencies not being list."""
        component = SSOTComponent(
            dependencies="dep1,dep2"  # Should be list
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("dependencies must be a list" in issue for issue in issues)

    def test_validate_component_metadata_dependency_not_string(self):
        """Test metadata validation with dependency not being string."""
        component = SSOTComponent(
            dependencies=["dep1", 456, "dep3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("Dependency at index 1 must be a string" in issue for issue in issues)

    def test_validate_component_metadata_empty_dependency(self):
        """Test metadata validation with empty dependency."""
        component = SSOTComponent(
            dependencies=["dep1", "", "dep3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert any("Dependency at index 1 cannot be empty" in issue for issue in issues)

    def test_validate_component_metadata_valid_dependencies(self):
        """Test metadata validation with valid dependencies."""
        component = SSOTComponent(
            dependencies=["dep1", "dep2", "dep3"]
        )
        issues = self.validator.validate_component_metadata(component)
        assert len(issues) == 0

    def test_get_validation_score_no_issues(self):
        """Test validation score with no issues."""
        score = self.validator.get_validation_score([])
        assert score == 100.0

    def test_get_validation_score_some_issues(self):
        """Test validation score with some issues."""
        issues = ["issue1", "issue2"]
        score = self.validator.get_validation_score(issues)
        # 100 - (2 * 10) = 80
        assert score == 80.0

    def test_get_validation_score_many_issues(self):
        """Test validation score with many issues (floor at 0)."""
        issues = ["issue" + str(i) for i in range(15)]
        score = self.validator.get_validation_score(issues)
        # Should not go below 0
        assert score == 0.0

    def test_validate_basic_fields_exception_handling(self):
        """Test exception handling in validate_basic_fields."""
        component = SSOTComponent()
        component.__getattribute__ = lambda self, name: (_ for _ in ()).throw(Exception("Test error"))
        
        issues = self.validator.validate_basic_fields(component)
        assert any("Basic validation error" in issue for issue in issues)

    def test_validate_component_metadata_exception_handling(self):
        """Test exception handling in validate_component_metadata."""
        component = SSOTComponent()
        component.__getattribute__ = lambda self, name: (_ for _ in ()).throw(Exception("Test error"))
        
        issues = self.validator.validate_component_metadata(component)
        assert any("Metadata validation error" in issue for issue in issues)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

