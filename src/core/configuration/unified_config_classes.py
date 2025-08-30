#!/usr/bin/env python3
"""
Unified Configuration Classes - Agent Cellphone V2
================================================

Consolidated configuration classes system that eliminates duplication across
multiple configuration implementations. Provides unified configuration containers,
managers, and utilities for all application domains.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Union, Optional, List, Type
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import yaml
import logging
from abc import ABC, abstractmethod
import threading
from datetime import datetime

from .unified_constants import (
    ConfigCategory, ConfigPriority, get_constant,
    DEFAULT_MAX_WORKERS, DEFAULT_CACHE_SIZE, DEFAULT_OPERATION_TIMEOUT,
    DEFAULT_AI_MODEL_TIMEOUT, DEFAULT_FSM_TIMEOUT, DEFAULT_TEST_TIMEOUT
)


# ============================================================================
# UNIFIED CONFIGURATION CLASSES
# ============================================================================

class ConfigFormat(Enum):
    """Configuration file format enumeration."""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    PYTHON = "python"
    ENV = "env"
    AUTO = "auto"


class ConfigValidationLevel(Enum):
    """Configuration validation level enumeration."""
    NONE = 0
    BASIC = 1
    STRICT = 2
    COMPREHENSIVE = 3


class ConfigType(Enum):
    """Configuration type enumeration."""
    GLOBAL = "global"
    SYSTEM = "system"
    SERVICE = "service"
    AGENT = "agent"
    MODULE = "module"
    USER = "user"
    ENVIRONMENT = "environment"
    CUSTOM = "custom"


@dataclass
class ConfigMetadata:
    """Configuration metadata for tracking and validation."""
    name: str
    config_type: ConfigType
    format: ConfigFormat
    source_path: Optional[str] = None
    last_modified: Optional[str] = None
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    validation_level: ConfigValidationLevel = ConfigValidationLevel.BASIC
    is_encrypted: bool = False
    encryption_algorithm: Optional[str] = None
    checksum: Optional[str] = None


@dataclass
class ConfigSection:
    """Configuration section with hierarchical organization."""
    name: str
    data: Dict[str, Any]
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metadata: Optional[ConfigMetadata] = None
    is_override: bool = False
    override_source: Optional[str] = None


@dataclass
class ConfigValidationResult:
    """Result of configuration validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validation_level: ConfigValidationLevel = ConfigValidationLevel.BASIC
    timestamp: str = ""
    validator_version: str = "1.0.0"


@dataclass
class ConfigChangeEvent:
    """Configuration change event for tracking modifications."""
    config_name: str
    change_type: str  # "create", "update", "delete", "reload"
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    timestamp: str = ""
    user: Optional[str] = None
    source: Optional[str] = None


# ============================================================================
# DOMAIN-SPECIFIC CONFIGURATION CLASSES
# ============================================================================

@dataclass
class AIConfig:
    """Unified AI/ML configuration container."""
    api_keys: Dict[str, str] = field(default_factory=dict)
    model_timeout: float = DEFAULT_AI_MODEL_TIMEOUT
    batch_size: int = get_constant("DEFAULT_AI_BATCH_SIZE", 32)
    max_tokens: int = get_constant("DEFAULT_AI_MAX_TOKENS", 2048)
    retry_count: int = get_constant("DEFAULT_AI_API_RETRY_COUNT", 3)
    retry_delay: float = get_constant("DEFAULT_AI_API_RETRY_DELAY", 1.0)
    model_type: str = "gpt"
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: List[str] = field(default_factory=list)
    log_level: str = "INFO"
    cache_enabled: bool = True
    cache_ttl: int = get_constant("DEFAULT_CACHE_TTL", 3600)


@dataclass
class FSMConfig:
    """Unified FSM configuration container."""
    timeout: float = DEFAULT_FSM_TIMEOUT
    max_states: int = get_constant("DEFAULT_FSM_MAX_STATES", 100)
    max_transitions: int = get_constant("DEFAULT_FSM_MAX_TRANSITIONS", 200)
    execution_timeout: float = get_constant("DEFAULT_FSM_EXECUTION_TIMEOUT", 300.0)
    step_timeout: float = get_constant("DEFAULT_FSM_STEP_TIMEOUT", 30.0)
    auto_save: bool = True
    save_interval: float = 60.0
    validation_enabled: bool = True
    strict_mode: bool = False
    debug_mode: bool = False
    log_transitions: bool = True
    max_history_size: int = 1000
    persistence_enabled: bool = True
    persistence_path: str = "fsm_states.json"


@dataclass
class PerformanceConfig:
    """Unified performance configuration container."""
    max_workers: int = DEFAULT_MAX_WORKERS
    thread_pool_size: int = get_constant("DEFAULT_THREAD_POOL_SIZE", 10)
    process_pool_size: int = get_constant("DEFAULT_PROCESS_POOL_SIZE", 4)
    cache_size: int = DEFAULT_CACHE_SIZE
    cache_ttl: int = get_constant("DEFAULT_CACHE_TTL", 3600)
    batch_size: int = get_constant("DEFAULT_BATCH_SIZE", 100)
    operation_timeout: float = DEFAULT_OPERATION_TIMEOUT
    request_timeout: float = get_constant("DEFAULT_REQUEST_TIMEOUT", 30.0)
    connection_timeout: float = get_constant("DEFAULT_CONNECTION_TIMEOUT", 10.0)
    enable_profiling: bool = False
    profiling_interval: float = 5.0
    memory_limit_mb: int = 1024
    cpu_limit_percent: int = 80
    enable_monitoring: bool = True
    monitoring_interval: float = 30.0


@dataclass
class QualityConfig:
    """Unified quality configuration container."""
    check_interval: float = get_constant("DEFAULT_CHECK_INTERVAL", 30.0)
    health_check_interval: float = get_constant("DEFAULT_HEALTH_CHECK_INTERVAL", 60.0)
    coverage_threshold: float = get_constant("DEFAULT_COVERAGE_THRESHOLD", 80.0)
    performance_threshold: float = get_constant("DEFAULT_PERFORMANCE_THRESHOLD", 100.0)
    error_threshold: int = get_constant("DEFAULT_ERROR_THRESHOLD", 0)
    history_window: int = get_constant("DEFAULT_HISTORY_WINDOW", 100)
    retention_days: int = get_constant("DEFAULT_RETENTION_DAYS", 30)
    alert_enabled: bool = True
    alert_threshold: float = 0.8
    auto_fix_enabled: bool = False
    quality_gates_enabled: bool = True
    reporting_enabled: bool = True
    metrics_collection: bool = True


@dataclass
class MessagingConfig:
    """Unified messaging configuration container."""
    mode: str = get_constant("DEFAULT_MESSAGING_MODE", "pyautogui")
    coordinate_mode: str = get_constant("DEFAULT_COORDINATE_MODE", "8-agent")
    agent_count: int = get_constant("DEFAULT_AGENT_COUNT", 8)
    captain_id: str = get_constant("DEFAULT_CAPTAIN_ID", "Agent-4")
    message_timeout: float = get_constant("DEFAULT_MESSAGE_TIMEOUT", 5.0)
    retry_delay: float = get_constant("DEFAULT_RETRY_DELAY", 1.0)
    max_retries: int = get_constant("DEFAULT_MAX_RETRIES", 3)
    encryption_enabled: bool = False
    encryption_key: Optional[str] = None
    compression_enabled: bool = False
    queue_size: int = 1000
    priority_levels: int = 5
    dead_letter_queue: bool = True
    message_persistence: bool = False


@dataclass
class TestingConfig:
    """Unified testing configuration container."""
    timeout: float = DEFAULT_TEST_TIMEOUT
    retry_count: int = get_constant("DEFAULT_TEST_RETRY_COUNT", 3)
    parallel_workers: int = get_constant("DEFAULT_TEST_PARALLEL_WORKERS", 4)
    coverage_min_percent: float = get_constant("DEFAULT_COVERAGE_MIN_PERCENT", 80.0)
    coverage_fail_under: float = get_constant("DEFAULT_COVERAGE_FAIL_UNDER", 70.0)
    test_discovery_pattern: str = "test_*.py"
    exclude_patterns: List[str] = field(default_factory=lambda: ["*_test.py", "test_*_*.py"])
    random_seed: Optional[int] = None
    verbose_output: bool = False
    stop_on_failure: bool = False
    generate_reports: bool = True
    report_format: str = "html"
    report_path: str = "test_reports"
    enable_debugging: bool = False
    debug_breakpoints: bool = False


@dataclass
class NetworkConfig:
    """Unified network configuration container."""
    host: str = get_constant("DEFAULT_NETWORK_HOST", "localhost")
    port: int = get_constant("DEFAULT_NETWORK_PORT", 8080)
    max_connections: int = get_constant("DEFAULT_MAX_CONNECTIONS", 100)
    connection_timeout: float = get_constant("DEFAULT_CONNECTION_TIMEOUT", 10.0)
    read_timeout: float = get_constant("DEFAULT_READ_TIMEOUT", 30.0)
    write_timeout: float = get_constant("DEFAULT_WRITE_TIMEOUT", 30.0)
    keep_alive: bool = True
    keep_alive_timeout: float = 60.0
    max_retries: int = 3
    retry_delay: float = 1.0
    ssl_enabled: bool = False
    ssl_cert_file: Optional[str] = None
    ssl_key_file: Optional[str] = None
    compression_enabled: bool = False
    rate_limiting_enabled: bool = True
    max_requests_per_minute: int = 1000


@dataclass
class SecurityConfig:
    """Unified security configuration container."""
    authentication_enabled: bool = True
    authorization_enabled: bool = True
    session_timeout: float = get_constant("DEFAULT_SECURITY_TIMEOUT", 3600.0)
    max_login_attempts: int = get_constant("DEFAULT_MAX_LOGIN_ATTEMPTS", 5)
    lockout_duration: float = 300.0
    password_min_length: int = 8
    password_require_special: bool = True
    password_require_numbers: bool = True
    password_require_uppercase: bool = True
    encryption_enabled: bool = True
    encryption_algorithm: str = "AES-256"
    jwt_secret: Optional[str] = None
    jwt_expiration: float = 3600.0
    csrf_protection: bool = True
    rate_limiting_enabled: bool = True
    max_requests_per_ip: int = 100
    ip_whitelist: List[str] = field(default_factory=list)
    ip_blacklist: List[str] = field(default_factory=list)


@dataclass
class DatabaseConfig:
    """Unified database configuration container."""
    host: str = get_constant("DEFAULT_DB_HOST", "localhost")
    port: int = get_constant("DEFAULT_DB_PORT", 5432)
    database: str = "agent_cellphone_v2"
    username: Optional[str] = None
    password: Optional[str] = None
    pool_size: int = get_constant("DEFAULT_DB_POOL_SIZE", 10)
    max_connections: int = 20
    connection_timeout: float = 10.0
    query_timeout: float = 30.0
    transaction_timeout: float = 60.0
    retry_count: int = 3
    retry_delay: float = 1.0
    ssl_enabled: bool = False
    ssl_cert_file: Optional[str] = None
    ssl_key_file: Optional[str] = None
    backup_enabled: bool = True
    backup_interval: float = 86400.0
    backup_retention_days: int = 30
    logging_enabled: bool = True
    slow_query_threshold: float = 1.0


@dataclass
class LoggingConfig:
    """Unified logging configuration container."""
    level: str = get_constant("LOG_LEVEL", "INFO")
    format: str = get_constant("DEFAULT_LOG_FORMAT", "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    file_enabled: bool = True
    file_path: str = "logs/agent_cellphone_v2.log"
    file_max_size: int = get_constant("DEFAULT_LOG_FILE_SIZE", 10 * 1024 * 1024)  # 10MB
    file_backup_count: int = 5
    console_enabled: bool = True
    console_level: str = "INFO"
    syslog_enabled: bool = False
    syslog_host: Optional[str] = None
    syslog_port: int = 514
    syslog_facility: str = "local0"
    json_format: bool = False
    include_timestamp: bool = True
    include_level: bool = True
    include_name: bool = True
    include_thread: bool = False
    include_process: bool = False
    color_enabled: bool = True
    sensitive_fields: List[str] = field(default_factory=lambda: ["password", "token", "secret", "key"])


# ============================================================================
# UNIFIED CONFIGURATION MANAGER
# ============================================================================

class UnifiedConfigurationManager(ABC):
    """Abstract base class for unified configuration management."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, ConfigMetadata] = {}
        self.change_history: List[ConfigChangeEvent] = []
        self._lock = threading.Lock()
    
    @abstractmethod
    def load_config(self, config_name: str, config_type: ConfigType) -> bool:
        """Load configuration from source."""
        pass
    
    @abstractmethod
    def save_config(self, config_name: str, config_data: Dict[str, Any], 
                   config_type: ConfigType, format: ConfigFormat = ConfigFormat.JSON) -> bool:
        """Save configuration to destination."""
        pass
    
    @abstractmethod
    def get_config(self, config_name: str, default: Any = None) -> Any:
        """Get configuration value."""
        pass
    
    @abstractmethod
    def set_config(self, config_name: str, key: str, value: Any) -> bool:
        """Set configuration value."""
        pass
    
    @abstractmethod
    def delete_config(self, config_name: str) -> bool:
        """Delete configuration."""
        pass
    
    @abstractmethod
    def validate_config(self, config_name: str) -> ConfigValidationResult:
        """Validate configuration."""
        pass
    
    def list_configs(self) -> List[str]:
        """List all available configurations."""
        with self._lock:
            return list(self.configs.keys())
    
    def get_metadata(self, config_name: str) -> Optional[ConfigMetadata]:
        """Get configuration metadata."""
        with self._lock:
            return self.metadata.get(config_name)
    
    def get_change_history(self, config_name: Optional[str] = None) -> List[ConfigChangeEvent]:
        """Get configuration change history."""
        with self._lock:
            if config_name:
                return [event for event in self.change_history if event.config_name == config_name]
            return self.change_history.copy()
    
    def _add_change_event(self, config_name: str, change_type: str, 
                         old_value: Any = None, new_value: Any = None):
        """Add change event to history."""
        event = ConfigChangeEvent(
            config_name=config_name,
            change_type=change_type,
            old_value=old_value,
            new_value=new_value,
            timestamp=datetime.now().isoformat()
        )
        with self._lock:
            self.change_history.append(event)
            # Keep only last 1000 events
            if len(self.change_history) > 1000:
                self.change_history = self.change_history[-1000:]


# ============================================================================
# FILE-BASED CONFIGURATION MANAGER
# ============================================================================

class FileBasedConfigurationManager(UnifiedConfigurationManager):
    """File-based configuration manager supporting multiple formats."""
    
    def __init__(self, config_dir: str = "config"):
        super().__init__(config_dir)
        self.supported_formats = {ConfigFormat.JSON, ConfigFormat.YAML, ConfigFormat.INI, ConfigFormat.PYTHON}
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_config_path(self, config_name: str, format: ConfigFormat) -> Path:
        """Get configuration file path."""
        extension_map = {
            ConfigFormat.JSON: ".json",
            ConfigFormat.YAML: ".yaml",
            ConfigFormat.INI: ".ini",
            ConfigFormat.PYTHON: ".py"
        }
        extension = extension_map.get(format, ".json")
        return self.config_dir / f"{config_name}{extension}"
    
    def load_config(self, config_name: str, config_type: ConfigType) -> bool:
        """Load configuration from file."""
        try:
            # Try to auto-detect format
            for format in [ConfigFormat.JSON, ConfigFormat.YAML, ConfigFormat.INI, ConfigFormat.PYTHON]:
                config_path = self._get_config_path(config_name, format)
                if config_path.exists():
                    return self._load_from_file(config_name, config_path, format, config_type)
            
            # If no file exists, create default
            self.configs[config_name] = {}
            self.metadata[config_name] = ConfigMetadata(
                name=config_name,
                config_type=config_type,
                format=ConfigFormat.JSON
            )
            return True
            
        except Exception as e:
            logging.error(f"Failed to load config {config_name}: {e}")
            return False
    
    def _load_from_file(self, config_name: str, config_path: Path, 
                        format: ConfigFormat, config_type: ConfigType) -> bool:
        """Load configuration from specific file format."""
        try:
            if format == ConfigFormat.JSON:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            elif format == ConfigFormat.YAML:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            elif format == ConfigFormat.INI:
                config_data = self._load_ini_file(config_path)
            elif format == ConfigFormat.PYTHON:
                config_data = self._load_python_file(config_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            with self._lock:
                self.configs[config_name] = config_data
                self.metadata[config_name] = ConfigMetadata(
                    name=config_name,
                    config_type=config_type,
                    format=format,
                    source_path=str(config_path),
                    last_modified=datetime.fromtimestamp(config_path.stat().st_mtime).isoformat()
                )
            
            self._add_change_event(config_name, "reload")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load {format.value} config from {config_path}: {e}")
            return False
    
    def _load_ini_file(self, config_path: Path) -> Dict[str, Any]:
        """Load INI configuration file."""
        import configparser
        config = configparser.ConfigParser()
        config.read(config_path)
        
        result = {}
        for section in config.sections():
            result[section] = dict(config.items(section))
        
        return result
    
    def _load_python_file(self, config_path: Path) -> Dict[str, Any]:
        """Load Python configuration file."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("config_module", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Extract configuration variables (uppercase)
        config_data = {}
        for attr_name in dir(module):
            if attr_name.isupper() and not attr_name.startswith('_'):
                config_data[attr_name] = getattr(module, attr_name)
        
        return config_data
    
    def save_config(self, config_name: str, config_data: Dict[str, Any], 
                   config_type: ConfigType, format: ConfigFormat = ConfigFormat.JSON) -> bool:
        """Save configuration to file."""
        try:
            config_path = self._get_config_path(config_name, format)
            
            if format == ConfigFormat.JSON:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            elif format == ConfigFormat.YAML:
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            elif format == ConfigFormat.INI:
                self._save_ini_file(config_path, config_data)
            elif format == ConfigFormat.PYTHON:
                self._save_python_file(config_path, config_data)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            with self._lock:
                self.configs[config_name] = config_data
                if config_name in self.metadata:
                    self.metadata[config_name].last_modified = datetime.now().isoformat()
                    self.metadata[config_name].format = format
                else:
                    self.metadata[config_name] = ConfigMetadata(
                        name=config_name,
                        config_type=config_type,
                        format=format,
                        source_path=str(config_path)
                    )
            
            self._add_change_event(config_name, "update")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save config {config_name}: {e}")
            return False
    
    def _save_ini_file(self, config_path: Path, config_data: Dict[str, Any]):
        """Save configuration to INI file."""
        import configparser
        config = configparser.ConfigParser()
        
        for section_name, section_data in config_data.items():
            if isinstance(section_data, dict):
                config.add_section(section_name)
                for key, value in section_data.items():
                    config.set(section_name, key, str(value))
            else:
                # Single value, put in DEFAULT section
                if not config.has_section('DEFAULT'):
                    config.add_section('DEFAULT')
                config.set('DEFAULT', section_name, str(section_data))
        
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
    
    def _save_python_file(self, config_path: Path, config_data: Dict[str, Any]):
        """Save configuration to Python file."""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("# Configuration file generated by UnifiedConfigurationManager\n")
            f.write("# Generated on: {}\n\n".format(datetime.now().isoformat()))
            
            for key, value in config_data.items():
                if isinstance(value, str):
                    f.write(f'{key} = "{value}"\n')
                else:
                    f.write(f'{key} = {repr(value)}\n')
    
    def get_config(self, config_name: str, default: Any = None) -> Any:
        """Get configuration value."""
        with self._lock:
            return self.configs.get(config_name, default)
    
    def set_config(self, config_name: str, key: str, value: Any) -> bool:
        """Set configuration value."""
        try:
            with self._lock:
                if config_name not in self.configs:
                    self.configs[config_name] = {}
                
                old_value = self.configs[config_name].get(key)
                self.configs[config_name][key] = value
                
                # Update metadata
                if config_name in self.metadata:
                    self.metadata[config_name].last_modified = datetime.now().isoformat()
                
                self._add_change_event(config_name, "update", old_value, value)
                return True
                
        except Exception as e:
            logging.error(f"Failed to set config {config_name}.{key}: {e}")
            return False
    
    def delete_config(self, config_name: str) -> bool:
        """Delete configuration."""
        try:
            with self._lock:
                if config_name in self.configs:
                    old_config = self.configs[config_name]
                    del self.configs[config_name]
                    
                    if config_name in self.metadata:
                        del self.metadata[config_name]
                    
                    self._add_change_event(config_name, "delete", old_config, None)
                
                # Remove file
                for format in self.supported_formats:
                    config_path = self._get_config_path(config_name, format)
                    if config_path.exists():
                        config_path.unlink()
                        break
                
                return True
                
        except Exception as e:
            logging.error(f"Failed to delete config {config_name}: {e}")
            return False
    
    def validate_config(self, config_name: str) -> ConfigValidationResult:
        """Validate configuration."""
        try:
            with self._lock:
                if config_name not in self.configs:
                    return ConfigValidationResult(
                        is_valid=False,
                        errors=[f"Configuration '{config_name}' not found"]
                    )
                
                config_data = self.configs[config_name]
                metadata = self.metadata.get(config_name)
                
                # Basic validation
                errors = []
                warnings = []
                
                if not isinstance(config_data, dict):
                    errors.append("Configuration data must be a dictionary")
                
                if metadata and metadata.validation_level == ConfigValidationLevel.STRICT:
                    # Strict validation
                    if not metadata.name:
                        warnings.append("Configuration name is empty")
                    
                    if not metadata.format:
                        warnings.append("Configuration format is not specified")
                
                elif metadata and metadata.validation_level == ConfigValidationLevel.COMPREHENSIVE:
                    # Comprehensive validation
                    if not metadata.name:
                        errors.append("Configuration name is required")
                    
                    if not metadata.format:
                        errors.append("Configuration format is required")
                    
                    if not metadata.version:
                        warnings.append("Configuration version is not specified")
                    
                    if not metadata.description:
                        warnings.append("Configuration description is not specified")
                
                return ConfigValidationResult(
                    is_valid=len(errors) == 0,
                    errors=errors,
                    warnings=warnings,
                    validation_level=metadata.validation_level if metadata else ConfigValidationLevel.BASIC
                )
                
        except Exception as e:
            return ConfigValidationResult(
                is_valid=False,
                errors=[f"Validation failed: {e}"],
                validation_level=ConfigValidationLevel.BASIC
            )


# ============================================================================
# CONFIGURATION FACTORY
# ============================================================================

class ConfigurationFactory:
    """Factory for creating configuration instances and managers."""
    
    @staticmethod
    def create_ai_config(**kwargs) -> AIConfig:
        """Create AI configuration instance."""
        return AIConfig(**kwargs)
    
    @staticmethod
    def create_fsm_config(**kwargs) -> FSMConfig:
        """Create FSM configuration instance."""
        return FSMConfig(**kwargs)
    
    @staticmethod
    def create_performance_config(**kwargs) -> PerformanceConfig:
        """Create performance configuration instance."""
        return PerformanceConfig(**kwargs)
    
    @staticmethod
    def create_quality_config(**kwargs) -> QualityConfig:
        """Create quality configuration instance."""
        return QualityConfig(**kwargs)
    
    @staticmethod
    def create_messaging_config(**kwargs) -> MessagingConfig:
        """Create messaging configuration instance."""
        return MessagingConfig(**kwargs)
    
    @staticmethod
    def create_testing_config(**kwargs) -> TestingConfig:
        """Create testing configuration instance."""
        return TestingConfig(**kwargs)
    
    @staticmethod
    def create_network_config(**kwargs) -> NetworkConfig:
        """Create network configuration instance."""
        return NetworkConfig(**kwargs)
    
    @staticmethod
    def create_security_config(**kwargs) -> SecurityConfig:
        """Create security configuration instance."""
        return SecurityConfig(**kwargs)
    
    @staticmethod
    def create_database_config(**kwargs) -> DatabaseConfig:
        """Create database configuration instance."""
        return DatabaseConfig(**kwargs)
    
    @staticmethod
    def create_logging_config(**kwargs) -> LoggingConfig:
        """Create logging configuration instance."""
        return LoggingConfig(**kwargs)
    
    @staticmethod
    def create_manager(manager_type: str = "file", **kwargs) -> UnifiedConfigurationManager:
        """Create configuration manager instance."""
        if manager_type == "file":
            return FileBasedConfigurationManager(**kwargs)
        else:
            raise ValueError(f"Unknown manager type: {manager_type}")


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Global configuration factory
CONFIG_FACTORY = ConfigurationFactory()

# Global file-based configuration manager
FILE_CONFIG_MANAGER = FileBasedConfigurationManager()


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Enums
    "ConfigFormat",
    "ConfigValidationLevel", 
    "ConfigType",
    
    # Base classes
    "ConfigMetadata",
    "ConfigSection",
    "ConfigValidationResult",
    "ConfigChangeEvent",
    "UnifiedConfigurationManager",
    
    # Domain-specific configurations
    "AIConfig",
    "FSMConfig", 
    "PerformanceConfig",
    "QualityConfig",
    "MessagingConfig",
    "TestingConfig",
    "NetworkConfig",
    "SecurityConfig",
    "DatabaseConfig",
    "LoggingConfig",
    
    # Managers
    "FileBasedConfigurationManager",
    
    # Factory
    "ConfigurationFactory",
    
    # Global instances
    "CONFIG_FACTORY",
    "FILE_CONFIG_MANAGER"
]
