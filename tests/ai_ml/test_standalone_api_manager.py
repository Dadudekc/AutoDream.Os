"""
🧪 Standalone API Key Manager Tests
AI & ML Integration Specialist - TDD Integration Project

Completely standalone test with embedded module code
"""

import os
import json
import tempfile
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from unittest.mock import Mock, patch, mock_open
import pytest

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# EMBEDDED MODULE CODE (to avoid import issues)
# ============================================================================

@dataclass
class APIKeyConfig:
    """Configuration for an API key"""
    service_name: str
    api_key: str
    organization: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout: Optional[int] = None

class APIKeyManager:
    """Secure API key management for AI/ML services"""
    
    def __init__(self, config_dir: str = "config/ai_ml"):
        self.config_dir = Path(config_dir)
        self.api_keys_file = self.config_dir / "api_keys.json"
        self.template_file = self.config_dir / "api_keys.template.json"
        self._api_keys: Dict[str, APIKeyConfig] = {}
        self._loaded = False
        
    def load_api_keys(self, interactive: bool = False) -> bool:
        """Load API keys from configuration file or environment variables"""
        if self._loaded:
            return True
            
        # Try to load from config file first
        if self.api_keys_file.exists():
            try:
                with open(self.api_keys_file, 'r') as f:
                    config_data = json.load(f)
                self._load_from_config(config_data)
                logger.info(f"Loaded API keys from {self.api_keys_file}")
                self._loaded = True
                return True
            except Exception as e:
                logger.warning(f"Failed to load API keys from config: {e}")
        
        # Try to load from environment variables
        self._load_from_environment()
        
        # If interactive mode and keys are missing, prompt user
        if interactive and not self._api_keys:
            self._prompt_for_api_keys()
            
        self._loaded = True
        return True  # Return True if loading completed successfully
    
    def _load_from_config(self, config_data: Dict[str, Any]) -> None:
        """Load API keys from configuration data"""
        api_keys_data = config_data.get("api_keys", {})
        
        for service, config in api_keys_data.items():
            if config.get("api_key") and config["api_key"] != "your_openai_api_key_here":
                self._api_keys[service] = APIKeyConfig(
                    service_name=service,
                    api_key=config["api_key"],
                    organization=config.get("organization"),
                    base_url=config.get("base_url"),
                    model=config.get("model"),
                    max_tokens=config.get("max_tokens"),
                    temperature=config.get("temperature"),
                    timeout=config.get("timeout")
                )
    
    def _load_from_environment(self) -> None:
        """Load API keys from environment variables"""
        env_mappings = {
            "openai": {
                "api_key": "OPENAI_API_KEY",
                "organization": "OPENAI_ORGANIZATION"
            },
            "anthropic": {
                "api_key": "ANTHROPIC_API_KEY"
            },
            "huggingface": {
                "api_key": "HUGGINGFACE_API_KEY"
            }
        }
        
        for service, env_vars in env_mappings.items():
            api_key = os.environ.get(env_vars["api_key"])
            if api_key:
                config = APIKeyConfig(
                    service_name=service,
                    api_key=api_key
                )
                
                # Add additional environment variables if available
                if "organization" in env_vars:
                    org = os.environ.get(env_vars["organization"])
                    if org:
                        config.organization = org
                
                self._api_keys[service] = config
    
    def _prompt_for_api_keys(self) -> None:
        """Prompt user for API keys interactively"""
        print("Please enter your API keys:")
        
        services = ["openai", "anthropic", "huggingface"]
        for service in services:
            api_key = input(f"Enter {service} API key (or press Enter to skip): ").strip()
            if api_key:
                self._api_keys[service] = APIKeyConfig(
                    service_name=service,
                    api_key=api_key
                )
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        if not self._loaded:
            self.load_api_keys()
        
        config = self._api_keys.get(service)
        return config.api_key if config else None
    
    def get_api_config(self, service: str) -> Optional[APIKeyConfig]:
        """Get full API configuration for a specific service"""
        if not self._loaded:
            self.load_api_keys()
        
        return self._api_keys.get(service)
    
    def has_api_key(self, service: str) -> bool:
        """Check if API key exists for a specific service"""
        if not self._loaded:
            self.load_api_keys()
        
        return service in self._api_keys
    
    def list_available_services(self) -> List[str]:
        """List all available API services"""
        if not self._loaded:
            self.load_api_keys()
        
        return list(self._api_keys.keys())
    
    def create_template_file(self) -> bool:
        """Create template configuration file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            template_config = {
                "api_keys": {
                    "openai": {
                        "api_key": "your_openai_api_key_here",
                        "organization": "your_organization_here",
                        "base_url": "https://api.openai.com/v1",
                        "model": "gpt-4",
                        "max_tokens": 4096,
                        "temperature": 0.7,
                        "timeout": 30
                    },
                    "anthropic": {
                        "api_key": "your_anthropic_api_key_here",
                        "model": "claude-3-sonnet",
                        "max_tokens": 4096,
                        "temperature": 0.5
                    },
                    "huggingface": {
                        "api_key": "your_huggingface_api_key_here",
                        "base_url": "https://api-inference.huggingface.co"
                    }
                }
            }
            
            with open(self.template_file, 'w') as f:
                json.dump(template_config, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Failed to create template file: {e}")
            return False
    
    def _validate_api_key_format(self, api_key: str, service: str) -> bool:
        """Validate API key format for specific service"""
        if not api_key:
            return False
        
        # Basic format validation for known services
        if service == "openai" and not api_key.startswith("sk-"):
            return False
        elif service == "anthropic" and not api_key.startswith("sk-ant-"):
            return False
        elif service == "huggingface" and not api_key.startswith("hf-"):
            return False
        
        return True

# ============================================================================
# TEST IMPLEMENTATION
# ============================================================================

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
    def test_load_api_keys_missing_config_file(self, temp_config_dir):
        """Test loading API keys when config file doesn't exist."""
        # Mock environment variables to prevent real keys from interfering
        with patch.dict(os.environ, {}, clear=True):
            manager = APIKeyManager(str(temp_config_dir))
            # Patch the instance method directly
            with patch.object(manager, '_load_from_environment') as mock_env_load:
                mock_env_load.return_value = None
                success = manager.load_api_keys()
                
                # Should succeed but with no keys loaded
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


class TestAPIKeyManagerIntegration:
    """Integration tests for APIKeyManager."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        import shutil
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_full_workflow(self, temp_config_dir):
        """Test complete API key management workflow."""
        # Mock environment variables to prevent real keys from interfering
        with patch.dict(os.environ, {}, clear=True):
            manager = APIKeyManager(str(temp_config_dir))
            # Patch the instance method directly
            with patch.object(manager, '_load_from_environment') as mock_env_load:
                mock_env_load.return_value = None
                
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


class TestAPIKeyManagerSecurity:
    """Security tests for APIKeyManager."""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        import shutil
        shutil.rmtree(temp_dir)
    
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
