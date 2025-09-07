#!/usr/bin/env python3
"""
Unified Configuration Management System
Consolidates all scattered configuration files into a hierarchical, maintainable structure.
Eliminates SSOT violations and provides a single source of truth for all system configuration.

Author: Agent-8 (Integration Enhancement Manager)
Contract: SSOT-003: Configuration Management Consolidation (350 pts)
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging

class ConfigValidator:
    """Validate configuration against schemas and rules"""
    
    @staticmethod
    def validate_required_fields(config: Dict[str, Any], required: List[str]) -> bool:
        """Validate required fields are present"""
        for field in required:
            if field not in config:
                logging.error(f"Required field missing: {field}")
                return False
        return True
    
    @staticmethod
    def validate_field_types(config: Dict[str, Any], type_map: Dict[str, str]) -> bool:
        """Validate field types match expected types"""
        for field, expected_type in type_map.items():
            if field in config:
                actual_type = type(config[field]).__name__
                if actual_type != expected_type:
                    logging.error(f"Field {field} has type {actual_type}, expected {expected_type}")
                    return False
        return True
    
    @staticmethod
    def validate_schema(config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate configuration against JSON schema (basic implementation)"""
        # Basic schema validation - can be enhanced with jsonschema library
        if not isinstance(config, dict):
            return False
        
        # Check required fields
        required = schema.get("required", [])
        if not ConfigValidator.validate_required_fields(config, required):
            return False
        
        # Check field types
        properties = schema.get("properties", {})
        type_map = {field: props.get("type") for field, props in properties.items()}
        if not ConfigValidator.validate_field_types(config, type_map):
            return False
        
        return True

class ConfigLoader:
    """Load configuration files with support for multiple formats"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.yaml_cache = {}
        self.json_cache = {}
    
    def load_yaml(self, filepath: Path) -> Dict[str, Any]:
        """Load YAML configuration file"""
        try:
            if filepath in self.yaml_cache:
                return self.yaml_cache[filepath]
            
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self.yaml_cache[filepath] = config
                    return config or {}
            return {}
        except Exception as e:
            logging.error(f"Error loading YAML config {filepath}: {e}")
            return {}
    
    def load_json(self, filepath: Path) -> Dict[str, Any]:
        """Load JSON configuration file"""
        try:
            if filepath in self.json_cache:
                return self.json_cache[filepath]
            
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.json_cache[filepath] = config
                    return config or {}
            return {}
        except Exception as e:
            logging.error(f"Error loading JSON config {filepath}: {e}")
            return {}
    
    def load_env_overrides(self) -> Dict[str, Any]:
        """Load environment variable overrides"""
        overrides = {}
        for key, value in os.environ.items():
            if key.startswith("CONFIG_"):
                config_key = key[7:].lower().replace("_", ".")
                overrides[config_key] = value
        return overrides
    
    def resolve_variables(self, config: Dict[str, Any], env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Resolve variable references in configuration"""
        if isinstance(config, dict):
            resolved = {}
            for key, value in config.items():
                resolved[key] = self.resolve_variables(value, env_vars)
            return resolved
        elif isinstance(config, list):
            return [self.resolve_variables(item, env_vars) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            var_name = config[2:-1]
            if ":" in var_name:
                var_name, default = var_name.split(":", 1)
            else:
                default = None
            
            # Check environment variables first
            if var_name in env_vars:
                return env_vars[var_name]
            elif var_name in os.environ:
                return os.environ[var_name]
            else:
                return default or ""
        else:
            return config

class UnifiedConfigManager:
    """Unified configuration management system"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.loader = ConfigLoader(config_dir)
        self.validator = ConfigValidator()
        
        # Load environment overrides
        self.env_overrides = self.loader.load_env_overrides()
        
        # Initialize configuration
        self._load_all_configs()
    
    def _load_all_configs(self) -> None:
        """Load all configuration files"""
        try:
            # Load system configuration
            self.config_cache["system"] = self._load_system_config()
            
            # Load development configuration
            self.config_cache["development"] = self._load_development_config()
            
            # Load runtime configuration
            self.config_cache["runtime"] = self._load_runtime_config()
            
            # Apply environment overrides
            self._apply_env_overrides()
            
            logging.info("Configuration loaded successfully")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
    
    def _load_system_config(self) -> Dict[str, Any]:
        """Load system configuration files"""
        system_config = {}
        
        # Core system configuration
        core_file = self.config_dir / "system" / "core.yaml"
        if core_file.exists():
            core_config = self.loader.load_yaml(core_file)
            # Flatten the YAML structure by removing the top-level key
            if isinstance(core_config, dict) and len(core_config) == 1:
                system_config["core"] = list(core_config.values())[0]
            else:
                system_config["core"] = core_config
        
        # Logging configuration
        logging_file = self.config_dir / "system" / "logging.yaml"
        if logging_file.exists():
            logging_config = self.loader.load_yaml(logging_file)
            if isinstance(logging_config, dict) and len(logging_config) == 1:
                system_config["logging"] = list(logging_config.values())[0]
            else:
                system_config["logging"] = logging_config
        
        # Agent configuration
        agents_file = self.config_dir / "system" / "agents.yaml"
        if agents_file.exists():
            agents_config = self.loader.load_yaml(agents_file)
            if isinstance(agents_config, dict) and len(agents_config) == 1:
                system_config["agents"] = list(agents_config.values())[0]
            else:
                system_config["agents"] = agents_config
        
        # Service configuration
        services_file = self.config_dir / "system" / "services.yaml"
        if services_file.exists():
            services_config = self.loader.load_yaml(services_file)
            if isinstance(services_config, dict) and len(services_config) == 1:
                system_config["services"] = list(services_config.values())[0]
            else:
                system_config["services"] = services_config
        
        return system_config
    
    def _load_development_config(self) -> Dict[str, Any]:
        """Load development configuration files"""
        dev_config = {}
        
        # Testing configuration
        testing_file = self.config_dir / "development" / "testing.yaml"
        if testing_file.exists():
            testing_config = self.loader.load_yaml(testing_file)
            if isinstance(testing_config, dict) and len(testing_config) == 1:
                dev_config["testing"] = list(testing_config.values())[0]
            else:
                dev_config["testing"] = testing_config
        
        # CI/CD configuration
        cicd_file = self.config_dir / "development" / "ci_cd.yaml"
        if cicd_file.exists():
            cicd_config = self.loader.load_yaml(cicd_file)
            if isinstance(cicd_config, dict) and len(cicd_config) == 1:
                dev_config["ci_cd"] = list(cicd_config.values())[0]
            else:
                dev_config["ci_cd"] = cicd_config
        
        return dev_config
    
    def _load_runtime_config(self) -> Dict[str, Any]:
        """Load runtime configuration files"""
        runtime_config = {}
        
        # Emergency response configuration
        emergency_file = self.config_dir / "runtime" / "emergency.yaml"
        if emergency_file.exists():
            emergency_config = self.loader.load_yaml(emergency_file)
            if isinstance(emergency_config, dict) and len(emergency_config) == 1:
                runtime_config["emergency"] = list(emergency_config.values())[0]
            else:
                runtime_config["emergency"] = emergency_config
        
        # Monitoring configuration
        monitoring_file = self.config_dir / "runtime" / "monitoring.yaml"
        if monitoring_file.exists():
            monitoring_config = self.loader.load_yaml(monitoring_file)
            if isinstance(monitoring_config, dict) and len(monitoring_config) == 1:
                runtime_config["monitoring"] = list(monitoring_config.values())[0]
            else:
                runtime_config["monitoring"] = monitoring_config
        
        return runtime_config
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration"""
        for key_path, value in self.env_overrides.items():
            self.set_config(key_path, value)
    
    def get_config(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'system.core.version')"""
        try:
            keys = key_path.split(".")
            config = self.config_cache
            
            # Navigate through the configuration structure
            for key in keys:
                if isinstance(config, dict) and key in config:
                    config = config[key]
                else:
                    return default
            
            return config
        except Exception as e:
            logging.error(f"Error getting config {key_path}: {e}")
            return default
    
    def set_config(self, key_path: str, value: Any) -> bool:
        """Set configuration value using dot notation"""
        try:
            keys = key_path.split(".")
            config = self.config_cache
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set the value
            config[keys[-1]] = value
            return True
        except Exception as e:
            logging.error(f"Error setting config {key_path}: {e}")
            return False
    
    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """Get service configuration with inheritance"""
        try:
            service_config = self.get_config(f"system.services.{service_name}", {})
            base_config = self.get_config("system.services.base", {})
            
            # Merge base configuration with service-specific configuration
            merged_config = base_config.copy()
            merged_config.update(service_config)
            
            return merged_config
        except Exception as e:
            logging.error(f"Error getting service config for {service_name}: {e}")
            return {}
    
    def get_env_config(self, environment: str = None) -> Dict[str, Any]:
        """Get environment-specific configuration"""
        if environment is None:
            environment = self.environment
        
        # Load environment-specific configuration file
        env_file = self.config_dir / f"environments/{environment}.yaml"
        if env_file.exists():
            return self.loader.load_yaml(env_file)
        
        return {}
    
    def validate_config(self, config: Dict[str, Any], schema: Dict[str, Any] = None) -> bool:
        """Validate configuration against schema"""
        if schema:
            return self.validator.validate_schema(config, schema)
        else:
            # Basic validation - check for required fields
            required_fields = ["version", "environment"]
            return self.validator.validate_required_fields(config, required_fields)
    
    def reload_config(self) -> bool:
        """Reload all configuration files"""
        try:
            # Clear caches
            self.config_cache.clear()
            self.loader.yaml_cache.clear()
            self.loader.json_cache.clear()
            
            # Reload configuration
            self._load_all_configs()
            return True
        except Exception as e:
            logging.error(f"Error reloading configuration: {e}")
            return False
    
    def export_config(self, format: str = "yaml") -> str:
        """Export current configuration to specified format"""
        try:
            if format.lower() == "json":
                return json.dumps(self.config_cache, indent=2, default=str)
            elif format.lower() == "yaml":
                return yaml.dump(self.config_cache, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            logging.error(f"Error exporting configuration: {e}")
            return ""
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary and statistics"""
        try:
            summary = {
                "total_configs": len(self.config_cache),
                "categories": list(self.config_cache.keys()),
                "environment": self.environment,
                "last_loaded": datetime.now().isoformat(),
                "config_sizes": {}
            }
            
            for category, config in self.config_cache.items():
                summary["config_sizes"][category] = len(str(config))
            
            return summary
        except Exception as e:
            logging.error(f"Error getting config summary: {e}")
            return {}

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the configuration manager."""
        return {
            "environment": self.environment,
            "last_loaded": datetime.now().isoformat(),
            "config_cache_size": len(self.config_cache),
            "config_cache_keys": list(self.config_cache.keys()),
            "config_summary": self.get_config_summary()
        }

# Global configuration manager instance
config_manager = UnifiedConfigManager()

# Convenience functions
def get_config(key_path: str, default: Any = None) -> Any:
    """Get configuration value using dot notation"""
    return config_manager.get_config(key_path, default)

def set_config(key_path: str, value: Any) -> bool:
    """Set configuration value using dot notation"""
    return config_manager.set_config(key_path, value)

def get_service_config(service_name: str) -> Dict[str, Any]:
    """Get service configuration with inheritance"""
    return config_manager.get_service_config(service_name)

def get_env_config(environment: str = None) -> Dict[str, Any]:
    """Get environment-specific configuration"""
    return config_manager.get_env_config(environment)

def reload_config() -> bool:
    """Reload all configuration files"""
    return config_manager.reload_config()

if __name__ == "__main__":
    # Test the configuration manager
    logging.basicConfig(level=logging.INFO)
    
    print("=== Unified Configuration Management System ===")
    print(f"Environment: {config_manager.environment}")
    print(f"Config Summary: {config_manager.get_config_summary()}")
    
    # Test configuration access
    print(f"\nSystem Version: {get_config('system.core.version', 'Not set')}")
    print(f"Agent Count: {get_config('system.agents.count', 'Not set')}")
    
    # Test service configuration
    messaging_config = get_service_config("messaging")
    print(f"\nMessaging Service Config: {messaging_config}")
