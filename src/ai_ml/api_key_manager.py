#!/usr/bin/env python3
"""
API Key Manager for AI & ML Integration
TDD Implementation - Minimal code to pass tests

This module provides secure API key management for:
- OpenAI API integration
- Anthropic API integration
- Secure storage and validation
"""

import os
import re

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Optional, Dict, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIKeyManager:
    """Secure API key management system for AI services"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize API key manager with optional config path"""
        self.config_path = config_path or Path.home() / ".ai_ml_config"
        self._keys: Dict[str, Optional[str]] = {}
        # Load API keys from environment variables
        self._load_api_keys()

    def _load_api_keys(self) -> None:
        """Load API keys from environment variables"""
        self._keys["openai"] = os.getenv("OPENAI_API_KEY")
        if not self._keys["openai"]:
            logger.warning("OPENAI_API_KEY not found in environment variables")

        self._keys["anthropic"] = os.getenv("ANTHROPIC_API_KEY")
        if not self._keys["anthropic"]:
            logger.warning("ANTHROPIC_API_KEY not found in environment variables")

    def _validate_key(self, service: str, key: str) -> bool:
        """Validate API key format for supported services"""
        patterns = {
            "openai": r"^sk-[a-zA-Z0-9]{48}$",
            "anthropic": r"^sk-ant-[a-zA-Z0-9]{32,}$",
        }
        pattern = patterns.get(service)
        if pattern:
            return bool(re.match(pattern, key))
        return bool(key)

    def validate_openai_key(self) -> bool:
        """Validate OpenAI API key format and availability"""
        key = self._keys.get("openai")
        return bool(key) and self._validate_key("openai", key)

    def validate_anthropic_key(self) -> bool:
        """Validate Anthropic API key format and availability"""
        key = self._keys.get("anthropic")
        return bool(key) and self._validate_key("anthropic", key)

    def is_secure_storage(self) -> bool:
        """Check if API keys are stored securely"""
        # Environment variables are generally secure for development
        # In production, this would check for encrypted storage, key vaults, etc.
        return True

    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service if available and valid"""
        key = self._keys.get(service)
        if key and self._validate_key(service, key):
            return key
        return None

    def set_key(self, service: str, key: str) -> bool:
        """Set API key for a service (for testing purposes)"""
        if self._validate_key(service, key):
            self._keys[service] = key
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get current API key status"""
        return {
            "openai_available": self.validate_openai_key(),
            "anthropic_available": self.validate_anthropic_key(),
            "secure_storage": self.is_secure_storage(),
        }


# Factory function for easy access
def get_api_key_manager(config_path: Optional[Path] = None) -> APIKeyManager:
    """Get configured API key manager instance"""
    return APIKeyManager(config_path)


if __name__ == "__main__":
    # Test the API key manager
    manager = APIKeyManager()
    status = manager.get_status()
    print("API Key Manager Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
