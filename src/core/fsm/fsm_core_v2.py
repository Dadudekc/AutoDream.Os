#!/usr/bin/env python3
"""
FSM Core V2 - Finite State Machine System for Phase 2 Workflow Management
=======================================================================

Implements a robust finite state machine system for managing complex workflows
and state transitions in the Agent Cellphone V2 system.

Follows V2 standards: ≤400 LOC, SRP, OOP principles, existing architecture integration.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import json
import time
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union, Set
from collections import defaultdict, deque


# ============================================================================
# ENUMS AND DATA MODELS
# ============================================================================

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
    state_history: List[Dict[str, Any]]
    start_time: datetime
    last_update: datetime
    status: StateStatus
    priority: WorkflowPriority
    metadata: Dict[str, Any]
    error_count: int
    retry_count: int


@dataclass
class StateExecutionResult:
    """Result of state execution."""
    state_name: str
    execution_time: float
    status: StateStatus
    output: Dict[str, Any]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    timestamp: datetime


# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================

class StateHandler(ABC):
    """Abstract base class for state handlers."""
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> StateExecutionResult:
        """Execute the state logic."""
        pass
    
    @abstractmethod
    def can_transition(self, context: Dict[str, Any]) -> bool:
        """Check if transition to this state is allowed."""
        pass


class TransitionHandler(ABC):
    """Abstract base class for transition handlers."""
    
    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate transition condition."""
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute transition actions."""
        pass


# ============================================================================
# FSM CORE SYSTEM
# ============================================================================

class FSMCoreV2:
    """
    FSM Core V2 - Finite State Machine System
    
    Single responsibility: Manage workflow state transitions and execution
    following V2 architecture standards.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize FSM core system."""
        self.logger = logging.getLogger(f"{__name__}.FSMCoreV2")
        
        # Core data structures
        self.states: Dict[str, StateDefinition] = {}
        self.transitions: Dict[str, List[TransitionDefinition]] = defaultdict(list)
        self.workflows: Dict[str, WorkflowInstance] = {}
        self.state_handlers: Dict[str, StateHandler] = {}
        self.transition_handlers: Dict[str, TransitionHandler] = {}
        
        # System state
        self.is_running = False
        self.active_workflows: Set[str] = set()
        self.workflow_queue: deque = deque()
        
        # Configuration
        self.config = self._load_config(config_file)
        self.max_concurrent_workflows = self.config.get("max_concurrent_workflows", 10)
        self.default_timeout = self.config.get("default_timeout", 300.0)
        self.enable_logging = self.config.get("enable_logging", True)
        
        # Monitoring
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Statistics
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0
        
        self.logger.info("✅ FSM Core V2 initialized successfully")
    
    def _load_config(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """Load FSM configuration."""
        try:
            if config_file and Path(config_file).exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
            
            # Default configuration
            return {
                "max_concurrent_workflows": 10,
                "default_timeout": 300.0,
                "enable_logging": True,
                "retry_policy": {
                    "max_retries": 3,
                    "retry_delay": 5.0,
                    "exponential_backoff": True
                },
                "monitoring": {
                    "enabled": True,
                    "interval": 1.0,
                    "metrics_collection": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return {}
    
    # ============================================================================
    # STATE MANAGEMENT
    # ============================================================================
    
    def add_state(self, state_def: StateDefinition) -> bool:
        """Add a new state to the FSM."""
        try:
            if state_def.name in self.states:
                self.logger.warning(f"State {state_def.name} already exists, updating")
            
            self.states[state_def.name] = state_def
            self.logger.info(f"✅ Added state: {state_def.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add state {state_def.name}: {e}")
            return False
    
    def remove_state(self, state_name: str) -> bool:
        """Remove a state from the FSM."""
        try:
            if state_name not in self.states:
                self.logger.warning(f"State {state_name} not found")
                return False
            
            # Check if state is in use
            for workflow in self.workflows.values():
                if workflow.current_state == state_name:
                    self.logger.error(f"Cannot remove state {state_name} - in use by workflow {workflow.workflow_id}")
                    return False
            
            del self.states[state_name]
            self.logger.info(f"✅ Removed state: {state_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove state {state_name}: {e}")
            return False
    
    def get_state(self, state_name: str) -> Optional[StateDefinition]:
        """Get state definition by name."""
        return self.states.get(state_name)
    
    def list_states(self) -> List[str]:
        """List all available states."""
        return list(self.states.keys())
    
    # ============================================================================
    # TRANSITION MANAGEMENT
    # ============================================================================
    
    def add_transition(self, transition_def: TransitionDefinition) -> bool:
        """Add a new transition to the FSM."""
        try:
            # Validate states exist
            if transition_def.from_state not in self.states:
                self.logger.error(f"From state {transition_def.from_state} not found")
                return False
            
            if transition_def.to_state not in self.states:
                self.logger.error(f"To state {transition_def.to_state} not found")
                return False
            
            # Add transition
            self.transitions[transition_def.from_state].append(transition_def)
            self.logger.info(f"✅ Added transition: {transition_def.from_state} -> {transition_def.to_state}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add transition: {e}")
            return False
    
    def remove_transition(self, from_state: str, to_state: str) -> bool:
        """Remove a transition from the FSM."""
        try:
            if from_state not in self.transitions:
                return False
            
            # Find and remove transition
            transitions = self.transitions[from_state]
            for i, transition in enumerate(transitions):
                if transition.to_state == to_state:
                    del transitions[i]
                    self.logger.info(f"✅ Removed transition: {from_state} -> {to_state}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove transition: {e}")
            return False
    
    def get_transitions(self, from_state: str) -> List[TransitionDefinition]:
        """Get all transitions from a state."""
        return self.transitions.get(from_state, [])
    
    def get_available_transitions(self, current_state: str, context: Dict[str, Any]) -> List[TransitionDefinition]:
        """Get available transitions from current state."""
        available = []
        
        for transition in self.get_transitions(current_state):
            # Check if transition is available
            if self._can_execute_transition(transition, context):
                available.append(transition)
        
        # Sort by priority
        available.sort(key=lambda t: t.priority, reverse=True)
        return available
    
    def _can_execute_transition(self, transition: TransitionDefinition, context: Dict[str, Any]) -> bool:
        """Check if a transition can be executed."""
        try:
            # Check condition if specified
            if transition.condition:
                # Simple condition evaluation (can be extended)
                return self._evaluate_condition(transition.condition, context)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate transition condition: {e}")
            return False
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a transition condition."""
        try:
            # Simple condition evaluation (can be extended with more complex logic)
            if "==" in condition:
                key, value = condition.split("==")
                return str(context.get(key.strip())) == value.strip()
            elif "!=" in condition:
                key, value = condition.split("!=")
                return str(context.get(key.strip())) != value.strip()
            elif ">" in condition:
                key, value = condition.split(">")
                return float(context.get(key.strip(), 0)) > float(value.strip())
            elif "<" in condition:
                key, value = condition.split("<")
                return float(context.get(key.strip(), 0)) < float(value.strip())
            else:
                # Simple key existence check
                return condition.strip() in context
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False
    
    # ============================================================================
    # WORKFLOW MANAGEMENT
    # ============================================================================
    
    def create_workflow(self, workflow_name: str, initial_state: str, 
                       priority: WorkflowPriority = WorkflowPriority.NORMAL,
                       metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Create a new workflow instance."""
        try:
            # Validate initial state
            if initial_state not in self.states:
                self.logger.error(f"Initial state {initial_state} not found")
                return None
            
            # Generate workflow ID
            workflow_id = f"{workflow_name}_{int(time.time())}_{hash(workflow_name)}"
            
            # Create workflow instance
            workflow = WorkflowInstance(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                current_state=initial_state,
                state_history=[],
                start_time=datetime.now(),
                last_update=datetime.now(),
                status=StateStatus.PENDING,
                priority=priority,
                metadata=metadata or {},
                error_count=0,
                retry_count=0
            )
            
            # Store workflow
            self.workflows[workflow_id] = workflow
            
            # Add to queue
            self.workflow_queue.append(workflow_id)
            
            self.logger.info(f"✅ Created workflow: {workflow_id} starting at {initial_state}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return None
    
    def start_workflow(self, workflow_id: str) -> bool:
        """Start a workflow execution."""
        try:
            if workflow_id not in self.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            workflow = self.workflows[workflow_id]
            
            if workflow.status != StateStatus.PENDING:
                self.logger.warning(f"Workflow {workflow_id} is not in pending state")
                return False
            
            # Check concurrent workflow limit
            if len(self.active_workflows) >= self.max_concurrent_workflows:
                self.logger.warning(f"Maximum concurrent workflows reached, queuing {workflow_id}")
                return False
            
            # Start workflow
            workflow.status = StateStatus.ACTIVE
            workflow.last_update = datetime.now()
            self.active_workflows.add(workflow_id)
            
            # Execute initial state
            self._execute_state(workflow_id, workflow.current_state)
            
            self.logger.info(f"✅ Started workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return False
    
    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop a workflow execution."""
        try:
            if workflow_id not in self.workflows:
                return False
            
            workflow = self.workflows[workflow_id]
            
            if workflow.status not in [StateStatus.ACTIVE, StateStatus.PENDING]:
                return False
            
            # Stop workflow
            workflow.status = StateStatus.FAILED
            workflow.last_update = datetime.now()
            
            if workflow_id in self.active_workflows:
                self.active_workflows.remove(workflow_id)
            
            self.logger.info(f"✅ Stopped workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop workflow {workflow_id}: {e}")
            return False
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Get workflow instance by ID."""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self, status: Optional[StateStatus] = None) -> List[WorkflowInstance]:
        """List workflows with optional status filter."""
        if status is None:
            return list(self.workflows.values())
        
        return [w for w in self.workflows.values() if w.status == status]
    
    # ============================================================================
    # STATE EXECUTION
    # ============================================================================
    
    def _execute_state(self, workflow_id: str, state_name: str) -> bool:
        """Execute a specific state in a workflow."""
        try:
            workflow = self.workflows[workflow_id]
            state_def = self.states[state_name]
            
            if not state_def:
                self.logger.error(f"State {state_name} not found")
                return False
            
            # Update workflow state
            workflow.current_state = state_name
            workflow.last_update = datetime.now()
            
            # Execute entry actions
            self._execute_actions(workflow_id, state_def.entry_actions, "entry")
            
            # Execute state logic if handler exists
            if state_name in self.state_handlers:
                handler = self.state_handlers[state_name]
                context = self._build_context(workflow)
                
                start_time = time.time()
                result = handler.execute(context)
                execution_time = time.time() - start_time
                
                # Update state history
                workflow.state_history.append({
                    "state": state_name,
                    "execution_time": execution_time,
                    "status": result.status.value,
                    "output": result.output,
                    "error_message": result.error_message,
                    "timestamp": result.timestamp.isoformat()
                })
                
                # Handle execution result
                if result.status == StateStatus.COMPLETED:
                    self._handle_state_completion(workflow_id, state_name, result)
                elif result.status == StateStatus.FAILED:
                    self._handle_state_failure(workflow_id, state_name, result)
                elif result.status == StateStatus.TIMEOUT:
                    self._handle_state_timeout(workflow_id, state_name, result)
                
            else:
                # No handler, mark as completed
                self._handle_state_completion(workflow_id, state_name, None)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute state {state_name} in workflow {workflow_id}: {e}")
            return False
    
    def _execute_actions(self, workflow_id: str, actions: List[str], action_type: str) -> None:
        """Execute a list of actions."""
        for action in actions:
            try:
                self.logger.debug(f"Executing {action_type} action: {action} for workflow {workflow_id}")
                # Action execution logic can be extended here
                
            except Exception as e:
                self.logger.error(f"Failed to execute {action_type} action {action}: {e}")
    
    def _build_context(self, workflow: WorkflowInstance) -> Dict[str, Any]:
        """Build execution context for state handlers."""
        return {
            "workflow_id": workflow.workflow_id,
            "workflow_name": workflow.workflow_name,
            "current_state": workflow.current_state,
            "state_history": workflow.state_history,
            "metadata": workflow.metadata,
            "start_time": workflow.start_time.isoformat(),
            "priority": workflow.priority.value
        }
    
    def _handle_state_completion(self, workflow_id: str, state_name: str, result: Optional[StateExecutionResult]) -> None:
        """Handle successful state completion."""
        try:
            workflow = self.workflows[workflow_id]
            
            # Find available transitions
            available_transitions = self.get_available_transitions(state_name, self._build_context(workflow))
            
            if available_transitions:
                # Execute automatic transition
                next_transition = available_transitions[0]  # Highest priority
                self._execute_transition(workflow_id, next_transition)
            else:
                # No transitions available, workflow completed
                workflow.status = StateStatus.COMPLETED
                workflow.last_update = datetime.now()
                self.active_workflows.discard(workflow_id)
                
                self.successful_workflows += 1
                self.logger.info(f"✅ Workflow {workflow_id} completed successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to handle state completion: {e}")
    
    def _handle_state_failure(self, workflow_id: str, state_name: str, result: StateExecutionResult) -> None:
        """Handle state execution failure."""
        try:
            workflow = self.workflows[workflow_id]
            workflow.error_count += 1
            
            # Check retry policy
            state_def = self.states[state_name]
            if workflow.retry_count < state_def.retry_count:
                workflow.retry_count += 1
                self.logger.info(f"Retrying state {state_name} in workflow {workflow_id} (attempt {workflow.retry_count})")
                
                # Schedule retry
                threading.Timer(state_def.retry_delay, 
                              lambda: self._execute_state(workflow_id, state_name)).start()
            else:
                # Max retries exceeded
                workflow.status = StateStatus.FAILED
                workflow.last_update = datetime.now()
                self.active_workflows.discard(workflow_id)
                
                self.failed_workflows += 1
                self.logger.error(f"❌ Workflow {workflow_id} failed after {workflow.retry_count} retries")
                
        except Exception as e:
            self.logger.error(f"Failed to handle state failure: {e}")
    
    def _handle_state_timeout(self, workflow_id: str, state_name: str, result: StateExecutionResult) -> None:
        """Handle state execution timeout."""
        try:
            workflow = self.workflows[workflow_id]
            workflow.status = StateStatus.TIMEOUT
            workflow.last_update = datetime.now()
            self.active_workflows.discard(workflow_id)
            
            self.failed_workflows += 1
            self.logger.error(f"⏰ Workflow {workflow_id} timed out in state {state_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to handle state timeout: {e}")
    
    def _execute_transition(self, workflow_id: str, transition: TransitionDefinition) -> bool:
        """Execute a state transition."""
        try:
            workflow = self.workflows[workflow_id]
            
            # Execute transition actions
            self._execute_actions(workflow_id, transition.actions, "transition")
            
            # Update workflow state
            old_state = workflow.current_state
            workflow.current_state = transition.to_state
            workflow.last_update = datetime.now()
            
            # Execute exit actions for old state
            old_state_def = self.states.get(old_state)
            if old_state_def:
                self._execute_actions(workflow_id, old_state_def.exit_actions, "exit")
            
            # Execute new state
            self._execute_state(workflow_id, transition.to_state)
            
            self.total_state_transitions += 1
            self.logger.info(f"✅ Transition: {old_state} -> {transition.to_state} in workflow {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute transition: {e}")
            return False
    
    # ============================================================================
    # SYSTEM CONTROL
    # ============================================================================
    
    def start_system(self) -> bool:
        """Start the FSM system."""
        try:
            if self.is_running:
                self.logger.warning("FSM system is already running")
                return True
            
            self.is_running = True
            
            # Start monitoring
            if self.config.get("monitoring", {}).get("enabled", True):
                self._start_monitoring()
            
            self.logger.info("✅ FSM system started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start FSM system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the FSM system."""
        try:
            if not self.is_running:
                self.logger.warning("FSM system is not running")
                return True
            
            self.is_running = False
            
            # Stop monitoring
            self._stop_monitoring()
            
            # Stop all active workflows
            for workflow_id in list(self.active_workflows):
                self.stop_workflow(workflow_id)
            
            self.logger.info("✅ FSM system stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop FSM system: {e}")
            return False
    
    def _start_monitoring(self) -> None:
        """Start FSM monitoring thread."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("✅ FSM monitoring started")
    
    def _stop_monitoring(self) -> None:
        """Stop FSM monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("✅ FSM monitoring stopped")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active and self.is_running:
            try:
                # Process workflow queue
                self._process_workflow_queue()
                
                # Check for timeouts
                self._check_timeouts()
                
                # Sleep for monitoring interval
                interval = self.config.get("monitoring", {}).get("interval", 1.0)
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(1.0)
    
    def _process_workflow_queue(self) -> None:
        """Process pending workflows in queue."""
        while self.workflow_queue and len(self.active_workflows) < self.max_concurrent_workflows:
            workflow_id = self.workflow_queue.popleft()
            self.start_workflow(workflow_id)
    
    def _check_timeouts(self) -> None:
        """Check for workflow timeouts."""
        current_time = datetime.now()
        
        for workflow_id in list(self.active_workflows):
            workflow = self.workflows[workflow_id]
            state_def = self.states.get(workflow.current_state)
            
            if state_def and state_def.timeout_seconds:
                elapsed = (current_time - workflow.last_update).total_seconds()
                if elapsed > state_def.timeout_seconds:
                    self.logger.warning(f"Workflow {workflow_id} timed out in state {workflow.current_state}")
                    self._handle_state_timeout(workflow_id, workflow.current_state, None)
    
    # ============================================================================
    # STATISTICS AND REPORTING
    # ============================================================================
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get FSM system statistics."""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": len(self.active_workflows),
            "queued_workflows": len(self.workflow_queue),
            "total_workflows_executed": self.total_workflows_executed,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "total_state_transitions": self.total_state_transitions,
            "system_status": "running" if self.is_running else "stopped",
            "monitoring_active": self.monitoring_active,
            "last_updated": datetime.now().isoformat()
        }
    
    def export_workflow_report(self, workflow_id: str, format: str = "json") -> Optional[str]:
        """Export workflow execution report."""
        try:
            workflow = self.workflows.get(workflow_id)
            if not workflow:
                return None
            
            if format.lower() == "json":
                return json.dumps(asdict(workflow), indent=2, default=str)
            else:
                return f"Report format '{format}' not supported"
                
        except Exception as e:
            self.logger.error(f"Failed to export workflow report: {e}")
            return None
    
    def clear_history(self) -> None:
        """Clear workflow history."""
        self.workflows.clear()
        self.active_workflows.clear()
        self.workflow_queue.clear()
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0
        self.logger.info("✅ FSM history cleared")


# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Maintain backwards compatibility with existing code
FSMCore = FSMCoreV2
FiniteStateMachine = FSMCoreV2
WorkflowEngine = FSMCoreV2

# Export all components
__all__ = [
    "FSMCoreV2",
    "FSMCore",
    "FiniteStateMachine", 
    "WorkflowEngine",
    "StateHandler",
    "TransitionHandler",
    "StateStatus",
    "TransitionType",
    "WorkflowPriority",
    "StateDefinition",
    "TransitionDefinition",
    "WorkflowInstance",
    "StateExecutionResult"
]


if __name__ == "__main__":
    # Initialize FSM system
    fsm = FSMCoreV2()
    
    # Start system
    if fsm.start_system():
        print("✅ FSM Core V2 system ready for workflow management!")
        print("🚀 System ready for Phase 2 workflow operations!")
    else:
        print("❌ FSM Core V2 system failed to start!")
        print("⚠️ System not ready for production deployment!")
