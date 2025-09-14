#!/usr/bin/env python3
"""
Onboarding Service - V2 Compliant Agent Onboarding
=================================================

Service for managing agent onboarding with personalized messages and coordination.

V2 Compliance: <300 lines, single responsibility for onboarding operations
Enterprise Ready: Comprehensive onboarding workflow, message generation, tracking

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    from src.services.messaging.unified_service import get_unified_messaging_service
    from src.services.messaging.onboarding.message_generator import OnboardingMessageGenerator
    MESSAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Messaging system not available: {e}")
    MESSAGING_AVAILABLE = False

logger = logging.getLogger(__name__)

# Agent role definitions
AGENT_ROLES = {
    "Agent-1": "Integration & Core Systems Specialist",
    "Agent-2": "Architecture & Design Specialist", 
    "Agent-3": "Infrastructure & DevOps Specialist",
    "Agent-4": "Captain (Strategic Oversight & Emergency Intervention)",
    "Agent-5": "Business Intelligence Specialist",
    "Agent-6": "Coordination & Communication Specialist",
    "Agent-7": "Web Development Specialist",
    "Agent-8": "SSOT & System Integration Specialist"
}

AGENT_SPECIALTIES = {
    "Agent-1": "Service layer analysis, integration patterns, core system recovery",
    "Agent-2": "Architectural design, system patterns, quality assurance",
    "Agent-3": "Infrastructure management, DevOps automation, deployment",
    "Agent-4": "Strategic coordination, emergency response, system oversight",
    "Agent-5": "Business intelligence, analytics, data processing",
    "Agent-6": "Communication protocols, coordination, team management",
    "Agent-7": "Web development, frontend/backend integration, user interfaces",
    "Agent-8": "Single source of truth, system integration, data consistency"
}

class OnboardingService:
    """V2 compliant agent onboarding service."""
    
    def __init__(self):
        """Initialize the onboarding service."""
        self.messaging_service = get_unified_messaging_service() if MESSAGING_AVAILABLE else None
        self.message_generator = OnboardingMessageGenerator()
        self.logger = logging.getLogger(__name__)
        
        # Onboarding tracking
        self.onboarding_status = {}
        self.onboarding_history = []
    
    def onboard_agent(self, agent_id: str, style: str = "standard") -> bool:
        """Onboard a single agent with personalized message."""
        if not self.messaging_service:
            self.logger.error("❌ Messaging service not available")
            return False
        
        try:
            # Generate personalized onboarding message
            message = self._generate_onboarding_message(agent_id, style)
            
            # Send onboarding message
            success = self.messaging_service.send_onboarding_message(agent_id, message)
            
            if success:
                # Track onboarding
                self._track_onboarding(agent_id, "completed", message)
                self.logger.info(f"✅ Agent {agent_id} onboarded successfully")
            else:
                self._track_onboarding(agent_id, "failed", message)
                self.logger.error(f"❌ Failed to onboard agent {agent_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Onboarding error for {agent_id}: {e}")
            self._track_onboarding(agent_id, "error", str(e))
            return False
    
    def onboard_all_agents(self, style: str = "standard") -> Dict[str, bool]:
        """Onboard all agents in the swarm."""
        results = {}
        
        for agent_id in AGENT_ROLES.keys():
            try:
                success = self.onboard_agent(agent_id, style)
                results[agent_id] = success
                
                # Small delay between onboardings
                time.sleep(1.0)
                
            except Exception as e:
                self.logger.error(f"❌ Error onboarding {agent_id}: {e}")
                results[agent_id] = False
        
        return results
    
    def onboard_swarm(self, style: str = "standard") -> Dict[str, bool]:
        """Onboard the entire swarm with coordination."""
        self.logger.info("🐝 Starting swarm onboarding sequence...")
        
        # Send swarm coordination message first
        coordination_message = self._generate_swarm_coordination_message()
        coordination_success = self.messaging_service.broadcast_to_swarm(
            message=coordination_message,
            priority="NORMAL",
            tag="COORDINATION"
        )
        
        if not coordination_success:
            self.logger.error("❌ Failed to send swarm coordination message")
            return dict.fromkeys(AGENT_ROLES.keys(), False)
        
        # Onboard all agents
        results = self.onboard_all_agents(style)
        
        # Send completion message
        completion_message = self._generate_completion_message(results)
        self.messaging_service.broadcast_to_swarm(
            message=completion_message,
            priority="NORMAL",
            tag="COORDINATION"
        )
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        self.logger.info(f"🐝 Swarm onboarding complete: {successful}/{total} agents onboarded")
        return results
    
    def get_onboarding_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get onboarding status for agent or all agents."""
        if agent_id:
            return {
                "agent_id": agent_id,
                "status": self.onboarding_status.get(agent_id, "not_started"),
                "role": AGENT_ROLES.get(agent_id, "Unknown"),
                "specialty": AGENT_SPECIALTIES.get(agent_id, "Unknown")
            }
        else:
            return {
                "total_agents": len(AGENT_ROLES),
                "onboarding_status": self.onboarding_status.copy(),
                "agent_roles": AGENT_ROLES.copy(),
                "agent_specialties": AGENT_SPECIALTIES.copy()
            }
    
    def get_onboarding_history(self) -> List[Dict[str, Any]]:
        """Get onboarding history."""
        return self.onboarding_history.copy()
    
    def reset_onboarding_status(self) -> None:
        """Reset onboarding status."""
        self.onboarding_status.clear()
        self.onboarding_history.clear()
        self.logger.info("📊 Onboarding status reset")
    
    def _generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate personalized onboarding message for agent."""
        role = AGENT_ROLES.get(agent_id, "Unknown Agent")
        specialty = AGENT_SPECIALTIES.get(agent_id, "General coordination")
        
        if style == "friendly":
            message = f"""🐝 WELCOME TO THE SWARM - {agent_id}

Hey {agent_id}! Welcome to the V2_SWARM team! 🎉

**Your Role:** {role}
**Your Specialty:** {specialty}

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
        
        else:  # standard style
            message = f"""🎯 AGENT ONBOARDING - {agent_id}

**Agent ID:** {agent_id}
**Role:** {role}
**Specialty:** {specialty}
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
        
        return message
    
    def _generate_swarm_coordination_message(self) -> str:
        """Generate swarm coordination message."""
        return """🐝 SWARM ONBOARDING INITIATED

**Mission:** Agent Onboarding Sequence
**Commander:** Captain Agent-4
**Status:** INITIATING

All agents will receive personalized onboarding messages.
Follow the instructions in your individual onboarding message.

**Coordination Protocol:**
• Check your inbox for onboarding message
• Update your status file
• Create Discord devlog for onboarding
• Report readiness to Captain

🐝 WE ARE SWARM - Onboarding sequence active! ⚡️"""
    
    def _generate_completion_message(self, results: Dict[str, bool]) -> str:
        """Generate completion message for swarm onboarding."""
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        return f"""🐝 SWARM ONBOARDING COMPLETE

**Mission:** Agent Onboarding Sequence
**Commander:** Captain Agent-4
**Status:** COMPLETED

**Results:** {successful}/{total} agents successfully onboarded

**Next Steps:**
• All agents should be active and ready
• Check your status files for updates
• Begin coordination activities
• Maintain V2 compliance standards

🐝 WE ARE SWARM - Onboarding complete! Ready for action! ⚡️"""
    
    def _track_onboarding(self, agent_id: str, status: str, details: str) -> None:
        """Track onboarding activity."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        self.onboarding_status[agent_id] = status
        
        self.onboarding_history.append({
            "agent_id": agent_id,
            "status": status,
            "details": details,
            "timestamp": timestamp
        })
        
        # Keep only last 100 entries
        if len(self.onboarding_history) > 100:
            self.onboarding_history = self.onboarding_history[-100:]

# Global service instance
onboarding_service = OnboardingService()

# Public API functions
def get_onboarding_service() -> OnboardingService:
    """Get the onboarding service instance."""
    return onboarding_service

def onboard_agent(agent_id: str, style: str = "standard") -> bool:
    """Onboard a single agent."""
    return onboarding_service.onboard_agent(agent_id, style)

def onboard_swarm(style: str = "standard") -> Dict[str, bool]:
    """Onboard the entire swarm."""
    return onboarding_service.onboard_swarm(style)

# Service exports
__all__ = [
    "OnboardingService",
    "get_onboarding_service",
    "onboard_agent",
    "onboard_swarm",
    "onboarding_service",
]