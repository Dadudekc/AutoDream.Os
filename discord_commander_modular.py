#!/usr/bin/env python3
"""
Discord Commander - Modular Version
===================================

Modular Discord Commander with clean architecture and V2 compliance.
Features:
- Modular component design
- Clean separation of concerns
- V2 compliance (≤400 lines per file)
- Enhanced error handling
- Swarm intelligence integration

🐝 WE ARE SWARM - Discord Commander Active!
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import modular components
from src.services.discord_commander.bot import DiscordCommanderBot

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('discord_commander.log')
        ]
    )

def print_banner():
    """Print startup banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    DISCORD COMMANDER                         ║
║                  Modular V2 Architecture                     ║
║                                                              ║
║  🐝 WE ARE SWARM - Agent Coordination System                ║
║  🚀 V2 Compliance - Clean & Modular Design                  ║
║  ⚡ Enhanced Performance & Reliability                       ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check system requirements."""
    print("🔍 Checking system requirements...")
    
    # Check Discord.py
    try:
        import discord
        print("✅ Discord.py available")
    except ImportError:
        print("❌ Discord.py not installed! Please install: pip install discord.py")
        return False
    
    # Check environment variables
    import os
    required_vars = ["DISCORD_BOT_TOKEN", "DISCORD_GUILD_ID"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please set these variables in your .env file or environment")
        return False
    
    print("✅ Environment variables configured")
    
    # Check project structure
    required_dirs = ["src/services/discord_commander", "agent_workspaces"]
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Required directory not found: {dir_path}")
            return False
    
    print("✅ Project structure validated")
    return True

async def run_bot():
    """Run the Discord Commander Bot."""
    print("🚀 Starting Discord Commander Bot...")
    
    try:
        bot = DiscordCommanderBot()
        
        if await bot.initialize():
            print("✅ Bot initialized successfully")
            await bot.start()
        else:
            print("❌ Failed to initialize bot")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        logging.error(f"Bot error: {e}", exc_info=True)
        return False
    finally:
        if 'bot' in locals():
            await bot.stop()
        print("👋 Discord Commander Bot stopped")
    
    return True

def main():
    """Main entry point."""
    print_banner()
    
    # Set up logging
    setup_logging()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🎯 Starting Discord Commander Bot...")
    
    try:
        # Run the bot
        success = asyncio.run(run_bot())
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()




