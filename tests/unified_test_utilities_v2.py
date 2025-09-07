#!/usr/bin/env python3
"""
Unified Test Utilities System V2 - Agent Cellphone V2
===================================================

V2-compliant test utilities system (under 500 lines).
Uses modular components from tests/core/ to achieve compliance.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import os
import sys
import json
import tempfile
import shutil
import subprocess
import time
import inspect
import ast
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch, call
import pytest

# Import modular components
from .core.test_utilities_enums import TestUtilityType, MockObjectType, TestDataType, ValidationType
from .core.test_utilities_dataclasses import (
    MockObjectConfig, TestDataConfig, ValidationRule, TestEnvironment, TestReport
)


class UnifiedTestUtilitiesV2:
    """V2-compliant unified test utilities system."""
    
    def __init__(self):
        """Initialize the unified test utilities system."""
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging for the utilities system."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # ========================================================================
    # MOCK OBJECT CREATION UTILITIES
    # ========================================================================
    
    def create_mock_agent(self, config: MockObjectConfig = None) -> Mock:
        """Create a mock agent object."""
        if config is None:
            config = MockObjectConfig(object_type=MockObjectType.AGENT)
        
        mock_agent = Mock()
        mock_agent.agent_id = config.properties.get("agent_id", "test_agent_001")
        mock_agent.name = config.properties.get("name", "Test Agent")
        mock_agent.role = config.properties.get("role", "testing")
        mock_agent.status = config.properties.get("status", "active")
        mock_agent.capabilities = config.properties.get("capabilities", ["testing"])
        
        # Setup methods
        for method_name, return_value in config.return_values.items():
            getattr(mock_agent, method_name).return_value = return_value
        
        for method_name, side_effect in config.side_effects.items():
            getattr(mock_agent, method_name).side_effect = side_effect
        
        return mock_agent
    
    def create_mock_task(self, config: MockObjectConfig = None) -> Mock:
        """Create a mock task object."""
        if config is None:
            config = MockObjectConfig(object_type=MockObjectType.TASK)
        
        mock_task = Mock()
        mock_task.task_id = config.properties.get("task_id", "test_task_001")
        mock_task.name = config.properties.get("name", "Test Task")
        mock_task.description = config.properties.get("description", "Test task description")
        mock_task.status = config.properties.get("status", "pending")
        mock_task.priority = config.properties.get("priority", "medium")
        mock_task.assigned_agent = config.properties.get("assigned_agent", None)
        
        # Setup methods
        for method_name, return_value in config.return_values.items():
            getattr(mock_task, method_name).return_value = return_value
        
        for method_name, side_effect in config.side_effects.items():
            getattr(mock_task, method_name).side_effect = side_effect
        
        return mock_task
    
    def create_mock_config(self, config: MockObjectConfig = None) -> Mock:
        """Create a mock configuration object."""
        if config is None:
            config = MockObjectConfig(object_type=MockObjectType.CONFIG)
        
        mock_config = Mock()
        mock_config.config_id = config.properties.get("config_id", "test_config_001")
        mock_config.name = config.properties.get("name", "Test Config")
        mock_config.type = config.properties.get("type", "test")
        mock_config.values = config.properties.get("values", {})
        mock_config.enabled = config.properties.get("enabled", True)
        
        # Setup methods
        for method_name, return_value in config.return_values.items():
            getattr(mock_config, method_name).return_value = return_value
        
        for method_name, side_effect in config.side_effects.items():
            getattr(mock_config, method_name).side_effect = side_effect
        
        return mock_config
    
    # ========================================================================
    # TEST DATA GENERATION UTILITIES
    # ========================================================================
    
    def generate_test_data(self, config: TestDataConfig) -> Union[Dict, List[Dict]]:
        """Generate test data based on configuration."""
        if config.data_type == TestDataType.USER:
            return self._generate_user_data(config)
        elif config.data_type == TestDataType.TASK:
            return self._generate_task_data(config)
        elif config.data_type == TestDataType.CONFIG:
            return self._generate_config_data(config)
        else:
            return self._generate_generic_data(config)
    
    def _generate_user_data(self, config: TestDataConfig) -> Union[Dict, List[Dict]]:
        """Generate user test data."""
        base_user = {
            "user_id": f"user_{int(time.time())}",
            "username": f"testuser_{int(time.time())}",
            "email": f"testuser_{int(time.time())}@example.com",
            "role": config.properties.get("role", "user"),
            "status": config.properties.get("status", "active"),
            "created_at": datetime.now().isoformat()
        }
        
        if config.size == 1:
            return base_user
        else:
            return [base_user.copy() for _ in range(config.size)]
    
    def _generate_task_data(self, config: TestDataConfig) -> Union[Dict, List[Dict]]:
        """Generate task test data."""
        base_task = {
            "task_id": f"task_{int(time.time())}",
            "name": f"Test Task {int(time.time())}",
            "description": f"Test task description {int(time.time())}",
            "status": config.properties.get("status", "pending"),
            "priority": config.properties.get("priority", "medium"),
            "assigned_agent": config.properties.get("assigned_agent", None),
            "created_at": datetime.now().isoformat()
        }
        
        if config.size == 1:
            return base_task
        else:
            return [base_task.copy() for _ in range(config.size)]
    
    def _generate_config_data(self, config: TestDataConfig) -> Union[Dict, List[Dict]]:
        """Generate configuration test data."""
        base_config = {
            "config_id": f"config_{int(time.time())}",
            "name": f"Test Config {int(time.time())}",
            "type": config.properties.get("type", "test"),
            "values": config.properties.get("values", {}),
            "enabled": config.properties.get("enabled", True),
            "created_at": datetime.now().isoformat()
        }
        
        if config.size == 1:
            return base_config
        else:
            return [base_config.copy() for _ in range(config.size)]
    
    def _generate_generic_data(self, config: TestDataConfig) -> Union[Dict, List[Dict]]:
        """Generate generic test data."""
        base_data = {
            "id": f"{config.data_type.value}_{int(time.time())}",
            "name": f"Test {config.data_type.value.title()} {int(time.time())}",
            "created_at": datetime.now().isoformat()
        }
        
        # Add custom properties
        base_data.update(config.properties)
        
        if config.size == 1:
            return base_data
        else:
            return [base_data.copy() for _ in range(config.size)]
    
    # ========================================================================
    # FILE AND DIRECTORY UTILITIES
    # ========================================================================
    
    def create_temp_file(self, content: str = "", suffix: str = ".txt") -> Path:
        """Create a temporary file with content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False)
        temp_file.write(content)
        temp_file.close()
        return Path(temp_file.name)
    
    def create_temp_directory(self) -> Path:
        """Create a temporary directory."""
        temp_dir = tempfile.mkdtemp()
        return Path(temp_dir)
    
    def cleanup_temp_files(self, *paths: Path):
        """Clean up temporary files and directories."""
        for path in paths:
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
            except Exception as e:
                self.logger.warning(f"Failed to cleanup {path}: {e}")
    
    def create_test_file_structure(self, base_path: Path, structure: Dict[str, Any]):
        """Create a test file structure."""
        for name, content in structure.items():
            file_path = base_path / name
            if isinstance(content, dict):
                # Directory
                file_path.mkdir(parents=True, exist_ok=True)
                self.create_test_file_structure(file_path, content)
            else:
                # File
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(str(content))
    
    # ========================================================================
    # VALIDATION UTILITIES
    # ========================================================================
    
    def validate_object(self, obj: Any, rules: List[ValidationRule]) -> Dict[str, Any]:
        """Validate an object against validation rules."""
        results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        for rule in rules:
            if not hasattr(obj, rule.field_name):
                if rule.required:
                    results["valid"] = False
                    results["errors"].append(f"Required field '{rule.field_name}' missing")
                continue
            
            value = getattr(obj, rule.field_name)
            validation_result = self._validate_field(value, rule)
            
            if not validation_result["valid"]:
                results["valid"] = False
                results["errors"].extend(validation_result["errors"])
            
            if validation_result["warnings"]:
                results["warnings"].extend(validation_result["warnings"])
        
        return results
    
    def _validate_field(self, value: Any, rule: ValidationRule) -> Dict[str, Any]:
        """Validate a single field against a rule."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Type validation
        if rule.validation_type == ValidationType.STRING:
            if not isinstance(value, str):
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' must be a string")
                return result
            
            # Length validation
            if rule.min_length is not None and len(value) < rule.min_length:
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' too short (min: {rule.min_length})")
            
            if rule.max_length is not None and len(value) > rule.max_length:
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' too long (max: {rule.max_length})")
        
        elif rule.validation_type == ValidationType.INTEGER:
            if not isinstance(value, int):
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' must be an integer")
                return result
            
            # Value validation
            if rule.min_value is not None and value < rule.min_value:
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' too small (min: {rule.min_value})")
            
            if rule.max_value is not None and value > rule.max_value:
                result["valid"] = False
                result["errors"].append(f"Field '{rule.field_name}' too large (max: {rule.max_value})")
        
        # Custom validation
        if rule.custom_validator:
            try:
                if not rule.custom_validator(value):
                    result["valid"] = False
                    result["errors"].append(f"Field '{rule.field_name}' failed custom validation")
            except Exception as e:
                result["valid"] = False
                result["errors"].append(f"Custom validation error for '{rule.field_name}': {e}")
        
        return result
    
    # ========================================================================
    # TEST ENVIRONMENT UTILITIES
    # ========================================================================
    
    def setup_test_environment(self, config: TestEnvironment) -> bool:
        """Setup a test environment."""
        try:
            # Set environment variables
            for var_name, var_value in config.variables.items():
                os.environ[var_name] = var_value
            
            # Run setup commands
            for command in config.setup_commands:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error(f"Setup command failed: {command}")
                    return False
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup test environment: {e}")
            return False
    
    def teardown_test_environment(self, config: TestEnvironment) -> bool:
        """Teardown a test environment."""
        try:
            # Run teardown commands
            for command in config.teardown_commands:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.warning(f"Teardown command failed: {command}")
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to teardown test environment: {e}")
            return False
    
    # ========================================================================
    # REPORTING UTILITIES
    # ========================================================================
    
    def generate_test_report(self, config: TestReport) -> str:
        """Generate a test report."""
        report_data = {
            "title": config.title,
            "description": config.description,
            "timestamp": config.timestamp.isoformat(),
            "results": config.results,
            "summary": config.summary,
            "metadata": config.metadata
        }
        
        return json.dumps(report_data, indent=2)
    
    def save_test_report(self, report: str, file_path: Path):
        """Save a test report to file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(report)
        except Exception as e:
            self.logger.error(f"Failed to save test report: {e}")


# Global instance for convenience
UNIFIED_TEST_UTILITIES = UnifiedTestUtilitiesV2()


def get_test_utilities() -> UnifiedTestUtilitiesV2:
    """Get the global test utilities instance."""
    return UNIFIED_TEST_UTILITIES


def create_mock_agent(config: MockObjectConfig = None) -> Mock:
    """Create a mock agent object."""
    return UNIFIED_TEST_UTILITIES.create_mock_agent(config)


def create_mock_task(config: MockObjectConfig = None) -> Mock:
    """Create a mock task object."""
    return UNIFIED_TEST_UTILITIES.create_mock_task(config)


def create_mock_config(config: MockObjectConfig = None) -> Mock:
    """Create a mock configuration object."""
    return UNIFIED_TEST_UTILITIES.create_mock_config(config)


def generate_test_data(config: TestDataConfig) -> Union[Dict, List[Dict]]:
    """Generate test data based on configuration."""
    return UNIFIED_TEST_UTILITIES.generate_test_data(config)
