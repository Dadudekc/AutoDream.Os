#!/usr/bin/env python3
"""From ..core.unified_entry_point_system import main Discord Administrator Commander
Launcher Launch script for the Discord Administrator Commander bot.

This script launches the Discord Administrator Commander with Administrator privileges
for comprehensive server management capabilities.

Author: Agent-7 - V2 SWARM CAPTAIN

EXAMPLE USAGE:
==============

# Run the script directly
python run_admin_commander.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.execution.run_admin_commander import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.execution.run_admin_commander import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

"""

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
    get_logger(__name__).info("✅ Loaded environment variables from .env file")
except ImportError:
    get_logger(__name__).info("⚠️  python-dotenv not installed, using system environment variables")
    get_logger(__name__).info("   Install with: pip install python-dotenv")

# Add src to path for imports
current_dir = get_unified_utility().Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def load_env_file():
    """Load environment variables from .env file manually if dotenv not available."""
    env_file = get_unified_utility().Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        get_logger(__name__).info("✅ Loaded environment variables from .env file manually")
    else:
        get_logger(__name__).info("⚠️  No .env file found")


# Load .env file if dotenv not available
if "dotenv" not in sys.modules:
    load_env_file()

# Import the admin commander


if __name__ == "__main__":
    main()
