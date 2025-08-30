#!/usr/bin/env python3
"""
Test Suite for Unified Services - Agent Cellphone V2
===================================================

Comprehensive testing for all unified services to ensure they work correctly
and integrate properly. Tests cover functionality, error handling, and
integration between services.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import unittest
import tempfile
import json
import yaml
import os
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.services import (
    UnifiedTaskService,
    UnifiedWorkflowService,
    UnifiedValidationService,
    UnifiedConfigurationService
)
from src.core.services.unified_workflow_service import (
    WorkflowDefinition, WorkflowStep, WorkflowStatus, WorkflowType
)
from src.core.services.unified_validation_service import (
    ValidationSchema, ValidationType, ValidationContext
)
from src.core.services.unified_configuration_service import (
    ConfigurationProfile, ConfigurationType, ConfigurationScope
)


class TestUnifiedTaskService(unittest.TestCase):
    """Test cases for UnifiedTaskService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task_service = UnifiedTaskService()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self.task_service, 'stop'):
            self.task_service.stop()
    
    def test_service_initialization(self):
        """Test that the task service initializes correctly."""
        self.assertIsNotNone(self.task_service)
        self.assertEqual(self.task_service.config.name, "UnifiedTaskService")
        self.assertEqual(self.task_service.state.value, "active")
    
    def test_create_task(self):
        """Test task creation."""
        task_data = {
            "name": "Test Task",
            "description": "A test task",
            "priority": 3,
            "estimated_duration": 60
        }
        
        task_id = self.task_service.create_task(task_data)
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.task_service.tasks)
        
        task = self.task_service.tasks[task_id]
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "A test task")
        self.assertEqual(task.priority.value, 3)
        self.assertEqual(task.estimated_duration, 60)
    
    def test_assign_task(self):
        """Test task assignment."""
        # Create a task first
        task_id = self.task_service.create_task({"name": "Test Task"})
        
        # Assign the task
        result = self.task_service.assign_task(task_id, "agent_123")
        self.assertTrue(result)
        
        # Check assignment
        self.assertEqual(self.task_service.tasks[task_id].assignee, "agent_123")
        self.assertEqual(self.task_service.executions[task_id].status.value, "assigned")
    
    def test_start_task(self):
        """Test task starting."""
        # Create and assign a task
        task_id = self.task_service.create_task({"name": "Test Task"})
        self.task_service.assign_task(task_id, "agent_123")
        
        # Start the task
        result = self.task_service.start_task(task_id, "agent_123")
        self.assertTrue(result)
        
        # Check status
        self.assertEqual(self.task_service.executions[task_id].status.value, "in_progress")
    
    def test_complete_task(self):
        """Test task completion."""
        # Create, assign, and start a task
        task_id = self.task_service.create_task({"name": "Test Task"})
        self.task_service.assign_task(task_id, "agent_123")
        self.task_service.start_task(task_id, "agent_123")
        
        # Complete the task
        result = self.task_service.complete_task(task_id, "Task completed")
        self.assertTrue(result)
        
        # Check status
        self.assertEqual(self.task_service.executions[task_id].status.value, "completed")
        self.assertEqual(self.task_service.tasks[task_id].result, "Task completed")
    
    def test_fail_task(self):
        """Test task failure."""
        # Create, assign, and start a task
        task_id = self.task_service.create_task({"name": "Test Task"})
        self.task_service.assign_task(task_id, "agent_123")
        self.task_service.start_task(task_id, "agent_123")
        
        # Fail the task
        result = self.task_service.fail_task(task_id, "Task failed")
        self.assertTrue(result)
        
        # Check status
        self.assertEqual(self.task_service.executions[task_id].status.value, "failed")
        self.assertEqual(self.task_service.tasks[task_id].error, "Task failed")
    
    def test_get_task_status(self):
        """Test getting task status."""
        # Create a task
        task_id = self.task_service.create_task({
            "name": "Test Task",
            "description": "A test task",
            "priority": 4
        })
        
        # Get status
        status = self.task_service.get_task_status(task_id)
        self.assertIsNotNone(status)
        self.assertEqual(status["name"], "Test Task")
        self.assertEqual(status["description"], "A test task")
        self.assertEqual(status["priority"], 4)
        self.assertEqual(status["status"], "pending")
    
    def test_get_agent_tasks(self):
        """Test getting tasks for a specific agent."""
        # Create and assign tasks
        task1_id = self.task_service.create_task({"name": "Task 1"})
        task2_id = self.task_service.create_task({"name": "Task 2"})
        
        self.task_service.assign_task(task1_id, "agent_123")
        self.task_service.assign_task(task2_id, "agent_123")
        
        # Get agent tasks
        agent_tasks = self.task_service.get_agent_tasks("agent_123")
        self.assertEqual(len(agent_tasks), 2)
        
        task_names = [task["name"] for task in agent_tasks]
        self.assertIn("Task 1", task_names)
        self.assertIn("Task 2", task_names)
    
    def test_task_statistics(self):
        """Test task statistics tracking."""
        # Create some tasks
        self.task_service.create_task({"name": "Task 1"})
        self.task_service.create_task({"name": "Task 2"})
        
        # Get statistics
        stats = self.task_service.get_task_statistics()
        self.assertEqual(stats["total_tasks"], 2)
        self.assertEqual(stats["pending_tasks"], 2)
    
    def test_cleanup_completed_tasks(self):
        """Test cleanup of completed tasks."""
        # Create and complete a task
        task_id = self.task_service.create_task({"name": "Test Task"})
        self.task_service.assign_task(task_id, "agent_123")
        self.task_service.start_task(task_id, "agent_123")
        self.task_service.complete_task(task_id)
        
        # Cleanup
        cleaned_count = self.task_service.cleanup_completed_tasks(max_age_hours=0)
        self.assertEqual(cleaned_count, 1)
        
        # Check that task was removed
        self.assertNotIn(task_id, self.task_service.tasks)


class TestUnifiedWorkflowService(unittest.TestCase):
    """Test cases for UnifiedWorkflowService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.workflow_service = UnifiedWorkflowService()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self.workflow_service, 'stop'):
            self.workflow_service.stop()
    
    def test_service_initialization(self):
        """Test that the workflow service initializes correctly."""
        self.assertIsNotNone(self.workflow_service)
        self.assertEqual(self.workflow_service.config.name, "UnifiedWorkflowService")
        self.assertEqual(self.workflow_service.state.value, "active")
    
    def test_create_workflow(self):
        """Test workflow creation."""
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="A test workflow",
            steps=[
                WorkflowStep(step_id="step1", name="Step 1", step_type="action"),
                WorkflowStep(step_id="step2", name="Step 2", step_type="action")
            ]
        )
        
        workflow_id = self.workflow_service.create_workflow(workflow_def)
        self.assertEqual(workflow_id, "test_workflow")
        self.assertIn("test_workflow", self.workflow_service.workflow_definitions)
    
    def test_deploy_workflow(self):
        """Test workflow deployment."""
        # Create a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[]
        )
        self.workflow_service.create_workflow(workflow_def)
        
        # Deploy the workflow
        result = self.workflow_service.deploy_workflow("test_workflow")
        self.assertTrue(result)
        
        # Check status
        workflow = self.workflow_service.workflow_definitions["test_workflow"]
        self.assertEqual(workflow.status, WorkflowStatus.DEPLOYED)
    
    def test_start_workflow(self):
        """Test workflow execution."""
        # Create and deploy a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[
                WorkflowStep(step_id="step1", name="Step 1", step_type="action")
            ]
        )
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("test_workflow")
        
        # Start the workflow
        execution_id = self.workflow_service.start_workflow("test_workflow")
        self.assertIsNotNone(execution_id)
        self.assertIn(execution_id, self.workflow_service.workflow_executions)
    
    def test_get_workflow_status(self):
        """Test getting workflow status."""
        # Create a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="A test workflow",
            steps=[]
        )
        self.workflow_service.create_workflow(workflow_def)
        
        # Get status
        status = self.workflow_service.get_workflow_status("test_workflow")
        self.assertIsNotNone(status)
        self.assertEqual(status["name"], "Test Workflow")
        self.assertEqual(status["description"], "A test workflow")
        self.assertEqual(status["step_count"], 0)
    
    def test_get_execution_status(self):
        """Test getting execution status."""
        # Create, deploy, and start a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[
                WorkflowStep(step_id="step1", name="Step 1", step_type="action")
            ]
        )
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("test_workflow")
        execution_id = self.workflow_service.start_workflow("test_workflow")
        
        # Get execution status
        status = self.workflow_service.get_execution_status(execution_id)
        self.assertIsNotNone(status)
        self.assertEqual(status["workflow_id"], "test_workflow")
        self.assertEqual(status["workflow_name"], "Test Workflow")
    
    def test_pause_and_resume_workflow(self):
        """Test workflow pause and resume."""
        # Create, deploy, and start a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[]
        )
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("test_workflow")
        execution_id = self.workflow_service.start_workflow("test_workflow")
        
        # Pause the workflow
        result = self.workflow_service.pause_workflow(execution_id)
        self.assertTrue(result)
        
        # Resume the workflow
        result = self.workflow_service.resume_workflow(execution_id)
        self.assertTrue(result)
    
    def test_cancel_workflow(self):
        """Test workflow cancellation."""
        # Create, deploy, and start a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[]
        )
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("test_workflow")
        execution_id = self.workflow_service.start_workflow("test_workflow")
        
        # Cancel the workflow
        result = self.workflow_service.cancel_workflow(execution_id)
        self.assertTrue(result)
        
        # Check status
        execution = self.workflow_service.workflow_executions[execution_id]
        self.assertEqual(execution.status, WorkflowStatus.CANCELLED)
    
    def test_workflow_statistics(self):
        """Test workflow statistics tracking."""
        # Create a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            steps=[]
        )
        self.workflow_service.create_workflow(workflow_def)
        
        # Get statistics
        stats = self.workflow_service.get_workflow_statistics()
        self.assertEqual(stats["total_workflows"], 1)


class TestUnifiedValidationService(unittest.TestCase):
    """Test cases for UnifiedValidationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validation_service = UnifiedValidationService()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self.validation_service, 'stop'):
            self.validation_service.stop()
    
    def test_service_initialization(self):
        """Test that the validation service initializes correctly."""
        self.assertIsNotNone(self.validation_service)
        self.assertEqual(self.validation_service.config.name, "UnifiedValidationService")
        self.assertEqual(self.validation_service.state.value, "active")
    
    def test_builtin_validators_initialization(self):
        """Test that built-in validators are initialized."""
        self.assertIn("builtin_string", self.validation_service.validation_rules)
        self.assertIn("builtin_integer", self.validation_service.validation_rules)
        self.assertIn("builtin_email", self.validation_service.validation_rules)
    
    def test_validate_data_with_rules(self):
        """Test data validation using built-in rules."""
        # Test valid data
        result = self.validation_service.validate_data({
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        })
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        
        # Test invalid data
        result = self.validation_service.validate_data({
            "name": "",  # Empty string
            "email": "invalid-email",  # Invalid email
            "age": -5  # Negative age
        })
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_validate_data_with_schema(self):
        """Test data validation using schema."""
        # Create a validation schema
        schema = ValidationSchema(
            schema_id="user_schema",
            name="User Validation Schema",
            fields={
                "name": {"type": "string", "required": True},
                "email": {"type": "email", "required": True},
                "age": {"type": "integer", "min_value": 0, "max_value": 150}
            },
            required_fields=["name", "email"]
        )
        
        self.validation_service.add_schema(schema)
        
        # Test valid data
        result = self.validation_service.validate_data(
            {"name": "John Doe", "email": "john@example.com", "age": 30},
            schema_id="user_schema"
        )
        self.assertTrue(result.is_valid)
        
        # Test invalid data (missing required field)
        result = self.validation_service.validate_data(
            {"email": "john@example.com", "age": 30},
            schema_id="user_schema"
        )
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_add_schema(self):
        """Test adding validation schemas."""
        schema = ValidationSchema(
            schema_id="test_schema",
            name="Test Schema",
            fields={"test_field": {"type": "string"}}
        )
        
        result = self.validation_service.add_schema(schema)
        self.assertTrue(result)
        self.assertIn("test_schema", self.validation_service.validation_schemas)
    
    def test_get_schema(self):
        """Test retrieving validation schemas."""
        schema = ValidationSchema(
            schema_id="test_schema",
            name="Test Schema",
            fields={}
        )
        
        self.validation_service.add_schema(schema)
        retrieved_schema = self.validation_service.get_schema("test_schema")
        self.assertEqual(retrieved_schema, schema)
    
    def test_list_schemas(self):
        """Test listing validation schemas."""
        # Add a schema
        schema = ValidationSchema(
            schema_id="test_schema",
            name="Test Schema",
            fields={}
        )
        self.validation_service.add_schema(schema)
        
        # List schemas
        schemas = self.validation_service.list_schemas()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0]["schema_id"], "test_schema")
    
    def test_validation_statistics(self):
        """Test validation statistics tracking."""
        # Perform some validations
        self.validation_service.validate_data({"test": "data"})
        self.validation_service.validate_data({"invalid": None})
        
        # Get statistics
        stats = self.validation_service.get_validation_statistics()
        self.assertEqual(stats["total_validations"], 2)
        self.assertEqual(stats["successful_validations"], 1)
        self.assertEqual(stats["failed_validations"], 1)
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Add a schema to populate cache
        schema = ValidationSchema(
            schema_id="test_schema",
            name="Test Schema",
            fields={}
        )
        self.validation_service.add_schema(schema)
        
        # Clear cache
        self.validation_service.clear_cache()
        # Cache should be empty (though this is implementation-dependent)
        # We're just testing that the method doesn't raise an exception


class TestUnifiedConfigurationService(unittest.TestCase):
    """Test cases for UnifiedConfigurationService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config_service = UnifiedConfigurationService()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self.config_service, 'stop'):
            self.config_service.stop()
    
    def test_service_initialization(self):
        """Test that the configuration service initializes correctly."""
        self.assertIsNotNone(self.config_service)
        self.assertEqual(self.config_service.config.name, "UnifiedConfigurationService")
        self.assertEqual(self.config_service.state.value, "active")
    
    def test_default_configuration_initialization(self):
        """Test that default configuration is initialized."""
        # Check that default profile exists
        self.assertIn("default", self.config_service.configuration_profiles)
        
        # Check that default sections exist
        self.assertIn("application", self.config_service.sections)
        self.assertIn("database", self.config_service.sections)
        self.assertIn("network", self.config_service.sections)
        self.assertIn("performance", self.config_service.sections)
    
    def test_get_value(self):
        """Test getting configuration values."""
        # Test getting existing value
        app_name = self.config_service.get_value("application", "name")
        self.assertEqual(app_name, "Agent Cellphone V2")
        
        # Test getting non-existent value with default
        non_existent = self.config_service.get_value("non_existent", "key", "default_value")
        self.assertEqual(non_existent, "default_value")
    
    def test_set_value(self):
        """Test setting configuration values."""
        # Set a new value
        result = self.config_service.set_value("custom", "test_key", "test_value", "Test description")
        self.assertTrue(result)
        
        # Verify the value was set
        value = self.config_service.get_value("custom", "test_key")
        self.assertEqual(value, "test_value")
    
    def test_load_json_configuration(self):
        """Test loading JSON configuration."""
        # Create a temporary JSON config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "test_section": {
                    "test_key": "test_value"
                }
            }, f)
            temp_file = f.name
        
        try:
            # Load the configuration
            result = self.config_service.load_configuration(temp_file)
            self.assertTrue(result)
            
            # Verify the configuration was loaded
            value = self.config_service.get_value("test_section", "test_key")
            self.assertEqual(value, "test_value")
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_load_yaml_configuration(self):
        """Test loading YAML configuration."""
        # Create a temporary YAML config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            yaml.dump({
                "test_section": {
                    "test_key": "test_value"
                }
            }, f)
            temp_file = f.name
        
        try:
            # Load the configuration
            result = self.config_service.load_configuration(temp_file)
            self.assertTrue(result)
            
            # Verify the configuration was loaded
            value = self.config_service.get_value("test_section", "test_key")
            self.assertEqual(value, "test_value")
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_add_configuration_profile(self):
        """Test adding configuration profiles."""
        profile = ConfigurationProfile(
            profile_id="test_profile",
            name="Test Profile",
            description="A test configuration profile",
            profile_type=ConfigurationType.USER,
            scope=ConfigurationScope.USER
        )
        
        result = self.config_service.add_configuration_profile(profile)
        self.assertTrue(result)
        self.assertIn("test_profile", self.config_service.configuration_profiles)
    
    def test_activate_profile(self):
        """Test profile activation."""
        # Add a profile
        profile = ConfigurationProfile(
            profile_id="test_profile",
            name="Test Profile",
            is_active=False
        )
        self.config_service.add_configuration_profile(profile)
        
        # Activate the profile
        result = self.config_service.activate_profile("test_profile")
        self.assertTrue(result)
        self.assertIn("test_profile", self.config_service.active_profiles)
    
    def test_deactivate_profile(self):
        """Test profile deactivation."""
        # Add and activate a profile
        profile = ConfigurationProfile(
            profile_id="test_profile",
            name="Test Profile",
            is_active=True
        )
        self.config_service.add_configuration_profile(profile)
        self.config_service.activate_profile("test_profile")
        
        # Deactivate the profile
        result = self.config_service.deactivate_profile("test_profile")
        self.assertTrue(result)
        self.assertNotIn("test_profile", self.config_service.active_profiles)
    
    def test_get_configuration_profile(self):
        """Test retrieving configuration profiles."""
        profile = ConfigurationProfile(
            profile_id="test_profile",
            name="Test Profile"
        )
        
        self.config_service.add_configuration_profile(profile)
        retrieved_profile = self.config_service.get_configuration_profile("test_profile")
        self.assertEqual(retrieved_profile, profile)
    
    def test_list_configuration_profiles(self):
        """Test listing configuration profiles."""
        # Add a profile
        profile = ConfigurationProfile(
            profile_id="test_profile",
            name="Test Profile"
        )
        self.config_service.add_configuration_profile(profile)
        
        # List profiles
        profiles = self.config_service.list_configuration_profiles()
        self.assertGreaterEqual(len(profiles), 1)  # At least default profile
        
        profile_ids = [p["profile_id"] for p in profiles]
        self.assertIn("test_profile", profile_ids)
    
    def test_get_active_profiles(self):
        """Test getting active profiles."""
        active_profiles = self.config_service.get_active_profiles()
        self.assertIn("default", active_profiles)
    
    def test_export_configuration(self):
        """Test configuration export."""
        # Export to JSON
        json_export = self.config_service.export_configuration()
        self.assertIsNotNone(json_export)
        
        # Parse the export to verify it's valid JSON
        parsed = json.loads(json_export)
        self.assertIn("sections", parsed)
        self.assertIn("profiles", parsed)
    
    def test_configuration_statistics(self):
        """Test configuration statistics tracking."""
        # Load some configuration to update statistics
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"test": {"key": "value"}}, f)
            temp_file = f.name
        
        try:
            self.config_service.load_configuration(temp_file)
            
            # Get statistics
            stats = self.config_service.get_configuration_statistics()
            self.assertGreaterEqual(stats["total_configs_loaded"], 1)
        finally:
            os.unlink(temp_file)
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Set a value to populate cache
        self.config_service.set_value("test", "key", "value")
        
        # Clear cache
        self.config_service.clear_cache()
        # Cache should be empty (though this is implementation-dependent)
        # We're just testing that the method doesn't raise an exception
    
    def test_reload_configuration(self):
        """Test configuration reloading."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"test": {"key": "value"}}, f)
            temp_file = f.name
        
        try:
            # Load configuration
            self.config_service.load_configuration(temp_file)
            
            # Reload configuration
            result = self.config_service.reload_configuration()
            self.assertTrue(result)
        finally:
            os.unlink(temp_file)


class TestUnifiedServicesIntegration(unittest.TestCase):
    """Test cases for integration between unified services."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task_service = UnifiedTaskService()
        self.workflow_service = UnifiedWorkflowService()
        self.validation_service = UnifiedValidationService()
        self.config_service = UnifiedConfigurationService()
    
    def tearDown(self):
        """Clean up test fixtures."""
        for service in [self.task_service, self.workflow_service, 
                       self.validation_service, self.config_service]:
            if hasattr(service, 'stop'):
                service.stop()
    
    def test_services_workflow_integration(self):
        """Test integration between task and workflow services."""
        # Create a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="integration_test",
            name="Integration Test Workflow",
            steps=[
                WorkflowStep(step_id="step1", name="Create Task", step_type="task_creation"),
                WorkflowStep(step_id="step2", name="Execute Task", step_type="task_execution")
            ]
        )
        
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("integration_test")
        
        # Start workflow execution
        execution_id = self.workflow_service.start_workflow("integration_test")
        
        # Create a task that the workflow might manage
        task_id = self.task_service.create_task({
            "name": "Workflow Task",
            "description": "Task created by workflow",
            "priority": 4
        })
        
        # Verify both services are working
        workflow_status = self.workflow_service.get_execution_status(execution_id)
        task_status = self.task_service.get_task_status(task_id)
        
        self.assertIsNotNone(workflow_status)
        self.assertIsNotNone(task_status)
    
    def test_validation_integration(self):
        """Test integration between validation and other services."""
        # Create a validation schema for task data
        task_schema = ValidationSchema(
            schema_id="task_schema",
            name="Task Validation Schema",
            fields={
                "name": {"type": "string", "required": True},
                "priority": {"type": "integer", "min_value": 1, "max_value": 5},
                "estimated_duration": {"type": "integer", "min_value": 1}
            },
            required_fields=["name"]
        )
        
        self.validation_service.add_schema(task_schema)
        
        # Validate task data before creating
        task_data = {
            "name": "Valid Task",
            "priority": 3,
            "estimated_duration": 60
        }
        
        validation_result = self.validation_service.validate_data(
            task_data, schema_id="task_schema"
        )
        
        self.assertTrue(validation_result.is_valid)
        
        # Create task with validated data
        task_id = self.task_service.create_task(task_data)
        self.assertIsNotNone(task_id)
    
    def test_configuration_integration(self):
        """Test integration between configuration and other services."""
        # Set configuration values that other services might use
        self.config_service.set_value("task_service", "max_workers", 10, "Maximum worker threads")
        self.config_service.set_value("workflow_service", "max_executions", 5, "Maximum concurrent executions")
        self.config_service.set_value("validation_service", "cache_size", 1000, "Validation cache size")
        
        # Verify configuration is accessible
        max_workers = self.config_service.get_value("task_service", "max_workers")
        max_executions = self.config_service.get_value("workflow_service", "max_executions")
        cache_size = self.config_service.get_value("validation_service", "cache_size")
        
        self.assertEqual(max_workers, 10)
        self.assertEqual(max_executions, 5)
        self.assertEqual(cache_size, 1000)
    
    def test_comprehensive_workflow(self):
        """Test a comprehensive workflow using all services."""
        # 1. Configure the system
        self.config_service.set_value("workflow", "timeout", 300, "Workflow timeout in seconds")
        self.config_service.set_value("task", "default_priority", 3, "Default task priority")
        
        # 2. Create and validate a workflow
        workflow_def = WorkflowDefinition(
            workflow_id="comprehensive_test",
            name="Comprehensive Test Workflow",
            steps=[
                WorkflowStep(step_id="step1", name="Validate Input", step_type="validation"),
                WorkflowStep(step_id="step2", name="Create Task", step_type="task_creation"),
                WorkflowStep(step_id="step3", name="Execute Task", step_type="task_execution"),
                WorkflowStep(step_id="step4", name="Validate Output", step_type="validation")
            ]
        )
        
        # Validate workflow definition
        workflow_data = {
            "workflow_id": workflow_def.workflow_id,
            "name": workflow_def.name,
            "steps": [{"step_id": step.step_id, "name": step.name} for step in workflow_def.steps]
        }
        
        validation_result = self.validation_service.validate_data(workflow_data)
        self.assertTrue(validation_result.is_valid)
        
        # 3. Create and deploy workflow
        self.workflow_service.create_workflow(workflow_def)
        self.workflow_service.deploy_workflow("comprehensive_test")
        
        # 4. Start workflow execution
        execution_id = self.workflow_service.start_workflow("comprehensive_test")
        
        # 5. Create tasks as part of workflow execution
        task_id = self.task_service.create_task({
            "name": "Workflow Task",
            "description": "Task created by comprehensive workflow",
            "priority": self.config_service.get_value("task", "default_priority", 3)
        })
        
        # 6. Verify all services are working together
        workflow_status = self.workflow_service.get_execution_status(execution_id)
        task_status = self.task_service.get_task_status(task_id)
        config_timeout = self.config_service.get_value("workflow", "timeout")
        
        self.assertIsNotNone(workflow_status)
        self.assertIsNotNone(task_status)
        self.assertEqual(config_timeout, 300)
        
        # 7. Complete the workflow
        self.task_service.assign_task(task_id, "system")
        self.task_service.start_task(task_id, "system")
        self.task_service.complete_task(task_id, "Workflow completed successfully")


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
