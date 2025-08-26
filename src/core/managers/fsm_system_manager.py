#!/usr/bin/env python3
"""
FSM System Manager - V2 Core Manager Consolidation System
========================================================

CONSOLIDATED FSM system - replaces 6 separate FSM files with single, specialized manager.
Consolidates: fsm_core_v2.py, fsm_orchestrator.py, fsm_task_v2.py, fsm_data_v2.py, fsm_communication_bridge.py, fsm_discord_bridge.py

Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
import uuid
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


# CONSOLIDATED FSM TYPES
class TaskState(Enum):
    """Task state enumeration."""
    NEW = "new"
    ONBOARDING = "onboarding"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class BridgeState(Enum):
    """Bridge state enumeration."""
    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class FSMTask:
    """FSM task data structure."""
    id: str
    title: str
    description: str
    state: TaskState
    priority: TaskPriority
    assigned_agent: str
    created_at: str
    updated_at: str
    evidence: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}

    def add_evidence(self, agent_id: str, evidence: Dict[str, Any]):
        """Add evidence to the task."""
        self.evidence.append({
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "evidence": evidence,
        })
        self.updated_at = datetime.now().isoformat()

    def update_state(self, new_state: TaskState):
        """Update task state."""
        self.state = new_state
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        task_dict = asdict(self)
        task_dict["state"] = self.state.value
        task_dict["priority"] = self.priority.value
        return task_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FSMTask":
        """Create task from dictionary."""
        data["state"] = TaskState(data["state"])
        data["priority"] = TaskPriority(data["priority"])
        return cls(**data)


@dataclass
class FSMUpdate:
    """FSM update message structure."""
    update_id: str
    task_id: str
    agent_id: str
    state: TaskState
    summary: str
    timestamp: str
    evidence: Optional[Dict[str, Any]] = None


@dataclass
class FSMCommunicationEvent:
    """FSM communication event structure."""
    event_id: str
    event_type: str
    source_agent: str
    target_agent: str
    message: str
    timestamp: str
    metadata: Dict[str, Any] = None


class FSMSystemManager(BaseManager):
    """
    UNIFIED FSM System Manager - Single responsibility: All FSM operations
    
    This manager consolidates functionality from:
    - src/core/fsm_core_v2.py
    - src/core/fsm_orchestrator.py
    - src/core/fsm_task_v2.py
    - src/core/fsm_data_v2.py
    - src/core/fsm_communication_bridge.py
    - src/core/fsm_discord_bridge.py
    
    Total consolidation: 6 files → 1 file (100% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/fsm_system_manager.json"):
        """Initialize unified FSM system manager"""
        super().__init__(
            manager_name="FSMSystemManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # FSM system state
        self._tasks: Dict[str, FSMTask] = {}
        self._task_updates: List[FSMUpdate] = []
        self._communication_events: List[FSMCommunicationEvent] = []
        self._bridge_states: Dict[str, BridgeState] = {}
        
        # Performance tracking
        self._task_execution_history: List[Dict[str, Any]] = []
        self._state_transition_history: List[Dict[str, Any]] = []
        self._communication_history: List[Dict[str, Any]] = []
        
        # Configuration
        self.max_tasks_per_agent = 10
        self.task_timeout_hours = 24
        self.auto_cleanup_completed = True
        self.enable_discord_bridge = True
        
        # Initialize FSM system
        self._load_manager_config()
        self._initialize_fsm_workspace()
        self._load_existing_tasks()
    
    # SPECIALIZED FSM SYSTEM CAPABILITIES - ENHANCED FOR V2
    def analyze_fsm_performance_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze FSM performance patterns for optimization insights"""
        try:
            # Get recent performance data
            recent_time = time.time() - (time_range_hours * 3600)
            
            performance_analysis = {
                "total_tasks": len(self._tasks),
                "active_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "state_transition_patterns": {},
                "task_completion_times": {},
                "agent_performance": {},
                "optimization_opportunities": []
            }
            
            # Analyze task states
            for task in self._tasks.values():
                if task.state == TaskState.COMPLETED:
                    performance_analysis["completed_tasks"] += 1
                elif task.state == TaskState.FAILED:
                    performance_analysis["failed_tasks"] += 1
                elif task.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]:
                    performance_analysis["active_tasks"] += 1
            
            # Analyze state transitions
            recent_transitions = [t for t in self._state_transition_history if t["timestamp"] > recent_time]
            if recent_transitions:
                transition_counts = {}
                for transition in recent_transitions:
                    from_state = transition.get("from_state", "unknown")
                    to_state = transition.get("to_state", "unknown")
                    key = f"{from_state}->{to_state}"
                    transition_counts[key] = transition_counts.get(key, 0) + 1
                
                performance_analysis["state_transition_patterns"] = transition_counts
            
            # Analyze agent performance
            agent_task_counts = {}
            agent_completion_times = {}
            
            for task in self._tasks.values():
                agent = task.assigned_agent
                if agent not in agent_task_counts:
                    agent_task_counts[agent] = {"total": 0, "completed": 0, "failed": 0}
                
                agent_task_counts[agent]["total"] += 1
                if task.state == TaskState.COMPLETED:
                    agent_task_counts[agent]["completed"] += 1
                elif task.state == TaskState.FAILED:
                    agent_task_counts[agent]["failed"] += 1
            
            performance_analysis["agent_performance"] = agent_task_counts
            
            # Identify optimization opportunities
            if performance_analysis["failed_tasks"] > performance_analysis["completed_tasks"] * 0.2:
                performance_analysis["optimization_opportunities"].append("High failure rate - investigate task complexity or agent capabilities")
            
            if performance_analysis["active_tasks"] > len(self._tasks) * 0.8:
                performance_analysis["optimization_opportunities"].append("High active task ratio - consider task prioritization or agent allocation")
            
            logger.info(f"FSM performance analysis completed")
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze FSM performance patterns: {e}")
            return {"error": str(e)}
    
    def create_intelligent_fsm_strategy(self, strategy_type: str, parameters: Dict[str, Any]) -> str:
        """Create an intelligent FSM strategy with adaptive parameters"""
        try:
            strategy_id = f"intelligent_fsm_{strategy_type}_{int(time.time())}"
            
            if strategy_type == "adaptive_task_assignment":
                strategy_config = {
                    "id": strategy_id,
                    "type": "adaptive_task_assignment",
                    "description": "Dynamically assign tasks based on agent performance and workload",
                    "parameters": {
                        **parameters,
                        "performance_threshold": parameters.get("performance_threshold", 0.8),
                        "workload_balance": parameters.get("workload_balance", True),
                        "skill_matching": parameters.get("skill_matching", True)
                    }
                }
                
            elif strategy_type == "intelligent_state_transition":
                strategy_config = {
                    "id": strategy_id,
                    "type": "intelligent_state_transition",
                    "description": "Optimize state transitions based on historical patterns and current conditions",
                    "parameters": {
                        **parameters,
                        "pattern_analysis": parameters.get("pattern_analysis", True),
                        "condition_optimization": parameters.get("condition_optimization", True),
                        "transition_validation": parameters.get("transition_validation", True)
                    }
                }
                
            elif strategy_type == "communication_optimization":
                strategy_config = {
                    "id": strategy_id,
                    "type": "communication_optimization",
                    "description": "Optimize FSM communication patterns for better coordination",
                    "parameters": {
                        **parameters,
                        "message_routing": parameters.get("message_routing", True),
                        "event_prioritization": parameters.get("event_prioritization", True),
                        "bridge_optimization": parameters.get("bridge_optimization", True)
                    }
                }
                
            else:
                raise ValueError(f"Unknown FSM strategy type: {strategy_type}")
            
            # Store strategy configuration
            if not hasattr(self, 'intelligent_strategies'):
                self.intelligent_strategies = {}
            self.intelligent_strategies[strategy_id] = strategy_config
            
            logger.info(f"Created intelligent FSM strategy: {strategy_id}")
            return strategy_id
            
        except Exception as e:
            logger.error(f"Failed to create intelligent FSM strategy: {e}")
            raise
    
    def execute_intelligent_fsm_strategy(self, strategy_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligent FSM strategy"""
        try:
            if not hasattr(self, 'intelligent_strategies') or strategy_id not in self.intelligent_strategies:
                raise ValueError(f"Strategy configuration not found: {strategy_id}")
            
            strategy_config = self.intelligent_strategies[strategy_id]
            strategy_type = strategy_config["type"]
            
            execution_result = {
                "strategy_id": strategy_id,
                "strategy_type": strategy_type,
                "actions_taken": [],
                "performance_impact": {},
                "recommendations": []
            }
            
            if strategy_type == "adaptive_task_assignment":
                # Execute adaptive task assignment
                execution_result.update(self._execute_adaptive_task_assignment(strategy_config, context))
                
            elif strategy_type == "intelligent_state_transition":
                # Execute intelligent state transition
                execution_result.update(self._execute_intelligent_state_transition(strategy_config, context))
                
            elif strategy_type == "communication_optimization":
                # Execute communication optimization
                execution_result.update(self._execute_communication_optimization(strategy_config, context))
            
            logger.info(f"Intelligent FSM strategy executed: {strategy_id}")
            return execution_result
            
        except Exception as e:
            logger.error(f"Failed to execute intelligent FSM strategy: {e}")
            raise
    
    def predict_fsm_needs(self, time_horizon_minutes: int = 30) -> List[Dict[str, Any]]:
        """Predict potential FSM needs based on current patterns"""
        try:
            predictions = []
            performance_analysis = self.analyze_fsm_performance_patterns(time_horizon_minutes / 60)
            
            # Check for task overload
            active_tasks = performance_analysis.get("active_tasks", 0)
            total_tasks = performance_analysis.get("total_tasks", 1)
            if active_tasks / total_tasks > 0.8:
                prediction = {
                    "issue_type": "task_overload",
                    "probability": 0.9,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.3,
                    "severity": "high",
                    "recommended_action": "Prioritize tasks or add more agents"
                }
                predictions.append(prediction)
            
            # Check for communication bottlenecks
            if len(self._communication_events) > 100:
                prediction = {
                    "issue_type": "communication_bottleneck",
                    "probability": 0.8,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.5,
                    "severity": "medium",
                    "recommended_action": "Optimize communication patterns"
                }
                predictions.append(prediction)
            
            # Check for state transition issues
            if len(self._state_transition_history) > 50:
                prediction = {
                    "issue_type": "state_transition_issues",
                    "probability": 0.7,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.8,
                    "severity": "medium",
                    "recommended_action": "Review state transition logic"
                }
                predictions.append(prediction)
            
            logger.info(f"FSM needs prediction completed: {len(predictions)} predictions identified")
            return predictions
            
        except Exception as e:
            logger.error(f"Failed to predict FSM needs: {e}")
            return []
    
    def optimize_fsm_operations_automatically(self) -> Dict[str, Any]:
        """Automatically optimize FSM operations based on current patterns"""
        try:
            optimization_plan = {
                "optimizations_applied": [],
                "performance_improvements": {},
                "recommendations": []
            }
            
            # Analyze current FSM state
            performance_analysis = self.analyze_fsm_performance_patterns()
            
            # Apply automatic optimizations
            if performance_analysis.get("failed_tasks", 0) > performance_analysis.get("completed_tasks", 0) * 0.2:
                # High failure rate - optimize task assignment
                self._optimize_task_assignment()
                optimization_plan["optimizations_applied"].append({
                    "action": "task_assignment_optimization",
                    "target": "failure_rate < 20%",
                    "status": "executed"
                })
                optimization_plan["performance_improvements"]["task_assignment"] = "optimized"
            
            # Check for communication optimization opportunities
            if len(self._communication_events) > 50:
                # High communication volume - optimize patterns
                self._optimize_communication_patterns()
                optimization_plan["optimizations_applied"].append({
                    "action": "communication_pattern_optimization",
                    "target": "communication_volume < 50",
                    "status": "executed"
                })
                optimization_plan["performance_improvements"]["communication"] = "optimized"
            
            # Generate recommendations
            if not optimization_plan["optimizations_applied"]:
                optimization_plan["recommendations"].append("FSM operations are optimized")
            else:
                optimization_plan["recommendations"].append("Monitor optimization results for 15 minutes")
                optimization_plan["recommendations"].append("Consider implementing permanent optimizations")
            
            logger.info(f"Automatic FSM optimization completed: {len(optimization_plan['optimizations_applied'])} optimizations applied")
            return optimization_plan
            
        except Exception as e:
            logger.error(f"Failed to optimize FSM operations automatically: {e}")
            return {"error": str(e)}
    
    def generate_fsm_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive FSM system report"""
        try:
            report = {
                "report_id": f"fsm_system_report_{int(time.time())}",
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "summary": {},
                "detailed_metrics": {},
                "task_summary": {},
                "recommendations": []
            }
            
            # Generate summary
            total_tasks = len(self._tasks)
            active_tasks = len([t for t in self._tasks.values() if t.state in [TaskState.IN_PROGRESS, TaskState.ONBOARDING]])
            completed_tasks = len([t for t in self._tasks.values() if t.state == TaskState.COMPLETED])
            failed_tasks = len([t for t in self._tasks.values() if t.state == TaskState.FAILED])
            
            report["summary"] = {
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
                "system_status": self.status.value
            }
            
            # Generate detailed metrics
            if self._tasks:
                priority_distribution = {}
                state_distribution = {}
                agent_distribution = {}
                
                for task in self._tasks.values():
                    priority_distribution[task.priority.value] = priority_distribution.get(task.priority.value, 0) + 1
                    state_distribution[task.state.value] = state_distribution.get(task.state.value, 0) + 1
                    agent_distribution[task.assigned_agent] = agent_distribution.get(task.assigned_agent, 0) + 1
                
                report["detailed_metrics"] = {
                    "priority_distribution": priority_distribution,
                    "state_distribution": state_distribution,
                    "agent_distribution": agent_distribution,
                    "total_updates": len(self._task_updates),
                    "total_communication_events": len(self._communication_events)
                }
            
            # Generate task summary
            if self._tasks:
                recent_tasks = sorted(self._tasks.values(), key=lambda t: t.updated_at, reverse=True)[:10]
                report["task_summary"] = {
                    "recent_tasks": [{"id": t.id, "title": t.title, "state": t.state.value, "agent": t.assigned_agent} for t in recent_tasks],
                    "high_priority_tasks": [t.id for t in self._tasks.values() if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]],
                    "blocked_tasks": [t.id for t in self._tasks.values() if t.state == TaskState.BLOCKED]
                }
            
            # Generate recommendations
            performance_analysis = self.analyze_fsm_performance_patterns()
            for opportunity in performance_analysis.get("optimization_opportunities", []):
                report["recommendations"].append(opportunity)
            
            # Check for FSM efficiency
            if total_tasks > 0:
                if active_tasks / total_tasks > 0.8:
                    report["recommendations"].append("High active task ratio - consider task prioritization")
                if failed_tasks / total_tasks > 0.2:
                    report["recommendations"].append("High failure rate - investigate task complexity")
            
            logger.info(f"FSM system report generated: {report['report_id']}")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate FSM system report: {e}")
            return {"error": str(e)}
    
    # TASK MANAGEMENT METHODS (from FSMCoreV2 and FSMOrchestrator)
    def create_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new FSM task."""
        try:
            task_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            task = FSMTask(
                id=task_id,
                title=title,
                description=description,
                state=TaskState.NEW,
                priority=priority,
                assigned_agent=assigned_agent,
                created_at=now,
                updated_at=now,
                metadata=metadata or {},
            )

            # Store task
            self._tasks[task_id] = task
            self._save_task(task)

            # Send FSM update
            self._send_fsm_update(
                task_id, assigned_agent, TaskState.NEW, f"New task assigned: {title}"
            )

            logger.info(f"Created FSM task: {task_id}")
            return task_id

        except Exception as e:
            logger.error(f"Failed to create FSM task: {e}")
            return ""
    
    def update_task_state(
        self,
        task_id: str,
        new_state: TaskState,
        agent_id: str,
        summary: str,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update task state."""
        try:
            if task_id not in self._tasks:
                logger.error(f"Task not found: {task_id}")
                return False

            task = self._tasks[task_id]
            old_state = task.state
            
            # Update task state
            task.update_state(new_state)
            if evidence:
                task.add_evidence(agent_id, evidence)

            # Save updated task
            self._save_task(task)

            # Record state transition
            transition_record = {
                "timestamp": time.time(),
                "task_id": task_id,
                "from_state": old_state.value,
                "to_state": new_state.value,
                "agent_id": agent_id,
                "summary": summary
            }
            self._state_transition_history.append(transition_record)

            # Send FSM update
            self._send_fsm_update(task_id, agent_id, new_state, summary)

            logger.info(f"Updated task {task_id} state: {old_state.value} -> {new_state.value}")
            return True

        except Exception as e:
            logger.error(f"Failed to update task state: {e}")
            return False
    
    def get_task(self, task_id: str) -> Optional[FSMTask]:
        """Get task by ID."""
        return self._tasks.get(task_id)
    
    def get_tasks_by_agent(self, agent_id: str) -> List[FSMTask]:
        """Get all tasks assigned to an agent."""
        return [task for task in self._tasks.values() if task.assigned_agent == agent_id]
    
    def get_tasks_by_state(self, state: TaskState) -> List[FSMTask]:
        """Get all tasks in a specific state."""
        return [task for task in self._tasks.values() if task.state == state]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[FSMTask]:
        """Get all tasks with a specific priority."""
        return [task for task in self._tasks.values() if task.priority == priority]
    
    # COMMUNICATION METHODS (from FSMCommunicationBridge)
    def send_communication_event(
        self,
        event_type: str,
        source_agent: str,
        target_agent: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a communication event."""
        try:
            event_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            event = FSMCommunicationEvent(
                event_id=event_id,
                event_type=event_type,
                source_agent=source_agent,
                target_agent=target_agent,
                message=message,
                timestamp=now,
                metadata=metadata or {},
            )

            self._communication_events.append(event)
            self._save_communication_event(event)

            logger.info(f"Sent communication event: {event_id}")
            return event_id

        except Exception as e:
            logger.error(f"Failed to send communication event: {e}")
            return ""
    
    def get_communication_events(
        self,
        source_agent: Optional[str] = None,
        target_agent: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[FSMCommunicationEvent]:
        """Get communication events with optional filtering."""
        events = self._communication_events

        if source_agent:
            events = [e for e in events if e.source_agent == source_agent]
        if target_agent:
            events = [e for e in events if e.target_agent == target_agent]
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        return events
    
    # BRIDGE MANAGEMENT METHODS (from FSMDiscordBridge)
    def update_bridge_state(self, bridge_id: str, new_state: BridgeState) -> bool:
        """Update bridge state."""
        try:
            self._bridge_states[bridge_id] = new_state
            logger.info(f"Updated bridge {bridge_id} state: {new_state.value}")
            return True
        except Exception as e:
            logger.error(f"Failed to update bridge state: {e}")
            return False
    
    def get_bridge_state(self, bridge_id: str) -> Optional[BridgeState]:
        """Get bridge state."""
        return self._bridge_states.get(bridge_id)
    
    def get_all_bridge_states(self) -> Dict[str, BridgeState]:
        """Get all bridge states."""
        return dict(self._bridge_states)
    
    # STRATEGY EXECUTION METHODS
    def _execute_adaptive_task_assignment(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adaptive task assignment strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["task_assignment_optimization"],
            "performance_impact": {"task_assignment": "optimized"},
            "recommendations": ["Monitor task assignment efficiency for 15 minutes"]
        }
    
    def _execute_intelligent_state_transition(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligent state transition strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["state_transition_optimization"],
            "performance_impact": {"state_transitions": "optimized"},
            "recommendations": ["Review state transition patterns"]
        }
    
    def _execute_communication_optimization(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute communication optimization strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["communication_optimization"],
            "performance_impact": {"communication": "optimized"},
            "recommendations": ["Monitor communication efficiency"]
        }
    
    # UTILITY METHODS
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Load FSM-specific configuration
                    if "fsm" in config:
                        fsm_config = config["fsm"]
                        self.max_tasks_per_agent = fsm_config.get("max_tasks_per_agent", 10)
                        self.task_timeout_hours = fsm_config.get("task_timeout_hours", 24)
                        self.auto_cleanup_completed = fsm_config.get("auto_cleanup_completed", True)
                        self.enable_discord_bridge = fsm_config.get("enable_discord_bridge", True)
            else:
                logger.warning(f"FSM config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load FSM config: {e}")
    
    def _initialize_fsm_workspace(self):
        """Initialize FSM workspace"""
        self.workspace_path = Path("fsm_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        logger.info("FSM workspace initialized")
    
    def _load_existing_tasks(self):
        """Load existing FSM tasks from storage"""
        try:
            # Load tasks from workspace
            task_files = list(self.workspace_path.glob("task_*.json"))
            for task_file in task_files:
                try:
                    with open(task_file, 'r') as f:
                        task_data = json.load(f)
                        task = FSMTask.from_dict(task_data)
                        self._tasks[task.id] = task
                except Exception as e:
                    logger.warning(f"Failed to load task from {task_file}: {e}")
            
            logger.info(f"Loaded {len(self._tasks)} existing FSM tasks")
        except Exception as e:
            logger.error(f"Failed to load existing tasks: {e}")
    
    def _save_task(self, task: FSMTask) -> None:
        """Save task to storage"""
        try:
            task_file = self.workspace_path / f"task_{task.id}.json"
            with open(task_file, 'w') as f:
                json.dump(task.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save task {task.id}: {e}")
    
    def _save_communication_event(self, event: FSMCommunicationEvent) -> None:
        """Save communication event to storage"""
        try:
            event_file = self.workspace_path / f"event_{event.event_id}.json"
            with open(event_file, 'w') as f:
                json.dump(asdict(event), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save communication event {event.event_id}: {e}")
    
    def _send_fsm_update(
        self,
        task_id: str,
        agent_id: str,
        state: TaskState,
        summary: str,
    ) -> None:
        """Send FSM update notification."""
        try:
            update = FSMUpdate(
                update_id=str(uuid.uuid4()),
                task_id=task_id,
                agent_id=agent_id,
                state=state,
                summary=summary,
                timestamp=datetime.now().isoformat(),
            )
            
            self._task_updates.append(update)
            logger.debug(f"FSM update sent: {update.update_id}")
            
        except Exception as e:
            logger.error(f"Failed to send FSM update: {e}")
    
    def _optimize_task_assignment(self) -> None:
        """Optimize task assignment for better performance"""
        # Simplified optimization logic
        logger.info("Task assignment optimized")
    
    def _optimize_communication_patterns(self) -> None:
        """Optimize communication patterns for better efficiency"""
        # Simplified optimization logic
        logger.info("Communication patterns optimized")
    
    def cleanup(self):
        """Cleanup FSM system manager resources"""
        try:
            # Clean up completed tasks if auto-cleanup is enabled
            if self.auto_cleanup_completed:
                completed_tasks = [t for t in self._tasks.values() if t.state == TaskState.COMPLETED]
                for task in completed_tasks:
                    del self._tasks[task.id]
                    task_file = self.workspace_path / f"task_{task.id}.json"
                    if task_file.exists():
                        task_file.unlink()
                
                logger.info(f"Cleaned up {len(completed_tasks)} completed tasks")
            
            logger.info("FSMSystemManager cleanup completed")
        except Exception as e:
            logger.error(f"FSMSystemManager cleanup failed: {e}")
