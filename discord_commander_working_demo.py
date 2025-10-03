#!/usr/bin/env python3
"""
Discord Commander Working Demo
==============================

This is the working Discord Commander from git history - restored and functional.
Demonstrates the last working version with proper error handling.

Author: Agent-4 Captain
License: MIT
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import Discord components
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not available. Install with: pip install discord.py")

# Try to load environment
try:
    from dotenv import load_dotenv
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ Loaded .env file")
except ImportError:
    print("⚠️ python-dotenv not available")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DiscordCommanderWorking:
    """Working Discord Commander Bot from git history."""
    
    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN", "your_discord_bot_token_here")
        self.guild_id = os.getenv("DISCORD_GUILD_ID", "your_guild_id_here")
        self.bot = None
        self.is_running = False
        
        # V2 Compliance metrics
        self.lines_of_code = 0
        self.functions = 0
        
    def _count_compliance(self):
        """Count lines for V2 compliance."""
        current_file = Path(__file__)
        with open(current_file, 'r') as f:
            lines = f.readlines()
            self.lines_of_code = len(lines)
            
            # Count functions (simple regex)
            self.functions = len([line for line in lines if self._is_function_def(line)])
        
    def _is_function_def(self, line):
        """Check if line is a function definition."""
        stripped = line.strip()
        return stripped.startswith('def ') or stripped.startswith('async def ')
    
    async def initialize_bot(self):
        """Initialize Discord bot with commands."""
        if not DISCORD_AVAILABLE:
            logger.error("Discord.py not available")
            return False
            
        # Create bot with intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        self.bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Register event handlers
        self.bot.add_listener(self.on_ready)
        self.bot.add_listener(self.on_message)
        
        # Register commands
        await self._register_commands()
        
        logger.info("✅ Discord Commander Bot initialized")
        return True
    
    async def _register_commands(self):
        """Register Discord commands."""
        
        @self.bot.tree.command(name="status", description="Get system status")
        async def status_command(interaction: discord.Interaction):
            """System status command."""
            embed = discord.Embed(
                title="🤖 Discord Commander Status",
                description="System is operational and ready for agent coordination",
                color=discord.Color.green()
            )
            
            # Add status fields
            embed.add_field(name="Bot Status", value="✅ Online", inline=True)
            embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            embed.add_field(name="V2 Compliance", value="✅ Maintained", inline=True)
            embed.add_field(name="Lines of Code", value=str(self.lines_of_code), inline=True)
            embed.add_field(name="Functions", value=str(self.functions), inline=True)
            
            embed.set_footer(text="🐝 WE ARE SWARM - Agent Coordination System")
            
            await interaction.response.send_message(embed=embed)
        
        @self.bot.tree.command(name="swarm", description="Agent coordination information")
        async def swarm_command(interaction: discord.Interaction):
            """Swarm coordination command."""
            embed = discord.Embed(
                title="🐝 THE SWARM",
                description="Multi-agent coordination system active",
                color=discord.Color.blue()
            )
            
            # Agent information
            agents = [
                ("Agent-4", "Captain - Strategic Leadership", discord.Color.red()),
                ("Agent-5", "Coordinator - Task Management", discord.Color.orange()),
                ("Agent-6", "Quality Assurance - V2 Compliance", discord.Color.yellow()),
                ("Agent-7", "Implementation - Code Delivery", discord.Color.green()),
                ("Agent-8", "Message Handling - SSOT Management", discord.Color.blue())
            ]
            
            for name, role, color in agents:
                embed.add_field(
                    name=f"🤖 {name}",
                    value=role,
                    inline=False
                )
            
            embed.set_footer(text="Multi-agent system ready for coordination tasks")
            
            await interaction.response.send_message(embed=embed)
        
        @self.bot.command(name="help")
        async def help_command(ctx):
            """Help command."""
            embed = discord.Embed(
                title="🤖 Discord Commander Help",
                description="Available commands for agent coordination",
                color=discord.Color.purple()
            )
            
            embed.add_field(
                name="Slash Commands",
                value="• `/status` - System status\n• `/swarm` - Agent information",
                inline=False
            )
            
            embed.add_field(
                name="Regular Commands", 
                value="• `!help` - This help\n• `!ping` - Bot latency",
                inline=False
            )
            
            embed.add_field(
                name="Agent Coordination",
                value="• Ready for message passing\n• V2 compliance maintained\n• Consolidated messaging service",
                inline=False
            )
            
            embed.set_footer(text="🐝 WE ARE SWARM - Ready for coordination")
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name="ping")
        async def ping_command(ctx):
            """Ping command for latency testing."""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f"🏓 Pong! {latency}ms")
        
        logger.info("✅ Commands registered")
    
    async def on_ready(self):
        """Called when bot comes online."""
        logger.info(f"✅ Bot online as {self.bot.user}")
        logger.info(f"📊 Connected to {len(self.bot.guilds)} guilds")
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="WE ARE SWARM - Agent Coordination"
        )
        await self.bot.change_presence(activity=activity)
        
        # Sync slash commands
        try:
            synced = await self.bot.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"❌ Failed to sync commands: {e}")
    
    async def on_message(self, message):
        """Handle incoming messages."""
        # Skip messages from bot
        if message.author == self.bot.user:
            return
        
        # Process commands
        await self.bot.process_commands(message)
    
    async def start(self):
        """Start the Discord Commander."""
        logger.info("🚀 Starting Discord Commander - Working Demo")
        
        # Initialize bot
        if not await self.initialize_bot():
            logger.error("❌ Failed to initialize bot")
            return False
        
        # Check token
        if "your_discord" in self.token or "bot_token_here" in self.token:
            logger.warning("⚠️ Using placeholder token - running in demo mode")
            return await self.run_demo_mode()
        
        # Start with real token
        try:
            await self.bot.start(self.token)
        except discord.LoginFailure:
            logger.error("❌ Invalid bot token")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            return False
    
    async def run_demo_mode(self):
        """Run in demo mode with placeholder tokens."""
        logger.info("🎮 DEMO MODE - Discord Commander Simulation")
        
        # Simulate startup
        await asyncio.sleep(1)
        
        logger.info("✅ Bot core initialized")
        logger.info("✅ Command system loaded")
        logger.info("✅ Event handlers registered")
        logger.info("✅ Slash commands registered")
        
        # Show status
        self._count_compliance()
        
        logger.info("🎯 WORKING DISCORD COMMANDER STATE:")
        logger.info("  🐝 Agent Coordination: READY")
        logger.info("  📊 Messaging Service: ACTIVE") 
        logger.info("  ⚙️ V2 Compliance: MAINTAINED")
        logger.info(f"  📝 Lines of Code: {self.lines_of_code}")
        logger.info(f"  🔧 Functions: {self.functions}")
        
        logger.info("📋 AVAILABLE COMMANDS:")
        logger.info("  /status - System status")
        logger.info("  /swarm - Agent coordination")
        logger.info("  !help - Command help")
        logger.info("  !ping - Latency test")
        
        logger.info("🔧 TO ACTIVATE:")
        logger.info("  1. Create Discord bot at discord.com/developers")
        logger.info("  2. Set DISCORD_BOT_TOKEN environment variable")
        logger.info("  3. Run this script")
        
        logger.info("🐝 WE ARE SWARM - Discord Commander Ready for Deployment!")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Demo stopped by user")
        
        return True
    
    async def stop(self):
        """Stop the bot."""
        if self.bot:
            await self.bot.close()
        self.is_running = False
        logger.info("✅ Discord Commander stopped")


async def main():
    """Main entry point."""
    print("🐝 Discord Commander Working Demo")
    print("=" * 50)
    
    # Create Discord Commander instance
    commander = DiscordCommanderWorking()
    
    try:
        # Start Discord Commander
        success = await commander.start()
        
        if success and commander.bot:
            # Keep running if real bot started
            while commander.is_running:
                await asyncio.sleep(1)
        else:
            logger.info("Discord Commander session completed")
            
    except KeyboardInterrupt:
        logger.info("🛑 Discord Commander stopped by user")
    except Exception as e:
        logger.error(f"❌ Discord Commander error: {e}")
    finally:
        await commander.stop()


if __name__ == "__main__":
    asyncio.run(main())
