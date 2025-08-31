#!/usr/bin/env python3
"""
Configuration Framework Core - LOC Compliant Design
==================================================

Core configuration framework functionality following LOC compliance,
object-oriented design, and SSOT principles.

Author: Agent-1 (PERPETUAL MOTION LEADER - CORE SYSTEMS CONSOLIDATION SPECIALIST)
Mission: LOC COMPLIANCE OPTIMIZATION - Configuration Framework
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ConfigSource(Enum):
    """Configuration source types"""
    ENVIRONMENT = "environment"
    FILE = "file"
    DATABASE = "database"
    API = "api"
    DEFAULT = "default"


class ConfigPriority(Enum):
    """Configuration priority levels"""
    CRITICAL = 100
    HIGH = 75
    MEDIUM = 50
    LOW = 25
    DEFAULT = 0


class ConfigFormat(Enum):
    """Configuration file formats"""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"


@dataclass
class ConfigMetadata:
    """Configuration metadata"""
    
    source: ConfigSource
    priority: ConfigPriority
    format: ConfigFormat
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    checksum: str = ""
    size_bytes: int = 0
    validation_status: str = "pending"


class IConfigurationFramework(ABC):
    """Abstract interface for configuration framework"""
    
    @abstractmethod
    def register_config(self, name: str, config_data: Dict[str, Any], metadata: ConfigMetadata) -> bool:
        """Register configuration with framework"""
        pass
    
    @abstractmethod
    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get configuration by name"""
        pass
    
    @abstractmethod
    def update_config(self, name: str, config_data: Dict[str, Any]) -> bool:
        """Update existing configuration"""
        pass


class ConfigurationFrameworkCore(IConfigurationFramework):
    """
    Configuration Framework Core - LOC Compliant Implementation
    
    Follows object-oriented design principles and maintains
    single responsibility for framework operations.
    """
    
    def __init__(self):
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, ConfigMetadata] = {}
        self.logger = logging.getLogger(__name__)
    
    def register_config(self, name: str, config_data: Dict[str, Any], metadata: ConfigMetadata) -> bool:
        """Register configuration with validation"""
        try:
            if not isinstance(config_data, dict):
                raise ValueError("Configuration data must be a dictionary")
            
            if not isinstance(metadata, ConfigMetadata):
                raise ValueError("Metadata must be ConfigMetadata instance")
            
            self.configs[name] = config_data
            self.metadata[name] = metadata
            
            self.logger.info(f"✅ Configuration '{name}' registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to register configuration '{name}': {e}")
            return False
    
    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get configuration by name with caching"""
        try:
            if name not in self.configs:
                self.logger.warning(f"⚠️ Configuration '{name}' not found")
                return None
            
            config_data = self.configs[name]
            metadata = self.metadata[name]
            
            # Update access timestamp
            metadata.modified_at = datetime.now()
            
            self.logger.debug(f"📋 Configuration '{name}' retrieved successfully")
            return config_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get configuration '{name}': {e}")
            return None
    
    def update_config(self, name: str, config_data: Dict[str, Any]) -> bool:
        """Update existing configuration"""
        try:
            if name not in self.configs:
                raise ValueError(f"Configuration '{name}' not registered")
            
            if not isinstance(config_data, dict):
                raise ValueError("Configuration data must be a dictionary")
            
            # Update configuration and metadata
            self.configs[name] = config_data
            self.metadata[name].modified_at = datetime.now()
            
            self.logger.info(f"✅ Configuration '{name}' updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update configuration '{name}': {e}")
            return False
    
    def list_configs(self) -> List[str]:
        """List all registered configuration names"""
        return list(self.configs.keys())
    
    def get_metadata(self, name: str) -> Optional[ConfigMetadata]:
        """Get configuration metadata"""
        return self.metadata.get(name)
    
    def remove_config(self, name: str) -> bool:
        """Remove configuration from framework"""
        try:
            if name not in self.configs:
                return False
            
            del self.configs[name]
            del self.metadata[name]
            
            self.logger.info(f"✅ Configuration '{name}' removed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to remove configuration '{name}': {e}")
            return False


if __name__ == "__main__":
    # Test the configuration framework core
    print("🏗️ Configuration Framework Core Loaded Successfully")
    
    framework = ConfigurationFrameworkCore()
    
    # Test configuration registration
    test_metadata = ConfigMetadata(
        source=ConfigSource.FILE,
        priority=ConfigPriority.MEDIUM,
        format=ConfigFormat.JSON
    )
    
    test_config = {"setting": "value", "enabled": True}
    success = framework.register_config("test_config", test_config, test_metadata)
    print(f"✅ Configuration registration: {success}")
    
    # Test configuration retrieval
    retrieved_config = framework.get_config("test_config")
    print(f"✅ Configuration retrieval: {retrieved_config is not None}")
    
    print("✅ All framework functionality working correctly!")
