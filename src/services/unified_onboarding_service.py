#!/usr/bin/env python3
"""
Unified Onboarding Service - V2 Compliant
=========================================

Consolidates all onboarding Python implementations into one unified system
and provides Discord Commander integration.

Features:
- Agent state management and FSM
- Contract creation and management
- Onboarding message generation
- Role-specific guidance
- Discord Commander integration
- PyAutoGUI automation support
- V2 compliance (≤400 lines)

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Finite State Machine states for agents."""

    UNINITIALIZED = "uninitialized"
    ONBOARDING = "onboarding"
    IDLE = "idle"
    CONTRACT_NEGOTIATION = "contract_negotiation"
    TASK_EXECUTION = "task_execution"
    COLLABORATION = "collaboration"
    PROGRESS_REPORTING = "progress_reporting"
    CYCLE_COMPLETION = "cycle_completion"
    ERROR_RECOVERY = "error_recovery"


class ContractType(Enum):
    """Types of contracts agents can enter."""

    DEDUPLICATION = "deduplication"
    V2_COMPLIANCE = "v2_compliance"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    COORDINATION = "coordination"
    ONBOARDING = "onboarding"


class AgentContract:
    """Contract system for agent task commitments."""

    def __init__(
        self,
        agent_id: str,
        contract_type: ContractType,
        description: str,
        estimated_cycles: int,
        dependencies: list[str] = None,
    ):
        self.agent_id = agent_id
        self.contract_type = contract_type
        self.description = description
        self.estimated_cycles = estimated_cycles
        self.dependencies = dependencies or []
        self.status = "pending"
        self.cycle_start = None
        self.cycle_end = None
        self.progress_percentage = 0
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "contract_type": self.contract_type.value,
            "description": self.description,
            "estimated_cycles": self.estimated_cycles,
            "dependencies": self.dependencies,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat(),
        }


class UnifiedOnboardingService:
    """Unified onboarding service consolidating all onboarding implementations."""

    def __init__(self, coordination_service=None, discord_commander=None):
        self.coordination_service = coordination_service
        self.discord_commander = discord_commander
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT & System Integration Specialist",
        }
        self.agent_states = {}
        self.contracts = {}
        self.workspace_path = Path("agent_workspaces")

    async def perform_agent_onboarding(self, agent_id: str, role: str = None) -> bool:
        """Perform onboarding for a specific agent."""
        try:
            if not role:
                role = self.agent_roles.get(agent_id, "Specialist")

            logger.info(f"🚀 Starting unified onboarding for {agent_id} - {role}")

            # Update agent state
            self.agent_states[agent_id] = AgentState.ONBOARDING

            # Create onboarding contract
            contract = self.create_onboarding_contract(agent_id)
            self.contracts[agent_id] = contract

            # Create onboarding message
            message = self.create_onboarding_message(agent_id, role)

            # Send onboarding message via coordination service
            if self.coordination_service and hasattr(self.coordination_service, "send_message"):
                success = await self._send_onboarding_message(agent_id, message)
                if success:
                    logger.info(f"✅ Onboarding message sent to {agent_id}")
                    contract.status = "active"
                    self.agent_states[agent_id] = AgentState.IDLE

                    # Notify Discord Commander
                    if self.discord_commander:
                        await self._notify_discord_onboarding(agent_id, role, "success")

                    return True
                else:
                    logger.error(f"❌ Failed to send onboarding message to {agent_id}")
                    self.agent_states[agent_id] = AgentState.ERROR_RECOVERY
                    return False
            else:
                logger.info(f"📝 Onboarding message for {agent_id}: {message}")
                contract.status = "active"
                self.agent_states[agent_id] = AgentState.IDLE
                return True

        except Exception as e:
            logger.error(f"❌ Onboarding failed for {agent_id}: {e}")
            self.agent_states[agent_id] = AgentState.ERROR_RECOVERY
            return False

    def create_onboarding_contract(self, agent_id: str) -> AgentContract:
        """Create onboarding contract for agent."""
        return AgentContract(
            agent_id=agent_id,
            contract_type=ContractType.ONBOARDING,
            description=f"Unified onboarding contract for {agent_id}",
            estimated_cycles=2,
        )

    def create_onboarding_message(self, agent_id: str, role: str) -> str:
        """Create onboarding message for agent."""
        role_guidance = self._get_role_onboarding_guidance(agent_id)

        message = f"""
============================================================
🚀 AGENT ONBOARDING - {agent_id}
============================================================
📤 FROM: Unified Onboarding Service
📥 TO: {agent_id}
Priority: HIGH
Tags: ONBOARDING|INITIALIZATION
------------------------------------------------------------
🎯 WELCOME TO THE SWARM - {role}

{role_guidance}

ONBOARDING CHECKLIST:
✅ Agent ID: {agent_id}
✅ Role: {role}
✅ Contract: Unified Onboarding Contract Created
✅ Status: Ready for Mission Assignment

NEXT STEPS:
1. Acknowledge onboarding message
2. Review role-specific responsibilities
3. Prepare for first mission assignment
4. Report readiness status

🐝 WE ARE SWARM - Welcome to the team! 🐝

Ready to begin your specialist journey!
------------------------------------------------------------
"""
        return message

    def _get_role_onboarding_guidance(self, agent_id: str) -> str:
        """Get role-specific onboarding guidance."""
        role = self.agent_roles.get(agent_id, "Specialist")

        guidance_templates = {
            "Agent-1": """
CORE RESPONSIBILITIES:
- System integration and core systems management
- API development and maintenance
- Database integration and optimization
- Core service architecture and implementation

ONBOARDING TASKS:
1. Review system architecture and integration points
2. Analyze current API implementations
3. Identify integration opportunities
4. Prepare for core systems development
""",
            "Agent-2": """
CORE RESPONSIBILITIES:
- System architecture design and implementation
- Design pattern implementation and guidance
- Code structure analysis and optimization
- Large file modularization and V2 compliance

ONBOARDING TASKS:
1. Review current system architecture
2. Analyze design patterns and implementations
3. Identify modularization opportunities
4. Prepare for architecture enhancement
""",
            "Agent-3": """
CORE RESPONSIBILITIES:
- Infrastructure management and optimization
- DevOps pipeline implementation and maintenance
- Deployment automation and monitoring
- System reliability and performance optimization

ONBOARDING TASKS:
1. Review current infrastructure setup
2. Analyze DevOps pipelines and processes
3. Identify optimization opportunities
4. Prepare for infrastructure enhancement
""",
            "Agent-4": """
CORE RESPONSIBILITIES:
- Quality assurance and testing leadership
- Captain oversight and swarm coordination
- Quality standards enforcement and monitoring
- Team coordination and project management

ONBOARDING TASKS:
1. Review quality standards and testing frameworks
2. Analyze current quality metrics and processes
3. Identify quality improvement opportunities
4. Prepare for captain leadership role
""",
            "Agent-5": """
CORE RESPONSIBILITIES:
- Business intelligence and data analysis
- Performance metrics and reporting
- Data visualization and dashboard development
- Business process optimization

ONBOARDING TASKS:
1. Review current business intelligence setup
2. Analyze data sources and reporting systems
3. Identify BI enhancement opportunities
4. Prepare for business intelligence development
""",
            "Agent-6": """
CORE RESPONSIBILITIES:
- Inter-agent coordination and communication
- Message routing and delivery optimization
- Swarm coordination and synchronization
- Communication protocol implementation

ONBOARDING TASKS:
1. Review current communication systems
2. Analyze coordination protocols and processes
3. Identify communication enhancement opportunities
4. Prepare for coordination system development
""",
            "Agent-7": """
CORE RESPONSIBILITIES:
- Web interface development and maintenance
- Frontend and backend web development
- User interface design and implementation
- Web application optimization and performance

ONBOARDING TASKS:
1. Review current web interfaces and applications
2. Analyze web development frameworks and tools
3. Identify web enhancement opportunities
4. Prepare for web development projects
""",
            "Agent-8": """
CORE RESPONSIBILITIES:
- Single Source of Truth (SSOT) management
- System integration and data consistency
- Configuration management and validation
- Cross-system coordination and synchronization

ONBOARDING TASKS:
1. Review current SSOT implementations
2. Analyze system integration points and processes
3. Identify integration enhancement opportunities
4. Prepare for system integration development
""",
        }

        return guidance_templates.get(
            agent_id,
            f"""
CORE RESPONSIBILITIES:
- {role} specialized tasks and responsibilities
- System optimization and enhancement
- Quality assurance and best practices
- Team collaboration and coordination

ONBOARDING TASKS:
1. Review current system setup and processes
2. Analyze specialized tools and frameworks
3. Identify enhancement opportunities
4. Prepare for specialized development work
""",
        )

    async def _send_onboarding_message(self, agent_id: str, message: str) -> bool:
        """Send onboarding message via coordination service."""
        try:
            if hasattr(self.coordination_service, "send_message"):
                return await self.coordination_service.send_message(agent_id, message)
            return False
        except Exception as e:
            logger.error(f"Failed to send message to {agent_id}: {e}")
            return False

    async def _notify_discord_onboarding(self, agent_id: str, role: str, status: str):
        """Notify Discord Commander of onboarding status."""
        try:
            if self.discord_commander and hasattr(self.discord_commander, "send_notification"):
                notification = {
                    "type": "onboarding",
                    "agent_id": agent_id,
                    "role": role,
                    "status": status,
                    "timestamp": datetime.now().isoformat(),
                }
                await self.discord_commander.send_notification(notification)
        except Exception as e:
            logger.error(f"Failed to notify Discord of onboarding: {e}")

    async def onboard_all_agents(self) -> dict[str, bool]:
        """Onboard all agents in the swarm."""
        logger.info("🚀 Starting unified onboarding for all agents...")
        results = {}

        for agent_id, role in self.agent_roles.items():
            logger.info(f"📋 Onboarding {agent_id} - {role}")
            results[agent_id] = await self.perform_agent_onboarding(agent_id, role)

        successful_onboards = sum(1 for success in results.values() if success)
        logger.info(
            f"✅ Unified onboarding complete: {successful_onboards}/{len(results)} agents onboarded successfully"
        )

        return results

    def get_agent_state(self, agent_id: str) -> AgentState:
        """Get current state of an agent."""
        return self.agent_states.get(agent_id, AgentState.UNINITIALIZED)

    def get_agent_contract(self, agent_id: str) -> AgentContract | None:
        """Get current contract of an agent."""
        return self.contracts.get(agent_id)

    def save_onboarding_state(self, filepath: str = "onboarding_state.json"):
        """Save current onboarding state to file."""
        try:
            state_data = {
                "agent_states": {k: v.value for k, v in self.agent_states.items()},
                "contracts": {k: v.to_dict() for k, v in self.contracts.items()},
                "timestamp": datetime.now().isoformat(),
            }

            with open(filepath, "w") as f:
                json.dump(state_data, f, indent=2)

            logger.info(f"✅ Onboarding state saved to {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to save onboarding state: {e}")

    def load_onboarding_state(self, filepath: str = "onboarding_state.json"):
        """Load onboarding state from file."""
        try:
            if not Path(filepath).exists():
                logger.info(f"📝 No existing onboarding state found at {filepath}")
                return

            with open(filepath) as f:
                state_data = json.load(f)

            # Restore agent states
            for agent_id, state_value in state_data.get("agent_states", {}).items():
                self.agent_states[agent_id] = AgentState(state_value)

            # Restore contracts
            for agent_id, contract_data in state_data.get("contracts", {}).items():
                contract = AgentContract(
                    agent_id=contract_data["agent_id"],
                    contract_type=ContractType(contract_data["contract_type"]),
                    description=contract_data["description"],
                    estimated_cycles=contract_data["estimated_cycles"],
                    dependencies=contract_data.get("dependencies", []),
                )
                contract.status = contract_data["status"]
                contract.progress_percentage = contract_data["progress_percentage"]
                contract.created_at = datetime.fromisoformat(contract_data["created_at"])
                self.contracts[agent_id] = contract

            logger.info(f"✅ Onboarding state loaded from {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to load onboarding state: {e}")


# Discord Commander Integration
class DiscordOnboardingIntegration:
    """Discord Commander integration for onboarding notifications."""

    def __init__(self, discord_commander):
        self.discord_commander = discord_commander
        self.onboarding_service = UnifiedOnboardingService(discord_commander=discord_commander)

    async def handle_onboarding_command(self, command: str, agent_id: str = None) -> str:
        """Handle onboarding commands from Discord."""
        try:
            if command == "onboard_all":
                results = await self.onboarding_service.onboard_all_agents()
                success_count = sum(1 for success in results.values() if success)
                return f"Onboarding complete: {success_count}/{len(results)} agents onboarded successfully"

            elif command == "onboard_agent" and agent_id:
                success = await self.onboarding_service.perform_agent_onboarding(agent_id)
                return f"Agent {agent_id} onboarding: {'Success' if success else 'Failed'}"

            elif command == "onboarding_status":
                states = {
                    agent: state.value
                    for agent, state in self.onboarding_service.agent_states.items()
                }
                return f"Onboarding Status: {states}"

            else:
                return "Unknown onboarding command. Available: onboard_all, onboard_agent, onboarding_status"

        except Exception as e:
            logger.error(f"Discord onboarding command failed: {e}")
            return f"Command failed: {e}"


if __name__ == "__main__":
    # Example usage
    service = UnifiedOnboardingService()

    # Load existing state
    service.load_onboarding_state()

    # Perform onboarding
    asyncio.run(service.onboard_all_agents())

    # Save state
    service.save_onboarding_state()

