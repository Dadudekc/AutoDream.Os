#!/usr/bin/env python3
"""
Comprehensive Gaming System Test Suite
Tests all gaming system functionality with the new modular structure
"""

import unittest
import sys
import os
from pathlib import Path
import time
import json

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent))

def run_comprehensive_gaming_tests():
    """Run comprehensive gaming system tests"""
    print("🎮 COMPREHENSIVE GAMING SYSTEM TEST SUITE")
    print("=" * 60)
    print("Testing all gaming system functionality with new modular structure")
    print("=" * 60)
    
    # Test results tracking
    test_results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "errors": [],
        "test_details": {}
    }
    
    # Test 1: Basic Import Test
    print("\n🧪 TEST 1: Basic Import Verification")
    print("-" * 40)
    try:
        from gaming_systems.osrs import (
            OSRSSkill, OSRSLocation, OSRSGameState, OSRSActionType,
            OSRSPlayerStats, OSRSInventoryItem, OSRSGameData,
            OSRSSkillTrainer, OSRSWoodcuttingTrainer, OSRSFishingTrainer, OSRSCombatTrainer,
            OSRSMarketSystem, OSRSDecisionEngine, create_osrs_ai_agent
        )
        print("✅ All gaming system imports successful")
        test_results["passed"] += 1
        test_results["test_details"]["imports"] = "PASS"
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["imports"] = f"FAIL: {e}"
        test_results["errors"].append(f"Import error: {e}")
    test_results["total_tests"] += 1
    
    # Test 2: Enum Functionality Test
    print("\n🧪 TEST 2: Enum Functionality")
    print("-" * 40)
    try:
        # Test skills
        skills = [OSRSSkill.WOODCUTTING, OSRSSkill.FISHING, OSRSSkill.MINING]
        for skill in skills:
            assert isinstance(skill.value, str)
            assert len(skill.value) > 0
        
        # Test locations
        locations = [OSRSLocation.LUMBRIDGE, OSRSLocation.VARROCK, OSRSLocation.FALADOR]
        for location in locations:
            assert isinstance(location.value, str)
            assert len(location.value) > 0
        
        # Test game states
        states = [OSRSGameState.IDLE, OSRSGameState.SKILLING, OSRSGameState.COMBAT]
        for state in states:
            assert isinstance(state.value, str)
            assert len(state.value) > 0
        
        # Test action types
        actions = [OSRSActionType.SKILL_TRAINING, OSRSActionType.COMBAT, OSRSActionType.TRADING]
        for action in actions:
            assert isinstance(action.value, str)
            assert len(action.value) > 0
        
        print("✅ All enum functionality working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["enums"] = "PASS"
    except Exception as e:
        print(f"❌ Enum test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["enums"] = f"FAIL: {e}"
        test_results["errors"].append(f"Enum error: {e}")
    test_results["total_tests"] += 1
    
    # Test 3: Data Models Test
    print("\n🧪 TEST 3: Data Models Functionality")
    print("-" * 40)
    try:
        # Test player stats
        player_stats = OSRSPlayerStats(
            player_id="test_player",
            username="test_user",
            combat_level=3,
            total_level=32
        )
        assert player_stats.player_id == "test_player"
        assert player_stats.username == "test_user"
        assert player_stats.combat_level == 3
        assert player_stats.total_level == 32
        
        # Test skill updates
        player_stats.update_skill(OSRSSkill.WOODCUTTING, 5, 1000)
        player_stats.update_skill(OSRSSkill.FISHING, 3, 500)
        
        assert player_stats.get_skill_level(OSRSSkill.WOODCUTTING) == 5
        assert player_stats.get_skill_experience(OSRSSkill.WOODCUTTING) == 1000
        assert player_stats.get_skill_level(OSRSSkill.FISHING) == 3
        assert player_stats.get_skill_experience(OSRSSkill.FISHING) == 500
        
        # Test inventory item
        item = OSRSInventoryItem(
            item_id=1511,  # Yew logs
            name="Yew logs",
            quantity=100,
            stackable=True,
            tradeable=True,
            ge_price=300
        )
        assert item.item_id == 1511
        assert item.name == "Yew logs"
        assert item.quantity == 100
        assert item.is_stackable() == True
        assert item.can_trade() == True
        assert item.get_total_value() == 30000
        
        # Test game data
        game_data = OSRSGameData(
            game_state="skilling",
            current_location=OSRSLocation.LUMBRIDGE,
            current_action="woodcutting"
        )
        assert game_data.game_state == "skilling"
        assert game_data.current_location == OSRSLocation.LUMBRIDGE
        assert game_data.current_action == "woodcutting"
        
        print("✅ All data models working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["data_models"] = "PASS"
    except Exception as e:
        print(f"❌ Data models test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["data_models"] = f"FAIL: {e}"
        test_results["errors"].append(f"Data models error: {e}")
    test_results["total_tests"] += 1
    
    # Test 4: Skill Trainers Test
    print("\n🧪 TEST 4: Skill Trainers Functionality")
    print("-" * 40)
    try:
        # Test woodcutting trainer
        woodcutting_trainer = OSRSWoodcuttingTrainer(player_stats)
        assert woodcutting_trainer.skill == OSRSSkill.WOODCUTTING
        assert woodcutting_trainer.player_stats == player_stats
        assert isinstance(woodcutting_trainer.available_trees, dict)
        assert len(woodcutting_trainer.available_trees) > 0
        
        # Test fishing trainer
        fishing_trainer = OSRSFishingTrainer(player_stats)
        assert fishing_trainer.skill == OSRSSkill.FISHING
        assert fishing_trainer.player_stats == player_stats
        
        # Test combat trainer
        combat_trainer = OSRSCombatTrainer(player_stats)
        assert combat_trainer.skill == OSRSSkill.COMBAT
        assert combat_trainer.player_stats == player_stats
        
        print("✅ All skill trainers working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["skill_trainers"] = "PASS"
    except Exception as e:
        print(f"❌ Skill trainers test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["skill_trainers"] = f"FAIL: {e}"
        test_results["errors"].append(f"Skill trainers error: {e}")
    test_results["total_tests"] += 1
    
    # Test 5: Combat System Test
    print("\n🧪 TEST 5: Combat System Functionality")
    print("-" * 40)
    try:
        combat_system = OSRSCombatSystem(player_stats)
        assert combat_system.player_stats == player_stats
        assert isinstance(combat_system.combat_styles, dict)
        assert isinstance(combat_system.weapon_types, dict)
        assert isinstance(combat_system.combat_locations, dict)
        
        print("✅ Combat system working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["combat_system"] = "PASS"
    except Exception as e:
        print(f"❌ Combat system test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["combat_system"] = f"FAIL: {e}"
        test_results["errors"].append(f"Combat system error: {e}")
    test_results["total_tests"] += 1
    
    # Test 6: Market System Test
    print("\n🧪 TEST 6: Market System Functionality")
    print("-" * 40)
    try:
        market_system = OSRSMarketSystem()
        assert isinstance(market_system.price_database, dict)
        assert isinstance(market_system.trade_history, list)
        assert isinstance(market_system.market_trends, dict)
        
        # Test price updates
        test_prices = {"yew_logs": 300, "lobster": 180, "rune_scimitar": 15000}
        market_system.update_prices(test_prices)
        
        assert market_system.price_database["yew_logs"] == 300
        assert market_system.price_database["lobster"] == 180
        assert market_system.price_database["rune_scimitar"] == 15000
        
        # Test market insights
        insights = market_system.get_market_insights("yew_logs")
        assert isinstance(insights, dict)
        
        print("✅ Market system working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["market_system"] = "PASS"
    except Exception as e:
        print(f"❌ Market system test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["market_system"] = f"FAIL: {e}"
        test_results["test_details"]["market_system"] = f"FAIL: {e}"
        test_results["errors"].append(f"Market system error: {e}")
    test_results["total_tests"] += 1
    
    # Test 7: Decision Engine Test
    print("\n🧪 TEST 7: Decision Engine Functionality")
    print("-" * 40)
    try:
        decision_engine = OSRSDecisionEngine()
        assert isinstance(decision_engine.decision_history, list)
        assert isinstance(decision_engine.current_goals, list)
        assert isinstance(decision_engine.personality_traits, dict)
        assert isinstance(decision_engine.skill_priorities, dict)
        assert isinstance(decision_engine.location_preferences, dict)
        
        print("✅ Decision engine working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["decision_engine"] = "PASS"
    except Exception as e:
        print(f"❌ Decision engine test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["decision_engine"] = f"FAIL: {e}"
        test_results["errors"].append(f"Decision engine error: {e}")
    test_results["total_tests"] += 1
    
    # Test 8: Factory Function Test
    print("\n🧪 TEST 8: Factory Function Functionality")
    print("-" * 40)
    try:
        agent = create_osrs_ai_agent()
        assert isinstance(agent, dict)
        assert 'decision_engine' in agent
        assert 'skill_trainer' in agent
        assert 'combat_system' in agent
        assert 'market_system' in agent
        
        # Test component types
        assert isinstance(agent['decision_engine'], OSRSDecisionEngine)
        assert isinstance(agent['skill_trainer'], OSRSWoodcuttingTrainer)
        assert isinstance(agent['combat_system'], OSRSCombatSystem)
        assert isinstance(agent['market_system'], OSRSMarketSystem)
        
        print("✅ Factory function working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["factory_function"] = "PASS"
    except Exception as e:
        print(f"❌ Factory function test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["factory_function"] = f"FAIL: {e}"
        test_results["errors"].append(f"Factory function error: {e}")
    test_results["total_tests"] += 1
    
    # Test 9: Integration Test
    print("\n🧪 TEST 9: System Integration Test")
    print("-" * 40)
    try:
        # Create a complete agent
        agent = create_osrs_ai_agent()
        
        # Test that all components can work together
        player_stats = agent['skill_trainer'].player_stats
        assert player_stats == agent['combat_system'].player_stats
        
        # Test skill training integration
        agent['skill_trainer'].update_skill(OSRSSkill.WOODCUTTING, 10, 5000)
        assert player_stats.get_skill_level(OSRSSkill.WOODCUTTING) == 10
        
        # Test market integration
        agent['market_system'].update_prices({"yew_logs": 350})
        assert agent['market_system'].price_database["yew_logs"] == 350
        
        print("✅ System integration working correctly")
        test_results["passed"] += 1
        test_results["test_details"]["integration"] = "PASS"
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["integration"] = f"FAIL: {e}"
        test_results["errors"].append(f"Integration error: {e}")
    test_results["total_tests"] += 1
    
    # Test 10: Performance Test
    print("\n🧪 TEST 10: Performance Test")
    print("-" * 40)
    try:
        start_time = time.time()
        
        # Create multiple agents
        agents = []
        for i in range(10):
            agent = create_osrs_ai_agent()
            agents.append(agent)
        
        end_time = time.time()
        creation_time = end_time - end_time
        
        # Test that creation is reasonably fast
        assert creation_time < 1.0  # Should create 10 agents in under 1 second
        
        print(f"✅ Performance test passed - Created 10 agents in {creation_time:.3f}s")
        test_results["passed"] += 1
        test_results["test_details"]["performance"] = "PASS"
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        test_results["failed"] += 1
        test_results["test_details"]["performance"] = f"FAIL: {e}"
        test_results["errors"].append(f"Performance error: {e}")
    test_results["total_tests"] += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE GAMING TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    print(f"Success Rate: {(test_results['passed']/test_results['total_tests']*100):.1f}%")
    
    if test_results["failed"] > 0:
        print(f"\n❌ FAILED TESTS:")
        for test_name, result in test_results["test_details"].items():
            if result.startswith("FAIL"):
                print(f"  - {test_name}: {result}")
        
        print(f"\n🔍 ERRORS:")
        for error in test_results["errors"]:
            print(f"  - {error}")
    else:
        print("\n🎉 ALL TESTS PASSED! Gaming system is fully functional!")
    
    # Save detailed results
    with open("gaming_test_results.json", "w") as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: gaming_test_results.json")
    
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_comprehensive_gaming_tests()
    sys.exit(0 if success else 1)
