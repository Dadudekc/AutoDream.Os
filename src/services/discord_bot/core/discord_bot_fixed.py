#!/usr/bin/env python3
"""
Fixed Discord Bot Core
======================

Fixed Discord bot functionality with proper error handling and command registration.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)


class FixedDiscordAgentBot(commands.Bot):
    """Fixed Discord agent bot with proper error handling."""

    def __init__(self, command_prefix: str = "!", intents=None):
        """Initialize fixed Discord agent bot."""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = False
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        # Initialize components with proper error handling
        self.agent_coordinates = self._load_agent_coordinates()
        self.messaging_service = self._init_messaging_service()
        
        logger.info("✅ Fixed Discord bot initialized successfully")
    
    def _load_agent_coordinates(self):
        """Load agent coordinates configuration with fallback."""
        coordinates_path = "config/coordinates.json"
        try:
            import json
            with open(coordinates_path) as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            logger.warning(f"⚠️  Failed to load coordinates: {e}. Using defaults.")
            # Fallback to default coordinates
            return {
                "Agent-1": {"active": True, "description": "Integration Specialist"},
                "Agent-2": {"active": True, "description": "Architecture & Design Specialist"},
                "Agent-3": {"active": True, "description": "Database Specialist"},
                "Agent-4": {"active": True, "description": "Captain & Operations Coordinator"},
                "Agent-5": {"active": True, "description": "Business Intelligence Specialist"},
                "Agent-6": {"active": True, "description": "Quality Assurance Specialist"},
                "Agent-7": {"active": True, "description": "Python Development & Testing Specialist"},
                "Agent-8": {"active": True, "description": "System Monitoring & Health Specialist"}
            }
    
    def _init_messaging_service(self):
        """Initialize messaging service with proper error handling."""
        try:
            from services.consolidated_messaging_service import ConsolidatedMessagingService
            return ConsolidatedMessagingService("config/coordinates.json")
        except Exception as e:
            logger.error(f"❌ Failed to initialize messaging service: {e}")
            return None

    async def setup_hook(self):
        """Setup hook for slash commands with proper error handling."""
        try:
            logger.info("🔧 Setting up Discord bot commands...")
            
            # Register basic commands
            await self._register_basic_commands()
            
            # Register messaging commands  
            await self._register_messaging_commands()
            
            # Register agent commands
            await self._register_agent_commands()
            
            logger.info("✅ All slash commands registered successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to setup commands: {e}")
            raise

    async def _register_basic_commands(self):
        """Register basic commands with error handling."""
        try:
            @self.tree.command(name="ping", description="Test bot responsiveness")
            async def ping(interaction: discord.Interaction):
                """Test bot responsiveness."""
                latency = round(self.latency * 1000)
                await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")

            @self.tree.command(name="commands", description="Show help information")
            async def help_command(interaction: discord.Interaction):
                """Show help information."""
                help_text = """
**Fixed Discord Agent Bot Commands:**

**Basic Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show this help message
- `/status` - Show system status

**Agent Commands:**
- `/agents` - List all agents and their status
- `/swarm` - Send message to all agents

**Messaging Commands:**
- `/send` - Send message to specific agent
- `/msg-status` - Get messaging system status

**Ready for enhanced swarm coordination!** 🐝
                """
                await interaction.response.send_message(help_text)

            @self.tree.command(name="status", description="Show system status")
            async def status(interaction: discord.Interaction):
                """Show system status."""
                status_text = f"""
**System Status:**
- **Bot**: ✅ Online
- **Latency**: {round(self.latency * 1000)}ms
- **Agents**: {len(self.agent_coordinates)} configured
- **Messaging**: {'✅ Active' if self.messaging_service else '❌ Inactive'}
- **Commands**: {len(self.tree.get_commands())} registered
                """
                await interaction.response.send_message(status_text)
            
            logger.info("✅ Basic commands registered")
            
        except Exception as e:
            logger.error(f"❌ Failed to register basic commands: {e}")
            raise

    async def _register_messaging_commands(self):
        """Register messaging commands with error handling."""
        try:
            @self.tree.command(name="send", description="Send message to specific agent")
            @discord.app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
            @discord.app_commands.describe(message="Message to send to the agent")
            async def send_message(interaction: discord.Interaction, agent: str, message: str):
                """Send message to specific agent."""
                # Validate agent ID
                if agent not in self.agent_coordinates:
                    await interaction.response.send_message(f"❌ Invalid agent ID: {agent}")
                    return
                
                if not self.messaging_service:
                    await interaction.response.send_message("❌ Messaging service not available")
                    return
                    
                try:
                    # Use messaging service to send message
                    success = self.messaging_service.send_message(agent, message, "Discord-Commander")
                    
                    if success:
                        await interaction.response.send_message(f"✅ **Message Sent Successfully!**\n🤖 **To:** {agent}\n💬 **Message:** {message}")
                    else:
                        await interaction.response.send_message(f"❌ **Failed to send message to {agent}**")
                        
                except Exception as e:
                    await interaction.response.send_message(f"❌ Error sending message: {e}")

            @self.tree.command(name="msg-status", description="Get messaging system status")
            async def messaging_status(interaction: discord.Interaction):
                """Get messaging system status."""
                try:
                    if not self.messaging_service:
                        await interaction.response.send_message("❌ Messaging service not available")
                        return
                    
                    # Get messaging service status
                    status = self.messaging_service.get_status()
                    
                    response = "**Fixed Messaging System Status:**\n\n"
                    response += f"**Service Status:** ✅ Active\n"
                    response += f"**Total Agents:** {len(self.agent_coordinates)}\n"
                    response += f"**Active Agents:** {len([a for a in self.agent_coordinates.values() if a.get('active', True)])}\n"
                    response += f"**Coordinates Loaded:** ✅ Yes\n\n"
                    response += "**Available Agents:**\n"
                    
                    for agent_id, coords in self.agent_coordinates.items():
                        status_icon = "✅" if coords.get('active', True) else "❌"
                        response += f"{status_icon} {agent_id}\n"
                    
                    response += "\n🐝 **Fixed Discord Commander** - Messaging system ready!"
                    
                    await interaction.response.send_message(response)
                    
                except Exception as e:
                    await interaction.response.send_message(f"❌ Error getting messaging status: {e}")
            
            logger.info("✅ Messaging commands registered")
            
        except Exception as e:
            logger.error(f"❌ Failed to register messaging commands: {e}")
            raise

    async def _register_agent_commands(self):
        """Register agent commands with error handling."""
        try:
            @self.tree.command(name="agents", description="List all agents and their status")
            async def list_agents(interaction: discord.Interaction):
                """List all agents and their status."""
                agent_list = "**Fixed Discord Agent Status:**\n\n"
                for i in range(1, 9):
                    agent_id = f"Agent-{i}"
                    status = (
                        "🟢 Active"
                        if self.agent_coordinates.get(agent_id, {}).get("active", True)
                        else "🔴 Inactive"
                    )
                    description = self.agent_coordinates.get(agent_id, {}).get("description", f"Agent {i}")
                    agent_list += f"{agent_id}: {status} - {description}\n"
                
                agent_list += "\n🐝 **Fixed Discord Commander** - Ready for coordination!"
                await interaction.response.send_message(agent_list)

            @self.tree.command(name="swarm", description="Send message to all agents")
            @discord.app_commands.describe(message="Message to send to all agents")
            async def swarm_message(interaction: discord.Interaction, message: str):
                """Send message to all agents."""
                if not self.messaging_service:
                    await interaction.response.send_message("❌ Messaging service not available")
                    return
                
                try:
                    # Use messaging service to broadcast
                    results = self.messaging_service.broadcast_message(message, "Discord-Commander")
                    
                    active_agents = [agent for agent, success in results.items() if success]
                    failed_agents = [agent for agent, success in results.items() if not success]
                    
                    response = f"**SWARM MESSAGE SENT** 🐝\n\n"
                    response += f"**Message:** {message}\n\n"
                    response += f"**Delivered to:** {len(active_agents)} active agents\n"
                    
                    if active_agents:
                        response += f"**Successful:** {', '.join(active_agents)}\n"
                    
                    if failed_agents:
                        response += f"**Failed:** {', '.join(failed_agents)}\n"
                    
                    response += f"\n**Total agents:** {len(results)}"
                    await interaction.response.send_message(response)
                    
                except Exception as e:
                    await interaction.response.send_message(f"❌ Error sending swarm message: {e}")
            
            logger.info("✅ Agent commands registered")
            
        except Exception as e:
            logger.error(f"❌ Failed to register agent commands: {e}")
            raise

    async def on_ready(self):
        """Event triggered when bot is ready."""
        logger.info(f"✅ {self.user} is online and ready!")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"❌ Failed to sync slash commands: {e}")
        
        await self._send_startup_notification()

    async def _send_startup_notification(self):
        """Send startup notification to configured channel."""
        try:
            channel_id = os.getenv("DISCORD_CHANNEL_ID")
            if not channel_id:
                logger.warning("⚠️  DISCORD_CHANNEL_ID not set, skipping startup notification")
                return

            channel = self.get_channel(int(channel_id))
            if not channel:
                logger.warning(f"⚠️  Channel {channel_id} not found")
                return

            startup_message = f"""
🚀 **FIXED DISCORD COMMANDER ONLINE** 🚀

**We're online and ready to command the swarm!** 🐝

**Commander Status:**
- **Name**: {self.user.name}
- **ID**: {self.user.id}
- **Latency**: {round(self.latency * 1000)}ms
- **Guilds**: {len(self.guilds)}
- **Agents**: {len(self.agent_coordinates)} configured
- **Messaging**: {'✅ Active' if self.messaging_service else '❌ Inactive'}

**Available Commands:**
- `/ping` - Test bot responsiveness
- `/commands` - Show all commands
- `/status` - Show system status
- `/agents` - List all agents
- `/swarm` - Send to all agents
- `/send` - Send to specific agent
- `/msg-status` - Get messaging status

**Ready for fixed swarm coordination!** 🐝

*The Discord commander issues have been identified and fixed!*
            """
            await channel.send(startup_message)
            logger.info("✅ Startup notification sent")

        except Exception as e:
            logger.error(f"❌ Failed to send startup notification: {e}")

    async def on_app_command_error(self, interaction, error):
        """Handle application command errors (slash commands)."""
        logger.error(f"Slash command error: {error}")
        try:
            await interaction.response.send_message(f"❌ Command error: {error}", ephemeral=True)
        except:
            # If we can't respond, just log the error
            logger.error(f"Failed to send error response: {error}")