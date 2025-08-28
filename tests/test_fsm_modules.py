import pytest

from src.fsm import (
    DEFAULT_STATES,
    DEFAULT_TRANSITIONS,
    generate_report,
    load_default_definitions,
    validate_states,
    validate_transitions,
)


def test_default_definitions_match_constants():
    states, transitions = load_default_definitions()
    assert [s.name for s in states] == list(DEFAULT_STATES)
    assert len(transitions) == sum(len(v) for v in DEFAULT_TRANSITIONS.values())


def test_compliance_validation_passes_for_defaults():
    states, transitions = load_default_definitions()
    assert validate_states([s.name for s in states])
    assert validate_transitions([(t.source, t.target) for t in transitions])


def test_compliance_validation_detects_errors():
    with pytest.raises(ValueError):
        validate_states(["unknown"])
    with pytest.raises(ValueError):
        validate_transitions([("pending", "unknown")])


def test_reporting_generates_summary():
    report = generate_report()
    assert report["state_count"] == len(DEFAULT_STATES)
    assert report["transition_count"] == sum(
        len(v) for v in DEFAULT_TRANSITIONS.values()
    )
