#!/usr/bin/env python3
"""
Agent Communication Engine
===========================

Enhanced agent communication system for Discord bot integration.
"""

import asyncio
import logging
import json
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    """Message status."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class AgentMessage:
    """Agent message structure."""
    id: str
    from_agent: str
    to_agent: str
    content: str
    priority: MessagePriority
    timestamp: float
    status: MessageStatus
    metadata: Dict[str, Any]
    response_required: bool = False
    response_timeout: float = 300.0  # 5 minutes default


@dataclass
class AgentStatus:
    """Agent status information."""
    agent_id: str
    online: bool
    last_seen: float
    capabilities: List[str]
    current_task: Optional[str]
    performance_metrics: Dict[str, Any]


class AgentCommunicationEngine:
    """Enhanced agent communication engine."""
    
    def __init__(self, bot, messaging_service):
        """Initialize agent communication engine."""
        self.bot = bot
        self.messaging_service = messaging_service
        self.agents: Dict[str, AgentStatus] = {}
        self.message_queue: List[AgentMessage] = []
        self.message_history: List[AgentMessage] = []
        self.communication_callbacks: Dict[str, Callable] = {}
        self.broadcast_channels: Dict[str, str] = {}
        
        # Load agent configuration
        self._load_agent_config()
        
        # Initialize communication monitoring
        self._init_communication_monitoring()
        
        logger.info("✅ Agent Communication Engine initialized")
    
    def _load_agent_config(self):
        """Load agent configuration."""
        try:
            # Load from bot's agent coordinates
            for agent_id, config in self.bot.agent_coordinates.items():
                self.agents[agent_id] = AgentStatus(
                    agent_id=agent_id,
                    online=config.get("active", True),
                    last_seen=time.time(),
                    capabilities=config.get("capabilities", []),
                    current_task=None,
                    performance_metrics={}
                )
            
            logger.info(f"✅ Loaded {len(self.agents)} agents")
        except Exception as e:
            logger.error(f"❌ Failed to load agent config: {e}")
    
    def _init_communication_monitoring(self):
        """Initialize communication monitoring."""
        # Start background monitoring task
        asyncio.create_task(self._monitor_agent_communication())
        logger.info("✅ Communication monitoring initialized")
    
    async def _monitor_agent_communication(self):
        """Monitor agent communication in background."""
        while True:
            try:
                await self._process_message_queue()
                await self._update_agent_status()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"❌ Error in communication monitoring: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _process_message_queue(self):
        """Process pending messages in queue."""
        current_time = time.time()
        processed_messages = []
        
        for message in self.message_queue:
            try:
                # Check for timeout
                if current_time - message.timestamp > message.response_timeout:
                    message.status = MessageStatus.TIMEOUT
                    processed_messages.append(message)
                    continue
                
                # Send message
                success = await self._send_agent_message(message)
                if success:
                    message.status = MessageStatus.SENT
                    processed_messages.append(message)
                else:
                    message.status = MessageStatus.FAILED
                    processed_messages.append(message)
                    
            except Exception as e:
                logger.error(f"❌ Error processing message {message.id}: {e}")
                message.status = MessageStatus.FAILED
                processed_messages.append(message)
        
        # Move processed messages to history
        for message in processed_messages:
            self.message_queue.remove(message)
            self.message_history.append(message)
    
    async def _send_agent_message(self, message: AgentMessage) -> bool:
        """Send message to specific agent."""
        try:
            # Use existing messaging service
            success = self.messaging_service.send_message(
                message.to_agent,
                message.content,
                message.from_agent
            )
            
            if success:
                # Update agent last seen
                if message.to_agent in self.agents:
                    self.agents[message.to_agent].last_seen = time.time()
                
                # Trigger callback if registered
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to {message.to_agent}: {e}")
            return False
    
    async def _update_agent_status(self):
        """Update agent status information."""
        current_time = time.time()
        
        for agent_id, status in self.agents.items():
            # Check if agent is online (last seen within 5 minutes)
            status.online = (current_time - status.last_seen) < 300
            
            # Update performance metrics
            status.performance_metrics.update({
                "last_check": current_time,
                "uptime": current_time - status.last_seen if status.online else 0
            })
    
    async def send_message(self, from_agent: str, to_agent: str, content: str, 
                          priority: MessagePriority = MessagePriority.NORMAL,
                          response_required: bool = False,
                          timeout: float = 300.0) -> str:
        """Send message to agent."""
        message_id = f"{from_agent}_{to_agent}_{int(time.time())}"
        
        message = AgentMessage(
            id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            priority=priority,
            timestamp=time.time(),
            status=MessageStatus.PENDING,
            metadata={},
            response_required=response_required,
            response_timeout=timeout
        )
        
        # Add to queue
        self.message_queue.append(message)
        
        # Process immediately for high priority messages
        if priority in [MessagePriority.HIGH, MessagePriority.URGENT]:
            await self._process_message_queue()
        
        logger.info(f"📤 Message queued: {message_id} ({priority.value})")
        return message_id
    
    async def broadcast_message(self, from_agent: str, content: str, 
                               priority: MessagePriority = MessagePriority.NORMAL,
                               exclude_agents: List[str] = None) -> List[str]:
        """Broadcast message to all agents."""
        if exclude_agents is None:
            exclude_agents = []
        
        message_ids = []
        
        for agent_id in self.agents:
            if agent_id not in exclude_agents and agent_id != from_agent:
                message_id = await self.send_message(
                    from_agent, agent_id, content, priority
                )
                message_ids.append(message_id)
        
        logger.info(f"📢 Broadcast sent to {len(message_ids)} agents")
        return message_ids
    
    async def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get agent status."""
        return self.agents.get(agent_id)
    
    async def get_all_agent_status(self) -> Dict[str, AgentStatus]:
        """Get all agent status."""
        return self.agents.copy()
    
    async def register_communication_callback(self, from_agent: str, to_agent: str, 
                                            callback: Callable):
        """Register callback for agent communication."""
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
    
    async def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics."""
        total_messages = len(self.message_history)
        successful_messages = len([m for m in self.message_history if m.status == MessageStatus.SENT])
        failed_messages = len([m for m in self.message_history if m.status == MessageStatus.FAILED])
        
        return {
            "total_messages": total_messages,
            "successful_messages": successful_messages,
            "failed_messages": failed_messages,
            "success_rate": (successful_messages / total_messages * 100) if total_messages > 0 else 0,
            "active_agents": len([a for a in self.agents.values() if a.online]),
            "total_agents": len(self.agents),
            "pending_messages": len(self.message_queue)
        }
    
    async def get_message_history(self, limit: int = 50) -> List[AgentMessage]:
        """Get recent message history."""
        return self.message_history[-limit:] if self.message_history else []
    
    async def create_discord_embed(self, title: str, description: str, 
                                 color: discord.Color = discord.Color.blue()) -> discord.Embed:
        """Create Discord embed for agent communication."""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        
        # Add agent status fields
        stats = await self.get_communication_stats()
        embed.add_field(
            name="Active Agents",
            value=f"{stats['active_agents']}/{stats['total_agents']}",
            inline=True
        )
        embed.add_field(
            name="Success Rate",
            value=f"{stats['success_rate']:.1f}%",
            inline=True
        )
        embed.add_field(
            name="Pending Messages",
            value=str(stats['pending_messages']),
            inline=True
        )
        
        embed.set_footer(text="🐝 WE ARE SWARM - Agent Communication Engine")
        return embed
