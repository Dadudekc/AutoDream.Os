"""
Agent Assignment Manager - V2 Compliance Module
==============================================

Manages agent-to-principle assignments following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

import json
import os

from .architectural_models import ArchitecturalPrinciple


class AgentAssignmentManager:
    """Manages agent-to-principle assignments with persistence."""

    def __init__(self, config_path: str = "src/config/architectural_assignments.json"):

EXAMPLE USAGE:
==============

# Import the service
from src.services.agent_assignment_manager import Agent_Assignment_ManagerService

# Initialize service
service = Agent_Assignment_ManagerService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Agent_Assignment_ManagerService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Initialize assignment manager."""
        self.config_path = config_path
        self.assignments: dict[str, ArchitecturalPrinciple] = {}
        self._load_assignments()

    def _load_assignments(self) -> None:
        """Load agent assignments from configuration."""
        # Default assignments
        default_assignments = {
            "Agent-1": ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
            "Agent-2": ArchitecturalPrinciple.OPEN_CLOSED,
            "Agent-3": ArchitecturalPrinciple.LISKOV_SUBSTITUTION,
            "Agent-4": ArchitecturalPrinciple.INTERFACE_SEGREGATION,
            "Agent-5": ArchitecturalPrinciple.DEPENDENCY_INVERSION,
            "Agent-6": ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH,
            "Agent-7": ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
            "Agent-8": ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
        }

        self.assignments = default_assignments.copy()

        # Try to load from configuration file
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    config = json.load(f)
                    # Convert string principles back to enum
                    for agent, principle_str in config.items():
                        principle = ArchitecturalPrinciple(principle_str)
                        self.assignments[agent] = principle
            except Exception:
                # Use defaults if config loading fails
                pass

    def get_agent_principle(self, agent_id: str) -> ArchitecturalPrinciple | None:
        """Get the architectural principle assigned to an agent."""
        return self.assignments.get(agent_id)

    def assign_principle(self, agent_id: str, principle: ArchitecturalPrinciple) -> None:
        """Assign a principle to an agent."""
        self.assignments[agent_id] = principle
        self._save_assignments()

    def _save_assignments(self) -> None:
        """Save assignments to configuration file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            # Convert enum values to strings for JSON serialization
            config = {agent: principle.value for agent, principle in self.assignments.items()}
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception:
            # Silently fail if saving fails
            pass

    def get_all_assignments(self) -> dict[str, ArchitecturalPrinciple]:
        """Get all agent assignments."""
        return self.assignments.copy()

    def get_agents_by_principle(self, principle: ArchitecturalPrinciple) -> list[str]:
        """Get all agents assigned to a specific principle."""
        return [
            agent
            for agent, assigned_principle in self.assignments.items()
            if assigned_principle == principle
        ]
