#!/usr/bin/env python3
"""
Coordination Service Module
==========================

Handles coordination and state management including:
- FSM (Finite State Machine) management
- Persistent state management
- Coordinate management
- Contract management

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from .onboarding_coordinator import AgentContract, AgentState, ContractType

logger = logging.getLogger(__name__)


class AgentFSM:
    """Finite State Machine for agent state management."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = AgentState.UNINITIALIZED
        self.previous_state = None
        self.state_history = []
        self.transition_count = 0

    def transition_to(self, new_state: AgentState):
        """Transition to a new state."""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_history.append(
                {
                    "timestamp": datetime.now(),
                    "from": self.previous_state.value if self.previous_state else None,
                    "to": new_state.value,
                }
            )
            self.transition_count += 1
            logger.info(
                f"🔄 {self.agent_id} FSM: {self.previous_state.value if self.previous_state else 'None'} → {new_state.value}"
            )

    def get_state_info(self):
        """Get current state information."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transition_count": self.transition_count,
            "state_history_count": len(self.state_history),
        }


class CoordinationService:
    """Service for coordination and state management."""

    def __init__(self):
        self.coordinates_file = Path("cursor_agent_coords.json")
        self.agent_coordinates = self.load_coordinates()
        self.agent_fsms = {}
        self.contracts = {}
        self.persistent_state_file = Path("agent_workspaces/persistent_state.json")
        self.swarm_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]

        # Initialize FSM for all agents
        for agent_id in self.swarm_agents:
            self.agent_fsms[agent_id] = AgentFSM(agent_id)

        # Load persistent state
        self.load_persistent_state()

    def load_persistent_state(self):
        """Load persistent state from file."""
        try:
            if self.persistent_state_file.exists():
                with open(self.persistent_state_file) as f:
                    state_data = json.load(f)
                    # Restore FSM states
                    for agent_id, fsm_data in state_data.get("fsms", {}).items():
                        if agent_id in self.agent_fsms:
                            fsm = self.agent_fsms[agent_id]
                            fsm.current_state = AgentState(fsm_data["current_state"])
                            fsm.transition_count = fsm_data["transition_count"]
                            # Restore state history if available
                            if "state_history" in fsm_data:
                                fsm.state_history = fsm_data["state_history"]
                    # Restore contracts
                    for contract_data in state_data.get("contracts", []):
                        contract = AgentContract(
                            contract_data["agent_id"],
                            ContractType(contract_data["contract_type"]),
                            contract_data["description"],
                            contract_data["estimated_cycles"],
                            contract_data["dependencies"],
                        )
                        contract.status = contract_data["status"]
                        contract.progress_percentage = contract_data["progress_percentage"]
                        if "created_at" in contract_data:
                            contract.created_at = datetime.fromisoformat(
                                contract_data["created_at"]
                            )
                        self.contracts[contract_data["agent_id"]] = contract
                logger.info("✅ Persistent state loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load persistent state: {e}")

    def save_persistent_state(self):
        """Save persistent state to file."""
        try:
            state_data = {
                "fsms": {
                    agent_id: fsm.get_state_info() for agent_id, fsm in self.agent_fsms.items()
                },
                "contracts": [contract.to_dict() for contract in self.contracts.values()],
                "timestamp": datetime.now().isoformat(),
            }
            self.persistent_state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.persistent_state_file, "w") as f:
                json.dump(state_data, f, indent=2)
            logger.info("✅ Persistent state saved successfully")
        except Exception as e:
            logger.error(f"❌ Failed to save persistent state: {e}")

    def load_coordinates(self) -> dict[str, dict]:
        """Load agent coordinates from file."""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file) as f:
                    return json.load(f)
            else:
                logger.warning(f"⚠️ Coordinates file not found: {self.coordinates_file}")
                return {}
        except Exception as e:
            logger.error(f"❌ Failed to load coordinates: {e}")
            return {}

    def get_chat_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get chat input coordinates for agent."""
        try:
            agent_data = self.agent_coordinates.get("agents", {}).get(agent_id)
            if agent_data and "chat_input_coordinates" in agent_data:
                coords = agent_data["chat_input_coordinates"]
                return (coords[0], coords[1])
            return None
        except Exception as e:
            logger.error(f"❌ Failed to get chat coordinates for {agent_id}: {e}")
            return None

    def get_onboarding_coordinates(self, agent_id: str) -> tuple[int, int] | None:
        """Get onboarding coordinates for agent."""
        # DEDUPLICATION: Consolidated function - using unified implementation
        from src.core.unified_onboarding_coordinates import get_onboarding_coordinates

        return get_onboarding_coordinates(agent_id)

    def create_contract(
        self,
        agent_id: str,
        contract_type: ContractType,
        description: str,
        estimated_cycles: int,
        dependencies: list[str] = None,
    ) -> AgentContract:
        """Create a new contract for an agent."""
        contract = AgentContract(
            agent_id, contract_type, description, estimated_cycles, dependencies
        )
        self.contracts[agent_id] = contract
        logger.info(f"📋 Contract created for {agent_id}: {contract_type.value}")
        return contract

    def get_contract(self, agent_id: str) -> AgentContract | None:
        """Get contract for an agent."""
        return self.contracts.get(agent_id)

    def update_contract_status(self, agent_id: str, status: str, progress: int = None):
        """Update contract status and progress."""
        contract = self.contracts.get(agent_id)
        if contract:
            contract.status = status
            if progress is not None:
                contract.progress_percentage = progress
            logger.info(f"📋 Contract updated for {agent_id}: {status} ({progress}%)")

    def get_agent_fsm(self, agent_id: str) -> AgentFSM | None:
        """Get FSM for an agent."""
        return self.agent_fsms.get(agent_id)

    def transition_agent_state(self, agent_id: str, new_state: AgentState):
        """Transition agent to new state."""
        fsm = self.agent_fsms.get(agent_id)
        if fsm:
            fsm.transition_to(new_state)
            # Save state after transition
            self.save_persistent_state()
        else:
            logger.error(f"❌ No FSM found for agent {agent_id}")

    def get_agent_state(self, agent_id: str) -> AgentState | None:
        """Get current state of an agent."""
        fsm = self.agent_fsms.get(agent_id)
        return fsm.current_state if fsm else None

    def get_all_agent_states(self) -> dict[str, str]:
        """Get current states of all agents."""
        return {agent_id: fsm.current_state.value for agent_id, fsm in self.agent_fsms.items()}

    def get_contract_status(self) -> dict[str, dict]:
        """Get status of all contracts."""
        return {agent_id: contract.to_dict() for agent_id, contract in self.contracts.items()}

    def is_agent_onboarded(self, agent_id: str) -> bool:
        """Check if agent is onboarded."""
        state = self.get_agent_state(agent_id)
        return state is not None and state != AgentState.UNINITIALIZED

    def get_onboarded_agents(self) -> list[str]:
        """Get list of onboarded agents."""
        return [agent_id for agent_id in self.swarm_agents if self.is_agent_onboarded(agent_id)]

    def get_agent_coordinates_summary(self) -> dict[str, dict]:
        """Get summary of all agent coordinates."""
        summary = {}
        for agent_id in self.swarm_agents:
            coords = self.get_chat_coordinates(agent_id)
            summary[agent_id] = {
                "coordinates": coords,
                "has_coordinates": coords is not None,
                "state": (
                    self.get_agent_state(agent_id).value if self.get_agent_state(agent_id) else None
                ),
                "onboarded": self.is_agent_onboarded(agent_id),
            }
        return summary

    def validate_coordinates(self) -> dict[str, bool]:
        """Validate coordinates for all agents."""
        validation_results = {}
        for agent_id in self.swarm_agents:
            coords = self.get_chat_coordinates(agent_id)
            validation_results[agent_id] = coords is not None
        return validation_results

    def get_system_status(self) -> dict:
        """Get comprehensive system status."""
        return {
            "total_agents": len(self.swarm_agents),
            "onboarded_agents": len(self.get_onboarded_agents()),
            "active_contracts": len(self.contracts),
            "agent_states": self.get_all_agent_states(),
            "contract_status": self.get_contract_status(),
            "coordinates_validation": self.validate_coordinates(),
            "last_updated": datetime.now().isoformat(),
        }

    def cleanup_expired_contracts(self):
        """Clean up expired or completed contracts."""
        expired_contracts = []
        for agent_id, contract in self.contracts.items():
            if contract.status in ["completed", "expired", "cancelled"]:
                expired_contracts.append(agent_id)

        for agent_id in expired_contracts:
            del self.contracts[agent_id]
            logger.info(f"🧹 Cleaned up expired contract for {agent_id}")

        if expired_contracts:
            self.save_persistent_state()

    def reset_agent_state(self, agent_id: str):
        """Reset agent state to uninitialized."""
        if agent_id in self.agent_fsms:
            self.agent_fsms[agent_id] = AgentFSM(agent_id)
            if agent_id in self.contracts:
                del self.contracts[agent_id]
            self.save_persistent_state()
            logger.info(f"🔄 Reset state for {agent_id}")

    def get_agent_statistics(self) -> dict:
        """Get statistics about agent states and transitions."""
        stats = {
            "total_agents": len(self.swarm_agents),
            "state_distribution": {},
            "total_transitions": 0,
            "average_transitions": 0,
        }

        # Count state distribution
        for fsm in self.agent_fsms.values():
            state = fsm.current_state.value
            stats["state_distribution"][state] = stats["state_distribution"].get(state, 0) + 1
            stats["total_transitions"] += fsm.transition_count

        # Calculate average transitions
        if self.agent_fsms:
            stats["average_transitions"] = stats["total_transitions"] / len(self.agent_fsms)

        return stats
