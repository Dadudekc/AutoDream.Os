#!/usr/bin/env python3
"""
Dream.OS + DreamVault Setup Script - Automated Installation.

V2 Compliance: Setup automation for Dream.OS and DreamVault integration
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
    """Install Dream.OS and DreamVault dependencies."""
    logger.info("📦 Installing Dream.OS + DreamVault dependencies...")
    
    dependencies = [
        # Dream.OS dependencies
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        
        # DreamVault dependencies
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "requests>=2.31.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0"
    ]
    
    try:
        for dep in dependencies:
            logger.info(f"   Installing {dep}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep, "-q"
            ])
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False


def create_runtime_directories():
    """Create runtime directories for Dream.OS and DreamVault."""
    logger.info("📁 Creating runtime directories...")
    
    dirs = [
        # Dream.OS directories
        Path("runtime/dreamos/fsm_data"),
        Path("runtime/dreamos/workflows"),
        Path("runtime/dreamos/tasks"),
        Path("logs/dreamos"),
        
        # DreamVault directories
        Path("runtime/dreamvault/database"),
        Path("runtime/dreamvault/embeddings"),
        Path("runtime/dreamvault/cookies"),
        Path("logs/dreamvault")
    ]
    
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"   Created: {directory}")
    
    logger.info("✅ Runtime directories created")
    return True


def test_imports():
    """Test that Dream.OS and DreamVault can be imported."""
    logger.info("🧪 Testing imports...")
    
    success = True
    
    # Test Dream.OS import
    try:
        from src.gaming.dreamos import FSMOrchestrator
        logger.info("✅ Dream.OS import successful")
        logger.info(f"   FSMOrchestrator: {FSMOrchestrator}")
    except ImportError as e:
        logger.warning(f"⚠️ Dream.OS import failed (may need dependencies): {e}")
        success = False
    
    # Test DreamVault import
    try:
        from src.ai_training.dreamvault import Config, Database
        logger.info("✅ DreamVault import successful")
        logger.info(f"   Config: {Config}")
        logger.info(f"   Database: {Database}")
    except ImportError as e:
        logger.warning(f"⚠️ DreamVault import failed (may need dependencies): {e}")
        success = False
    
    return success


def main():
    """Main setup execution."""
    logger.info("🚀 Dream.OS + DreamVault Setup Starting...")
    logger.info("=" * 60)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        logger.error("❌ Setup failed: Dependencies installation failed")
        return 1
    
    # Step 2: Create runtime directories
    if not create_runtime_directories():
        logger.error("❌ Setup failed: Directory creation failed")
        return 1
    
    # Step 3: Test imports
    if not test_imports():
        logger.warning("⚠️ Setup complete but imports failed")
        logger.warning("   You may need to install additional dependencies")
        logger.warning("   Run: pip install -r requirements.txt")
        return 0
    
    logger.info("=" * 60)
    logger.info("✅ Dream.OS + DreamVault setup complete!")
    logger.info("")
    logger.info("📋 Dream.OS Usage:")
    logger.info("   from src.gaming.dreamos import FSMOrchestrator")
    logger.info("")
    logger.info("📋 DreamVault Usage:")
    logger.info("   from src.ai_training.dreamvault import Config, Database")
    logger.info("   from src.ai_training.dreamvault.scrapers import ChatGPTScraper")
    logger.info("")
    logger.info("🐝 WE. ARE. SWARM. ⚡️🔥")
    return 0


if __name__ == "__main__":
    sys.exit(main())



