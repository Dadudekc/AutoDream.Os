#!/usr/bin/env python3
"""
Unified Configuration Management Framework - Agent-2 Consolidation Implementation
Consolidates all configuration management implementations into unified framework
"""

import json
import yaml
import os
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Callable, Type
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
import logging

# Import existing unified configuration classes
from unified_config_classes import (
    ConfigFormat, ConfigValidationLevel, ConfigType, ConfigMetadata,
    ConfigSection, ConfigValidationResult, ConfigChangeEvent,
    AIConfig, FSMConfig, PerformanceConfig, QualityConfig, MessagingConfig
)


@dataclass
class ConfigurationResult:
    """Unified configuration result structure."""
    success: bool
    data: Optional[Any] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_error(self, error: str) -> None:
        """Add configuration error."""
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str) -> None:
        """Add configuration warning."""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'success': self.success,
            'data': self.data,
            'errors': self.errors,
            'warnings': self.warnings,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class IConfigurationManager(ABC):
    """Unified configuration manager interface."""
    
    @abstractmethod
    def load_config(self, config_path: str, config_type: ConfigType) -> ConfigurationResult:
        """Load configuration from path."""
        pass
    
    @abstractmethod
    def save_config(self, config_path: str, config_data: Any) -> ConfigurationResult:
        """Save configuration to path."""
        pass
    
    @abstractmethod
    def get_config(self, config_name: str) -> ConfigurationResult:
        """Get configuration by name."""
        pass
    
    @abstractmethod
    def set_config(self, config_name: str, config_data: Any) -> ConfigurationResult:
        """Set configuration by name."""
        pass
    
    @abstractmethod
    def get_manager_name(self) -> str:
        """Get manager name."""
        pass


class IConfigurationLoader(ABC):
    """Unified configuration loader interface."""
    
    @abstractmethod
    def load(self, file_path: str) -> ConfigurationResult:
        """Load configuration from file."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[ConfigFormat]:
        """Get supported configuration formats."""
        pass
    
    @abstractmethod
    def get_loader_name(self) -> str:
        """Get loader name."""
        pass


class IConfigurationValidator(ABC):
    """Unified configuration validator interface."""
    
    @abstractmethod
    def validate(self, config_data: Any, validation_level: ConfigValidationLevel) -> ConfigValidationResult:
        """Validate configuration data."""
        pass
    
    @abstractmethod
    def get_validator_name(self) -> str:
        """Get validator name."""
        pass


class BaseConfigurationManager(IConfigurationManager):
    """Base configuration manager implementation."""
    
    def __init__(self, name: str, loaders: Optional[Dict[ConfigFormat, IConfigurationLoader]] = None, validators: Optional[List[IConfigurationValidator]] = None):
        """Initialize base configuration manager."""
        self.name = name
        self.loaders = loaders or {}
        self.validators = validators or []
        self.config_cache: Dict[str, Any] = {}
        self.config_history: List[ConfigChangeEvent] = []
        self.logger = logging.getLogger(f"ConfigManager.{name}")
    
    def load_config(self, config_path: str, config_type: ConfigType) -> ConfigurationResult:
        """Load configuration from path."""
        try:
            file_path = Path(config_path)
            if not file_path.exists():
                return ConfigurationResult(success=False, errors=[f"Configuration file not found: {config_path}"])
            
            # Determine format
            config_format = self._detect_format(file_path)
            if config_format not in self.loaders:
                return ConfigurationResult(success=False, errors=[f"No loader available for format: {config_format}"])
            
            # Load configuration
            loader = self.loaders[config_format]
            load_result = loader.load(str(file_path))
            
            if load_result.success:
                # Cache the configuration
                self.config_cache[config_path] = load_result.data
                
                # Record change event
                change_event = ConfigChangeEvent(
                    config_name=config_path,
                    change_type="load",
                    new_value=load_result.data,
                    timestamp=datetime.now().isoformat(),
                    source=self.name
                )
                self.config_history.append(change_event)
                
                # Validate if validators available
                if self.validators:
                    for validator in self.validators:
                        validation_result = validator.validate(load_result.data, ConfigValidationLevel.BASIC)
                        if not validation_result.is_valid:
                            load_result.add_warning(f"Validation warnings: {validation_result.warnings}")
                
                return load_result
            else:
                return load_result
                
        except Exception as e:
            error_msg = f"Error loading configuration from {config_path}: {e}"
            self.logger.error(error_msg)
            return ConfigurationResult(success=False, errors=[error_msg])
    
    def save_config(self, config_path: str, config_data: Any) -> ConfigurationResult:
        """Save configuration to path."""
        try:
            file_path = Path(config_path)
            
            # Determine format
            config_format = self._detect_format(file_path)
            
            # Save based on format
            if config_format == ConfigFormat.JSON:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            elif config_format == ConfigFormat.YAML:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            else:
                return ConfigurationResult(success=False, errors=[f"Unsupported format for saving: {config_format}"])
            
            # Update cache
            self.config_cache[config_path] = config_data
            
            # Record change event
            change_event = ConfigChangeEvent(
                config_name=config_path,
                change_type="save",
                new_value=config_data,
                timestamp=datetime.now().isoformat(),
                source=self.name
            )
            self.config_history.append(change_event)
            
            return ConfigurationResult(success=True, data=config_data)
            
        except Exception as e:
            error_msg = f"Error saving configuration to {config_path}: {e}"
            self.logger.error(error_msg)
            return ConfigurationResult(success=False, errors=[error_msg])
    
    def get_config(self, config_name: str) -> ConfigurationResult:
        """Get configuration by name."""
        if config_name in self.config_cache:
            return ConfigurationResult(success=True, data=self.config_cache[config_name])
        else:
            return ConfigurationResult(success=False, errors=[f"Configuration not found: {config_name}"])
    
    def set_config(self, config_name: str, config_data: Any) -> ConfigurationResult:
        """Set configuration by name."""
        try:
            old_value = self.config_cache.get(config_name)
            self.config_cache[config_name] = config_data
            
            # Record change event
            change_event = ConfigChangeEvent(
                config_name=config_name,
                change_type="update",
                old_value=old_value,
                new_value=config_data,
                timestamp=datetime.now().isoformat(),
                source=self.name
            )
            self.config_history.append(change_event)
            
            return ConfigurationResult(success=True, data=config_data)
            
        except Exception as e:
            error_msg = f"Error setting configuration {config_name}: {e}"
            self.logger.error(error_msg)
            return ConfigurationResult(success=False, errors=[error_msg])
    
    def get_manager_name(self) -> str:
        """Get manager name."""
        return self.name
    
    def _detect_format(self, file_path: Path) -> ConfigFormat:
        """Detect configuration file format."""
        suffix = file_path.suffix.lower()
        if suffix == '.json':
            return ConfigFormat.JSON
        elif suffix in ['.yaml', '.yml']:
            return ConfigFormat.YAML
        elif suffix == '.ini':
            return ConfigFormat.INI
        elif suffix == '.py':
            return ConfigFormat.PYTHON
        else:
            return ConfigFormat.AUTO
    
    def get_config_history(self) -> List[ConfigChangeEvent]:
        """Get configuration change history."""
        return self.config_history.copy()
    
    def clear_cache(self) -> None:
        """Clear configuration cache."""
        self.config_cache.clear()


class BaseConfigurationLoader(IConfigurationLoader):
    """Base configuration loader implementation."""
    
    def __init__(self, name: str, supported_formats: List[ConfigFormat]):
        """Initialize base configuration loader."""
        self.name = name
        self.supported_formats = supported_formats
        self.load_history: List[ConfigurationResult] = []
    
    def load(self, file_path: str) -> ConfigurationResult:
        """Load configuration from file."""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return ConfigurationResult(success=False, errors=[f"File not found: {file_path}"])
            
            # Determine format
            config_format = self._detect_format(file_path_obj)
            if config_format not in self.supported_formats:
                return ConfigurationResult(success=False, errors=[f"Unsupported format: {config_format}"])
            
            # Load based on format
            if config_format == ConfigFormat.JSON:
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif config_format == ConfigFormat.YAML:
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            else:
                return ConfigurationResult(success=False, errors=[f"Format not implemented: {config_format}"])
            
            result = ConfigurationResult(success=True, data=data)
            self.load_history.append(result)
            return result
            
        except Exception as e:
            error_msg = f"Error loading configuration from {file_path}: {e}"
            result = ConfigurationResult(success=False, errors=[error_msg])
            self.load_history.append(result)
            return result
    
    def get_supported_formats(self) -> List[ConfigFormat]:
        """Get supported configuration formats."""
        return self.supported_formats.copy()
    
    def get_loader_name(self) -> str:
        """Get loader name."""
        return self.name
    
    def _detect_format(self, file_path: Path) -> ConfigFormat:
        """Detect configuration file format."""
        suffix = file_path.suffix.lower()
        if suffix == '.json':
            return ConfigFormat.JSON
        elif suffix in ['.yaml', '.yml']:
            return ConfigFormat.YAML
        elif suffix == '.ini':
            return ConfigFormat.INI
        elif suffix == '.py':
            return ConfigFormat.PYTHON
        else:
            return ConfigFormat.AUTO
    
    def get_load_history(self) -> List[ConfigurationResult]:
        """Get load history."""
        return self.load_history.copy()


class BaseConfigurationValidator(IConfigurationValidator):
    """Base configuration validator implementation."""
    
    def __init__(self, name: str, validation_rules: Optional[Dict[str, Callable]] = None):
        """Initialize base configuration validator."""
        self.name = name
        self.validation_rules = validation_rules or {}
        self.validation_history: List[ConfigValidationResult] = []
    
    def validate(self, config_data: Any, validation_level: ConfigValidationLevel) -> ConfigValidationResult:
        """Validate configuration data."""
        result = ConfigValidationResult(
            is_valid=True,
            validation_level=validation_level,
            timestamp=datetime.now().isoformat(),
            validator_version="1.0.0"
        )
        
        # Apply validation rules based on level
        if validation_level == ConfigValidationLevel.NONE:
            pass
        elif validation_level == ConfigValidationLevel.BASIC:
            self._apply_basic_validation(config_data, result)
        elif validation_level == ConfigValidationLevel.STRICT:
            self._apply_strict_validation(config_data, result)
        elif validation_level == ConfigValidationLevel.COMPREHENSIVE:
            self._apply_comprehensive_validation(config_data, result)
        
        # Apply custom validation rules
        for rule_name, rule_func in self.validation_rules.items():
            try:
                rule_result = rule_func(config_data)
                if not rule_result:
                    result.add_error(f"Custom validation rule failed: {rule_name}")
            except Exception as e:
                result.add_warning(f"Custom validation rule error: {rule_name} - {e}")
        
        result.is_valid = len(result.errors) == 0
        self.validation_history.append(result)
        
        return result
    
    def get_validator_name(self) -> str:
        """Get validator name."""
        return self.name
    
    def _apply_basic_validation(self, config_data: Any, result: ConfigValidationResult) -> None:
        """Apply basic validation rules."""
        if config_data is None:
            result.add_error("Configuration data is None")
            return
        
        if isinstance(config_data, dict):
            if not config_data:
                result.add_warning("Configuration data is empty")
        elif isinstance(config_data, list):
            if not config_data:
                result.add_warning("Configuration data is empty list")
    
    def _apply_strict_validation(self, config_data: Any, result: ConfigValidationResult) -> None:
        """Apply strict validation rules."""
        self._apply_basic_validation(config_data, result)
        
        if isinstance(config_data, dict):
            # Check for required keys
            required_keys = ['version', 'name']
            for key in required_keys:
                if key not in config_data:
                    result.add_warning(f"Missing recommended key: {key}")
    
    def _apply_comprehensive_validation(self, config_data: Any, result: ConfigValidationResult) -> None:
        """Apply comprehensive validation rules."""
        self._apply_strict_validation(config_data, result)
        
        if isinstance(config_data, dict):
            # Deep validation of nested structures
            for key, value in config_data.items():
                if isinstance(value, dict):
                    nested_result = self.validate(value, ConfigValidationLevel.STRICT)
                    if not nested_result.is_valid:
                        result.errors.extend([f"{key}.{error}" for error in nested_result.errors])
                        result.warnings.extend([f"{key}.{warning}" for warning in nested_result.warnings])
    
    def get_validation_history(self) -> List[ConfigValidationResult]:
        """Get validation history."""
        return self.validation_history.copy()


class UnifiedConfigurationFramework:
    """Unified configuration framework for all configuration implementations."""
    
    def __init__(self):
        """Initialize unified configuration framework."""
        self.managers: Dict[str, IConfigurationManager] = {}
        self.loaders: Dict[ConfigFormat, IConfigurationLoader] = {}
        self.validators: Dict[str, IConfigurationValidator] = {}
        self.framework_stats = {
            'total_managers': 0,
            'total_loaders': 0,
            'total_validators': 0,
            'configs_loaded': 0,
            'configs_saved': 0,
            'validations_performed': 0
        }
    
    def register_manager(self, manager: IConfigurationManager) -> None:
        """Register configuration manager in framework."""
        name = manager.get_manager_name()
        self.managers[name] = manager
        self.framework_stats['total_managers'] += 1
    
    def register_loader(self, loader: IConfigurationLoader) -> None:
        """Register configuration loader in framework."""
        for format_type in loader.get_supported_formats():
            self.loaders[format_type] = loader
        self.framework_stats['total_loaders'] += 1
    
    def register_validator(self, validator: IConfigurationValidator) -> None:
        """Register configuration validator in framework."""
        name = validator.get_validator_name()
        self.validators[name] = validator
        self.framework_stats['total_validators'] += 1
    
    def get_manager(self, manager_name: str) -> Optional[IConfigurationManager]:
        """Get configuration manager by name."""
        return self.managers.get(manager_name)
    
    def get_loader(self, format_type: ConfigFormat) -> Optional[IConfigurationLoader]:
        """Get configuration loader by format."""
        return self.loaders.get(format_type)
    
    def get_validator(self, validator_name: str) -> Optional[IConfigurationValidator]:
        """Get configuration validator by name."""
        return self.validators.get(validator_name)
    
    def load_config_with_manager(self, manager_name: str, config_path: str, config_type: ConfigType) -> ConfigurationResult:
        """Load configuration using specific manager."""
        manager = self.get_manager(manager_name)
        if not manager:
            result = ConfigurationResult(success=False)
            result.add_error(f"Manager '{manager_name}' not found")
            return result
        
        result = manager.load_config(config_path, config_type)
        if result.success:
            self.framework_stats['configs_loaded'] += 1
        return result
    
    def save_config_with_manager(self, manager_name: str, config_path: str, config_data: Any) -> ConfigurationResult:
        """Save configuration using specific manager."""
        manager = self.get_manager(manager_name)
        if not manager:
            result = ConfigurationResult(success=False)
            result.add_error(f"Manager '{manager_name}' not found")
            return result
        
        result = manager.save_config(config_path, config_data)
        if result.success:
            self.framework_stats['configs_saved'] += 1
        return result
    
    def validate_config(self, validator_name: str, config_data: Any, validation_level: ConfigValidationLevel) -> ConfigValidationResult:
        """Validate configuration using specific validator."""
        validator = self.get_validator(validator_name)
        if not validator:
            result = ConfigValidationResult(is_valid=False)
            result.add_error(f"Validator '{validator_name}' not found")
            return result
        
        result = validator.validate(config_data, validation_level)
        self.framework_stats['validations_performed'] += 1
        return result
    
    def get_framework_stats(self) -> Dict[str, Any]:
        """Get framework statistics."""
        return self.framework_stats.copy()
    
    def list_managers(self) -> List[str]:
        """List all registered managers."""
        return list(self.managers.keys())
    
    def list_loaders(self) -> List[ConfigFormat]:
        """List all registered loaders."""
        return list(self.loaders.keys())
    
    def list_validators(self) -> List[str]:
        """List all registered validators."""
        return list(self.validators.keys())


class ConfigurationFactory:
    """Factory for creating configuration components."""
    
    @staticmethod
    def create_manager(name: str, loaders: Optional[Dict[ConfigFormat, IConfigurationLoader]] = None, validators: Optional[List[IConfigurationValidator]] = None) -> BaseConfigurationManager:
        """Create new configuration manager."""
        return BaseConfigurationManager(name, loaders, validators)
    
    @staticmethod
    def create_loader(name: str, supported_formats: List[ConfigFormat]) -> BaseConfigurationLoader:
        """Create new configuration loader."""
        return BaseConfigurationLoader(name, supported_formats)
    
    @staticmethod
    def create_validator(name: str, validation_rules: Optional[Dict[str, Callable]] = None) -> BaseConfigurationValidator:
        """Create new configuration validator."""
        return BaseConfigurationValidator(name, validation_rules)
    
    @staticmethod
    def create_json_loader(name: str = "JSONLoader") -> BaseConfigurationLoader:
        """Create JSON configuration loader."""
        return BaseConfigurationLoader(name, [ConfigFormat.JSON])
    
    @staticmethod
    def create_yaml_loader(name: str = "YAMLLoader") -> BaseConfigurationLoader:
        """Create YAML configuration loader."""
        return BaseConfigurationLoader(name, [ConfigFormat.YAML])
    
    @staticmethod
    def create_multi_format_loader(name: str = "MultiFormatLoader") -> BaseConfigurationLoader:
        """Create multi-format configuration loader."""
        return BaseConfigurationLoader(name, [ConfigFormat.JSON, ConfigFormat.YAML, ConfigFormat.INI])


# Global framework instance
unified_config_framework = UnifiedConfigurationFramework()


def get_unified_config_framework() -> UnifiedConfigurationFramework:
    """Get global unified configuration framework."""
    return unified_config_framework


# Example usage and migration helpers
def migrate_existing_config_manager(old_manager: Any, new_name: str) -> BaseConfigurationManager:
    """Migrate existing configuration manager to unified framework."""
    # This is a placeholder for actual migration logic
    # In practice, you would analyze the old manager and create a compatible one
    return BaseConfigurationManager(new_name)


def create_consolidated_config_manager(manager_names: List[str], consolidated_name: str) -> BaseConfigurationManager:
    """Create consolidated configuration manager from multiple existing managers."""
    # This is a placeholder for actual consolidation logic
    # In practice, you would merge configuration logic from multiple managers
    return BaseConfigurationManager(consolidated_name)


if __name__ == "__main__":
    # Example usage
    print("🚀 Unified Configuration Framework - Agent-2 Consolidation Implementation")
    print("=" * 80)
    
    # Create example components
    json_loader = ConfigurationFactory.create_json_loader()
    yaml_loader = ConfigurationFactory.create_yaml_loader()
    validator = ConfigurationFactory.create_validator("BasicValidator")
    
    # Create manager with loaders
    loaders = {ConfigFormat.JSON: json_loader, ConfigFormat.YAML: yaml_loader}
    manager = ConfigurationFactory.create_manager("ExampleManager", loaders, [validator])
    
    # Register in framework
    unified_config_framework.register_loader(json_loader)
    unified_config_framework.register_loader(yaml_loader)
    unified_config_framework.register_validator(validator)
    unified_config_framework.register_manager(manager)
    
    print(f"Framework stats: {unified_config_framework.get_framework_stats()}")
    print("✅ Unified Configuration Framework ready for consolidation!")
