#!/usr/bin/env python3
"""
Discord Commander Fixed - V2 Compliant (Refactored)
==================================================

Refactored Discord Commander importing from modular components.
Maintains backward compatibility while achieving V2 compliance.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import asyncio
import logging
from typing import Optional

from discord_commander_core import DiscordCommanderCore

logger = logging.getLogger(__name__)


class DiscordCommanderBot:
    """Discord Commander Bot with V2 compliance."""
    
    def __init__(self, token: str):
        """Initialize the Discord Commander Bot."""
        self.token = token
        self.core = DiscordCommanderCore()
        self.is_running = False
        logger.info("Discord Commander Bot initialized")
    
    async def start(self) -> None:
        """Start the Discord Commander Bot."""
        try:
            self.is_running = True
            await self.core.start_bot(self.token)
            logger.info("Discord Commander Bot started")
        except Exception as e:
            logger.error(f"Failed to start Discord Commander Bot: {e}")
            self.is_running = False
    
    async def stop(self) -> None:
        """Stop the Discord Commander Bot."""
        try:
            self.is_running = False
            await self.core.stop_bot()
            logger.info("Discord Commander Bot stopped")
        except Exception as e:
            logger.error(f"Failed to stop Discord Commander Bot: {e}")
    
    def get_status(self) -> dict:
        """Get bot status."""
        return {
            "is_running": self.is_running,
            "core_status": self.core.get_status()
        }
    
    async def send_message(self, channel_id: int, message: str) -> bool:
        """Send message to Discord channel."""
        try:
            return await self.core.send_message(channel_id, message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False


async def main():
    """Main entry point for Discord Commander Bot."""
    print("🚀 Starting Discord Commander Bot")
    
    # Get token from environment or config
    token = "YOUR_DISCORD_BOT_TOKEN"  # Replace with actual token
    
    # Initialize bot
    bot = DiscordCommanderBot(token)
    
    try:
        # Start bot
        await bot.start()
        
        # Keep running
        while bot.is_running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Discord Commander Bot...")
        await bot.stop()
    except Exception as e:
        logger.error(f"Discord Commander Bot error: {e}")
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())