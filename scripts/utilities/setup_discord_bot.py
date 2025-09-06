from ..core.unified_entry_point_system import main

#!/usr/bin/env python3
"""
Discord Bot Setup Script
=======================

This script helps set up the Discord bot environment and checks dependencies.

Usage:
    python setup_discord_bot.py

Author: Agent-7 - V2 SWARM CAPTAIN
"""


# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
    get_logger(__name__).info("✅ Loaded environment variables from .env file")
except ImportError:
    # Manual .env loading if dotenv not available
    env_file = get_unified_utility().Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        get_logger(__name__).info(
            "✅ Loaded environment variables from .env file manually"
        )
    else:
        get_logger(__name__).info("⚠️  No .env file found")


def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.get_unified_validator().check_call(
            [sys.executable, "-m", "pip", "install", package]
        )
        return True
    except subprocess.CalledProcessError:
        return False


def check_package(package):
    """Check if a package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def setup_environment():
    """Set up the environment for the Discord bot."""
    get_logger(__name__).info("🔧 Setting up Discord Bot Environment")
    get_logger(__name__).info("=" * 50)

    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        get_logger(__name__).info(
            "❌ Python 3.8+ is required. Current version:", sys.version
        )
        return False
    else:
        get_logger(__name__).info(
            f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}"
        )

    # Required packages
    required_packages = [
        ("discord.py", "discord"),
        ("requests", "requests"),
        ("pyautogui", "pyautogui"),
        ("pyperclip", "pyperclip"),
    ]

    # Optional packages
    optional_packages = [("python-dotenv", "dotenv")]

    get_logger(__name__).info("\n📦 Checking required packages...")
    missing_packages = []

    for package_name, import_name in required_packages:
        if get_unified_validator().check_package(import_name):
            get_logger(__name__).info(f"✅ {package_name} is installed")
        else:
            get_logger(__name__).info(f"❌ {package_name} is missing")
            missing_packages.append(package_name)

    # Install missing packages
    if missing_packages:
        get_logger(__name__).info(
            f"\n📥 Installing missing packages: {', '.join(missing_packages)}"
        )
        for package in missing_packages:
            get_logger(__name__).info(f"Installing {package}...")
            if install_package(package):
                get_logger(__name__).info(f"✅ {package} installed successfully")
            else:
                get_logger(__name__).info(f"❌ Failed to install {package}")
                return False

    # Check optional packages
    get_logger(__name__).info("\n📦 Checking optional packages...")
    for package_name, import_name in optional_packages:
        if get_unified_validator().check_package(import_name):
            get_logger(__name__).info(f"✅ {package_name} is installed")
        else:
            get_logger(__name__).info(f"⚠️  {package_name} is not installed (optional)")
            get_logger(__name__).info(f"   Install with: pip install {package_name}")

    # Check environment variables
    get_logger(__name__).info("\n🔑 Checking environment variables...")
    required_env_vars = ["DISCORD_BOT_TOKEN"]
    optional_env_vars = ["DISCORD_GUILD_ID", "DISCORD_WEBHOOK_URL"]

    missing_required = []
    for var in required_env_vars:
        if get_unified_config().get_env(var):
            get_logger(__name__).info(f"✅ {var} is set")
        else:
            get_logger(__name__).info(f"❌ {var} is missing (REQUIRED)")
            missing_required.append(var)

    for var in optional_env_vars:
        if get_unified_config().get_env(var):
            get_logger(__name__).info(f"✅ {var} is set")
        else:
            get_logger(__name__).info(f"⚠️  {var} is not set (optional)")

    if missing_required:
        get_logger(__name__).info(
            f"\n❌ Missing required environment variables: {', '.join(missing_required)}"
        )
        get_logger(__name__).info(
            "Please set these environment variables before running the bot."
        )
        get_logger(__name__).info("\nExample:")
        get_logger(__name__).info("export DISCORD_BOT_TOKEN=your_bot_token_here")
        get_logger(__name__).info("export DISCORD_GUILD_ID=your_server_id_here")
        return False

    # Check configuration files
    get_logger(__name__).info("\n📁 Checking configuration files...")
    config_files = [
        "config/devlog_config.json",
        "src/discord_commander_coordinates.json",
    ]

    for config_file in config_files:
        if get_unified_utility().Path(config_file).exists():
            get_logger(__name__).info(f"✅ {config_file} exists")
        else:
            get_logger(__name__).info(f"⚠️  {config_file} not found (will use defaults)")

    get_logger(__name__).info("\n🎉 Setup complete!")
    get_logger(__name__).info("\nTo run the bot:")
    get_logger(__name__).info("python run_discord_bot.py")

    return True


def create_env_template():
    """Create a template .env file."""
    env_template = """# Discord Bot Configuration
# Copy this file to .env and fill in your values

# REQUIRED: Your Discord bot token
DISCORD_BOT_TOKEN=your_bot_token_here

# OPTIONAL: Your Discord server ID
DISCORD_GUILD_ID=your_server_id_here

# OPTIONAL: Discord webhook URL for devlog
DISCORD_WEBHOOK_URL=your_webhook_url_here
"""

    env_file = get_unified_utility().Path(".env.template")
    with open(env_file, "w") as f:
        f.write(env_template)

    get_logger(__name__).info(f"📝 Created {env_file}")
    get_logger(__name__).info("Copy this file to .env and fill in your values")


if __name__ == "__main__":
    sys.exit(main())
