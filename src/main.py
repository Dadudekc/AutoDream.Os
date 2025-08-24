#!/usr/bin/env python3
"""
V2 System Main Entry Point
==========================

This is the main entry point for the Agent Cellphone V2 system.
It provides access to all V2 features and serves as the system launcher.

Usage:
    python main.py                    # Interactive mode
    python main.py --help            # Show help
    python main.py --test            # Run V2 feature tests
    python main.py --demo            # Run V2 feature demos
    python main.py --health          # Check system health
    python main.py --features        # List all V2 features
"""

import sys
import os
import argparse

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional
import logging

from logging_config import configure_logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

configure_logging()
logger = logging.getLogger(__name__)


class V2SystemLauncher:
    """Main launcher for the V2 system"""

    def __init__(self):
        self.features = {
            "pyautogui": {
                "name": "PyAutoGUI Service Coordinate Path Resolution",
                "module": "services.pyautogui_service",
                "class": "PyAutoGUIService",
                "description": "Robust coordinate path resolution with fallback mechanisms",
            },
            "messaging": {
                "name": "Messaging-Coordination Integration",
                "module": "services.messaging_coordination_bridge",
                "class": "MessagingCoordinationBridge",
                "description": "Unified messaging-coordination bridge with automatic fallback",
            },
            "health": {
                "name": "Service Health Monitoring and Auto-Recovery",
                "module": "services.service_health_monitor",
                "class": "ServiceHealthMonitor",
                "description": "Comprehensive health monitoring with intelligent recovery strategies",
            },
            "error": {
                "name": "Advanced Error Handling and Logging",
                "module": "services.error_analytics_system",
                "class": "ErrorAnalyticsSystem",
                "description": "Enterprise-grade error management with analytics and reporting",
            },
        }

        self.system_status = {
            "operational": True,
            "features_available": len(self.features),
            "services_running": 0,
        }

    def show_banner(self):
        """Display V2 system banner"""
        logger.info("=" * 60)
        logger.info("🤖 AGENT CELLPHONE V2 SYSTEM")
        logger.info("=" * 60)
        logger.info("Advanced Agent Coordination Platform")
        logger.info("Enterprise-Grade Features & Professional Architecture")
        logger.info("=" * 60)

    def show_help(self):
        """Display help information"""
        logger.info("\n📚 V2 SYSTEM USAGE:")
        logger.info("  python main.py                    # Interactive mode")
        logger.info("  python main.py --help            # Show this help")
        logger.info("  python main.py --test            # Run V2 feature tests")
        logger.info("  python main.py --demo            # Run V2 feature demos")
        logger.info("  python main.py --health          # Check system health")
        logger.info("  python main.py --features        # List all V2 features")
        logger.info("  python main.py --feature <name>  # Run specific feature")

        logger.info("\n🔧 AVAILABLE V2 FEATURES:")
        for key, feature in self.features.items():
            logger.info(f"  {key:12} - {feature['name']}")
            logger.info(f"              {feature['description']}")

    def list_features(self):
        """List all available V2 features"""
        logger.info("\n🚀 V2 FEATURES OVERVIEW:")
        logger.info("=" * 60)

        for key, feature in self.features.items():
            logger.info(f"\n🔹 {feature['name']}")
            logger.info(f"   Key: {key}")
            logger.info(f"   Module: {feature['module']}")
            logger.info(f"   Class: {feature['class']}")
            logger.info(f"   Description: {feature['description']}")
            logger.info("-" * 40)

    def check_system_health(self):
        """Check overall system health"""
        logger.info("\n🏥 V2 SYSTEM HEALTH CHECK:")
        logger.info("=" * 40)

        # Check directory structure
        directories = [
            "src",
            "src/services",
            "src/core",
            "tests",
            "docs",
            "examples",
            "config",
        ]

        for directory in directories:
            if os.path.exists(directory):
                logger.info(f"✅ {directory:20} - Available")
            else:
                logger.warning(f"❌ {directory:20} - Missing")
                self.system_status["operational"] = False

        # Check V2 feature files
        logger.info("\n🔍 V2 FEATURE STATUS:")
        for key, feature in self.features.items():
            module_path = feature["module"].replace(".", "/") + ".py"
            full_path = f"src/{module_path}"

            if os.path.exists(full_path):
                logger.info(f"✅ {key:12} - {feature['name']}")
                self.system_status["services_running"] += 1
            else:
                logger.warning(f"❌ {key:12} - {feature['name']} (File missing)")
                self.system_status["operational"] = False

        # Overall status
        logger.info(f"\n📊 SYSTEM STATUS:")
        logger.info(
            f"   Operational: {'✅ Yes' if self.system_status['operational'] else '❌ No'}"
        )
        logger.info(
            f"   Features Available: {self.system_status['features_available']}"
        )
        logger.info(f"   Services Running: {self.system_status['services_running']}")

        return self.system_status["operational"]

    def run_feature_tests(self):
        """Run tests for all V2 features"""
        logger.info("\n🧪 RUNNING V2 FEATURE TESTS:")
        logger.info("=" * 40)

        # Check if pytest is available
        try:
            import pytest

            logger.info("✅ pytest available")
        except ImportError:
            logger.error("❌ pytest not available - install with: pip install pytest")
            return False

        # Run tests
        test_dirs = ["tests/unit", "tests/integration"]
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                logger.info(f"\n🔍 Running tests in {test_dir}:")
                os.system(f"python -m pytest {test_dir} -v")
            else:
                logger.warning(f"⚠️  Test directory {test_dir} not found")

        return True

    def run_feature_demos(self):
        """Run demonstrations for V2 features"""
        logger.info("\n🎬 RUNNING V2 FEATURE DEMOS:")
        logger.info("=" * 40)

        demo_files = ["examples/demonstrate_advanced_error_handling_logging.py"]

        for demo_file in demo_files:
            if os.path.exists(demo_file):
                logger.info(f"\n🎭 Running demo: {demo_file}")
                try:
                    os.system(f"python {demo_file}")
                except Exception as e:
                    logger.error(f"❌ Demo failed: {e}")
            else:
                logger.warning(f"⚠️  Demo file not found: {demo_file}")

        return True

    def run_specific_feature(self, feature_name: str):
        """Run a specific V2 feature"""
        if feature_name not in self.features:
            logger.error(f"❌ Unknown feature: {feature_name}")
            logger.info(f"Available features: {', '.join(self.features.keys())}")
            return False

        feature = self.features[feature_name]
        logger.info(f"\n🚀 RUNNING V2 FEATURE: {feature['name']}")
        logger.info("=" * 50)

        try:
            # Import the feature module
            module = __import__(feature["module"], fromlist=[feature["class"]])
            feature_class = getattr(module, feature["class"])

            # Create instance and show basic info
            instance = feature_class()
            logger.info(f"✅ Feature loaded successfully: {feature['name']}")
            logger.info(f"   Class: {feature['class']}")
            logger.info(f"   Module: {feature['module']}")

            # Show available methods
            methods = [m for m in dir(instance) if not m.startswith("_")]
            logger.info(f"   Available methods: {', '.join(methods[:5])}...")

        except Exception as e:
            logger.error(f"❌ Failed to load feature: {e}")
            return False

        return True

    def interactive_mode(self):
        """Run interactive mode"""
        logger.info("\n🎮 INTERACTIVE V2 SYSTEM MODE:")
        logger.info("=" * 40)

        while True:
            logger.info("\nOptions:")
            logger.info("  1. List V2 features")
            logger.info("  2. Check system health")
            logger.info("  3. Run feature tests")
            logger.info("  4. Run feature demos")
            logger.info("  5. Run specific feature")
            logger.info("  6. Exit")

            try:
                choice = input("\nEnter choice (1-6): ").strip()

                if choice == "1":
                    self.list_features()
                elif choice == "2":
                    self.check_system_health()
                elif choice == "3":
                    self.run_feature_tests()
                elif choice == "4":
                    self.run_feature_demos()
                elif choice == "5":
                    feature = input("Enter feature name: ").strip()
                    self.run_specific_feature(feature)
                elif choice == "6":
                    logger.info("👋 Exiting V2 system. Goodbye!")
                    break
                else:
                    logger.warning("❌ Invalid choice. Please enter 1-6.")

            except KeyboardInterrupt:
                logger.info("\n\n👋 Exiting V2 system. Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")

    def run(self, args):
        """Main run method"""
        self.show_banner()

        if args.help:
            self.show_help()
        elif args.test:
            self.run_feature_tests()
        elif args.demo:
            self.run_feature_demos()
        elif args.health:
            self.check_system_health()
        elif args.features:
            self.list_features()
        elif args.feature:
            self.run_specific_feature(args.feature)
        else:
            # Default to interactive mode
            self.interactive_mode()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Agent Cellphone V2 System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py --test            # Run all tests
  python main.py --demo            # Run all demos
  python main.py --health          # Check system health
  python main.py --feature pyautogui  # Run specific feature
        """,
    )

    parser.add_argument(
        "--help", "-h", action="store_true", help="Show detailed help information"
    )
    parser.add_argument("--test", action="store_true", help="Run V2 feature tests")
    parser.add_argument("--demo", action="store_true", help="Run V2 feature demos")
    parser.add_argument("--health", action="store_true", help="Check system health")
    parser.add_argument("--features", action="store_true", help="List all V2 features")
    parser.add_argument(
        "--feature", type=str, metavar="NAME", help="Run specific V2 feature"
    )

    args = parser.parse_args()

    # Create and run launcher
    launcher = V2SystemLauncher()
    launcher.run(args)


if __name__ == "__main__":
    main()
