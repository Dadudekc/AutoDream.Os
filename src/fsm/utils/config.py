
# MIGRATED: This file has been migrated to the centralized configuration system
"""
Configuration Management - FSM Core V2 Modularization
Captain Agent-3: Configuration Utility Implementation
"""

from typing import Dict, Any, Optional

from src.core.config_loader import load_config as _load_config

class FSMConfig:
    """Manages FSM configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "fsm_config.json"
        self.config_data: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> bool:
        """Load configuration using the project SSOT loader."""
        self.config_data = _load_config(self.config_path, {})
        return bool(self.config_data)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config_data.get(key, default)
