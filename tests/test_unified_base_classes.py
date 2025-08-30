"""
Test Unified Base Classes

This test file verifies that our consolidated base classes work correctly
and can be imported without errors.
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

# Import our unified base classes
from src.core.base import BaseManager, BaseValidator, BaseConfig, BaseModel
from src.core.base.base_manager import ManagerConfig, ManagerType, ManagerState
from src.core.base.base_validator import ValidationConfig, ValidationType, ValidationRule, ValidationSeverity
from src.core.base.base_config import ConfigOptions, ConfigType
from src.core.base.base_model import ModelType, ModelStatus


class TestUnifiedBaseClasses(unittest.TestCase):
    """Test that unified base classes can be imported and instantiated."""
    
    def test_base_classes_importable(self):
        """Test that all base classes can be imported."""
        self.assertIsNotNone(BaseManager)
        self.assertIsNotNone(BaseValidator)
        self.assertIsNotNone(BaseConfig)
        self.assertIsNotNone(BaseModel)
    
    def test_manager_enums_importable(self):
        """Test that manager enums can be imported."""
        self.assertIsNotNone(ManagerConfig)
        self.assertIsNotNone(ManagerType)
        self.assertIsNotNone(ManagerState)
    
    def test_validator_enums_importable(self):
        """Test that validator enums can be imported."""
        self.assertIsNotNone(ValidationConfig)
        self.assertIsNotNone(ValidationType)
        self.assertIsNotNone(ValidationRule)
        self.assertIsNotNone(ValidationSeverity)
    
    def test_config_enums_importable(self):
        """Test that config enums can be imported."""
        self.assertIsNotNone(ConfigOptions)
        self.assertIsNotNone(ConfigType)
    
    def test_model_enums_importable(self):
        """Test that model enums can be imported."""
        self.assertIsNotNone(ModelType)
        self.assertIsNotNone(ModelStatus)
    
    def test_manager_config_creation(self):
        """Test that ManagerConfig can be created."""
        config = ManagerConfig(
            name="test_manager",
            manager_type=ManagerType.TASK
        )
        self.assertEqual(config.name, "test_manager")
        self.assertEqual(config.manager_type, ManagerType.TASK)
        self.assertTrue(config.enabled)
    
    def test_validation_config_creation(self):
        """Test that ValidationConfig can be created."""
        config = ValidationConfig(
            name="test_validator",
            validation_type=ValidationType.CONTRACT
        )
        self.assertEqual(config.name, "test_validator")
        self.assertEqual(config.validation_type, ValidationType.CONTRACT)
        self.assertTrue(config.enabled)
    
    def test_config_options_creation(self):
        """Test that ConfigOptions can be created."""
        options = ConfigOptions()
        self.assertTrue(options.auto_reload)
        self.assertEqual(options.reload_interval, 300.0)
        self.assertTrue(options.validate_on_load)
    
    def test_validation_rule_creation(self):
        """Test that ValidationRule can be created."""
        rule = ValidationRule(
            name="test_rule",
            description="Test validation rule",
            validation_type=ValidationType.CONTRACT,
            severity=ValidationSeverity.ERROR
        )
        self.assertEqual(rule.name, "test_rule")
        self.assertEqual(rule.description, "Test validation rule")
        self.assertEqual(rule.validation_type, ValidationType.CONTRACT)
        self.assertEqual(rule.severity, ValidationSeverity.ERROR)
        self.assertTrue(rule.enabled)


class TestBaseConfig(unittest.TestCase):
    """Test BaseConfig functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.json"
        
        # Create test configuration
        test_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "test_db"
            },
            "logging": {
                "level": "INFO",
                "format": "json"
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_base_config_abstract(self):
        """Test that BaseConfig is abstract and cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            BaseConfig()
    
    def test_base_config_with_concrete_implementation(self):
        """Test BaseConfig with a concrete implementation."""
        
        class TestConfig(BaseConfig):
            def _initialize_resources(self):
                pass
        
        config = TestConfig(config_path=self.config_file)
        self.assertIsNotNone(config)
        self.assertEqual(len(config.sections), 2)
        self.assertIn("database", config.sections)
        self.assertIn("logging", config.sections)
    
    def test_config_value_retrieval(self):
        """Test that configuration values can be retrieved."""
        
        class TestConfig(BaseConfig):
            def _initialize_resources(self):
                pass
        
        config = TestConfig(config_path=self.config_file)
        
        # Test getting values
        self.assertEqual(config.get_value("host", section="database"), "localhost")
        self.assertEqual(config.get_value("port", section="database"), 5432)
        self.assertEqual(config.get_value("level", section="logging"), "INFO")
        
        # Test default values
        self.assertEqual(config.get_value("nonexistent", default="default_value"), "default_value")
    
    def test_config_value_setting(self):
        """Test that configuration values can be set."""
        
        class TestConfig(BaseConfig):
            def _initialize_resources(self):
                pass
        
        config = TestConfig(config_path=self.config_file)
        
        # Test setting values
        config.set_value("timeout", 30, section="database")
        self.assertEqual(config.get_value("timeout", section="database"), 30)
        
        # Test setting values in new section
        config.set_value("enabled", True, section="features")
        self.assertTrue(config.get_value("enabled", section="features"))


class TestBaseModel(unittest.TestCase):
    """Test BaseModel functionality."""
    
    def test_base_model_abstract(self):
        """Test that BaseModel is abstract and cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            BaseModel()
    
    def test_base_model_with_concrete_implementation(self):
        """Test BaseModel with a concrete implementation."""
        
        class TestModel(BaseModel):
            name: str
            value: int
            
            def __init__(self, name: str, value: int, **kwargs):
                self.name = name
                self.value = value
                super().__init__(**kwargs)
            
            def _initialize_resources(self):
                pass
        
        model = TestModel(name="test", value=42)
        self.assertIsNotNone(model)
        self.assertEqual(model.name, "test")
        self.assertEqual(model.value, 42)
        self.assertTrue(model.is_valid())
    
    def test_model_validation(self):
        """Test that model validation works."""
        
        class TestModel(BaseModel):
            name: str
            value: int
            
            def __init__(self, name: str, value: int, **kwargs):
                self.name = name
                self.value = value
                super().__init__(**kwargs)
            
            def _initialize_resources(self):
                pass
        
        # Valid model
        model = TestModel(name="test", value=42)
        self.assertTrue(model.is_valid())
        
        # Invalid model (missing required field)
        with self.assertRaises(TypeError):
            TestModel(value=42)  # Missing name
    
    def test_model_serialization(self):
        """Test that models can be serialized to dict and JSON."""
        
        class TestModel(BaseModel):
            name: str
            value: int
            
            def __init__(self, name: str, value: int, **kwargs):
                self.name = name
                self.value = value
                super().__init__(**kwargs)
            
            def _initialize_resources(self):
                pass
        
        model = TestModel(name="test", value=42)
        
        # Test to_dict
        model_dict = model.to_dict()
        self.assertIn("name", model_dict)
        self.assertIn("value", model_dict)
        self.assertEqual(model_dict["name"], "test")
        self.assertEqual(model_dict["value"], 42)
        
        # Test to_json
        model_json = model.to_json()
        self.assertIsInstance(model_json, str)
        self.assertIn("test", model_json)
        self.assertIn("42", model_json)


if __name__ == "__main__":
    unittest.main()
