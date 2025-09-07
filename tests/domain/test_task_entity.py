"""
Domain Tests - Task Entity
==========================

Unit tests for the Task entity to validate domain logic.
"""

import pytest
from datetime import datetime, timedelta
from src.domain.entities.task import Task
from src.domain.value_objects.ids import TaskId, AgentId


class TestTask:
    """Test cases for Task entity business logic."""

    def test_task_creation(self):
        """Test basic task creation."""
        task_id = TaskId("task-123")
        task = Task(id=task_id, title="Test Task")

        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.is_pending
        assert not task.is_assigned
        assert not task.is_completed
        assert task.priority == 1

    def test_task_with_description_and_priority(self):
        """Test task creation with description and custom priority."""
        task_id = TaskId("task-456")
        task = Task(
            id=task_id,
            title="Important Task",
            description="This is a very important task",
            priority=4
        )

        assert task.description == "This is a very important task"
        assert task.priority == 4

    def test_task_creation_validation(self):
        """Test task creation validation."""
        # Empty title should raise ValueError
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=TaskId("task-123"), title="")

        # Invalid priority should raise ValueError
        with pytest.raises(ValueError, match="Task priority must be between 1 and 4"):
            Task(id=TaskId("task-123"), title="Test", priority=0)

        with pytest.raises(ValueError, match="Task priority must be between 1 and 4"):
            Task(id=TaskId("task-123"), title="Test", priority=5)

    def test_task_assignment(self):
        """Test task assignment to agent."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id = AgentId("agent-456")

        # Initially unassigned
        assert task.is_pending
        assert not task.is_assigned

        # Assign to agent
        task.assign_to(agent_id)

        assert task.is_assigned
        assert task.assigned_agent_id == agent_id
        assert task.assigned_at is not None
        assert not task.is_pending

    def test_task_completion(self):
        """Test task completion."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id = AgentId("agent-456")

        # Assign first
        task.assign_to(agent_id)
        assert task.is_assigned
        assert not task.is_completed

        # Complete task
        task.complete()

        assert task.is_completed
        assert task.completed_at is not None
        assert not task.is_pending

    def test_cannot_assign_completed_task(self):
        """Test that completed tasks cannot be reassigned."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id_1 = AgentId("agent-456")
        agent_id_2 = AgentId("agent-789")

        # Assign and complete
        task.assign_to(agent_id_1)
        task.complete()

        # Try to assign again - should raise error
        with pytest.raises(ValueError, match="Cannot assign a completed task"):
            task.assign_to(agent_id_2)

    def test_cannot_complete_unassigned_task(self):
        """Test that unassigned tasks cannot be completed."""
        task = Task(id=TaskId("task-123"), title="Test Task")

        # Try to complete without assignment
        with pytest.raises(ValueError, match="Cannot complete an unassigned task"):
            task.complete()

    def test_task_unassignment(self):
        """Test task unassignment from agent."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id = AgentId("agent-456")

        # Assign first
        task.assign_to(agent_id)
        assert task.is_assigned

        # Unassign
        task.unassign()

        assert not task.is_assigned
        assert task.assigned_agent_id is None
        assert task.assigned_at is None
        assert task.is_pending

    def test_cannot_unassign_completed_task(self):
        """Test that completed tasks cannot be unassigned."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id = AgentId("agent-456")

        # Assign and complete
        task.assign_to(agent_id)
        task.complete()

        # Try to unassign - should raise error
        with pytest.raises(ValueError, match="Cannot unassign a completed task"):
            task.unassign()

    def test_task_assignment_validation(self):
        """Test task assignment validation methods."""
        task = Task(id=TaskId("task-123"), title="Test Task")
        agent_id = AgentId("agent-456")

        # Initially can be assigned to any agent
        assert task.can_be_assigned_to(agent_id)

        # After assignment, cannot be assigned to same agent again
        task.assign_to(agent_id)
        assert not task.can_be_assigned_to(agent_id)

        # After completion, cannot be assigned to any agent
        task.complete()
        assert not task.can_be_assigned_to(agent_id)
        assert not task.can_be_assigned_to(AgentId("different-agent"))

    def test_task_properties(self):
        """Test task computed properties."""
        task = Task(id=TaskId("task-123"), title="Test Task")

        # Initially pending
        assert task.is_pending
        assert not task.is_assigned
        assert not task.is_completed

        # After assignment
        task.assign_to(AgentId("agent-456"))
        assert not task.is_pending
        assert task.is_assigned
        assert not task.is_completed

        # After completion
        task.complete()
        assert not task.is_pending
        assert task.is_assigned  # Completed tasks remain assigned (historical record)
        assert task.is_completed
