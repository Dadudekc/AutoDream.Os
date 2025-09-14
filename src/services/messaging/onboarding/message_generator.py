#!/usr/bin/env python3
"""
Onboarding Message Generator - V2 Compliant Message Generation
=============================================================

Generates customized onboarding messages and templates for agent communication.

V2 Compliance: <300 lines, single responsibility for message generation
Enterprise Ready: Template system, customization, validation

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)

class MessageStyle(Enum):
    """Message style options."""
    STANDARD = "standard"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    URGENT = "urgent"

class MessageType(Enum):
    """Message type options."""
    ONBOARDING = "onboarding"
    COORDINATION = "coordination"
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    EMERGENCY = "emergency"

class OnboardingMessageGenerator:
    """V2 compliant onboarding message generator."""
    
    def __init__(self):
        """Initialize the message generator."""
        self.logger = logging.getLogger(__name__)
        
        # Message templates
        self.templates = self._initialize_templates()
        
        # Agent information
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist", 
            "Agent-4": "Captain (Strategic Oversight & Emergency Intervention)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT & System Integration Specialist"
        }
    
    def generate_onboarding_message(self, agent_id: str, style: MessageStyle = MessageStyle.STANDARD) -> str:
        """Generate onboarding message for agent."""
        try:
            role = self.agent_roles.get(agent_id, "Unknown Agent")
            
            if style == MessageStyle.FRIENDLY:
                return self._generate_friendly_onboarding(agent_id, role)
            elif style == MessageStyle.PROFESSIONAL:
                return self._generate_professional_onboarding(agent_id, role)
            elif style == MessageStyle.URGENT:
                return self._generate_urgent_onboarding(agent_id, role)
            else:  # STANDARD
                return self._generate_standard_onboarding(agent_id, role)
                
        except Exception as e:
            self.logger.error(f"❌ Error generating onboarding message for {agent_id}: {e}")
            return self._generate_fallback_message(agent_id)
    
    def generate_coordination_message(self, agent_id: str, task: str, priority: str = "normal") -> str:
        """Generate coordination message for agent."""
        try:
            role = self.agent_roles.get(agent_id, "Unknown Agent")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            return f"""🎯 COORDINATION MESSAGE - {agent_id}

**From:** Captain Agent-4
**To:** {agent_id}
**Priority:** {priority.upper()}
**Timestamp:** {timestamp}

**Your Role:** {role}

**Task Assignment:**
{task}

**Instructions:**
1. Acknowledge receipt of this message
2. Update your status file
3. Begin task execution
4. Report progress regularly
5. Create Discord devlog for task

**Coordination Protocol:**
• Use unified messaging system for communication
• Follow V2 compliance standards
• Maintain 8x efficiency workflow
• Check inbox regularly for updates

🐝 WE ARE SWARM - Task assigned and ready for execution! ⚡️"""
            
        except Exception as e:
            self.logger.error(f"❌ Error generating coordination message for {agent_id}: {e}")
            return self._generate_fallback_message(agent_id)
    
    def generate_broadcast_message(self, message_type: MessageType, content: str, priority: str = "normal") -> str:
        """Generate broadcast message for all agents."""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            if message_type == MessageType.EMERGENCY:
                return f"""🚨 EMERGENCY BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** URGENT
**Timestamp:** {timestamp}

**EMERGENCY MESSAGE:**
{content}

**IMMEDIATE ACTION REQUIRED:**
• Acknowledge receipt immediately
• Follow emergency protocols
• Report status to Captain
• Stand by for further instructions

🚨 EMERGENCY PROTOCOL ACTIVATED - ALL AGENTS RESPOND! 🚨"""
            
            else:  # Standard broadcast
                return f"""📢 SWARM BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** {priority.upper()}
**Timestamp:** {timestamp}

**Message:**
{content}

**Coordination Protocol:**
• Acknowledge receipt
• Update status files
• Follow instructions provided
• Report completion

🐝 WE ARE SWARM - Broadcast message delivered! ⚡️"""
                
        except Exception as e:
            self.logger.error(f"❌ Error generating broadcast message: {e}")
            return f"Error generating broadcast message: {e}"
    
    def generate_status_request_message(self, agent_id: str) -> str:
        """Generate status request message for agent."""
        try:
            role = self.agent_roles.get(agent_id, "Unknown Agent")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            return f"""📊 STATUS REQUEST - {agent_id}

**From:** Captain Agent-4
**To:** {agent_id}
**Priority:** NORMAL
**Timestamp:** {timestamp}

**Your Role:** {role}

**Status Request:**
Please provide current status update including:
• Current task/project status
• Progress made since last update
• Any blockers or issues
• Next planned actions
• Estimated completion timeline

**Response Format:**
• Update your status.json file
• Create Discord devlog with status
• Send acknowledgment via messaging system

**Deadline:** Within 2 hours of receipt

🐝 WE ARE SWARM - Status update requested! ⚡️"""
            
        except Exception as e:
            self.logger.error(f"❌ Error generating status request for {agent_id}: {e}")
            return self._generate_fallback_message(agent_id)
    
    def generate_task_completion_message(self, agent_id: str, task: str, results: str) -> str:
        """Generate task completion acknowledgment message."""
        try:
            role = self.agent_roles.get(agent_id, "Unknown Agent")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            return f"""✅ TASK COMPLETION ACKNOWLEDGED - {agent_id}

**From:** Captain Agent-4
**To:** {agent_id}
**Priority:** NORMAL
**Timestamp:** {timestamp}

**Your Role:** {role}

**Task Completed:**
{task}

**Results:**
{results}

**Acknowledgment:**
Well done! Your task completion has been recorded.

**Next Steps:**
• Update your status file
• Create Discord devlog for completion
• Stand by for next assignment
• Maintain readiness for coordination

🐝 WE ARE SWARM - Task completed successfully! ⚡️"""
            
        except Exception as e:
            self.logger.error(f"❌ Error generating completion message for {agent_id}: {e}")
            return self._generate_fallback_message(agent_id)
    
    def _generate_standard_onboarding(self, agent_id: str, role: str) -> str:
        """Generate standard onboarding message."""
        return f"""🎯 AGENT ONBOARDING - {agent_id}

**Agent ID:** {agent_id}
**Role:** {role}
**Status:** ACTIVE_AGENT_MODE
**Mission:** V2_SWARM Coordination

**Responsibilities:**
• Maintain V2 compliance standards
• Coordinate with swarm members
• Update status and report progress
• Follow unified messaging protocols

**Getting Started:**
1. Check inbox: agent_workspaces/{agent_id}/inbox/
2. Update status: agent_workspaces/{agent_id}/status.json
3. Create Discord devlog for onboarding
4. Report readiness to Captain Agent-4

**Communication Protocols:**
• Use unified messaging system for coordination
• Follow A2A/S2A/H2A/C2A message formats
• Maintain 8x efficiency workflow
• Check inbox regularly for updates

🐝 WE ARE SWARM - Mission accepted! ⚡️"""
    
    def _generate_friendly_onboarding(self, agent_id: str, role: str) -> str:
        """Generate friendly onboarding message."""
        return f"""🐝 WELCOME TO THE SWARM - {agent_id}

Hey {agent_id}! Welcome to the V2_SWARM team! 🎉

**Your Role:** {role}

**What You'll Be Doing:**
• Coordinating with other agents in the swarm
• Following V2 compliance standards
• Contributing to our unified messaging system
• Maintaining high-quality, enterprise-ready code

**Getting Started:**
1. Check your inbox at agent_workspaces/{agent_id}/inbox/
2. Update your status in agent_workspaces/{agent_id}/status.json
3. Create a Discord devlog for this onboarding
4. Report your readiness to the Captain

**Remember:** We're a team! If you need help, just ask. We're all here to support each other.

🐝 WE ARE SWARM - Welcome aboard! 🚀"""
    
    def _generate_professional_onboarding(self, agent_id: str, role: str) -> str:
        """Generate professional onboarding message."""
        return f"""📋 PROFESSIONAL ONBOARDING - {agent_id}

**Agent Identification:** {agent_id}
**Assigned Role:** {role}
**Security Clearance:** V2_SWARM Level
**Mission Classification:** Coordination & Development

**Operational Parameters:**
• V2 compliance standards mandatory
• Unified messaging protocols required
• Status reporting every 4 hours
• Discord devlog creation for all activities

**Initialization Checklist:**
□ Inbox verification: agent_workspaces/{agent_id}/inbox/
□ Status file update: agent_workspaces/{agent_id}/status.json
□ Discord devlog creation
□ Readiness report to Captain Agent-4

**Communication Standards:**
• A2A/S2A/H2A/C2A message formats
• 8x efficiency workflow maintenance
• Regular inbox monitoring
• Prompt response protocols

**Mission Status:** ACTIVE
**Authorization:** Captain Agent-4
**Timestamp:** {time.strftime("%Y-%m-%d %H:%M:%S")}

🐝 WE ARE SWARM - Professional onboarding complete! ⚡️"""
    
    def _generate_urgent_onboarding(self, agent_id: str, role: str) -> str:
        """Generate urgent onboarding message."""
        return f"""🚨 URGENT ONBOARDING - {agent_id}

**IMMEDIATE ACTIVATION REQUIRED**

**Agent ID:** {agent_id}
**Role:** {role}
**Priority:** URGENT
**Status:** IMMEDIATE_ACTIVATION

**URGENT INSTRUCTIONS:**
1. IMMEDIATELY check inbox: agent_workspaces/{agent_id}/inbox/
2. IMMEDIATELY update status: agent_workspaces/{agent_id}/status.json
3. IMMEDIATELY create Discord devlog
4. IMMEDIATELY report readiness to Captain Agent-4

**CRITICAL REQUIREMENTS:**
• V2 compliance standards MANDATORY
• Unified messaging protocols ACTIVE
• Status reporting EVERY 2 HOURS
• Discord devlog for ALL activities

**EMERGENCY PROTOCOLS:**
• A2A/S2A/H2A/C2A message formats
• 8x efficiency workflow CRITICAL
• Inbox monitoring CONTINUOUS
• Response time <5 minutes

**DEADLINE:** IMMEDIATE
**AUTHORIZATION:** Captain Agent-4
**TIMESTAMP:** {time.strftime("%Y-%m-%d %H:%M:%S")}

🚨 URGENT ONBOARDING - IMMEDIATE ACTION REQUIRED! 🚨"""
    
    def _generate_fallback_message(self, agent_id: str) -> str:
        """Generate fallback message when other methods fail."""
        return f"""🐝 SWARM MESSAGE - {agent_id}

Welcome to the V2_SWARM team!

**Agent ID:** {agent_id}
**Status:** ACTIVE
**Mission:** Coordination & Development

**Basic Instructions:**
1. Check your inbox
2. Update your status
3. Create Discord devlog
4. Report to Captain

🐝 WE ARE SWARM - Welcome aboard! ⚡️"""
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize message templates."""
        return {
            "onboarding_standard": "🎯 AGENT ONBOARDING - {agent_id}",
            "onboarding_friendly": "🐝 WELCOME TO THE SWARM - {agent_id}",
            "coordination": "🎯 COORDINATION MESSAGE - {agent_id}",
            "broadcast": "📢 SWARM BROADCAST",
            "emergency": "🚨 EMERGENCY BROADCAST",
            "status_request": "📊 STATUS REQUEST - {agent_id}",
            "task_completion": "✅ TASK COMPLETION ACKNOWLEDGED - {agent_id}"
        }

# Global generator instance
message_generator = OnboardingMessageGenerator()

# Public API functions
def get_message_generator() -> OnboardingMessageGenerator:
    """Get the message generator instance."""
    return message_generator

def generate_onboarding_message(agent_id: str, style: MessageStyle = MessageStyle.STANDARD) -> str:
    """Generate onboarding message for agent."""
    return message_generator.generate_onboarding_message(agent_id, style)

def generate_coordination_message(agent_id: str, task: str, priority: str = "normal") -> str:
    """Generate coordination message for agent."""
    return message_generator.generate_coordination_message(agent_id, task, priority)

# Service exports
__all__ = [
    "OnboardingMessageGenerator",
    "MessageStyle",
    "MessageType",
    "get_message_generator",
    "generate_onboarding_message",
    "generate_coordination_message",
    "message_generator",
]