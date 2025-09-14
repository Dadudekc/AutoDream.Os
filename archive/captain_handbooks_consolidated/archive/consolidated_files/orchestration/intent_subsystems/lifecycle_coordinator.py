#!/usr/bin/env python3
"""
Lifecycle Coordinator - Intent-Oriented Subsystem
=================================================

Decomposed from SwarmOrchestrator to handle standardized agent lifecycle management.
Enforces observe→debate→act contract interface with clear separation of concerns.

Author: Swarm Representative (Following Commander Thea directives)
Mission: Orchestration Layer Decomposition - Intent Subsystem Creation
License: MIT
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol

from ..contracts import OrchestrationContext, Step


class LifecyclePhase(Enum):
    """Agent lifecycle phases."""

    INITIALIZING = "initializing"
    OBSERVING = "observing"
    ANALYZING = "analyzing"
    DEBATING = "debating"
    DECIDING = "deciding"
    ACTING = "acting"
    REFLECTING = "reflecting"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class LifecycleStatus(Enum):
    """Agent lifecycle status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    TERMINATED = "terminated"


class AgentCapability(Enum):
    """Standard agent capabilities."""

    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    COORDINATION = "coordination"
    EXECUTION = "execution"
    LEARNING = "learning"
    ADAPTATION = "adaptation"


@dataclass
class AgentState:
    """Agent state representation."""

    agent_id: str
    current_phase: LifecyclePhase = LifecyclePhase.INITIALIZING
    status: LifecycleStatus = LifecycleStatus.ACTIVE
    capabilities: list[AgentCapability] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    actions_taken: list[dict[str, Any]] = field(default_factory=list)
    performance_metrics: dict[str, float] = field(default_factory=dict)
    last_activity: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LifecycleTransition:
    """Lifecycle transition record."""

    transition_id: str
    agent_id: str
    from_phase: LifecyclePhase
    to_phase: LifecyclePhase
    trigger: str
    context: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error_message: str | None = None


class SwarmAgent(Protocol):
    """Standardized Swarm Agent interface with observe→debate→act contract."""

    @property
    def agent_id(self) -> str: ...

    @property
    def capabilities(self) -> list[AgentCapability]: ...

    def observe(self, context: dict[str, Any]) -> dict[str, Any]:
        """Phase 1: Observation - Gather information from environment."""
        ...

    def analyze(self, observations: dict[str, Any]) -> dict[str, Any]:
        """Phase 2: Analysis - Process and analyze observations."""
        ...

    def debate(self, analysis: dict[str, Any], peer_inputs: list[dict[str, Any]]) -> dict[str, Any]:
        """Phase 3: Debate - Participate in swarm decision-making."""
        ...

    def decide(self, debate_results: dict[str, Any]) -> dict[str, Any]:
        """Phase 4: Decision - Make final determination."""
        ...

    def act(self, decision: dict[str, Any]) -> dict[str, Any]:
        """Phase 5: Action - Execute the decision."""
        ...

    def reflect(self, action_results: dict[str, Any]) -> dict[str, Any]:
        """Phase 6: Reflection - Learn from action outcomes."""
        ...

    def get_status(self) -> dict[str, Any]:
        """Get current agent status."""
        ...


class LifecycleStrategy(Protocol):
    """Strategy pattern for lifecycle management."""

    def should_transition(
        self, agent: SwarmAgent, current_state: AgentState, context: dict[str, Any]
    ) -> LifecyclePhase | None: ...

    def validate_transition(
        self, agent: SwarmAgent, from_phase: LifecyclePhase, to_phase: LifecyclePhase
    ) -> bool: ...

    def handle_transition_error(
        self, agent: SwarmAgent, transition: LifecycleTransition
    ) -> None: ...


class SwarmLifecycleStrategy:
    """Swarm-optimized lifecycle strategy."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Phase transition rules
        self.transition_rules = {
            LifecyclePhase.INITIALIZING: [LifecyclePhase.OBSERVING],
            LifecyclePhase.OBSERVING: [LifecyclePhase.ANALYZING, LifecyclePhase.ERROR],
            LifecyclePhase.ANALYZING: [
                LifecyclePhase.DEBATING,
                LifecyclePhase.OBSERVING,
                LifecyclePhase.ERROR,
            ],
            LifecyclePhase.DEBATING: [
                LifecyclePhase.DECIDING,
                LifecyclePhase.ANALYZING,
                LifecyclePhase.ERROR,
            ],
            LifecyclePhase.DECIDING: [
                LifecyclePhase.ACTING,
                LifecyclePhase.DEBATING,
                LifecyclePhase.ERROR,
            ],
            LifecyclePhase.ACTING: [LifecyclePhase.REFLECTING, LifecyclePhase.ERROR],
            LifecyclePhase.REFLECTING: [
                LifecyclePhase.OBSERVING,
                LifecyclePhase.MAINTENANCE,
                LifecyclePhase.ERROR,
            ],
            LifecyclePhase.MAINTENANCE: [LifecyclePhase.OBSERVING, LifecyclePhase.ERROR],
            LifecyclePhase.ERROR: [LifecyclePhase.INITIALIZING, LifecyclePhase.SHUTDOWN],
            LifecyclePhase.SHUTDOWN: [],
        }

        # Phase timeouts (seconds)
        self.phase_timeouts = {
            LifecyclePhase.OBSERVING: 300,  # 5 minutes
            LifecyclePhase.ANALYZING: 600,  # 10 minutes
            LifecyclePhase.DEBATING: 1800,  # 30 minutes
            LifecyclePhase.DECIDING: 300,  # 5 minutes
            LifecyclePhase.ACTING: 900,  # 15 minutes
            LifecyclePhase.REFLECTING: 300,  # 5 minutes
        }

    def should_transition(
        self, agent: SwarmAgent, current_state: AgentState, context: dict[str, Any]
    ) -> LifecyclePhase | None:
        """Determine if agent should transition to next phase."""
        current_phase = current_state.current_phase

        # Check for phase timeout
        if current_phase in self.phase_timeouts:
            timeout = self.phase_timeouts[current_phase]
            if (datetime.now() - current_state.last_activity).total_seconds() > timeout:
                return LifecyclePhase.ERROR

        # Phase-specific transition logic
        if current_phase == LifecyclePhase.OBSERVING:
            # Transition to analysis if we have sufficient observations
            if len(current_state.observations) >= 3:
                return LifecyclePhase.ANALYZING

        elif current_phase == LifecyclePhase.ANALYZING:
            # Transition to debate if analysis is complete
            if "analysis_complete" in current_state.context:
                return LifecyclePhase.DEBATING

        elif current_phase == LifecyclePhase.DEBATING:
            # Transition to decision if debate period ended
            debate_end = current_state.context.get("debate_deadline")
            if debate_end and datetime.now() > debate_end:
                return LifecyclePhase.DECIDING

        elif current_phase == LifecyclePhase.DECIDING:
            # Transition to action if decision made
            if "decision_made" in current_state.context:
                return LifecyclePhase.ACTING

        elif current_phase == LifecyclePhase.ACTING:
            # Transition to reflection if action completed
            if "action_complete" in current_state.context:
                return LifecyclePhase.REFLECTING

        elif current_phase == LifecyclePhase.REFLECTING:
            # Transition back to observing for next cycle
            if "reflection_complete" in current_state.context:
                return LifecyclePhase.OBSERVING

        return None

    def validate_transition(
        self, agent: SwarmAgent, from_phase: LifecyclePhase, to_phase: LifecyclePhase
    ) -> bool:
        """Validate if a transition is allowed."""
        allowed_transitions = self.transition_rules.get(from_phase, [])
        return to_phase in allowed_transitions

    def handle_transition_error(self, agent: SwarmAgent, transition: LifecycleTransition) -> None:
        """Handle transition errors."""
        self.logger.error(
            f"Transition error for {agent.agent_id}: {transition.from_phase.value} → {transition.to_phase.value}"
        )
        self.logger.error(f"Error: {transition.error_message}")


class LifecycleCoordinator:
    """Lifecycle Coordinator - Intent-Oriented Subsystem for agent lifecycle management."""

    def __init__(self, strategy: LifecycleStrategy | None = None):
        self.logger = logging.getLogger(__name__)
        self.strategy = strategy or SwarmLifecycleStrategy()

        # Agent registry
        self.registered_agents: dict[str, SwarmAgent] = {}
        self.agent_states: dict[str, AgentState] = {}
        self.lifecycle_history: list[LifecycleTransition] = []

        # Coordination settings
        self.coordination_cycle_seconds = 60  # Check every minute
        self.max_agents_per_cycle = 50

        # Monitoring
        self.monitoring_active = False
        self.monitoring_thread: threading.Thread | None = None

    def register_agent(self, agent: SwarmAgent) -> bool:
        """Register an agent with the lifecycle coordinator."""
        agent_id = agent.agent_id

        if agent_id in self.registered_agents:
            self.logger.warning(f"Agent {agent_id} already registered")
            return False

        # Create initial state
        initial_state = AgentState(agent_id=agent_id, capabilities=agent.capabilities.copy())

        self.registered_agents[agent_id] = agent
        self.agent_states[agent_id] = initial_state

        self.logger.info(
            f"Registered agent: {agent_id} with capabilities: {[c.value for c in agent.capabilities]}"
        )
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id not in self.registered_agents:
            return False

        # Record shutdown transition
        state = self.agent_states[agent_id]
        transition = LifecycleTransition(
            transition_id=str(uuid.uuid4()),
            agent_id=agent_id,
            from_phase=state.current_phase,
            to_phase=LifecyclePhase.SHUTDOWN,
            trigger="unregistration",
            context={"reason": "unregistered"},
        )
        self.lifecycle_history.append(transition)

        del self.registered_agents[agent_id]
        del self.agent_states[agent_id]

        self.logger.info(f"Unregistered agent: {agent_id}")
        return True

    def start_coordination(self):
        """Start the lifecycle coordination process."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._coordination_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("Lifecycle coordination started")

    def stop_coordination(self):
        """Stop the lifecycle coordination process."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        self.logger.info("Lifecycle coordination stopped")

    def execute_lifecycle_cycle(
        self, agent_id: str, context: dict[str, Any]
    ) -> LifecycleTransition | None:
        """Execute a complete lifecycle cycle for an agent."""
        if agent_id not in self.registered_agents:
            return None

        agent = self.registered_agents[agent_id]
        state = self.agent_states[agent_id]
        original_phase = state.current_phase

        try:
            # Execute current phase
            result = self._execute_phase(agent, state, context)

            # Store results in state
            if state.current_phase == LifecyclePhase.OBSERVING:
                state.observations.append(result)
            elif state.current_phase == LifecyclePhase.ANALYZING:
                state.context["analysis_result"] = result
            elif state.current_phase == LifecyclePhase.DEBATING:
                state.context["debate_result"] = result
            elif state.current_phase == LifecyclePhase.DECIDING:
                state.decisions.append(result)
                state.context["decision_made"] = True
            elif state.current_phase == LifecyclePhase.ACTING:
                state.actions_taken.append(result)
                state.context["action_complete"] = True
            elif state.current_phase == LifecyclePhase.REFLECTING:
                state.context["reflection_result"] = result
                state.context["reflection_complete"] = True

            # Check for transition
            next_phase = self.strategy.should_transition(agent, state, context)
            if next_phase and next_phase != state.current_phase:
                return self._transition_agent(agent, state, next_phase, "cycle_completion", context)

            return None

        except Exception as e:
            self.logger.error(f"Error in lifecycle cycle for {agent_id}: {e}")
            return self._transition_agent(
                agent, state, LifecyclePhase.ERROR, "cycle_error", context
            )

    def force_transition(
        self, agent_id: str, to_phase: LifecyclePhase, trigger: str, context: dict[str, Any]
    ) -> LifecycleTransition | None:
        """Force an agent to transition to a specific phase."""
        if agent_id not in self.registered_agents:
            return None

        agent = self.registered_agents[agent_id]
        state = self.agent_states[agent_id]

        return self._transition_agent(agent, state, to_phase, trigger, context)

    def get_agent_status(self, agent_id: str) -> dict[str, Any] | None:
        """Get comprehensive status for an agent."""
        if agent_id not in self.registered_agents:
            return None

        agent = self.registered_agents[agent_id]
        state = self.agent_states[agent_id]

        return {
            "agent_id": agent_id,
            "capabilities": [c.value for c in agent.capabilities],
            "current_phase": state.current_phase.value,
            "status": state.status.value,
            "observations_count": len(state.observations),
            "decisions_count": len(state.decisions),
            "actions_count": len(state.actions_taken),
            "performance_metrics": state.performance_metrics,
            "last_activity": state.last_activity.isoformat(),
            "context_summary": {
                k: v
                for k, v in state.context.items()
                if not isinstance(v, (list, dict)) or len(str(v)) < 100
            },
        }

    def get_coordination_stats(self) -> dict[str, Any]:
        """Get coordination statistics."""
        stats = {
            "total_agents": len(self.registered_agents),
            "active_agents": 0,
            "agents_by_phase": {},
            "agents_by_status": {},
            "total_transitions": len(self.lifecycle_history),
            "recent_transitions": [],
        }

        for agent_id, state in self.agent_states.items():
            if state.status == LifecycleStatus.ACTIVE:
                stats["active_agents"] += 1

            # Count by phase
            phase = state.current_phase.value
            stats["agents_by_phase"][phase] = stats["agents_by_phase"].get(phase, 0) + 1

            # Count by status
            status = state.status.value
            stats["agents_by_status"][status] = stats["agents_by_status"].get(status, 0) + 1

        # Recent transitions
        for transition in self.lifecycle_history[-20:]:
            stats["recent_transitions"].append(
                {
                    "agent_id": transition.agent_id,
                    "transition": f"{transition.from_phase.value} → {transition.to_phase.value}",
                    "trigger": transition.trigger,
                    "timestamp": transition.timestamp.isoformat(),
                    "success": transition.success,
                }
            )

        return stats

    def _execute_phase(
        self, agent: SwarmAgent, state: AgentState, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute the current phase for an agent."""
        phase = state.current_phase

        if phase == LifecyclePhase.OBSERVING:
            return agent.observe(context)
        elif phase == LifecyclePhase.ANALYZING:
            observations = {"observations": state.observations[-5:]}  # Last 5 observations
            return agent.analyze(observations)
        elif phase == LifecyclePhase.DEBATING:
            analysis = state.context.get("analysis_result", {})
            peer_inputs = []  # Would be populated from other agents
            return agent.debate(analysis, peer_inputs)
        elif phase == LifecyclePhase.DECIDING:
            debate_results = state.context.get("debate_result", {})
            return agent.decide(debate_results)
        elif phase == LifecyclePhase.ACTING:
            decision = state.decisions[-1] if state.decisions else {}
            return agent.act(decision)
        elif phase == LifecyclePhase.REFLECTING:
            action_results = state.actions_taken[-1] if state.actions_taken else {}
            return agent.reflect(action_results)
        else:
            return {"status": "idle", "phase": phase.value}

    def _transition_agent(
        self,
        agent: SwarmAgent,
        state: AgentState,
        to_phase: LifecyclePhase,
        trigger: str,
        context: dict[str, Any],
    ) -> LifecycleTransition:
        """Transition an agent to a new phase."""
        from_phase = state.current_phase

        # Validate transition
        if not self.strategy.validate_transition(agent, from_phase, to_phase):
            error_msg = f"Invalid transition: {from_phase.value} → {to_phase.value}"
            self.logger.error(error_msg)

            transition = LifecycleTransition(
                transition_id=str(uuid.uuid4()),
                agent_id=agent.agent_id,
                from_phase=from_phase,
                to_phase=to_phase,
                trigger=trigger,
                context=context,
                success=False,
                error_message=error_msg,
            )
            self.lifecycle_history.append(transition)
            return transition

        # Execute transition
        try:
            state.current_phase = to_phase
            state.last_activity = datetime.now()

            transition = LifecycleTransition(
                transition_id=str(uuid.uuid4()),
                agent_id=agent.agent_id,
                from_phase=from_phase,
                to_phase=to_phase,
                trigger=trigger,
                context=context,
                success=True,
            )

            self.lifecycle_history.append(transition)
            self.logger.info(
                f"Agent {agent.agent_id} transitioned: {from_phase.value} → {to_phase.value}"
            )

            return transition

        except Exception as e:
            error_msg = f"Transition execution failed: {e}"
            self.logger.error(error_msg)

            transition = LifecycleTransition(
                transition_id=str(uuid.uuid4()),
                agent_id=agent.agent_id,
                from_phase=from_phase,
                to_phase=to_phase,
                trigger=trigger,
                context=context,
                success=False,
                error_message=error_msg,
            )

            self.lifecycle_history.append(transition)
            self.strategy.handle_transition_error(agent, transition)
            return transition

    def _coordination_loop(self):
        """Main coordination loop."""
        while self.monitoring_active:
            try:
                # Process agents in batches
                agent_ids = list(self.registered_agents.keys())
                for i in range(0, len(agent_ids), self.max_agents_per_cycle):
                    batch = agent_ids[i : i + self.max_agents_per_cycle]

                    for agent_id in batch:
                        try:
                            # Create context for this cycle
                            context = {
                                "coordination_cycle": datetime.now().isoformat(),
                                "active_agents": len(self.registered_agents),
                                "system_status": "operational",
                            }

                            # Execute lifecycle cycle
                            transition = self.execute_lifecycle_cycle(agent_id, context)
                            if transition:
                                self.logger.debug(
                                    f"Transition: {agent_id} {transition.from_phase.value} → {transition.to_phase.value}"
                                )

                        except Exception as e:
                            self.logger.error(f"Error coordinating {agent_id}: {e}")

                    # Brief pause between batches
                    time.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Coordination loop error: {e}")

            # Wait for next cycle
            time.sleep(self.coordination_cycle_seconds)


class LifecycleOrchestrationStep(Step):
    """Orchestration step for lifecycle operations."""

    def __init__(self, lifecycle_coordinator: LifecycleCoordinator, operation: str, **params):
        self.lifecycle_coordinator = lifecycle_coordinator
        self.operation = operation
        self.params = params

    def name(self) -> str:
        return f"lifecycle_{self.operation}"

    def run(self, ctx: OrchestrationContext, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute lifecycle operation."""
        try:
            if self.operation == "register":
                agent = self.params.get("agent")
                if agent:
                    success = self.lifecycle_coordinator.register_agent(agent)
                    payload["registration_success"] = success

            elif self.operation == "execute_cycle":
                agent_id = self.params.get("agent_id")
                context = self.params.get("context", payload)
                if agent_id:
                    transition = self.lifecycle_coordinator.execute_lifecycle_cycle(
                        agent_id, context
                    )
                    payload["lifecycle_transition"] = transition

            elif self.operation == "force_transition":
                agent_id = self.params.get("agent_id")
                to_phase = self.params.get("to_phase")
                trigger = self.params.get("trigger", "forced")
                context = self.params.get("context", payload)
                if agent_id and to_phase:
                    transition = self.lifecycle_coordinator.force_transition(
                        agent_id, to_phase, trigger, context
                    )
                    payload["forced_transition"] = transition

            elif self.operation == "status":
                agent_id = self.params.get("agent_id")
                if agent_id:
                    status = self.lifecycle_coordinator.get_agent_status(agent_id)
                    payload["agent_status"] = status

            elif self.operation == "stats":
                stats = self.lifecycle_coordinator.get_coordination_stats()
                payload["coordination_stats"] = stats

            ctx.logger(f"Lifecycle operation completed: {self.operation}")
            return payload

        except Exception as e:
            ctx.logger(f"Lifecycle operation failed: {e}")
            payload["lifecycle_error"] = str(e)
            return payload


# Factory function for creating LifecycleCoordinator instances
def create_lifecycle_coordinator(strategy: LifecycleStrategy | None = None) -> LifecycleCoordinator:
    """Factory function for LifecycleCoordinator creation."""
    return LifecycleCoordinator(strategy=strategy)


__all__ = [
    "LifecycleCoordinator",
    "SwarmAgent",
    "AgentState",
    "LifecycleTransition",
    "LifecyclePhase",
    "LifecycleStatus",
    "AgentCapability",
    "LifecycleStrategy",
    "SwarmLifecycleStrategy",
    "LifecycleOrchestrationStep",
    "create_lifecycle_coordinator",
]
