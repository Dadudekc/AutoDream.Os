#!/usr/bin/env python3
"""
Unified Configuration System - Eliminates Configuration Management Duplication

This module provides a unified configuration system that eliminates configuration
management duplication found across multiple files in the codebase, specifically
addressing the configuration management duplication identified in the duplicate logic analysis.

Agent: Agent-7 (Web Development Specialist)
Mission: Technical Debt Elimination - Configuration Management Consolidation
Status: CONSOLIDATED - Single Source of Truth for Configuration Management
"""

import os
import json
import yaml
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

# ================================
# CONFIGURATION TYPES
# ================================

class ConfigType(Enum):
    """Types of configuration sources."""
    ENVIRONMENT = "environment"
    FILE = "file"
    DICTIONARY = "dictionary"
    DEFAULT = "default"

@dataclass
class ConfigSource:
    """Configuration source definition."""
    name: str
    config_type: ConfigType
    source: Union[str, Dict[str, Any]]
    priority: int = 0
    required: bool = False

# ================================
# UNIFIED CONFIGURATION SYSTEM
# ================================

class UnifiedConfigurationSystem:
    """
    Unified configuration system that eliminates configuration management duplication.
    
    This system consolidates the common configuration patterns found across:
    - Multiple config files: src/config.py, src/settings.py, src/constants.py
    - Hardcoded agent configurations in messaging_core.py, messaging_pyautogui.py
    - Environment variable handling repeated across multiple files
    - Path resolution logic duplicated in config_core.py, paths.py
    
    CONSOLIDATED: Single source of truth for all configuration management.
    """
    
    def __init__(self, config_name: str = "unified_config"):
        self.config_name = config_name
        self.config_sources: List[ConfigSource] = []
        self.config_data: Dict[str, Any] = {}
        self.agent_configs: Dict[str, Dict[str, Any]] = {}
        self.environment_vars: Dict[str, str] = {}
        self.path_configs: Dict[str, str] = {}
        
        # Initialize default configurations
        self._initialize_default_configs()
    
    def _initialize_default_configs(self) -> None:
        """Initialize default configuration values."""
        # Default agent configurations
        self.agent_configs = {
            "Agent-1": {
                "coordinates": (-1269, 481),
                "role": "Integration & Core Systems Specialist",
                "points": 600
            },
            "Agent-2": {
                "coordinates": (-308, 480),
                "role": "Architecture & Design Specialist",
                "points": 550
            },
            "Agent-3": {
                "coordinates": (-1269, 1001),
                "role": "Infrastructure & DevOps Specialist",
                "points": 575
            },
            "Agent-4": {
                "coordinates": (-308, 1000),
                "role": "Captain (Strategic Oversight & Emergency Intervention)",
                "points": 0
            },
            "Agent-5": {
                "coordinates": (652, 421),
                "role": "Business Intelligence Specialist",
                "points": 425
            },
            "Agent-6": {
                "coordinates": (1612, 419),
                "role": "Coordination & Communication Specialist",
                "points": 500
            },
            "Agent-7": {
                "coordinates": (653, 940),
                "role": "Web Development Specialist",
                "points": 685
            },
            "Agent-8": {
                "coordinates": (1611, 941),
                "role": "SSOT & System Integration Specialist",
                "points": 650
            }
        }
        
        # Default path configurations
        self.path_configs = {
            "agent_workspaces": "agent_workspaces",
            "inbox": "inbox",
            "status_file": "status.json",
            "devlog_script": "scripts/devlog.py",
            "messaging_cli": "src/services/messaging_cli.py"
        }
        
        # Default environment variables
        self.environment_vars = {
            "PYTHONPATH": ".",
            "LOG_LEVEL": "INFO",
            "DEBUG_MODE": "false"
        }
    
    # ================================
    # CONFIGURATION SOURCE MANAGEMENT
    # ================================
    
    def add_config_source(self, source: ConfigSource) -> None:
        """Add a configuration source."""
        self.config_sources.append(source)
        # Sort by priority (higher priority first)
        self.config_sources.sort(key=lambda x: x.priority, reverse=True)
    
    def add_environment_config(self, name: str, env_var: str, default_value: Any = None, priority: int = 0) -> None:
        """Add environment variable configuration source."""
        source = ConfigSource(
            name=name,
            config_type=ConfigType.ENVIRONMENT,
            source=env_var,
            priority=priority
        )
        self.add_config_source(source)
    
    def add_file_config(self, name: str, file_path: str, priority: int = 0, required: bool = False) -> None:
        """Add file-based configuration source."""
        source = ConfigSource(
            name=name,
            config_type=ConfigType.FILE,
            source=file_path,
            priority=priority,
            required=required
        )
        self.add_config_source(source)
    
    def add_dict_config(self, name: str, config_dict: Dict[str, Any], priority: int = 0) -> None:
        """Add dictionary-based configuration source."""
        source = ConfigSource(
            name=name,
            config_type=ConfigType.DICTIONARY,
            source=config_dict,
            priority=priority
        )
        self.add_config_source(source)
    
    # ================================
    # CONFIGURATION LOADING
    # ================================
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from all sources."""
        self.config_data = {}
        
        for source in self.config_sources:
            try:
                if source.config_type == ConfigType.ENVIRONMENT:
                    self._load_environment_config(source)
                elif source.config_type == ConfigType.FILE:
                    self._load_file_config(source)
                elif source.config_type == ConfigType.DICTIONARY:
                    self._load_dict_config(source)
            except Exception as e:
                if source.required:
                    raise Exception(f"Failed to load required config source {source.name}: {str(e)}")
                else:
                    print(f"Warning: Failed to load config source {source.name}: {str(e)}")
        
        return self.config_data
    
    def _load_environment_config(self, source: ConfigSource) -> None:
        """Load configuration from environment variable."""
        env_var = source.source
        value = os.getenv(env_var)
        if value is not None:
            self.config_data[source.name] = value
        else:
            # Try to parse as JSON if it looks like structured data
            try:
                self.config_data[source.name] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                self.config_data[source.name] = value
    
    def _load_file_config(self, source: ConfigSource) -> None:
        """Load configuration from file."""
        file_path = source.source
        if not os.path.exists(file_path):
            if source.required:
                raise FileNotFoundError(f"Required config file not found: {file_path}")
            return
        
        file_extension = Path(file_path).suffix.lower()
        
        with open(file_path, 'r') as f:
            if file_extension in ['.json']:
                config_data = json.load(f)
            elif file_extension in ['.yaml', '.yml']:
                config_data = yaml.safe_load(f)
            else:
                # Try to parse as JSON first, then as plain text
                try:
                    f.seek(0)
                    config_data = json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    config_data = f.read()
            
            self.config_data[source.name] = config_data
    
    def _load_dict_config(self, source: ConfigSource) -> None:
        """Load configuration from dictionary."""
        self.config_data[source.name] = source.source
    
    # ================================
    # CONFIGURATION ACCESS
    # ================================
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self.config_data.get(key, default)
    
    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Get agent configuration."""
        return self.agent_configs.get(agent_id, {})
    
    def get_agent_coordinates(self, agent_id: str) -> tuple:
        """Get agent coordinates."""
        agent_config = self.get_agent_config(agent_id)
        return agent_config.get('coordinates', (0, 0))
    
    def get_agent_role(self, agent_id: str) -> str:
        """Get agent role."""
        agent_config = self.get_agent_config(agent_id)
        return agent_config.get('role', 'Unknown')
    
    def get_agent_points(self, agent_id: str) -> int:
        """Get agent points."""
        agent_config = self.get_agent_config(agent_id)
        return agent_config.get('points', 0)
    
    def get_path(self, path_name: str) -> str:
        """Get path configuration."""
        return self.path_configs.get(path_name, "")
    
    def get_environment_var(self, var_name: str) -> str:
        """Get environment variable."""
        return self.environment_vars.get(var_name, "")
    
    # ================================
    # CONFIGURATION UPDATES
    # ================================
    
    def update_config(self, key: str, value: Any) -> None:
        """Update configuration value."""
        self.config_data[key] = value
    
    def update_agent_config(self, agent_id: str, config_updates: Dict[str, Any]) -> None:
        """Update agent configuration."""
        if agent_id not in self.agent_configs:
            self.agent_configs[agent_id] = {}
        self.agent_configs[agent_id].update(config_updates)
    
    def update_path_config(self, path_name: str, path_value: str) -> None:
        """Update path configuration."""
        self.path_configs[path_name] = path_value
    
    def update_environment_var(self, var_name: str, var_value: str) -> None:
        """Update environment variable."""
        self.environment_vars[var_name] = var_value
    
    # ================================
    # CONFIGURATION VALIDATION
    # ================================
    
    def validate_configuration(self) -> Dict[str, List[str]]:
        """Validate configuration completeness and correctness."""
        validation_errors = {
            'missing_required': [],
            'invalid_values': [],
            'missing_agents': [],
            'invalid_paths': []
        }
        
        # Check for missing required configurations
        for source in self.config_sources:
            if source.required and source.name not in self.config_data:
                validation_errors['missing_required'].append(source.name)
        
        # Check agent configurations
        for agent_id in self.agent_configs:
            agent_config = self.agent_configs[agent_id]
            if 'coordinates' not in agent_config:
                validation_errors['missing_agents'].append(f"{agent_id}: missing coordinates")
            elif not isinstance(agent_config['coordinates'], tuple) or len(agent_config['coordinates']) != 2:
                validation_errors['invalid_values'].append(f"{agent_id}: invalid coordinates format")
        
        # Check path configurations
        for path_name, path_value in self.path_configs.items():
            if not path_value:
                validation_errors['invalid_paths'].append(f"{path_name}: empty path")
        
        return validation_errors
    
    # ================================
    # CONFIGURATION EXPORT
    # ================================
    
    def export_config(self, file_path: str, format_type: str = "json") -> None:
        """Export configuration to file."""
        export_data = {
            'config_data': self.config_data,
            'agent_configs': self.agent_configs,
            'path_configs': self.path_configs,
            'environment_vars': self.environment_vars
        }
        
        with open(file_path, 'w') as f:
            if format_type.lower() == 'json':
                json.dump(export_data, f, indent=2)
            elif format_type.lower() in ['yaml', 'yml']:
                yaml.dump(export_data, f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def get_all_agent_ids(self) -> List[str]:
        """Get all agent IDs."""
        return list(self.agent_configs.keys())
    
    def get_all_paths(self) -> Dict[str, str]:
        """Get all path configurations."""
        return self.path_configs.copy()
    
    def get_all_environment_vars(self) -> Dict[str, str]:
        """Get all environment variables."""
        return self.environment_vars.copy()
    
    def clear_configuration(self) -> None:
        """Clear all configuration data."""
        self.config_data.clear()
        self.config_sources.clear()

# ================================
# FACTORY FUNCTIONS
# ================================

def create_unified_configuration_system(config_name: str = "unified_config") -> UnifiedConfigurationSystem:
    """Create a new unified configuration system instance."""
    return UnifiedConfigurationSystem(config_name)

# ================================
# GLOBAL INSTANCE
# ================================

# Global unified configuration system instance
_unified_config = None

def get_unified_config() -> UnifiedConfigurationSystem:
    """Get the global unified configuration system instance."""
    global _unified_config
    if _unified_config is None:
        _unified_config = create_unified_configuration_system()
    return _unified_config

# ================================
# EXPORTS
# ================================

__all__ = [
    'UnifiedConfigurationSystem',
    'ConfigSource',
    'ConfigType',
    'create_unified_configuration_system',
    'get_unified_config'
]
