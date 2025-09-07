from src.core.smooth_handoff import HandoffInitiator, HandoffContext


def test_initiate_handoff_creates_record():
    active = {}
    initiator = HandoffInitiator(active)
    context = HandoffContext(handoff_id="123", source="A", target="B")
    execution_id = initiator.initiate(context)
    assert execution_id in active
    record = active[execution_id]
    assert record.context == context
    assert record.status == "in_progress"

