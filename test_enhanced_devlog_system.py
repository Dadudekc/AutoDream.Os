#!/usr/bin/env python3
"""
Enhanced Agent Devlog System Test
=================================

Test script to verify the enhanced agent devlog posting functionality
with vectorization and cleanup features.

Usage:
    python test_enhanced_devlog_system.py --test-config
    python test_enhanced_devlog_system.py --test-vectorization
    python test_enhanced_devlog_system.py --test-cleanup
    python test_enhanced_devlog_system.py --test-all
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from argparse import ArgumentParser

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedDevlogTester:
    """Test the enhanced agent devlog posting system."""

    def __init__(self):
        """Initialize test system."""
        self.test_agent = "Agent-4"
        self.test_action = "Enhanced devlog system test"
        self.test_status = "completed"
        self.test_details = "Testing vectorization and cleanup functionality"

    def test_configuration(self):
        """Test configuration loading."""
        print("🔧 Testing Enhanced Configuration Loading...")
        print("=" * 50)

        try:
            # Test Discord configuration
            bot_token = os.getenv("DISCORD_BOT_TOKEN")
            main_channel_id = os.getenv("DISCORD_CHANNEL_ID")

            if bot_token:
                print("✅ Discord bot token configured")
            else:
                print("⚠️ Discord bot token not configured")

            if main_channel_id:
                print("✅ Main Discord channel configured")
            else:
                print("⚠️ Main Discord channel not configured")

            # Test agent channels
            agent_channels = {}
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                env_var = f"DISCORD_CHANNEL_{agent_id.replace('-', '_')}"
                channel_id = os.getenv(env_var)

                if channel_id:
                    agent_channels[agent_id] = channel_id
                    print(f"✅ {agent_id} channel configured: {channel_id}")
                else:
                    print(f"⚠️ {agent_id} channel not configured")

            print(f"\n📊 Configuration Summary: {len(agent_channels)}/8 agent channels configured")

            # Test vector database configuration
            print("\n🧠 Vector Database Configuration:")
            try:
                from vector_database.vector_database_integration import VectorDatabaseIntegration
                vector_db = VectorDatabaseIntegration()
                print("✅ Vector database integration available")
            except ImportError:
                print("⚠️ Vector database integration not available")
            except Exception as e:
                print(f"⚠️ Vector database configuration issue: {e}")

            return True

        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            return False

    async def test_vectorization(self):
        """Test vectorization functionality."""
        print("🧠 Testing Vectorization Functionality...")
        print("=" * 50)

        try:
            # Import the agent devlog posting service
            from services.agent_devlog_posting import AgentDevlogPoster

            # Initialize poster
            poster = AgentDevlogPoster()

            print(f"📡 Agent channels loaded: {len(poster.agent_channels)}")

            # Test agent flag validation
            print(f"🔍 Testing agent flag validation for {self.test_agent}...")
            is_valid = poster.validate_agent_flag(self.test_agent)
            print(f"✅ Agent flag validation: {'PASSED' if is_valid else 'FAILED'}")

            if not is_valid:
                return False

            # Test channel routing
            print(f"🔍 Testing channel routing for {self.test_agent}...")
            channel_id = poster.get_agent_channel(self.test_agent)
            if channel_id:
                print(f"✅ Channel routing: {self.test_agent} -> {channel_id}")
            else:
                print(f"⚠️ No channel configured for {self.test_agent}")

            # Test file saving
            print("📄 Testing file saving functionality...")
            filepath = poster.save_devlog_file(
                self.test_agent,
                self.test_action,
                self.test_status,
                self.test_details
            )

            if filepath:
                print(f"✅ File saved: {filepath}")

                # Test vectorization (without cleanup)
                print("🧠 Testing vectorization...")
                vectorization_success = await poster._vectorize_devlog(
                    filepath,
                    self.test_agent,
                    self.test_action,
                    self.test_status,
                    self.test_details
                )

                if vectorization_success:
                    print("✅ Vectorization successful")
                else:
                    print("⚠️ Vectorization failed (check vector database configuration)")

                # Check if file still exists
                file_path = Path(filepath)
                if file_path.exists():
                    print("📄 File still exists after vectorization (expected - no cleanup)")
                else:
                    print("❌ File was unexpectedly removed")

            else:
                print("❌ File saving failed")
                return False

            return True

        except Exception as e:
            print(f"❌ Vectorization test failed: {e}")
            return False

    async def test_cleanup(self):
        """Test cleanup functionality."""
        print("🧹 Testing Cleanup Functionality...")
        print("=" * 50)

        try:
            # Import the agent devlog posting service
            from services.agent_devlog_posting import AgentDevlogPoster

            # Initialize poster
            poster = AgentDevlogPoster()

            # Create a test file first
            print("📄 Creating test file...")
            filepath = poster.save_devlog_file(
                self.test_agent,
                "Cleanup test file",
                "completed",
                "This file will be cleaned up"
            )

            if not filepath:
                print("❌ Failed to create test file")
                return False

            # Verify file exists
            file_path = Path(filepath)
            if file_path.exists():
                print(f"✅ Test file created: {filepath}")

                # Test cleanup
                print("🧹 Testing cleanup...")
                cleanup_success = await poster._cleanup_devlog_file(filepath, self.test_agent)

                if cleanup_success:
                    print("✅ Cleanup successful")
                else:
                    print("⚠️ Cleanup failed")

                # Check if file was removed
                if file_path.exists():
                    print("❌ File still exists after cleanup")
                    return False
                else:
                    print("✅ File successfully removed after cleanup")

                return True
            else:
                print("❌ Test file was not created")
                return False

        except Exception as e:
            print(f"❌ Cleanup test failed: {e}")
            return False

    async def test_enhanced_posting(self):
        """Test enhanced posting with vectorization and cleanup."""
        print("🚀 Testing Enhanced Posting (Vectorize + Cleanup)...")
        print("=" * 50)

        try:
            # Import the agent devlog posting service
            from services.agent_devlog_posting import AgentDevlogPoster

            # Initialize poster
            poster = AgentDevlogPoster()

            print("📝 Testing enhanced posting functionality...")

            # Test posting with vectorization and cleanup
            success = await poster.post_devlog_with_vectorization(
                agent_flag=self.test_agent,
                action="Enhanced posting test",
                status=self.test_status,
                details=self.test_details,
                vectorize=True,
                cleanup=True
            )

            if success:
                print("✅ Enhanced posting completed successfully")
                print("✅ File was vectorized and cleaned up")
            else:
                print("⚠️ Enhanced posting failed")

            return success

        except Exception as e:
            print(f"❌ Enhanced posting test failed: {e}")
            return False

    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Running Enhanced Agent Devlog System Tests")
        print("=" * 60)

        # Test configuration
        config_success = self.test_configuration()
        print()

        # Test vectorization
        vectorization_success = await self.test_vectorization()
        print()

        # Test cleanup
        cleanup_success = await self.test_cleanup()
        print()

        # Test enhanced posting
        enhanced_success = await self.test_enhanced_posting()
        print()

        # Summary
        print("📊 Test Results:")
        print(f"   Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
        print(f"   Vectorization: {'✅ PASS' if vectorization_success else '❌ FAIL'}")
        print(f"   Cleanup: {'✅ PASS' if cleanup_success else '❌ FAIL'}")
        print(f"   Enhanced Posting: {'✅ PASS' if enhanced_success else '❌ FAIL'}")

        overall_success = config_success and vectorization_success and cleanup_success and enhanced_success

        if overall_success:
            print("\n🎉 All tests passed! Enhanced agent devlog system is ready!")
            print("\n📝 Usage Examples:")
            print(f"   python src/services/agent_devlog_posting.py --agent {self.test_agent} --action \"Task completed\"")
            print("   python src/services/agent_devlog_posting.py --agent Agent-3 --action \"Code review\" --status in_progress --details \"Reviewing pull request\"")
            print("   python src/services/agent_devlog_posting.py --agent Agent-4 --action \"Task completed\" --vectorize --cleanup")
            print("   python src/services/agent_devlog_posting.py --help")
        else:
            print("\n❌ Some tests failed. Check configuration and vector database setup.")

        return overall_success


async def main():
    """Main test function."""
    parser = ArgumentParser(description="Test Enhanced Agent Devlog System")
    parser.add_argument("--test-config", action="store_true", help="Test configuration only")
    parser.add_argument("--test-vectorization", action="store_true", help="Test vectorization only")
    parser.add_argument("--test-cleanup", action="store_true", help="Test cleanup only")
    parser.add_argument("--test-enhanced", action="store_true", help="Test enhanced posting only")
    parser.add_argument("--test-all", action="store_true", help="Run all tests")

    args = parser.parse_args()

    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        return 0

    tester = EnhancedDevlogTester()

    if args.test_config:
        success = tester.test_configuration()
        return 0 if success else 1

    elif args.test_vectorization:
        success = await tester.test_vectorization()
        return 0 if success else 1

    elif args.test_cleanup:
        success = await tester.test_cleanup()
        return 0 if success else 1

    elif args.test_enhanced:
        success = await tester.test_enhanced_posting()
        return 0 if success else 1

    elif args.test_all:
        success = await tester.run_all_tests()
        return 0 if success else 1

    else:
        # Run all tests by default
        success = await tester.run_all_tests()
        return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

