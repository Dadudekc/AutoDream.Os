"""Cross-Platform Environment Utils - Helper functions"""

import platform
from .cross_platform_env_advanced import EnvironmentConfig

env_config = EnvironmentConfig()


def get_platform_info():
    """Get comprehensive platform information."""
    return env_config.get_platform_info()


def get_agent_config():
    """Get agent-specific configuration from environment."""
    return env_config.get_agent_config()


def get_development_config():
    """Get development-specific configuration."""
    return env_config.get_development_config()


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"

