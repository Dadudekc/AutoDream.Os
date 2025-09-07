import pytest


class SimpleNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []

    def execute(self):
        return self.name


@pytest.fixture
def behavior_tree():
    """Provide a minimal behavior tree for testing."""
    child = SimpleNode("child")
    root = SimpleNode("root", [child])
    return root
