from datetime import datetime
from typing import TYPE_CHECKING
import asyncio

import pytest
import unittest

    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager_refactored import DevelopmentTaskManager
from src.autonomous_development.workflow.manager import AutonomousWorkflowManager
from src.utils.stability_improvements import safe_import
from unittest.mock import Mock, AsyncMock, patch, call

#!/usr/bin/env python3
"""
Tests for Autonomous Development Workflow Module
===============================================

Tests the workflow management functionality for autonomous development.
"""


# Use type hints with strings to avoid circular imports
if TYPE_CHECKING:


autonomous_dev_module = safe_import("src.core.autonomous_development")
AutonomousDevelopmentEngine = getattr(
    autonomous_dev_module, "AutonomousDevelopmentEngine", None
)
IntelligentPromptGenerator = getattr(
    autonomous_dev_module, "IntelligentPromptGenerator", None
)
DevelopmentAction = getattr(autonomous_dev_module, "DevelopmentAction", None)


class TestAutonomousWorkflowManager:
    """Test cases for AutonomousWorkflowManager"""

    @pytest.fixture
    def mock_comm_system(self):
        """Create a mock communication system"""
        mock_system = Mock()
        mock_system.send_message_to_all_agents_with_line_breaks = AsyncMock()
        mock_system.send_message_to_agent_with_line_breaks = AsyncMock()
        mock_system.send_message_to_agent = AsyncMock()
        return mock_system

    @pytest.fixture
    def mock_task_manager(self):
        """Create a mock task manager"""
        mock_manager = Mock()
        mock_manager.workflow_stats = {
            "overnight_cycles": 0,
            "autonomous_hours": 0,
            "total_tasks_completed": 0
        }
        mock_manager.get_available_tasks.return_value = []
        mock_manager.get_task_summary.return_value = {
            "total_tasks": 0,
            "available_tasks": 0,
            "claimed_tasks": 0,
            "in_progress_tasks": 0,
            "completed_tasks": 0,
            "completion_rate": 0.0,
            "workflow_stats": {
                "overnight_cycles": 0,
                "autonomous_hours": 0,
                "total_tasks_completed": 0
            }
        }
        return mock_manager

    @pytest.fixture
    def workflow_manager(self, mock_comm_system, mock_task_manager):
        """Create a workflow manager instance for testing"""
        return AutonomousWorkflowManager(mock_comm_system, mock_task_manager)

    def test_init(self, workflow_manager):
        """Test workflow manager initialization"""
        assert workflow_manager.comm_system is not None
        assert workflow_manager.task_manager is not None
        assert workflow_manager.workflow_active is False
        assert workflow_manager.cycle_duration == 3600

    @pytest.mark.asyncio
    async def test_broadcast_workflow_start(self, workflow_manager, mock_comm_system):
        """Test workflow start broadcast"""
        await workflow_manager._broadcast_workflow_start()
        
        # Verify messages were sent
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called
        assert mock_comm_system.send_message_to_agent_with_line_breaks.called

    @pytest.mark.asyncio
    async def test_execute_workflow_cycle(self, workflow_manager, mock_task_manager):
        """Test workflow cycle execution"""
        # Mock the phase methods
        workflow_manager._task_review_and_claiming_phase = AsyncMock()
        workflow_manager._work_execution_phase = AsyncMock()
        workflow_manager._progress_reporting_phase = AsyncMock()
        workflow_manager._cycle_summary_phase = AsyncMock()

        await workflow_manager._execute_workflow_cycle()

        # Verify all phases were called
        workflow_manager._task_review_and_claiming_phase.assert_called_once()
        workflow_manager._work_execution_phase.assert_called_once()
        workflow_manager._progress_reporting_phase.assert_called_once()
        workflow_manager._cycle_summary_phase.assert_called_once()

        # Verify workflow stats were updated
        assert mock_task_manager.workflow_stats["overnight_cycles"] == 1
        assert mock_task_manager.workflow_stats["autonomous_hours"] == 1

    @pytest.mark.asyncio
    async def test_task_review_and_claiming_phase_no_tasks(self, workflow_manager, mock_task_manager):
        """Test task review phase when no tasks are available"""
        mock_task_manager.get_available_tasks.return_value = []
        
        # Mock the broadcast method
        workflow_manager._broadcast_no_tasks_available = AsyncMock()
        
        await workflow_manager._task_review_and_claiming_phase()
        
        # Verify no tasks message was broadcast
        workflow_manager._broadcast_no_tasks_available.assert_called_once()

    @pytest.mark.asyncio
    async def test_task_review_and_claiming_phase_with_tasks(self, workflow_manager, mock_task_manager, mock_comm_system):
        """Test task review phase when tasks are available"""
        # Create mock tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, priority=8, complexity="high", estimated_hours=4.0, required_skills=["python"]),
            Mock(spec=DevelopmentTask, priority=5, complexity="medium", estimated_hours=2.0, required_skills=["git"])
        ]
        mock_task_manager.get_available_tasks.return_value = mock_tasks
        
        # Mock the simulation method
        workflow_manager._simulate_autonomous_task_claiming = AsyncMock()
        
        await workflow_manager._task_review_and_claiming_phase()
        
        # Verify tasks were broadcast
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called
        workflow_manager._simulate_autonomous_task_claiming.assert_called_once_with(mock_tasks)

    def test_format_task_list_for_agents(self, workflow_manager):
        """Test task list formatting for agents"""
        # Create mock tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, 
                 priority=8, 
                 complexity="high", 
                 estimated_hours=4.0, 
                 required_skills=["python", "testing"],
                 title="Test Task 1",
                 description="A test task",
                 task_id="TASK-001"),
            Mock(spec=DevelopmentTask, 
                 priority=5, 
                 complexity="medium", 
                 estimated_hours=2.0, 
                 required_skills=["git"],
                 title="Test Task 2",
                 description="Another test task",
                 task_id="TASK-002")
        ]

        formatted = workflow_manager._format_task_list_for_agents(mock_tasks)
        
        # Verify formatting
        assert "Test Task 1" in formatted
        assert "Test Task 2" in formatted
        assert "Priority: 8" in formatted
        assert "Priority: 5" in formatted
        assert "Complexity: High" in formatted
        assert "Complexity: Medium" in formatted

    def test_format_task_list_for_agents_empty(self, workflow_manager):
        """Test task list formatting with empty task list"""
        formatted = workflow_manager._format_task_list_for_agents([])
        assert formatted == "No tasks available for claiming."

    @pytest.mark.asyncio
    async def test_work_execution_phase_no_active_tasks(self, workflow_manager, mock_task_manager, mock_comm_system):
        """Test work execution phase when no active tasks"""
        mock_task_manager.tasks = {}
        
        await workflow_manager._work_execution_phase()
        
        # Verify no active tasks message was sent
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called

    @pytest.mark.asyncio
    async def test_work_execution_phase_with_active_tasks(self, workflow_manager, mock_task_manager):
        """Test work execution phase with active tasks"""
        # Create mock active tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, status="claimed", progress_percentage=0.0),
            Mock(spec=DevelopmentTask, status="in_progress", progress_percentage=50.0)
        ]
        mock_task_manager.tasks = {"task1": mock_tasks[0], "task2": mock_tasks[1]}
        
        # Mock the simulation method
        workflow_manager._simulate_work_progress = AsyncMock()
        
        await workflow_manager._work_execution_phase()
        
        # Verify work progress simulation was called
        workflow_manager._simulate_work_progress.assert_called_once()

    @pytest.mark.asyncio
    async def test_progress_reporting_phase(self, workflow_manager, mock_task_manager, mock_comm_system):
        """Test progress reporting phase"""
        await workflow_manager._progress_reporting_phase()
        
        # Verify progress summary was sent
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called

    @pytest.mark.asyncio
    async def test_cycle_summary_phase(self, workflow_manager, mock_task_manager, mock_comm_system):
        """Test cycle summary phase"""
        await workflow_manager._cycle_summary_phase()
        
        # Verify cycle summary was sent
        assert mock_comm_system.send_message_to_cycles.called

    def test_format_progress_summary(self, workflow_manager, mock_task_manager):
        """Test progress summary formatting"""
        # Create mock active tasks
        mock_tasks = [
            Mock(spec=DevelopmentTask, 
                 status="claimed", 
                 title="Task 1", 
                 claimed_by="Agent-2", 
                 progress_percentage=0.0, 
                 blockers=[]),
            Mock(spec=DevelopmentTask, 
                 status="in_progress", 
                 title="Task 2", 
                 claimed_by="Agent-3", 
                 progress_percentage=75.0, 
                 blockers=["Waiting for review"])
        ]
        mock_task_manager.tasks = {"task1": mock_tasks[0], "task2": mock_tasks[1]}

        formatted = workflow_manager._format_progress_summary()
        
        # Verify formatting
        assert "Task 1" in formatted
        assert "Task 2" in formatted
        assert "Agent: Agent-2" in formatted
        assert "Agent: Agent-3" in formatted
        assert "Progress: 0.0%" in formatted
        assert "Progress: 75.0%" in formatted

    def test_format_progress_summary_no_active_tasks(self, workflow_manager, mock_task_manager):
        """Test progress summary formatting with no active tasks"""
        mock_task_manager.tasks = {}
        
        formatted = workflow_manager._format_progress_summary()
        assert formatted == "No active tasks to report progress on."

    @pytest.mark.asyncio
    async def test_broadcast_no_tasks_available(self, workflow_manager, mock_comm_system):
        """Test broadcasting when no tasks are available"""
        await workflow_manager._broadcast_no_tasks_available()
        
        # Verify no tasks message was sent
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called

    @pytest.mark.asyncio
    async def test_stop_overnight_workflow(self, workflow_manager, mock_comm_system):
        """Test stopping the overnight workflow"""
        workflow_manager.workflow_active = True
        
        await workflow_manager.stop_overnight_workflow()
        
        # Verify workflow was stopped
        assert workflow_manager.workflow_active is False
        
        # Verify final message was sent
        assert mock_comm_system.send_message_to_all_agents_with_line_breaks.called

    @pytest.mark.asyncio
    async def test_start_overnight_workflow_success(self, workflow_manager):
        """Test successful workflow start"""
        # Mock the workflow cycle to run once then stop
        original_cycle = workflow_manager._execute_workflow_cycle
        workflow_manager._execute_workflow_cycle = AsyncMock()
        workflow_manager.cycle_duration = 0.1  # Very short for testing
        
        # Start workflow
        workflow_manager.workflow_active = True
        result = await workflow_manager.start_overnight_workflow()
        
        # Verify workflow started successfully
        assert result is True
        assert workflow_manager._execute_workflow_cycle.called

    @pytest.mark.asyncio
    async def test_start_overnight_workflow_error(self, workflow_manager):
        """Test workflow start with error handling"""
        # Mock the workflow cycle to raise an exception
        workflow_manager._execute_workflow_cycle = AsyncMock(side_effect=Exception("Test error"))
        workflow_manager.cycle_duration = 0.1  # Very short for testing
        
        # Start workflow
        workflow_manager.workflow_active = True
        result = await workflow_manager.start_overnight_workflow()
        
        # Verify workflow failed gracefully
        assert result is False
        assert workflow_manager.workflow_active is False


@unittest.skipUnless(
    AutonomousDevelopmentEngine and DevelopmentAction and IntelligentPromptGenerator,
    "Autonomous development engine not available",
)
class TestAutonomousDevelopmentEngine(unittest.TestCase):
    """Tests for the AutonomousDevelopmentEngine workflow"""

    def setUp(self):
        """Set up test fixtures"""
        self.pyautogui_patcher = patch("src.core.autonomous_development.pyautogui")
        self.mock_pyautogui = self.pyautogui_patcher.start()

        self.pyperclip_patcher = patch("src.core.autonomous_development.pyperclip")
        self.mock_pyperclip = self.pyperclip_patcher.start()

        self.mock_perpetual_motion = Mock()
        self.mock_cursor_capture = Mock()

        with patch("src.core.autonomous_development.PYAUTOGUI_AVAILABLE", True):
            with patch(
                "src.core.autonomous_development.PerpetualMotionEngine",
                return_value=self.mock_perpetual_motion,
            ):
                with patch(
                    "src.core.autonomous_development.CursorResponseCapture",
                    return_value=self.mock_cursor_capture,
                ):
                    self.engine = AutonomousDevelopmentEngine()

    def tearDown(self):
        """Clean up after tests"""
        self.pyautogui_patcher.stop()
        self.pyperclip_patcher.stop()

    def test_engine_initialization(self):
        """Engine initializes correctly"""
        self.assertIsNotNone(self.engine.prompt_generator)
        self.assertIsInstance(self.engine.prompt_generator, IntelligentPromptGenerator)
        self.assertEqual(len(self.engine.development_actions), 0)
        self.assertEqual(self.engine.autonomous_cycle_count, 0)
        self.assertFalse(self.engine.is_autonomous)

    def test_pyautogui_setup(self):
        """PyAutoGUI configured safely"""
        self.mock_pyautogui.FAILSAFE.assert_called_with(True)
        self.mock_pyautogui.PAUSE.assert_called_with(0.1)
        self.mock_pyautogui.size.assert_called_once()

    def test_autonomous_triggers_setup(self):
        """Autonomous triggers properly configured"""
        self.mock_perpetual_motion.add_trigger.assert_called()
        self.mock_perpetual_motion.register_agent_activation.assert_called()

        expected_calls = [
            call("autonomous_code_review", self.engine.autonomous_code_review),
            call("autonomous_documentation", self.engine.autonomous_documentation),
            call("autonomous_testing", self.engine.autonomous_testing),
            call("autonomous_optimization", self.engine.autonomous_optimization),
        ]
        self.mock_perpetual_motion.register_agent_activation.assert_has_calls(
            expected_calls, any_order=True
        )

    def test_start_autonomous_development(self):
        """Starting autonomous development mode"""
        self.mock_perpetual_motion.start_perpetual_motion.return_value = None
        result = self.engine.start_autonomous_development()

        self.assertTrue(result)
        self.assertTrue(self.engine.is_autonomous)
        self.mock_perpetual_motion.start_perpetual_motion.assert_called_once()
        self.assertTrue(hasattr(self.engine, "autonomous_thread"))
        self.assertTrue(self.engine.autonomous_thread.is_alive())

    def test_stop_autonomous_development(self):
        """Stopping autonomous development mode"""
        self.engine.is_autonomous = True
        self.engine.start_autonomous_development()
        self.engine.stop_autonomous_development()

        self.assertFalse(self.engine.is_autonomous)
        self.mock_perpetual_motion.stop_perpetual_motion.assert_called_once()

    def test_message_improvement_analysis(self):
        """Messages analyzed for improvement opportunities"""
        test_message = {
            "content": "This function needs optimization and better documentation",
            "role": "assistant",
            "thread_id": "test_thread_123",
        }
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        self.engine._execute_autonomous_cycle()

        self.assertGreater(len(self.engine.development_actions), 0)
        for action in self.engine.development_actions:
            self.assertEqual(action.target_element, "cursor_editor")
            self.assertEqual(action.action_type, "code_generation")

    def test_context_extraction(self):
        """Development context properly extracted"""
        test_message = {
            "content": "This Python API endpoint function is too complex and needs refactoring",
            "role": "assistant",
            "thread_id": "test_thread_456",
        }
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        self.engine._execute_autonomous_cycle()

        self.assertGreater(len(self.engine.development_actions), 0)
        action = self.engine.development_actions[0]
        context = action.action_data.get("context")

        self.assertIsNotNone(context)
        self.assertEqual(context["language"], "python")
        self.assertEqual(context["file_type"], "API endpoint")
        self.assertEqual(context["complexity"], "high")

    def test_action_priority_ordering(self):
        """Actions executed in priority order"""
        low_priority = DevelopmentAction(
            action_id="low_priority",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},
            priority=1,
        )
        high_priority = DevelopmentAction(
            action_id="high_priority",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},
            priority=10,
        )
        self.engine.development_actions.append(low_priority)
        self.engine.development_actions.append(high_priority)

        with patch.object(
            self.engine, "_execute_intelligent_code_generation_action"
        ) as mock_execute:
            self.engine._execute_development_actions()
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args[0][0]
            self.assertEqual(call_args.action_id, "high_priority")

    def test_autonomous_agent_activation(self):
        """Autonomous agents activated correctly"""
        test_message = {
            "content": "This code needs security review",
            "role": "assistant",
            "thread_id": "test_thread_789",
        }
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        self.engine._execute_autonomous_cycle()

        self.assertGreater(len(self.engine.development_actions), 0)
        action = self.engine.development_actions[0]
        cursor_agent_prompt = action.action_data.get("cursor_agent_prompt")
        self.assertEqual(cursor_agent_prompt.agent_type, "security_expert")

    def test_conversation_generation(self):
        """New intelligent conversations are generated"""
        self.engine.autonomous_cycle_count = 10
        self.engine.active_conversations = 2

        with patch.object(
            self.engine, "_generate_intelligent_conversation"
        ) as mock_generate:
            self.engine._execute_autonomous_cycle()
            mock_generate.assert_called_once()

    def test_error_handling(self):
        """Errors handled gracefully"""
        malformed_message = {"content": "", "role": "assistant"}
        self.mock_cursor_capture.get_recent_messages.return_value = [malformed_message]

        try:
            self.engine._execute_autonomous_cycle()
            self.assertTrue(True)
        except Exception as e:  # pragma: no cover - safeguard
            self.fail(f"Should handle malformed messages gracefully: {e}")

    def test_performance_metrics(self):
        """Performance metrics tracked correctly"""
        self.engine.start_autonomous_development()

        self.assertTrue(self.engine.is_autonomous)
        stats = self.engine.get_autonomous_stats()
        self.assertIn("autonomous_cycle_count", stats)
        self.assertIn("pending_actions", stats)
        self.assertIn("enhanced_prompts", stats)
        self.assertIn("intelligent_agents", stats)

        self.engine.stop_autonomous_development()


if __name__ == "__main__":
    pytest.main([__file__])
