"""Tests for state analysis systems."""


def test_state_analysis(game_environment):
    state = game_environment["state"]
    assert state["health"] > 0 and state["mana"] >= 0
