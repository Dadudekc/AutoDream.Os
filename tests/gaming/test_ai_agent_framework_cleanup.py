import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.ai_agent_framework import (
    AIGamingAgent,
    MultiAgentCoordinator,
    GameState,
)


class TestMultiAgentCoordinator(unittest.TestCase):
    def setUp(self):
        self.coordinator = MultiAgentCoordinator()
        self.agent1 = AIGamingAgent("a1")
        self.agent2 = AIGamingAgent("a2")

    def test_register_and_unregister_agent(self):
        self.coordinator.register_agent(self.agent1)
        self.assertIn("a1", self.coordinator.agents)
        self.coordinator.unregister_agent("a1")
        self.assertNotIn("a1", self.coordinator.agents)

    def test_create_communication_channel(self):
        self.assertTrue(self.coordinator.create_communication_channel("ch"))
        self.assertIn("ch", self.coordinator.communication_channels)

    def test_send_message(self):
        self.coordinator.create_communication_channel("ch")
        self.assertTrue(self.coordinator.send_message("ch", "hi", "a1"))
        self.assertIn("a1: hi", self.coordinator.communication_channels["ch"])

    def test_get_agent_by_name(self):
        self.coordinator.register_agent(self.agent1)
        self.assertEqual(self.coordinator.get_agent_by_name("a1"), self.agent1)
        self.assertIsNone(self.coordinator.get_agent_by_name("none"))

    def test_coordinate_agents(self):
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        self.coordinator.coordinate_agents(GameState())
        self.assertEqual(len(self.coordinator.agents), 2)

    def test_get_coordination_metrics(self):
        self.coordinator.register_agent(self.agent1)
        self.coordinator.create_communication_channel("ch")
        metrics = self.coordinator.get_coordination_metrics()
        self.assertEqual(metrics["total_agents"], 1)
        self.assertEqual(metrics["communication_channels"], 1)
