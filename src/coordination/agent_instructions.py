#!/usr/bin/env python3
"""
Agent Instructions Module
=========================

Handles agent-specific instructions and prompts including:
- Agent-specific instruction generation
- State-based prompt creation
- Contract-based guidance
- Role-specific instructions

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging

from .onboarding_coordinator import AgentContract, AgentState

logger = logging.getLogger(__name__)


class AgentInstructions:
    """Handles agent-specific instructions and prompts."""

    def __init__(self):
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

    def get_agent_instructions(
        self,
        agent_id: str,
        state: AgentState,
        contract: AgentContract | None,
        is_onboarded: bool,
    ) -> str:
        """Get agent-specific instructions based on state and contract."""
        try:
            if agent_id == "Agent-1":
                return self._get_agent1_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-2":
                return self._get_agent2_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-3":
                return self._get_agent3_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-4":
                return self._get_agent4_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-5":
                return self._get_agent5_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-6":
                return self._get_agent6_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-7":
                return self._get_agent7_instructions(state, contract, is_onboarded)
            elif agent_id == "Agent-8":
                return self._get_agent8_instructions(state, contract, is_onboarded)
            else:
                return self._get_generic_instructions(agent_id, state, contract, is_onboarded)
        except Exception as e:
            logger.error(f"❌ Failed to get instructions for {agent_id}: {e}")
            return f"Error generating instructions for {agent_id}"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🔧 AGENT-1 TASK EXECUTION - Integration & Core Systems

Current Mission: Core Systems Integration

TASK EXECUTION GUIDANCE:
1. Focus on system integration tasks
2. Optimize API performance and reliability
3. Ensure database integration efficiency
4. Maintain core service architecture standards

INTEGRATION PRIORITIES:
- API endpoint optimization
- Database query performance
- Service communication protocols
- Error handling and recovery

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-1 COLLABORATION - Integration & Core Systems

Collaboration Focus: Cross-system Integration

COLLABORATION TASKS:
1. Coordinate with other agents for system integration
2. Share integration best practices
3. Support other agents with core systems needs
4. Maintain integration standards across the swarm

INTEGRATION SUPPORT:
- Provide API integration guidance
- Share database optimization techniques
- Support service architecture decisions
- Coordinate cross-system communication

Maintain active collaboration with all agents.
"""

        return "Agent-1 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🏗️ AGENT-2 TASK EXECUTION - Architecture & Design

Current Mission: Architecture Enhancement and Modularization

TASK EXECUTION GUIDANCE:
1. Focus on architecture design and implementation
2. Apply design patterns (Repository, Factory, Service Layer)
3. Ensure V2 compliance (≤400 lines per module)
4. Optimize code structure and maintainability

ARCHITECTURE PRIORITIES:
- Design pattern implementation
- Code modularization and refactoring
- V2 compliance enforcement
- Architecture documentation

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-2 COLLABORATION - Architecture & Design

Collaboration Focus: Architectural Guidance

COLLABORATION TASKS:
1. Provide architectural guidance to other agents
2. Review and validate design implementations
3. Share architecture best practices
4. Support V2 compliance across the swarm

ARCHITECTURE SUPPORT:
- Provide design pattern guidance
- Review code structure and modularization
- Support V2 compliance validation
- Coordinate architectural decisions

Maintain active collaboration with all agents.
"""

        return "Agent-2 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🔧 AGENT-3 TASK EXECUTION - Infrastructure & DevOps

Current Mission: Infrastructure Optimization

TASK EXECUTION GUIDANCE:
1. Focus on infrastructure management and optimization
2. Implement and maintain DevOps pipelines
3. Ensure deployment automation and monitoring
4. Optimize system reliability and performance

INFRASTRUCTURE PRIORITIES:
- DevOps pipeline optimization
- Deployment automation enhancement
- System monitoring and alerting
- Performance optimization

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-3 COLLABORATION - Infrastructure & DevOps

Collaboration Focus: Infrastructure Support

COLLABORATION TASKS:
1. Provide infrastructure support to other agents
2. Share DevOps best practices
3. Support deployment and monitoring needs
4. Coordinate infrastructure optimization

INFRASTRUCTURE SUPPORT:
- Provide deployment guidance
- Share monitoring and alerting techniques
- Support performance optimization
- Coordinate infrastructure decisions

Maintain active collaboration with all agents.
"""

        return "Agent-3 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
👑 AGENT-4 TASK EXECUTION - Quality Assurance (CAPTAIN)

Current Mission: Quality Leadership and Swarm Coordination

TASK EXECUTION GUIDANCE:
1. Lead quality assurance and testing efforts
2. Coordinate swarm activities and missions
3. Enforce quality standards across all agents
4. Monitor and report on swarm performance

CAPTAIN PRIORITIES:
- Quality standards enforcement
- Swarm coordination and leadership
- Performance monitoring and reporting
- Mission planning and execution

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-4 COLLABORATION - Quality Assurance (CAPTAIN)

Collaboration Focus: Swarm Leadership

COLLABORATION TASKS:
1. Lead and coordinate all swarm activities
2. Provide quality guidance to all agents
3. Monitor swarm performance and progress
4. Coordinate mission planning and execution

CAPTAIN SUPPORT:
- Provide leadership and guidance
- Coordinate cross-agent activities
- Monitor quality and performance
- Plan and execute swarm missions

Maintain active leadership with all agents.
"""

        return "Agent-4 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
📊 AGENT-5 TASK EXECUTION - Business Intelligence

Current Mission: BI Development and Analytics

TASK EXECUTION GUIDANCE:
1. Focus on business intelligence and data analysis
2. Develop performance metrics and reporting
3. Create data visualizations and dashboards
4. Optimize business processes and workflows

BI PRIORITIES:
- Data analysis and insights
- Performance metrics development
- Dashboard and visualization creation
- Business process optimization

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-5 COLLABORATION - Business Intelligence

Collaboration Focus: Data and Analytics Support

COLLABORATION TASKS:
1. Provide data analysis support to other agents
2. Share BI best practices and techniques
3. Support reporting and visualization needs
4. Coordinate business process optimization

BI SUPPORT:
- Provide data analysis guidance
- Share reporting and visualization techniques
- Support performance metrics development
- Coordinate business process decisions

Maintain active collaboration with all agents.
"""

        return "Agent-5 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🤝 AGENT-6 TASK EXECUTION - Coordination & Communication

Current Mission: Communication System Enhancement

TASK EXECUTION GUIDANCE:
1. Focus on inter-agent coordination and communication
2. Optimize message routing and delivery
3. Enhance swarm coordination and synchronization
4. Implement advanced communication protocols

COORDINATION PRIORITIES:
- Message routing optimization
- Communication protocol enhancement
- Swarm coordination improvement
- Performance optimization

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-6 COLLABORATION - Coordination & Communication

Collaboration Focus: Communication Leadership

COLLABORATION TASKS:
1. Lead communication and coordination efforts
2. Provide communication guidance to all agents
3. Optimize inter-agent communication
4. Coordinate swarm synchronization

COMMUNICATION SUPPORT:
- Provide communication guidance
- Share coordination best practices
- Support message routing optimization
- Coordinate communication protocols

Maintain active communication with all agents.
"""

        return "Agent-6 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🌐 AGENT-7 TASK EXECUTION - Web Development

Current Mission: Web Interface Development

TASK EXECUTION GUIDANCE:
1. Focus on web interface development and maintenance
2. Implement frontend and backend web solutions
3. Design and implement user interfaces
4. Optimize web application performance

WEB PRIORITIES:
- Interface development and enhancement
- User experience optimization
- Web application performance
- Frontend and backend integration

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-7 COLLABORATION - Web Development

Collaboration Focus: Web Development Support

COLLABORATION TASKS:
1. Provide web development support to other agents
2. Share web development best practices
3. Support interface and user experience needs
4. Coordinate web application development

WEB SUPPORT:
- Provide web development guidance
- Share UI/UX best practices
- Support web application optimization
- Coordinate web development decisions

Maintain active collaboration with all agents.
"""

        return "Agent-7 specific instructions based on current state and contract"

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

        # State-based instructions
        if state == AgentState.TASK_EXECUTION:
            return """
🔗 AGENT-8 TASK EXECUTION - SSOT & System Integration

Current Mission: SSOT Management and System Integration

TASK EXECUTION GUIDANCE:
1. Focus on SSOT management and data consistency
2. Implement system integration and coordination
3. Manage configuration and validation
4. Ensure cross-system synchronization

SSOT PRIORITIES:
- Data consistency and validation
- System integration coordination
- Configuration management
- Cross-system synchronization

Report progress every 2 agent response cycles.
"""
        elif state == AgentState.COLLABORATION:
            return """
🤝 AGENT-8 COLLABORATION - SSOT & System Integration

Collaboration Focus: System Integration Leadership

COLLABORATION TASKS:
1. Lead system integration and coordination efforts
2. Provide SSOT guidance to all agents
3. Ensure data consistency across systems
4. Coordinate cross-system synchronization

SSOT SUPPORT:
- Provide system integration guidance
- Share SSOT best practices
- Support data consistency validation
- Coordinate system integration decisions

Maintain active collaboration with all agents.
"""

        return "Agent-8 specific instructions based on current state and contract"

    def _get_generic_instructions(
        self,
        agent_id: str,
        state: AgentState,
        contract: AgentContract | None,
        is_onboarded: bool,
    ) -> str:
        """Get generic instructions for unknown agents."""
        role = self.agent_roles.get(agent_id, "Specialist")

        if not is_onboarded:
            return f"""
🎯 {agent_id} ONBOARDING - {role}

Welcome to the swarm! Your role is {role}.

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

Ready to begin your specialist journey!
"""

        return f"Generic instructions for {agent_id} - {role} based on current state and contract"
