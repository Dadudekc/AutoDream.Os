from src.core.smooth_handoff import HandoffInitiator, HandoffContext
from src.core.smooth_handoff import HandoffMonitor


def test_monitor_reports_status():
    active = {}
    initiator = HandoffInitiator(active)
    monitor = HandoffMonitor(active)
    context = HandoffContext(handoff_id="x", source="s", target="t")
    execution_id = initiator.initiate(context)
    assert monitor.get_status(execution_id) == "in_progress"

