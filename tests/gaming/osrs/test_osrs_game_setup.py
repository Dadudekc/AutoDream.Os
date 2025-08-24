import unittest

from gaming_systems.osrs import (
    OSRSSkill,
    OSRSLocation,
    OSRSGameState,
    OSRSActionType,
    OSRSPlayerStats,
    OSRSInventoryItem,
    OSRSGameData,
)


class TestOSRSEnums(unittest.TestCase):
    """Basic checks for OSRS enumeration classes"""

    def test_skill_enum_values(self):
        for skill in OSRSSkill:
            self.assertIsInstance(skill.value, str)

    def test_location_enum_values(self):
        for location in OSRSLocation:
            self.assertIsInstance(location.value, str)

    def test_game_state_enum_values(self):
        for state in OSRSGameState:
            self.assertIsInstance(state.value, str)

    def test_action_type_enum_values(self):
        for action in OSRSActionType:
            self.assertIsInstance(action.value, str)


class TestOSRSPlayerStats(unittest.TestCase):
    """Tests for the OSRSPlayerStats dataclass"""

    def test_update_and_retrieve_skill(self):
        stats = OSRSPlayerStats(player_id="p1", username="tester")
        stats.update_skill(OSRSSkill.ATTACK, 10, 1000)

        self.assertEqual(stats.get_skill_level(OSRSSkill.ATTACK), 10)
        self.assertEqual(stats.get_skill_experience(OSRSSkill.ATTACK), 1000)


class TestOSRSInventoryItem(unittest.TestCase):
    """Tests for OSRSInventoryItem dataclass"""

    def test_stackable_item(self):
        item = OSRSInventoryItem(
            item_id=995,
            name="Coins",
            quantity=1000,
            stackable=True,
            ge_price=1,
        )

        self.assertTrue(item.is_stackable())
        self.assertEqual(item.get_total_value(), 1000)


class TestOSRSGameData(unittest.TestCase):
    """Tests for OSRSGameData dataclass"""

    def test_action_cycle(self):
        data = OSRSGameData()
        data.start_action("chopping", duration=5)

        self.assertEqual(data.current_action, "chopping")
        self.assertEqual(data.game_state, "active")

        data.complete_action()
        self.assertEqual(data.game_state, "idle")
        self.assertIsNone(data.current_action)


if __name__ == "__main__":
    unittest.main()
