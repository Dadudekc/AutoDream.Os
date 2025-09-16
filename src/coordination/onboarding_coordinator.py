#!/usr/bin/env python3
"""
Onboarding Coordinator Module
============================

Handles agent onboarding functionality including:
- Agent state management
- Contract creation and management
- Onboarding message generation
- Role-specific guidance

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
from datetime import datetime
from enum import Enum

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


class OnboardingCoordinator:
    """Coordinates agent onboarding process."""

    def __init__(self, coordination_service):
        self.coordination_service = coordination_service
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

    def perform_agent_onboarding(self, agent_id: str, role: str) -> bool:
        """Perform onboarding for a specific agent."""
        try:
            logger.info(f"🚀 Starting onboarding for {agent_id} - {role}")

            # Get agent coordinates
            coords = self.coordination_service.get_onboarding_coordinates(agent_id)
            if not coords:
                logger.error(f"❌ No coordinates found for {agent_id}")
                return False

            # Create onboarding contract
            contract = self.create_onboarding_contract(agent_id)
            self.coordination_service.contracts[agent_id] = contract

            # Create onboarding message
            message = self.create_onboarding_message(agent_id, role)

            # Send onboarding message (if PyAutoGUI available)
            if hasattr(self.coordination_service, "send_message"):
                success = self.coordination_service.send_message(agent_id, message)
                if success:
                    logger.info(f"✅ Onboarding message sent to {agent_id}")
                    contract.status = "active"
                    return True
                else:
                    logger.error(f"❌ Failed to send onboarding message to {agent_id}")
                    return False
            else:
                logger.info(f"📝 Onboarding message for {agent_id}: {message}")
                contract.status = "active"
                return True

        except Exception as e:
            logger.error(f"❌ Onboarding failed for {agent_id}: {e}")
            return False

    def create_onboarding_contract(self, agent_id: str) -> AgentContract:
        """Create onboarding contract for agent."""
        return AgentContract(
            agent_id=agent_id,
            contract_type=ContractType.ONBOARDING,
            description=f"Onboarding contract for {agent_id}",
            estimated_cycles=2,
        )

    def create_onboarding_message(self, agent_id: str, role: str) -> str:
        """Create onboarding message for agent."""
        role_guidance = self._get_role_onboarding_guidance(agent_id)

        message = f"""
============================================================
🚀 AGENT ONBOARDING - {agent_id}
============================================================
📤 FROM: System
📥 TO: {agent_id}
Priority: HIGH
Tags: ONBOARDING|INITIALIZATION
------------------------------------------------------------
🎯 WELCOME TO THE SWARM - {role}

{role_guidance}

ONBOARDING CHECKLIST:
✅ Agent ID: {agent_id}
✅ Role: {role}
✅ Contract: Onboarding Contract Created
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

    def onboard_all_agents(self) -> dict[str, bool]:
        """Onboard all agents in the swarm."""
        logger.info("🚀 Starting onboarding for all agents...")
        results = {}

        for agent_id, role in self.agent_roles.items():
            logger.info(f"📋 Onboarding {agent_id} - {role}")
            results[agent_id] = self.perform_agent_onboarding(agent_id, role)

        successful_onboards = sum(1 for success in results.values() if success)
        logger.info(
            f"✅ Onboarding complete: {successful_onboards}/{len(results)} agents onboarded successfully"
        )

        return results

    def get_agent_specific_prompt(self, agent_id: str) -> str:
        """Get agent-specific prompt based on state and contract."""
        try:
            # Get agent FSM state
            fsm = self.coordination_service.agent_fsms.get(agent_id)
            current_state = fsm.current_state if fsm else AgentState.UNINITIALIZED

            # Get agent contract
            contract = self.coordination_service.contracts.get(agent_id)

            # Check if agent is onboarded
            is_onboarded = current_state != AgentState.UNINITIALIZED

            # Get role
            role = self.agent_roles.get(agent_id, "Specialist")

            # Generate agent-specific instructions
            if agent_id == "Agent-1":
                return self._get_agent1_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-2":
                return self._get_agent2_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-3":
                return self._get_agent3_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-4":
                return self._get_agent4_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-5":
                return self._get_agent5_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-6":
                return self._get_agent6_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-7":
                return self._get_agent7_instructions(current_state, contract, is_onboarded)
            elif agent_id == "Agent-8":
                return self._get_agent8_instructions(current_state, contract, is_onboarded)
            else:
                return f"General instructions for {agent_id} - {role}"

        except Exception as e:
            logger.error(f"❌ Failed to get agent-specific prompt for {agent_id}: {e}")
            return f"Error generating prompt for {agent_id}"

    def _get_agent1_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-1 specific instructions."""
        if not is_onboarded:
            return """
🚀 AGENT-1 ONBOARDING - Integration & Core Systems Specialist

Welcome to the swarm! Your role is Integration & Core Systems Specialist.

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

Ready to begin your integration specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-1 specific instructions based on state and contract"

    def _get_agent2_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-2 specific instructions."""
        if not is_onboarded:
            return """
🏗️ AGENT-2 ONBOARDING - Architecture & Design Specialist

Welcome to the swarm! Your role is Architecture & Design Specialist.

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

Ready to begin your architecture specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-2 specific instructions based on state and contract"

    def _get_agent3_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-3 specific instructions."""
        if not is_onboarded:
            return """
🔧 AGENT-3 ONBOARDING - Infrastructure & DevOps Specialist

Welcome to the swarm! Your role is Infrastructure & DevOps Specialist.

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

Ready to begin your infrastructure specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-3 specific instructions based on state and contract"

    def _get_agent4_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-4 specific instructions."""
        if not is_onboarded:
            return """
👑 AGENT-4 ONBOARDING - Quality Assurance Specialist (CAPTAIN)

Welcome to the swarm! Your role is Quality Assurance Specialist (CAPTAIN).

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

Ready to begin your captain journey!
"""
        # Additional state-based instructions...
        return "Agent-4 specific instructions based on state and contract"

    def _get_agent5_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-5 specific instructions."""
        if not is_onboarded:
            return """
📊 AGENT-5 ONBOARDING - Business Intelligence Specialist

Welcome to the swarm! Your role is Business Intelligence Specialist.

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

Ready to begin your BI specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-5 specific instructions based on state and contract"

    def _get_agent6_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-6 specific instructions."""
        if not is_onboarded:
            return """
🤝 AGENT-6 ONBOARDING - Coordination & Communication Specialist

Welcome to the swarm! Your role is Coordination & Communication Specialist.

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

Ready to begin your coordination specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-6 specific instructions based on state and contract"

    def _get_agent7_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-7 specific instructions."""
        if not is_onboarded:
            return """
🌐 AGENT-7 ONBOARDING - Web Development Specialist

Welcome to the swarm! Your role is Web Development Specialist.

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

Ready to begin your web development specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-7 specific instructions based on state and contract"

    def _get_agent8_instructions(
        self, state: AgentState, contract: AgentContract | None, is_onboarded: bool
    ) -> str:
        """Get Agent-8 specific instructions."""
        if not is_onboarded:
            return """
🔗 AGENT-8 ONBOARDING - SSOT & System Integration Specialist

Welcome to the swarm! Your role is SSOT & System Integration Specialist.

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

Ready to begin your SSOT specialist journey!
"""
        # Additional state-based instructions...
        return "Agent-8 specific instructions based on state and contract"
