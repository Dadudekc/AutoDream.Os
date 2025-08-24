import pytest


class AgentNetwork:
    def __init__(self, agents: list[str]):
        self.agents = agents

    def broadcast(self, message: str) -> list[str]:
        return [f"{agent}:{message}" for agent in self.agents]


@pytest.fixture
def agent_network():
    """Provide a simple agent network for coordination tests."""
    return AgentNetwork(["agent_a", "agent_b"])
