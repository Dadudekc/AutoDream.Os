#!/usr/bin/env python3
"""
Discord Views Controller Launcher
=================================

Launches the Discord Commander with full GUI views controller integration.
Provides both command-line interface and interactive Discord GUI.

Features:
- Interactive agent messaging with dropdowns and modals
- Real-time swarm status monitoring with refresh buttons
- Broadcast messaging to all agents
- Agent selection and communication interface
- Comprehensive error handling and logging

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

from src.services.discord_commander.enhanced_bot import EnhancedBotManager
from src.services.discord_commander.core import DiscordConfig

logger = logging.getLogger(__name__)


class DiscordViewsControllerLauncher:
    """Launcher for Discord Views Controller with full GUI integration."""
    
    def __init__(self):
        """Initialize the launcher."""
        self.bot_manager = EnhancedBotManager()
        self.logger = logging.getLogger(__name__)
    
    def validate_environment(self) -> bool:
        """Validate environment configuration."""
        self.logger.info("🔍 Validating Discord environment...")
        
        # Check configuration
        config_issues = self.bot_manager.config.validate()
        if config_issues:
            self.logger.error(f"Configuration issues: {config_issues}")
            return False
        
        self.logger.info("✅ Environment validation successful")
        return True
    
    def display_startup_info(self):
        """Display startup information."""
        print("🎮 DISCORD VIEWS CONTROLLER LAUNCHER")
        print("=====================================")
        print()
        print("🤖 Features Available:")
        print("  • Interactive agent messaging with dropdowns")
        print("  • Real-time swarm status monitoring")
        print("  • Broadcast messaging to all agents")
        print("  • Agent selection and communication interface")
        print("  • Modal-based message input")
        print("  • Priority-based message routing")
        print()
        print("📋 Available Commands:")
        print("  • !message_agent <agent_id> <message> [priority]")
        print("  • !agent_interact - Interactive messaging interface")
        print("  • !swarm_status - View current swarm status")
        print("  • !broadcast <message> [priority] - Broadcast to all agents")
        print("  • !agent_list - List all available agents")
        print("  • !help_messaging - Get help with messaging commands")
        print()
        print("🎯 Discord Views Controller Features:")
        print("  • AgentMessagingView - Dropdown agent selection + modal input")
        print("  • SwarmStatusView - Real-time status with refresh buttons")
        print("  • MessageModal - Text input with priority selection")
        print("  • BroadcastModal - Broadcast message input")
        print()
    
    async def start_bot_with_views(self) -> bool:
        """Start the Discord bot with views controller integration."""
        try:
            self.logger.info("🚀 Starting Discord Views Controller...")
            
            # Validate environment
            if not self.validate_environment():
                return False
            
            # Display startup info
            self.display_startup_info()
            
            # Start the enhanced bot with messaging controller
            success = await self.bot_manager.start_bot()
            
            if success:
                self.logger.info("✅ Discord Views Controller started successfully!")
                print("🎉 Discord Views Controller is now running!")
                print("🌐 Web Controller: http://localhost:8080")
                print("🤖 Discord Bot: Connected and ready")
                print("📱 Views Controller: Active with interactive GUI")
                return True
            else:
                self.logger.error("❌ Failed to start Discord Views Controller")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting Discord Views Controller: {e}")
            return False
    
    async def stop_bot(self):
        """Stop the Discord bot."""
        try:
            await self.bot_manager.stop_bot()
            self.logger.info("🛑 Discord Views Controller stopped")
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
    
    def get_status(self) -> dict:
        """Get current bot status."""
        return self.bot_manager.get_bot_status()


async def main():
    """Main function."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    launcher = DiscordViewsControllerLauncher()
    
    try:
        print("🎮 Launching Discord Views Controller...")
        print()
        
        success = await launcher.start_bot_with_views()
        
        if success:
            print()
            print("🎯 Discord Views Controller Status:")
            status = launcher.get_status()
            print(f"  • Status: {status.get('status', 'Unknown')}")
            print(f"  • Guilds: {status.get('guilds', 0)}")
            print(f"  • Users: {status.get('users', 0)}")
            print(f"  • Latency: {status.get('latency', 'N/A')}ms")
            print()
            print("🎮 Interactive Discord GUI Features:")
            print("  • Use !agent_interact for dropdown agent selection")
            print("  • Use !swarm_status for real-time monitoring")
            print("  • Use !broadcast for swarm-wide messaging")
            print("  • All commands support interactive modals and views")
            print()
            print("Press Ctrl+C to stop the bot...")
            
            # Keep running until interrupted
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down Discord Views Controller...")
                await launcher.stop_bot()
                print("✅ Shutdown complete")
        else:
            print("❌ Failed to start Discord Views Controller")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Launcher failed: {e}")
        print(f"❌ Launcher failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

