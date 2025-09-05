"""
Onboarding Handler - V2 Compliant Module
=======================================

Handles onboarding-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional

from ..messaging_core import UnifiedMessagingCore
from ..models.messaging_models import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, SenderType, RecipientType
)
from ..unified_messaging_imports import load_coordinates_from_json


class OnboardingHandler:
    """
    Handles onboarding-related commands for messaging CLI.
    
    Manages agent onboarding and welcome message distribution.
    """
    
    def __init__(self):
        """Initialize onboarding handler."""
        self.messaging_core = UnifiedMessagingCore()
        self.onboarded_agents = set()
        self.onboarding_history = []
    
    def handle_onboarding_commands(self, args) -> bool:
        """Handle onboarding-related commands."""
        try:
            if args.onboarding:
                return self._handle_bulk_onboarding(args)
                
            if args.onboard:
                if not args.agent:
                    print("❌ Error: --agent required for --onboard")
                    return True
                
                return self._handle_single_onboarding(args)
                
        except Exception as e:
            print(f"❌ Error handling onboarding command: {e}")
            return False
        
        return False
    
    def _handle_bulk_onboarding(self, args) -> bool:
        """Handle bulk onboarding to all agents."""
        try:
            print("🚀 Starting bulk onboarding...")
            # Load coordinates
            agents = load_coordinates_from_json()
            if not agents:
                print("❌ No agent coordinates found")
                return True
            
            # Send onboarding to all agents
            success_count = 0
            
            for agent_id in agents.keys():
                message = self.messaging_core.create_message(
                    content=f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM.",
                    sender="Captain Agent-4",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.ONBOARDING,
                    priority=UnifiedMessagePriority.REGULAR,
                    tags=[UnifiedMessageTag.ONBOARDING],
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT
                )
                
                if message:
                    success = self.messaging_core.send_message(message, mode=args.mode)
                    if success:
                        success_count += 1
                        self.onboarded_agents.add(agent_id)
                        print(f"✅ Onboarding sent to {agent_id}")
                    else:
                        print(f"❌ Failed to send onboarding to {agent_id}")
                else:
                    print(f"❌ Failed to create onboarding message for {agent_id}")
            
            print(f"📊 Onboarding complete: {success_count}/{len(agents)} agents")
            return True
            
        except Exception as e:
            print(f"❌ Error in bulk onboarding: {e}")
            return False
    
    def _handle_single_onboarding(self, args) -> bool:
        """Handle single agent onboarding."""
        try:
            print(f"🚀 Onboarding {args.agent}...")
            
            message = self.messaging_core.create_message(
                content=f"Welcome to the team, {args.agent}! You are now part of the V2 SWARM.",
                sender="Captain Agent-4",
                recipient=args.agent,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=args.mode)
                if success:
                    self.onboarded_agents.add(args.agent)
                    print(f"✅ Onboarding sent to {args.agent}")
                    return True
                else:
                    print(f"❌ Failed to send onboarding to {args.agent}")
                    return False
            else:
                print(f"❌ Failed to create onboarding message for {args.agent}")
                return False
                
        except Exception as e:
            print(f"❌ Error in single onboarding: {e}")
            return False
    
    def onboard_agent(self, agent_id: str, mode: str = "pyautogui") -> bool:
        """Onboard a specific agent."""
        try:
            message = self.messaging_core.create_message(
                content=f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM.",
                sender="Captain Agent-4",
                recipient=agent_id,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.ONBOARDING],
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT
            )
            
            if message:
                success = self.messaging_core.send_message(message, mode=mode)
                if success:
                    self.onboarded_agents.add(agent_id)
                    self.onboarding_history.append({
                        "agent_id": agent_id,
                        "timestamp": "now",
                        "status": "success"
                    })
                    return True
                else:
                    self.onboarding_history.append({
                        "agent_id": agent_id,
                        "timestamp": "now",
                        "status": "failed"
                    })
                    return False
            return False
            
        except Exception as e:
            print(f"❌ Error onboarding agent {agent_id}: {e}")
            return False
    
    def get_onboarded_agents(self) -> List[str]:
        """Get list of onboarded agents."""
        return list(self.onboarded_agents)
    
    def get_onboarding_history(self) -> List[Dict[str, Any]]:
        """Get onboarding history."""
        return self.onboarding_history.copy()
    
    def is_agent_onboarded(self, agent_id: str) -> bool:
        """Check if agent is onboarded."""
        return agent_id in self.onboarded_agents
    
    def get_onboarding_status(self) -> Dict[str, Any]:
        """Get onboarding handler status."""
        return {
            "onboarded_count": len(self.onboarded_agents),
            "history_count": len(self.onboarding_history),
            "onboarded_agents": list(self.onboarded_agents)
        }
    
    def reset_onboarding(self):
        """Reset onboarding data."""
        self.onboarded_agents.clear()
        self.onboarding_history.clear()
