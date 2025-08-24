import pytest


class LearningAgent:
    def __init__(self):
        self.knowledge = 0

    def learn(self, value: int):
        self.knowledge += value


@pytest.fixture
def learning_agent():
    """Provide a simple learning agent."""
    return LearningAgent()
