#!/usr/bin/env python3
"""
Test Utilities Dataclasses - Agent Cellphone V2
=============================================

Core dataclass definitions for the unified testing utilities.
Extracted from unified_test_utilities.py to achieve V2 compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta

from .test_utilities_enums import MockObjectType, TestDataType, ValidationType


@dataclass
class MockObjectConfig:
    """Mock object configuration."""
    object_type: MockObjectType
    properties: Dict[str, Any] = field(default_factory=dict)
    methods: Dict[str, Any] = field(default_factory=dict)
    return_values: Dict[str, Any] = field(default_factory=dict)
    side_effects: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestDataConfig:
    """Test data configuration."""
    data_type: TestDataType
    size: int = 1
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Validation rule configuration."""
    field_name: str
    validation_type: ValidationType
    required: bool = True
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    custom_validator: Optional[Callable] = None


@dataclass
class TestEnvironment:
    """Test environment configuration."""
    name: str
    description: str
    variables: Dict[str, str] = field(default_factory=dict)
    setup_commands: List[str] = field(default_factory=list)
    teardown_commands: List[str] = field(default_factory=list)
    timeout: int = 300


@dataclass
class TestReport:
    """Test report configuration."""
    title: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    results: Dict[str, Any] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
