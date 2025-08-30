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
    host: str = get_constant("DEFAULT_NETWORK_HOST", "0.0.0.0")
    port: int = get_constant("DEFAULT_NETWORK_PORT", 8000)
    timeout: float = get_constant("DEFAULT_NETWORK_TIMEOUT", 30.0)
    max_connections: int = get_constant("DEFAULT_MAX_CONNECTIONS", 100)
    keep_alive: bool = get_constant("DEFAULT_KEEP_ALIVE", True)
    ssl_enabled: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
    rate_limiting_enabled: bool = False
    rate_limit_requests: int = 100
    rate_limit_window: float = 60.0
    cors_enabled: bool = False
    cors_origins: List[str] = field(default_factory=list)
    proxy_enabled: bool = False
    proxy_url: Optional[str] = None


@dataclass
class SecurityConfig:
    """Unified security configuration container."""
    timeout: float = get_constant("DEFAULT_SECURITY_TIMEOUT", 30.0)
    max_login_attempts: int = get_constant("DEFAULT_MAX_LOGIN_ATTEMPTS", 5)
    session_timeout: float = get_constant("DEFAULT_SESSION_TIMEOUT", 3600.0)
    encryption_algorithm: str = get_constant("DEFAULT_ENCRYPTION_ALGORITHM", "AES-256")
    hash_algorithm: str = get_constant("DEFAULT_HASH_ALGORITHM", "SHA-256")
    password_min_length: int = 8
    password_require_special: bool = True
    password_require_numbers: bool = True
    password_require_uppercase: bool = True
    jwt_secret: Optional[str] = None
    jwt_expiry_hours: int = 24
    mfa_enabled: bool = False
    mfa_type: str = "totp"
    audit_logging_enabled: bool = True
    ip_whitelist: List[str] = field(default_factory=list)
    ip_blacklist: List[str] = field(default_factory=list)


@dataclass
class DatabaseConfig:
    """Unified database configuration container."""
    host: str = get_constant("DEFAULT_DB_HOST", "localhost")
    port: int = get_constant("DEFAULT_DB_PORT", 5432)
    name: str = get_constant("DEFAULT_DB_NAME", "agent_cellphone_v2")
    pool_size: int = get_constant("DEFAULT_DB_POOL_SIZE", 10)
    timeout: float = get_constant("DEFAULT_DB_TIMEOUT", 30.0)
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_mode: str = "prefer"
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    ssl_ca: Optional[str] = None
    connection_retries: int = 3
    retry_delay: float = 1.0
    enable_logging: bool = False
    log_queries: bool = False
    log_slow_queries: bool = True
    slow_query_threshold: float = 1.0
    enable_pooling: bool = True
    max_overflow: int = 20


@dataclass
class LoggingConfig:
    """Unified logging configuration container."""
    format: str = get_constant("DEFAULT_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    date_format: str = get_constant("DEFAULT_LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
    file_size: int = get_constant("DEFAULT_LOG_FILE_SIZE", 10485760)
    backup_count: int = get_constant("DEFAULT_LOG_BACKUP_COUNT", 5)
    level: str = "INFO"
    file_enabled: bool = True
    console_enabled: bool = True
    syslog_enabled: bool = False
    syslog_host: Optional[str] = None
    syslog_port: int = 514
    syslog_facility: str = "user"
    json_format: bool = False
    include_timestamp: bool = True
    include_level: bool = True
    include_logger: bool = True
    include_thread: bool = False
    include_process: bool = False
    enable_rotation: bool = True
    rotation_when: str = "midnight"
    rotation_interval: int = 1


# ============================================================================
# UNIFIED CONFIGURATION MANAGER
# ============================================================================

class UnifiedConfigurationManager(ABC):
    """Abstract base class for unified configuration management."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Any] = {}
        self.metadata: Dict[str, ConfigMetadata] = {}
        self.validation_results: Dict[str, ConfigValidationResult] = {}
        self.change_history: List[ConfigChangeEvent] = []
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def load_config(self, config_name: str, config_type: ConfigType) -> bool:
        """Load configuration from source."""
        pass
    
    @abstractmethod
    def save_config(self, config_name: str, config_data: Any) -> bool:
        """Save configuration to destination."""
        pass
    
    @abstractmethod
    def validate_config(self, config_name: str) -> ConfigValidationResult:
        """Validate configuration."""
        pass
    
    def get_config(self, config_name: str, default: Any = None) -> Any:
        """Get configuration by name."""
        return self.configs.get(config_name, default)
    
    def set_config(self, config_name: str, config_data: Any) -> bool:
        """Set configuration by name."""
        try:
            old_value = self.configs.get(config_name)
            self.configs[config_name] = config_data
            
            # Record change event
            change_event = ConfigChangeEvent(
                config_name=config_name,
                change_type="update" if old_value is not None else "create",
                old_value=old_value,
                new_value=config_data,
                timestamp=self._get_timestamp(),
                source=self.__class__.__name__
            )
            self.change_history.append(change_event)
            
            return True
        except Exception as e:
            self.logger.error(f"Error setting config {config_name}: {e}")
            return False
    
    def delete_config(self, config_name: str) -> bool:
        """Delete configuration by name."""
        try:
            if config_name in self.configs:
                old_value = self.configs[config_name]
                del self.configs[config_name]
                
                # Record change event
                change_event = ConfigChangeEvent(
                    config_name=config_name,
                    change_type="delete",
                    old_value=old_value,
                    new_value=None,
                    timestamp=self._get_timestamp(),
                    source=self.__class__.__name__
                )
                self.change_history.append(change_event)
                
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting config {config_name}: {e}")
            return False
    
    def list_configs(self) -> List[str]:
        """List all configuration names."""
        return list(self.configs.keys())
    
    def get_metadata(self, config_name: str) -> Optional[ConfigMetadata]:
        """Get configuration metadata."""
        return self.metadata.get(config_name)
    
    def get_validation_result(self, config_name: str) -> Optional[ConfigValidationResult]:
        """Get configuration validation result."""
        return self.validation_results.get(config_name)
    
    def get_change_history(self, config_name: Optional[str] = None) -> List[ConfigChangeEvent]:
        """Get configuration change history."""
        if config_name:
            return [event for event in self.change_history if event.config_name == config_name]
        return self.change_history
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()


# ============================================================================
# CONCRETE CONFIGURATION MANAGERS
# ============================================================================

class FileBasedConfigurationManager(UnifiedConfigurationManager):
    """File-based configuration manager supporting multiple formats."""
    
    def __init__(self, config_dir: str = "config"):
        super().__init__(config_dir)
        self.supported_formats = {ConfigFormat.JSON, ConfigFormat.YAML, ConfigFormat.INI, ConfigFormat.PYTHON}
    
    def load_config(self, config_name: str, config_type: ConfigType) -> bool:
        """Load configuration from file."""
        try:
            # Try different file formats
            for format_type in self.supported_formats:
                file_path = self._get_config_file_path(config_name, format_type)
                if file_path.exists():
                    config_data = self._load_file(file_path, format_type)
                    if config_data:
                        self.configs[config_name] = config_data
                        
                        # Create metadata
                        metadata = ConfigMetadata(
                            name=config_name,
                            config_type=config_type,
                            format=format_type,
                            source_path=str(file_path),
                            last_modified=self._get_file_timestamp(file_path)
                        )
                        self.metadata[config_name] = metadata
                        
                        # Validate configuration
                        self.validation_results[config_name] = self.validate_config(config_name)
                        
                        self.logger.info(f"Loaded config {config_name} from {file_path}")
                        return True
            
            self.logger.warning(f"No configuration file found for {config_name}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error loading config {config_name}: {e}")
            return False
    
    def save_config(self, config_name: str, config_data: Any) -> bool:
        """Save configuration to file."""
        try:
            metadata = self.metadata.get(config_name)
            if not metadata:
                self.logger.error(f"No metadata found for config {config_name}")
                return False
            
            file_path = self._get_config_file_path(config_name, metadata.format)
            success = self._save_file(file_path, config_data, metadata.format)
            
            if success:
                # Update metadata
                metadata.last_modified = self._get_file_timestamp(file_path)
                self.metadata[config_name] = metadata
                
                # Record change event
                change_event = ConfigChangeEvent(
                    config_name=config_name,
                    change_type="update",
                    old_value=self.configs.get(config_name),
                    new_value=config_data,
                    timestamp=self._get_timestamp(),
                    source=self.__class__.__name__
                )
                self.change_history.append(change_event)
                
                self.logger.info(f"Saved config {config_name} to {file_path}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error saving config {config_name}: {e}")
            return False
    
    def validate_config(self, config_name: str) -> ConfigValidationResult:
        """Validate configuration."""
        try:
            config_data = self.configs.get(config_name)
            if not config_data:
                return ConfigValidationResult(
                    is_valid=False,
                    errors=[f"Configuration {config_name} not found"],
                    validation_level=ConfigValidationLevel.BASIC,
                    timestamp=self._get_timestamp()
                )
            
            metadata = self.metadata.get(config_name)
            validation_level = metadata.validation_level if metadata else ConfigValidationLevel.BASIC
            
            errors = []
            warnings = []
            
            # Basic validation
            if not isinstance(config_data, dict):
                errors.append("Configuration must be a dictionary")
            
            # Type-specific validation based on config name
            if "ai" in config_name.lower():
                errors.extend(self._validate_ai_config(config_data))
            elif "fsm" in config_name.lower():
                errors.extend(self._validate_fsm_config(config_data))
            elif "performance" in config_name.lower():
                errors.extend(self._validate_performance_config(config_data))
            elif "quality" in config_name.lower():
                errors.extend(self._validate_quality_config(config_data))
            elif "messaging" in config_name.lower():
                errors.extend(self._validate_messaging_config(config_data))
            elif "testing" in config_name.lower():
                errors.extend(self._validate_testing_config(config_data))
            elif "network" in config_name.lower():
                errors.extend(self._validate_network_config(config_data))
            elif "security" in config_name.lower():
                errors.extend(self._validate_security_config(config_data))
            elif "database" in config_name.lower():
                errors.extend(self._validate_database_config(config_data))
            elif "logging" in config_name.lower():
                errors.extend(self._validate_logging_config(config_data))
            
            is_valid = len(errors) == 0
            
            return ConfigValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                validation_level=validation_level,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            return ConfigValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                validation_level=ConfigValidationLevel.BASIC,
                timestamp=self._get_timestamp()
            )
    
    def _get_config_file_path(self, config_name: str, format_type: ConfigFormat) -> Path:
        """Get configuration file path for given format."""
        if format_type == ConfigFormat.JSON:
            return self.config_dir / f"{config_name}.json"
        elif format_type == ConfigFormat.YAML:
            return self.config_dir / f"{config_name}.yaml"
        elif format_type == ConfigFormat.INI:
            return self.config_dir / f"{config_name}.ini"
        elif format_type == ConfigFormat.PYTHON:
            return self.config_dir / f"{config_name}.py"
        else:
            return self.config_dir / f"{config_name}.json"
    
    def _load_file(self, file_path: Path, format_type: ConfigFormat) -> Optional[Dict[str, Any]]:
        """Load configuration from file based on format."""
        try:
            if format_type == ConfigFormat.JSON:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif format_type == ConfigFormat.YAML:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            elif format_type == ConfigFormat.INI:
                import configparser
                config = configparser.ConfigParser()
                config.read(file_path)
                return {section: dict(config[section]) for section in config.sections()}
            elif format_type == ConfigFormat.PYTHON:
                import importlib.util
                spec = importlib.util.spec_from_file_location("config_module", file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return {key: value for key, value in module.__dict__.items() 
                       if not key.startswith('_') and not callable(value)}
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error loading file {file_path}: {e}")
            return None
    
    def _save_file(self, file_path: Path, config_data: Any, format_type: ConfigFormat) -> bool:
        """Save configuration to file based on format."""
        try:
            if format_type == ConfigFormat.JSON:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            elif format_type == ConfigFormat.YAML:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            elif format_type == ConfigFormat.INI:
                import configparser
                config = configparser.ConfigParser()
                if isinstance(config_data, dict):
                    for section, data in config_data.items():
                        config[section] = data
                with open(file_path, 'w', encoding='utf-8') as f:
                    config.write(f)
            elif format_type == ConfigFormat.PYTHON:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# Configuration file - Auto-generated\n\n")
                    for key, value in config_data.items():
                        if isinstance(value, str):
                            f.write(f'{key} = "{value}"\n')
                        else:
                            f.write(f'{key} = {value}\n')
            else:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving file {file_path}: {e}")
            return False
    
    def _get_file_timestamp(self, file_path: Path) -> str:
        """Get file modification timestamp."""
        try:
            stat = file_path.stat()
            return str(stat.st_mtime)
        except Exception:
            return ""
    
    # Validation methods for different configuration types
    def _validate_ai_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate AI configuration."""
        errors = []
        if "api_keys" in config_data and not isinstance(config_data["api_keys"], dict):
            errors.append("api_keys must be a dictionary")
        if "model_timeout" in config_data and not isinstance(config_data["model_timeout"], (int, float)):
            errors.append("model_timeout must be a number")
        return errors
    
    def _validate_fsm_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate FSM configuration."""
        errors = []
        if "timeout" in config_data and not isinstance(config_data["timeout"], (int, float)):
            errors.append("timeout must be a number")
        if "max_states" in config_data and not isinstance(config_data["max_states"], int):
            errors.append("max_states must be an integer")
        return errors
    
    def _validate_performance_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate performance configuration."""
        errors = []
        if "max_workers" in config_data and not isinstance(config_data["max_workers"], int):
            errors.append("max_workers must be an integer")
        if "cache_size" in config_data and not isinstance(config_data["cache_size"], int):
            errors.append("cache_size must be an integer")
        return errors
    
    def _validate_quality_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate quality configuration."""
        errors = []
        if "coverage_threshold" in config_data and not isinstance(config_data["coverage_threshold"], (int, float)):
            errors.append("coverage_threshold must be a number")
        if "check_interval" in config_data and not isinstance(config_data["check_interval"], (int, float)):
            errors.append("check_interval must be a number")
        return errors
    
    def _validate_messaging_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate messaging configuration."""
        errors = []
        if "agent_count" in config_data and not isinstance(config_data["agent_count"], int):
            errors.append("agent_count must be an integer")
        if "message_timeout" in config_data and not isinstance(config_data["message_timeout"], (int, float)):
            errors.append("message_timeout must be a number")
        return errors
    
    def _validate_testing_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate testing configuration."""
        errors = []
        if "timeout" in config_data and not isinstance(config_data["timeout"], (int, float)):
            errors.append("timeout must be a number")
        if "coverage_min_percent" in config_data and not isinstance(config_data["coverage_min_percent"], (int, float)):
            errors.append("coverage_min_percent must be a number")
        return errors
    
    def _validate_network_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate network configuration."""
        errors = []
        if "port" in config_data and not isinstance(config_data["port"], int):
            errors.append("port must be an integer")
        if "max_connections" in config_data and not isinstance(config_data["max_connections"], int):
            errors.append("max_connections must be an integer")
        return errors
    
    def _validate_security_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate security configuration."""
        errors = []
        if "max_login_attempts" in config_data and not isinstance(config_data["max_login_attempts"], int):
            errors.append("max_login_attempts must be an integer")
        if "session_timeout" in config_data and not isinstance(config_data["session_timeout"], (int, float)):
            errors.append("session_timeout must be a number")
        return errors
    
    def _validate_database_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate database configuration."""
        errors = []
        if "port" in config_data and not isinstance(config_data["port"], int):
            errors.append("port must be an integer")
        if "pool_size" in config_data and not isinstance(config_data["pool_size"], int):
            errors.append("pool_size must be an integer")
        return errors
    
    def _validate_logging_config(self, config_data: Dict[str, Any]) -> List[str]:
        """Validate logging configuration."""
        errors = []
        if "file_size" in config_data and not isinstance(config_data["file_size"], int):
            errors.append("file_size must be an integer")
        if "backup_count" in config_data and not isinstance(config_data["backup_count"], int):
            errors.append("backup_count must be an integer")
        return errors


# ============================================================================
# CONFIGURATION FACTORY
# ============================================================================

class ConfigurationFactory:
    """Factory for creating configuration instances."""
    
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
