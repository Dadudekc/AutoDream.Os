#!/usr/bin/env python3
"""
Simple Discord Commander - Agent-4
==================================

Simple Discord bot runner for Agent-4 without complex architecture dependencies.
Uses KISS principle for immediate deployment.

Author: Agent-4
Date: 2025-01-15
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import discord
    from discord.ext import commands
    from discord import app_commands
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("📝 Run: pip install discord.py python-dotenv")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleDiscordCommander(commands.Bot):
    """Simple Discord commander for Agent-4."""
    
    def __init__(self):
        """Initialize simple Discord commander."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = False
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        
        self.agent_id = "Agent-4"
        self.logger = logging.getLogger(f"{__name__}.SimpleDiscordCommander")
    
    async def setup_hook(self):
        """Setup hook for bot initialization."""
        self.logger.info("🚀 Setting up Simple Discord Commander...")
        
        # Add basic commands
        await self._setup_commands()
        
        self.logger.info("✅ Simple Discord Commander setup complete")
    
    async def _setup_commands(self):
        """Setup basic commands."""
        
        # Setup slash commands
        @self.tree.command(name="ping", description="Test bot responsiveness")
        async def ping(interaction: discord.Interaction):
            """Test bot responsiveness."""
            latency = round(self.latency * 1000)
            await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")
        
        # Keep prefix commands for backward compatibility
        @self.command(name="ping")
        async def ping_prefix(ctx):
            """Test bot responsiveness."""
            latency = round(self.latency * 1000)
            await ctx.send(f"🏓 Pong! Latency: {latency}ms")
        
        # Slash command for status
        @self.tree.command(name="status", description="Show system status")
        async def status_slash(interaction: discord.Interaction):
            """Show system status."""
            status_embed = discord.Embed(
                title="🤖 Simple Discord Commander Status",
                description="Agent-4 Discord Commander is operational",
                color=0x00ff00
            )
            status_embed.add_field(
                name="Agent ID",
                value=self.agent_id,
                inline=True
            )
            status_embed.add_field(
                name="Latency",
                value=f"{round(self.latency * 1000)}ms",
                inline=True
            )
            status_embed.add_field(
                name="Guilds",
                value=len(self.guilds),
                inline=True
            )
            status_embed.add_field(
                name="Commands",
                value="ping, status, help, send, swarm, onboard",
                inline=False
            )
            
            await interaction.response.send_message(embed=status_embed)
        
        # Keep prefix command for backward compatibility
        @self.command(name="status")
        async def status_prefix(ctx):
            """Show system status."""
            status_embed = discord.Embed(
                title="🤖 Simple Discord Commander Status",
                description="Agent-4 Discord Commander is operational",
                color=0x00ff00
            )
            status_embed.add_field(
                name="Agent ID",
                value=self.agent_id,
                inline=True
            )
            status_embed.add_field(
                name="Latency",
                value=f"{round(self.latency * 1000)}ms",
                inline=True
            )
            status_embed.add_field(
                name="Guilds",
                value=len(self.guilds),
                inline=True
            )
            status_embed.add_field(
                name="Commands",
                value="ping, status, help, send, swarm, onboard",
                inline=False
            )
            
            await ctx.send(embed=status_embed)
        
        # Slash command for help
        @self.tree.command(name="help", description="Show help information")
        async def help_slash(interaction: discord.Interaction):
            """Show help information."""
            help_embed = discord.Embed(
                title="🤖 Simple Discord Commander Help",
                description="Agent-4 Discord Commander Commands",
                color=0x0099ff
            )
            help_embed.add_field(
                name="Slash Commands",
                value="• `/ping` - Test bot responsiveness\n• `/status` - Show system status\n• `/help` - Show this help\n• `/send` - Send message to specific agent\n• `/swarm` - Send message to all agents\n• `/onboard` - Onboard new agent to swarm",
                inline=False
            )
            help_embed.add_field(
                name="Prefix Commands",
                value="• `!ping` - Test bot responsiveness\n• `!status` - Show system status\n• `!help` - Show this help\n• `!swarm-status` - Show swarm coordination status",
                inline=False
            )
            help_embed.add_field(
                name="Messaging Examples",
                value="• `/send agent:Agent-1 message:Hello priority:URGENT`\n• `/swarm message:All agents report status priority:HIGH`\n• `/onboard agent:Agent-1 hard_onboarding:true`",
                inline=False
            )
            help_embed.add_field(
                name="Agent-4 Status",
                value="✅ Operational and ready for swarm coordination",
                inline=False
            )
            
            await interaction.response.send_message(embed=help_embed)
        
        # Keep prefix command for backward compatibility
        @self.command(name="help")
        async def help_prefix(ctx):
            """Show help information."""
            help_embed = discord.Embed(
                title="🤖 Simple Discord Commander Help",
                description="Agent-4 Discord Commander Commands",
                color=0x0099ff
            )
            help_embed.add_field(
                name="Slash Commands",
                value="• `/ping` - Test bot responsiveness\n• `/status` - Show system status\n• `/help` - Show this help",
                inline=False
            )
            help_embed.add_field(
                name="Prefix Commands",
                value="• `!ping` - Test bot responsiveness\n• `!status` - Show system status\n• `!help` - Show this help\n• `!swarm-status` - Show swarm coordination status",
                inline=False
            )
            help_embed.add_field(
                name="Agent-4 Status",
                value="✅ Operational and ready for swarm coordination",
                inline=False
            )
            
            await ctx.send(embed=help_embed)
        
        # Slash command for send message
        @self.tree.command(name="send", description="Send message to specific agent")
        @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
        @app_commands.describe(message="Message to send to the agent")
        @app_commands.describe(priority="Message priority (NORMAL, HIGH, URGENT)")
        async def send_message_slash(interaction: discord.Interaction, agent: str, message: str, priority: str = "NORMAL"):
            """Send message to specific agent."""
            try:
                # Import messaging service
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent / "src"))
                from services.messaging.core.messaging_service import MessagingService
                
                # Initialize messaging service with absolute path
                coord_path = str(Path(__file__).parent / "config" / "coordinates.json")
                messaging_service = MessagingService(coord_path)
                
                # Send message with priority
                success = messaging_service.send_message(agent, message, "Discord-Commander", priority)
                
                if success:
                    priority_emoji = "🔴" if priority == "URGENT" else "🟡" if priority == "HIGH" else "🟢"
                    response = f"✅ **Message Sent Successfully!**\n\n"
                    response += f"**To:** {agent}\n"
                    response += f"**Message:** {message}\n"
                    response += f"**Priority:** {priority_emoji} {priority}\n"
                    response += f"**From:** Discord-Commander\n"
                    response += "\n🐝 **WE ARE SWARM** - Message delivered!"
                else:
                    response = f"❌ **Failed to send message to {agent}**\n\n"
                    response += f"**Possible reasons:**\n"
                    response += f"• Agent {agent} is not active\n"
                    response += f"• Invalid agent ID\n"
                    response += f"• Messaging system error"
                
                await interaction.response.send_message(response)
                
            except Exception as e:
                await interaction.response.send_message(f"❌ Error sending message: {e}")
        
        # Slash command for swarm broadcast
        @self.tree.command(name="swarm", description="Send message to all agents")
        @app_commands.describe(message="Message to send to all agents")
        @app_commands.describe(priority="Message priority (NORMAL, HIGH, URGENT)")
        async def swarm_message_slash(interaction: discord.Interaction, message: str, priority: str = "NORMAL"):
            """Send message to all agents."""
            try:
                # Import messaging service
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent / "src"))
                from services.messaging.core.messaging_service import MessagingService
                
                # Initialize messaging service with absolute path
                coord_path = str(Path(__file__).parent / "config" / "coordinates.json")
                messaging_service = MessagingService(coord_path)
                
                # Broadcast message with priority
                results = messaging_service.broadcast_message(message, "Discord-Commander", priority)
                
                active_agents = [agent for agent, success in results.items() if success]
                failed_agents = [agent for agent, success in results.items() if not success]
                
                priority_emoji = "🔴" if priority == "URGENT" else "🟡" if priority == "HIGH" else "🟢"
                response = f"**SWARM MESSAGE SENT** 🐝\n\n"
                response += f"**Message:** {message}\n"
                response += f"**Priority:** {priority_emoji} {priority}\n\n"
                response += f"**Delivered to:** {len(active_agents)} active agents\n"
                
                if active_agents:
                    response += f"**Successful:** {', '.join(active_agents)}\n"
                
                if failed_agents:
                    response += f"**Failed:** {', '.join(failed_agents)}\n"
                
                response += f"\n**Total agents:** {len(results)}"
                await interaction.response.send_message(response)
                
            except Exception as e:
                await interaction.response.send_message(f"❌ Error sending swarm message: {e}")
        
        # Slash command for agent onboarding
        @self.tree.command(name="onboard", description="Onboard a new agent to the swarm")
        @app_commands.describe(agent="Agent ID to onboard (e.g., Agent-1, Agent-2)")
        @app_commands.describe(hard_onboarding="Use hard onboarding mode (default: false)")
        async def onboard_agent_slash(interaction: discord.Interaction, agent: str, hard_onboarding: bool = False):
            """Onboard a new agent to the swarm."""
            try:
                # Import messaging and onboarding services
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent / "src"))
                from services.messaging.core.messaging_service import MessagingService
                from services.messaging.onboarding.onboarding_service import OnboardingService
                
                # Initialize services
                coord_path = str(Path(__file__).parent / "config" / "coordinates.json")
                messaging_service = MessagingService(coord_path)
                onboarding_service = OnboardingService(messaging_service)
                
                # Execute onboarding sequence
                success = onboarding_service.execute_onboarding_sequence(agent, "Discord-Commander Onboarding")
                
                if success:
                    response = f"✅ **Agent Onboarding Initiated!**\n\n"
                    response += f"**Agent:** {agent}\n"
                    response += f"**Mode:** {'Hard Onboarding' if hard_onboarding else 'Standard Onboarding'}\n"
                    response += f"**Status:** Onboarding sequence completed\n"
                    response += f"**From:** Discord-Commander\n\n"
                    response += f"🐝 **{agent} is now part of the swarm!**\n\n"
                    response += f"**Next Steps:**\n"
                    response += f"• Agent should check inbox for onboarding message\n"
                    response += f"• Review agent workspace structure\n"
                    response += f"• Begin autonomous operation cycle"
                else:
                    response = f"❌ **Failed to onboard {agent}**\n\n"
                    response += f"**Possible reasons:**\n"
                    response += f"• Agent coordinates not found\n"
                    response += f"• Onboarding system error\n"
                    response += f"• Invalid agent ID"
                
                await interaction.response.send_message(response)
                
            except Exception as e:
                await interaction.response.send_message(f"❌ Error during onboarding: {e}")
        
        # Keep prefix commands for backward compatibility
        @self.command(name="swarm-status")
        async def swarm_status(ctx):
            """Show swarm coordination status."""
            swarm_embed = discord.Embed(
                title="🐝 Swarm Coordination Status",
                description="Agent-4 reporting swarm status",
                color=0xff9900
            )
            swarm_embed.add_field(
                name="Agent-4 Status",
                value="✅ Online and operational",
                inline=True
            )
            swarm_embed.add_field(
                name="Discord Commander",
                value="✅ Simple commander active",
                inline=True
            )
            swarm_embed.add_field(
                name="Swarm Ready",
                value="✅ Ready for coordination",
                inline=True
            )
            swarm_embed.add_field(
                name="Coordinates",
                value="Monitor 1: (-308, 1000)",
                inline=False
            )
            
            await ctx.send(embed=swarm_embed)
    
    async def on_ready(self):
        """Event fired when bot is ready."""
        self.logger.info(f"🤖 {self.user} is online and ready!")
        self.logger.info(f"📊 Connected to {len(self.guilds)} guilds")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            self.logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            self.logger.error(f"❌ Failed to sync slash commands: {e}")
        
        # Send startup notification
        try:
            # Try to send to a general channel if available
            for guild in self.guilds:
                for channel in guild.text_channels:
                    if channel.name in ['general', 'bot-commands', 'swarm-coordination']:
                        startup_embed = discord.Embed(
                            title="🚀 Agent-4 Discord Commander Online",
                            description="Simple Discord Commander is now operational",
                            color=0x00ff00
                        )
                        startup_embed.add_field(
                            name="Agent",
                            value="Agent-4",
                            inline=True
                        )
                        startup_embed.add_field(
                            name="Status",
                            value="✅ Operational",
                            inline=True
                        )
                        startup_embed.add_field(
                            name="Commands",
                            value="Use `!help` for available commands",
                            inline=False
                        )
                        
                        await channel.send(embed=startup_embed)
                        break
                break
        except Exception as e:
            self.logger.warning(f"Could not send startup notification: {e}")
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `!help` for available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing required argument. Use `!help` for command usage.")
        else:
            self.logger.error(f"Command error: {error}")
            await ctx.send("❌ An error occurred while processing the command.")


async def main():
    """Main function to run the simple Discord commander."""
    print("🤖 Starting Simple Discord Commander (Agent-4)...")
    print("=" * 60)
    print("📁 Loading environment variables from .env file...")
    
    # Check for Discord bot token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token or token == "your_discord_bot_token_here":
        print("❌ Discord bot token not configured!")
        print("📝 Please set DISCORD_BOT_TOKEN in .env file")
        print("   Current .env file location: " + str(Path(__file__).parent / ".env"))
        return
    
    print(f"✅ Discord bot token loaded from .env file")
    print(f"🔑 Token preview: {token[:20]}...")
    
    # Create and start bot
    bot = SimpleDiscordCommander()
    
    try:
        print("🚀 Starting Discord bot...")
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ Invalid Discord bot token!")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
    finally:
        print("🛑 Shutting down Discord bot...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
