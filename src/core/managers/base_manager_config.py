
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Base Manager Configuration - Agent Cellphone V2
=============================================

Configuration management functionality for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .base_manager_types import ManagerConfig


class BaseManagerConfiguration:
    """
    Configuration management functionality for base managers.
    
    Handles config updates, file loading, and configuration validation.
    """
    
    def __init__(self, manager_id: str, name: str, description: str, logger: logging.Logger):
        self.manager_id = manager_id
        self.name = name
        self.description = description
        self.logger = logger
        self.config = ManagerConfig(
            manager_id=manager_id,
            name=name,
            description=description
        )
    
    def update_config(self, **kwargs) -> bool:
        """Update manager configuration - common config method"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    self.logger.info(f"Updated config {key}: {value}")
                else:
                    self.logger.warning(f"Unknown config key: {key}")
            
            self.config.updated_at = datetime.now()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update config: {e}")
            return False
    
    def load_config_from_file(self, config_file: str) -> bool:
        """Load configuration from file - common config method"""
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                self.logger.error(f"Config file not found: {config_file}")
                return False
            
            with open(config_path, "r") as f:
                config_data = json.load(f)
            
            # Update config with file data
            for key, value in config_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    self.logger.info(f"Loaded config {key}: {value}")
            
            self.config.updated_at = datetime.now()
            self.logger.info(f"Configuration loaded from {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load config from {config_file}: {e}")
            return False
    
    def save_config_to_file(self, config_file: str) -> bool:
        """Save current configuration to file"""
        try:
            config_path = Path(config_file)
            
            # Convert config to dict for JSON serialization
            config_dict = {
                "manager_id": self.config.manager_id,
                "name": self.config.name,
                "description": self.config.description,
                "enabled": self.config.enabled,
                "auto_start": self.config.auto_start,
                "heartbeat_interval": self.config.heartbeat_interval,
                "max_retries": self.config.max_retries,
                "timeout_seconds": self.config.timeout_seconds,
                "log_level": self.config.log_level
            }
            
            with open(config_path, "w") as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            self.logger.info(f"Configuration saved to {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config to {config_file}: {e}")
            return False
    
    def get_config(self) -> ManagerConfig:
        """Get current configuration"""
        return self.config
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            "manager_id": self.config.manager_id,
            "name": self.config.name,
            "description": self.config.description,
            "enabled": self.config.enabled,
            "auto_start": self.config.auto_start,
            "heartbeat_interval": self.config.heartbeat_interval,
            "max_retries": self.config.max_retries,
            "timeout_seconds": self.config.timeout_seconds,
            "log_level": self.config.log_level,
            "created_at": self.config.created_at.isoformat(),
            "updated_at": self.config.updated_at.isoformat()
        }

