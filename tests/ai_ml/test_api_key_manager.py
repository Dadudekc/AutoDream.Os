"""
🧪 API Key Manager Tests
AI & ML Integration Specialist - TDD Integration Project

Test-Driven Development implementation for API Key Manager module
"""

import os
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest

from src.ai_ml.api_key_manager import APIKeyManager, APIKeyConfig


class TestAPIKeyConfig:
    """Test APIKeyConfig dataclass."""
    
    @pytest.mark.unit
    def test_api_key_config_creation(self):
        """Test creating APIKeyConfig with all parameters."""
        config = APIKeyConfig(
            service_name="openai",
            api_key="sk-test-key-12345",
            organization="test-org",
            base_url="https://api.openai.com/v1",
            model="gpt-4",
            max_tokens=4096,
            temperature=0.7,
            timeout=30
        )
        
        assert config.service_name == "openai"
        assert config.api_key == "sk-test-key-12345"
        assert config.organization == "test-org"
        assert config.base_url == "https://api.openai.com/v1"
        assert config.model == "gpt-4"
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.timeout == 30
    
    @pytest.mark.unit
    def test_api_key_config_minimal(self):
        """Test creating APIKeyConfig with minimal parameters."""
        config = APIKeyConfig(
            service_name="anthropic",
            api_key="sk-ant-test-key-12345"
        )
        
        assert config.service_name == "anthropic"
        assert config.api_key == "sk-ant-test-key-12345"
        assert config.organization is None
        assert config.base_url is None
        assert config.model is None
        assert config.max_tokens is None
        assert config.temperature is None
        assert config.timeout is None


class TestAPIKeyManager:
    """Test APIKeyManager class."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        import shutil
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_api_keys_config(self):
        """Sample API keys configuration."""
        return {
            "api_keys": {
                "openai": {
                    "api_key": "sk-test-openai-key-12345",
                    "organization": "test-org",
                    "base_url": "https://api.openai.com/v1",
                    "model": "gpt-4",
                    "max_tokens": 4096,
                    "temperature": 0.7,
                    "timeout": 30
                },
                "anthropic": {
                    "api_key": "sk-ant-test-anthropic-key-12345",
                    "model": "claude-3-sonnet",
                    "max_tokens": 4096,
                    "temperature": 0.5
                }
            }
        }
    
    @pytest.mark.unit
    def test_api_key_manager_initialization(self, temp_config_dir):
        """Test APIKeyManager initialization."""
        manager = APIKeyManager(str(temp_config_dir))
        
        assert manager.config_dir == temp_config_dir
        assert manager.api_keys_file == temp_config_dir / "api_keys.json"
        assert manager.template_file == temp_config_dir / "api_keys.template.json"
        assert not manager._loaded
        assert manager._api_keys == {}
    
    @pytest.mark.unit
    def test_load_api_keys_from_config_file(self, temp_config_dir, sample_api_keys_config):
        """Test loading API keys from configuration file."""
        # Create config file
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(sample_api_keys_config, f)
        
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.load_api_keys()
        
        assert success is True
        assert manager._loaded is True
        assert len(manager._api_keys) == 2
        
        # Check OpenAI config
        openai_config = manager._api_keys["openai"]
        assert openai_config.service_name == "openai"
        assert openai_config.api_key == "sk-test-openai-key-12345"
        assert openai_config.organization == "test-org"
        assert openai_config.model == "gpt-4"
        
        # Check Anthropic config
        anthropic_config = manager._api_keys["anthropic"]
        assert anthropic_config.service_name == "anthropic"
        assert anthropic_config.api_key == "sk-ant-test-anthropic-key-12345"
        assert anthropic_config.model == "claude-3-sonnet"
    
    @pytest.mark.unit
    def test_load_api_keys_from_environment(self, temp_config_dir):
        """Test loading API keys from environment variables."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "sk-env-openai-key-12345",
            "OPENAI_ORGANIZATION": "env-test-org",
            "ANTHROPIC_API_KEY": "sk-ant-env-key-12345"
        }):
            manager = APIKeyManager(str(temp_config_dir))
            success = manager.load_api_keys()
            
            assert success is True
            assert len(manager._api_keys) >= 2
            
            # Check environment-loaded keys
            openai_key = manager._api_keys.get("openai")
            if openai_key:
                assert openai_key.api_key == "sk-env-openai-key-12345"
                assert openai_key.organization == "env-test-org"
    
    @pytest.mark.unit
    def test_load_api_keys_missing_config_file(self, temp_config_dir):
        """Test loading API keys when config file doesn't exist."""
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.load_api_keys()
        
        # Should succeed but with no keys loaded
        assert success is True
        assert len(manager._api_keys) == 0
    
    @pytest.mark.unit
    def test_load_api_keys_invalid_config_file(self, temp_config_dir):
        """Test loading API keys from invalid config file."""
        # Create invalid JSON file
        config_file = temp_config_dir / "api_keys.json"
        config_file.write_text("invalid json content")
        
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.load_api_keys()
        
        # Should succeed but with no keys loaded due to error
        assert success is True
        assert len(manager._api_keys) == 0
    
    @pytest.mark.unit
    def test_get_api_key_existing(self, temp_config_dir, sample_api_keys_config):
        """Test getting existing API key."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(sample_api_keys_config, f)
        
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        # Get OpenAI key
        openai_key = manager.get_api_key("openai")
        assert openai_key == "sk-test-openai-key-12345"
        
        # Get Anthropic key
        anthropic_key = manager.get_api_key("anthropic")
        assert anthropic_key == "sk-ant-test-anthropic-key-12345"
    
    @pytest.mark.unit
    def test_get_api_key_nonexistent(self, temp_config_dir):
        """Test getting non-existent API key."""
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        # Try to get non-existent key
        key = manager.get_api_key("nonexistent")
        assert key is None
    
    @pytest.mark.unit
    def test_get_api_config_existing(self, temp_config_dir, sample_api_keys_config):
        """Test getting existing API configuration."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(sample_api_keys_config, f)
        
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        # Get OpenAI config
        openai_config = manager.get_api_config("openai")
        assert openai_config is not None
        assert openai_config.service_name == "openai"
        assert openai_config.api_key == "sk-test-openai-key-12345"
        assert openai_config.organization == "test-org"
    
    @pytest.mark.unit
    def test_get_api_config_nonexistent(self, temp_config_dir):
        """Test getting non-existent API configuration."""
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        # Try to get non-existent config
        config = manager.get_api_config("nonexistent")
        assert config is None
    
    @pytest.mark.unit
    def test_has_api_key_existing(self, temp_config_dir, sample_api_keys_config):
        """Test checking if existing API key exists."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(sample_api_keys_config, f)
        
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        assert manager.has_api_key("openai") is True
        assert manager.has_api_key("anthropic") is True
    
    @pytest.mark.unit
    def test_has_api_key_nonexistent(self, temp_config_dir):
        """Test checking if non-existent API key exists."""
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        assert manager.has_api_key("nonexistent") is False
    
    @pytest.mark.unit
    def test_list_available_services(self, temp_config_dir, sample_api_keys_config):
        """Test listing available API services."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(sample_api_keys_config, f)
        
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        services = manager.list_available_services()
        assert "openai" in services
        assert "anthropic" in services
        assert len(services) == 2
    
    @pytest.mark.unit
    def test_list_available_services_empty(self, temp_config_dir):
        """Test listing available services when none exist."""
        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()
        
        services = manager.list_available_services()
        assert services == []
    
    @pytest.mark.unit
    def test_create_template_file(self, temp_config_dir):
        """Test creating template configuration file."""
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.create_template_file()
        
        assert success is True
        assert manager.template_file.exists()
        
        # Check template content
        with open(manager.template_file, 'r') as f:
            template_content = json.load(f)
        
        assert "api_keys" in template_content
        assert "openai" in template_content["api_keys"]
        assert "anthropic" in template_content["api_keys"]
    
    @pytest.mark.unit
    def test_create_template_file_already_exists(self, temp_config_dir):
        """Test creating template file when it already exists."""
        manager = APIKeyManager(str(temp_config_dir))
        
        # Create template first time
        success1 = manager.create_template_file()
        assert success1 is True
        
        # Try to create again
        success2 = manager.create_template_file()
        assert success2 is True  # Should still succeed
    
    @pytest.mark.unit
    def test_validate_api_key_format_valid(self):
        """Test validating valid API key formats."""
        manager = APIKeyManager()
        
        # Valid OpenAI key
        assert manager._validate_api_key_format("sk-test-key-12345", "openai") is True
        
        # Valid Anthropic key
        assert manager._validate_api_key_format("sk-ant-test-key-12345", "anthropic") is True
        
        # Valid HuggingFace key
        assert manager._validate_api_key_format("hf-test-key-12345", "huggingface") is True
    
    @pytest.mark.unit
    def test_validate_api_key_format_invalid(self):
        """Test validating invalid API key formats."""
        manager = APIKeyManager()
        
        # Invalid OpenAI key
        assert manager._validate_api_key_format("invalid-key", "openai") is False
        
        # Invalid Anthropic key
        assert manager._validate_api_key_format("invalid-key", "anthropic") is False
        
        # Invalid HuggingFace key
        assert manager._validate_api_key_format("invalid-key", "huggingface") is False
    
    @pytest.mark.unit
    def test_validate_api_key_format_unknown_service(self):
        """Test validating API key for unknown service."""
        manager = APIKeyManager()
        
        # Unknown service should return True (no validation)
        assert manager._validate_api_key_format("any-key", "unknown_service") is True


class TestAPIKeyManagerIntegration:
    """Integration tests for APIKeyManager."""
    
    @pytest.mark.integration
    def test_full_workflow(self, temp_config_dir):
        """Test complete API key management workflow."""
        manager = APIKeyManager(str(temp_config_dir))
        
        # 1. Create template
        assert manager.create_template_file() is True
        
        # 2. Load keys (should be empty initially)
        assert manager.load_api_keys() is True
        assert len(manager._api_keys) == 0
        
        # 3. Add keys manually
        manager._api_keys["test_service"] = APIKeyConfig(
            service_name="test_service",
            api_key="test-key-12345"
        )
        
        # 4. Verify key exists
        assert manager.has_api_key("test_service") is True
        assert manager.get_api_key("test_service") == "test-key-12345"
        
        # 5. List services
        services = manager.list_available_services()
        assert "test_service" in services
    
    @pytest.mark.integration
    def test_environment_override(self, temp_config_dir):
        """Test that environment variables override config file."""
        # Create config file with one key
        config_data = {
            "api_keys": {
                "openai": {
                    "api_key": "sk-config-file-key-12345"
                }
            }
        }
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        # Set environment variable with different key
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-env-override-key-12345"}):
            manager = APIKeyManager(str(temp_config_dir))
            manager.load_api_keys()
            
            # Environment should override config file
            openai_key = manager.get_api_key("openai")
            assert openai_key == "sk-env-override-key-12345"


class TestAPIKeyManagerSecurity:
    """Security tests for APIKeyManager."""
    
    @pytest.mark.security
    def test_api_key_not_logged(self, temp_config_dir, caplog):
        """Test that API keys are not logged."""
        manager = APIKeyManager(str(temp_config_dir))
        
        # Add a key
        manager._api_keys["test_service"] = APIKeyConfig(
            service_name="test_service",
            api_key="sk-secret-key-12345"
        )
        
        # Perform operations that might log
        manager.has_api_key("test_service")
        manager.get_api_key("test_service")
        
        # Check that secret key is not in logs
        log_text = caplog.text
        assert "sk-secret-key-12345" not in log_text
    
    @pytest.mark.security
    def test_template_file_no_real_keys(self, temp_config_dir):
        """Test that template file doesn't contain real API keys."""
        manager = APIKeyManager(str(temp_config_dir))
        manager.create_template_file()
        
        # Check template content
        with open(manager.template_file, 'r') as f:
            template_content = json.load(f)
        
        # Template should contain placeholder values, not real keys
        openai_config = template_content["api_keys"]["openai"]
        assert "your_openai_api_key_here" in openai_config["api_key"]
        
        anthropic_config = template_content["api_keys"]["anthropic"]
        assert "your_anthropic_api_key_here" in anthropic_config["api_key"]
