import pytest

from src.services.coordinator import (
    PyAutoGUIInterface,
    MessageQueueClient,
    CoordinationStrategy,
    CoordinatorOrchestrator,
)


class DummyGUI:
    def __init__(self) -> None:
        self.messages = []

    def write(self, text: str) -> None:
        self.messages.append(text)


@pytest.mark.smoke

def test_orchestrator_smoke():
    gui = DummyGUI()
    gui_interface = PyAutoGUIInterface(gui_module=gui)
    queue_client = MessageQueueClient()
    strategy = CoordinationStrategy(threshold=5)
    orchestrator = CoordinatorOrchestrator(gui_interface, queue_client, strategy)

    orchestrator.deliver("hi")
    assert queue_client.receive() == "hi"

    orchestrator.deliver("hello world")
    assert gui.messages == ["hello world"]
