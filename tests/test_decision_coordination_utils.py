import logging

from src.core.coordination_status import CoordinationMode, CoordinationStatus
from src.core.coordination_scheduler import CoordinationScheduler
from src.core import coordination_results as results


def test_coordination_status_values():
    assert CoordinationMode.CONSENSUS.value == "consensus"
    assert CoordinationStatus.COMPLETED.value == "completed"


def test_scheduler_runs_finalize():
    calls = []

    scheduler = CoordinationScheduler(
        lambda sys, ses: calls.append("gather"),
        lambda sys, ses, proto: calls.append("deliberate"),
        lambda sys, ses, proto: True,
        lambda sys, ses: calls.append("finalize"),
        lambda sys, ses, proto: calls.append("failure"),
    )

    class DummySystem:
        logger = logging.getLogger("dummy")

    class DummySession:
        session_id = "s"
        status = ""
        end_time = None

    thread = scheduler.start(DummySystem(), DummySession(), {})
    thread.join(timeout=1)

    assert "gather" in calls and "finalize" in calls
    assert "failure" not in calls


def test_apply_majority_logic():
    inputs = [{"choice": "A"}, {"choice": "A"}, {"choice": "B"}]
    result = results.apply_majority_logic(inputs)
    assert result["method"] == "majority"
    assert result["decision"] == str({"choice": "A"})
    assert result["confidence"] == 2 / 3
