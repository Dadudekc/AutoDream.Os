#!/usr/bin/env python3
"""
Unified Configuration Service - Modular Components
==================================================

Split from unified_configuration_service.py (835 lines) to achieve V2 compliance.
This module contains the core service components.

Author: Agent-1 (PERPETUAL MOTION LEADER - V2 COMPLIANCE SPECIALIST)
Mission: V2 COMPLIANCE OPTIMIZATION - File Size Reduction
License: MIT
"""

import json
import yaml
import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ConfigurationServiceConfig:
    """Configuration service settings"""
    enable_caching: bool = True
    cache_ttl: int = 300
    max_config_size: int = 1024 * 1024  # 1MB
    enable_validation: bool = True


class ConfigurationServiceCore:
    """Core configuration service functionality"""
    
    def __init__(self, config: ConfigurationServiceConfig):
        self.config = config
        self.cache = {}
        self.cache_timestamps = {}
        
    def load_config(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            logger.error(f"Failed to load config {file_path}: {e}")
            return {}
    
    def save_config(self, config: Dict[str, Any], file_path: str) -> bool:
        """Save configuration to file"""
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                with open(file_path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config {file_path}: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure"""
        if not self.config.enable_validation:
            return True
            
        try:
            # Basic validation - can be extended
            if not isinstance(config, dict):
                return False
            return True
        except Exception as e:
            logger.error(f"Config validation failed: {e}")
            return False


class ConfigurationCacheManager:
    """Configuration caching functionality"""
    
    def __init__(self, config: ConfigurationServiceConfig):
        self.config = config
        self.cache = {}
        self.timestamps = {}
        
    def get_cached(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached configuration"""
        if not self.config.enable_caching:
            return None
            
        if key in self.cache:
            timestamp = self.timestamps.get(key, 0)
            if datetime.now().timestamp() - timestamp < self.config.cache_ttl:
                return self.cache[key]
            else:
                # Expired, remove from cache
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set_cached(self, key: str, config: Dict[str, Any]) -> None:
        """Cache configuration"""
        if not self.config.enable_caching:
            return
            
        self.cache[key] = config
        self.timestamps[key] = datetime.now().timestamp()




# Main service class that orchestrates all components
class UnifiedConfigurationService:
    """Unified configuration service - main orchestrator"""
    
    def __init__(self, config: ConfigurationServiceConfig = None):
        self.config = config or ConfigurationServiceConfig()
        self.core = ConfigurationServiceCore(self.config)
        self.cache_manager = ConfigurationCacheManager(self.config)
        
    def load_configuration(self, file_path: str) -> Dict[str, Any]:
        """Load configuration with caching and validation"""
        # Check cache first
        cached = self.cache_manager.get_cached(file_path)
        if cached:
            return cached
            
        # Load from file
        config = self.core.load_config(file_path)
        
        # Validate
        if not self.core.validate_config(config):
            logger.error(f"Invalid configuration in {file_path}")
            return {}
            
        # Cache result
        self.cache_manager.set_cached(file_path, config)            
        return config
    
    def save_configuration(self, config: Dict[str, Any], file_path: str) -> bool:
        """Save configuration"""            
        # Save to file
        success = self.core.save_config(config, file_path)
        
        # Update cache
        if success:
            self.cache_manager.set_cached(file_path, config)
            
        return success
    
    def cleanup(self) -> int:
        """No backups to clean; rely on version control"""
        return 0


if __name__ == "__main__":
    # Test the modularized configuration service
    service = UnifiedConfigurationService()
    
    # Test configuration
    test_config = {
        "app_name": "TestApp",
        "version": "1.0.0",
        "settings": {
            "debug": True,
            "port": 8080
        }
    }
    
    # Test save and load
    test_file = "test_config.json"
    if service.save_configuration(test_config, test_file):
        loaded_config = service.load_configuration(test_file)
        print(f"✅ Configuration service test successful")
        print(f"Loaded config: {loaded_config}")
    else:
        print("❌ Configuration service test failed")
    
    # Cleanup test file
    if os.path.exists(test_file):
        os.remove(test_file)
