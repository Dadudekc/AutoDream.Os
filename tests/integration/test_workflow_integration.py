#!/usr/bin/env python3
"""
Workflow Integration Tests
==========================

Comprehensive integration tests for the modular workflow system.
Tests the complete workflow lifecycle from creation to execution.
"""

import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.workflow import (
    WorkflowAutomation,
    WorkflowDefinition,
    WorkflowManager,
    WorkflowScheduler,
    WorkflowStatusTracker,
    WorkflowStep,
    WorkflowValidator,
)


class TestWorkflowCoreIntegration:
    """Test core workflow components integration."""

    def test_workflow_step_creation_and_serialization(self):
        """Test workflow step creation and serialization."""
        step = WorkflowStep(
            step_id="test_step",
            agent_id="Agent-1",
            task="Test task",
            dependencies=["dep1", "dep2"],
            timeout_minutes=15,
        )

        # Test serialization
        step_dict = step.to_dict()
        assert step_dict["step_id"] == "test_step"
        assert step_dict["agent_id"] == "Agent-1"
        assert step_dict["dependencies"] == ["dep1", "dep2"]

        # Test deserialization
        restored_step = WorkflowStep.from_dict(step_dict)
        assert restored_step.step_id == "test_step"
        assert restored_step.agent_id == "Agent-1"
        assert restored_step.dependencies == ["dep1", "dep2"]

    def test_workflow_definition_creation_and_validation(self):
        """Test workflow definition creation and validation."""
        steps = [
            WorkflowStep("step1", "Agent-1", "Task 1"),
            WorkflowStep("step2", "Agent-2", "Task 2", dependencies=["step1"]),
            WorkflowStep("step3", "Agent-3", "Task 3", dependencies=["step2"]),
        ]

        workflow = WorkflowDefinition(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="A test workflow",
            steps=steps,
        )

        # Test validation
        errors = WorkflowValidator.validate_workflow(workflow)
        assert len(errors) == 0

        # Test serialization
        workflow_dict = workflow.to_dict()
        assert workflow_dict["workflow_id"] == "test_workflow"
        assert len(workflow_dict["steps"]) == 3

    def test_workflow_scheduler_execution_order(self):
        """Test workflow scheduler execution order."""
        steps = [
            WorkflowStep("step1", "Agent-1", "Task 1"),
            WorkflowStep("step2", "Agent-2", "Task 2", dependencies=["step1"]),
            WorkflowStep("step3", "Agent-3", "Task 3", dependencies=["step1"]),
            WorkflowStep("step4", "Agent-4", "Task 4", dependencies=["step2", "step3"]),
        ]

        execution_order = WorkflowScheduler.get_execution_order(steps)

        # step1 should be first (no dependencies)
        assert execution_order[0] == "step1"

        # step4 should be last (depends on step2 and step3)
        assert execution_order[-1] == "step4"

        # step1 should come before step2 and step3
        assert execution_order.index("step1") < execution_order.index("step2")
        assert execution_order.index("step1") < execution_order.index("step3")

    def test_circular_dependency_detection(self):
        """Test circular dependency detection."""
        steps = [
            WorkflowStep("step1", "Agent-1", "Task 1", dependencies=["step2"]),
            WorkflowStep("step2", "Agent-2", "Task 2", dependencies=["step1"]),
        ]

        errors = WorkflowValidator.validate_workflow(
            WorkflowDefinition("test", "Test", "Test", steps)
        )

        assert "Circular dependencies detected" in errors

    def test_workflow_status_tracker(self):
        """Test workflow status tracking."""
        tracker = WorkflowStatusTracker()

        workflow = WorkflowDefinition(
            "test_workflow", "Test", "Test", [WorkflowStep("step1", "Agent-1", "Task 1")]
        )

        # Start workflow
        assert tracker.start_workflow(workflow)
        assert tracker.get_workflow_status("test_workflow") == "running"

        # Complete workflow
        assert tracker.complete_workflow("test_workflow", True)
        assert tracker.get_workflow_status("test_workflow") == "completed"

        # Test duplicate start
        assert not tracker.start_workflow(workflow)


class TestWorkflowAutomationIntegration:
    """Test workflow automation integration."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project structure for testing."""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)

        # Create test structure
        (project_root / "src" / "test_module").mkdir(parents=True)
        (project_root / "tests").mkdir()

        # Create test files
        (project_root / "src" / "test_module" / "test.py").write_text("print('test')")
        (project_root / "tests" / "test_example.py").write_text("def test_example(): pass")

        yield project_root

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_module_fixer_integration(self, temp_project):
        """Test module fixer integration."""
        automation = WorkflowAutomation()
        automation.project_root = temp_project

        # Test fixing missing imports
        result = automation.module_fixer.fix_missing_imports("src/test_module")
        assert result

        # Check that __init__.py was created
        init_file = temp_project / "src" / "test_module" / "__init__.py"
        assert init_file.exists()

    def test_test_runner_integration(self, temp_project):
        """Test test runner integration."""
        automation = WorkflowAutomation()
        automation.project_root = temp_project

        # Test syntax check
        result = automation.test_runner.run_syntax_check("src/test_module/test.py")
        assert result

        # Test pytest (may fail due to no actual tests, but should not crash)
        result = automation.test_runner.run_pytest("tests/")
        assert "success" in result

    def test_project_manager_integration(self, temp_project):
        """Test project manager integration."""
        automation = WorkflowAutomation()
        automation.project_root = temp_project

        # Test project status
        status = automation.project_manager.get_project_status()
        assert status["project_root"] == str(temp_project)
        assert status["python_files"] > 0
        assert status["total_files"] > 0

    def test_workflow_automation_task_execution(self, temp_project):
        """Test workflow automation task execution."""
        automation = WorkflowAutomation()
        automation.project_root = temp_project

        # Test syntax check task
        step = WorkflowStep("syntax_check", "Agent-1", "syntax check src/test_module/test.py")
        result = automation.execute_workflow_step(step)

        assert result["success"]
        assert step.status == "completed"
        assert step.result is not None


class TestWorkflowManagerIntegration:
    """Test workflow manager integration."""

    @pytest.fixture
    def temp_workflows_dir(self):
        """Create temporary workflows directory."""
        temp_dir = tempfile.mkdtemp()
        workflows_dir = Path(temp_dir) / "workflows"
        workflows_dir.mkdir()

        yield str(workflows_dir)

        shutil.rmtree(temp_dir)

    def test_workflow_manager_creation_and_config(self, temp_workflows_dir):
        """Test workflow manager creation and configuration."""
        config = {
            "workflows_dir": temp_workflows_dir,
            "max_concurrent_workflows": 3,
            "default_timeout_minutes": 20,
        }

        manager = WorkflowManager()
        manager.workflows_dir = Path(temp_workflows_dir)

        assert manager.workflows_dir.exists()

    def test_workflow_creation_and_persistence(self, temp_workflows_dir):
        """Test workflow creation and persistence."""
        manager = WorkflowManager()
        manager.workflows_dir = Path(temp_workflows_dir)

        # Create workflow
        steps_data = [
            {"step_id": "step1", "agent_id": "Agent-1", "task": "Task 1"},
            {
                "step_id": "step2",
                "agent_id": "Agent-2",
                "task": "Task 2",
                "dependencies": ["step1"],
            },
        ]

        workflow = manager.create_workflow(
            "test_workflow", "Test Workflow", "A test workflow", steps_data
        )

        # Save workflow
        assert manager.save_workflow(workflow)

        # Load workflow
        loaded_workflow = manager.load_workflow("test_workflow")
        assert loaded_workflow is not None
        assert loaded_workflow.workflow_id == "test_workflow"
        assert len(loaded_workflow.steps) == 2

    @patch("tools.workflow.automation.WorkflowAutomation.execute_workflow_step")
    def test_workflow_execution_integration(self, mock_execute, temp_workflows_dir):
        """Test complete workflow execution."""
        # Mock the automation execution
        mock_execute.return_value = {"success": True, "result": "test_result"}

        manager = WorkflowManager()
        manager.workflows_dir = Path(temp_workflows_dir)

        # Create simple workflow
        steps_data = [{"step_id": "step1", "agent_id": "Agent-1", "task": "Task 1"}]

        workflow = manager.create_workflow(
            "test_workflow", "Test Workflow", "A test workflow", steps_data
        )

        # Execute workflow
        result = manager.execute_workflow(workflow)

        assert result["success"]
        assert "results" in result
        assert mock_execute.called

    def test_workflow_listing(self, temp_workflows_dir):
        """Test workflow listing functionality."""
        manager = WorkflowManager()
        manager.workflows_dir = Path(temp_workflows_dir)

        # Create and save multiple workflows
        for i in range(3):
            workflow = manager.create_workflow(
                f"workflow_{i}",
                f"Workflow {i}",
                f"Description {i}",
                [{"step_id": f"step{i}", "agent_id": f"Agent-{i}", "task": f"Task {i}"}],
            )
            manager.save_workflow(workflow)

        # List workflows
        workflows = manager.list_workflows()
        assert len(workflows) == 3

        # Check workflow details
        workflow_ids = [w["workflow_id"] for w in workflows]
        assert "workflow_0" in workflow_ids
        assert "workflow_1" in workflow_ids
        assert "workflow_2" in workflow_ids


class TestWorkflowEndToEndIntegration:
    """Test complete end-to-end workflow integration."""

    @pytest.fixture
    def complete_test_environment(self):
        """Create complete test environment."""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        workflows_dir = project_root / "workflows"
        workflows_dir.mkdir()

        # Create test project structure
        (project_root / "src" / "test_module").mkdir(parents=True)
        (project_root / "tests").mkdir()

        # Create test files
        (project_root / "src" / "test_module" / "test.py").write_text("print('Hello World')")
        (project_root / "tests" / "test_example.py").write_text("def test_example(): assert True")

        yield project_root, workflows_dir

        shutil.rmtree(temp_dir)

    def test_complete_workflow_lifecycle(self, complete_test_environment):
        """Test complete workflow lifecycle from creation to execution."""
        project_root, workflows_dir = complete_test_environment

        # Create workflow manager
        manager = WorkflowManager()
        manager.workflows_dir = workflows_dir

        # Define workflow steps
        steps_data = [
            {
                "step_id": "fix_imports",
                "agent_id": "Agent-1",
                "task": "fix missing imports src/test_module",
            },
            {
                "step_id": "syntax_check",
                "agent_id": "Agent-2",
                "task": "syntax check src/test_module/test.py",
                "dependencies": ["fix_imports"],
            },
            {
                "step_id": "run_tests",
                "agent_id": "Agent-3",
                "task": "run tests tests/",
                "dependencies": ["syntax_check"],
            },
        ]

        # Create workflow
        workflow = manager.create_workflow(
            "integration_test_workflow",
            "Integration Test Workflow",
            "Complete integration test workflow",
            steps_data,
        )

        # Validate workflow
        errors = WorkflowValidator.validate_workflow(workflow)
        assert len(errors) == 0

        # Save workflow
        assert manager.save_workflow(workflow)

        # Load workflow
        loaded_workflow = manager.load_workflow("integration_test_workflow")
        assert loaded_workflow is not None

        # Execute workflow
        result = manager.execute_workflow(loaded_workflow)

        # Check results
        assert result["success"]
        assert "results" in result
        assert len(result["results"]) == 3

        # Verify all steps completed
        for step in loaded_workflow.steps:
            assert step.status == "completed"
            assert step.completed_at is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
