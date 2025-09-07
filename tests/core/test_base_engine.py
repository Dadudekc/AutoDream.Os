from src.core.common.base_engine import BaseEngine


class DummyEngine(BaseEngine):
    def __init__(self) -> None:
        super().__init__()
        self.cleaned = False

    def clear_resources(self) -> None:
        self.cleaned = True


def test_initialize_and_status():
    engine = DummyEngine()
    assert engine.get_status()["status"] == "INACTIVE"
    engine.initialize()
    status = engine.get_status()
    assert status["is_initialized"] is True
    assert status["status"] == "ACTIVE"


def test_shutdown_triggers_cleanup():
    engine = DummyEngine()
    engine.initialize()
    engine.shutdown()
    assert engine.cleaned is True
    assert engine.get_status()["status"] == "INACTIVE"
