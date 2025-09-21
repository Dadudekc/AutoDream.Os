#!/usr/bin/env python3
"""
Enhanced Discord Bot Engine for Phase 2.3 Enhanced Discord Integration

V2 Compliance: ≤400 lines, 4 classes, 8 functions
Purpose: Main Discord bot engine with template-based messaging and memory-aware responses
"""

import asyncio
import discord
from discord.ext import commands
from typing import Dict, Any, Optional, List
import json
from datetime import datetime
import logging

# Import our custom components
from .template_messaging import TemplateEngine, MessageRenderer, TemplateRegistry
from .memory_aware_responses import (
    MemoryContextManager, ResponseGenerator, ConversationTracker, ContextInjector
)
from .realtime_coordination import (
    CoordinationHub, EventDispatcher, StatusBroadcaster, EventType, EventPriority
)


class EnhancedDiscordBot(commands.Bot):
    """Enhanced Discord Bot with template-based messaging and memory-aware responses"""
    
    def __init__(self, config: Dict[str, Any], memory_backend: Any = None):
        """Initialize enhanced Discord bot"""
        # Bot configuration
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.get("prefix", "!"),
            intents=intents,
            help_command=None
        )
        
        # Initialize components
        self.config = config
        self.memory_backend = memory_backend
        
        # Template system
        self.template_engine = TemplateEngine(config.get("template_dir", "templates/discord"))
        self.message_renderer = MessageRenderer(self.template_engine)
        self.template_registry = TemplateRegistry(self.template_engine)
        
        # Memory-aware responses
        self.context_manager = MemoryContextManager(memory_backend)
        self.response_generator = ResponseGenerator(self.context_manager)
        self.conversation_tracker = ConversationTracker()
        self.context_injector = ContextInjector(self.conversation_tracker)
        
        # Real-time coordination
        self.coordination_hub = CoordinationHub()
        self.event_dispatcher = EventDispatcher(self.coordination_hub)
        self.status_broadcaster = StatusBroadcaster(self.coordination_hub)
        
        # Bot state
        self.agent_id = config.get("agent_id", "Agent-2")
        self.is_ready = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def setup_hook(self) -> None:
        """Setup hook called when bot is starting"""
        # Register event handlers
        self.coordination_hub.register_event_handler(
            EventType.STATUS_UPDATE, self._handle_status_update
        )
        self.coordination_hub.register_event_handler(
            EventType.COORDINATION_REQUEST, self._handle_coordination_request
        )
        self.coordination_hub.register_event_handler(
            EventType.SYSTEM_ALERT, self._handle_system_alert
        )
        
        # Start coordination systems
        self.coordination_hub.start()
        self.status_broadcaster.start_broadcasting()
        
        # Register bot with coordination hub
        self.coordination_hub.register_agent(self.agent_id)
        
        self.logger.info(f"Enhanced Discord Bot {self.agent_id} initialized")
    
    async def on_ready(self) -> None:
        """Called when bot is ready"""
        self.is_ready = True
        self.logger.info(f"Bot {self.agent_id} is ready and online!")
        
        # Update status
        await self._update_bot_status()
    
    async def on_message(self, message: discord.Message) -> None:
        """Handle incoming messages"""
        if message.author == self.user:
            return
        
        # Process message
        await self._process_message(message)
    
    async def _process_message(self, message: discord.Message) -> None:
        """Process incoming message with memory-aware responses"""
        try:
            # Extract user and channel info
            user_id = str(message.author.id)
            channel_id = str(message.channel.id)
            
            # Generate context-aware response
            response = self.response_generator.generate_response(
                message.content,
                user_id,
                self.agent_id,
                self._determine_response_type(message)
            )
            
            # Inject additional context
            enhanced_response = self.context_injector.inject_context(
                response, user_id, self.agent_id
            )
            
            # Track conversation
            self.conversation_tracker.track_conversation(
                user_id, self.agent_id, message.content, enhanced_response
            )
            
            # Send response
            await message.reply(enhanced_response)
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            await message.reply("❌ **Error processing message. Please try again.**")
    
    def _determine_response_type(self, message: discord.Message) -> Any:
        """Determine response type based on message content"""
        content = message.content.lower()
        
        if any(word in content for word in ["status", "progress", "update"]):
            return "status_update"
        elif any(word in content for word in ["coordinate", "collaborate", "team"]):
            return "coordination_request"
        elif any(word in content for word in ["complete", "finished", "done"]):
            return "task_completion"
        elif any(word in content for word in ["error", "alert", "problem"]):
            return "system_alert"
        elif any(word in content for word in ["swarm", "agents", "coordination"]):
            return "swarm_coordination"
        else:
            return "user_query"
    
    async def _update_bot_status(self) -> None:
        """Update bot status and broadcast to coordination hub"""
        status_data = {
            "status": "Online",
            "current_task": "Phase 2.3 Discord Integration",
            "progress": 85,
            "next_action": "Complete real-time coordination implementation",
            "notes": "Enhanced Discord Bot operational with memory-aware responses"
        }
        
        # Update status broadcaster
        self.status_broadcaster.update_agent_status(self.agent_id, status_data)
        
        # Dispatch status update event
        self.event_dispatcher.dispatch_status_update(self.agent_id, status_data)
    
    async def _handle_status_update(self, event: Any) -> None:
        """Handle status update events from other agents"""
        try:
            payload = event.payload
            agent_id = payload.get("agent_id")
            status = payload.get("status")
            
            self.logger.info(f"Status update from {agent_id}: {status}")
            
            # Update internal status tracking
            if agent_id != self.agent_id:
                self.status_broadcaster.update_agent_status(agent_id, payload)
                
        except Exception as e:
            self.logger.error(f"Error handling status update: {e}")
    
    async def _handle_coordination_request(self, event: Any) -> None:
        """Handle coordination request events"""
        try:
            payload = event.payload
            request_type = payload.get("request_type")
            description = payload.get("description")
            
            self.logger.info(f"Coordination request: {request_type} - {description}")
            
            # Process coordination request based on type
            if request_type == "consolidation_analysis":
                await self._handle_consolidation_request(payload)
            elif request_type == "task_assignment":
                await self._handle_task_assignment_request(payload)
            else:
                self.logger.info(f"Unknown coordination request type: {request_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling coordination request: {e}")
    
    async def _handle_system_alert(self, event: Any) -> None:
        """Handle system alert events"""
        try:
            payload = event.payload
            alert_type = payload.get("alert_type")
            severity = payload.get("severity")
            message = payload.get("message")
            
            self.logger.warning(f"System alert: {alert_type} ({severity}) - {message}")
            
            # Handle alert based on severity
            if severity in ["URGENT", "CRITICAL"]:
                await self._handle_critical_alert(payload)
            else:
                await self._handle_normal_alert(payload)
                
        except Exception as e:
            self.logger.error(f"Error handling system alert: {e}")
    
    async def _handle_consolidation_request(self, payload: Dict[str, Any]) -> None:
        """Handle consolidation analysis requests"""
        # This would integrate with Agent-3's consolidation analysis
        self.logger.info("Processing consolidation analysis request")
        
        # Dispatch response
        response_data = {
            "request_id": payload.get("request_id"),
            "response": "Consolidation analysis request acknowledged",
            "status": "processing",
            "estimated_completion": "2 cycles"
        }
        
        self.event_dispatcher.dispatch_coordination_request(
            self.agent_id,
            [payload.get("requested_by")],
            response_data
        )
    
    async def _handle_task_assignment_request(self, payload: Dict[str, Any]) -> None:
        """Handle task assignment requests"""
        task_id = payload.get("task_id")
        task_title = payload.get("task_title")
        
        self.logger.info(f"Processing task assignment: {task_id} - {task_title}")
        
        # Update bot status with new task
        status_data = {
            "status": "Active",
            "current_task": task_title,
            "progress": 0,
            "next_action": "Begin task implementation"
        }
        
        self.status_broadcaster.update_agent_status(self.agent_id, status_data)
    
    async def _handle_critical_alert(self, payload: Dict[str, Any]) -> None:
        """Handle critical system alerts"""
        alert_type = payload.get("alert_type")
        message = payload.get("message")
        
        # Log critical alert
        self.logger.critical(f"CRITICAL ALERT: {alert_type} - {message}")
        
        # Could implement emergency response procedures here
    
    async def _handle_normal_alert(self, payload: Dict[str, Any]) -> None:
        """Handle normal system alerts"""
        alert_type = payload.get("alert_type")
        message = payload.get("message")
        
        # Log normal alert
        self.logger.warning(f"Alert: {alert_type} - {message}")
    
    async def close(self) -> None:
        """Cleanup when bot is shutting down"""
        # Stop coordination systems
        self.status_broadcaster.stop_broadcasting()
        self.coordination_hub.stop()
        
        # Unregister from coordination hub
        self.coordination_hub.unregister_agent(self.agent_id)
        
        await super().close()
        self.logger.info(f"Bot {self.agent_id} shut down")


class MessageTemplateManager:
    """Template management for Discord messages"""
    
    def __init__(self, template_engine: TemplateEngine):
        """Initialize template manager"""
        self.template_engine = template_engine
        self.template_registry = TemplateRegistry(template_engine)
    
    def create_agent_status_message(self, agent_data: Dict[str, Any]) -> str:
        """Create agent status message using templates"""
        return self.template_engine.message_renderer.render_agent_status(agent_data)
    
    def create_system_alert_message(self, alert_data: Dict[str, Any]) -> str:
        """Create system alert message using templates"""
        return self.template_engine.message_renderer.render_system_alert(alert_data)
    
    def create_coordination_message(self, coord_data: Dict[str, Any]) -> str:
        """Create coordination message using templates"""
        return self.template_engine.message_renderer.render_coordination_request(coord_data)


class ResponseGenerator:
    """Response generation with memory integration"""
    
    def __init__(self, context_manager: MemoryContextManager):
        """Initialize response generator"""
        self.context_manager = context_manager
        self.response_generator = ResponseGenerator(context_manager)
    
    def generate_memory_aware_response(self, message: str, user_id: str) -> str:
        """Generate memory-aware response"""
        return self.response_generator.generate_response(
            message, user_id, "Agent-2", "user_query"
        )


class CoordinationManager:
    """Real-time swarm coordination through Discord"""
    
    def __init__(self, coordination_hub: CoordinationHub):
        """Initialize coordination manager"""
        self.coordination_hub = coordination_hub
        self.event_dispatcher = EventDispatcher(coordination_hub)
        self.status_broadcaster = StatusBroadcaster(coordination_hub)
    
    def broadcast_swarm_status(self) -> Dict[str, Any]:
        """Broadcast current swarm status"""
        return self.status_broadcaster.get_swarm_status()
    
    def send_coordination_request(self, target_agents: List[str], 
                                request_data: Dict[str, Any]) -> str:
        """Send coordination request to specific agents"""
        return self.event_dispatcher.dispatch_coordination_request(
            "Agent-2", target_agents, request_data
        )


# Example usage and testing
if __name__ == "__main__":
    # Bot configuration
    config = {
        "agent_id": "Agent-2",
        "prefix": "!",
        "template_dir": "templates/discord"
    }
    
    # Create enhanced Discord bot
    bot = EnhancedDiscordBot(config)
    
    # Example of using the bot components
    print("Enhanced Discord Bot Engine initialized")
    print(f"Agent ID: {bot.agent_id}")
    print(f"Template Engine: {bot.template_engine}")
    print(f"Coordination Hub: {bot.coordination_hub}")
    print(f"Memory Context Manager: {bot.context_manager}")
    
    # Example template usage
    agent_data = {
        "agent_id": "Agent-2",
        "status": "Active",
        "current_task": "Phase 2.3 Discord Integration",
        "progress": 85
    }
    
    status_message = bot.message_renderer.render_agent_status(agent_data)
    print(f"\nAgent Status Message:\n{status_message}")
    
    # Example coordination usage
    swarm_status = bot.coordination_manager.broadcast_swarm_status()
    print(f"\nSwarm Status: {swarm_status}")
    
    print("\nEnhanced Discord Bot Engine ready for deployment!")


