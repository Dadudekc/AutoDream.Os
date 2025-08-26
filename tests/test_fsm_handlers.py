import pytest

from src.core.fsm.handlers import ConcreteStateHandler, ConditionalTransitionHandler
from src.core.fsm.models import StateStatus


def test_allowed_transition():
    context = {"current_state": "start", "value": 10, "actions": []}
    state_handler = ConcreteStateHandler(
        action=lambda ctx: ctx["actions"].append("processed"),
        check=lambda ctx: ctx["value"] >= 0,
    )
    result = state_handler.execute(context)
    assert result.status == StateStatus.COMPLETED
    assert state_handler.can_transition(context) is True
    assert context["actions"] == ["processed"]

    transition = ConditionalTransitionHandler(lambda ctx: ctx["value"] > 5, "end")
    outcome = transition.execute(context)
    assert outcome["allowed"] is True
    assert context["current_state"] == "end"


def test_disallowed_transition():
    context = {"current_state": "start", "value": 1, "actions": []}
    state_handler = ConcreteStateHandler(
        action=lambda ctx: ctx["actions"].append("processed"),
        check=lambda ctx: ctx["value"] >= 0,
    )
    result = state_handler.execute(context)
    assert result.status == StateStatus.COMPLETED
    assert state_handler.can_transition(context) is True

    transition = ConditionalTransitionHandler(lambda ctx: ctx["value"] > 5, "end")
    outcome = transition.execute(context)
    assert outcome["allowed"] is False
    assert context["current_state"] == "start"
