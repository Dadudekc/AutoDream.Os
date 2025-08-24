"""
Configuration Loader - Unified Configuration Management
"""
import json
import yaml

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Any, Dict, Union

class ConfigLoader:
    """Unified configuration loader for all config types"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON configuration file"""
        filepath = self.config_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        filepath = self.config_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration file (auto-detect type)"""
        if filename.endswith('.json'):
            return self.load_json(filename)
        elif filename.endswith(('.yaml', '.yml')):
            return self.load_yaml(filename)
        else:
            # Try both formats
            result = self.load_json(filename)
            if not result:
                result = self.load_yaml(filename)
            return result

# Global config loader instance
config_loader = ConfigLoader()

def get_config(filename: str) -> Dict[str, Any]:
    """Get configuration from file"""
    return config_loader.load_config(filename)

def get_system_config() -> Dict[str, Any]:
    """Get system configuration"""
    return get_config("system/performance.json")

def get_agent_config() -> Dict[str, Any]:
    """Get agent configuration"""
    return get_config("agents/agent_config.json")

def get_service_config(service: str) -> Dict[str, Any]:
    """Get service-specific configuration"""
    return get_config(f"services/{service}.yaml")
