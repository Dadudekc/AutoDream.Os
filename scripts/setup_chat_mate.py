#!/usr/bin/env python3
"""
Chat_Mate Setup Script - Automated Installation.

V2 Compliance: Setup automation for Chat_Mate browser integration
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def install_dependencies():
    """Install Chat_Mate browser automation dependencies."""
    logger.info("📦 Installing Chat_Mate dependencies...")

    dependencies = ["selenium>=4.0.0", "undetected-chromedriver>=3.5.0", "webdriver-manager>=4.0.0"]

    try:
        for dep in dependencies:
            logger.info(f"   Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        logger.info("✅ Chat_Mate dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False


def create_runtime_directories():
    """Create runtime directories for browser profiles and cookies."""
    logger.info("📁 Creating runtime directories...")

    dirs = [Path("runtime/browser/profiles"), Path("runtime/browser"), Path("logs/core")]

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"   Created: {directory}")

    logger.info("✅ Runtime directories created")
    return True


def test_chat_mate_import():
    """Test that Chat_Mate can be imported."""
    logger.info("🧪 Testing Chat_Mate import...")

    try:
        from src.infrastructure.browser.unified import UnifiedDriverManager, get_driver_manager

        logger.info("✅ Chat_Mate import successful")
        logger.info(f"   UnifiedDriverManager: {UnifiedDriverManager}")
        logger.info(f"   get_driver_manager: {get_driver_manager}")
        return True
    except ImportError as e:
        logger.error(f"❌ Chat_Mate import failed: {e}")
        return False


def main():
    """Main setup execution."""
    logger.info("🚀 Chat_Mate Setup Starting...")
    logger.info("=" * 50)

    # Step 1: Install dependencies
    if not install_dependencies():
        logger.error("❌ Setup failed: Dependencies installation failed")
        return 1

    # Step 2: Create runtime directories
    if not create_runtime_directories():
        logger.error("❌ Setup failed: Directory creation failed")
        return 1

    # Step 3: Test import
    if not test_chat_mate_import():
        logger.error("❌ Setup failed: Import test failed")
        logger.warning("⚠️ You may need to restart your Python environment")
        return 1

    logger.info("=" * 50)
    logger.info("✅ Chat_Mate setup complete!")
    logger.info("")
    logger.info("📋 Next steps:")
    logger.info("   1. Import: from src.infrastructure.browser.unified import get_driver_manager")
    logger.info("   2. Usage: driver = get_driver_manager().get_driver()")
    logger.info("   3. Cleanup: driver.quit() or use context manager")
    logger.info("")
    logger.info("🐝 WE. ARE. SWARM. ⚡️🔥")
    return 0


if __name__ == "__main__":
    sys.exit(main())
