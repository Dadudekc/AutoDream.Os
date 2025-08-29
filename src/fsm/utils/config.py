"""
Configuration Management - FSM Core V2 Modularization
Captain Agent-3: Configuration Utility Implementation
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class FSMConfig:
    """Manages FSM configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "fsm_config.json"
        self.config_data = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
                return True
            return False
        except Exception:
            return False
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config_data.get(key, default)
