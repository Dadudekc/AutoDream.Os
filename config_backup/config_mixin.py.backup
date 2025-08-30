from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import json


@dataclass
class ManagerConfig:
    """Unified manager configuration"""

    manager_id: str
    name: str
    description: str
    enabled: bool = True
    auto_start: bool = True
    heartbeat_interval: int = 30
    max_retries: int = 3
    timeout_seconds: int = 60
    log_level: str = "INFO"
    config_file: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ConfigMixin:
    """Mixin providing configuration management."""

    def __init__(self, manager_id: str, name: str, description: str = "", *args, **kwargs):
        super().__init__(manager_id, name, description, *args, **kwargs)
        self.config = ManagerConfig(manager_id=manager_id, name=name, description=description)
        self.heartbeat_interval = self.config.heartbeat_interval

    def update_config(self, **kwargs) -> bool:
        """Update manager configuration."""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    if hasattr(self, "logger"):
                        self.logger.info(f"Updated config {key}: {value}")
                else:
                    if hasattr(self, "logger"):
                        self.logger.warning(f"Unknown config key: {key}")
            self.config.updated_at = datetime.now()
            return True
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.error(f"Failed to update config: {e}")
            return False

    def load_config_from_file(self, config_file: str) -> bool:
        """Load configuration from a JSON file."""
        try:
            if not Path(config_file).exists():
                if hasattr(self, "logger"):
                    self.logger.warning(f"Config file not found: {config_file}")
                return False
            with open(config_file, "r") as f:
                config_data = json.load(f)
            self.update_config(**config_data)
            self.config.config_file = config_file
            if hasattr(self, "logger"):
                self.logger.info(f"Loaded config from: {config_file}")
            return True
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.error(f"Failed to load config from {config_file}: {e}")
            return False
