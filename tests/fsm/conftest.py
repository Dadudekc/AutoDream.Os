import sys
import types
from pathlib import Path
from datetime import datetime
import pytest
from src.utils.config_core import get_config

# Repository root used for fsm package stubbing
ROOT = Path(__file__).resolve().parents[2]

# Mock the fsm package to avoid importing heavy dependencies in __init__
fsm_pkg = types.ModuleType("src.core.fsm")
fsm_pkg.__path__ = [str(ROOT / "src/core/fsm")]
sys.modules.setdefault("src", types.ModuleType("src"))
sys.modules.setdefault("src.core", types.ModuleType("src.core"))
sys.modules["src.core.fsm"] = fsm_pkg

from src.core.fsm.models import (
    WorkflowInstance,
    StateDefinition,
    TransitionDefinition,
    TransitionType,
    WorkflowPriority,
    StateStatus,
)


@pytest.fixture
def workflow_instance():
    """Factory fixture for creating WorkflowInstance objects."""
    def _factory(workflow_id: str) -> WorkflowInstance:
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

    return _factory


@pytest.fixture
def states_and_transitions():
    """Provide minimal states and transitions for tests."""
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


@pytest.fixture
def state_handler():
    """Provide a basic ConcreteStateHandler used in multiple tests."""
    from src.core.fsm.handlers import ConcreteStateHandler

    return ConcreteStateHandler(
        action=lambda ctx: ctx["actions"].append("processed"),
        check=lambda ctx: ctx["value"] >= 0,
    )
