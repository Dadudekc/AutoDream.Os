"""Tests for game skill systems."""


def test_skill_systems(game_environment):
    skills = game_environment["skills"]
    assert "attack" in skills and skills["attack"] >= 0
