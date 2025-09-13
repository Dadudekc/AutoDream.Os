#!/usr/bin/env python3
"""
Consolidated Discord Utility
============================

Unified Discord bot management, testing, and configuration system.
Consolidates functionality from multiple Discord-related scripts.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DiscordConfig:
    """Discord bot configuration."""

    token: str
    channel_id: str
    guild_id: Optional[str] = None
    webhook_url: Optional[str] = None
    enabled: bool = True


class DiscordUtility:
    """Unified Discord utility for bot management."""

    def __init__(self):
        """Initialize the Discord utility."""
        self.config_path = Path("config/discord.json")
        self.bot_path = Path("src/web/discord_bot.py")
        self.agent_bot_path = Path("src/web/discord_agent_bot.py")

    def setup_bot(self, token: str, channel_id: str, guild_id: str = None) -> bool:
        """Setup Discord bot configuration."""
        try:
            config = DiscordConfig(
                token=token,
                channel_id=channel_id,
                guild_id=guild_id
            )

            # Create config directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Save configuration
            with open(self.config_path, 'w') as f:
                json.dump({
                    "token": config.token,
                    "channel_id": config.channel_id,
                    "guild_id": config.guild_id,
                    "webhook_url": config.webhook_url,
                    "enabled": config.enabled
                }, f, indent=2)

            # Set environment variables
            os.environ["DISCORD_TOKEN"] = token
            os.environ["DISCORD_CHANNEL_ID"] = channel_id
            if guild_id:
                os.environ["DISCORD_GUILD_ID"] = guild_id

            logger.info("Discord bot configuration saved successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Discord bot: {str(e)}")
            return False

    def configure_webhooks(self, webhook_url: str) -> bool:
        """Configure Discord webhooks."""
        try:
            if not self.config_path.exists():
                logger.error("Discord configuration not found. Run setup first.")
                return False

            # Load existing config
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            # Update webhook URL
            config["webhook_url"] = webhook_url

            # Save updated config
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            logger.info("Discord webhook configured successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to configure webhook: {str(e)}")
            return False

    def test_bot(self, bot_type: str = "standard") -> bool:
        """Test Discord bot functionality."""
        try:
            if not self.config_path.exists():
                logger.error("Discord configuration not found. Run setup first.")
                return False

            # Load configuration
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            if not config.get("enabled", False):
                logger.warning("Discord bot is disabled in configuration")
                return False

            # Choose bot script
            if bot_type == "agent":
                bot_script = self.agent_bot_path
            else:
                bot_script = self.bot_path

            if not bot_script.exists():
                logger.error(f"Bot script not found: {bot_script}")
                return False

            # Run bot test
            logger.info(f"Testing {bot_type} Discord bot...")
            result = subprocess.run([
                sys.executable, str(bot_script), "--test"
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                logger.info("✅ Discord bot test passed")
                return True
            else:
                logger.error(f"❌ Discord bot test failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Discord bot test timed out")
            return False
        except Exception as e:
            logger.error(f"Failed to test Discord bot: {str(e)}")
            return False

    def test_enhanced_discord(self) -> bool:
        """Test enhanced Discord functionality."""
        try:
            # Check for enhanced Discord features
            enhanced_features = [
                "src/web/discord_agent_bot.py",
                "src/core/swarm_communication_coordinator.py"
            ]

            missing_features = []
            for feature in enhanced_features:
                if not Path(feature).exists():
                    missing_features.append(feature)

            if missing_features:
                logger.warning(f"Enhanced features missing: {missing_features}")
                return False

            # Test enhanced functionality
            logger.info("Testing enhanced Discord features...")

            # Test swarm coordination
            try:
                result = subprocess.run([
                    sys.executable, "-c",
                    "from src.core.swarm_communication_coordinator import SwarmCommunicationCoordinator; print('Swarm coordination available')"
                ], capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    logger.info("✅ Enhanced Discord features available")
                    return True
                else:
                    logger.error(f"❌ Enhanced features test failed: {result.stderr}")
                    return False

            except Exception as e:
                logger.error(f"Enhanced features test error: {str(e)}")
                return False

        except Exception as e:
            logger.error(f"Failed to test enhanced Discord: {str(e)}")
            return False

    def run_discord_bot(self, bot_type: str = "standard", daemon: bool = False) -> bool:
        """Run Discord bot."""
        try:
            if not self.config_path.exists():
                logger.error("Discord configuration not found. Run setup first.")
                return False

            # Choose bot script
            if bot_type == "agent":
                bot_script = self.agent_bot_path
            else:
                bot_script = self.bot_path

            if not bot_script.exists():
                logger.error(f"Bot script not found: {bot_script}")
                return False

            # Run bot
            logger.info(f"Starting {bot_type} Discord bot...")

            if daemon:
                # Run in background
                subprocess.Popen([
                    sys.executable, str(bot_script)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.info("Discord bot started in background")
            else:
                # Run in foreground
                subprocess.run([sys.executable, str(bot_script)])

            return True

        except Exception as e:
            logger.error(f"Failed to run Discord bot: {str(e)}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get Discord bot status."""
        status = {
            "configured": False,
            "enabled": False,
            "bot_available": False,
            "agent_bot_available": False,
            "webhook_configured": False,
            "issues": []
        }

        try:
            # Check configuration
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)

                status["configured"] = True
                status["enabled"] = config.get("enabled", False)
                status["webhook_configured"] = bool(config.get("webhook_url"))

                if not config.get("token"):
                    status["issues"].append("Discord token not configured")
                if not config.get("channel_id"):
                    status["issues"].append("Discord channel ID not configured")
            else:
                status["issues"].append("Discord configuration not found")

            # Check bot availability
            status["bot_available"] = self.bot_path.exists()
            status["agent_bot_available"] = self.agent_bot_path.exists()

            if not status["bot_available"]:
                status["issues"].append("Standard Discord bot not found")
            if not status["agent_bot_available"]:
                status["issues"].append("Agent Discord bot not found")

        except Exception as e:
            status["issues"].append(f"Status check failed: {str(e)}")

        return status


def main():
    """Main entry point for the Discord utility."""
    parser = argparse.ArgumentParser(description="Consolidated Discord Utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup Discord bot configuration")
    setup_parser.add_argument("--token", required=True, help="Discord bot token")
    setup_parser.add_argument("--channel-id", required=True, help="Discord channel ID")
    setup_parser.add_argument("--guild-id", help="Discord guild ID")

    # Configure webhook command
    webhook_parser = subparsers.add_parser("webhook", help="Configure Discord webhook")
    webhook_parser.add_argument("--url", required=True, help="Webhook URL")

    # Test command
    test_parser = subparsers.add_parser("test", help="Test Discord bot")
    test_parser.add_argument("--type", choices=["standard", "agent"], default="standard", help="Bot type to test")

    # Test enhanced command
    enhanced_parser = subparsers.add_parser("test-enhanced", help="Test enhanced Discord features")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run Discord bot")
    run_parser.add_argument("--type", choices=["standard", "agent"], default="standard", help="Bot type to run")
    run_parser.add_argument("--daemon", action="store_true", help="Run in background")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get Discord bot status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    utility = DiscordUtility()

    try:
        if args.command == "setup":
            if utility.setup_bot(args.token, args.channel_id, args.guild_id):
                print("✅ Discord bot setup completed")
            else:
                print("❌ Discord bot setup failed")
                return 1

        elif args.command == "webhook":
            if utility.configure_webhooks(args.url):
                print("✅ Discord webhook configured")
            else:
                print("❌ Discord webhook configuration failed")
                return 1

        elif args.command == "test":
            if utility.test_bot(args.type):
                print(f"✅ {args.type} Discord bot test passed")
            else:
                print(f"❌ {args.type} Discord bot test failed")
                return 1

        elif args.command == "test-enhanced":
            if utility.test_enhanced_discord():
                print("✅ Enhanced Discord features test passed")
            else:
                print("❌ Enhanced Discord features test failed")
                return 1

        elif args.command == "run":
            if utility.run_discord_bot(args.type, args.daemon):
                print(f"✅ {args.type} Discord bot started")
            else:
                print(f"❌ Failed to start {args.type} Discord bot")
                return 1

        elif args.command == "status":
            status = utility.get_status()
            print("Discord Bot Status:")
            print(f"  Configured: {'✅' if status['configured'] else '❌'}")
            print(f"  Enabled: {'✅' if status['enabled'] else '❌'}")
            print(f"  Standard Bot: {'✅' if status['bot_available'] else '❌'}")
            print(f"  Agent Bot: {'✅' if status['agent_bot_available'] else '❌'}")
            print(f"  Webhook: {'✅' if status['webhook_configured'] else '❌'}")

            if status["issues"]:
                print("\nIssues:")
                for issue in status["issues"]:
                    print(f"  - {issue}")

        return 0

    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
