from src.core.fsm.handlers import ConditionalTransitionHandler
from src.core.fsm.models import StateStatus


def test_allowed_transition(state_handler):
    context = {"current_state": "start", "value": 10, "actions": []}
    result = state_handler.execute(context)
    assert result.status == StateStatus.COMPLETED
    assert state_handler.can_transition(context)
    assert context["actions"] == ["processed"]

    transition = ConditionalTransitionHandler(lambda ctx: ctx["value"] > 5, "end")
    outcome = transition.execute(context)
    assert outcome["allowed"]
    assert context["current_state"] == "end"


def test_disallowed_transition(state_handler):
    context = {"current_state": "start", "value": 1, "actions": []}
    result = state_handler.execute(context)
    assert result.status == StateStatus.COMPLETED
    assert state_handler.can_transition(context)

    transition = ConditionalTransitionHandler(lambda ctx: ctx["value"] > 5, "end")
    outcome = transition.execute(context)
    assert not outcome["allowed"]
    assert context["current_state"] == "start"
