#!/usr/bin/env python3
"""
Discord Views Controller - Fixed Compatibility Launcher
======================================================

Launches the Discord Commander with full GUI views controller integration.
Fixed for Discord.py 2.5.2 compatibility.

Features:
- Interactive agent messaging with dropdowns and modals
- Real-time swarm status monitoring with refresh buttons
- Broadcast messaging to all agents
- Agent selection and communication interface
- Comprehensive error handling and logging
- Discord.py 2.5.2 compatibility

V2 Compliance: ≤400 lines, focused launcher tool
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.services.discord_commander.core import DiscordConfig, DiscordConnectionManager
from src.services.discord_commander.messaging_controller import DiscordMessagingController
from src.services.messaging_service import ConsolidatedMessagingService

# Discord imports with error handling
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logger = logging.getLogger(__name__)


class DiscordViewsControllerBot(commands.Bot):
    """Discord bot with views controller integration."""
    
    def __init__(self, config: DiscordConfig):
        """Initialize the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.messaging_service = ConsolidatedMessagingService()
        self.messaging_controller = DiscordMessagingController(self.messaging_service)
        self.logger = logging.getLogger(__name__)
    
    async def on_ready(self):
        """Bot ready event."""
        self.logger.info(f'Discord Views Controller Bot ready: {self.user}')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="the swarm with interactive GUI 🤖"
            )
        )
        
        # Register commands
        await self._register_commands()
        
        self.logger.info("Discord Views Controller Bot initialized successfully!")
    
    async def _register_commands(self):
        """Register Discord commands with views."""
        
        @self.command(name="agent_interact")
        async def agent_interact(ctx):
            """Interactive agent messaging interface."""
            try:
                embed = discord.Embed(
                    title="🤖 Agent Messaging Interface",
                    description="Select an agent below to send a message",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(
                    name="How to use",
                    value="1. Select an agent from the dropdown\n2. Type your message in the modal\n3. Set priority if needed",
                    inline=False
                )
                
                view = self.messaging_controller.create_agent_messaging_view()
                await ctx.send(embed=embed, view=view)
                
            except Exception as e:
                self.logger.error(f"Error in agent_interact command: {e}")
                await ctx.send(f"❌ Error creating interface: {str(e)}")
        
        @self.command(name="swarm_status")
        async def swarm_status(ctx):
            """View current swarm status."""
            try:
                view = self.messaging_controller.create_swarm_status_view()
                embed = await view._create_status_embed()
                
                await ctx.send(embed=embed, view=view)
                
            except Exception as e:
                self.logger.error(f"Error in swarm_status command: {e}")
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error getting swarm status: {str(e)}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                await ctx.send(embed=embed)
        
        @self.command(name="broadcast")
        async def broadcast(ctx, *, message: str):
            """Broadcast message to all agents."""
            try:
                # Broadcast message
                success = await self.messaging_controller.broadcast_to_swarm(
                    message=message,
                    priority="NORMAL"
                )
                
                if success:
                    embed = discord.Embed(
                        title="✅ Broadcast Sent",
                        description="Message broadcasted to all agents",
                        color=discord.Color.green(),
                        timestamp=discord.utils.utcnow()
                    )
                    embed.add_field(name="Message", value=message[:500], inline=False)
                    embed.add_field(name="From", value=ctx.author.display_name, inline=True)
                    
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Broadcast Failed",
                        description="Failed to broadcast message to agents",
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                    await ctx.send(embed=embed)
                    
            except Exception as e:
                self.logger.error(f"Error in broadcast command: {e}")
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error broadcasting message: {str(e)}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                await ctx.send(embed=embed)
        
        @self.command(name="agent_list")
        async def agent_list(ctx):
            """List all available agents."""
            try:
                agent_status = self.messaging_controller.get_agent_status()
                
                if not agent_status:
                    embed = discord.Embed(
                        title="❌ No Agents Found",
                        description="No agents are currently available",
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                    await ctx.send(embed=embed)
                    return
                
                embed = discord.Embed(
                    title="🤖 Available Agents",
                    description="List of all agents in the swarm",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                
                for agent_id, info in agent_status.items():
                    status_emoji = "🟢" if info['active'] else "🔴"
                    embed.add_field(
                        name=f"{status_emoji} {agent_id}",
                        value=f"Status: {'Active' if info['active'] else 'Inactive'}\nCoordinates: {info['coordinates']}",
                        inline=True
                    )
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                self.logger.error(f"Error in agent_list command: {e}")
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error listing agents: {str(e)}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                await ctx.send(embed=embed)
        
        @self.command(name="message_agent")
        async def message_agent(ctx, agent_id: str, *, message: str):
            """Send message to specific agent."""
            try:
                # Send message
                success = await self.messaging_controller.send_agent_message(
                    agent_id=agent_id,
                    message=message,
                    priority="NORMAL"
                )
                
                if success:
                    embed = discord.Embed(
                        title="✅ Message Sent",
                        description=f"Message sent to **{agent_id}**",
                        color=discord.Color.green(),
                        timestamp=discord.utils.utcnow()
                    )
                    embed.add_field(name="Message", value=message[:500], inline=False)
                    embed.add_field(name="From", value=ctx.author.display_name, inline=True)
                    
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Message Failed",
                        description=f"Failed to send message to **{agent_id}**",
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                    await ctx.send(embed=embed)
                    
            except Exception as e:
                self.logger.error(f"Error in message_agent command: {e}")
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error sending message: {str(e)}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                await ctx.send(embed=embed)
        
        @self.command(name="help_views")
        async def help_views(ctx):
            """Get help with views controller commands."""
            embed = discord.Embed(
                title="🎮 Discord Views Controller Help",
                description="Available commands with interactive GUI",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            
            commands_help = [
                ("`!agent_interact`", "Interactive messaging interface with dropdowns"),
                ("`!swarm_status`", "Real-time status monitoring with refresh buttons"),
                ("`!broadcast <message>`", "Broadcast message to all agents"),
                ("`!agent_list`", "List all available agents with status"),
                ("`!message_agent <agent_id> <message>`", "Send message to specific agent"),
                ("`!help_views`", "Show this help message")
            ]
            
            for command, description in commands_help:
                embed.add_field(name=command, value=description, inline=False)
            
            embed.add_field(
                name="🎮 Interactive Features",
                value="• Agent selection dropdowns\n• Modal-based message input\n• Real-time status updates\n• Priority-based messaging",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return
        
        self.logger.error(f"Command error: {error}")
        
        embed = discord.Embed(
            title="❌ Command Error",
            description=f"An error occurred: {str(error)}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        
        try:
            await ctx.send(embed=embed)
        except:
            pass


class DiscordViewsControllerLauncher:
    """Launcher for Discord Views Controller."""
    
    def __init__(self):
        """Initialize the launcher."""
        self.config = DiscordConfig()
        self.bot = None
        self.logger = logging.getLogger(__name__)
    
    def validate_environment(self) -> bool:
        """Validate environment configuration."""
        self.logger.info("🔍 Validating Discord environment...")
        
        # Check configuration
        config_issues = self.config.validate()
        if config_issues:
            self.logger.error(f"Configuration issues: {config_issues}")
            return False
        
        self.logger.info("✅ Environment validation successful")
        return True
    
    async def start_bot(self) -> bool:
        """Start the Discord bot with views controller."""
        try:
            self.logger.info("🚀 Starting Discord Views Controller...")
            
            # Validate environment
            if not self.validate_environment():
                return False
            
            # Create bot instance
            self.bot = DiscordViewsControllerBot(self.config)
            
            # Start bot
            await self.bot.start(self.config.token)
            
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return False
    
    async def stop_bot(self):
        """Stop the Discord bot."""
        try:
            if self.bot:
                self.logger.info("🛑 Stopping Discord Views Controller...")
                await self.bot.close()
                self.bot = None
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")


async def main():
    """Main function."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if not DISCORD_AVAILABLE:
        print("❌ Discord.py not available. Install with: pip install discord.py")
        sys.exit(1)
    
    launcher = DiscordViewsControllerLauncher()
    
    try:
        print("🎮 Discord Views Controller - Fixed Compatibility Version")
        print("========================================================")
        print()
        print("🤖 Features:")
        print("  • Interactive agent messaging with dropdowns")
        print("  • Real-time swarm status monitoring")
        print("  • Broadcast messaging to all agents")
        print("  • Modal-based message input")
        print("  • Discord.py 2.5.2 compatibility")
        print()
        print("📋 Available Commands:")
        print("  • !agent_interact - Interactive messaging interface")
        print("  • !swarm_status - Real-time status monitoring")
        print("  • !broadcast <message> - Broadcast to all agents")
        print("  • !agent_list - List all available agents")
        print("  • !message_agent <agent_id> <message> - Send to specific agent")
        print("  • !help_views - Show help")
        print()
        
        await launcher.start_bot()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Discord Views Controller...")
        await launcher.stop_bot()
        print("✅ Shutdown complete")
    except Exception as e:
        logger.error(f"Launcher failed: {e}")
        print(f"❌ Launcher failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

