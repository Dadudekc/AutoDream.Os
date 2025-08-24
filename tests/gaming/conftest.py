import pytest

@pytest.fixture(scope="module")
def game_environment():
    """Provide a shared game environment for gaming tests."""
    return {
        "skills": {"attack": 1, "defense": 1},
        "state": {"health": 100, "mana": 50},
        "anti_detection": {"stealth": True, "logging": False},
        "automation": {"enabled": True, "macro_slots": 3},
    }
