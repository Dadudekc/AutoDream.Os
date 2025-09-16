#!/usr/bin/env python3
"""
Test Task Claiming Automation - Task Claiming Automation Test
============================================================

Test script for task claiming automation system.
Part of the task claiming automation implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import sys
import tempfile
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.task_claiming_automation import TaskClaimingAutomation, Task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_task_claiming_automation_initialization():
    """Test task claiming automation initialization."""
    logger.info("Testing task claiming automation initialization...")
    
    try:
        # Initialize automation
        automation = TaskClaimingAutomation("Agent-2")
        
        # Verify initialization
        assert automation.agent_id == "Agent-2"
        assert automation.workspace_path.name == "Agent-2"
        
        # Check metrics
        metrics = automation.get_metrics()
        assert metrics["total_claims_attempted"] == 0
        assert metrics["successful_claims"] == 0
        assert metrics["failed_claims"] == 0
        
        logger.info("✅ Task claiming automation initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Task claiming automation initialization test failed: {e}")
        return False


def test_task_class():
    """Test Task class functionality."""
    logger.info("Testing Task class functionality...")
    
    try:
        # Create test task data
        task_data = {
            "id": "test_task",
            "description": "Test task description",
            "status": "available",
            "assigned_to": "",
            "priority": "high",
            "created_at": "2025-09-15T10:00:00",
            "updated_at": "2025-09-15T10:00:00",
            "completed_at": "",
            "phases": [],
            "dependencies": [],
            "estimated_duration": "30 minutes",
            "created_by": "Agent-2"
        }
        
        # Create task
        task = Task(task_data)
        
        # Verify task properties
        assert task.id == "test_task"
        assert task.description == "Test task description"
        assert task.status == "available"
        assert task.priority == "high"
        
        # Test claimable check
        assert task.is_claimable() == True
        assert task.can_be_claimed_by("Agent-2") == True
        
        # Test to_dict conversion
        task_dict = task.to_dict()
        assert task_dict["id"] == "test_task"
        assert task_dict["priority"] == "high"
        
        logger.info("✅ Task class test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Task class test failed: {e}")
        return False


def test_task_claiming_with_temp_files():
    """Test task claiming with temporary files."""
    logger.info("Testing task claiming with temporary files...")
    
    try:
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test workspace structure
            workspace_dir = temp_path / "agent_workspaces" / "Agent-2"
            workspace_dir.mkdir(parents=True)
            
            # Create test future tasks
            future_tasks = {
                "pending_tasks": [
                    {
                        "id": "test_task_1",
                        "description": "Test task 1",
                        "status": "available",
                        "assigned_to": "",
                        "priority": "high",
                        "created_at": "2025-09-15T10:00:00",
                        "updated_at": "2025-09-15T10:00:00",
                        "dependencies": [],
                        "estimated_duration": "30 minutes",
                        "created_by": "Agent-2"
                    },
                    {
                        "id": "test_task_2",
                        "description": "Test task 2",
                        "status": "available",
                        "assigned_to": "",
                        "priority": "medium",
                        "created_at": "2025-09-15T10:00:00",
                        "updated_at": "2025-09-15T10:00:00",
                        "dependencies": ["test_task_1"],
                        "estimated_duration": "20 minutes",
                        "created_by": "Agent-2"
                    }
                ],
                "completed_future_tasks": []
            }
            
            # Create test working tasks (empty)
            working_tasks = {
                "current_task": None,
                "previous_task": None,
                "completed_tasks": []
            }
            
            # Write test files
            future_tasks_file = workspace_dir / "future_tasks.json"
            working_tasks_file = workspace_dir / "working_tasks.json"
            
            future_tasks_file.write_text(json.dumps(future_tasks, indent=2))
            working_tasks_file.write_text(json.dumps(working_tasks, indent=2))
            
            # Initialize automation with temporary path
            automation = TaskClaimingAutomation("Agent-2")
            automation.workspace_path = workspace_dir
            automation.future_tasks_path = future_tasks_file
            automation.working_tasks_path = working_tasks_file
            
            # Test getting available tasks
            available_tasks = automation.get_available_tasks()
            assert len(available_tasks) == 2
            
            # Test task claiming
            result = automation.claim_task()
            assert result["success"] == True
            assert result["task_id"] == "test_task_1"  # Should select high priority task
            
            # Verify task was moved to working tasks
            updated_working_tasks = automation._load_working_tasks()
            assert updated_working_tasks["current_task"]["id"] == "test_task_1"
            assert updated_working_tasks["current_task"]["status"] == "in_progress"
            
            # Verify task was removed from future tasks
            updated_future_tasks = automation._load_future_tasks()
            assert len(updated_future_tasks["pending_tasks"]) == 1
            assert updated_future_tasks["pending_tasks"][0]["id"] == "test_task_2"
            
        logger.info("✅ Task claiming with temporary files test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Task claiming with temporary files test failed: {e}")
        return False


def test_dependency_validation():
    """Test task dependency validation."""
    logger.info("Testing task dependency validation...")
    
    try:
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            workspace_dir = temp_path / "agent_workspaces" / "Agent-2"
            workspace_dir.mkdir(parents=True)
            
            # Create test working tasks with completed task
            working_tasks = {
                "current_task": None,
                "previous_task": None,
                "completed_tasks": [
                    {"id": "completed_task", "description": "Completed task", "status": "completed"}
                ]
            }
            
            # Create test future tasks with dependency
            future_tasks = {
                "pending_tasks": [
                    {
                        "id": "dependent_task",
                        "description": "Task with dependency",
                        "status": "available",
                        "assigned_to": "",
                        "priority": "high",
                        "created_at": "2025-09-15T10:00:00",
                        "updated_at": "2025-09-15T10:00:00",
                        "dependencies": ["completed_task"],
                        "estimated_duration": "30 minutes",
                        "created_by": "Agent-2"
                    },
                    {
                        "id": "blocked_task",
                        "description": "Task with unmet dependency",
                        "status": "available",
                        "assigned_to": "",
                        "priority": "high",
                        "created_at": "2025-09-15T10:00:00",
                        "updated_at": "2025-09-15T10:00:00",
                        "dependencies": ["unmet_dependency"],
                        "estimated_duration": "30 minutes",
                        "created_by": "Agent-2"
                    }
                ],
                "completed_future_tasks": []
            }
            
            # Write test files
            future_tasks_file = workspace_dir / "future_tasks.json"
            working_tasks_file = workspace_dir / "working_tasks.json"
            
            future_tasks_file.write_text(json.dumps(future_tasks, indent=2))
            working_tasks_file.write_text(json.dumps(working_tasks, indent=2))
            
            # Initialize automation
            automation = TaskClaimingAutomation("Agent-2")
            automation.workspace_path = workspace_dir
            automation.future_tasks_path = future_tasks_file
            automation.working_tasks_path = working_tasks_file
            
            # Test dependency validation
            available_tasks = automation.get_available_tasks()
            assert len(available_tasks) == 2
            
            # Test task claiming (should select task with met dependency)
            result = automation.claim_task()
            assert result["success"] == True
            assert result["task_id"] == "dependent_task"
            
        logger.info("✅ Dependency validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Dependency validation test failed: {e}")
        return False


def test_metrics_and_reporting():
    """Test metrics and reporting functionality."""
    logger.info("Testing metrics and reporting functionality...")
    
    try:
        automation = TaskClaimingAutomation("Agent-2")
        
        # Initial metrics
        metrics = automation.get_metrics()
        assert metrics["total_claims_attempted"] == 0
        assert metrics["successful_claims"] == 0
        assert metrics["failed_claims"] == 0
        assert metrics["last_claim_attempt"] is None
        
        # Test report generation
        report = automation.generate_report()
        assert "TASK CLAIMING AUTOMATION REPORT" in report
        assert "Agent-2" in report
        assert "Total Claims Attempted: 0" in report
        
        logger.info("✅ Metrics and reporting test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Metrics and reporting test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting task claiming automation tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Task Claiming Automation Initialization", test_task_claiming_automation_initialization()))
    test_results.append(("Task Class Functionality", test_task_class()))
    test_results.append(("Task Claiming with Temporary Files", test_task_claiming_with_temp_files()))
    test_results.append(("Dependency Validation", test_dependency_validation()))
    test_results.append(("Metrics and Reporting", test_metrics_and_reporting()))
    
    # Report results
    logger.info("\n📊 Test Results Summary:")
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info(f"\n🎯 Overall Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Task claiming automation is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())





