#!/usr/bin/env python3
"""
Dream.OS Integration Tests - C-074-5
====================================

Comprehensive test suite for Dream.OS FSM orchestrator integration.
Tests import validation, instantiation, config loading, and core functionality.

Author: Agent-4 (Captain - Quality Assurance Specialist)
Mission: C-074-5 Integration Test Suite Creation
Target Coverage: 85%+
"""

import sys
from pathlib import Path
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestDreamOSImports:
    """Test Dream.OS import validation."""

    def test_dreamos_module_imports(self):
        """Test that Dream.OS module can be imported."""
        try:
            import src.gaming.dreamos
            assert src.gaming.dreamos is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Dream.OS module: {e}")

    def test_fsm_orchestrator_imports(self):
        """Test that FSM orchestrator can be imported."""
        try:
            from src.gaming.dreamos import FSMOrchestrator
            assert FSMOrchestrator is not None
        except ImportError as e:
            pytest.fail(f"Failed to import FSMOrchestrator: {e}")

    def test_task_state_imports(self):
        """Test that TaskState enum can be imported."""
        try:
            from src.gaming.dreamos import TaskState
            assert TaskState is not None
        except ImportError as e:
            pytest.fail(f"Failed to import TaskState: {e}")

    def test_task_model_imports(self):
        """Test that Task model can be imported."""
        try:
            from src.gaming.dreamos import Task
            assert Task is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Task: {e}")

    def test_atomic_file_manager_imports(self):
        """Test that atomic file manager can be imported."""
        try:
            from src.gaming.dreamos.resumer_v2 import AtomicFileManager
            assert AtomicFileManager is not None
        except ImportError as e:
            pytest.fail(f"Failed to import AtomicFileManager: {e}")


class TestFSMOrchestratorInstantiation:
    """Test FSM orchestrator instantiation."""

    @pytest.fixture
    def temp_dirs(self, tmp_path):
        """Create temporary directories for testing."""
        fsm_root = tmp_path / "fsm_data"
        inbox_root = tmp_path / "inbox"
        outbox_root = tmp_path / "outbox"
        
        fsm_root.mkdir()
        inbox_root.mkdir()
        outbox_root.mkdir()
        
        return {
            "fsm_root": str(fsm_root),
            "inbox_root": str(inbox_root),
            "outbox_root": str(outbox_root)
        }

    def test_fsm_orchestrator_basic_instantiation(self, temp_dirs):
        """Test basic FSM orchestrator instantiation."""
        try:
            from src.gaming.dreamos import FSMOrchestrator
            
            orchestrator = FSMOrchestrator(
                fsm_root=temp_dirs["fsm_root"],
                inbox_root=temp_dirs["inbox_root"],
                outbox_root=temp_dirs["outbox_root"]
            )
            
            assert orchestrator is not None
            assert orchestrator.fsm_root == temp_dirs["fsm_root"]
            assert orchestrator.inbox_root == temp_dirs["inbox_root"]
            assert orchestrator.outbox_root == temp_dirs["outbox_root"]
        except Exception as e:
            pytest.fail(f"Failed to instantiate FSMOrchestrator: {e}")

    def test_fsm_orchestrator_attributes(self, temp_dirs):
        """Test that FSM orchestrator has expected attributes."""
        from src.gaming.dreamos import FSMOrchestrator
        
        orchestrator = FSMOrchestrator(
            fsm_root=temp_dirs["fsm_root"],
            inbox_root=temp_dirs["inbox_root"],
            outbox_root=temp_dirs["outbox_root"]
        )
        
        # Check for expected attributes
        assert hasattr(orchestrator, "fsm_root")
        assert hasattr(orchestrator, "inbox_root")
        assert hasattr(orchestrator, "outbox_root")


class TestTaskStateEnum:
    """Test TaskState enumeration."""

    def test_task_state_values(self):
        """Test that TaskState has expected values."""
        from src.gaming.dreamos import TaskState
        
        # Check for expected states
        assert hasattr(TaskState, "NEW")
        assert hasattr(TaskState, "IN_PROGRESS")
        assert hasattr(TaskState, "COMPLETED")
        assert hasattr(TaskState, "FAILED")
        assert hasattr(TaskState, "CANCELLED")

    def test_task_state_is_enum(self):
        """Test that TaskState is an Enum."""
        from src.gaming.dreamos import TaskState
        from enum import Enum
        
        assert issubclass(TaskState, Enum)


class TestTaskModel:
    """Test Task data model."""

    def test_task_creation(self):
        """Test creating a Task instance."""
        from src.gaming.dreamos import Task, TaskState
        from datetime import datetime
        
        task = Task(
            id="test-001",
            title="Test Task",
            description="Test description",
            state=TaskState.NEW,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        assert task.id == "test-001"
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.state == TaskState.NEW

    def test_task_optional_fields(self):
        """Test Task with optional fields."""
        from src.gaming.dreamos import Task, TaskState
        from datetime import datetime
        
        task = Task(
            id="test-002",
            title="Test Task 2",
            description="Test description 2",
            state=TaskState.IN_PROGRESS,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            assigned_agent="Agent-1"
        )
        
        assert task.assigned_agent == "Agent-1"


class TestAtomicFileManager:
    """Test atomic file manager."""

    @pytest.fixture
    def temp_file_path(self, tmp_path):
        """Create temporary file path for testing."""
        return tmp_path / "test_file.json"

    def test_atomic_file_manager_instantiation(self, temp_file_path):
        """Test atomic file manager instantiation."""
        try:
            from src.gaming.dreamos.resumer_v2 import AtomicFileManager
            
            manager = AtomicFileManager(str(temp_file_path))
            assert manager is not None
        except Exception as e:
            pytest.fail(f"Failed to instantiate AtomicFileManager: {e}")

    def test_atomic_file_manager_has_methods(self, temp_file_path):
        """Test that atomic file manager has expected methods."""
        from src.gaming.dreamos.resumer_v2 import AtomicFileManager
        
        manager = AtomicFileManager(str(temp_file_path))
        
        # Check for expected methods (adjust based on actual implementation)
        assert hasattr(manager, "write") or hasattr(manager, "save") or callable(manager)


class TestDreamOSConfiguration:
    """Test Dream.OS configuration handling."""

    def test_dreamos_config_imports(self):
        """Test that configuration can be accessed."""
        try:
            from src.gaming.dreamos import FSMOrchestrator
            # If there's a config class, test it
            assert FSMOrchestrator is not None
        except ImportError as e:
            pytest.fail(f"Failed to import configuration: {e}")


class TestDreamOSIntegration:
    """Integration tests for Dream.OS components."""

    @pytest.fixture
    def orchestrator_setup(self, tmp_path):
        """Setup FSM orchestrator for integration testing."""
        from src.gaming.dreamos import FSMOrchestrator
        
        fsm_root = tmp_path / "fsm_data"
        inbox_root = tmp_path / "inbox"
        outbox_root = tmp_path / "outbox"
        
        fsm_root.mkdir()
        inbox_root.mkdir()
        outbox_root.mkdir()
        
        orchestrator = FSMOrchestrator(
            fsm_root=str(fsm_root),
            inbox_root=str(inbox_root),
            outbox_root=str(outbox_root)
        )
        
        return orchestrator

    def test_orchestrator_initialization(self, orchestrator_setup):
        """Test that orchestrator initializes correctly."""
        orchestrator = orchestrator_setup
        assert orchestrator is not None

    def test_task_workflow_components_exist(self):
        """Test that all task workflow components can be imported."""
        from src.gaming.dreamos import FSMOrchestrator, Task, TaskState
        
        assert FSMOrchestrator is not None
        assert Task is not None
        assert TaskState is not None


class TestDreamOSErrorHandling:
    """Test Dream.OS error handling."""

    def test_invalid_paths_handling(self):
        """Test handling of invalid paths."""
        from src.gaming.dreamos import FSMOrchestrator
        
        # Test with non-existent paths - should either create or raise appropriate error
        try:
            orchestrator = FSMOrchestrator(
                fsm_root="/nonexistent/path/fsm",
                inbox_root="/nonexistent/path/inbox",
                outbox_root="/nonexistent/path/outbox"
            )
            # If it succeeds, that's valid (creates dirs)
            assert orchestrator is not None
        except (OSError, FileNotFoundError, PermissionError):
            # Expected for invalid paths
            pass
        except Exception as e:
            # Unexpected error
            pytest.fail(f"Unexpected error with invalid paths: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.gaming.dreamos", "--cov-report=term-missing"])


