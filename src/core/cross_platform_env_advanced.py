"""Cross-Platform Environment Advanced - Configuration and validation"""

import logging
from pathlib import Path
from typing import Any

from .cross_platform_env_core import CrossPlatformEnvironment

logger = logging.getLogger(__name__)


class EnvironmentConfig:
    """Environment configuration management"""

    def __init__(self):
        self.env = CrossPlatformEnvironment()

    def get_platform_info(self) -> dict[str, Any]:
        """Get platform information."""
        return {
            "platform": self.env.platform,
            "is_windows": self.env.is_windows,
            "is_linux": self.env.is_linux,
            "is_macos": self.env.is_macos,
            "python_version": self.env.get_python_version(),
            "python_path": str(self.env.get_python_path())
        }

    def load_env_file(self, env_file: str | Path) -> bool:
        """Load environment variables from file."""
        try:
            env_path = Path(env_file)
            if not env_path.exists():
                logger.warning(f"Environment file not found: {env_file}")
                return False

            with open(env_path, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.env.set_env_var(key.strip(), value.strip())

            logger.info(f"Loaded environment from {env_file}")
            return True

        except Exception as e:
            logger.error(f"Error loading env file: {e}")
            return False

    def get_agent_config(self) -> dict[str, Any]:
        """Get agent configuration from environment."""
        return {
            "agent_id": self.env.get_env_var("AGENT_ID", "Agent-5"),
            "workspace_path": self.env.get_env_var("WORKSPACE_PATH", "."),
            "config_path": self.env.get_env_var("CONFIG_PATH", "config"),
            "log_level": self.env.get_env_var("LOG_LEVEL", "INFO")
        }

    def validate_required_env_vars(self, required_vars: list) -> dict[str, bool]:
        """Validate required environment variables."""
        results = {}
        for var in required_vars:
            results[var] = self.env.get_env_var(var) is not None
        return results

    def get_development_config(self) -> dict[str, Any]:
        """Get development configuration."""
        return {
            "debug": self.env.get_env_var("DEBUG", "false").lower() == "true",
            "log_level": self.env.get_env_var("LOG_LEVEL", "INFO"),
            "dev_mode": self.env.get_env_var("DEV_MODE", "false").lower() == "true"
        }

