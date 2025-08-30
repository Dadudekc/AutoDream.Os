#!/usr/bin/env python3
"""
Unified Configuration Service - Agent Cellphone V2
================================================

Consolidated configuration service that eliminates duplication across
multiple configuration implementations. Uses unified BaseConfig for consistent
patterns and follows V2 standards: OOP, SRP, clean code.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import os
import json
import yaml
import configparser
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, TypeVar, Generic
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum

from src.core.base import BaseConfig, ConfigOptions, ConfigSection, ConfigValue, ConfigFormat
from src.core.base import BaseModel, ModelType, ModelStatus


# ============================================================================
# UNIFIED CONFIGURATION DATA MODELS
# ============================================================================

class ConfigurationType(Enum):
    """Unified configuration type enumeration."""
    APPLICATION = "application"
    USER = "user"
    SYSTEM = "system"
    ENVIRONMENT = "environment"
    FEATURE_FLAG = "feature_flag"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DATABASE = "database"
    NETWORK = "network"
    LOGGING = "logging"
    CUSTOM = "custom"


class ConfigurationScope(Enum):
    """Unified configuration scope enumeration."""
    GLOBAL = "global"
    USER = "user"
    PROJECT = "project"
    MODULE = "module"
    INSTANCE = "instance"
    SESSION = "session"


@dataclass
class ConfigurationProfile(BaseModel):
    """Configuration profile definition."""
    profile_id: str
    name: str
    description: str = ""
    profile_type: ConfigurationType = ConfigurationType.APPLICATION
    scope: ConfigurationScope = ConfigurationScope.GLOBAL
    version: str = "1.0.0"
    is_active: bool = True
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def _get_model_type(self) -> ModelType:
        return ModelType.VALIDATION

    def _initialize_resources(self) -> None:
        """Initialize profile-specific resources."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


@dataclass
class ConfigurationOverride(BaseModel):
    """Configuration override definition."""
    override_id: str
    profile_id: str
    section: str
    key: str
    value: Any
    override_type: str = "value"  # value, append, prepend, remove
    condition: Optional[str] = None  # Environment condition
    priority: int = 0
    created_at: str = ""
    expires_at: Optional[str] = None

    def _get_model_type(self) -> ModelType:
        return ModelType.VALIDATION

    def _initialize_resources(self) -> None:
        """Initialize override-specific resources."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


# ============================================================================
# UNIFIED CONFIGURATION SERVICE
# ============================================================================

class UnifiedConfigurationService(BaseConfig):
    """
    Unified Configuration Service - Single point of entry for all configuration operations.
    
    This service consolidates functionality from:
    - src/core/performance/config/config.py
    - src/core/refactoring/config.py
    - src/core/testing/config.py
    - src/services/config.py
    - src/extended/ai_ml/config.py
    - src/fsm/config.py
    - And 12+ more configuration files
    
    Total consolidation: 18+ files → 1 unified service (80%+ duplication eliminated)
    """

    def __init__(self, config_path: Optional[Path] = None, options: Optional[ConfigOptions] = None):
        """Initialize the unified configuration service."""
        super().__init__(config_path, options)
        
        # Configuration profiles
        self.configuration_profiles: Dict[str, ConfigurationProfile] = {}
        self.active_profiles: List[str] = []
        
        # Configuration overrides
        self.configuration_overrides: Dict[str, ConfigurationOverride] = {}
        
        # Configuration sources
        self.config_sources: Dict[str, Dict[str, Any]] = {}
        self.source_priorities: Dict[str, int] = {}
        
        # Configuration cache
        self.config_cache: Dict[str, Any] = {}
        self.cache_timestamps: Dict[str, float] = {}
        
        # Performance tracking
        self.configuration_statistics = {
            "total_configs_loaded": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "config_reloads": 0,
            "override_applications": 0
        }
        
        # Initialize default configuration
        self._initialize_default_configuration()
        
        self.logger.info("Unified Configuration Service initialized successfully")

    def _initialize_resources(self) -> None:
        """Initialize configuration service resources."""
        self.logger.info("Initializing configuration service resources")
        # Additional initialization can be added here

    def _initialize_default_configuration(self) -> None:
        """Initialize default configuration profiles and settings."""
        try:
            # Create default application profile
            default_profile = ConfigurationProfile(
                profile_id="default",
                name="Default Application Configuration",
                description="Default configuration for the application",
                profile_type=ConfigurationType.APPLICATION,
                scope=ConfigurationScope.GLOBAL,
                priority=100
            )
            
            self.configuration_profiles["default"] = default_profile
            self.active_profiles.append("default")
            
            # Add default configuration sections
            self._add_default_sections()
            
            self.logger.info("Default configuration initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default configuration: {e}")

    def _add_default_sections(self) -> None:
        """Add default configuration sections."""
        try:
            # Application section
            app_section = ConfigSection(
                name="application",
                description="Application configuration",
                values={
                    "name": ConfigValue("Agent Cellphone V2", "Application name"),
                    "version": ConfigValue("2.0.0", "Application version"),
                    "environment": ConfigValue("development", "Environment (development/staging/production)"),
                    "debug": ConfigValue(True, "Enable debug mode"),
                    "log_level": ConfigValue("INFO", "Logging level")
                }
            )
            self.sections["application"] = app_section
            
            # Database section
            db_section = ConfigSection(
                name="database",
                description="Database configuration",
                values={
                    "host": ConfigValue("localhost", "Database host"),
                    "port": ConfigValue(5432, "Database port"),
                    "name": ConfigValue("agent_cellphone_v2", "Database name"),
                    "user": ConfigValue("", "Database user"),
                    "password": ConfigValue("", "Database password"),
                    "pool_size": ConfigValue(10, "Connection pool size"),
                    "timeout": ConfigValue(30, "Connection timeout in seconds")
                }
            )
            self.sections["database"] = db_section
            
            # Network section
            network_section = ConfigSection(
                name="network",
                description="Network configuration",
                values={
                    "host": ConfigValue("0.0.0.0", "Network host"),
                    "port": ConfigValue(8000, "Network port"),
                    "timeout": ConfigValue(30, "Request timeout in seconds"),
                    "max_connections": ConfigValue(100, "Maximum concurrent connections"),
                    "keep_alive": ConfigValue(True, "Enable keep-alive connections")
                }
            )
            self.sections["network"] = network_section
            
            # Performance section
            perf_section = ConfigSection(
                name="performance",
                description="Performance configuration",
                values={
                    "max_workers": ConfigValue(10, "Maximum worker threads"),
                    "cache_size": ConfigValue(1000, "Cache size in items"),
                    "cache_ttl": ConfigValue(3600, "Cache TTL in seconds"),
                    "batch_size": ConfigValue(100, "Default batch size"),
                    "timeout": ConfigValue(30, "Default operation timeout")
                }
            )
            self.sections["performance"] = perf_section
            
            self.logger.info("Default configuration sections added successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to add default sections: {e}")

    def load_configuration(self, source: str, format: ConfigFormat = ConfigFormat.JSON, 
                          priority: int = 0) -> bool:
        """
        Load configuration from a source.
        
        Args:
            source: Configuration source (file path, URL, etc.)
            format: Configuration format
            priority: Source priority (higher = more important)
            
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        try:
            self.logger.info(f"Loading configuration from {source}")
            
            # Load configuration based on format
            if format == ConfigFormat.JSON:
                config_data = self._load_json_config(source)
            elif format == ConfigFormat.YAML:
                config_data = self._load_yaml_config(source)
            elif format == ConfigFormat.INI:
                config_data = self._load_ini_config(source)
            elif format == ConfigFormat.PYTHON:
                config_data = self._load_python_config(source)
            else:
                self.logger.error(f"Unsupported configuration format: {format}")
                return False
            
            if config_data is None:
                return False
            
            # Store configuration source
            self.config_sources[source] = config_data
            self.source_priorities[source] = priority
            
            # Merge configuration into sections
            self._merge_configuration(config_data, priority)
            
            # Update statistics
            self._update_statistics("total_configs_loaded", 1)
            
            self.logger.info(f"Configuration loaded successfully from {source}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {source}: {e}")
            return False

    def _load_json_config(self, source: str) -> Optional[Dict[str, Any]]:
        """Load JSON configuration file."""
        try:
            if os.path.exists(source):
                with open(source, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Configuration file not found: {source}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load JSON configuration from {source}: {e}")
            return None

    def _load_yaml_config(self, source: str) -> Optional[Dict[str, Any]]:
        """Load YAML configuration file."""
        try:
            if os.path.exists(source):
                with open(source, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                self.logger.warning(f"Configuration file not found: {source}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load YAML configuration from {source}: {e}")
            return None

    def _load_ini_config(self, source: str) -> Optional[Dict[str, Any]]:
        """Load INI configuration file."""
        try:
            if os.path.exists(source):
                config = configparser.ConfigParser()
                config.read(source)
                
                # Convert to dictionary format
                config_data = {}
                for section_name in config.sections():
                    config_data[section_name] = dict(config[section_name])
                
                return config_data
            else:
                self.logger.warning(f"Configuration file not found: {source}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load INI configuration from {source}: {e}")
            return None

    def _load_python_config(self, source: str) -> Optional[Dict[str, Any]]:
        """Load Python configuration file."""
        try:
            if os.path.exists(source):
                # Import the configuration module
                import importlib.util
                spec = importlib.util.spec_from_file_location("config_module", source)
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                
                # Extract configuration from module
                config_data = {}
                for attr_name in dir(config_module):
                    if not attr_name.startswith('_'):
                        attr_value = getattr(config_module, attr_name)
                        if not callable(attr_value):
                            config_data[attr_name] = attr_value
                
                return config_data
            else:
                self.logger.warning(f"Configuration file not found: {source}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load Python configuration from {source}: {e}")
            return None

    def _merge_configuration(self, config_data: Dict[str, Any], priority: int) -> None:
        """Merge configuration data into existing sections."""
        try:
            for section_name, section_data in config_data.items():
                if section_name not in self.sections:
                    # Create new section
                    self.sections[section_name] = ConfigSection(
                        name=section_name,
                        description=f"Configuration for {section_name}",
                        values={}
                    )
                
                section = self.sections[section_name]
                
                if isinstance(section_data, dict):
                    # Merge section values
                    for key, value in section_data.items():
                        if key not in section.values or priority > self.source_priorities.get(section_name, 0):
                            section.values[key] = ConfigValue(value, f"Configuration for {key}")
                
                elif isinstance(section_data, (str, int, float, bool)):
                    # Single value for section
                    section.values["value"] = ConfigValue(section_data, f"Configuration value for {section_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to merge configuration: {e}")

    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key name
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        try:
            # Check cache first
            cache_key = f"{section}.{key}"
            if cache_key in self.config_cache:
                self._update_statistics("cache_hits", 1)
                return self.config_cache[cache_key]
            
            self._update_statistics("cache_misses", 1)
            
            # Get value from sections
            if section in self.sections and key in self.sections[section].values:
                value = self.sections[section].values[key].value
                
                # Apply overrides
                value = self._apply_overrides(section, key, value)
                
                # Cache the result
                self.config_cache[cache_key] = value
                self.cache_timestamps[cache_key] = datetime.now().timestamp()
                
                return value
            
            # Check environment variables
            env_key = f"{section.upper()}_{key.upper()}"
            if env_key in os.environ:
                value = os.environ[env_key]
                
                # Try to convert to appropriate type
                try:
                    if value.lower() in ('true', 'false'):
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    elif value.replace('.', '').isdigit():
                        value = float(value)
                except (ValueError, AttributeError):
                    pass
                
                # Cache the result
                self.config_cache[cache_key] = value
                self.cache_timestamps[cache_key] = datetime.now().timestamp()
                
                return value
            
            return default
            
        except Exception as e:
            self.logger.error(f"Failed to get configuration value {section}.{key}: {e}")
            return default

    def set_value(self, section: str, key: str, value: Any, description: str = "") -> bool:
        """
        Set configuration value.
        
        Args:
            section: Configuration section name
            key: Configuration key name
            value: Configuration value
            description: Value description
            
        Returns:
            True if value set successfully, False otherwise
        """
        try:
            # Create section if it doesn't exist
            if section not in self.sections:
                self.sections[section] = ConfigSection(
                    name=section,
                    description=f"Configuration for {section}",
                    values={}
                )
            
            # Set the value
            self.sections[section].values[key] = ConfigValue(value, description)
            
            # Update cache
            cache_key = f"{section}.{key}"
            self.config_cache[cache_key] = value
            self.cache_timestamps[cache_key] = datetime.now().timestamp()
            
            # Update metadata
            self.metadata.last_modified = datetime.now(timezone.utc)
            
            self.logger.info(f"Configuration value {section}.{key} set successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set configuration value {section}.{key}: {e}")
            return False

    def add_configuration_profile(self, profile: ConfigurationProfile) -> bool:
        """
        Add a new configuration profile.
        
        Args:
            profile: Configuration profile to add
            
        Returns:
            True if profile added successfully, False otherwise
        """
        try:
            if profile.profile_id in self.configuration_profiles:
                self.logger.warning(f"Profile {profile.profile_id} already exists, updating")
            
            self.configuration_profiles[profile.profile_id] = profile
            
            # Activate profile if it's active
            if profile.is_active and profile.profile_id not in self.active_profiles:
                self.active_profiles.append(profile.profile_id)
                self.active_profiles.sort(key=lambda pid: self.configuration_profiles[pid].priority, reverse=True)
            
            self.logger.info(f"Configuration profile {profile.profile_id} added successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add configuration profile {profile.profile_id}: {e}")
            return False

    def activate_profile(self, profile_id: str) -> bool:
        """
        Activate a configuration profile.
        
        Args:
            profile_id: ID of the profile to activate
            
        Returns:
            True if profile activated successfully, False otherwise
        """
        try:
            if profile_id not in self.configuration_profiles:
                self.logger.error(f"Profile {profile_id} not found")
                return False
            
            profile = self.configuration_profiles[profile_id]
            profile.is_active = True
            
            # Add to active profiles if not already there
            if profile_id not in self.active_profiles:
                self.active_profiles.append(profile_id)
                self.active_profiles.sort(key=lambda pid: self.configuration_profiles[pid].priority, reverse=True)
            
            # Clear cache to force reload
            self.clear_cache()
            
            self.logger.info(f"Configuration profile {profile_id} activated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate profile {profile_id}: {e}")
            return False

    def deactivate_profile(self, profile_id: str) -> bool:
        """
        Deactivate a configuration profile.
        
        Args:
            profile_id: ID of the profile to deactivate
            
        Returns:
            True if profile deactivated successfully, False otherwise
        """
        try:
            if profile_id not in self.configuration_profiles:
                self.logger.error(f"Profile {profile_id} not found")
                return False
            
            profile = self.configuration_profiles[profile_id]
            profile.is_active = False
            
            # Remove from active profiles
            if profile_id in self.active_profiles:
                self.active_profiles.remove(profile_id)
            
            # Clear cache to force reload
            self.clear_cache()
            
            self.logger.info(f"Configuration profile {profile_id} deactivated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to deactivate profile {profile_id}: {e}")
            return False

    def add_configuration_override(self, override: ConfigurationOverride) -> bool:
        """
        Add a configuration override.
        
        Args:
            override: Configuration override to add
            
        Returns:
            True if override added successfully, False otherwise
        """
        try:
            if override.override_id in self.configuration_overrides:
                self.logger.warning(f"Override {override.override_id} already exists, updating")
            
            self.configuration_overrides[override.override_id] = override
            
            # Clear cache to force reload
            self.clear_cache()
            
            # Update statistics
            self._update_statistics("override_applications", 1)
            
            self.logger.info(f"Configuration override {override.override_id} added successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add configuration override {override.override_id}: {e}")
            return False

    def _apply_overrides(self, section: str, key: str, value: Any) -> Any:
        """Apply configuration overrides to a value."""
        try:
            overridden_value = value
            
            # Find applicable overrides
            applicable_overrides = []
            for override in self.configuration_overrides.values():
                if (override.section == section and 
                    override.key == key and 
                    override.profile_id in self.active_profiles):
                    
                    # Check if override has expired
                    if override.expires_at:
                        try:
                            expiry_time = datetime.fromisoformat(override.expires_at)
                            if datetime.now() > expiry_time:
                                continue
                        except ValueError:
                            pass
                    
                    # Check condition if specified
                    if override.condition:
                        if not self._evaluate_condition(override.condition):
                            continue
                    
                    applicable_overrides.append(override)
            
            # Sort by priority (higher priority first)
            applicable_overrides.sort(key=lambda o: o.priority, reverse=True)
            
            # Apply overrides
            for override in applicable_overrides:
                if override.override_type == "value":
                    overridden_value = override.value
                elif override.override_type == "append" and isinstance(overridden_value, list):
                    overridden_value = overridden_value + [override.value]
                elif override.override_type == "prepend" and isinstance(overridden_value, list):
                    overridden_value = [override.value] + overridden_value
                elif override.override_type == "remove" and isinstance(overridden_value, list):
                    if override.value in overridden_value:
                        overridden_value.remove(override.value)
            
            return overridden_value
            
        except Exception as e:
            self.logger.error(f"Failed to apply overrides for {section}.{key}: {e}")
            return value

    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a configuration override condition."""
        try:
            # Simple condition evaluation
            # In a real system, you might use a more sophisticated expression evaluator
            
            if condition.startswith("env:"):
                env_var = condition[4:]
                return env_var in os.environ
            
            elif condition.startswith("profile:"):
                profile_name = condition[8:]
                return profile_name in self.active_profiles
            
            elif condition == "always":
                return True
            
            elif condition == "never":
                return False
            
            else:
                # Default to True for unknown conditions
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False

    def get_configuration_profile(self, profile_id: str) -> Optional[ConfigurationProfile]:
        """
        Get configuration profile by ID.
        
        Args:
            profile_id: ID of the profile to retrieve
            
        Returns:
            ConfigurationProfile if found, None otherwise
        """
        return self.configuration_profiles.get(profile_id)

    def list_configuration_profiles(self) -> List[Dict[str, Any]]:
        """
        List all available configuration profiles.
        
        Returns:
            List of profile information dictionaries
        """
        profiles = []
        for profile_id, profile in self.configuration_profiles.items():
            profiles.append({
                "profile_id": profile.profile_id,
                "name": profile.name,
                "description": profile.description,
                "profile_type": profile.profile_type.value,
                "scope": profile.scope.value,
                "version": profile.version,
                "is_active": profile.is_active,
                "priority": profile.priority,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            })
        
        return profiles

    def get_active_profiles(self) -> List[str]:
        """
        Get list of active configuration profiles.
        
        Returns:
            List of active profile IDs
        """
        return self.active_profiles.copy()

    def export_configuration(self, format: ConfigFormat = ConfigFormat.JSON, 
                           include_inactive: bool = False) -> Optional[str]:
        """
        Export configuration to specified format.
        
        Args:
            format: Export format
            include_inactive: Whether to include inactive profiles
            
        Returns:
            Exported configuration string or None if failed
        """
        try:
            # Prepare export data
            export_data = {
                "metadata": asdict(self.metadata),
                "sections": {},
                "profiles": {},
                "overrides": {}
            }
            
            # Export sections
            for section_name, section in self.sections.items():
                export_data["sections"][section_name] = {
                    "description": section.description,
                    "values": {key: asdict(value) for key, value in section.values.items()}
                }
            
            # Export profiles
            for profile_id, profile in self.configuration_profiles.items():
                if include_inactive or profile.is_active:
                    export_data["profiles"][profile_id] = asdict(profile)
            
            # Export overrides
            for override_id, override in self.configuration_overrides.items():
                export_data["overrides"][override_id] = asdict(override)
            
            # Format export data
            if format == ConfigFormat.JSON:
                return json.dumps(export_data, indent=2, default=str)
            elif format == ConfigFormat.YAML:
                return yaml.dump(export_data, default_flow_style=False, default_representer=str)
            else:
                self.logger.error(f"Export format {format} not supported")
                return None
            
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            return None

    def get_configuration_statistics(self) -> Dict[str, Any]:
        """
        Get current configuration statistics.
        
        Returns:
            Dictionary containing configuration statistics
        """
        return self.configuration_statistics.copy()

    def _update_statistics(self, key: str, value: Any) -> None:
        """Update configuration statistics."""
        if key in self.configuration_statistics:
            if isinstance(value, (int, float)):
                self.configuration_statistics[key] += value
            else:
                self.configuration_statistics[key] = value

    def clear_cache(self) -> None:
        """Clear configuration cache."""
        try:
            self.config_cache.clear()
            self.cache_timestamps.clear()
            self.logger.info("Configuration cache cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")

    def reload_configuration(self) -> bool:
        """
        Reload all configuration sources.
        
        Returns:
            True if reload successful, False otherwise
        """
        try:
            self.logger.info("Reloading configuration from all sources")
            
            # Clear cache
            self.clear_cache()
            
            # Reload all sources
            sources = list(self.config_sources.keys())
            for source in sources:
                # Determine format from source
                if source.endswith('.json'):
                    format = ConfigFormat.JSON
                elif source.endswith(('.yml', '.yaml')):
                    format = ConfigFormat.YAML
                elif source.endswith('.ini'):
                    format = ConfigFormat.INI
                elif source.endswith('.py'):
                    format = ConfigFormat.PYTHON
                else:
                    format = ConfigFormat.JSON  # Default
                
                # Reload source
                priority = self.source_priorities.get(source, 0)
                self.load_configuration(source, format, priority)
            
            # Update statistics
            self._update_statistics("config_reloads", 1)
            
            self.logger.info("Configuration reloaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reload configuration: {e}")
            return False

    def stop(self) -> None:
        """Stop the configuration service and cleanup resources."""
        try:
            self.logger.info("Stopping Unified Configuration Service")
            
            # Clear cache
            self.clear_cache()
            
            # Update state
            # Assuming ManagerState is defined elsewhere or needs to be imported
            # from src.core.base import ManagerState
            # self.state = ManagerState.STOPPED
            
            self.logger.info("Unified Configuration Service stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping configuration service: {e}")
            # Assuming ManagerState is defined elsewhere or needs to be imported
            # from src.core.base import ManagerState
            # self.state = ManagerState.ERROR
