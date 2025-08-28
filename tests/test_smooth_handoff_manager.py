from src.core.smooth_handoff_manager import SmoothHandoffManager, HandoffContext


def test_manager_coordinates_flow():
    manager = SmoothHandoffManager()
    ctx = HandoffContext(handoff_id="abc", source="A", target="B")
    execution_id = manager.initiate_handoff(ctx)
    assert manager.get_handoff_status(execution_id) == "in_progress"
    assert manager.complete_handoff(execution_id)
    assert manager.get_handoff_status(execution_id) is None
