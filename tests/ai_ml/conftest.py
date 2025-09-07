"""
🧪 AI/ML Test Configuration
AI & ML Integration Specialist - TDD Integration Project

AI/ML specific test fixtures, mock data, and configuration
"""

import os
import sys
import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Generator, Optional
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

import pytest
from pytest import FixtureRequest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# AI/ML Test Configuration
AI_ML_TEST_CONFIG = {
    "test_timeout": 60,  # ML operations can take longer
    "coverage_threshold": 90,  # High coverage for AI/ML modules
    "max_test_duration": 120,  # Allow longer tests for ML operations
    "mock_api_responses": True,  # Use mock responses for API calls
    "test_data_size": "small",  # Use small datasets for testing
}

# Mock AI/ML Data
MOCK_AI_MODELS = {
    "gpt-4": {
        "name": "GPT-4",
        "provider": "openai",
        "model_id": "gpt-4",
        "version": "latest",
        "capabilities": ["text-generation", "code-generation", "analysis"],
        "parameters": {"max_tokens": 4096, "temperature": 0.7},
    },
    "claude-3": {
        "name": "Claude 3",
        "provider": "anthropic",
        "model_id": "claude-3-sonnet",
        "version": "2024",
        "capabilities": ["text-generation", "code-generation", "reasoning"],
        "parameters": {"max_tokens": 4096, "temperature": 0.5},
    },
}

MOCK_ML_WORKFLOWS = {
    "text_classification": {
        "name": "Text Classification Pipeline",
        "description": "Classify text using pre-trained models",
        "steps": [
            {
                "name": "data_preprocessing",
                "type": "preprocessing",
                "status": "pending",
            },
            {"name": "model_loading", "type": "model", "status": "pending"},
            {"name": "prediction", "type": "inference", "status": "pending"},
        ],
    }
}



@pytest.fixture(scope="session")
def ai_ml_test_config() -> Dict[str, Any]:
    """Provide AI/ML test configuration."""
    return AI_ML_TEST_CONFIG.copy()


@pytest.fixture(scope="session")
def mock_ai_models() -> Dict[str, Any]:
    """Provide mock AI model configurations."""
    return MOCK_AI_MODELS.copy()


@pytest.fixture(scope="session")
def mock_ml_workflows() -> Dict[str, Any]:
    """Provide mock ML workflow definitions."""
    return MOCK_ML_WORKFLOWS.copy()


def mock_openai_client() -> Generator[Mock, None, None]:
    """Provide mock OpenAI client."""
    with patch("openai.OpenAI") as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Mock chat completion response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mock AI response"
        mock_instance.chat.completions.create.return_value = mock_response

        yield mock_instance


@pytest.fixture(scope="function")
def mock_anthropic_client() -> Generator[Mock, None, None]:
    """Provide mock Anthropic client."""
    with patch("anthropic.Anthropic") as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        # Mock message response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Mock Claude response"
        mock_instance.messages.create.return_value = mock_response

        yield mock_instance


@pytest.fixture(scope="function")
def mock_api_keys() -> Generator[Dict[str, str], None, None]:
    """Provide mock API keys for testing."""
    return {
        "openai": "sk-test-openai-key-12345",
        "anthropic": "sk-ant-test-anthropic-key-12345",
        "huggingface": "hf-test-huggingface-key-12345",
    }


@pytest.fixture(scope="function")
def mock_ml_framework() -> Generator[Mock, None, None]:
    """Provide mock ML framework for testing."""
    with patch("torch") as mock_torch:
        mock_torch.__version__ = "2.0.0"
        mock_torch.cuda.is_available.return_value = False
        mock_torch.device.return_value = "cpu"
        yield mock_torch


