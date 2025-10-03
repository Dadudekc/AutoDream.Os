#!/usr/bin/env python3
"""
Discord Commander Runner
========================

Main script to run the Discord Commander bot.

Author: Agent-7 (Web Development Specialist)
Date: 2025-01-16
Version: 1.0.0
"""

# ---- UTF-8 console safety (Windows-friendly) ----
import os, sys
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    # Python 3.7+ — make stdout/stderr UTF-8 and never crash on emoji
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
# -------------------------------------------------

import asyncio
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.discord_bot.core.discord_bot import EnhancedDiscordAgentBot

logger = logging.getLogger(__name__)


async def main():
    """Main function to run Discord Commander."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Starting Discord Commander...")
    print("=" * 50)
    print("🚀 Ready.")
    
    # Check for Discord bot token
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        print("Please set your Discord bot token:")
        print("export DISCORD_BOT_TOKEN='your_bot_token_here'")
        return
    
    try:
        # Create bot instance
        bot = EnhancedDiscordAgentBot()
        
        print("🤖 Discord Commander initialized")
        print("📋 Available commands:")
        print("   - /ping - Test bot responsiveness")
        print("   - /commands - Show help information")
        print("   - /agents - List all agents and their status")
        print("   - /swarm - Send message to all agents")
        print("   - /send - Send message to specific agent")
        print("   - /devlog - Create devlog entry")
        print("   - And many more...")
        print()
        print("🔗 Connecting to Discord...")
        
        # Run the bot
        await bot.start(token)
        
    except Exception as e:
        logger.error(f"❌ Failed to start Discord Commander: {e}")
        print(f"❌ Error: {e}")
        return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Discord Commander stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
