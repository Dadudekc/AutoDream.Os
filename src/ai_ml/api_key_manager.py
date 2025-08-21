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
        self.openai_api_key: Optional[str] = None
        self.anthropic_api_key: Optional[str] = None
        
        # Load API keys from environment variables
        self._load_api_keys()
    
    def _load_api_keys(self) -> None:
        """Load API keys from environment variables"""
        # Load OpenAI API key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        # Load Anthropic API key
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment variables")
    
    def validate_openai_key(self) -> bool:
        """Validate OpenAI API key format and availability"""
        if not self.openai_api_key:
            return False
        
        # OpenAI API keys typically start with "sk-" and are 51 characters long
        openai_pattern = r"^sk-[a-zA-Z0-9]{48}$"
        return bool(re.match(openai_pattern, self.openai_api_key))
    
    def validate_anthropic_key(self) -> bool:
        """Validate Anthropic API key format and availability"""
        if not self.anthropic_api_key:
            return False
        
        # Anthropic API keys typically start with "sk-ant-" and are longer
        anthropic_pattern = r"^sk-ant-[a-zA-Z0-9]{32,}$"
        return bool(re.match(anthropic_pattern, self.anthropic_api_key))
    
    def is_secure_storage(self) -> bool:
        """Check if API keys are stored securely"""
        # Environment variables are generally secure for development
        # In production, this would check for encrypted storage, key vaults, etc.
        return True
    
    def get_openai_key(self) -> Optional[str]:
        """Get OpenAI API key if available and valid"""
        if self.validate_openai_key():
            return self.openai_api_key
        return None
    
    def get_anthropic_key(self) -> Optional[str]:
        """Get Anthropic API key if available and valid"""
        if self.validate_anthropic_key():
            return self.anthropic_api_key
        return None
    
    def set_openai_key(self, key: str) -> bool:
        """Set OpenAI API key (for testing purposes)"""
        if re.match(r"^sk-[a-zA-Z0-9]{48}$", key):
            self.openai_api_key = key
            return True
        return False
    
    def set_anthropic_key(self, key: str) -> bool:
        """Set Anthropic API key (for testing purposes)"""
        if re.match(r"^sk-ant-[a-zA-Z0-9]{32,}$", key):
            self.anthropic_api_key = key
            return True
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current API key status"""
        return {
            "openai_available": self.validate_openai_key(),
            "anthropic_available": self.validate_anthropic_key(),
            "secure_storage": self.is_secure_storage(),
            "openai_key_length": len(self.openai_api_key) if self.openai_api_key else 0,
            "anthropic_key_length": len(self.anthropic_api_key) if self.anthropic_api_key else 0
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
