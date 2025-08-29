"""
ML Framework Module
Extracted from core.py for modularization

Contains:
- MLFramework: Abstract base class for ML frameworks
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

from .models import AIModel, MLWorkflow

# Configure logging
logger = logging.getLogger(__name__)


class MLFramework(ABC):
    """Abstract base class for ML frameworks

    Provides common interface for different ML frameworks
    """

    def __init__(self, name: str, version: str):
        """Initialize ML framework"""
        self.name = name
        self.version = version
        self.supported_models: List[str] = []
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the ML framework"""
        pass

    @abstractmethod
    def load_model(self, model_path: Union[str, Path]) -> Any:
        """Load a model from path"""
        pass

    @abstractmethod
    def save_model(self, model: Any, model_path: Union[str, Path]) -> bool:
        """Save a model to path"""
        pass

    @abstractmethod
    def predict(self, model: Any, input_data: Any) -> Any:
        """Make predictions using a model"""
        pass

    @abstractmethod
    def train(self, model: Any, training_data: Any, **kwargs) -> bool:
        """Train a model"""
        pass

    @abstractmethod
    def evaluate(self, model: Any, test_data: Any) -> Dict[str, float]:
        """Evaluate model performance"""
        pass

    def get_supported_models(self) -> List[str]:
        """Get list of supported model types"""
        return self.supported_models

    def add_supported_model(self, model_type: str) -> None:
        """Add a supported model type"""
        if model_type not in self.supported_models:
            self.supported_models.append(model_type)
            self.logger.info(f"Added supported model type: {model_type}")

    def remove_supported_model(self, model_type: str) -> bool:
        """Remove a supported model type"""
        if model_type in self.supported_models:
            self.supported_models.remove(model_type)
            self.logger.info(f"Removed supported model type: {model_type}")
            return True
        return False

    def get_config(self) -> Dict[str, Any]:
        """Get framework configuration"""
        return self.config.copy()

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update framework configuration"""
        try:
            self.config.update(updates)
            self.logger.info(f"Updated configuration: {list(updates.keys())}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    def validate_config(self) -> bool:
        """Validate framework configuration"""
        try:
            required_keys = ["framework_name", "version"]
            for key in required_keys:
                if key not in self.config:
                    self.logger.error(f"Missing required config key: {key}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False

    def get_framework_info(self) -> Dict[str, Any]:
        """Get framework information"""
        return {
            "name": self.name,
            "version": self.version,
            "supported_models": self.supported_models,
            "config_keys": list(self.config.keys())
        }

    def export_config(self, config_path: Union[str, Path]) -> bool:
        """Export configuration to file"""
        try:
            config_path = Path(config_path)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info(f"Exported configuration to {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            return False

    def import_config(self, config_path: Union[str, Path]) -> bool:
        """Import configuration from file"""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                self.logger.error(f"Configuration file not found: {config_path}")
                return False
            
            with open(config_path, "r") as f:
                imported_config = json.load(f)
            
            self.config.update(imported_config)
            self.logger.info(f"Imported configuration from {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import configuration: {e}")
            return False

    def cleanup(self) -> None:
        """Cleanup framework resources"""
        try:
            self.logger.info(f"Cleaning up {self.name} framework")
            # Framework-specific cleanup logic here
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")

    def __str__(self) -> str:
        """String representation of framework"""
        return f"{self.name} v{self.version}"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"MLFramework(name='{self.name}', version='{self.version}', supported_models={self.supported_models})"
