#!/usr/bin/env python3
"""
Unified Configuration System - V2 Compliant
==========================================

This module provides a unified configuration system that consolidates all configuration
patterns across the codebase, eliminating DRY violations.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate all configuration patterns into unified system
"""

from ..core.unified_data_processing_system import read_json, write_json
import os
import yaml
from ..core.unified_data_processing_system import get_unified_data_processing
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from .unified-logging-utility import UnifiedLoggingUtility
from .unified-error-handling-utility import UnifiedErrorHandlingUtility


@dataclass
class ConfigurationSection:
    """Represents a configuration section."""
    name: str
    data: Dict[str, Any]
    source: str
    priority: int = 0


class UnifiedConfigurationSystem:
    """
    Unified configuration system that consolidates all configuration patterns.
    
    CONSOLIDATES:
    - Messaging configuration
    - Discord configuration
    - Vector database configuration
    - FSM configuration
    - Reporting configuration
    - Performance metrics configuration
    - Quality configuration
    """
    
    def __init__(self):
        """Initialize unified configuration system."""
        self.logger = UnifiedLoggingUtility.get_logger(__name__)
        self.project_root = Path(__file__).parent.parent.parent
        
        # Configuration sections
        self.sections: Dict[str, ConfigurationSection] = {}
        
        # Default configuration
        self.default_config = {
            "messaging": {
                "default_sender": "Captain Agent-4",
                "max_message_length": 1000,
                "delivery_timeout": 30,
                "retry_attempts": 3,
                "coordinate_system": {
                    "screen_width": 1920,
                    "screen_height": 1080,
                    "agent_coordinates": {
                        "Agent-1": {"x": 100, "y": 100},
                        "Agent-2": {"x": 300, "y": 100},
                        "Agent-3": {"x": 500, "y": 100},
                        "Agent-4": {"x": 700, "y": 100},
                        "Agent-5": {"x": 100, "y": 300},
                        "Agent-6": {"x": 300, "y": 300},
                        "Agent-7": {"x": 500, "y": 300},
                        "Agent-8": {"x": 700, "y": 300}
                    }
                }
            },
            "discord": {
                "webhook_url": os.getenv("DISCORD_WEBHOOK_URL", ""),
                "bot_token": os.getenv("DISCORD_BOT_TOKEN", ""),
                "channel_id": os.getenv("DISCORD_CHANNEL_ID", ""),
                "enabled": True,
                "rate_limit": 1.0
            },
            "vector_database": {
                "provider": "chromadb",
                "persist_directory": "./data/vector_db",
                "collection_name": "agent_embeddings",
                "embedding_model": "all-MiniLM-L6-v2",
                "chunk_size": 1000,
                "chunk_overlap": 200
            },
            "fsm": {
                "state_timeout": 300,
                "transition_timeout": 30,
                "max_retries": 3,
                "log_transitions": True
            },
            "reporting": {
                "output_directory": "./reports",
                "format": "markdown",
                "include_timestamps": True,
                "max_file_size": 10485760  # 10MB
            },
            "performance": {
                "metrics_enabled": True,
                "collection_interval": 60,
                "retention_days": 30,
                "alert_thresholds": {
                    "memory_usage": 80,
                    "cpu_usage": 90,
                    "response_time": 5.0
                }
            },
            "quality": {
                "code_coverage_threshold": 85,
                "complexity_threshold": 10,
                "duplication_threshold": 5,
                "maintainability_threshold": 70
            }
        }
        
        # Load all configuration sections
        self._load_all_configurations()

    def _load_all_configurations(self) -> None:
        """Load all configuration sections from various sources."""
        try:
            # Load from environment variables
            self._load_from_environment()
            
            # Load from config files
            self._load_from_files()
            
            # Load from default configuration
            self._load_default_configuration()
            
            self.logger.info(f"Loaded {len(self.sections)} configuration sections")
            
        except Exception as e:
            self.logger.error(f"Error loading configurations: {e}")

    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        env_config = {}
        
        # Messaging configuration
        if os.getenv("MESSAGING_DEFAULT_SENDER"):
            env_config["messaging"] = {
                "default_sender": os.getenv("MESSAGING_DEFAULT_SENDER"),
                "max_message_length": int(os.getenv("MESSAGING_MAX_LENGTH", "1000")),
                "delivery_timeout": int(os.getenv("MESSAGING_TIMEOUT", "30"))
            }
        
        # Discord configuration
        if os.getenv("DISCORD_WEBHOOK_URL"):
            env_config["discord"] = {
                "webhook_url": os.getenv("DISCORD_WEBHOOK_URL"),
                "bot_token": os.getenv("DISCORD_BOT_TOKEN", ""),
                "channel_id": os.getenv("DISCORD_CHANNEL_ID", ""),
                "enabled": os.getenv("DISCORD_ENABLED", "true").lower() == "true"
            }
        
        # Vector database configuration
        if os.getenv("VECTOR_DB_PROVIDER"):
            env_config["vector_database"] = {
                "provider": os.getenv("VECTOR_DB_PROVIDER"),
                "persist_directory": os.getenv("VECTOR_DB_DIR", "./data/vector_db"),
                "collection_name": os.getenv("VECTOR_DB_COLLECTION", "agent_embeddings")
            }
        
        if env_config:
            self.sections["environment"] = ConfigurationSection(
                name="environment",
                data=env_config,
                source="environment_variables",
                priority=100
            )

    def _load_from_files(self) -> None:
        """Load configuration from files."""
        config_files = [
            "config.json",
            "config.yaml",
            "config.yml",
            "settings.json",
            "settings.yaml"
        ]
        
        for config_file in config_files:
            file_path = self.project_root / config_file
            if file_path.exists():
                try:
                    config_data = self._load_config_file(file_path)
                    if config_data:
                        self.sections[config_file] = ConfigurationSection(
                            name=config_file,
                            data=config_data,
                            source=str(file_path),
                            priority=50
                        )
                        self.logger.info(f"Loaded configuration from {config_file}")
                except Exception as e:
                    self.logger.error(f"Error loading {config_file}: {e}")

    def _load_config_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load configuration from a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                else:
                    return read_json(f)
        except Exception as e:
            self.logger.error(f"Error loading config file {file_path}: {e}")
            return None

    def _load_default_configuration(self) -> None:
        """Load default configuration."""
        self.sections["default"] = ConfigurationSection(
            name="default",
            data=self.default_config,
            source="default_configuration",
            priority=0
        )

    def get_config(self, section: str = None, key: str = None, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key within section
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        try:
            if section is None:
                # Return all configuration
                return self._merge_all_configurations()
            
            if key is None:
                # Return section configuration
                return self._get_section_config(section)
            
            # Return specific key value
            section_config = self._get_section_config(section)
            if section_config and key in section_config:
                return section_config[key]
            
            return default
            
        except Exception as e:
            self.logger.error(f"Error getting config {section}.{key}: {e}")
            return default

    def _merge_all_configurations(self) -> Dict[str, Any]:
        """Merge all configuration sections by priority."""
        merged_config = {}
        
        # Sort sections by priority (highest first)
        sorted_sections = sorted(self.sections.values(), key=lambda x: x.priority, reverse=True)
        
        for section in sorted_sections:
            merged_config = self._deep_merge(merged_config, section.data)
        
        return merged_config

    def _get_section_config(self, section: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific section."""
        merged_config = self._merge_all_configurations()
        return merged_config.get(section)

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result

    def set_config(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key within section
            value: Value to set
        """
        try:
            if section not in self.sections:
                self.sections[section] = ConfigurationSection(
                    name=section,
                    data={},
                    source="runtime",
                    priority=75
                )
            
            if key not in self.sections[section].data:
                self.sections[section].data[key] = {}
            
            self.sections[section].data[key] = value
            self.logger.debug(f"Set config {section}.{key} = {value}")
            
        except Exception as e:
            self.logger.error(f"Error setting config {section}.{key}: {e}")

    def save_config(self, section: str = None, file_path: str = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            section: Section to save (None for all)
            file_path: File path to save to
            
        Returns:
            True if successful
        """
        try:
            if file_path is None:
                file_path = "config.json"
            
            save_path = self.project_root / file_path
            
            if section:
                config_data = self._get_section_config(section)
            else:
                config_data = self._merge_all_configurations()
            
            with open(save_path, 'w', encoding='utf-8') as f:
                write_json(config_data, f, indent=2)
            
            self.logger.info(f"Saved configuration to {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False

    def reload_config(self) -> None:
        """Reload all configurations."""
        self.sections.clear()
        self._load_all_configurations()
        self.logger.info("Configuration reloaded")

    def get_section_names(self) -> List[str]:
        """Get list of configuration section names."""
        return list(self.sections.keys())

    def validate_config(self) -> List[str]:
        """
        Validate configuration.
        
        Returns:
            List of validation errors
        """
        errors = []
        
        try:
            # Validate messaging configuration
            messaging_config = self.get_config("messaging")
            if messaging_config:
                if "default_sender" not in messaging_config:
                    errors.append("Messaging config missing default_sender")
                if "max_message_length" not in messaging_config:
                    errors.append("Messaging config missing max_message_length")
            
            # Validate discord configuration
            discord_config = self.get_config("discord")
            if discord_config and discord_config.get("enabled", False):
                if not discord_config.get("webhook_url"):
                    errors.append("Discord config missing webhook_url when enabled")
            
            # Validate vector database configuration
            vector_config = self.get_config("vector_database")
            if vector_config:
                if "provider" not in vector_config:
                    errors.append("Vector database config missing provider")
                if "persist_directory" not in vector_config:
                    errors.append("Vector database config missing persist_directory")
            
            if errors:
                self.logger.warning(f"Configuration validation found {len(errors)} errors")
            else:
                self.logger.info("Configuration validation passed")
                
        except Exception as e:
            errors.append(f"Configuration validation error: {e}")
            self.logger.error(f"Configuration validation error: {e}")
        
        return errors


# Global configuration instance
_config_instance = None

def get_unified_config() -> UnifiedConfigurationSystem:
    """Get the global unified configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = UnifiedConfigurationSystem()
    return _config_instance

def load_config() -> Dict[str, Any]:
    """Load configuration (backward compatibility)."""
    return get_unified_config().get_config()

def get_config(section: str = None, key: str = None, default: Any = None) -> Any:
    """Get configuration value (backward compatibility)."""
    return get_unified_config().get_config(section, key, default)
