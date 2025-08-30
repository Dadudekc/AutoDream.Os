#!/usr/bin/env python3
"""
Config Manager - High-Level Configuration Management

This module provides high-level configuration management functionality for the
unified configuration system.

Agent: Agent-6 (Performance Optimization Manager)
Mission: SSOT Consolidation - Utility Systems
Status: IN PROGRESS - Phase 2: Configuration System Consolidation
"""

from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging

from .config_loader import ConfigLoader
from .config_validator import ConfigValidator
from .environment_manager import EnvironmentManager

logger = logging.getLogger(__name__)


class UnifiedConfigManager:
    """
    High-level configuration manager for the unified configuration system.
    
    This class provides high-level configuration management functionality,
    coordinating the various configuration components.
    """
    
    def __init__(self, config_path: str = "config/services/unified.yaml"):
        """
        Initialize the unified configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config_loader = ConfigLoader(config_path)
        self.config_validator = ConfigValidator()
        self.environment_manager = EnvironmentManager()
        
        # Configuration state
        self.config_data: Dict[str, Any] = {}
        self.loaded = False
        self.validated = False
    
    def load_and_validate_config(self) -> bool:
        """
        Load and validate configuration.
        
        Returns:
            True if configuration loaded and validated successfully, False otherwise
        """
        try:
            # Load configuration
            if not self.config_loader.load_config():
                logger.error("Failed to load configuration")
                return False
            
            # Get configuration data
            self.config_data = self.config_loader.get_config_data()
            
            # Apply environment overrides
            self.config_data = self.environment_manager.apply_environment_overrides(
                self.config_data
            )
            
            # Validate configuration
            validation_result = self.config_validator.validate_config(self.config_data)
            if validation_result.is_valid():
                self.validated = True
                logger.info("Configuration loaded and validated successfully")
            else:
                logger.warning(f"Configuration validation warnings: {validation_result.warnings}")
                if validation_result.errors:
                    logger.error(f"Configuration validation errors: {validation_result.errors}")
                    return False
            
            self.loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to load and validate configuration: {e}")
            return False
    
    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key_path: Dot notation path to configuration value
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if not self.loaded:
            if not self.load_and_validate_config():
                return default
        
        return self.config_loader.get_config_value(key_path, default)
    
    def set_config_value(self, key_path: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Args:
            key_path: Dot notation path to configuration value
            value: Value to set
            
        Returns:
            True if value set successfully, False otherwise
        """
        if not self.loaded:
            if not self.load_and_validate_config():
                return False
        
        return self.config_loader.set_config_value(key_path, value)
    
    def get_config_section(self, section_name: str) -> Dict[str, Any]:
        """
        Get a configuration section.
        
        Args:
            section_name: Name of configuration section
            
        Returns:
            Configuration section dictionary
        """
        if not self.loaded:
            if not self.load_and_validate_config():
                return {}
        
        return self.config_loader.get_config_section(section_name)
    
    def reload_config(self) -> bool:
        """
        Reload configuration.
        
        Returns:
            True if configuration reloaded successfully, False otherwise
        """
        self.loaded = False
        self.validated = False
        return self.load_and_validate_config()
    
    def save_config(self, output_path: Optional[str] = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            output_path: Output file path (uses config_path if not specified)
            
        Returns:
            True if configuration saved successfully, False otherwise
        """
        if not self.loaded:
            logger.error("No configuration loaded to save")
            return False
        
        return self.config_loader.save_config(output_path)
    
    def validate_config(self) -> Dict[str, Any]:
        """
        Validate current configuration.
        
        Returns:
            Validation result dictionary
        """
        if not self.loaded:
            return {'valid': False, 'errors': ['No configuration loaded']}
        
        validation_result = self.config_validator.validate_config(self.config_data)
        return {
            'valid': validation_result.is_valid(),
            'errors': validation_result.errors,
            'warnings': validation_result.warnings,
            'message': validation_result.message
        }
    
    def get_config_status(self) -> Dict[str, Any]:
        """
        Get comprehensive configuration status.
        
        Returns:
            Configuration status dictionary
        """
        return {
            'loaded': self.loaded,
            'validated': self.validated,
            'config_file': str(self.config_path),
            'sections': list(self.config_data.keys()) if self.loaded else [],
            'environment_overrides': self.environment_manager.get_override_summary(self.config_data),
            'validation': self.validate_config()
        }
    
    def list_config_sections(self) -> List[str]:
        """
        List available configuration sections.
        
        Returns:
            List of configuration section names
        """
        if not self.loaded:
            if not self.load_and_validate_config():
                return []
        return list(self.config_data.keys())
    
    def has_config_section(self, section_name: str) -> bool:
        """
        Check if configuration section exists.
        
        Args:
            section_name: Name of configuration section
            
        Returns:
            True if section exists, False otherwise
        """
        if not self.loaded:
            if not self.load_and_validate_config():
                return False
        return section_name in self.config_data
    
    def get_environment_summary(self) -> Dict[str, Any]:
        """
        Get summary of environment overrides.
        
        Returns:
            Environment override summary
        """
        return self.environment_manager.get_override_summary(self.config_data)
    
    def clear_config(self) -> None:
        """Clear loaded configuration data."""
        self.config_data.clear()
        self.loaded = False
        self.validated = False
        logger.info("Configuration data cleared")
    
    def is_loaded(self) -> bool:
        """
        Check if configuration is loaded.
        
        Returns:
            True if configuration is loaded, False otherwise
        """
        return self.loaded
    
    def is_validated(self) -> bool:
        """
        Check if configuration is validated.
        
        Returns:
            True if configuration is validated, False otherwise
        """
        return self.validated
