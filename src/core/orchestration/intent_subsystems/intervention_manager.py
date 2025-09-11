#!/usr/bin/env python3
"""
Intervention Manager - Intent-Oriented Subsystem
===============================================

Decomposed from SwarmOrchestrator to handle emergency intervention logic.
Provides plug-and-play, testable intervention management with clear separation of concerns.

Author: Swarm Representative (Following Commander Thea directives)
Mission: Orchestration Layer Decomposition - Intent Subsystem Creation
License: MIT
"""

from __future__ import annotations

import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Callable, Union
from pathlib import Path
import threading
import json

from ..contracts import OrchestrationContext, OrchestrationResult, Step
from ..registry import StepRegistry


class InterventionPriority(Enum):
    """Intervention priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InterventionType(Enum):
    """Intervention type enumeration."""
    SYSTEM_HEALTH = "system_health"
    RESOURCE_OVERLOAD = "resource_overload"
    COMMUNICATION_FAILURE = "communication_failure"
    COORDINATION_BREAKDOWN = "coordination_breakdown"
    SECURITY_THREAT = "security_threat"
    DATA_INTEGRITY = "data_integrity"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    AGENT_FAILURE = "agent_failure"


class InterventionStatus(Enum):
    """Intervention status enumeration."""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    EXECUTING = "executing"
    MITIGATED = "mitigated"
    FAILED = "failed"
    ESCALATED = "escalated"


class InterventionScope(Enum):
    """Intervention scope enumeration."""
    AGENT_SPECIFIC = "agent_specific"
    SUBSYSTEM_SPECIFIC = "subsystem_specific"
    SYSTEM_WIDE = "system_wide"
    CLUSTER_WIDE = "cluster_wide"


@dataclass
class InterventionTrigger:
    """Intervention trigger conditions."""
    condition_type: str
    threshold: Any
    comparison: str  # "gt", "lt", "eq", "contains", etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionAction:
    """Intervention action definition."""
    action_type: str
    target: str
    parameters: Dict[str, Any]
    timeout_seconds: int = 30
    retry_count: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InterventionResult:
    """Result of intervention execution."""
    intervention_id: str
    status: InterventionStatus
    actions_executed: List[str]
    metrics_before: Dict[str, Any]
    metrics_after: Dict[str, Any]
    execution_time: float
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class InterventionProtocol:
    """Complete intervention protocol."""
    protocol_id: str
    name: str
    description: str
    intervention_type: InterventionType
    priority: InterventionPriority
    scope: InterventionScope
    triggers: List[InterventionTrigger]
    actions: List[InterventionAction]
    cooldown_period: int = 300  # 5 minutes default
    max_executions_per_hour: int = 10
    metadata: Dict[str, Any] = field(default_factory=dict)


class InterventionStrategy(Protocol):
    """Strategy pattern for intervention management."""

    def detect_intervention_needed(self, context: Dict[str, Any]) -> Optional[InterventionProtocol]: ...

    def execute_intervention(self, protocol: InterventionProtocol, context: Dict[str, Any]) -> InterventionResult: ...

    def validate_intervention_effectiveness(self, result: InterventionResult) -> bool: ...


class SwarmInterventionStrategy:
    """Swarm-optimized intervention strategy."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def detect_intervention_needed(self, context: Dict[str, Any]) -> Optional[InterventionProtocol]:
        """Detect if intervention is needed based on context."""
        # System health check
        system_health = context.get("system_health", {})
        if system_health.get("cpu_percent", 0) > 90:
            return self._create_resource_protocol("CPU_OVERLOAD")

        if system_health.get("memory_percent", 0) > 85:
            return self._create_resource_protocol("MEMORY_OVERLOAD")

        # Agent failure detection
        agent_status = context.get("agent_status", {})
        failed_agents = [aid for aid, status in agent_status.items() if status.get("status") == "failed"]
        if failed_agents:
            return self._create_agent_failure_protocol(failed_agents)

        # Communication failure detection
        communication_status = context.get("communication_status", {})
        if communication_status.get("failed_messages", 0) > 10:
            return self._create_communication_protocol()

        return None

    def execute_intervention(self, protocol: InterventionProtocol, context: Dict[str, Any]) -> InterventionResult:
        """Execute the intervention protocol."""
        start_time = time.time()
        intervention_id = f"intervention_{int(time.time())}_{protocol.protocol_id}"

        actions_executed = []
        errors = []

        # Record metrics before intervention
        metrics_before = self._collect_system_metrics(context)

        try:
            for action in protocol.actions:
                try:
                    self._execute_action(action, context)
                    actions_executed.append(action.action_type)
                except Exception as e:
                    errors.append(f"Action {action.action_type} failed: {e}")

            status = InterventionStatus.MITIGATED if not errors else InterventionStatus.FAILED

        except Exception as e:
            errors.append(f"Intervention execution failed: {e}")
            status = InterventionStatus.FAILED

        # Record metrics after intervention
        metrics_after = self._collect_system_metrics(context)
        execution_time = time.time() - start_time

        result = InterventionResult(
            intervention_id=intervention_id,
            status=status,
            actions_executed=actions_executed,
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            execution_time=execution_time,
            errors=errors
        )

        self.logger.info(f"Intervention {intervention_id} completed with status: {status.value}")
        return result

    def validate_intervention_effectiveness(self, result: InterventionResult) -> bool:
        """Validate if intervention was effective."""
        # Check if critical metrics improved
        try:
            cpu_before = result.metrics_before.get("system_health", {}).get("cpu_percent", 100)
            cpu_after = result.metrics_after.get("system_health", {}).get("cpu_percent", 100)

            memory_before = result.metrics_before.get("system_health", {}).get("memory_percent", 100)
            memory_after = result.metrics_after.get("system_health", {}).get("memory_percent", 100)

            # Consider intervention effective if CPU or memory usage decreased by at least 10%
            cpu_improved = (cpu_before - cpu_after) > 10
            memory_improved = (memory_before - memory_after) > 10

            return cpu_improved or memory_improved or not result.errors

        except Exception:
            # If we can't validate, assume it was effective if no errors
            return not result.errors

    def _create_resource_protocol(self, resource_type: str) -> InterventionProtocol:
        """Create resource overload intervention protocol."""
        actions = [
            InterventionAction(
                action_type="scale_resources",
                target="system",
                parameters={"resource_type": resource_type, "scale_factor": 1.2}
            ),
            InterventionAction(
                action_type="notify_admin",
                target="admin",
                parameters={"message": f"Resource overload detected: {resource_type}"}
            )
        ]

        return InterventionProtocol(
            protocol_id=f"resource_{resource_type.lower()}_{int(time.time())}",
            name=f"{resource_type} Resource Intervention",
            description=f"Handle {resource_type} resource overload situation",
            intervention_type=InterventionType.RESOURCE_OVERLOAD,
            priority=InterventionPriority.HIGH,
            scope=InterventionScope.SYSTEM_WIDE,
            triggers=[],
            actions=actions
        )

    def _create_agent_failure_protocol(self, failed_agents: List[str]) -> InterventionProtocol:
        """Create agent failure intervention protocol."""
        actions = []
        for agent in failed_agents:
            actions.append(InterventionAction(
                action_type="restart_agent",
                target=agent,
                parameters={"agent_id": agent, "restart_type": "graceful"}
            ))

        return InterventionProtocol(
            protocol_id=f"agent_failure_{int(time.time())}",
            name="Agent Failure Recovery",
            description="Recover from failed agent instances",
            intervention_type=InterventionType.AGENT_FAILURE,
            priority=InterventionPriority.CRITICAL,
            scope=InterventionScope.SUBSYSTEM_SPECIFIC,
            triggers=[],
            actions=actions
        )

    def _create_communication_protocol(self) -> InterventionProtocol:
        """Create communication failure intervention protocol."""
        actions = [
            InterventionAction(
                action_type="reset_communication_channels",
                target="communication_system",
                parameters={"reset_type": "soft"}
            ),
            InterventionAction(
                action_type="switch_to_backup_channel",
                target="communication_system",
                parameters={"backup_channel": "inbox_fallback"}
            )
        ]

        return InterventionProtocol(
            protocol_id=f"comm_failure_{int(time.time())}",
            name="Communication Failure Recovery",
            description="Handle communication system failures",
            intervention_type=InterventionType.COMMUNICATION_FAILURE,
            priority=InterventionPriority.HIGH,
            scope=InterventionScope.SYSTEM_WIDE,
            triggers=[],
            actions=actions
        )

    def _execute_action(self, action: InterventionAction, context: Dict[str, Any]):
        """Execute a specific intervention action."""
        if action.action_type == "scale_resources":
            self._scale_resources(action.parameters)
        elif action.action_type == "notify_admin":
            self._notify_admin(action.parameters)
        elif action.action_type == "restart_agent":
            self._restart_agent(action.parameters)
        elif action.action_type == "reset_communication_channels":
            self._reset_communication(action.parameters)
        elif action.action_type == "switch_to_backup_channel":
            self._switch_backup_channel(action.parameters)
        else:
            raise ValueError(f"Unknown action type: {action.action_type}")

    def _collect_system_metrics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Collect current system metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": context.get("system_health", {}),
            "agent_status": context.get("agent_status", {}),
            "communication_status": context.get("communication_status", {})
        }

    def _scale_resources(self, params: Dict[str, Any]):
        """Scale system resources."""
        resource_type = params.get("resource_type")
        scale_factor = params.get("scale_factor", 1.1)
        self.logger.info(f"Scaling {resource_type} resources by factor {scale_factor}")

    def _notify_admin(self, params: Dict[str, Any]):
        """Notify system administrator."""
        message = params.get("message", "System intervention triggered")
        self.logger.warning(f"ADMIN NOTIFICATION: {message}")

    def _restart_agent(self, params: Dict[str, Any]):
        """Restart a failed agent."""
        agent_id = params.get("agent_id")
        restart_type = params.get("restart_type", "hard")
        self.logger.info(f"Restarting agent {agent_id} with {restart_type} restart")

    def _reset_communication(self, params: Dict[str, Any]):
        """Reset communication channels."""
        reset_type = params.get("reset_type", "soft")
        self.logger.info(f"Resetting communication channels with {reset_type} reset")

    def _switch_backup_channel(self, params: Dict[str, Any]):
        """Switch to backup communication channel."""
        backup_channel = params.get("backup_channel", "inbox")
        self.logger.info(f"Switching to backup communication channel: {backup_channel}")


class InterventionManager:
    """Intervention Manager - Intent-Oriented Subsystem for emergency intervention handling."""

    def __init__(self, strategy: Optional[InterventionStrategy] = None):
        self.logger = logging.getLogger(__name__)
        self.strategy = strategy or SwarmInterventionStrategy()

        # Intervention tracking
        self.active_interventions: Dict[str, InterventionResult] = {}
        self.intervention_history: List[InterventionResult] = []
        self.protocol_registry: Dict[str, InterventionProtocol] = {}

        # Cooldown tracking
        self.last_execution_times: Dict[str, datetime] = {}
        self.execution_counts: Dict[str, int] = {}

        # Monitoring thread
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None

    def register_protocol(self, protocol: InterventionProtocol):
        """Register an intervention protocol."""
        self.protocol_registry[protocol.protocol_id] = protocol
        self.logger.info(f"Registered intervention protocol: {protocol.name}")

    def start_monitoring(self, context_provider: Callable[[], Dict[str, Any]]):
        """Start continuous monitoring for intervention triggers."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(context_provider,),
            daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info("Intervention monitoring started")

    def stop_monitoring(self):
        """Stop monitoring for intervention triggers."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("Intervention monitoring stopped")

    def trigger_intervention(self, protocol_id: str, context: Dict[str, Any]) -> Optional[str]:
        """Manually trigger an intervention."""
        if protocol_id not in self.protocol_registry:
            self.logger.error(f"Unknown intervention protocol: {protocol_id}")
            return None

        protocol = self.protocol_registry[protocol_id]

        # Check cooldown
        if not self._check_cooldown(protocol):
            self.logger.warning(f"Intervention {protocol_id} in cooldown period")
            return None

        # Check execution limits
        if not self._check_execution_limits(protocol):
            self.logger.warning(f"Intervention {protocol_id} exceeded execution limits")
            return None

        # Execute intervention
        result = self.strategy.execute_intervention(protocol, context)
        intervention_id = result.intervention_id

        self.active_interventions[intervention_id] = result
        self.intervention_history.append(result)
        self.last_execution_times[protocol_id] = datetime.now()
        self.execution_counts[protocol_id] = self.execution_counts.get(protocol_id, 0) + 1

        # Validate effectiveness
        if self.strategy.validate_intervention_effectiveness(result):
            self.logger.info(f"Intervention {intervention_id} was effective")
        else:
            self.logger.warning(f"Intervention {intervention_id} may not have been effective")

        return intervention_id

    def detect_and_trigger(self, context: Dict[str, Any]) -> Optional[str]:
        """Automatically detect and trigger appropriate intervention."""
        protocol = self.strategy.detect_intervention_needed(context)
        if protocol:
            # Register if not already registered
            if protocol.protocol_id not in self.protocol_registry:
                self.register_protocol(protocol)

            return self.trigger_intervention(protocol.protocol_id, context)

        return None

    def get_intervention_status(self, intervention_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific intervention."""
        result = self.active_interventions.get(intervention_id)
        if not result:
            # Check history
            for historical in self.intervention_history:
                if historical.intervention_id == intervention_id:
                    result = historical
                    break

        if not result:
            return None

        return {
            "intervention_id": result.intervention_id,
            "status": result.status.value,
            "actions_executed": result.actions_executed,
            "execution_time": result.execution_time,
            "errors": result.errors,
            "metrics_before": result.metrics_before,
            "metrics_after": result.metrics_after,
            "timestamp": result.timestamp.isoformat()
        }

    def get_intervention_stats(self) -> Dict[str, Any]:
        """Get intervention statistics."""
        stats = {
            "total_interventions": len(self.intervention_history),
            "active_interventions": len(self.active_interventions),
            "successful_interventions": 0,
            "failed_interventions": 0,
            "by_type": {},
            "by_priority": {},
            "recent_activity": []
        }

        for result in self.intervention_history[-20:]:  # Last 20 interventions
            if result.status == InterventionStatus.MITIGATED:
                stats["successful_interventions"] += 1
            elif result.status == InterventionStatus.FAILED:
                stats["failed_interventions"] += 1

            # Count by type (would need to track protocol types)
            stats["recent_activity"].append({
                "id": result.intervention_id,
                "status": result.status.value,
                "timestamp": result.timestamp.isoformat(),
                "actions": len(result.actions_executed)
            })

        return stats

    def _monitoring_loop(self, context_provider: Callable[[], Dict[str, Any]]):
        """Continuous monitoring loop for intervention triggers."""
        while self.monitoring_active:
            try:
                context = context_provider()
                intervention_id = self.detect_and_trigger(context)

                if intervention_id:
                    self.logger.info(f"Automatic intervention triggered: {intervention_id}")

            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")

            time.sleep(30)  # Check every 30 seconds

    def _check_cooldown(self, protocol: InterventionProtocol) -> bool:
        """Check if protocol is in cooldown period."""
        last_execution = self.last_execution_times.get(protocol.protocol_id)
        if not last_execution:
            return True

        cooldown_end = last_execution + timedelta(seconds=protocol.cooldown_period)
        return datetime.now() >= cooldown_end

    def _check_execution_limits(self, protocol: InterventionProtocol) -> bool:
        """Check if protocol has exceeded execution limits."""
        current_count = self.execution_counts.get(protocol.protocol_id, 0)

        # Reset counter if it's been more than an hour
        last_execution = self.last_execution_times.get(protocol.protocol_id)
        if last_execution:
            hour_ago = datetime.now() - timedelta(hours=1)
            if last_execution < hour_ago:
                current_count = 0
                self.execution_counts[protocol.protocol_id] = 0

        return current_count < protocol.max_executions_per_hour


class InterventionOrchestrationStep(Step):
    """Orchestration step for intervention operations."""

    def __init__(self, intervention_manager: InterventionManager, operation: str, **params):
        self.intervention_manager = intervention_manager
        self.operation = operation
        self.params = params

    def name(self) -> str:
        return f"intervention_{self.operation}"

    def run(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intervention operation."""
        try:
            if self.operation == "trigger":
                protocol_id = self.params.get("protocol_id")
                context = self.params.get("context", payload)
                if protocol_id:
                    intervention_id = self.intervention_manager.trigger_intervention(protocol_id, context)
                    payload["intervention_id"] = intervention_id

            elif self.operation == "detect":
                context = self.params.get("context", payload)
                intervention_id = self.intervention_manager.detect_and_trigger(context)
                payload["auto_intervention_id"] = intervention_id

            elif self.operation == "status":
                intervention_id = payload.get("intervention_id")
                if intervention_id:
                    status = self.intervention_manager.get_intervention_status(intervention_id)
                    payload["intervention_status"] = status

            elif self.operation == "stats":
                stats = self.intervention_manager.get_intervention_stats()
                payload["intervention_stats"] = stats

            ctx.logger(f"Intervention operation completed: {self.operation}")
            return payload

        except Exception as e:
            ctx.logger(f"Intervention operation failed: {e}")
            payload["intervention_error"] = str(e)
            return payload


# Factory function for creating InterventionManager instances
def create_intervention_manager(strategy: Optional[InterventionStrategy] = None) -> InterventionManager:
    """Factory function for InterventionManager creation."""
    return InterventionManager(strategy=strategy)


__all__ = [
    "InterventionManager",
    "InterventionProtocol",
    "InterventionResult",
    "InterventionPriority",
    "InterventionType",
    "InterventionStatus",
    "InterventionScope",
    "InterventionTrigger",
    "InterventionAction",
    "InterventionStrategy",
    "SwarmInterventionStrategy",
    "InterventionOrchestrationStep",
    "create_intervention_manager"
]
