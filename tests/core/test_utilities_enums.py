#!/usr/bin/env python3
"""
Test Utilities Enums - Agent Cellphone V2
========================================

Core enumeration definitions for the unified testing utilities.
Extracted from unified_test_utilities.py to achieve V2 compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from enum import Enum


class TestUtilityType(Enum):
    """Test utility type enumeration."""
    MOCK_OBJECTS = "mock_objects"
    STANDARDS_CHECKING = "standards_checking"
    TEST_HELPERS = "test_helpers"
    VALIDATION_UTILS = "validation_utils"
    FILE_UTILS = "file_utils"
    SYSTEM_UTILS = "system_utils"


class MockObjectType(Enum):
    """Mock object type enumeration."""
    AGENT = "agent"
    TASK = "task"
    CONFIG = "config"
    SERVICE = "service"
    MANAGER = "manager"
    VALIDATOR = "validator"
    DATABASE = "database"
    API = "api"


class TestDataType(Enum):
    """Test data type enumeration."""
    USER = "user"
    TASK = "task"
    CONFIG = "config"
    SERVICE = "service"
    MANAGER = "manager"
    VALIDATOR = "validator"
    DATABASE = "database"
    API = "api"
    FILE = "file"
    DIRECTORY = "directory"


class ValidationType(Enum):
    """Validation type enumeration."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    OBJECT = "object"
    FILE = "file"
    DIRECTORY = "directory"
    URL = "url"
    EMAIL = "email"
    JSON = "json"
