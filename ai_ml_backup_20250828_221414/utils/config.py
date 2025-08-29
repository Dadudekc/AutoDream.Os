import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def config_loader(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if config_path is None:
        config_path = "config/ai_ml/ai_ml.json"
    config_file = Path(config_path)
    if not config_file.exists():
        logger.warning(f"Configuration file not found: {config_path}")
        return {}
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from: {config_path}")
        return config
    except Exception as e:  # pragma: no cover - logging path
        logger.error(f"Error loading configuration from {config_path}: {e}")
        return {}


def setup_environment_variables() -> bool:
    """Setup environment variables from .env file."""
    try:
        from dotenv import load_dotenv

        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("Environment variables loaded from .env file")
            return True
        logger.warning(".env file not found. Using system environment variables.")
        return False
    except ImportError:  # pragma: no cover - dependency optional
        logger.warning("python-dotenv not installed. Cannot load .env file.")
        return False


def get_api_keys() -> Dict[str, Optional[str]]:
    """Get API keys from environment variables."""
    api_keys = {
        "openai": os.getenv("OPENAI_API_KEY"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "organization": os.getenv("OPENAI_ORGANIZATION"),
    }
    for service, key in api_keys.items():
        if key:
            logger.info(f"{service.title()} API key configured")
        else:
            logger.warning(f"{service.title()} API key not configured")
    return api_keys


def get_config_manager(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Return configuration data for compatibility."""
    return config_loader(config_path)
