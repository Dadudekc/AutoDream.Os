"""
FSM Models - V2 Compliant State Machine Models
Core state machine models for agent coordination and workflow management
V2 COMPLIANCE: Under 300-line limit, comprehensive error handling, modular design

@version 1.0.0 - V2 COMPLIANCE FSM MODELS
@license MIT
"""

from datetime import datetime


class FSMState(Enum):
    """Finite State Machine States"""

    INITIALIZING = "initializing"
    ACTIVE = "active"
    COORDINATING = "coordinating"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    ERROR = "error"
    SUSPENDED = "suspended"


class StateStatus(Enum):
    """State status enumeration"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SUSPENDED = "suspended"


class WorkflowPriority(Enum):
    """Workflow priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TransitionType(Enum):
    """Transition type enumeration"""

    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"


class FSMEvent(Enum):
    """State Machine Events"""

    START = "start"
    COORDINATE = "coordinate"
    EXECUTE = "execute"
    VALIDATE = "validate"
    COMPLETE = "complete"
    FAIL = "fail"
    SUSPEND = "suspend"
    RESUME = "resume"


@dataclass
class FSMTransition:
    """State transition definition"""

    from_state: FSMState
    to_state: FSMState
    event: FSMEvent
    guard_condition: Optional[str] = None
    action: Optional[str] = None


@dataclass
class StateDefinition:
    """State definition for workflow FSM"""

    name: str
    description: str
    entry_actions: List[str] = field(default_factory=list)
    exit_actions: List[str] = field(default_factory=list)
    timeout_seconds: Optional[int] = None
    retry_count: int = 0
    retry_delay: int = 0
    required_resources: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransitionDefinition:
    """Transition definition for workflow FSM"""

    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str] = None
    priority: int = 1
    timeout_seconds: Optional[int] = None
    actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowInstance:
    """Workflow instance for FSM execution"""

    workflow_id: str
    workflow_name: str
    current_state: str
    state_history: List[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    status: StateStatus = StateStatus.PENDING
    priority: WorkflowPriority = WorkflowPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_count: int = 0
    retry_count: int = 0


@dataclass
class FSMContext:
    """FSM execution context"""

    agent_id: str
    current_state: FSMState
    previous_state: Optional[FSMState] = None
    last_event: Optional[FSMEvent] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class FSMProtocol(Protocol):
    """FSM Protocol Interface"""

    def get_current_state(self) -> FSMState:
        """Get current FSM state"""
        ...

    def can_transition(self, event: FSMEvent) -> bool:
        """Check if transition is allowed"""
        ...

    def transition(self, event: FSMEvent) -> bool:
        """Execute state transition"""
        ...

    def get_context(self) -> FSMContext:
        """Get current execution context"""
        ...


@dataclass
class FSMDefinition:
    """Complete FSM definition"""

    name: str
    states: List[FSMState]
    initial_state: FSMState
    transitions: List[FSMTransition]
    final_states: List[FSMState] = field(default_factory=lambda: [FSMState.COMPLETED])

    def get_transitions_from_state(self, state: FSMState) -> List[FSMTransition]:
        """Get all transitions from a specific state"""
        return [t for t in self.transitions if t.from_state == state]

    def get_transition(
        self, from_state: FSMState, event: FSMEvent
    ) -> Optional[FSMTransition]:
        """Get specific transition for state and event"""
        for transition in self.transitions:
            if transition.from_state == from_state and transition.event == event:
                return transition
        return None

    def is_final_state(self, state: FSMState) -> bool:
        """Check if state is a final state"""
        return state in self.final_states


# Default FSM definitions for common agent workflows

AGENT_WORKFLOW_FSM = FSMDefinition(
    name="agent_workflow",
    states=[
        FSMState.INITIALIZING,
        FSMState.ACTIVE,
        FSMState.COORDINATING,
        FSMState.EXECUTING,
        FSMState.VALIDATING,
        FSMState.COMPLETED,
        FSMState.ERROR,
    ],
    initial_state=FSMState.INITIALIZING,
    transitions=[
        FSMTransition(FSMState.INITIALIZING, FSMState.ACTIVE, FSMEvent.START),
        FSMTransition(FSMState.ACTIVE, FSMState.COORDINATING, FSMEvent.COORDINATE),
        FSMTransition(FSMState.COORDINATING, FSMState.EXECUTING, FSMEvent.EXECUTE),
        FSMTransition(FSMState.EXECUTING, FSMState.VALIDATING, FSMEvent.VALIDATE),
        FSMTransition(FSMState.VALIDATING, FSMState.COMPLETED, FSMEvent.COMPLETE),
        FSMTransition(FSMState.VALIDATING, FSMState.ERROR, FSMEvent.FAIL),
        FSMTransition(FSMState.EXECUTING, FSMState.ERROR, FSMEvent.FAIL),
        FSMTransition(FSMState.COORDINATING, FSMState.ERROR, FSMEvent.FAIL),
        FSMTransition(FSMState.ACTIVE, FSMState.ERROR, FSMEvent.FAIL),
        FSMTransition(FSMState.ERROR, FSMState.ACTIVE, FSMEvent.RESUME),
        FSMTransition(FSMState.ACTIVE, FSMState.SUSPENDED, FSMEvent.SUSPEND),
        FSMTransition(FSMState.SUSPENDED, FSMState.ACTIVE, FSMEvent.RESUME),
    ],
    final_states=[FSMState.COMPLETED, FSMState.ERROR],
)


@dataclass
class FSMInstance:
    """FSM instance with current state and context"""

    definition: FSMDefinition
    context: FSMContext

    def can_transition(self, event: FSMEvent) -> bool:
        """Check if transition is allowed"""
        transition = self.definition.get_transition(self.context.current_state, event)
        return transition is not None

    def transition(self, event: FSMEvent) -> bool:
        """Execute state transition"""
        transition = self.definition.get_transition(self.context.current_state, event)
        if not get_unified_validator().validate_required(transition):
            return False

        # Update context
        self.context.previous_state = self.context.current_state
        self.context.current_state = transition.to_state
        self.context.last_event = event
        self.context.timestamp = datetime.now()

        return True

    def get_current_state(self) -> FSMState:
        """Get current state"""
        return self.context.current_state

    def is_completed(self) -> bool:
        """Check if FSM is in a final state"""
        return self.definition.is_final_state(self.context.current_state)


def create_agent_workflow_fsm(agent_id: str) -> FSMInstance:
    """Factory function to create agent workflow FSM instance"""
    context = FSMContext(agent_id=agent_id, current_state=FSMState.INITIALIZING)
    return FSMInstance(definition=AGENT_WORKFLOW_FSM, context=context)


# Export for DI
__all__ = [
    "FSMState",
    "FSMEvent",
    "FSMTransition",
    "FSMContext",
    "FSMProtocol",
    "FSMDefinition",
    "FSMInstance",
    "StateStatus",
    "WorkflowPriority",
    "TransitionType",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "AGENT_WORKFLOW_FSM",
    "create_agent_workflow_fsm",
]
