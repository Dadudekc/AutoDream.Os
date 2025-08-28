from src.core.smooth_handoff import (
    HandoffInitiator,
    HandoffContext,
    HandoffMonitor,
    HandoffCompleter,
)


def test_completion_moves_to_history():
    active = {}
    history = []
    initiator = HandoffInitiator(active)
    monitor = HandoffMonitor(active)
    completer = HandoffCompleter(active, history)
    context = HandoffContext(handoff_id="x", source="s", target="t")
    execution_id = initiator.initiate(context)
    assert monitor.get_status(execution_id) == "in_progress"
    assert completer.complete(execution_id)
    assert execution_id not in active
    assert len(history) == 1
    assert history[0].status == "completed"

