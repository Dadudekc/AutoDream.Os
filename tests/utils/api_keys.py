import pytest

from src.utils.stability_improvements import stability_manager, safe_import


@pytest.fixture
def set_api_keys(monkeypatch):
    """Set temporary API keys for tests."""
    def _set(openai=None, anthropic=None):
        if openai is not None:
            monkeypatch.setenv("OPENAI_API_KEY", openai)
        else:
            monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        if anthropic is not None:
            monkeypatch.setenv("ANTHROPIC_API_KEY", anthropic)
        else:
            monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return _set
