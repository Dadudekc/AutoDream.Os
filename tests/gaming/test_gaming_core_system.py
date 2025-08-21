#!/usr/bin/env python3
"""
Test Suite for Gaming Core System
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- Gaming core system initialization
- Game object management
- AI agent integration
- Performance monitoring
- Event handling
"""

import unittest
import sys
import os
import time
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.gaming_core_system import (
    GamingCoreSystem, 
    GameConfig, 
    GameState, 
    GameObject, 
    AIGamingAgent
)

class TestGameConfig(unittest.TestCase):
    """Test GameConfig data class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = GameConfig()
        self.assertEqual(config.title, "Agent_Cellphone_V2 Gaming System")
        self.assertEqual(config.width, 1024)
        self.assertEqual(config.height, 768)
        self.assertEqual(config.fps, 60)
        self.assertFalse(config.fullscreen)
        self.assertTrue(config.vsync)
        self.assertFalse(config.debug)
    
    def test_custom_config(self):
        """Test custom configuration values"""
        config = GameConfig(
            title="Test Game",
            width=800,
            height=600,
            fps=30,
            fullscreen=True,
            vsync=False,
            debug=True
        )
        self.assertEqual(config.title, "Test Game")
        self.assertEqual(config.width, 800)
        self.assertEqual(config.height, 600)
        self.assertEqual(config.fps, 30)
        self.assertTrue(config.fullscreen)
        self.assertFalse(config.vsync)
        self.assertTrue(config.debug)

class TestGameObject(unittest.TestCase):
    """Test GameObject base class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game_object = GameObject(x=100, y=200)
    
    def test_initialization(self):
        """Test GameObject initialization"""
        self.assertEqual(self.game_object.x, 100)
        self.assertEqual(self.game_object.y, 200)
        self.assertTrue(self.game_object.visible)
        self.assertTrue(self.game_object.active)
    
    def test_update_method(self):
        """Test GameObject update method"""
        # Should not raise any exceptions
        self.game_object.update(0.016)  # 60 FPS delta time
    
    def test_render_method(self):
        """Test GameObject render method"""
        # Should not raise any exceptions
        mock_screen = Mock()
        self.game_object.render(mock_screen)

class TestAIGamingAgent(unittest.TestCase):
    """Test AIGamingAgent base class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = AIGamingAgent("test_agent")
    
    def test_initialization(self):
        """Test AIGamingAgent initialization"""
        self.assertEqual(self.agent.name, "test_agent")
        self.assertTrue(self.agent.active)
        self.assertEqual(self.agent.intelligence_level, 1.0)
        self.assertEqual(len(self.agent.decision_memory), 0)
    
    def test_update_method(self):
        """Test AIGamingAgent update method"""
        # Should not raise any exceptions
        self.agent.update(0.016)  # 60 FPS delta time
    
    def test_render_method(self):
        """Test AIGamingAgent render method"""
        # Should not raise any exceptions
        mock_screen = Mock()
        self.agent.render(mock_screen)
    
    def test_make_decision_method(self):
        """Test AIGamingAgent decision making"""
        game_state = {"player_health": 100, "enemy_count": 3}
        decision = self.agent.make_decision(game_state)
        # Base implementation should return None
        self.assertIsNone(decision)
    
    def test_learn_method(self):
        """Test AIGamingAgent learning"""
        experience = {"action": "attack", "reward": 10, "state": "enemy_nearby"}
        # Should not raise any exceptions
        self.agent.learn(experience)

class TestGamingCoreSystem(unittest.TestCase):
    """Test GamingCoreSystem main class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use a minimal config for testing
        self.config = GameConfig(
            title="Test Game",
            width=800,
            height=600,
            fps=60,
            debug=True
        )
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_initialization(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test GamingCoreSystem initialization"""
        # Mock pygame components
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        # Verify pygame was initialized
        mock_init.assert_called_once()
        mock_mixer.assert_called_once()
        mock_display.assert_called_once()
        mock_caption.assert_called_once_with("Test Game")
        mock_clock.assert_called_once()
        
        # Verify system state
        self.assertEqual(gaming_system.state, GameState.INITIALIZING)
        self.assertIsNotNone(gaming_system.screen)
        self.assertIsNotNone(gaming_system.clock)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_add_game_object(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test adding game objects"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        game_object = GameObject(100, 200)
        
        gaming_system.add_game_object("test_obj", game_object)
        
        self.assertIn("test_obj", gaming_system.game_objects)
        self.assertEqual(gaming_system.game_objects["test_obj"], game_object)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_add_ai_agent(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test adding AI agents"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        ai_agent = AIGamingAgent("test_agent")
        
        gaming_system.add_ai_agent("test_agent", ai_agent)
        
        self.assertIn("test_agent", gaming_system.ai_agents)
        self.assertEqual(gaming_system.ai_agents["test_agent"], ai_agent)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_add_event_handler(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test adding event handlers"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        def test_handler(event):
            pass
        
        gaming_system.add_event_handler(123, test_handler)
        
        self.assertIn(123, gaming_system.event_handlers)
        self.assertIn(test_handler, gaming_system.event_handlers[123])
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_game_state_management(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test game state management"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        # Test pause/resume
        gaming_system.state = GameState.RUNNING
        gaming_system.pause()
        self.assertEqual(gaming_system.state, GameState.PAUSED)
        
        gaming_system.resume()
        self.assertEqual(gaming_system.state, GameState.RUNNING)
        
        # Test stop
        gaming_system.stop()
        self.assertEqual(gaming_system.state, GameState.STOPPED)
        self.assertFalse(gaming_system.running)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_performance_monitoring(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test performance monitoring"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_clock_instance.get_fps.return_value = 60.0
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        # Add some objects to test metrics
        gaming_system.add_game_object("obj1", GameObject())
        gaming_system.add_ai_agent("agent1", AIGamingAgent("test"))
        
        # Simulate performance update
        gaming_system._update_performance_metrics(0.016)
        
        metrics = gaming_system.get_performance_report()
        self.assertIn('fps', metrics)
        self.assertIn('frame_time', metrics)
        self.assertIn('active_objects', metrics)
        self.assertIn('active_agents', metrics)
        
        self.assertEqual(metrics['active_objects'], 1)
        self.assertEqual(metrics['active_agents'], 1)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_status_report(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test status reporting"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        status = gaming_system.get_status_report()
        
        self.assertIn('state', status)
        self.assertIn('running', status)
        self.assertIn('game_objects_count', status)
        self.assertIn('ai_agents_count', status)
        self.assertIn('performance_metrics', status)
        
        self.assertEqual(status['state'], 'initializing')
        self.assertFalse(status['running'])
        self.assertEqual(status['game_objects_count'], 0)
        self.assertEqual(status['ai_agents_count'], 0)

class TestGamingSystemIntegration(unittest.TestCase):
    """Test integration between gaming system components"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use a minimal config for testing
        self.config = GameConfig(
            title="Test Game",
            width=800,
            height=600,
            fps=60,
            debug=True
        )
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_game_object_integration(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test integration of game objects with the system"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        # Create a custom game object
        class CustomGameObject(GameObject):
            def __init__(self):
                super().__init__(100, 200)
                self.update_called = False
                self.render_called = False
            
            def update(self, dt):
                self.update_called = True
            
            def render(self, screen):
                self.render_called = True
        
        custom_obj = CustomGameObject()
        gaming_system.add_game_object("custom", custom_obj)
        
        # Test update integration
        gaming_system.update(0.016)
        self.assertTrue(custom_obj.update_called)
        
        # Test render integration
        gaming_system.render()
        self.assertTrue(custom_obj.render_called)
    
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_ai_agent_integration(self, mock_clock, mock_caption, mock_display, mock_mixer, mock_init):
        """Test integration of AI agents with the system"""
        mock_screen = Mock()
        mock_clock_instance = Mock()
        mock_display.return_value = mock_screen
        mock_clock.return_value = mock_clock_instance
        
        gaming_system = GamingCoreSystem(self.config)
        
        # Create a custom AI agent
        class CustomAIAgent(AIGamingAgent):
            def __init__(self):
                super().__init__("custom_ai")
                self.update_called = False
                self.render_called = False
            
            def update(self, dt):
                self.update_called = True
            
            def render(self, screen):
                self.render_called = True
        
        custom_agent = CustomAIAgent()
        gaming_system.add_ai_agent("custom_ai", custom_agent)
        
        # Test update integration
        gaming_system.update(0.016)
        self.assertTrue(custom_agent.update_called)
        
        # Test render integration
        gaming_system.render()
        self.assertTrue(custom_agent.render_called)

def run_gaming_tests():
    """Run all gaming tests"""
    print("🧪 Running Gaming Core System Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestGameConfig,
        TestGameObject,
        TestAIGamingAgent,
        TestGamingCoreSystem,
        TestGamingSystemIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 GAMING CORE SYSTEM TEST RESULTS:")
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
        print("\n🎉 ALL GAMING TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME GAMING TESTS FAILED!")
        return False

if __name__ == "__main__":
    success = run_gaming_tests()
    sys.exit(0 if success else 1)
