import pytest


class SimpleDecisionEngine:
    def decide(self, value: int) -> str:
        return "positive" if value > 0 else "non-positive"


@pytest.fixture
def decision_engine():
    """Provide a simple decision engine for tests."""
    return SimpleDecisionEngine()
