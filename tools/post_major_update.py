#!/usr/bin/env python3
"""
Post Major Update Tool
=====================

Tool for posting major system updates to the Discord major update channel.

Features:
- Post major announcements to Discord
- Support for V3 system updates
- Agent coordination announcements
- System status updates

Usage:
    python tools/post_major_update.py --message "V3 system launch"
    python tools/post_major_update.py --v3-launch
    python tools/post_major_update.py --custom "Custom announcement"
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.discord_devlog_service import DiscordDevlogService

logger = logging.getLogger(__name__)


class MajorUpdatePoster:
    """Tool for posting major updates to Discord."""
    
    def __init__(self):
        """Initialize major update poster."""
        self.major_update_channel_id = os.getenv("MAJOR_UPDATE_DISCORD_CHANNEL_ID")
        self.service = None
        
        if not self.major_update_channel_id:
            logger.error("MAJOR_UPDATE_DISCORD_CHANNEL_ID not set in environment")
            raise ValueError("Major update channel ID not configured")
    
    async def initialize(self) -> bool:
        """Initialize Discord service."""
        try:
            self.service = DiscordDevlogService()
            self.service.channel_id = int(self.major_update_channel_id)
            
            success = await self.service.initialize_bot()
            if not success:
                logger.error("Failed to initialize Discord bot")
                return False
            
            logger.info(f"Initialized major update poster for channel {self.major_update_channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize major update poster: {e}")
            return False
    
    async def post_v3_launch_announcement(self) -> bool:
        """Post V3 launch announcement."""
        message = """**🚀 MAJOR SYSTEM UPDATE - V3 LAUNCH** 🚀

**Discord Devlog System: BACK ONLINE** ✅

We are excited to announce that the Discord devlog system has been fully restored and enhanced! The system is now operational with significant improvements.

**🎯 What's New in V3:**
- ✅ **8 Agent-Specific Discord Channels** - Each agent now has their own dedicated channel
- ✅ **Enhanced Discord Bot** - New commands and improved functionality
- ✅ **Full Devlog Integration** - Complete devlog creation and posting system
- ✅ **V2 Compliance Maintained** - All components under 400 lines
- ✅ **Environment Integration** - Seamless .env file configuration

**🤖 New Discord Commands:**
- `!agent-devlog Agent-4 Mission completed` - Post to agent-specific channel
- `!agent-channels` - List all agent channels
- `!devlog <action>` - Post to main channel
- `!commands` - Show all commands

**📊 System Status:**
- **Discord Bot:** 🟢 Online
- **Agent Channels:** 🟢 8/8 Operational
- **Devlog System:** 🟢 Fully Functional
- **V2 Compliance:** 🟢 100% Compliant

**🐝 WE ARE SWARM - V3 OPERATIONAL**

The system is now ready for enhanced agent coordination and communication. All agents can now post devlogs to their dedicated channels while maintaining our V2 compliance standards.

**Ready for V3 operations!** 🚀"""
        
        return await self._post_message(message)
    
    async def post_custom_announcement(self, message: str) -> bool:
        """Post custom announcement."""
        formatted_message = f"""**📢 MAJOR SYSTEM ANNOUNCEMENT** 📢

{message}

**🐝 WE ARE SWARM** - V3 System Operational"""
        
        return await self._post_message(formatted_message)
    
    async def post_system_status_update(self, status: str, details: str = "") -> bool:
        """Post system status update."""
        message = f"""**📊 SYSTEM STATUS UPDATE** 📊

**Status:** {status}

{details if details else "System operating normally."}

**🐝 WE ARE SWARM** - V3 System Monitoring"""
        
        return await self._post_message(message)
    
    async def _post_message(self, message: str) -> bool:
        """Post message to major update channel."""
        try:
            channel = self.service.bot.get_channel(int(self.major_update_channel_id))
            if not channel:
                logger.error(f"Could not access channel {self.major_update_channel_id}")
                return False
            
            await channel.send(message)
            logger.info(f"Major update posted to channel {self.major_update_channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error posting major update: {e}")
            return False
    
    async def close(self):
        """Close Discord service."""
        if self.service:
            await self.service.close()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Post major updates to Discord",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/post_major_update.py --v3-launch
  python tools/post_major_update.py --custom "System maintenance completed"
  python tools/post_major_update.py --status "Operational" --details "All systems green"
        """
    )
    
    parser.add_argument(
        "--v3-launch",
        action="store_true",
        help="Post V3 launch announcement"
    )
    
    parser.add_argument(
        "--custom",
        type=str,
        help="Post custom announcement message"
    )
    
    parser.add_argument(
        "--status",
        type=str,
        help="Post system status update"
    )
    
    parser.add_argument(
        "--details",
        type=str,
        default="",
        help="Additional details for status update"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        # Initialize poster
        poster = MajorUpdatePoster()
        success = await poster.initialize()
        
        if not success:
            print("❌ Failed to initialize major update poster")
            return 1
        
        # Post based on arguments
        if args.v3_launch:
            print("🚀 Posting V3 launch announcement...")
            success = await poster.post_v3_launch_announcement()
        elif args.custom:
            print(f"📢 Posting custom announcement: {args.custom}")
            success = await poster.post_custom_announcement(args.custom)
        elif args.status:
            print(f"📊 Posting status update: {args.status}")
            success = await poster.post_system_status_update(args.status, args.details)
        else:
            print("❌ No action specified. Use --help for usage information.")
            return 1
        
        if success:
            print("✅ Major update posted successfully!")
            return 0
        else:
            print("❌ Failed to post major update")
            return 1
            
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        return 1
    finally:
        if 'poster' in locals():
            await poster.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))


