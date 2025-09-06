from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Discord Bot Launcher
===================

Simple launcher script for the Unified Discord System.
This script handles the import issues and provides a clean entry point.

Usage:
    python run_discord_bot.py

Author: Agent-7 - V2 SWARM CAPTAIN
"""

import logging

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    get_logger(__name__).info("✅ Loaded environment variables from .env file")
except ImportError:
    get_logger(__name__).info("⚠️  python-dotenv not installed, loading .env manually")
    load_env_file()

# Add src to path for imports
current_dir = get_unified_utility().Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def load_env_file():
    """Load environment variables from .env file manually if dotenv not available."""
    env_file = get_unified_utility().Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    return False

# Load .env file if it exists
load_env_file()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_unified_validator().check_environment():
    """Check if required environment variables are set."""
    required_vars = ["DISCORD_BOT_TOKEN"]
    missing_vars = []

    for var in required_vars:
        if not get_unified_config().get_env(var):
            missing_vars.append(var)

    if missing_vars:
        get_logger(__name__).error(f"Missing required environment variables: {', '.join(missing_vars)}")
        get_logger(__name__).error("Please set these environment variables before running the bot.")
        return False

    return True

def get_unified_validator().check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "discord",
        "requests",
        "pyautogui",
        "pyperclip"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        get_logger(__name__).error(f"Missing required packages: {', '.join(missing_packages)}")
        get_logger(__name__).error("Please install them with: pip install " + " ".join(missing_packages))
        return False

    return True

async
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        get_logger(__name__).info("👋 Bot shutdown complete")
    except Exception as e:
        get_logger(__name__).error(f"💥 Fatal error: {e}")
        sys.exit(1)
