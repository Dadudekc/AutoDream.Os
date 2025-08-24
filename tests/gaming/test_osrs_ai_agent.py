#!/usr/bin/env python3
"""
Test Suite for OSRS AI Agent System
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- OSRS-specific AI agent functionality
- Skill training systems
- Game state analysis
- Anti-detection measures
- Grand Exchange automation
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time

from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import numpy as np
from datetime import datetime

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.osrs import (
    OSRSSkill,
    OSRSLocation,
    OSRSGameState,
    OSRSActionType,
    OSRSPlayerStats,
    OSRSInventoryItem,
    OSRSGameData,
    OSRSSkillTrainer,
    OSRSWoodcuttingTrainer,
    OSRSFishingTrainer,
    OSRSCombatTrainer,
    OSRSMarketSystem,
    OSRSDecisionEngine,
    create_osrs_ai_agent,
)

from gaming_systems.ai_gaming_systems import GameType, AIDecisionType, GameObjectData


class TestOSRSEnums(unittest.TestCase):
    """Test OSRS enumeration classes"""

    def test_osrs_skills(self):
        """Test OSRS skills enumeration"""
        skills = [
            OSRSSkill.ATTACK,
            OSRSSkill.STRENGTH,
            OSRSSkill.DEFENCE,
            OSRSSkill.HITPOINTS,
            OSRSSkill.RANGED,
            OSRSSkill.PRAYER,
            OSRSSkill.MAGIC,
            OSRSSkill.COOKING,
            OSRSSkill.WOODCUTTING,
            OSRSSkill.FLETCHING,
            OSRSSkill.FISHING,
            OSRSSkill.FIREMAKING,
            OSRSSkill.CRAFTING,
            OSRSSkill.SMITHING,
            OSRSSkill.MINING,
            OSRSSkill.HERBLORE,
            OSRSSkill.AGILITY,
            OSRSSkill.THIEVING,
            OSRSSkill.SLAYER,
            OSRSSkill.FARMING,
            OSRSSkill.RUNECRAFTING,
            OSRSSkill.HUNTER,
            OSRSSkill.CONSTRUCTION,
        ]

        for skill in skills:
            self.assertIsInstance(skill.value, str)
            self.assertTrue(len(skill.value) > 0)

    def test_osrs_locations(self):
        """Test OSRS locations enumeration"""
        locations = [
            OSRSLocation.LUMBRIDGE,
            OSRSLocation.VARROCK,
            OSRSLocation.FALADOR,
            OSRSLocation.ARDOUGNE,
            OSRSLocation.CAMELOT,
            OSRSLocation.YANILLE,
            OSRSLocation.GRAND_EXCHANGE,
            OSRSLocation.BARBARIAN_VILLAGE,
            OSRSLocation.EDGEVILLE,
            OSRSLocation.DRAYNOR,
            OSRSLocation.AL_KHARID,
            OSRSLocation.TUTORIAL_ISLAND,
            OSRSLocation.WILDERNESS,
        ]

        for location in locations:
            self.assertIsInstance(location.value, str)
            self.assertTrue(len(location.value) > 0)

    def test_osrs_game_states(self):
        """Test OSRS game states enumeration"""
        states = [
            OSRSGameState.LOGGED_OUT,
            OSRSGameState.LOGIN_SCREEN,
            OSRSGameState.IDLE,
            OSRSGameState.COMBAT,
            OSRSGameState.SKILLING,
            OSRSGameState.BANKING,
            OSRSGameState.TRADING,
            OSRSGameState.QUEST_DIALOGUE,
            OSRSGameState.INVENTORY_FULL,
            OSRSGameState.DEAD,
            OSRSGameState.IN_COMBAT,
            OSRSGameState.TELEPORTING,
            OSRSGameState.LOADING,
        ]

        for state in states:
            self.assertIsInstance(state.value, str)
            self.assertTrue(len(state.value) > 0)

    def test_osrs_action_types(self):
        """Test OSRS action types enumeration"""
        actions = [
            OSRSActionType.LOGIN,
            OSRSActionType.LOGOUT,
            OSRSActionType.CLICK_NPC,
            OSRSActionType.CLICK_OBJECT,
            OSRSActionType.CLICK_GROUND,
            OSRSActionType.USE_ITEM,
            OSRSActionType.DROP_ITEM,
            OSRSActionType.EAT_FOOD,
            OSRSActionType.DRINK_POTION,
            OSRSActionType.CAST_SPELL,
            OSRSActionType.EQUIP_ITEM,
            OSRSActionType.BANK_DEPOSIT,
            OSRSActionType.BANK_WITHDRAW,
            OSRSActionType.WALK_TO,
            OSRSActionType.RUN_TO,
            OSRSActionType.TELEPORT,
        ]

        for action in actions:
            self.assertIsInstance(action.value, str)
            self.assertTrue(len(action.value) > 0)


class TestOSRSPlayerStats(unittest.TestCase):
    """Test OSRSPlayerStats dataclass"""

    def test_default_stats(self):
        """Test default player stats"""
        stats = OSRSPlayerStats()

        # Test combat stats
        self.assertEqual(stats.attack_level, 1)
        self.assertEqual(stats.strength_level, 1)
        self.assertEqual(stats.defence_level, 1)
        self.assertEqual(stats.hitpoints_level, 10)
        self.assertEqual(stats.current_hp, 10)
        self.assertEqual(stats.combat_level, 3)

        # Test resources
        self.assertEqual(stats.gp, 0)
        self.assertEqual(stats.run_energy, 100)
        self.assertEqual(stats.special_attack, 100)

        # Test location
        self.assertEqual(stats.current_location, OSRSLocation.LUMBRIDGE)

        # Test status effects
        self.assertFalse(stats.poisoned)
        self.assertFalse(stats.diseased)
        self.assertFalse(stats.on_fire)

    def test_custom_stats(self):
        """Test custom player stats"""
        stats = OSRSPlayerStats(
            attack_level=99,
            strength_level=99,
            defence_level=99,
            hitpoints_level=99,
            current_hp=50,
            combat_level=126,
            gp=1000000,
            current_location=OSRSLocation.VARROCK,
            poisoned=True,
        )

        self.assertEqual(stats.attack_level, 99)
        self.assertEqual(stats.strength_level, 99)
        self.assertEqual(stats.defence_level, 99)
        self.assertEqual(stats.hitpoints_level, 99)
        self.assertEqual(stats.current_hp, 50)
        self.assertEqual(stats.combat_level, 126)
        self.assertEqual(stats.gp, 1000000)
        self.assertEqual(stats.current_location, OSRSLocation.VARROCK)
        self.assertTrue(stats.poisoned)


class TestOSRSInventoryItem(unittest.TestCase):
    """Test OSRSInventoryItem dataclass"""

    def test_inventory_item_creation(self):
        """Test inventory item creation"""
        item = OSRSInventoryItem(
            item_id=995, name="Coins", quantity=1000, noted=False, slot=0, value=1
        )

        self.assertEqual(item.item_id, 995)
        self.assertEqual(item.name, "Coins")
        self.assertEqual(item.quantity, 1000)
        self.assertFalse(item.noted)
        self.assertEqual(item.slot, 0)
        self.assertEqual(item.value, 1)

    def test_noted_item(self):
        """Test noted item creation"""
        item = OSRSInventoryItem(
            item_id=1513,
            name="Yew logs (noted)",
            quantity=100,
            noted=True,
            slot=5,
            value=300,
        )

        self.assertEqual(item.item_id, 1513)
        self.assertEqual(item.name, "Yew logs (noted)")
        self.assertEqual(item.quantity, 100)
        self.assertTrue(item.noted)
        self.assertEqual(item.slot, 5)
        self.assertEqual(item.value, 300)


class TestOSRSGameData(unittest.TestCase):
    """Test OSRSGameData dataclass"""

    def test_game_data_creation(self):
        """Test OSRS game data creation"""
        stats = OSRSPlayerStats()
        inventory = [
            OSRSInventoryItem(995, "Coins", 1000, slot=0),
            OSRSInventoryItem(1511, "Yew logs", 5, slot=1),
        ]

        game_data = OSRSGameData(
            player_stats=stats,
            inventory=inventory,
            equipment={},
            current_location=OSRSLocation.CATHERBY,
            game_state=OSRSGameState.SKILLING,
            quest_points=50,
        )

        self.assertEqual(game_data.player_stats, stats)
        self.assertEqual(len(game_data.inventory), 2)
        self.assertEqual(game_data.current_location, OSRSLocation.CATHERBY)
        self.assertEqual(game_data.game_state, OSRSGameState.SKILLING)
        self.assertEqual(game_data.quest_points, 50)
        self.assertIsInstance(game_data.skill_experience, dict)
        self.assertIsInstance(game_data.bank_items, list)
        self.assertIsNotNone(game_data.timestamp)


class TestOSRSWoodcuttingTrainer(unittest.TestCase):
    """Test OSRSWoodcuttingTrainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.trainer = OSRSWoodcuttingTrainer(target_level=60, tree_type="oak")

    def test_trainer_initialization(self):
        """Test woodcutting trainer initialization"""
        self.assertEqual(self.trainer.skill, OSRSSkill.WOODCUTTING)
        self.assertEqual(self.trainer.target_level, 60)
        self.assertEqual(self.trainer.tree_type, "oak")
        self.assertFalse(self.trainer.training_active)

    def test_get_required_items(self):
        """Test getting required items"""
        required = self.trainer.get_required_items()

        self.assertIsInstance(required, list)
        self.assertIn("axe", required)
        self.assertIn("food", required)

    def test_should_bank_valuable_logs(self):
        """Test banking decision for valuable logs"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(1513, "yew logs", 5, slot=0)],
            equipment={},
            current_location=OSRSLocation.SEERS_VILLAGE,
            game_state=OSRSGameState.SKILLING,
        )

        should_bank = self.trainer.should_bank(game_data)
        self.assertTrue(should_bank)

    def test_should_bank_regular_logs(self):
        """Test banking decision for regular logs"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(1511, "oak logs", 10, slot=0)],
            equipment={},
            current_location=OSRSLocation.SEERS_VILLAGE,
            game_state=OSRSGameState.SKILLING,
        )

        should_bank = self.trainer.should_bank(game_data)
        self.assertFalse(should_bank)  # Oak logs not valuable enough

    def test_train_with_full_inventory(self):
        """Test training with full inventory"""
        # Create full inventory
        inventory = [OSRSInventoryItem(1511, "oak logs", 1, slot=i) for i in range(28)]

        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=inventory,
            equipment={},
            current_location=OSRSLocation.SEERS_VILLAGE,
            game_state=OSRSGameState.SKILLING,
        )

        decisions = self.trainer.train(game_data)

        self.assertIsInstance(decisions, list)
        self.assertTrue(len(decisions) > 0)
        # Should have drop or bank decision
        action_types = [d.decision_type for d in decisions]
        self.assertTrue(
            any(
                t in [AIDecisionType.NAVIGATE_PATH, AIDecisionType.MANAGE_INVENTORY]
                for t in action_types
            )
        )

    def test_train_without_axe(self):
        """Test training without axe"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(995, "coins", 1000, slot=0)],  # No axe
            equipment={},
            current_location=OSRSLocation.SEERS_VILLAGE,
            game_state=OSRSGameState.SKILLING,
        )

        decisions = self.trainer.train(game_data)

        self.assertIsInstance(decisions, list)
        self.assertTrue(len(decisions) > 0)
        # Should have get axe decision
        get_axe_decisions = [d for d in decisions if "axe" in d.reasoning.lower()]
        self.assertTrue(len(get_axe_decisions) > 0)

    def test_start_stop_training(self):
        """Test starting and stopping training"""
        self.assertFalse(self.trainer.training_active)

        self.trainer.start_training()
        self.assertTrue(self.trainer.training_active)
        self.assertIsNotNone(self.trainer.start_time)

        self.trainer.stop_training()
        self.assertFalse(self.trainer.training_active)


class TestOSRSFishingTrainer(unittest.TestCase):
    """Test OSRSFishingTrainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.trainer = OSRSFishingTrainer(target_level=80, fish_type="lobster")

    def test_trainer_initialization(self):
        """Test fishing trainer initialization"""
        self.assertEqual(self.trainer.skill, OSRSSkill.FISHING)
        self.assertEqual(self.trainer.target_level, 80)
        self.assertEqual(self.trainer.fish_type, "lobster")
        self.assertEqual(self.trainer.fishing_spot, "catherby")

    def test_get_required_items_lobster(self):
        """Test getting required items for lobster fishing"""
        required = self.trainer.get_required_items()

        self.assertIsInstance(required, list)
        self.assertIn("lobster_pot", required)
        self.assertIn("food", required)

    def test_get_required_items_salmon(self):
        """Test getting required items for salmon fishing"""
        trainer = OSRSFishingTrainer(fish_type="salmon")
        required = trainer.get_required_items()

        self.assertIsInstance(required, list)
        self.assertIn("fly_fishing_rod", required)
        self.assertIn("feathers", required)

    def test_should_bank_fish(self):
        """Test banking decision for fish"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(379, "lobster", 10, slot=0)],
            equipment={},
            current_location=OSRSLocation.CATHERBY,
            game_state=OSRSGameState.SKILLING,
        )

        should_bank = self.trainer.should_bank(game_data)
        self.assertTrue(should_bank)  # Always bank fish for profit

    def test_has_fishing_equipment_yes(self):
        """Test fishing equipment check - has equipment"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[
                OSRSInventoryItem(301, "lobster_pot", 1, slot=0),
                OSRSInventoryItem(379, "food", 5, slot=1),
            ],
            equipment={},
            current_location=OSRSLocation.CATHERBY,
            game_state=OSRSGameState.SKILLING,
        )

        has_equipment = self.trainer._has_fishing_equipment(game_data)
        self.assertTrue(has_equipment)

    def test_has_fishing_equipment_no(self):
        """Test fishing equipment check - missing equipment"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[
                OSRSInventoryItem(995, "coins", 1000, slot=0)
            ],  # No fishing gear
            equipment={},
            current_location=OSRSLocation.CATHERBY,
            game_state=OSRSGameState.SKILLING,
        )

        has_equipment = self.trainer._has_fishing_equipment(game_data)
        self.assertFalse(has_equipment)


class TestOSRSCombatTrainer(unittest.TestCase):
    """Test OSRSCombatTrainer"""

    def setUp(self):
        """Set up test fixtures"""
        self.trainer = OSRSCombatTrainer(
            combat_skill=OSRSSkill.ATTACK, target_level=60, training_monster="cow"
        )

    def test_trainer_initialization(self):
        """Test combat trainer initialization"""
        self.assertEqual(self.trainer.skill, OSRSSkill.ATTACK)
        self.assertEqual(self.trainer.target_level, 60)
        self.assertEqual(self.trainer.training_monster, "cow")
        self.assertEqual(self.trainer.food_threshold, 5)
        self.assertEqual(self.trainer.safe_location, OSRSLocation.LUMBRIDGE)

    def test_get_required_items(self):
        """Test getting required items for combat"""
        required = self.trainer.get_required_items()

        self.assertIsInstance(required, list)
        self.assertIn("weapon", required)
        self.assertIn("food", required)
        self.assertIn("armor", required)

    def test_train_low_health(self):
        """Test training with low health"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(current_hp=3),  # Very low health
            inventory=[OSRSInventoryItem(379, "lobster", 5, slot=0)],
            equipment={},
            current_location=OSRSLocation.LUMBRIDGE,
            game_state=OSRSGameState.IDLE,
        )

        decisions = self.trainer.train(game_data)

        self.assertIsInstance(decisions, list)
        self.assertTrue(len(decisions) > 0)
        # Should have eat food decision
        eat_decisions = [
            d for d in decisions if d.decision_type == AIDecisionType.USE_ITEM
        ]
        self.assertTrue(len(eat_decisions) > 0)

    def test_train_no_food(self):
        """Test training without food"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(995, "coins", 1000, slot=0)],  # No food
            equipment={},
            current_location=OSRSLocation.LUMBRIDGE,
            game_state=OSRSGameState.IDLE,
        )

        decisions = self.trainer.train(game_data)

        self.assertIsInstance(decisions, list)
        self.assertTrue(len(decisions) > 0)
        # Should have get food decision
        get_food_decisions = [d for d in decisions if "food" in d.reasoning.lower()]
        self.assertTrue(len(get_food_decisions) > 0)

    def test_train_in_combat(self):
        """Test training while in combat"""
        game_data = OSRSGameData(
            player_stats=OSRSPlayerStats(),
            inventory=[OSRSInventoryItem(379, "lobster", 5, slot=0)],
            equipment={},
            current_location=OSRSLocation.LUMBRIDGE,
            game_state=OSRSGameState.IN_COMBAT,
        )

        decisions = self.trainer.train(game_data)

        self.assertIsInstance(decisions, list)
        self.assertTrue(len(decisions) > 0)
        # Should have wait decision
        wait_decisions = [
            d for d in decisions if d.decision_type == AIDecisionType.WAIT_FOR_EVENT
        ]
        self.assertTrue(len(wait_decisions) > 0)


class TestOSRSGrandExchangeBot(unittest.TestCase):
    """Test OSRSGrandExchangeBot"""

    def setUp(self):
        """Set up test fixtures"""
        self.ge_bot = OSRSGrandExchangeBot()

    def test_ge_bot_initialization(self):
        """Test GE bot initialization"""
        self.assertIsInstance(self.ge_bot.price_database, dict)
        self.assertIsInstance(self.ge_bot.trading_history, list)
        self.assertEqual(self.ge_bot.profit_target, 0.1)
        self.assertEqual(len(self.ge_bot.price_database), 0)
        self.assertEqual(len(self.ge_bot.trading_history), 0)

    def test_update_prices(self):
        """Test updating item prices"""
        prices = {"rune_scimitar": 15000, "lobster": 180, "yew_logs": 300}

        self.ge_bot.update_prices(prices)

        self.assertEqual(len(self.ge_bot.price_database), 3)
        self.assertEqual(self.ge_bot.price_database["rune_scimitar"], 15000)
        self.assertEqual(self.ge_bot.price_database["lobster"], 180)

    def test_find_profitable_trades(self):
        """Test finding profitable trades"""
        self.ge_bot.price_database = {
            "rune_scimitar": 15000,
            "bronze_sword": 50,
            "rune_platebody": 40000,
        }

        opportunities = self.ge_bot.find_profitable_trades()

        self.assertIsInstance(opportunities, list)
        # Should find rune items as profitable
        rune_opportunities = [op for op in opportunities if "rune" in op["item"]]
        self.assertTrue(len(rune_opportunities) > 0)

    def test_create_buy_order(self):
        """Test creating buy order"""
        decision = self.ge_bot.create_buy_order("rune_scimitar", 5, 14000)

        self.assertEqual(decision.decision_type, AIDecisionType.CLICK_OBJECT)
        self.assertEqual(decision.target, "grand_exchange")
        self.assertEqual(decision.parameters["action"], "buy")
        self.assertEqual(decision.parameters["item"], "rune_scimitar")
        self.assertEqual(decision.parameters["quantity"], 5)
        self.assertEqual(decision.parameters["price"], 14000)

    def test_create_sell_order(self):
        """Test creating sell order"""
        decision = self.ge_bot.create_sell_order("yew_logs", 100, 350)

        self.assertEqual(decision.decision_type, AIDecisionType.CLICK_OBJECT)
        self.assertEqual(decision.target, "grand_exchange")
        self.assertEqual(decision.parameters["action"], "sell")
        self.assertEqual(decision.parameters["item"], "yew_logs")
        self.assertEqual(decision.parameters["quantity"], 100)
        self.assertEqual(decision.parameters["price"], 350)


class TestOSRSAntiDetection(unittest.TestCase):
    """Test OSRSAntiDetection"""

    def setUp(self):
        """Set up test fixtures"""
        self.anti_detection = OSRSAntiDetection()

    def test_anti_detection_initialization(self):
        """Test anti-detection initialization"""
        self.assertIsInstance(self.anti_detection.last_action_time, float)
        self.assertIsInstance(self.anti_detection.action_intervals, list)
        self.assertIsInstance(self.anti_detection.break_schedule, list)
        self.assertTrue(self.anti_detection.human_like_behavior)

    def test_get_action_delay(self):
        """Test getting action delay"""
        delay = self.anti_detection.get_action_delay()

        self.assertIsInstance(delay, float)
        self.assertGreaterEqual(delay, 0.5)
        self.assertLessEqual(delay, 20.0)  # Max with occasional long delays

    def test_get_action_delay_disabled(self):
        """Test getting action delay when disabled"""
        self.anti_detection.human_like_behavior = False
        delay = self.anti_detection.get_action_delay()

        self.assertEqual(delay, 0.1)

    def test_randomize_click_position(self):
        """Test randomizing click position"""
        original_pos = (100, 200)
        randomized = self.anti_detection.randomize_click_position(original_pos)

        self.assertIsInstance(randomized, tuple)
        self.assertEqual(len(randomized), 2)

        # Should be within 5 pixels of original
        x_diff = abs(randomized[0] - original_pos[0])
        y_diff = abs(randomized[1] - original_pos[1])
        self.assertLessEqual(x_diff, 5)
        self.assertLessEqual(y_diff, 5)

    def test_should_take_break(self):
        """Test break decision"""
        # Fresh instance should not need break
        should_break = self.anti_detection.should_take_break()
        self.assertIsInstance(should_break, bool)

        # Set last action time to long ago
        self.anti_detection.last_action_time = time.time() - 7200  # 2 hours ago
        should_break = self.anti_detection.should_take_break()
        self.assertTrue(should_break)

    def test_should_move_mouse_randomly(self):
        """Test random mouse movement decision"""
        should_move = self.anti_detection.should_move_mouse_randomly()
        self.assertIsInstance(should_move, bool)


class TestOSRSAIAgent(unittest.TestCase):
    """Test OSRSAIAgent"""

    def setUp(self):
        """Set up test fixtures"""
        config = {
            "templates_dir": tempfile.mkdtemp(),
            "anti_detection": True,
            "skill_training": True,
        }
        self.agent = OSRSAIAgent(config)

    def tearDown(self):
        """Clean up test fixtures"""
        if self.agent.is_running:
            self.agent.stop()
        shutil.rmtree(self.agent.config["templates_dir"], ignore_errors=True)

    def test_agent_initialization(self):
        """Test OSRS agent initialization"""
        self.assertEqual(self.agent.game_type, GameType.OSRS)
        self.assertIsInstance(self.agent.skill_trainers, dict)
        self.assertIsNotNone(self.agent.ge_bot)
        self.assertIsNotNone(self.agent.anti_detection)
        self.assertIsNone(self.agent.current_task)
        self.assertIsInstance(self.agent.game_data, OSRSGameData)

    def test_skill_trainers_initialization(self):
        """Test skill trainers initialization"""
        # Check that key trainers are initialized
        self.assertIn(OSRSSkill.WOODCUTTING, self.agent.skill_trainers)
        self.assertIn(OSRSSkill.FISHING, self.agent.skill_trainers)
        self.assertIn(OSRSSkill.ATTACK, self.agent.skill_trainers)
        self.assertIn(OSRSSkill.STRENGTH, self.agent.skill_trainers)
        self.assertIn(OSRSSkill.DEFENCE, self.agent.skill_trainers)

        # Check trainer types
        self.assertIsInstance(
            self.agent.skill_trainers[OSRSSkill.WOODCUTTING], OSRSWoodcuttingTrainer
        )
        self.assertIsInstance(
            self.agent.skill_trainers[OSRSSkill.FISHING], OSRSFishingTrainer
        )
        self.assertIsInstance(
            self.agent.skill_trainers[OSRSSkill.ATTACK], OSRSCombatTrainer
        )

    def test_start_skill_training_valid(self):
        """Test starting valid skill training"""
        success = self.agent.start_skill_training(OSRSSkill.WOODCUTTING, 60)

        self.assertTrue(success)
        self.assertEqual(self.agent.current_task, "training_woodcutting")
        self.assertTrue(
            self.agent.skill_trainers[OSRSSkill.WOODCUTTING].training_active
        )
        self.assertEqual(
            self.agent.skill_trainers[OSRSSkill.WOODCUTTING].target_level, 60
        )

    def test_start_skill_training_invalid(self):
        """Test starting invalid skill training"""
        # Remove a trainer to test failure
        del self.agent.skill_trainers[OSRSSkill.WOODCUTTING]

        success = self.agent.start_skill_training(OSRSSkill.WOODCUTTING, 60)

        self.assertFalse(success)
        self.assertIsNone(self.agent.current_task)

    def test_stop_skill_training(self):
        """Test stopping skill training"""
        # Start training first
        self.agent.start_skill_training(OSRSSkill.FISHING, 80)
        self.assertTrue(self.agent.skill_trainers[OSRSSkill.FISHING].training_active)

        # Stop training
        self.agent.stop_skill_training(OSRSSkill.FISHING)

        self.assertFalse(self.agent.skill_trainers[OSRSSkill.FISHING].training_active)
        self.assertIsNone(self.agent.current_task)

    def test_analyze_osrs_state(self):
        """Test OSRS state analysis"""
        test_image = np.zeros((600, 800, 3), dtype=np.uint8)
        test_objects = [
            GameObjectData("obj1", "HP: 75/100", (50, 50), "text", 0.9),
            GameObjectData("obj2", "tree", (100, 100), "resource", 0.8),
            GameObjectData("obj3", "lumbridge castle", (200, 200), "landmark", 0.9),
        ]

        game_data = self.agent.analyze_osrs_state(test_image, test_objects)

        self.assertIsInstance(game_data, OSRSGameData)
        self.assertEqual(game_data.player_stats.current_hp, 75)
        self.assertEqual(game_data.current_location, OSRSLocation.LUMBRIDGE)
        self.assertIsNotNone(game_data.timestamp)

    def test_get_osrs_recommendations_break_time(self):
        """Test recommendations when break is needed"""
        # Mock anti-detection to always suggest break
        with patch.object(
            self.agent.anti_detection, "should_take_break", return_value=True
        ):
            recommendations = self.agent.get_osrs_recommendations()

            self.assertIsInstance(recommendations, list)
            self.assertTrue(len(recommendations) > 0)

            # Should have break recommendation
            break_decisions = [
                r
                for r in recommendations
                if r.decision_type == AIDecisionType.WAIT_FOR_EVENT
            ]
            self.assertTrue(len(break_decisions) > 0)

    def test_get_osrs_recommendations_low_health(self):
        """Test recommendations for low health"""
        # Set low health
        self.agent.game_data.player_stats.current_hp = 1

        recommendations = self.agent.get_osrs_recommendations()

        self.assertIsInstance(recommendations, list)
        # Should have emergency action
        emergency_actions = [
            r
            for r in recommendations
            if r.decision_type == AIDecisionType.EMERGENCY_ACTION
        ]
        self.assertTrue(len(emergency_actions) > 0)

    def test_get_osrs_recommendations_skill_training(self):
        """Test recommendations during skill training"""
        # Start woodcutting training
        self.agent.start_skill_training(OSRSSkill.WOODCUTTING, 60)

        # Mock anti-detection to not suggest break
        with patch.object(
            self.agent.anti_detection, "should_take_break", return_value=False
        ):
            recommendations = self.agent.get_osrs_recommendations()

            self.assertIsInstance(recommendations, list)
            # Should have training-related recommendations when training is active


class TestCreateOSRSAIAgent(unittest.TestCase):
    """Test OSRS AI agent factory function"""

    def test_create_osrs_ai_agent_default(self):
        """Test creating OSRS agent with default config"""
        agent = create_osrs_ai_agent()

        self.assertIsInstance(agent, OSRSAIAgent)
        self.assertEqual(agent.game_type, GameType.OSRS)
        self.assertIn("templates_dir", agent.config)
        self.assertIn("anti_detection", agent.config)
        self.assertIn("skill_training", agent.config)

    def test_create_osrs_ai_agent_custom(self):
        """Test creating OSRS agent with custom config"""
        custom_config = {
            "templates_dir": "/custom/path",
            "action_delay": 1.0,
            "custom_setting": "test",
        }

        agent = create_osrs_ai_agent(custom_config)

        self.assertIsInstance(agent, OSRSAIAgent)
        self.assertEqual(agent.config["templates_dir"], "/custom/path")
        self.assertEqual(agent.config["action_delay"], 1.0)
        self.assertEqual(agent.config["custom_setting"], "test")
        # Should still have defaults
        self.assertIn("anti_detection", agent.config)


def run_osrs_ai_tests():
    """Run all OSRS AI agent tests"""
    print("🏰 Running OSRS AI Agent Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestOSRSEnums,
        TestOSRSPlayerStats,
        TestOSRSInventoryItem,
        TestOSRSGameData,
        TestOSRSWoodcuttingTrainer,
        TestOSRSFishingTrainer,
        TestOSRSCombatTrainer,
        TestOSRSGrandExchangeBot,
        TestOSRSAntiDetection,
        TestOSRSAIAgent,
        TestCreateOSRSAIAgent,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 OSRS AI AGENT TEST RESULTS:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\n🎉 ALL OSRS AI AGENT TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME OSRS AI AGENT TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_osrs_ai_tests()
    sys.exit(0 if success else 1)
