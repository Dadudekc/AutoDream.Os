import time
from datetime import datetime

from src.core.fsm.workflow_executor import WorkflowExecutor
from src.core.fsm.models import (
    StateDefinition,
    TransitionDefinition,
    WorkflowInstance,
    StateStatus,
    TransitionType,
    WorkflowPriority,
    StateExecutionResult,
    StateHandler,
)
from src.core.fsm.types import FSMConfig


class TestStateHandler(StateHandler):
    """Simple state handler used for testing."""

    def __init__(self, status_map):
        self.status_map = status_map

    def execute(self, context):
        status = self.status_map.get(context["workflow_id"], StateStatus.COMPLETED)
        return StateExecutionResult(
            state_name=context["current_state"],
            execution_time=0.0,
            status=status,
            output={},
            error_message=None,
            metadata={},
            timestamp=datetime.now(),
        )

    def can_transition(self, context):
        return True


def _build_workflow(workflow_id):
    return WorkflowInstance(
        workflow_id=workflow_id,
        workflow_name=workflow_id,
        current_state="start",
        state_history=[],
        start_time=datetime.now(),
        last_update=datetime.now(),
        status=StateStatus.PENDING,
        priority=WorkflowPriority.NORMAL,
        metadata={},
        error_count=0,
        retry_count=0,
    )


def _build_states_and_transitions():
    states = {
        "start": StateDefinition(
            name="start",
            description="start",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0,
            required_resources=[],
            dependencies=[],
            metadata={},
        ),
        "end": StateDefinition(
            name="end",
            description="end",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0,
            required_resources=[],
            dependencies=[],
            metadata={},
        ),
    }
    transitions = {
        "start": [
            TransitionDefinition(
                from_state="start",
                to_state="end",
                transition_type=TransitionType.AUTOMATIC,
                condition=None,
                priority=1,
                timeout_seconds=None,
                actions=[],
                metadata={},
            )
        ]
    }
    return states, transitions


def test_workflow_queue_processing():
    config = FSMConfig(max_concurrent_workflows=1)
    executor = WorkflowExecutor(config)

    states, transitions = _build_states_and_transitions()
    handler = TestStateHandler(
        {"wf1": StateStatus.ACTIVE, "wf2": StateStatus.COMPLETED}
    )
    state_handlers = {"start": handler}

    wf1 = _build_workflow("wf1")
    wf2 = _build_workflow("wf2")

    assert executor.start_workflow("wf1", wf1, states, transitions, state_handlers)
    assert not executor.start_workflow("wf2", wf2, states, transitions, state_handlers)

    # Complete first workflow to free capacity
    executor._handle_state_completion("wf1", wf1, "start", None, states, transitions)

    executor._process_workflow_queue()

    assert wf2.status == StateStatus.COMPLETED
    assert "wf2" not in executor.active_workflows
    assert len(executor.workflow_queue) == 0


def test_start_workflow_requires_pending_state():
    config = FSMConfig()
    executor = WorkflowExecutor(config)

    wf = _build_workflow("wf")
    wf.status = StateStatus.ACTIVE  # not pending

    states, transitions = _build_states_and_transitions()
    state_handlers = {"start": TestStateHandler({})}

    assert not executor.start_workflow("wf", wf, states, transitions, state_handlers)
    assert "wf" not in executor.active_workflows
