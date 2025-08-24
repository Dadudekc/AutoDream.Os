import unittest

from gaming_systems.osrs import OSRSPlayerStats, OSRSLocation
from gaming_systems.osrs.skills import (
    OSRSWoodcuttingTrainer,
    OSRSFishingTrainer,
    OSRSCombatTrainer,
)


class TestWoodcuttingTrainer(unittest.TestCase):
    """Scenario tests for woodcutting training"""

    def setUp(self):
        stats = OSRSPlayerStats(player_id="1", username="wc")
        self.trainer = OSRSWoodcuttingTrainer(stats)

    def test_can_train_at_location(self):
        self.assertTrue(self.trainer.can_train_at_location(OSRSLocation.LUMBRIDGE))

    def test_training_cycle(self):
        started = self.trainer.start_training(OSRSLocation.LUMBRIDGE)
        self.assertTrue(started)
        self.assertTrue(self.trainer.is_training)
        # perform a single action (may succeed or fail)
        self.trainer.perform_training_action()
        self.assertTrue(self.trainer.stop_training())
        self.assertFalse(self.trainer.is_training)


class TestFishingTrainer(unittest.TestCase):
    """Scenario tests for fishing training"""

    def setUp(self):
        stats = OSRSPlayerStats(player_id="2", username="fish")
        self.trainer = OSRSFishingTrainer(stats)

    def test_can_train_at_location(self):
        self.assertTrue(self.trainer.can_train_at_location(OSRSLocation.LUMBRIDGE))

    def test_training_cycle(self):
        started = self.trainer.start_training(OSRSLocation.LUMBRIDGE)
        self.assertTrue(started)
        self.assertTrue(self.trainer.stop_training())


class TestCombatTrainer(unittest.TestCase):
    """Scenario tests for combat training"""

    def setUp(self):
        stats = OSRSPlayerStats(player_id="3", username="combat")
        self.trainer = OSRSCombatTrainer(stats)

    def test_get_training_locations(self):
        locations = self.trainer.get_training_locations()
        self.assertTrue(len(locations) > 0)
        self.assertIsInstance(locations[0], OSRSLocation)


if __name__ == "__main__":
    unittest.main()
