#!/usr/bin/env python3
"""
Swarm Command Handlers - V2 Compliant Module
============================================

Swarm-wide command handlers for Discord Agent Bot.
V2 COMPLIANT: Swarm command handling under 200 lines.

Features:
- Broadcast message handling
- Urgent message processing
- Swarm coordination commands
- Multi-agent communication

Author: Agent-3 (Quality Assurance Co-Captain) - V2 Refactoring
License: MIT
"""

import asyncio
from typing import Any, Dict, List

try:
    from ..services.consolidated_messaging_service import ConsolidatedMessagingService
    from ..models.messaging_models import UnifiedMessage
    from ..models.messaging_enums import UnifiedMessageType, UnifiedMessagePriority
except ImportError:
    # Fallback for direct execution
    from src.services.consolidated_messaging_service import ConsolidatedMessagingService
    from src.services.messaging.models.messaging_models import UnifiedMessage
    from src.services.messaging.models.messaging_enums import UnifiedMessageType, UnifiedMessagePriority


class SwarmCommandHandlers:
    """Handlers for swarm-wide Discord commands."""

    def __init__(self, agent_engine, embed_manager):
        """Initialize swarm command handlers."""
        self.agent_engine = agent_engine
        self.embed_manager = embed_manager
        self.active_broadcasts = 0
        self.max_concurrent_broadcasts = 3

    async def handle_swarm_command(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle swarm broadcast command."""
        try:
            message = context.get("message", "")
            sender = context.get("sender", "Discord User")
            
            if not message.strip():
                return {
                    "embed": self.embed_manager.create_response_embed(
                        "error",
                        title="❌ Empty Message",
                        description="Please provide a message to broadcast to all agents."
                    )
                }
            
            # Check concurrent broadcast limit
            if self.active_broadcasts >= self.max_concurrent_broadcasts:
                return {
                    "embed": self.embed_manager.create_response_embed(
                        "error",
                        title="❌ Too Many Broadcasts",
                        description="Maximum concurrent broadcasts reached. Please wait."
                    )
                }
            
            self.active_broadcasts += 1
            
            try:
                # Execute broadcast
                result = await self.execute_swarm_broadcast(message, sender)
                
                if result.success:
                    return {
                        "embed": self.embed_manager.create_response_embed(
                            "success",
                            title="✅ Swarm Broadcast Sent",
                            description=f"Message broadcasted to {result.data.get('recipient_count', 0)} agents",
                            data=result.data
                        )
                    }
                else:
                    return {
                        "embed": self.embed_manager.create_response_embed(
                            "error",
                            title="❌ Broadcast Failed",
                            description=result.message
                        )
                    }
            finally:
                self.active_broadcasts -= 1
                
        except Exception as e:
            self.active_broadcasts -= 1
            return {
                "embed": self.embed_manager.create_response_embed(
                    "error",
                    title="❌ Broadcast Error",
                    description=f"Error sending swarm broadcast: {str(e)}"
                )
            }

    async def handle_urgent_command(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle urgent broadcast command."""
        try:
            message = context.get("message", "")
            sender = context.get("sender", "Discord User")
            
            if not message.strip():
                return {
                    "embed": self.embed_manager.create_response_embed(
                        "error",
                        title="❌ Empty Message",
                        description="Please provide an urgent message to broadcast to all agents."
                    )
                }
            
            # Check concurrent broadcast limit
            if self.active_broadcasts >= self.max_concurrent_broadcasts:
                return {
                    "embed": self.embed_manager.create_response_embed(
                        "error",
                        title="❌ Too Many Broadcasts",
                        description="Maximum concurrent broadcasts reached. Please wait."
                    )
                }
            
            self.active_broadcasts += 1
            
            try:
                # Execute urgent broadcast
                result = await self.execute_urgent_broadcast(message, sender)
                
                if result.success:
                    return {
                        "embed": self.embed_manager.create_response_embed(
                            "success",
                            title="🚨 Urgent Broadcast Sent",
                            description=f"Urgent message broadcasted to {result.data.get('recipient_count', 0)} agents",
                            data=result.data
                        )
                    }
                else:
                    return {
                        "embed": self.embed_manager.create_response_embed(
                            "error",
                            title="❌ Urgent Broadcast Failed",
                            description=result.message
                        )
                    }
            finally:
                self.active_broadcasts -= 1
                
        except Exception as e:
            self.active_broadcasts -= 1
            return {
                "embed": self.embed_manager.create_response_embed(
                    "error",
                    title="❌ Urgent Broadcast Error",
                    description=f"Error sending urgent broadcast: {str(e)}"
                )
            }

    async def execute_swarm_broadcast(self, message: str, sender: str) -> 'CommandResult':
        """Execute swarm broadcast to all agents."""
        try:
            # Try to use the consolidated messaging system
            try:
                from ..services.consolidated_messaging_service import broadcast_message
            except ImportError:
                from src.services.consolidated_messaging_service import broadcast_message

            print(f"📢 Executing swarm broadcast: {message}")

            # Use the consolidated messaging system for broadcast
            results = broadcast_message(message, sender)
            
            successful_count = sum(1 for success in results.values() if success)
            total_count = len(results)

            return CommandResult(
                success=True,
                message=f"Swarm broadcast delivered to {successful_count}/{total_count} agents",
                data={
                    "successful_deliveries": successful_count,
                    "total_agents": total_count,
                    "method": "consolidated_messaging",
                    "results": results
                }
            )
            
        except Exception as e:
            print(f"❌ Swarm broadcast error: {e}")
            return CommandResult(
                success=False,
                message=f"Swarm broadcast failed: {str(e)}",
                data={"error": str(e)}
            )

    async def execute_urgent_broadcast(self, message: str, sender: str) -> 'CommandResult':
        """Execute urgent broadcast to all agents with high priority."""
        try:
            # Try to use the consolidated messaging system
            try:
                from ..services.consolidated_messaging_service import broadcast_message
            except ImportError:
                from src.services.consolidated_messaging_service import broadcast_message

            print(f"🚨 Executing URGENT broadcast: {message}")

            # Create urgent message with high priority
            urgent_message = f"🚨 URGENT: {message}"

            # Use the consolidated messaging system for urgent broadcast
            results = broadcast_message(urgent_message, sender, priority="urgent")
            
            successful_count = sum(1 for success in results.values() if success)
            total_count = len(results)

            return CommandResult(
                success=True,
                message=f"Urgent broadcast delivered to {successful_count}/{total_count} agents",
                data={
                    "successful_deliveries": successful_count,
                    "total_agents": total_count,
                    "method": "consolidated_messaging_urgent",
                    "results": results
                }
            )
            
        except Exception as e:
            print(f"❌ Urgent broadcast error: {e}")
            return CommandResult(
                success=False,
                message=f"Urgent broadcast failed: {str(e)}",
                data={"error": str(e)}
            )

    async def handle_urgent_followup(self, command_id: str, result: 'CommandResult') -> Dict[str, Any]:
        """Handle urgent broadcast followup processing."""
        try:
            if result.success:
                return {
                    "edit": True,
                    "embed": self.embed_manager.create_response_embed(
                        "success",
                        title="🚨 Urgent Broadcast Complete",
                        description=f"Urgent message delivered to {result.data.get('successful_deliveries', 0)} agents",
                        data=result.data
                    )
                }
            else:
                return {
                    "edit": True,
                    "embed": self.embed_manager.create_response_embed(
                        "error",
                        title="❌ Urgent Broadcast Failed",
                        description=result.message
                    )
                }
        except Exception as e:
            return {
                "edit": True,
                "embed": self.embed_manager.create_response_embed(
                    "error",
                    title="❌ Followup Error",
                    description=f"Error processing urgent broadcast followup: {str(e)}"
                )
            }

    def get_active_broadcast_count(self) -> int:
        """Get number of active broadcasts."""
        return self.active_broadcasts


class CommandResult:
    """Result of a command execution."""
    
    def __init__(self, success: bool, message: str, data: Dict[str, Any] = None):
        """Initialize command result."""
        self.success = success
        self.message = message
        self.data = data or {}

