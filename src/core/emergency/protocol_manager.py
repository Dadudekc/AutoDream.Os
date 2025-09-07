#!/usr/bin/env python3
"""
Emergency Protocol Manager - Component of Emergency Response System
=================================================================

Responsible for managing emergency protocols, their activation conditions,
and response procedures. Extracted from EmergencyResponseSystem to follow 
Single Responsibility Principle.

Author: Agent-7 (Class Hierarchy Refactoring)
Contract: MODULAR-002: Class Hierarchy Refactoring (400 pts)
License: MIT
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

from ..base_manager import BaseManager


logger = logging.getLogger(__name__)


class ProtocolStatus(Enum):
    """Protocol activation status"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    ESCALATED = "escalated"
    COMPLETED = "completed"
    FAILED = "failed"


class ProtocolPriority(Enum):
    """Protocol priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ResponseAction:
    """Emergency response action definition"""
    action: str
    description: str
    priority: ProtocolPriority
    timeout: int  # seconds
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


@dataclass
class EscalationProcedure:
    """Protocol escalation procedure"""
    level: ProtocolPriority
    action: str
    timeout: int  # seconds
    description: str
    triggered: bool = False
    trigger_time: Optional[datetime] = None


@dataclass
class RecoveryProcedure:
    """Protocol recovery procedure"""
    action: str
    description: str
    validation_criteria: List[str]
    required: bool = True
    completed: bool = False
    completion_time: Optional[datetime] = None
    validation_results: Optional[Dict[str, bool]] = None


@dataclass
class EmergencyProtocol:
    """Emergency response protocol definition"""
    name: str
    description: str
    activation_conditions: List[str]
    response_actions: List[ResponseAction]
    escalation_procedures: List[EscalationProcedure]
    recovery_procedures: List[RecoveryProcedure]
    validation_criteria: List[str]
    documentation_requirements: List[str]
    status: ProtocolStatus = ProtocolStatus.INACTIVE
    activated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    activation_source: Optional[str] = None


@dataclass
class ProtocolExecution:
    """Protocol execution tracking"""
    protocol_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: ProtocolStatus = ProtocolStatus.ACTIVE
    actions_completed: int = 0
    total_actions: int = 0
    escalation_level: ProtocolPriority = ProtocolPriority.LOW
    errors: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


class ProtocolManager(BaseManager):
    """
    Emergency Protocol Manager - Single responsibility: Protocol management and execution
    
    This component is responsible for:
    - Managing emergency protocol definitions
    - Evaluating activation conditions
    - Executing response actions
    - Managing escalation procedures
    - Tracking recovery procedures
    """

    def __init__(self, config_path: str = "config/protocol_manager.json"):
        """Initialize protocol manager"""
        super().__init__(
            manager_name="ProtocolManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Protocol storage
        self.emergency_protocols: Dict[str, EmergencyProtocol] = {}
        self.protocol_handlers: Dict[str, Callable] = {}
        
        # Execution tracking
        self.active_executions: Dict[str, ProtocolExecution] = {}
        self.execution_history: List[ProtocolExecution] = []
        
        # Protocol state
        self.protocols_loaded = False
        self.default_protocols_configured = False
        
        # Load configuration and setup
        self._load_protocol_config()
        self._setup_default_protocols()
        
        self.logger.info("✅ Emergency Protocol Manager initialized successfully")

    def _load_protocol_config(self):
        """Load protocol manager configuration"""
        try:
            config = self.get_config()
            
            # Load custom protocols if available
            if 'custom_protocols' in config:
                for protocol_data in config['custom_protocols']:
                    protocol = self._create_protocol_from_data(protocol_data)
                    if protocol:
                        self.emergency_protocols[protocol.name] = protocol
            
            self.protocols_loaded = True
            
        except Exception as e:
            self.logger.error(f"Failed to load protocol config: {e}")

    def _setup_default_protocols(self):
        """Setup default emergency protocols based on captains handbook"""
        try:
            # Emergency Workflow Restoration Protocol
            workflow_restoration = EmergencyProtocol(
                name="Emergency Workflow Restoration",
                description="Critical intervention system for restoring stalled workflows and momentum",
                activation_conditions=[
                    "Workflow stall detected in any agent mission",
                    "Sprint acceleration momentum loss",
                    "Contract claiming system failures",
                    "Agent coordination breakdowns"
                ],
                response_actions=[
                    ResponseAction(
                        action="generate_emergency_contracts",
                        description="Generate 10+ emergency contracts worth 4,375+ points",
                        priority=ProtocolPriority.CRITICAL,
                        timeout=300  # 5 minutes
                    ),
                    ResponseAction(
                        action="activate_agent_mobilization",
                        description="Send emergency directives to all agents",
                        priority=ProtocolPriority.HIGH,
                        timeout=60  # 1 minute
                    ),
                    ResponseAction(
                        action="validate_system_health",
                        description="Perform comprehensive system health audit",
                        priority=ProtocolPriority.HIGH,
                        timeout=600  # 10 minutes
                    )
                ],
                escalation_procedures=[
                    EscalationProcedure(
                        level=ProtocolPriority.HIGH,
                        action="notify_captain_coordinator",
                        timeout=120,
                        description="Notify captain coordinator of critical situation"
                    ),
                    EscalationProcedure(
                        level=ProtocolPriority.CRITICAL,
                        action="activate_code_black_protocol",
                        timeout=60,
                        description="Activate highest level emergency protocol"
                    )
                ],
                recovery_procedures=[
                    RecoveryProcedure(
                        action="restore_contract_system",
                        description="Fix contract claiming system and synchronization",
                        validation_criteria=["Contract availability > 40"]
                    ),
                    RecoveryProcedure(
                        action="resolve_task_conflicts",
                        description="Resolve task assignment conflicts",
                        validation_criteria=["No task assignment conflicts"]
                    ),
                    RecoveryProcedure(
                        action="optimize_agent_priority",
                        description="Optimize agent priority system",
                        validation_criteria=["Agent priority system aligned"]
                    )
                ],
                validation_criteria=[
                    "All agents can claim emergency contracts",
                    "Perpetual motion system resumes operation",
                    "Contract system corruption resolved",
                    "System returns to 40+ available contracts",
                    "Workflow momentum restored"
                ],
                documentation_requirements=[
                    "Emergency event log",
                    "Response action timeline",
                    "Recovery validation results",
                    "Lessons learned documentation"
                ]
            )
            
            # Crisis Management Protocol
            crisis_management = EmergencyProtocol(
                name="Crisis Management",
                description="Real-time crisis management and system health monitoring",
                activation_conditions=[
                    "Contract completion rate < 40%",
                    "Agent idle time > 15 minutes",
                    "Workflow synchronization errors",
                    "Task assignment conflicts"
                ],
                response_actions=[
                    ResponseAction(
                        action="deploy_emergency_contracts",
                        description="Generate and deploy emergency contracts within 5 minutes",
                        priority=ProtocolPriority.CRITICAL,
                        timeout=300
                    ),
                    ResponseAction(
                        action="implement_bulk_messaging",
                        description="Send system-wide emergency announcements",
                        priority=ProtocolPriority.HIGH,
                        timeout=120
                    ),
                    ResponseAction(
                        action="activate_health_monitoring",
                        description="Enable continuous system health assessment",
                        priority=ProtocolPriority.HIGH,
                        timeout=60
                    )
                ],
                escalation_procedures=[
                    EscalationProcedure(
                        level=ProtocolPriority.MEDIUM,
                        action="increase_monitoring_frequency",
                        timeout=300,
                        description="Increase monitoring frequency for crisis situation"
                    ),
                    EscalationProcedure(
                        level=ProtocolPriority.HIGH,
                        action="activate_emergency_coordination",
                        timeout=180,
                        description="Activate emergency coordination protocols"
                    )
                ],
                recovery_procedures=[
                    RecoveryProcedure(
                        action="restore_workflow_momentum",
                        description="Restore workflow momentum and agent engagement",
                        validation_criteria=["Agent engagement > 90%"]
                    ),
                    RecoveryProcedure(
                        action="validate_system_synchronization",
                        description="Ensure system component synchronization",
                        validation_criteria=["All systems synchronized"]
                    )
                ],
                validation_criteria=[
                    "Workflow momentum restored",
                    "Agent engagement levels normalized",
                    "System synchronization validated",
                    "Performance metrics within thresholds"
                ],
                documentation_requirements=[
                    "Crisis timeline documentation",
                    "Response effectiveness analysis",
                    "System recovery validation",
                    "Prevention strategy documentation"
                ]
            )
            
            # Add default protocols
            self.emergency_protocols["workflow_restoration"] = workflow_restoration
            self.emergency_protocols["crisis_management"] = crisis_management
            
            self.default_protocols_configured = True
            self.logger.info("✅ Default emergency protocols configured")
            
        except Exception as e:
            self.logger.error(f"Failed to setup default protocols: {e}")

    def _create_protocol_from_data(self, protocol_data: Dict[str, Any]) -> Optional[EmergencyProtocol]:
        """Create EmergencyProtocol from configuration data"""
        try:
            # Convert response actions
            response_actions = []
            for action_data in protocol_data.get('response_actions', []):
                action = ResponseAction(
                    action=action_data['action'],
                    description=action_data['description'],
                    priority=ProtocolPriority(action_data['priority']),
                    timeout=action_data['timeout'],
                    required=action_data.get('required', True)
                )
                response_actions.append(action)
            
            # Convert escalation procedures
            escalation_procedures = []
            for escalation_data in protocol_data.get('escalation_procedures', []):
                escalation = EscalationProcedure(
                    level=ProtocolPriority(escalation_data['level']),
                    action=escalation_data['action'],
                    timeout=escalation_data['timeout'],
                    description=escalation_data.get('description', '')
                )
                escalation_procedures.append(escalation)
            
            # Convert recovery procedures
            recovery_procedures = []
            for recovery_data in protocol_data.get('recovery_procedures', []):
                recovery = RecoveryProcedure(
                    action=recovery_data['action'],
                    description=recovery_data['description'],
                    validation_criteria=recovery_data['validation_criteria']
                )
                recovery_procedures.append(recovery)
            
            # Create protocol
            protocol = EmergencyProtocol(
                name=protocol_data['name'],
                description=protocol_data['description'],
                activation_conditions=protocol_data['activation_conditions'],
                response_actions=response_actions,
                escalation_procedures=escalation_procedures,
                recovery_procedures=recovery_procedures,
                validation_criteria=protocol_data['validation_criteria'],
                documentation_requirements=protocol_data['documentation_requirements']
            )
            
            return protocol
            
        except Exception as e:
            self.logger.error(f"Failed to create protocol from data: {e}")
            return None

    def add_protocol(self, protocol: EmergencyProtocol):
        """Add a new emergency protocol"""
        self.emergency_protocols[protocol.name] = protocol
        self.logger.info(f"✅ Added emergency protocol: {protocol.name}")

    def remove_protocol(self, protocol_name: str):
        """Remove an emergency protocol"""
        if protocol_name in self.emergency_protocols:
            del self.emergency_protocols[protocol_name]
            self.logger.info(f"✅ Removed emergency protocol: {protocol_name}")

    def get_protocol(self, protocol_name: str) -> Optional[EmergencyProtocol]:
        """Get a specific emergency protocol"""
        return self.emergency_protocols.get(protocol_name)

    def list_protocols(self) -> List[str]:
        """List all available protocol names"""
        return list(self.emergency_protocols.keys())

    def evaluate_activation_conditions(self, protocol_name: str, 
                                    system_state: Dict[str, Any]) -> bool:
        """Evaluate if a protocol's activation conditions are met"""
        try:
            protocol = self.get_protocol(protocol_name)
            if not protocol:
                return False
            
            # Check each activation condition
            for condition in protocol.activation_conditions:
                if not self._evaluate_condition(condition, system_state):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate activation conditions for {protocol_name}: {e}")
            return False

    def _evaluate_condition(self, condition: str, system_state: Dict[str, Any]) -> bool:
        """Evaluate a single activation condition"""
        try:
            # Simple condition evaluation - can be enhanced with more sophisticated logic
            if "contract completion rate" in condition:
                rate = system_state.get('contract_completion_rate', 100)
                return rate < 40
            elif "agent idle time" in condition:
                idle_time = system_state.get('max_agent_idle_time', 0)
                return idle_time > 900  # 15 minutes
            elif "workflow stall" in condition:
                return system_state.get('workflow_stalled', False)
            elif "contract system down" in condition:
                return system_state.get('contract_system_available', True) == False
            else:
                # Default to true for unknown conditions
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False

    def activate_protocol(self, protocol_name: str, source: str = "system") -> bool:
        """Activate an emergency protocol"""
        try:
            protocol = self.get_protocol(protocol_name)
            if not protocol:
                self.logger.error(f"Protocol not found: {protocol_name}")
                return False
            
            if protocol.status != ProtocolStatus.INACTIVE:
                self.logger.warning(f"Protocol {protocol_name} is already {protocol.status.value}")
                return False
            
            # Update protocol status
            protocol.status = ProtocolStatus.ACTIVE
            protocol.activated_at = datetime.now()
            protocol.activation_source = source
            
            # Create execution tracking
            execution = ProtocolExecution(
                protocol_name=protocol_name,
                start_time=datetime.now(),
                total_actions=len(protocol.response_actions)
            )
            
            self.active_executions[protocol_name] = execution
            
            # Record event
            self.record_event("protocol_activated", {
                "protocol_name": protocol_name,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info(f"🚨 Emergency protocol activated: {protocol_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate protocol {protocol_name}: {e}")
            return False

    def execute_protocol_actions(self, protocol_name: str) -> Dict[str, Any]:
        """Execute all actions for an active protocol"""
        try:
            protocol = self.get_protocol(protocol_name)
            execution = self.active_executions.get(protocol_name)
            
            if not protocol or not execution:
                return {"error": "Protocol not found or not active"}
            
            if protocol.status != ProtocolStatus.ACTIVE:
                return {"error": f"Protocol is {protocol.status.value}"}
            
            results = {}
            
            # Execute response actions
            for action in protocol.response_actions:
                if not action.completed:
                    result = self._execute_action(action, protocol_name)
                    action.completed = True
                    action.completion_time = datetime.now()
                    action.result = result
                    
                    results[action.action] = result
                    execution.actions_completed += 1
                    
                    # Check for timeout
                    if action.timeout > 0:
                        elapsed = (datetime.now() - execution.start_time).total_seconds()
                        if elapsed > action.timeout:
                            self.logger.warning(f"Action {action.action} timed out after {action.timeout}s")
            
            # Check if all actions completed
            if execution.actions_completed >= execution.total_actions:
                protocol.status = ProtocolStatus.COMPLETED
                protocol.completed_at = datetime.now()
                execution.status = ProtocolStatus.COMPLETED
                execution.end_time = datetime.now()
                
                # Move to history
                self.execution_history.append(execution)
                del self.active_executions[protocol_name]
                
                self.logger.info(f"✅ Protocol {protocol_name} completed successfully")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to execute protocol actions for {protocol_name}: {e}")
            return {"error": str(e)}

    def _execute_action(self, action: ResponseAction, protocol_name: str) -> Dict[str, Any]:
        """Execute a single protocol action"""
        try:
            # This would integrate with actual action execution systems
            # For now, simulate action execution
            
            if action.action == "generate_emergency_contracts":
                return {
                    "status": "success",
                    "contracts_generated": 15,
                    "total_points": 5000,
                    "execution_time": 2.5
                }
            elif action.action == "activate_agent_mobilization":
                return {
                    "status": "success",
                    "agents_notified": 8,
                    "response_rate": 100,
                    "execution_time": 0.8
                }
            elif action.action == "validate_system_health":
                return {
                    "status": "success",
                    "health_score": 0.85,
                    "issues_found": 2,
                    "execution_time": 8.2
                }
            else:
                return {
                    "status": "simulated",
                    "action": action.action,
                    "execution_time": 1.0
                }
                
        except Exception as e:
            self.logger.error(f"Failed to execute action {action.action}: {e}")
            return {"status": "error", "error": str(e)}

    def get_protocol_status(self, protocol_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific protocol"""
        try:
            protocol = self.get_protocol(protocol_name)
            execution = self.active_executions.get(protocol_name)
            
            if not protocol:
                return None
            
            return {
                "name": protocol.name,
                "status": protocol.status.value,
                "activated_at": protocol.activated_at.isoformat() if protocol.activated_at else None,
                "completed_at": protocol.completed_at.isoformat() if protocol.completed_at else None,
                "activation_source": protocol.activation_source,
                "execution": {
                    "actions_completed": execution.actions_completed if execution else 0,
                    "total_actions": execution.total_actions if execution else len(protocol.response_actions),
                    "start_time": execution.start_time.isoformat() if execution else None,
                    "status": execution.status.value if execution else "not_started"
                } if execution else None
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get protocol status for {protocol_name}: {e}")
            return None

    def get_all_protocol_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all protocols"""
        return {
            name: self.get_protocol_status(name)
            for name in self.list_protocols()
        }

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get protocol execution history"""
        return [
            {
                "protocol_name": e.protocol_name,
                "start_time": e.start_time.isoformat(),
                "end_time": e.end_time.isoformat() if e.end_time else None,
                "status": e.status.value,
                "actions_completed": e.actions_completed,
                "total_actions": e.total_actions,
                "escalation_level": e.escalation_level.value,
                "errors": e.errors,
                "results": e.results
            }
            for e in self.execution_history
        ]

    def health_check(self) -> Dict[str, Any]:
        """Health check for the protocol manager"""
        try:
            return {
                "is_healthy": True,
                "protocols_loaded": self.protocols_loaded,
                "default_protocols_configured": self.default_protocols_configured,
                "total_protocols": len(self.emergency_protocols),
                "active_executions": len(self.active_executions),
                "total_executions": len(self.execution_history),
                "protocols": list(self.emergency_protocols.keys())
            }
            
        except Exception as e:
            return {
                "is_healthy": False,
                "error": str(e)
            }


# Export the main classes
__all__ = [
    "ProtocolManager", "EmergencyProtocol", "ProtocolStatus", "ProtocolPriority",
    "ResponseAction", "EscalationProcedure", "RecoveryProcedure", "ProtocolExecution"
]
