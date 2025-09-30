"""
Enhanced Discord Agent Bot Core
V2 Compliant main Discord bot implementation
"""

import asyncio
import logging
import sys
from pathlib import Path

import discord
from discord.ext import commands

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from .discord_bot_core import DiscordBotCore
from .discord_bot_models import BotConfiguration


class EnhancedDiscordAgentBot(commands.Bot):
    """Enhanced Discord Bot for Agent Coordination - V2 Compliant"""
    
    def __init__(self, command_prefix: str = "!", intents: discord.Intents = None):
        """Initialize the enhanced Discord agent bot"""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            intents.guilds = True
            
        super().__init__(command_prefix=command_prefix, intents=intents, help_command=None)
        self.logger = logging.getLogger(__name__)
        
    async def setup_hook(self):
        """Setup hook for bot initialization"""
        self.logger.info("Setting up Discord bot...")
        
    async def on_ready(self):
        """Bot ready event"""
        self.logger.info(f"Bot logged in as {self.user}")
        
    async def on_command_error(self, ctx, error):
        """Command error handler"""
        self.logger.error(f"Command error: {error}")
        
    async def start_bot(self, token: str):
        """Start the bot"""
        try:
            await self.start(token)
        except Exception as e:
            self.logger.error(f"Bot start error: {e}")
            raise
            
    async def stop_bot(self):
        """Stop the bot"""
        await self.close()


def create_discord_bot(config: BotConfiguration) -> EnhancedDiscordAgentBot:
    """Create Discord bot instance"""
    intents = discord.Intents.default()
    intents.message_content = config.intents.get("message_content", True)
    intents.members = config.intents.get("members", True)
    intents.guilds = config.intents.get("guilds", True)
    
    return EnhancedDiscordAgentBot(
        command_prefix=config.command_prefix,
        intents=intents
    )


async def main():
    """Main entry point"""
    logging.basicConfig(level=logging.INFO)
    
    config = BotConfiguration(
        command_prefix="!",
        intents={"message_content": True, "members": True, "guilds": True},
        guild_id=None,
        log_level="INFO",
        auto_sync=True
    )
    
    bot = create_discord_bot(config)
    
    try:
        # In a real implementation, you would load the token from environment
        token = "YOUR_BOT_TOKEN_HERE"
        await bot.start_bot(token)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    finally:
        await bot.stop_bot()


if __name__ == "__main__":
    asyncio.run(main())
