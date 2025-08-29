from .fsm_core import StateDefinition, TransitionDefinition, TransitionType

START_STATE = StateDefinition(
    name="start",
    description="Starting state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

PROCESS_STATE = StateDefinition(
    name="process",
    description="Processing state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

END_STATE = StateDefinition(
    name="end",
    description="Ending state",
    entry_actions=[],
    exit_actions=[],
    timeout_seconds=None,
    retry_count=0,
    retry_delay=0.0,
    required_resources=[],
    dependencies=[],
    metadata={},
)

DEFAULT_STATES = [START_STATE, PROCESS_STATE, END_STATE]

TRANSITION_START_PROCESS = TransitionDefinition(
    from_state="start",
    to_state="process",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

TRANSITION_PROCESS_END = TransitionDefinition(
    from_state="process",
    to_state="end",
    transition_type=TransitionType.AUTOMATIC,
    condition=None,
    priority=1,
    timeout_seconds=None,
    actions=[],
    metadata={},
)

DEFAULT_TRANSITIONS = [TRANSITION_START_PROCESS, TRANSITION_PROCESS_END]

__all__ = [
    "START_STATE",
    "PROCESS_STATE",
    "END_STATE",
    "DEFAULT_STATES",
    "TRANSITION_START_PROCESS",
    "TRANSITION_PROCESS_END",
    "DEFAULT_TRANSITIONS",
]
