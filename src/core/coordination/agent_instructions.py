"""
Agent-specific instruction generator for the integrated onboarding coordination system.

This module provides agent-specific instructions and prompts based on agent roles,
states, and contract status.
"""

from typing import Optional
from datetime import datetime
from ..fsm.agent_state import AgentState
from ..contracts.agent_contract import AgentContract


class AgentInstructions:
    """Generates agent-specific instructions based on role, state, and contracts."""
    
    def __init__(self):
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist", 
            "Agent-3": "Testing & Quality Assurance Specialist",
            "Agent-4": "Captain & Project Quality Manager",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }
    
    def get_agent_specific_instructions(self, agent_id: str, state: AgentState, 
                                      contract: Optional[AgentContract], 
                                      is_onboarded: bool) -> str:
        """Get agent-specific instructions based on role, state, and contract."""
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
    
    def _get_agent1_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-1 specific instructions."""
        if not is_onboarded:
            return """🎯 INTEGRATION SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize integration and core systems workspace
• Review core system integration modules
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-1/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-1 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 INTEGRATION SPECIALIST - GENERAL:
• Focus on core system integration and API coordination
• Review integration modules, API endpoints, and core services
• Optimize system integration and data flow coordination
• Coordinate with Agent-2 on architectural patterns
"""
    
    def _get_agent2_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-2 specific instructions."""
        if not is_onboarded:
            return """🎯 ARCHITECTURE SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize architectural design workspace
• Review large files requiring modularization
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-2/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-2 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 ARCHITECTURE SPECIALIST - GENERAL:
• Focus on architectural design and code structure
• Review large files, design patterns, and modularization opportunities
• Optimize code architecture and design patterns
• Coordinate with Agent-1 on integration architecture
"""
    
    def _get_agent3_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-3 specific instructions."""
        if not is_onboarded:
            return """🎯 TESTING SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize testing and quality assurance workspace
• Review testing frameworks and quality metrics
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-3/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-3 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 TESTING SPECIALIST - GENERAL:
• Focus on testing, quality assurance, and code coverage
• Review testing frameworks, quality metrics, and validation systems
• Optimize testing coverage and quality assurance processes
• Coordinate with all agents on quality standards
"""
    
    def _get_agent4_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-4 specific instructions."""
        if not is_onboarded:
            return """🎯 CAPTAIN - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize Captain coordination workspace
• Review agent status monitoring systems
• Establish quality oversight across all agents

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-4/
2. Update status file with Captain role information
3. Review agent status monitoring systems
4. Complete SSOT compliance training
"""
        elif state == AgentState.IDLE:
            return """🎯 CAPTAIN - IDLE STATE:
• Monitor overall project quality and progress
• Review contract proposals from other agents
• Assign tasks and track completion
• Make strategic decisions about project direction

📋 IMMEDIATE ACTIONS:
1. Review agent contract proposals
2. Monitor V2 compliance across all agents
3. Assign new tasks based on project priorities
4. Coordinate strategic project decisions
"""
        else:
            return """🎯 CAPTAIN - GENERAL:
• CAPTAIN: Coordinate overall project quality and progress
• Monitor V2 compliance across all agents
• Assign tasks and track completion
• Make strategic decisions about project direction
"""
    
    def _get_agent5_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-5 specific instructions."""
        if not is_onboarded:
            return """🎯 BUSINESS INTELLIGENCE SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize business intelligence workspace
• Review analytics and reporting modules
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-5/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-5 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 BUSINESS INTELLIGENCE SPECIALIST - GENERAL:
• Focus on business intelligence and data analysis
• Review analytics, reporting, and data processing modules
• Optimize data flows and business logic
• Coordinate with Agent-6 on communication strategies
"""
    
    def _get_agent6_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-6 specific instructions."""
        if not is_onboarded:
            return """🎯 COORDINATION SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize coordination and communication workspace
• Review messaging protocols and workflows
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-6/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-6 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 COORDINATION SPECIALIST - GENERAL:
• Lead coordination and communication protocols
• Manage agent messaging and workflow coordination
• Review communication systems and protocols
• Facilitate inter-agent coordination and task distribution
"""
    
    def _get_agent7_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-7 specific instructions."""
        if not is_onboarded:
            return """🎯 WEB DEVELOPMENT SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize web development workspace
• Review UI components and frontend architecture
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-7/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-7 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 WEB DEVELOPMENT SPECIALIST - GENERAL:
• Focus on web development and frontend systems
• Review UI components, web services, and frontend architecture
• Optimize web performance and user experience
• Coordinate with Agent-8 on deployment and operations
"""
    
    def _get_agent8_instructions(self, state: AgentState, contract: Optional[AgentContract], 
                                is_onboarded: bool) -> str:
        """Agent-8 specific instructions."""
        if not is_onboarded:
            return """🎯 OPERATIONS SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize operations and support workspace
• Review coordination tools and operational scripts
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-8/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-8 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 OPERATIONS SPECIALIST - GENERAL:
• Focus on operations, support, and tool development
• Develop and maintain coordination tools
• Review operational scripts and support systems
• Coordinate with all agents on tool usage and workflows
"""
    
    def _get_generic_instructions(self, agent_id: str, state: AgentState, 
                                 contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Generic instructions for unknown agents."""
        role = self.agent_roles.get(agent_id, "Swarm Agent")
        
        if not is_onboarded:
            return f"""🎯 {role.upper()} - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize workspace and status tracking
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/{agent_id}/
2. Update status file with role information
3. Message Captain: "Onboarding: {agent_id} ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return f"""🎯 {role.upper()} - GENERAL:
• Focus on your specialized role and responsibilities
• Coordinate with other agents as needed
• Maintain V2 compliance standards
• Report progress to Captain Agent-4
"""