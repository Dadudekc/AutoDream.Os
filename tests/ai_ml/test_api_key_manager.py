"""Tests for the API key manager."""

import importlib.util

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

import pytest

# Import the module directly to avoid heavy package imports
spec = importlib.util.spec_from_file_location(
    "api_key_manager", Path(__file__).resolve().parents[2] / "src/ai_ml/api_key_manager.py"
)
api_key_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_key_manager)
APIKeyManager = api_key_manager.APIKeyManager

pytest_plugins = ["tests.utils.api_keys"]

VALID_OPENAI = "sk-" + "a" * 48
VALID_ANTHROPIC = "sk-ant-" + "b" * 32


@pytest.mark.unit
def test_get_key_returns_env_var(set_api_keys):
    set_api_keys(openai=VALID_OPENAI)
    manager = APIKeyManager()
    assert manager.get_key("openai") == VALID_OPENAI


@pytest.mark.unit
def test_get_key_invalid_format(set_api_keys):
    set_api_keys(openai="invalid")
    manager = APIKeyManager()
    assert manager.get_key("openai") is None


@pytest.mark.unit
def test_set_key_overrides_env(set_api_keys):
    set_api_keys()
    manager = APIKeyManager()
    assert manager.get_key("openai") is None
    assert manager.set_key("openai", VALID_OPENAI)
    assert manager.get_key("openai") == VALID_OPENAI


@pytest.mark.unit
def test_status_reports_availability(set_api_keys):
    set_api_keys(openai=VALID_OPENAI)
    manager = APIKeyManager()
    status = manager.get_status()
    assert status["openai_available"] is True
    assert status["anthropic_available"] is False


@pytest.mark.unit
def test_anthropic_key(set_api_keys):
    set_api_keys(anthropic=VALID_ANTHROPIC)
    manager = APIKeyManager()
    assert manager.get_key("anthropic") == VALID_ANTHROPIC


@pytest.mark.unit
def test_unknown_service_returns_none(set_api_keys):
    set_api_keys(openai=VALID_OPENAI)
    manager = APIKeyManager()
    assert manager.get_key("unknown") is None
