from datetime import datetime
from typing import Dict, List, Optional, Any

    import argparse
from dataclasses import dataclass
from enum import Enum

#!/usr/bin/env python3
"""
FSM Models - Data models for FSM system

Single Responsibility: Define data structures for FSM system.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""



class StateStatus(Enum):
    """State execution status."""
    
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TransitionType(Enum):
    """Types of state transitions."""
    
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    CONDITIONAL = "conditional"
    TIMEOUT = "timeout"
    ERROR = "error"


class WorkflowPriority(Enum):
    """Workflow priority levels."""
    
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class StateDefinition:
    """State definition structure."""
    
    name: str
    description: str
    entry_actions: List[str]
    exit_actions: List[str]
    timeout_seconds: Optional[float]
    retry_count: int
    retry_delay: float
    required_resources: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]


@dataclass
class TransitionDefinition:
    """Transition definition structure."""
    
    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str]
    priority: int
    timeout_seconds: Optional[float]
    actions: List[str]
    metadata: Dict[str, Any]


@dataclass
class WorkflowInstance:
    """Workflow instance tracking."""
    
    workflow_id: str
    workflow_name: str
    current_state: str
    created_at: datetime
    last_transition: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: StateStatus = StateStatus.PENDING
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


def main():
    """CLI interface for FSM Models testing."""
    
    parser = argparse.ArgumentParser(description="FSM Models - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Models."""
    print("🧪 Running FSM Models smoke tests...")
    
    # Test enum creation
    status = StateStatus.ACTIVE
    assert status == StateStatus.ACTIVE
    print("✅ StateStatus enum test passed")
    
    # Test state definition
    state_def = StateDefinition(
        name="test_state",
        description="Test state",
        entry_actions=["action1"],
        exit_actions=["action2"],
        timeout_seconds=30.0,
        retry_count=3,
        retry_delay=1.0,
        required_resources=["resource1"],
        dependencies=["dep1"],
        metadata={"key": "value"}
    )
    assert state_def.name == "test_state"
    print("✅ StateDefinition test passed")
    
    # Test workflow instance
    now = datetime.now()
    workflow = WorkflowInstance(
        workflow_id="test_workflow",
        workflow_name="Test Workflow",
        current_state="initial",
        created_at=now,
        last_transition=now
    )
    assert workflow.workflow_id == "test_workflow"
    print("✅ WorkflowInstance test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
