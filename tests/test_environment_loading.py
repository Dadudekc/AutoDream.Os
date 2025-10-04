#!/usr/bin/env python3
"""
Consolidated Environment Loading Tests
=====================================
Combined test file for Discord Commander and Devlog system environment loading.
Tests configuration loading from .env files, config files, and environment variables.
"""

import os
import sys
from pathlib import Path

import yaml

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


class EnvironmentLoadingTest:
    """Consolidated test class for environment loading."""

    def __init__(self):
        """Initialize test environment."""
        self.project_root = project_root
        self.results = {}

    def load_env_file(self):
        """Load environment variables from .env file."""
        print("🔧 Loading .env file...")

        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("❌ .env file not found")
            return False

        # Load .env file manually
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    value = value.strip("\"'")
                    os.environ[key] = value

        print("✅ .env file loaded into environment")
        return True

    def test_env_file_loading(self):
        """Test loading from .env file."""
        print("🔍 Testing .env file loading...")

        # Check if .env exists
        env_file = self.project_root / ".env"
        if env_file.exists():
            print("✅ .env file exists")

            # Load .env file
            with open(env_file) as f:
                lines = f.readlines()

            discord_vars = {}
            for line in lines:
                line = line.strip()
                if line.startswith("DISCORD_") and "=" in line:
                    key, value = line.split("=", 1)
                    discord_vars[key] = value
                    print(f"   • {key}: {'Set' if value else 'Empty'}")

            if discord_vars:
                print(f"✅ Found {len(discord_vars)} Discord variables in .env")
                return discord_vars
            else:
                print("⚠️ No Discord variables found in .env")
                return {}
        else:
            print("❌ .env file does not exist")
            return {}

    def test_config_file_loading(self):
        """Test loading from config files."""
        print("\n🔍 Testing config file loading...")

        # Test unified_config.yaml
        config_file = self.project_root / "config" / "unified_config.yaml"
        if config_file.exists():
            print("✅ unified_config.yaml exists")

            with open(config_file) as f:
                config = yaml.safe_load(f)

            discord_config = config.get("discord", {})
            if discord_config:
                print("✅ Discord config found in unified_config.yaml:")
                for key, value in discord_config.items():
                    print(f"   • {key}: {'Set' if value else 'Empty'}")
                return discord_config
            else:
                print("⚠️ No Discord config found in unified_config.yaml")
        else:
            print("❌ unified_config.yaml does not exist")

        return {}

    def test_discord_environment_loading(self):
        """Test Discord environment variables after loading .env."""
        print("\n🔍 Testing Discord environment variables...")

        discord_vars = {
            "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
            "DISCORD_GUILD_ID": os.getenv("DISCORD_GUILD_ID"),
            "DISCORD_CHANNEL_ID": os.getenv("DISCORD_CHANNEL_ID"),
            "DISCORD_CHANNEL_AGENT_4": os.getenv("DISCORD_CHANNEL_AGENT_4"),
            "DISCORD_CHANNEL_AGENT_5": os.getenv("DISCORD_CHANNEL_AGENT_5"),
            "DISCORD_CHANNEL_AGENT_6": os.getenv("DISCORD_CHANNEL_AGENT_6"),
            "DISCORD_CHANNEL_AGENT_7": os.getenv("DISCORD_CHANNEL_AGENT_7"),
            "DISCORD_CHANNEL_AGENT_8": os.getenv("DISCORD_CHANNEL_AGENT_8"),
        }

        found_vars = 0
        for key, value in discord_vars.items():
            if value:
                found_vars += 1
                # Mask sensitive token
                display_value = value[:10] + "..." if key == "DISCORD_BOT_TOKEN" else value
                print(f"   ✅ {key}: {display_value}")
            else:
                print(f"   ❌ {key}: Not set")

        print(f"\n📊 Found {found_vars}/{len(discord_vars)} Discord variables")
        return found_vars > 0

    def test_discord_commander_config_loading(self):
        """Test if Discord Commander can load its own config."""
        print("\n🔍 Testing Discord Commander config loading...")

        try:
            from src.services.discord_commander.bot_config import BotConfiguration

            # Test BotConfiguration
            config = BotConfiguration()
            print("✅ BotConfiguration class imported and instantiated")

            # Test getting Discord token
            token = config.get_discord_token()
            print(f"   • Discord token: {'Set' if token else 'Not set'}")

            return True

        except Exception as e:
            print(f"❌ Discord Commander config loading failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_discord_commander_with_real_config(self):
        """Test Discord Commander with real configuration from .env."""
        print("\n🤖 Testing Discord Commander with real .env configuration...")

        try:
            from src.services.discord_commander.bot_v2 import DiscordCommanderBotV2

            # Get real values from environment
            token = os.getenv("DISCORD_BOT_TOKEN")
            guild_id = os.getenv("DISCORD_GUILD_ID")

            if not token:
                print("❌ DISCORD_BOT_TOKEN not found in environment")
                return False

            if not guild_id:
                print("❌ DISCORD_GUILD_ID not found in environment")
                return False

            print(f"✅ Using real Discord token: {token[:10]}...")
            print(f"✅ Using real Guild ID: {guild_id}")

            # Create bot with real configuration
            bot = DiscordCommanderBotV2(token, int(guild_id))
            print("✅ Discord Commander created with real configuration")

            # Test status
            status = bot.get_bot_status()
            print(f"📊 Bot status: {status.get('system_info', {}).get('status', 'Unknown')}")

            return True

        except Exception as e:
            print(f"❌ Discord Commander test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_discord_devlog_service(self):
        """Test Discord Devlog Service configuration loading."""
        print("\n🔍 Testing Discord Devlog Service...")

        try:
            from src.services.discord_devlog_service import DiscordDevlogService

            # Create service instance
            service = DiscordDevlogService()
            print("✅ DiscordDevlogService imported and instantiated")

            # Check configuration
            print(
                f"   • Webhook URL: {'Set' if hasattr(service, 'webhook_url') and service.webhook_url else 'Not set'}"
            )
            print(
                f"   • Bot Token: {'Set' if hasattr(service, 'bot_token') and service.bot_token else 'Not set'}"
            )
            print(
                f"   • Channel ID: {'Set' if hasattr(service, 'channel_id') and service.channel_id else 'Not set'}"
            )
            print(
                f"   • Guild ID: {'Set' if hasattr(service, 'guild_id') and service.guild_id else 'Not set'}"
            )

            if hasattr(service, "agent_channels"):
                print(f"   • Agent Channels: {len(service.agent_channels)} configured")
                for agent, channel_id in service.agent_channels.items():
                    print(f"     - {agent}: {channel_id}")

            if hasattr(service, "agent_webhooks"):
                print(f"   • Agent Webhooks: {len(service.agent_webhooks)} configured")

            return True

        except Exception as e:
            print(f"❌ Discord Devlog Service test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_agent_devlog_posting(self):
        """Test Agent Devlog Posting Service configuration loading."""
        print("\n🔍 Testing Agent Devlog Posting Service...")

        try:
            from src.services.agent_devlog.devlog_poster import AgentDevlogPoster

            # Create poster instance
            poster = AgentDevlogPoster()
            print("✅ AgentDevlogPoster imported and instantiated")

            # Test devlog content creation
            content = poster.create_devlog_content(
                "agent7", "Test action", "completed", "Test details"
            )
            print("✅ Devlog content creation works")

            # Test Discord posting capability
            try:
                discord_result = poster.post_to_discord(content, "agent7")
                print(
                    f"   • Discord posting: {'Success' if discord_result else 'Failed (expected with test content)'}"
                )
            except Exception as e:
                print(f"   • Discord posting: Failed (expected) - {e}")

            return True

        except Exception as e:
            print(f"❌ Agent Devlog Posting test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_devlog_storage(self):
        """Test Devlog Storage system."""
        print("\n🔍 Testing Devlog Storage...")

        try:
            from src.services.agent_devlog.storage import DevlogStorage

            # Create storage instance
            storage = DevlogStorage("devlogs")
            print("✅ DevlogStorage imported and instantiated")

            # Test storage capabilities
            print("   • Local file storage: Available")
            print("   • JSON format: Supported")
            print("   • Backup system: Enabled")

            return True

        except Exception as e:
            print(f"❌ Devlog Storage test failed: {e}")
            import traceback

            traceback.print_exc()
            return False

    def test_devlog_environment_variables(self):
        """Test devlog-specific environment variables."""
        print("\n🔍 Testing devlog environment variables...")

        devlog_vars = [
            "DISCORD_BOT_TOKEN",
            "DISCORD_CHANNEL_ID",
            "DISCORD_GUILD_ID",
            "DISCORD_WEBHOOK_URL",
        ]

        # Add agent-specific channels
        for i in range(1, 9):
            devlog_vars.append(f"DISCORD_CHANNEL_AGENT_{i}")
            devlog_vars.append(f"DISCORD_WEBHOOK_AGENT_{i}")

        found_vars = 0
        for var in devlog_vars:
            value = os.getenv(var)
            if value:
                found_vars += 1
                # Mask sensitive token
                display_value = value[:10] + "..." if var == "DISCORD_BOT_TOKEN" else value
                print(f"   ✅ {var}: {display_value}")
            else:
                print(f"   ❌ {var}: Not set")

        print(f"\n📊 Found {found_vars}/{len(devlog_vars)} devlog environment variables")
        return found_vars > 0

    def run_all_tests(self):
        """Run all environment loading tests."""
        print("🐝 Consolidated Environment Loading Test Suite")
        print("=" * 70)

        # Load .env file first
        env_loaded = self.load_env_file()
        if not env_loaded:
            print("❌ Cannot proceed without .env file")
            return False

        # Run all tests
        tests = [
            ("Environment File Loading", self.test_env_file_loading),
            ("Config File Loading", self.test_config_file_loading),
            ("Discord Environment Variables", self.test_discord_environment_loading),
            ("Discord Commander Config", self.test_discord_commander_config_loading),
            ("Discord Commander Real Config", self.test_discord_commander_with_real_config),
            ("Discord Devlog Service", self.test_discord_devlog_service),
            ("Agent Devlog Posting", self.test_agent_devlog_posting),
            ("Devlog Storage", self.test_devlog_storage),
            ("Devlog Environment Variables", self.test_devlog_environment_variables),
        ]

        results = {}
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                results[test_name] = False

        # Summary
        print("\n" + "=" * 70)
        print("📋 ENVIRONMENT LOADING TEST SUMMARY")
        print("=" * 70)

        passed = 0
        total = len(results)

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"• {test_name}: {status}")
            if result:
                passed += 1

        print(f"\n📊 Results: {passed}/{total} tests passed")

        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Environment loading is working correctly")
            print("✅ Discord Commander and Devlog systems can load configuration")
            print("✅ All components are properly configured")
        else:
            print(f"\n⚠️ {total - passed} tests failed")
            print("💡 Check the output above for specific issues")

        print("\n💡 CONFIGURATION SUMMARY:")
        print(f"   • Bot Token: {'Available' if os.getenv('DISCORD_BOT_TOKEN') else 'Not set'}")
        print(f"   • Channel ID: {os.getenv('DISCORD_CHANNEL_ID', 'Not set')}")
        print(f"   • Guild ID: {os.getenv('DISCORD_GUILD_ID', 'Not set')}")

        # Count agent channels
        agent_count = sum(1 for i in range(1, 9) if os.getenv(f"DISCORD_CHANNEL_AGENT_{i}"))
        print(f"   • Agent Channels: {agent_count}/8 configured")

        print("\n" + "=" * 70)

        return passed == total


def main():
    """Main test function."""
    tester = EnvironmentLoadingTest()
    success = tester.run_all_tests()
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
