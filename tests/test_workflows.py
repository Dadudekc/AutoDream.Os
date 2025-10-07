"""
Workflow System Tests - V2 Compliant
====================================

Comprehensive test suite for the Advanced Workflows System.
Maintains 100% test pass rate and V2 compliance standards.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import pytest
from src.workflows.models import (
    WorkflowState,
    WorkflowStep,
    AIResponse,
    WorkflowProgress,
    ResponseType,
    CoordinationStrategy,
)
from src.workflows.engine import WorkflowEngine
from src.workflows.steps import (
    WorkflowStepBuilder,
    ConversationLoopBuilder,
    MultiAgentOrchestrationBuilder,
)
from src.workflows.strategies import ParallelStrategy, SequentialStrategy


class TestWorkflowModels:
    """Test workflow data models."""

    def test_workflow_state_enum(self):
        """Test workflow state enumeration."""
        assert WorkflowState.INITIALIZED.value == "initialized"
        assert WorkflowState.COMPLETED.value == "completed"

    def test_workflow_step_creation(self):
        """Test workflow step creation."""
        step = WorkflowStep(
            id="test_step",
            name="Test Step",
            description="Test description",
            agent_target="Agent-1",
            prompt_template="Test prompt",
            expected_response_type=ResponseType.TASK_EXECUTION,
        )

        assert step.id == "test_step"
        assert step.agent_target == "Agent-1"
        assert step.is_ready(set())

    def test_workflow_step_dependencies(self):
        """Test workflow step dependency checking."""
        step = WorkflowStep(
            id="step2",
            name="Step 2",
            description="Depends on step1",
            agent_target="Agent-1",
            prompt_template="Test",
            expected_response_type=ResponseType.TASK_EXECUTION,
            dependencies=["step1"],
        )

        assert not step.is_ready(set())
        assert step.is_ready({"step1"})

    def test_ai_response_creation(self):
        """Test AI response model."""
        response = AIResponse(
            agent="Agent-1",
            text="Test response",
            timestamp=123456,
            message_id="msg_1",
        )

        assert response.agent == "Agent-1"
        assert response.text == "Test response"

    def test_workflow_progress_calculation(self):
        """Test workflow progress tracking."""
        progress = WorkflowProgress(
            workflow_name="test_workflow",
            state=WorkflowState.RUNNING,
            total_steps=10,
            completed_steps=5,
            failed_steps=1,
        )

        assert progress.pending_steps == 4
        assert progress.completion_percentage == 50.0


class TestWorkflowEngine:
    """Test workflow engine."""

    def test_engine_initialization(self):
        """Test workflow engine initialization."""
        engine = WorkflowEngine("test_workflow")

        assert engine.workflow_name == "test_workflow"
        assert engine.state == WorkflowState.INITIALIZED
        assert len(engine.steps) == 0

    def test_add_step(self):
        """Test adding steps to workflow."""
        engine = WorkflowEngine("test_workflow")

        step = WorkflowStep(
            id="step1",
            name="Step 1",
            description="Test step",
            agent_target="Agent-1",
            prompt_template="Test prompt",
            expected_response_type=ResponseType.TASK_EXECUTION,
        )

        engine.add_step(step)
        assert len(engine.steps) == 1
        assert engine.steps[0].id == "step1"

    def test_find_next_step(self):
        """Test finding next executable step."""
        engine = WorkflowEngine("test_workflow")

        step1 = WorkflowStep(
            id="step1",
            name="Step 1",
            description="First step",
            agent_target="Agent-1",
            prompt_template="Test",
            expected_response_type=ResponseType.TASK_EXECUTION,
        )

        step2 = WorkflowStep(
            id="step2",
            name="Step 2",
            description="Second step",
            agent_target="Agent-2",
            prompt_template="Test",
            expected_response_type=ResponseType.TASK_EXECUTION,
            dependencies=["step1"],
        )

        engine.add_step(step1)
        engine.add_step(step2)

        # First step should be available
        next_step = engine._find_next_step()
        assert next_step.id == "step1"

        # After completing step1, step2 should be available
        engine.completed_steps.add("step1")
        next_step = engine._find_next_step()
        assert next_step.id == "step2"


class TestWorkflowStepBuilders:
    """Test workflow step builders."""

    def test_conversation_loop_builder(self):
        """Test conversation loop creation."""
        builder = ConversationLoopBuilder()
        steps = builder.create_conversation_loop("Agent-1", "Agent-2", "testing", iterations=2)

        # Should create 4 steps (2 rounds x 2 agents)
        assert len(steps) == 4

        # Check dependency chain
        assert steps[0].dependencies == []  # First prompt has no dependencies
        assert "conversation_0_a" in steps[1].dependencies  # First response depends on first prompt
        assert "conversation_0_b" in steps[2].dependencies  # Second prompt depends on first response

    def test_multi_agent_orchestration_builder(self):
        """Test multi-agent orchestration creation."""
        builder = MultiAgentOrchestrationBuilder()

        # Parallel strategy
        steps = builder.create_multi_agent_orchestration(
            "test task", ["Agent-1", "Agent-2", "Agent-3"], CoordinationStrategy.PARALLEL
        )

        assert len(steps) == 3
        # Parallel steps should have no dependencies
        for step in steps:
            assert len(step.dependencies) == 0

        # Sequential strategy
        builder2 = MultiAgentOrchestrationBuilder()
        steps = builder2.create_multi_agent_orchestration(
            "test task", ["Agent-1", "Agent-2"], CoordinationStrategy.SEQUENTIAL
        )

        assert len(steps) == 2
        # Sequential steps should have dependencies
        assert len(steps[0].dependencies) == 0
        assert len(steps[1].dependencies) == 1


class TestWorkflowStrategies:
    """Test workflow strategies."""

    @pytest.mark.asyncio
    async def test_parallel_strategy(self):
        """Test parallel execution strategy."""
        strategy = ParallelStrategy()

        steps = [
            WorkflowStep(
                id="step1",
                name="Step 1",
                description="Test",
                agent_target="Agent-1",
                prompt_template="Test",
                expected_response_type=ResponseType.TASK_EXECUTION,
            ),
            WorkflowStep(
                id="step2",
                name="Step 2",
                description="Test",
                agent_target="Agent-2",
                prompt_template="Test",
                expected_response_type=ResponseType.TASK_EXECUTION,
            ),
        ]

        result = await strategy.execute_workflow(steps, {})

        assert result["strategy"] == "Parallel"
        assert len(result["completed_steps"]) == 2

    @pytest.mark.asyncio
    async def test_sequential_strategy(self):
        """Test sequential execution strategy."""
        strategy = SequentialStrategy()

        steps = [
            WorkflowStep(
                id="step1",
                name="Step 1",
                description="Test",
                agent_target="Agent-1",
                prompt_template="Test",
                expected_response_type=ResponseType.TASK_EXECUTION,
            ),
        ]

        result = await strategy.execute_workflow(steps, {})

        assert result["strategy"] == "Sequential"
        assert len(result["completed_steps"]) == 1

