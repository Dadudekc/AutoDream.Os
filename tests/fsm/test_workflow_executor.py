from datetime import datetime

from src.core.fsm.workflow_executor import WorkflowExecutor
from src.core.fsm.models import StateStatus, StateExecutionResult, StateHandler
from src.core.fsm.types import FSMConfig


class SampleStateHandler(StateHandler):
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


def test_workflow_queue_processing(workflow_instance, states_and_transitions):
    config = FSMConfig(max_concurrent_workflows=1)
    executor = WorkflowExecutor(config)

    states, transitions = states_and_transitions
    handler = SampleStateHandler({"wf1": StateStatus.ACTIVE, "wf2": StateStatus.COMPLETED})
    state_handlers = {"start": handler}

    wf1 = workflow_instance("wf1")
    wf2 = workflow_instance("wf2")

    assert executor.start_workflow("wf1", wf1, states, transitions, state_handlers)
    assert not executor.start_workflow("wf2", wf2, states, transitions, state_handlers)

    wf1.status = StateStatus.COMPLETED
    executor.active_workflows.discard("wf1")
    executor._process_workflow_queue()

    assert wf2.status == StateStatus.ACTIVE
    assert "wf2" in executor.active_workflows
    assert len(executor.workflow_queue) == 0


def test_start_workflow_requires_pending_state(workflow_instance, states_and_transitions):
    config = FSMConfig()
    executor = WorkflowExecutor(config)

    wf = workflow_instance("wf")
    wf.status = StateStatus.ACTIVE  # not pending

    states, transitions = states_and_transitions
    state_handlers = {"start": SampleStateHandler({})}

    assert not executor.start_workflow("wf", wf, states, transitions, state_handlers)
    assert "wf" not in executor.active_workflows
