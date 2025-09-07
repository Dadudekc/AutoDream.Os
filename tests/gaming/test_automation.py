"""Tests for automation features."""


def test_automation(game_environment):
    automation = game_environment["automation"]
    assert automation["enabled"] is True and automation["macro_slots"] > 0
