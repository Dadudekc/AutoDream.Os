#!/usr/bin/env python3
"""
Test Suite for Unified Configuration Classes - Agent Cellphone V2
===============================================================

Comprehensive testing of the unified configuration classes system to ensure
all functionality works correctly and backward compatibility is maintained.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import unittest
import tempfile
import os
import json
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.core.configuration import (
    # Enums
    ConfigFormat,
    ConfigValidationLevel,
    ConfigType,
    
    # Base classes
    ConfigMetadata,
    ConfigSection,
    ConfigValidationResult,
    ConfigChangeEvent,
    UnifiedConfigurationManager,
    
    # Domain-specific configurations
    AIConfig,
    FSMConfig,
    PerformanceConfig,
    QualityConfig,
    MessagingConfig,
    TestingConfig,
    NetworkConfig,
    SecurityConfig,
    DatabaseConfig,
    LoggingConfig,
    
    # Managers
    FileBasedConfigurationManager,
    
    # Factory
    ConfigurationFactory,
    
    # Global instances
    CONFIG_FACTORY,
    FILE_CONFIG_MANAGER
)


# ============================================================================
# TEST CONFIGURATION ENUMS
# ============================================================================

class TestConfigurationEnums(unittest.TestCase):
    """Test configuration enumeration values."""
    
    def test_config_format_enum(self):
        """Test ConfigFormat enum values."""
        self.assertEqual(ConfigFormat.JSON.value, "json")
        self.assertEqual(ConfigFormat.YAML.value, "yaml")
        self.assertEqual(ConfigFormat.INI.value, "ini")
        self.assertEqual(ConfigFormat.PYTHON.value, "python")
        self.assertEqual(ConfigFormat.ENV.value, "env")
        self.assertEqual(ConfigFormat.AUTO.value, "auto")
    
    def test_config_validation_level_enum(self):
        """Test ConfigValidationLevel enum values."""
        self.assertEqual(ConfigValidationLevel.NONE.value, 0)
        self.assertEqual(ConfigValidationLevel.BASIC.value, 1)
        self.assertEqual(ConfigValidationLevel.STRICT.value, 2)
        self.assertEqual(ConfigValidationLevel.COMPREHENSIVE.value, 3)
    
    def test_config_type_enum(self):
        """Test ConfigType enum values."""
        self.assertEqual(ConfigType.GLOBAL.value, "global")
        self.assertEqual(ConfigType.SYSTEM.value, "system")
        self.assertEqual(ConfigType.SERVICE.value, "service")
        self.assertEqual(ConfigType.AGENT.value, "agent")
        self.assertEqual(ConfigType.MODULE.value, "module")
        self.assertEqual(ConfigType.USER.value, "user")
        self.assertEqual(ConfigType.ENVIRONMENT.value, "environment")
        self.assertEqual(ConfigType.CUSTOM.value, "custom")


# ============================================================================
# TEST CONFIGURATION BASE CLASSES
# ============================================================================

class TestConfigurationBaseClasses(unittest.TestCase):
    """Test configuration base classes functionality."""
    
    def test_config_metadata_creation(self):
        """Test ConfigMetadata dataclass creation."""
        metadata = ConfigMetadata(
            name="test_config",
            config_type=ConfigType.MODULE,
            format=ConfigFormat.JSON,
            source_path="/path/to/config.json",
            description="Test configuration",
            author="Test Author"
        )
        
        self.assertEqual(metadata.name, "test_config")
        self.assertEqual(metadata.config_type, ConfigType.MODULE)
        self.assertEqual(metadata.format, ConfigFormat.JSON)
        self.assertEqual(metadata.source_path, "/path/to/config.json")
        self.assertEqual(metadata.description, "Test configuration")
        self.assertEqual(metadata.author, "Test Author")
        self.assertEqual(metadata.validation_level, ConfigValidationLevel.BASIC)
        self.assertFalse(metadata.is_encrypted)
    
    def test_config_section_creation(self):
        """Test ConfigSection dataclass creation."""
        metadata = ConfigMetadata(
            name="test_section",
            config_type=ConfigType.MODULE,
            format=ConfigFormat.JSON
        )
        
        section = ConfigSection(
            name="test_section",
            data={"key": "value"},
            parent="parent_section",
            children=["child1", "child2"],
            metadata=metadata,
            is_override=True,
            override_source="environment"
        )
        
        self.assertEqual(section.name, "test_section")
        self.assertEqual(section.data, {"key": "value"})
        self.assertEqual(section.parent, "parent_section")
        self.assertEqual(section.children, ["child1", "child2"])
        self.assertEqual(section.metadata, metadata)
        self.assertTrue(section.is_override)
        self.assertEqual(section.override_source, "environment")
    
    def test_config_validation_result_creation(self):
        """Test ConfigValidationResult dataclass creation."""
        result = ConfigValidationResult(
            is_valid=True,
            errors=[],
            warnings=["Warning 1", "Warning 2"],
            validation_level=ConfigValidationLevel.STRICT,
            timestamp="2025-01-01T00:00:00",
            validator_version="2.0.0"
        )
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, ["Warning 1", "Warning 2"])
        self.assertEqual(result.validation_level, ConfigValidationLevel.STRICT)
        self.assertEqual(result.timestamp, "2025-01-01T00:00:00")
        self.assertEqual(result.validator_version, "2.0.0")
    
    def test_config_change_event_creation(self):
        """Test ConfigChangeEvent dataclass creation."""
        event = ConfigChangeEvent(
            config_name="test_config",
            change_type="update",
            old_value={"key": "old_value"},
            new_value={"key": "new_value"},
            timestamp="2025-01-01T00:00:00",
            user="test_user",
            source="test_source"
        )
        
        self.assertEqual(event.config_name, "test_config")
        self.assertEqual(event.change_type, "update")
        self.assertEqual(event.old_value, {"key": "old_value"})
        self.assertEqual(event.new_value, {"key": "new_value"})
        self.assertEqual(event.timestamp, "2025-01-01T00:00:00")
        self.assertEqual(event.user, "test_user")
        self.assertEqual(event.source, "test_source")


# ============================================================================
# TEST DOMAIN-SPECIFIC CONFIGURATION CLASSES
# ============================================================================

class TestDomainSpecificConfigurations(unittest.TestCase):
    """Test domain-specific configuration classes."""
    
    def test_ai_config_creation(self):
        """Test AIConfig creation and defaults."""
        ai_config = AIConfig()
        
        # Test default values
        self.assertEqual(ai_config.api_keys, {})
        self.assertEqual(ai_config.model_type, "gpt")
        self.assertEqual(ai_config.temperature, 0.7)
        self.assertEqual(ai_config.top_p, 1.0)
        self.assertTrue(ai_config.cache_enabled)
        
        # Test custom values
        custom_ai_config = AIConfig(
            api_keys={"openai": "key123"},
            model_type="claude",
            temperature=0.5
        )
        
        self.assertEqual(custom_ai_config.api_keys, {"openai": "key123"})
        self.assertEqual(custom_ai_config.model_type, "claude")
        self.assertEqual(custom_ai_config.temperature, 0.5)
    
    def test_fsm_config_creation(self):
        """Test FSMConfig creation and defaults."""
        fsm_config = FSMConfig()
        
        # Test default values
        self.assertTrue(fsm_config.auto_save)
        self.assertEqual(fsm_config.save_interval, 60.0)
        self.assertTrue(fsm_config.validation_enabled)
        self.assertFalse(fsm_config.strict_mode)
        self.assertTrue(fsm_config.persistence_enabled)
        
        # Test custom values
        custom_fsm_config = FSMConfig(
            timeout=120.0,
            max_states=500,
            strict_mode=True
        )
        
        self.assertEqual(custom_fsm_config.timeout, 120.0)
        self.assertEqual(custom_fsm_config.max_states, 500)
        self.assertTrue(custom_fsm_config.strict_mode)
    
    def test_performance_config_creation(self):
        """Test PerformanceConfig creation and defaults."""
        perf_config = PerformanceConfig()
        
        # Test default values
        self.assertEqual(perf_config.enable_profiling, False)
        self.assertEqual(perf_config.profiling_interval, 5.0)
        self.assertEqual(perf_config.memory_limit_mb, 1024)
        self.assertEqual(perf_config.cpu_limit_percent, 80)
        self.assertTrue(perf_config.enable_monitoring)
        
        # Test custom values
        custom_perf_config = PerformanceConfig(
            max_workers=16,
            cache_size=5000,
            enable_profiling=True,
            memory_limit_mb=2048
        )
        
        self.assertEqual(custom_perf_config.max_workers, 16)
        self.assertEqual(custom_perf_config.cache_size, 5000)
        self.assertTrue(custom_perf_config.enable_profiling)
        self.assertEqual(custom_perf_config.memory_limit_mb, 2048)
    
    def test_quality_config_creation(self):
        """Test QualityConfig creation and defaults."""
        quality_config = QualityConfig()
        
        # Test default values
        self.assertTrue(quality_config.alert_enabled)
        self.assertEqual(quality_config.alert_threshold, 0.8)
        self.assertFalse(quality_config.auto_fix_enabled)
        self.assertTrue(quality_config.quality_gates_enabled)
        self.assertTrue(quality_config.reporting_enabled)
        
        # Test custom values
        custom_quality_config = QualityConfig(
            coverage_threshold=90.0,
            alert_threshold=0.9,
            auto_fix_enabled=True
        )
        
        self.assertEqual(custom_quality_config.coverage_threshold, 90.0)
        self.assertEqual(custom_quality_config.alert_threshold, 0.9)
        self.assertTrue(custom_quality_config.auto_fix_enabled)
    
    def test_messaging_config_creation(self):
        """Test MessagingConfig creation and defaults."""
        msg_config = MessagingConfig()
        
        # Test default values
        self.assertFalse(msg_config.encryption_enabled)
        self.assertIsNone(msg_config.encryption_key)
        self.assertFalse(msg_config.compression_enabled)
        self.assertEqual(msg_config.queue_size, 1000)
        self.assertEqual(msg_config.priority_levels, 5)
        self.assertTrue(msg_config.dead_letter_queue)
        
        # Test custom values
        custom_msg_config = MessagingConfig(
            encryption_enabled=True,
            encryption_key="secret_key",
            queue_size=2000,
            priority_levels=10
        )
        
        self.assertTrue(custom_msg_config.encryption_enabled)
        self.assertEqual(custom_msg_config.encryption_key, "secret_key")
        self.assertEqual(custom_msg_config.queue_size, 2000)
        self.assertEqual(custom_msg_config.priority_levels, 10)
    
    def test_testing_config_creation(self):
        """Test TestingConfig creation and defaults."""
        test_config = TestingConfig()
        
        # Test default values
        self.assertEqual(test_config.test_discovery_pattern, "test_*.py")
        self.assertEqual(test_config.exclude_patterns, ["*_test.py", "test_*_*.py"])
        self.assertIsNone(test_config.random_seed)
        self.assertFalse(test_config.verbose_output)
        self.assertFalse(test_config.stop_on_failure)
        self.assertTrue(test_config.generate_reports)
        
        # Test custom values
        custom_test_config = TestingConfig(
            test_discovery_pattern="spec_*.py",
            exclude_patterns=["*_spec.py"],
            random_seed=42,
            verbose_output=True
        )
        
        self.assertEqual(custom_test_config.test_discovery_pattern, "spec_*.py")
        self.assertEqual(custom_test_config.exclude_patterns, ["*_spec.py"])
        self.assertEqual(custom_test_config.random_seed, 42)
        self.assertTrue(custom_test_config.verbose_output)
    
    def test_network_config_creation(self):
        """Test NetworkConfig creation and defaults."""
        net_config = NetworkConfig()
        
        # Test default values
        self.assertFalse(net_config.ssl_enabled)
        self.assertIsNone(net_config.ssl_cert_path)
        self.assertFalse(net_config.rate_limiting_enabled)
        self.assertEqual(net_config.rate_limit_requests, 100)
        self.assertFalse(net_config.cors_enabled)
        self.assertFalse(net_config.proxy_enabled)
        
        # Test custom values
        custom_net_config = NetworkConfig(
            ssl_enabled=True,
            ssl_cert_path="/path/to/cert.pem",
            rate_limiting_enabled=True,
            rate_limit_requests=200,
            cors_enabled=True
        )
        
        self.assertTrue(custom_net_config.ssl_enabled)
        self.assertEqual(custom_net_config.ssl_cert_path, "/path/to/cert.pem")
        self.assertTrue(custom_net_config.rate_limiting_enabled)
        self.assertEqual(custom_net_config.rate_limit_requests, 200)
        self.assertTrue(custom_net_config.cors_enabled)
    
    def test_security_config_creation(self):
        """Test SecurityConfig creation and defaults."""
        sec_config = SecurityConfig()
        
        # Test default values
        self.assertEqual(sec_config.password_min_length, 8)
        self.assertTrue(sec_config.password_require_special)
        self.assertTrue(sec_config.password_require_numbers)
        self.assertTrue(sec_config.password_require_uppercase)
        self.assertIsNone(sec_config.jwt_secret)
        self.assertEqual(sec_config.jwt_expiry_hours, 24)
        self.assertFalse(sec_config.mfa_enabled)
        self.assertTrue(sec_config.audit_logging_enabled)
        
        # Test custom values
        custom_sec_config = SecurityConfig(
            password_min_length=12,
            password_require_special=False,
            jwt_secret="secret_key",
            mfa_enabled=True,
            mfa_type="sms"
        )
        
        self.assertEqual(custom_sec_config.password_min_length, 12)
        self.assertFalse(custom_sec_config.password_require_special)
        self.assertEqual(custom_sec_config.jwt_secret, "secret_key")
        self.assertTrue(custom_sec_config.mfa_enabled)
        self.assertEqual(custom_sec_config.mfa_type, "sms")
    
    def test_database_config_creation(self):
        """Test DatabaseConfig creation and defaults."""
        db_config = DatabaseConfig()
        
        # Test default values
        self.assertEqual(db_config.ssl_mode, "prefer")
        self.assertIsNone(db_config.ssl_cert)
        self.assertEqual(db_config.connection_retries, 3)
        self.assertEqual(db_config.retry_delay, 1.0)
        self.assertFalse(db_config.enable_logging)
        self.assertFalse(db_config.log_queries)
        self.assertTrue(db_config.log_slow_queries)
        self.assertTrue(db_config.enable_pooling)
        
        # Test custom values
        custom_db_config = DatabaseConfig(
            ssl_mode="require",
            ssl_cert="/path/to/cert.pem",
            connection_retries=5,
            enable_logging=True,
            log_queries=True
        )
        
        self.assertEqual(custom_db_config.ssl_mode, "require")
        self.assertEqual(custom_db_config.ssl_cert, "/path/to/cert.pem")
        self.assertEqual(custom_db_config.connection_retries, 5)
        self.assertTrue(custom_db_config.enable_logging)
        self.assertTrue(custom_db_config.log_queries)
    
    def test_logging_config_creation(self):
        """Test LoggingConfig creation and defaults."""
        log_config = LoggingConfig()
        
        # Test default values
        self.assertTrue(log_config.file_enabled)
        self.assertTrue(log_config.console_enabled)
        self.assertFalse(log_config.syslog_enabled)
        self.assertEqual(log_config.syslog_port, 514)
        self.assertEqual(log_config.syslog_facility, "user")
        self.assertFalse(log_config.json_format)
        self.assertTrue(log_config.include_timestamp)
        self.assertTrue(log_config.enable_rotation)
        self.assertEqual(log_config.rotation_when, "midnight")
        
        # Test custom values
        custom_log_config = LoggingConfig(
            file_enabled=False,
            console_enabled=False,
            syslog_enabled=True,
            syslog_host="localhost",
            json_format=True,
            enable_rotation=False
        )
        
        self.assertFalse(custom_log_config.file_enabled)
        self.assertFalse(custom_log_config.console_enabled)
        self.assertTrue(custom_log_config.syslog_enabled)
        self.assertEqual(custom_log_config.syslog_host, "localhost")
        self.assertTrue(custom_log_config.json_format)
        self.assertFalse(custom_log_config.enable_rotation)


# ============================================================================
# TEST CONFIGURATION FACTORY
# ============================================================================

class TestConfigurationFactory(unittest.TestCase):
    """Test configuration factory functionality."""
    
    def test_create_ai_config(self):
        """Test creating AI configuration instances."""
        ai_config = CONFIG_FACTORY.create_ai_config(
            api_keys={"openai": "key123"},
            model_type="claude",
            temperature=0.5
        )
        
        self.assertIsInstance(ai_config, AIConfig)
        self.assertEqual(ai_config.api_keys, {"openai": "key123"})
        self.assertEqual(ai_config.model_type, "claude")
        self.assertEqual(ai_config.temperature, 0.5)
    
    def test_create_fsm_config(self):
        """Test creating FSM configuration instances."""
        fsm_config = CONFIG_FACTORY.create_fsm_config(
            timeout=120.0,
            max_states=500,
            strict_mode=True
        )
        
        self.assertIsInstance(fsm_config, FSMConfig)
        self.assertEqual(fsm_config.timeout, 120.0)
        self.assertEqual(fsm_config.max_states, 500)
        self.assertTrue(fsm_config.strict_mode)
    
    def test_create_performance_config(self):
        """Test creating performance configuration instances."""
        perf_config = CONFIG_FACTORY.create_performance_config(
            max_workers=16,
            cache_size=5000,
            enable_profiling=True
        )
        
        self.assertIsInstance(perf_config, PerformanceConfig)
        self.assertEqual(perf_config.max_workers, 16)
        self.assertEqual(perf_config.cache_size, 5000)
        self.assertTrue(perf_config.enable_profiling)
    
    def test_create_manager(self):
        """Test creating configuration manager instances."""
        manager = CONFIG_FACTORY.create_manager("file", config_dir="test_config")
        
        self.assertIsInstance(manager, FileBasedConfigurationManager)
        self.assertEqual(manager.config_dir, Path("test_config"))
    
    def test_create_manager_invalid_type(self):
        """Test creating configuration manager with invalid type."""
        with self.assertRaises(ValueError):
            CONFIG_FACTORY.create_manager("invalid_type")


# ============================================================================
# TEST FILE-BASED CONFIGURATION MANAGER
# ============================================================================

class TestFileBasedConfigurationManager(unittest.TestCase):
    """Test file-based configuration manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir)
        self.manager = FileBasedConfigurationManager(str(self.config_dir))
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        self.assertEqual(self.manager.config_dir, self.config_dir)
        self.assertEqual(self.manager.configs, {})
        self.assertEqual(self.manager.metadata, {})
        self.assertEqual(self.manager.validation_results, {})
        self.assertEqual(self.manager.change_history, [])
    
    def test_get_config_file_path(self):
        """Test getting configuration file paths for different formats."""
        json_path = self.manager._get_config_file_path("test", ConfigFormat.JSON)
        yaml_path = self.manager._get_config_file_path("test", ConfigFormat.YAML)
        ini_path = self.manager._get_config_file_path("test", ConfigFormat.INI)
        python_path = self.manager._get_config_file_path("test", ConfigFormat.PYTHON)
        
        self.assertEqual(json_path, self.config_dir / "test.json")
        self.assertEqual(yaml_path, self.config_dir / "test.yaml")
        self.assertEqual(ini_path, self.config_dir / "test.ini")
        self.assertEqual(python_path, self.config_dir / "test.py")
    
    def test_load_json_config(self):
        """Test loading JSON configuration."""
        config_data = {"key": "value", "number": 42}
        config_file = self.config_dir / "test.json"
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        success = self.manager.load_config("test", ConfigType.MODULE)
        
        self.assertTrue(success)
        self.assertEqual(self.manager.get_config("test"), config_data)
        self.assertIn("test", self.manager.metadata)
        self.assertIn("test", self.manager.validation_results)
    
    def test_load_yaml_config(self):
        """Test loading YAML configuration."""
        config_data = {"key": "value", "number": 42}
        config_file = self.config_dir / "test.yaml"
        
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        success = self.manager.load_config("test", ConfigType.MODULE)
        
        self.assertTrue(success)
        self.assertEqual(self.manager.get_config("test"), config_data)
    
    def test_load_nonexistent_config(self):
        """Test loading non-existent configuration."""
        success = self.manager.load_config("nonexistent", ConfigType.MODULE)
        
        self.assertFalse(success)
        self.assertNotIn("nonexistent", self.manager.configs)
    
    def test_save_config(self):
        """Test saving configuration."""
        # First load a config
        config_data = {"key": "value"}
        config_file = self.config_dir / "test.json"
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        self.manager.load_config("test", ConfigType.MODULE)
        
        # Modify and save
        new_data = {"key": "new_value", "new_key": "new_value"}
        success = self.manager.save_config("test", new_data)
        
        self.assertTrue(success)
        
        # Verify file was updated
        with open(config_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, new_data)
    
    def test_validate_config(self):
        """Test configuration validation."""
        # Load a valid config
        config_data = {"api_keys": {"openai": "key123"}, "model_timeout": 60.0}
        config_file = self.config_dir / "ai_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        self.manager.load_config("ai_config", ConfigType.MODULE)
        
        # Validate
        result = self.manager.validate_config("ai_config")
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])
    
    def test_validate_invalid_config(self):
        """Test validation of invalid configuration."""
        # Load an invalid config
        config_data = {"api_keys": "not_a_dict", "model_timeout": "not_a_number"}
        config_file = self.config_dir / "invalid_ai_config.json"
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        self.manager.load_config("invalid_ai_config", ConfigType.MODULE)
        
        # Validate
        result = self.manager.validate_config("invalid_ai_config")
        
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_set_and_get_config(self):
        """Test setting and getting configuration."""
        config_data = {"key": "value"}
        
        success = self.manager.set_config("test", config_data)
        
        self.assertTrue(success)
        self.assertEqual(self.manager.get_config("test"), config_data)
        self.assertEqual(len(self.manager.change_history), 1)
        
        # Check change event
        change_event = self.manager.change_history[0]
        self.assertEqual(change_event.config_name, "test")
        self.assertEqual(change_event.change_type, "create")
        self.assertEqual(change_event.new_value, config_data)
    
    def test_delete_config(self):
        """Test deleting configuration."""
        # First set a config
        config_data = {"key": "value"}
        self.manager.set_config("test", config_data)
        
        # Delete it
        success = self.manager.delete_config("test")
        
        self.assertTrue(success)
        self.assertNotIn("test", self.manager.configs)
        self.assertEqual(len(self.manager.change_history), 2)  # create + delete
        
        # Check delete change event
        delete_event = self.manager.change_history[1]
        self.assertEqual(delete_event.change_type, "delete")
        self.assertIsNone(delete_event.new_value)
    
    def test_list_configs(self):
        """Test listing configurations."""
        self.manager.set_config("config1", {"key1": "value1"})
        self.manager.set_config("config2", {"key2": "value2"})
        
        config_list = self.manager.list_configs()
        
        self.assertIn("config1", config_list)
        self.assertIn("config2", config_list)
        self.assertEqual(len(config_list), 2)
    
    def test_get_change_history(self):
        """Test getting change history."""
        self.manager.set_config("test", {"key": "value"})
        self.manager.set_config("test", {"key": "new_value"})
        self.manager.delete_config("test")
        
        # Get all history
        all_history = self.manager.get_change_history()
        self.assertEqual(len(all_history), 3)
        
        # Get history for specific config
        test_history = self.manager.get_change_history("test")
        self.assertEqual(len(test_history), 3)
        
        # Check change types
        change_types = [event.change_type for event in test_history]
        self.assertEqual(change_types, ["create", "update", "delete"])


# ============================================================================
# TEST ABSTRACT CONFIGURATION MANAGER
# ============================================================================

class TestUnifiedConfigurationManager(unittest.TestCase):
    """Test abstract configuration manager functionality."""
    
    def test_abstract_methods(self):
        """Test that abstract methods cannot be instantiated."""
        with self.assertRaises(TypeError):
            UnifiedConfigurationManager("config")
    
    def test_concrete_manager_inheritance(self):
        """Test that concrete manager properly inherits from abstract base."""
        manager = FileBasedConfigurationManager("config")
        
        self.assertIsInstance(manager, UnifiedConfigurationManager)
        self.assertTrue(hasattr(manager, 'load_config'))
        self.assertTrue(hasattr(manager, 'save_config'))
        self.assertTrue(hasattr(manager, 'validate_config'))


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestConfigurationEnums))
    test_suite.addTest(unittest.makeSuite(TestConfigurationBaseClasses))
    test_suite.addTest(unittest.makeSuite(TestDomainSpecificConfigurations))
    test_suite.addTest(unittest.makeSuite(TestConfigurationFactory))
    test_suite.addTest(unittest.makeSuite(TestFileBasedConfigurationManager))
    test_suite.addTest(unittest.makeSuite(TestUnifiedConfigurationManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"UNIFIED CONFIGURATION CLASSES TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    print(f"\n{'='*60}")
    
    # Exit with appropriate code
    exit(len(result.failures) + len(result.errors))
