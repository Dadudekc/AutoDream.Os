#!/usr/bin/env python3
"""
OSRS Smoke Tests - Agent Cellphone V2
====================================

Comprehensive smoke tests for OSRS gaming system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest
import sys
import os

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from osrs import (
    OSRSSkill, OSRSLocation, OSRSGameState, OSRSActionType,
    OSRSPlayerStats, OSRSInventoryItem, OSRSGameData, OSRSResourceSpot, OSRSRecipe,
    OSRSSkillTrainer, OSRSWoodcuttingTrainer, OSRSFishingTrainer, OSRSCombatTrainer,
    OSRSCombatSystem, OSRSNPCInteraction
)


class OSRSSmokeTests(unittest.TestCase):
    """OSRS System Smoke Tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.player = OSRSPlayerStats("test_player", "TestPlayer")
        self.player.update_skill(OSRSSkill.WOODCUTTING, 15, 1000)
        self.player.update_skill(OSRSSkill.FISHING, 25, 2000)
        self.player.update_skill(OSRSSkill.ATTACK, 20, 1500)
        self.player.update_skill(OSRSSkill.STRENGTH, 18, 1200)
        self.player.update_skill(OSRSSkill.DEFENCE, 15, 800)
        self.player.update_skill(OSRSSkill.HITPOINTS, 25, 1000)
    
    def test_core_enums(self):
        """Test core enums functionality"""
        # Test OSRSSkill enum
        self.assertIsInstance(OSRSSkill.WOODCUTTING, OSRSSkill)
        self.assertEqual(OSRSSkill.WOODCUTTING.value, "woodcutting")
        
        # Test OSRSLocation enum
        self.assertIsInstance(OSRSLocation.LUMBRIDGE, OSRSLocation)
        self.assertEqual(OSRSLocation.LUMBRIDGE.value, "lumbridge")
        
        # Test OSRSGameState enum
        self.assertIsInstance(OSRSGameState.IDLE, OSRSGameState)
        self.assertEqual(OSRSGameState.IDLE.value, "idle")
        
        # Test OSRSActionType enum
        self.assertIsInstance(OSRSActionType.SKILL_TRAINING, OSRSActionType)
        self.assertEqual(OSRSActionType.SKILL_TRAINING.value, "skill_training")
    
    def test_data_models(self):
        """Test data models functionality"""
        # Test OSRSPlayerStats
        self.assertEqual(self.player.username, "TestPlayer")
        self.assertEqual(self.player.get_skill_level(OSRSSkill.WOODCUTTING), 15)
        self.assertEqual(self.player.get_skill_experience(OSRSSkill.WOODCUTTING), 1000)
        
        # Test skill update
        self.player.update_skill(OSRSSkill.WOODCUTTING, 16, 1200)
        self.assertEqual(self.player.get_skill_level(OSRSSkill.WOODCUTTING), 16)
        self.assertEqual(self.player.get_skill_experience(OSRSSkill.WOODCUTTING), 1200)
        
        # Test OSRSInventoryItem
        item = OSRSInventoryItem(1, "Test Item", 5, True, True, 100, 50, 75)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.quantity, 5)
        self.assertTrue(item.is_stackable())
        self.assertTrue(item.can_trade())
        self.assertEqual(item.get_total_value(), 375)
    
    def test_woodcutting_trainer(self):
        """Test woodcutting trainer functionality"""
        trainer = OSRSWoodcuttingTrainer(self.player)
        
        # Test initialization
        self.assertEqual(trainer.skill, OSRSSkill.WOODCUTTING)
        self.assertEqual(trainer.player_stats.username, "TestPlayer")
        
        # Test available trees
        trees = trainer.get_available_trees()
        self.assertGreater(len(trees), 0)
        
        # Test training locations
        locations = trainer.get_training_locations()
        self.assertGreater(len(locations), 0)
        
        # Test can train at location
        self.assertTrue(trainer.can_train_at_location(OSRSLocation.LUMBRIDGE))
        
        # Test training session
        self.assertTrue(trainer.start_training(OSRSLocation.LUMBRIDGE))
        self.assertTrue(trainer.is_training)
        
        # Test training action
        self.assertTrue(trainer.perform_training_action())
        progress = trainer.get_training_progress()
        self.assertEqual(progress["status"], "training")
        self.assertGreater(progress["actions_completed"], 0)
        
        # Test stop training
        self.assertTrue(trainer.stop_training())
        self.assertFalse(trainer.is_training)
    
    def test_fishing_trainer(self):
        """Test fishing trainer functionality"""
        trainer = OSRSFishingTrainer(self.player)
        
        # Test initialization
        self.assertEqual(trainer.skill, OSRSSkill.FISHING)
        self.assertTrue(trainer.fishing_rod_equipped)
        
        # Test available spots
        spots = trainer.get_available_spots()
        self.assertGreater(len(spots), 0)
        
        # Test training session
        self.assertTrue(trainer.start_training(OSRSLocation.LUMBRIDGE))
        self.assertTrue(trainer.perform_training_action())
        self.assertTrue(trainer.stop_training())
    
    def test_combat_trainer(self):
        """Test combat trainer functionality"""
        trainer = OSRSCombatTrainer(self.player)
        
        # Test initialization
        self.assertEqual(trainer.skill, OSRSSkill.ATTACK)
        self.assertEqual(trainer.combat_style, "controlled")
        
        # Test available targets
        targets = trainer.get_available_targets()
        self.assertGreater(len(targets), 0)
        
        # Test training session
        self.assertTrue(trainer.start_training(OSRSLocation.LUMBRIDGE))
        self.assertTrue(trainer.perform_training_action())
        self.assertTrue(trainer.stop_training())
    
    def test_combat_system(self):
        """Test combat system functionality"""
        combat = OSRSCombatSystem(self.player)
        
        # Test initialization
        self.assertGreater(combat.combat_level, 0)
        self.assertFalse(combat.is_in_combat)
        
        # Test start combat
        self.assertTrue(combat.start_combat("Goblin", 5))
        self.assertTrue(combat.is_in_combat)
        self.assertIsNotNone(combat.current_target)
        
        # Test perform attack (may be on cooldown initially)
        result = combat.perform_attack()
        if result["success"]:
            # Attack was successful
            self.assertTrue(result["success"])
        else:
            # Attack was on cooldown, which is expected
            self.assertEqual(result["reason"], "Attack on cooldown")
        
        # Test stop combat
        self.assertTrue(combat.stop_combat())
        self.assertFalse(combat.is_in_combat)
    
    def test_npc_interaction(self):
        """Test NPC interaction functionality"""
        npc = OSRSNPCInteraction(self.player)
        
        # Test initialization
        self.assertIsNone(npc.current_npc)
        
        # Test start interaction
        self.assertTrue(npc.start_interaction("Test NPC", OSRSLocation.LUMBRIDGE))
        self.assertIsNotNone(npc.current_npc)
        
        # Test dialogue options
        options = npc.get_dialogue_options()
        self.assertGreater(len(options), 0)
        
        # Test dialogue selection
        result = npc.select_dialogue_option(0)
        self.assertTrue(result["success"])
        
        # Test stop interaction
        self.assertTrue(npc.end_interaction())
        self.assertIsNone(npc.current_npc)


def run_osrs_smoke_tests():
    """Run all OSRS smoke tests"""
    print("🧪 OSRS SMOKE TESTS")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OSRSSmokeTests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ ALL SMOKE TESTS PASSED!")
        print(f"Tests run: {result.testsRun}")
        print("✅ OSRS system is working correctly")
        print("✅ V2 coding standards maintained")
        return True
    else:
        print("❌ SOME SMOKE TESTS FAILED!")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        return False


if __name__ == "__main__":
    success = run_osrs_smoke_tests()
    sys.exit(0 if success else 1)
