import time
import unittest

from gaming_systems.osrs import (
    OSRSLocation,
    OSRSGameState,
    OSRSPlayerStats,
    create_osrs_ai_agent,
)
from gaming_systems.osrs.ai.decision_engine import (
    OSRSDecisionEngine,
    DecisionContext,
)


class TestOSRSDecisionEngine(unittest.TestCase):
    """Agent-focused tests for the decision engine"""

    def setUp(self):
        self.engine = OSRSDecisionEngine()
        self.stats = OSRSPlayerStats(player_id="p1", username="tester")

    def test_analyze_situation_returns_decision(self):
        context = DecisionContext(
            player_stats=self.stats,
            current_location=OSRSLocation.LUMBRIDGE,
            game_state=OSRSGameState.IDLE,
            available_resources=[],
            current_goals=[],
            time_of_day=time.time(),
            energy_level=100,
        )

        decision = self.engine.analyze_situation(context)
        self.assertIsNotNone(decision)
        self.assertTrue(hasattr(decision, "action_description"))


class TestCreateOSRSAIAgent(unittest.TestCase):
    """Tests for the create_osrs_ai_agent factory"""

    def test_factory_returns_components(self):
        agent = create_osrs_ai_agent()
        self.assertIn("decision_engine", agent)
        self.assertIn("skill_trainer", agent)
        self.assertIn("combat_system", agent)
        self.assertIn("market_system", agent)


if __name__ == "__main__":
    unittest.main()
