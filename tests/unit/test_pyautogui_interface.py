from src.services.coordinator import PyAutoGUIInterface


class DummyGUI:
    def __init__(self) -> None:
        self.sent = []

    def write(self, text: str) -> None:
        self.sent.append(text)


def test_send_text_uses_gui_module():
    gui = DummyGUI()
    interface = PyAutoGUIInterface(gui_module=gui)
    interface.send_text("hello")
    assert gui.sent == ["hello"]
