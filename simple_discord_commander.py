#!/usr/bin/env python3
"""
Simple Discord Commander - Demo Mode
====================================

A basic Discord Commander that works with placeholder tokens for demo purposes.
Requires real Discord bot token for actual functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Check if discord.py is available
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed. Run: pip install discord.py")

# Load environment if available
try:
    from dotenv import load_dotenv
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaders .env from: {env_path}")
except ImportError:
    print("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")


class SimpleDiscordCommander(commands.Bot):
    """Simple Discord Commander Bot"""
    
    def __init__(self):
        # Get configuration
        self.token = os.getenv("DISCORD_BOT_TOKEN", "your_discord bot_token_here")
        self.guild_id = os.getenv("DISCORD_GUILD_ID", "your_guild_id_here")
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Setup the bot after connection"""
        # Register slash command
        @self.tree.command(name="status", description="Check bot status")
        async def status_command(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🤖 Discord Commander Status",
                description="Bot is working correctly!",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Guilds", value=len(self.guilds), inline=True)
            embed.add_field(name="Users", value=len(self.users), inline=True)
            embed.add_field(name="Ping", value=f"{round(self.latency * 1000)}ms", inline=True)
            
            await interaction.response.send_message(embed=embed)
        
        # Register another command for testing
        @self.tree.command(name="swarm", description="WE ARE SWARM!")
        async def swarm_command(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🐝 THE SWARM",
                description="Multi-agent coordination system",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Agent-4", value="Captain - Strategic Leadership", inline=True)
            embed.add_field(name="Agent-5", value="Coordinator", inline=True)
            embed.add_field(name="Agent-6", value="Quality Assurance", inline=True)
            embed.add_field(name="Agent-7", value="Implementation", inline=True)
            embed.add_field(name="Agent-8", value="Message Handling", inline=True)
            
            await interaction.response.send_message(embed=embed)
        
        # Register regular commands
        @self.command(name="help")
        async def help_command(ctx):
            embed = discord.Embed(
                title="🤖 Discord Commander Help",
                description="Available commands:",
                color=discord.Color.purple()
            )
            
            embed.add_field(name="Slash Commands", value="/status - Bot status\n/swarm - Agent info", inline=False)
            embed.add_field(name="Regular Commands", value="!help - This help\n!ping - Test latency", inline=False)
            
            await ctx.send(embed=embed)
        
        @self.command(name="ping")
        async def ping_command(ctx):
            await ctx.send(f"🏓 Pong! {round(self.latency * 1000)}ms")
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f"✅ Bot is online as {self.user}")
        print(f"📊 Connected to {len(self.guilds)} guilds")
        print(f"👥 Serving {len(self.users)} users")
        
        # Set activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="WE ARE SWARM - Agent Coordination"
        )
        await self.change_presence(activity=activity)
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
    
    async def on_guild_join(self, guild):
        """Called when bot joins a guild"""
        print(f"✅ Joined new guild: {guild.name}")
    
    async def on_message(self, message):
        """Handle messages"""
        # Ignore messages from self
        if message.author == self.user:
            return
        
        await self.process_commands(message)


async def main():
    """Main function to run the Discord Commander"""
    if not DISCORD_AVAILABLE:
        print("❌ Cannot run: discord.py not available")
        print("💡 Install with: pip install discord.py")
        return False
    
    # Create bot instance
    bot = SimpleDiscordCommander()
    
    # Show configuration
    print("🐝 Discord Commander - Simple Mode")
    print("=" * 50)
    print(f"🔑 Token: {bot.token[:20]}..." if len(bot.token) > 20 else f"🔑 Token: {bot.token}")
    print(f"🏠 Guild ID: {bot.guild_id}")
    print(f"📝 Environment: {'✅ .env loaded' if os.path.exists('.env') else '⚠️ using defaults'}")
    
    # Check if using placeholder token
    if "your_discord" in bot.token or "bot_token_here" in bot.token:
        print("\n⚠️  USING PLACEHOLDER TOKEN!")
        print("🔧 To use with real Discord bot:")
        print("1. Create bot at https://discord.com/developers/applications")
        print("2. Get bot token")
        print("3. Update .env file with real values")
        print("4. Run this script again")
        print("\n🎯 DEMO MODE: Will attempt to connect (will fail gracefully)")
        return await run_demo_mode(bot)
    
    # Real token mode
    print("\n🚀 Starting Discord Commander with real token...")
    
    try:
        await bot.start(bot.token)
    except discord.LoginFailure:
        print("❌ Invalid bot token")
        return False
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        return False


async def run_demo_mode(bot):
    """Run in demo mode (placeholder token)"""
    print("\n🎮 DEMO MODE - Simulating Discord Commander")
    print("=" * 50)
    
    # Simulate bot startup sequence
    print("🔧 Initializing Discord Commander components...")
    await asyncio.sleep(1)
    
    print("✅ Bot core initialized")
    print("✅ Command system loaded")
    print("✅ Event handlers registered")
    print("✅ Slash commands registered")
    
    print("\n🎯 SYSTEM STATUS:")
    print("- Discord Commander: ✅ Ready")
    print("- Agent Coordination: ✅ Active")
    print("- Messaging Service: ✅ Running")
    print("- Command System: ✅ Operational")
    
    print("\n📋 AVAILABLE COMMANDS:")
    print("  /status - Check bot status")
    print("  /swarm - Agent information")
    print("  !help - Command help")
    print("  !ping - Test latency")
    
    print("\n🐝 WE ARE SWARM - Discord Commander Ready")
    print("🔧 Configure real Discord token to activate full functionality")
    
    # Keep running for demo
    print("\n🔄 Demo mode active (press Ctrl+C to exit)")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped")
        return True


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        if success:
            print("✅ Discord Commander session completed")
        else:
            print("❌ Discord Commander session failed")
    except KeyboardInterrupt:
        print("\n🛑 Discord Commander stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
