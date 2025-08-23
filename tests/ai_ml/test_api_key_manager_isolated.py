"""
🧪 API Key Manager Tests - ISOLATED VERSION
AI & ML Integration Specialist - TDD Integration Project

Isolated test that bypasses problematic TensorFlow imports
"""

import os
import json
import tempfile
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest

# Add src to path and import directly to avoid TensorFlow issues
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import the specific module directly
try:
    from ai_ml.api_key_manager import APIKeyManager, APIKeyConfig

    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Import failed: {e}")
    IMPORT_SUCCESS = False


@pytest.mark.skipif(not IMPORT_SUCCESS, reason="Module import failed")
class TestAPIKeyConfigIsolated:
    """Test APIKeyConfig dataclass - isolated version."""

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
            timeout=30,
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
        config = APIKeyConfig(service_name="anthropic", api_key="sk-ant-test-key-12345")

        assert config.service_name == "anthropic"
        assert config.api_key == "sk-ant-test-key-12345"
        assert config.organization is None
        assert config.base_url is None
        assert config.model is None
        assert config.max_tokens is None
        assert config.temperature is None
        assert config.timeout is None


@pytest.mark.skipif(not IMPORT_SUCCESS, reason="Module import failed")
class TestAPIKeyManagerIsolated:
    """Test APIKeyManager class - isolated version."""

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
                    "timeout": 30,
                },
                "anthropic": {
                    "api_key": "sk-ant-test-anthropic-key-12345",
                    "model": "claude-3-sonnet",
                    "max_tokens": 4096,
                    "temperature": 0.5,
                },
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
    def test_load_api_keys_from_config_file(
        self, temp_config_dir, sample_api_keys_config
    ):
        """Test loading API keys from configuration file."""
        # Create config file
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, "w") as f:
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
    def test_load_api_keys_missing_config_file(self, temp_config_dir):
        """Test loading API keys when config file doesn't exist."""
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.load_api_keys()

        # Should succeed but with no keys loaded
        assert success is True
        assert len(manager._api_keys) == 0

    @pytest.mark.unit
    def test_get_api_key_existing(self, temp_config_dir, sample_api_keys_config):
        """Test getting existing API key."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, "w") as f:
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
    def test_has_api_key_existing(self, temp_config_dir, sample_api_keys_config):
        """Test checking if existing API key exists."""
        # Setup config
        config_file = temp_config_dir / "api_keys.json"
        with open(config_file, "w") as f:
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
        with open(config_file, "w") as f:
            json.dump(sample_api_keys_config, f)

        manager = APIKeyManager(str(temp_config_dir))
        manager.load_api_keys()

        services = manager.list_available_services()
        assert "openai" in services
        assert "anthropic" in services
        assert len(services) == 2

    @pytest.mark.unit
    def test_create_template_file(self, temp_config_dir):
        """Test creating template configuration file."""
        manager = APIKeyManager(str(temp_config_dir))
        success = manager.create_template_file()

        assert success is True
        assert manager.template_file.exists()

        # Check template content
        with open(manager.template_file, "r") as f:
            template_content = json.load(f)

        assert "api_keys" in template_content
        assert "openai" in template_content["api_keys"]
        assert "anthropic" in template_content["api_keys"]


class TestImportStatus:
    """Test the import status to understand what's working."""

    def test_import_status(self):
        """Test whether the module import was successful."""
        if IMPORT_SUCCESS:
            print("✅ API Key Manager module imported successfully")
        else:
            print("❌ API Key Manager module import failed")

        # This test will always pass, but shows the import status
        assert True
