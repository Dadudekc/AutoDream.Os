# tests/test_onboarding_modes.py
from src.services.onboarding_handler import OnboardingHandler


def test_round_robin_role_map_quality_suite():
    h = OnboardingHandler()
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6"]
    mapping = h._derive_role_map(agents, mode="quality-suite", role_map_str="")
    # Check cycle order SOLID, SSOT, DRY, KISS, TDD, SOLID...
    assert mapping["Agent-1"] == "SOLID"
    assert mapping["Agent-2"] == "SSOT"
    assert mapping["Agent-3"] == "DRY"
    assert mapping["Agent-4"] == "KISS"
    assert mapping["Agent-5"] == "TDD"
    assert mapping["Agent-6"] == "SOLID"


def test_explicit_role_map_parsing():
    h = OnboardingHandler()
    mapping = h._derive_role_map(
        ["Agent-1", "Agent-2"], mode="solid", role_map_str="Agent-2:DRY, Agent-1:KISS"
    )
    assert mapping == {"Agent-2": "DRY", "Agent-1": "KISS"}
