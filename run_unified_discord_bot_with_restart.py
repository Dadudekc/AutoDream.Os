#!/usr/bin/env python3
"""
Run Discord Bot with Auto-Restart Support
==========================================

Enhanced runner script that supports !restart command.
When !restart is used, bot gracefully shuts down and automatically restarts.

Author: Agent-6 (Co-Captain) - Implementation
Spec: Agent-2 (Architecture LEAD)
Date: 2025-10-15
"""

import os
import sys
import time
from pathlib import Path

def main():
    """Main loop with auto-restart support."""
    print("🚀 Discord Bot Runner with Auto-Restart")
    print("🐝 WE. ARE. SWARM.\n")
    
    while True:
        # Run bot
        print("▶️  Starting Discord bot...")
        exit_code = run_bot()
        
        # Check for restart flag
        restart_flag = Path('.discord_bot_restart')
        if restart_flag.exists():
            # Restart requested via !restart command
            restart_flag.unlink()  # Remove flag file
            print("\n🔄 Restart requested - restarting in 3 seconds...")
            time.sleep(3)
            continue  # Restart loop
        
        # Normal exit (from !shutdown or error)
        print("\n👋 Bot shutdown complete")
        break


def run_bot():
    """Run the Discord bot and return exit code."""
    try:
        import asyncio
        from src.discord_commander.unified_discord_bot import main as bot_main
        
        # Run bot (will block until shutdown or restart)
        asyncio.run(bot_main())
        
        return 0  # Clean exit
        
    except KeyboardInterrupt:
        print("\n⚠️  Bot interrupted by user (Ctrl+C)")
        return 1
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("💡 Make sure discord.py is installed: pip install discord.py")
        return 1
        
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Runner shutdown by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error in runner: {e}")
        sys.exit(1)

