"""Tests for anti-detection mechanisms."""


def test_anti_detection(game_environment):
    anti_detection = game_environment["anti_detection"]
    assert anti_detection["stealth"] is True and anti_detection["logging"] is False
