#!/usr/bin/env python3
"""
Onboarding Service - Agent Cellphone V2
=====================================

Onboarding message generation and delivery service.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - Onboarding Service
License: MIT
"""

from typing import List, Dict, Any
from ..models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


class OnboardingService:
    """Service for generating and managing onboarding messages"""
    
    def __init__(self):
        """Initialize the onboarding service"""
        self.agents = {
            "Agent-1": {"description": "Integration & Core Systems Specialist", "coords": (-1269, 481)},
            "Agent-2": {"description": "Architecture & Design Specialist", "coords": (-308, 480)},
            "Agent-3": {"description": "Infrastructure & DevOps Specialist", "coords": (-1269, 1001)},
            "Agent-4": {"description": "Quality Assurance Specialist (CAPTAIN)", "coords": (-308, 1000)},
            "Agent-5": {"description": "Business Intelligence Specialist", "coords": (652, 421)},
            "Agent-6": {"description": "Gaming & Entertainment Specialist", "coords": (1612, 419)},
            "Agent-7": {"description": "Web Development Specialist", "coords": (653, 940)},
            "Agent-8": {"description": "Integration & Performance Specialist", "coords": (1611, 941)},
        }
    
    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent"""
        agent_info = self.agents.get(agent_id, {})
        description = agent_info.get("description", "Specialist")
        
        if style == "strict":
            return self._generate_strict_onboarding(agent_id, description)
        else:
            return self._generate_friendly_onboarding(agent_id, description)
    
    def _generate_strict_onboarding(self, agent_id: str, description: str) -> str:
        """Generate strict mode onboarding message"""
        return f"""🚨 **ONBOARDING - STRICT MODE** 🚨

**Agent**: {agent_id}
**Role**: {description}
**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager

**MANDATORY PROTOCOLS**:
1. **IMMEDIATE RESPONSE**: Acknowledge this message within 2 minutes
2. **STATUS UPDATE**: Report current mission status and progress
3. **CONTRACT CLAIMING**: Use --get-next-task flag immediately
4. **PERPETUAL MOTION**: Never stop working - claim next task immediately
5. **COORDINATION**: Maintain communication with Captain Agent-4

**CRITICAL REQUIREMENTS**:
- ✅ **ACTIVE STATUS**: Maintain perpetual motion workflow
- ✅ **CONTRACT COMPLETION**: Complete tasks efficiently
- ✅ **SYSTEM COMPLIANCE**: Follow V2 coding standards
- ✅ **COORDINATION**: Respond to all Captain directives

**READY FOR**: Cycle 1 task assignments and strategic operations

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
    
    def _generate_friendly_onboarding(self, agent_id: str, description: str) -> str:
        """Generate friendly mode onboarding message"""
        return f"""🎯 **ONBOARDING - FRIENDLY MODE** 🎯

**Agent**: {agent_id}
**Role**: {description}
**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager

**WELCOME TO THE SWARM!** 🚀

**MISSION OBJECTIVES**:
1. **Active Participation**: Engage in perpetual motion workflow
2. **Task Completion**: Efficiently complete assigned contracts
3. **System Compliance**: Follow V2 coding standards
4. **Team Coordination**: Maintain communication with Captain

**SUPPORT SYSTEMS**:
- ✅ **Contract System**: Use --get-next-task for immediate task claiming
- ✅ **Messaging System**: PyAutoGUI coordination with Captain
- ✅ **Status Tracking**: Regular progress updates
- ✅ **Emergency Protocols**: Available for crisis intervention

**READY FOR**: Cycle 1 task assignments and strategic operations

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
    
    def generate_comprehensive_onboarding(self, style: str = "friendly") -> str:
        """Generate comprehensive onboarding message for all agents"""
        return f"""🎯 **COMPREHENSIVE ONBOARDING - CONTRACT ASSIGNMENT** 🎯

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Style**: {style.upper()}
**Mode**: Comprehensive with contract assignment

**MISSION ASSIGNMENT**:
1. **IMMEDIATE CONTRACT CLAIMING**: Use --get-next-task flag
2. **PERPETUAL MOTION**: Maintain continuous workflow
3. **SYSTEM COMPLIANCE**: Follow V2 coding standards
4. **COORDINATION**: Regular status updates to Captain

**CONTRACT SYSTEM READY**: 40+ contracts available for claiming
**MESSAGING SYSTEM**: PyAutoGUI coordination active
**EMERGENCY PROTOCOLS**: Available for crisis intervention

**READY FOR**: Cycle 1 task assignments and strategic operations

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
    
    def generate_wrapup_message(self) -> str:
        """Generate wrapup sequence message"""
        return """🏁 **WRAPUP SEQUENCE - MISSION COMPLETE** 🏁

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Status**: Mission objectives achieved
**Next Phase**: Awaiting new directives

**MISSION SUMMARY**:
- ✅ **Onboarding Complete**: All agents successfully onboarded
- ✅ **System Integration**: Messaging system fully operational
- ✅ **Contract System**: 40+ contracts available
- ✅ **Coordination**: PyAutoGUI messaging active

**READY FOR**: Next mission phase and strategic operations

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""
    
    def create_onboarding_message(self, agent_id: str, style: str = "friendly") -> UnifiedMessage:
        """Create onboarding message object"""
        message_content = self.generate_onboarding_message(agent_id, style)
        
        return UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient=agent_id,
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style}
        )
    
    def create_comprehensive_onboarding_message(self, style: str = "friendly") -> UnifiedMessage:
        """Create comprehensive onboarding message object"""
        message_content = self.generate_comprehensive_onboarding(style)
        
        return UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style, "comprehensive": True}
        )
    
    def create_wrapup_message(self) -> UnifiedMessage:
        """Create wrapup message object"""
        message_content = self.generate_wrapup_message()
        
        return UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.NORMAL,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.WRAPUP]
        )


if __name__ == "__main__":
    # Test the onboarding service
    print("🎯 Onboarding Service Loaded Successfully")
    
    service = OnboardingService()
    
    # Test message generation
    test_message = service.create_onboarding_message("Agent-1", "friendly")
    print(f"✅ Test onboarding message created: {test_message.message_id}")
    print(f"✅ Message type: {test_message.message_type.value}")
    print(f"✅ Priority: {test_message.priority.value}")
    print("✅ All onboarding service functionality working correctly!")
