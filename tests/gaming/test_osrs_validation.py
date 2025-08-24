import unittest

from gaming_systems.osrs import (
    OSRSResourceSpot,
    OSRSRecipe,
    OSRSSkill,
    OSRSLocation,
)


class TestOSRSResourceSpot(unittest.TestCase):
    """Validation tests for resource spot interactions"""

    def test_can_harvest(self):
        spot = OSRSResourceSpot(
            spot_id="tree",
            name="Tree",
            location=OSRSLocation.LUMBRIDGE,
            resource_type="wood",
            skill_required=OSRSSkill.WOODCUTTING,
            level_required=1,
        )

        self.assertTrue(spot.can_harvest(1))
        self.assertFalse(spot.can_harvest(0))


class TestOSRSRecipe(unittest.TestCase):
    """Validation tests for crafting recipes"""

    def test_can_craft(self):
        recipe = OSRSRecipe(
            recipe_id="bronze_bar",
            name="Bronze Bar",
            skill_required=OSRSSkill.SMITHING,
            level_required=1,
            ingredients={"copper": 1, "tin": 1},
            products={"bronze_bar": 1},
            experience_gained=10,
        )

        inventory = {"copper": 1, "tin": 1}
        self.assertTrue(recipe.can_craft(1, inventory))
        self.assertFalse(recipe.can_craft(1, {"copper": 1}))


if __name__ == "__main__":
    unittest.main()
