from pathlib import Path
import json
import os
import sys
import tempfile

import unittest

        import shutil
from services.messaging import UnifiedPyAutoGUIMessaging
from services.messaging.campaign_messaging import CampaignMessaging
from services.messaging.coordinate_manager import CoordinateManager, AgentCoordinates
from services.messaging.interfaces import (
from services.messaging.unified_messaging_service import UnifiedMessagingService
from services.messaging.yolo_messaging import YOLOMessaging
from src.utils.stability_improvements import stability_manager, safe_import
from unittest.mock import Mock, patch, MagicMock

#!/usr/bin/env python3
"""
TDD Tests for Unified Messaging System - Agent Cellphone V2
==========================================================

Test-Driven Development approach: Write tests FIRST, then implement.
These tests define the expected behavior for ALL messaging capabilities.

Author: V2 SWARM CAPTAIN
License: MIT
"""



# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the messaging system components
    MessagingMode, MessageType, IMessageSender, IBulkMessaging,
    ICampaignMessaging, IYOLOMessaging, ICoordinateManager
)


class TestCoordinateManager(unittest.TestCase):
    """Test coordinate management functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary coordinate file
        self.temp_dir = tempfile.mkdtemp()
        self.coord_file = Path(self.temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        self.sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                },
                "Agent-2": {
                    "starter_location_box": {"x": 200, "y": 300},
                    "input_box": {"x": 250, "y": 350}
                }
            }
        }
        
        # Write test coordinates
        with open(self.coord_file, 'w') as f:
            json.dump(self.sample_coords, f)
        
        self.coord_manager = CoordinateManager(str(self.coord_file))
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_load_coordinates(self):
        """Test coordinate loading from file"""
        self.assertEqual(len(self.coord_manager.coordinates), 1)
        self.assertIn("8-agent", self.coord_manager.coordinates)
        self.assertEqual(len(self.coord_manager.coordinates["8-agent"]), 2)
    
    def test_get_agent_coordinates(self):
        """Test retrieving agent coordinates"""
        coords = self.coord_manager.get_agent_coordinates("Agent-1", "8-agent")
        self.assertIsNotNone(coords)
        self.assertEqual(coords.agent_id, "Agent-1")
        self.assertEqual(coords.starter_location, (100, 200))
        self.assertEqual(coords.input_box, (150, 250))
    
    def test_validate_coordinates(self):
        """Test coordinate validation"""
        results = self.coord_manager.validate_coordinates()
        self.assertEqual(results["total_modes"], 1)
        self.assertEqual(results["total_agents"], 2)
        self.assertEqual(results["valid_coordinates"], 2)
        self.assertEqual(results["missing_coordinates"], 0)
        self.assertEqual(len(results["errors"]), 0)
    
    def test_get_available_modes(self):
        """Test getting available coordinate modes"""
        modes = self.coord_manager.get_available_modes()
        self.assertEqual(modes, ["8-agent"])
    
    def test_get_agents_in_mode(self):
        """Test getting agents in specific mode"""
        agents = self.coord_manager.get_agents_in_mode("8-agent")
        self.assertEqual(agents, ["Agent-1", "Agent-2"])


class TestPyAutoGUIMessaging(unittest.TestCase):
    """Test PyAutoGUI messaging functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_coord_manager = Mock(spec=ICoordinateManager)
        self.mock_coords = AgentCoordinates(
            agent_id="Agent-1",
            starter_location=(100, 200),
            input_box=(150, 250),
            mode="8-agent"
        )
        self.mock_coord_manager.get_agent_coordinates.return_value = self.mock_coords
        
        self.pyautogui_messaging = PyAutoGUIMessaging(self.mock_coord_manager)
    
    @patch('src.services.messaging.pyautogui_messaging.pyautogui')
    @patch('src.services.messaging.pyautogui_messaging.pyperclip')
    def test_send_message(self, mock_pyperclip, mock_pyautogui):
        """Test sending message via PyAutoGUI"""
        # Mock PyAutoGUI methods
        mock_pyautogui.moveTo.return_value = None
        mock_pyautogui.click.return_value = None
        mock_pyautogui.hotkey.return_value = None
        mock_pyautogui.press.return_value = None
        
        # Test message sending
        result = self.pyautogui_messaging.send_message("Agent-1", "Test message")
        
        # Verify success
        self.assertTrue(result)
        
        # Verify PyAutoGUI calls
        mock_pyautogui.moveTo.assert_called_with(150, 250, duration=0.3)
        mock_pyautogui.click.assert_called()
        mock_pyautogui.hotkey.assert_called()
        mock_pyautogui.press.assert_called()
        
        # Verify clipboard usage
        mock_pyperclip.copy.assert_called_with("Agent-1\n\nTest message")
    
    def test_send_message_no_coordinates(self):
        """Test sending message when coordinates not found"""
        self.mock_coord_manager.get_agent_coordinates.return_value = None
        
        result = self.pyautogui_messaging.send_message("Agent-1", "Test message")
        self.assertFalse(result)
    
    @patch('src.services.messaging.pyautogui_messaging.pyautogui')
    def test_activate_agent(self, mock_pyautogui):
        """Test agent activation"""
        # Mock PyAutoGUI methods
        mock_pyautogui.moveTo.return_value = None
        mock_pyautogui.click.return_value = None
        
        result = self.pyautogui_messaging.activate_agent("Agent-1", "8-agent")
        
        # Verify success
        self.assertTrue(result)
        
        # Verify PyAutoGUI calls
        mock_pyautogui.moveTo.assert_called_with(100, 200, duration=0.3)
        mock_pyautogui.click.assert_called()


class TestCampaignMessaging(unittest.TestCase):
    """Test campaign messaging functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_coord_manager = Mock(spec=ICoordinateManager)
        self.mock_pyautogui_messaging = Mock(spec=IBulkMessaging)
        
        self.campaign_messaging = CampaignMessaging(
            self.mock_coord_manager, 
            self.mock_pyautogui_messaging
        )
    
    def test_send_campaign_message(self):
        """Test sending campaign message to all agents"""
        # Mock coordinate manager
        self.mock_coord_manager.get_agents_in_mode.return_value = ["Agent-1", "Agent-2"]
        
        # Mock PyAutoGUI messaging
        expected_results = {"Agent-1": True, "Agent-2": True}
        self.mock_pyautogui_messaging.send_bulk_messages.return_value = expected_results
        
        # Test campaign messaging
        results = self.campaign_messaging.send_campaign_message("Campaign message", "election")
        
        # Verify results
        self.assertEqual(results, expected_results)
        
        # Verify coordinate manager call
        self.mock_coord_manager.get_agents_in_mode.assert_called_with("8-agent")
        
        # Verify PyAutoGUI messaging call
        expected_messages = {"Agent-1": "Campaign message", "Agent-2": "Campaign message"}
        self.mock_pyautogui_messaging.send_bulk_messages.assert_called_with(
            expected_messages, "8-agent"
        )
    
    def test_send_election_broadcast(self):
        """Test election broadcast functionality"""
        # Mock dependencies
        self.mock_coord_manager.get_agents_in_mode.return_value = ["Agent-1"]
        self.mock_pyautogui_messaging.send_bulk_messages.return_value = {"Agent-1": True}
        
        results = self.campaign_messaging.send_election_broadcast("Election message")
        
        self.assertEqual(results, {"Agent-1": True})


class TestYOLOMessaging(unittest.TestCase):
    """Test YOLO messaging functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_coord_manager = Mock(spec=ICoordinateManager)
        self.mock_pyautogui_messaging = Mock(spec=IMessageSender)
        
        self.yolo_messaging = YOLOMessaging(
            self.mock_coord_manager, 
            self.mock_pyautogui_messaging
        )
    
    def test_activate_yolo_mode(self):
        """Test YOLO mode activation"""
        # Mock coordinate manager
        self.mock_coord_manager.get_agents_in_mode.return_value = ["Agent-1", "Agent-2"]
        
        # Mock PyAutoGUI messaging
        self.mock_pyautogui_messaging.activate_agent.return_value = True
        self.mock_pyautogui_messaging.send_message.return_value = True
        
        # Test YOLO mode
        results = self.yolo_messaging.activate_yolo_mode("YOLO message")
        
        # Verify results
        expected_results = {"Agent-1": True, "Agent-2": True}
        self.assertEqual(results, expected_results)
        
        # Verify activation calls
        self.mock_pyautogui_messaging.activate_agent.assert_called()
        self.mock_pyautogui_messaging.send_message.assert_called()
    
    def test_activate_single_agent_yolo(self):
        """Test single agent YOLO activation"""
        # Mock PyAutoGUI messaging
        self.mock_pyautogui_messaging.activate_agent.return_value = True
        self.mock_pyautogui_messaging.send_message.return_value = True
        
        result = self.yolo_messaging.activate_single_agent_yolo("Agent-1", "YOLO message")
        
        self.assertTrue(result)
        self.mock_pyautogui_messaging.activate_agent.assert_called_with("Agent-1", "8-agent")
        self.mock_pyautogui_messaging.send_message.assert_called_with("Agent-1", "YOLO message")


class TestUnifiedMessagingService(unittest.TestCase):
    """Test unified messaging service orchestration"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary coordinate file
        self.temp_dir = tempfile.mkdtemp()
        self.coord_file = Path(self.temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                }
            }
        }
        
        # Write test coordinates
        with open(self.coord_file, 'w') as f:
            json.dump(sample_coords, f)
        
        self.service = UnifiedMessagingService(str(self.coord_file))
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test service initialization"""
        self.assertIsNotNone(self.service.coordinate_manager)
        self.assertIsNotNone(self.service.pyautogui_messaging)
        self.assertIsNotNone(self.service.campaign_messaging)
        self.assertIsNotNone(self.service.yolo_messaging)
        self.assertEqual(self.service.active_mode, MessagingMode.PYAUTOGUI)
    
    def test_set_mode(self):
        """Test mode setting"""
        self.service.set_mode(MessagingMode.CAMPAIGN)
        self.assertEqual(self.service.active_mode, MessagingMode.CAMPAIGN)
    
    def test_send_message_pyautogui_mode(self):
        """Test sending message in PyAutoGUI mode"""
        # Mock PyAutoGUI messaging
        self.service.pyautogui_messaging.send_message = Mock(return_value=True)
        
        result = self.service.send_message("Agent-1", "Test message", mode=MessagingMode.PYAUTOGUI)
        
        self.assertTrue(result)
        self.service.pyautogui_messaging.send_message.assert_called_with("Agent-1", "Test message")
    
    def test_send_message_campaign_mode(self):
        """Test sending message in campaign mode"""
        # Mock campaign messaging
        expected_results = {"Agent-1": True}
        self.service.campaign_messaging.send_campaign_message = Mock(return_value=expected_results)
        
        result = self.service.send_message("Agent-1", "Campaign message", mode=MessagingMode.CAMPAIGN)
        
        self.assertEqual(result, expected_results)
        self.service.campaign_messaging.send_campaign_message.assert_called_with("Campaign message")
    
    def test_send_message_yolo_mode(self):
        """Test sending message in YOLO mode"""
        # Mock YOLO messaging
        expected_results = {"Agent-1": True}
        self.service.yolo_messaging.activate_yolo_mode = Mock(return_value=expected_results)
        
        result = self.service.send_message("Agent-1", "YOLO message", mode=MessagingMode.YOLO)
        
        self.assertEqual(result, expected_results)
        self.service.yolo_messaging.activate_yolo_mode.assert_called_with("YOLO message")
    
    def test_validate_coordinates(self):
        """Test coordinate validation"""
        results = self.service.validate_coordinates()
        self.assertEqual(results["total_modes"], 1)
        self.assertEqual(results["total_agents"], 1)
        self.assertEqual(results["valid_coordinates"], 1)
    
    def test_get_available_modes(self):
        """Test getting available modes"""
        modes = self.service.get_available_modes()
        self.assertEqual(modes, ["8-agent"])
    
    def test_get_agents_in_mode(self):
        """Test getting agents in mode"""
        agents = self.service.get_agents_in_mode("8-agent")
        self.assertEqual(agents, ["Agent-1"])


class TestMessagingIntegration(unittest.TestCase):
    """Test integration between messaging components"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary coordinate file
        self.temp_dir = tempfile.mkdtemp()
        self.coord_file = Path(self.temp_dir) / "test_coords.json"
        
        # Sample coordinate data
        sample_coords = {
            "8-agent": {
                "Agent-1": {
                    "starter_location_box": {"x": 100, "y": 200},
                    "input_box": {"x": 150, "y": 250}
                },
                "Agent-2": {
                    "starter_location_box": {"x": 200, "y": 300},
                    "input_box": {"x": 250, "y": 350}
                }
            }
        }
        
        # Write test coordinates
        with open(self.coord_file, 'w') as f:
            json.dump(sample_coords, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_full_messaging_workflow(self):
        """Test complete messaging workflow"""
        # Initialize all components
        coord_manager = CoordinateManager(str(self.coord_file))
        pyautogui_messaging = PyAutoGUIMessaging(coord_manager)
        campaign_messaging = CampaignMessaging(coord_manager, pyautogui_messaging)
        yolo_messaging = YOLOMessaging(coord_manager, pyautogui_messaging)
        unified_service = UnifiedMessagingService(str(self.coord_file))
        
        # Test coordinate validation
        validation_results = coord_manager.validate_coordinates()
        self.assertEqual(validation_results["valid_coordinates"], 2)
        
        # Test getting agents
        agents = coord_manager.get_agents_in_mode("8-agent")
        self.assertEqual(len(agents), 2)
        self.assertIn("Agent-1", agents)
        self.assertIn("Agent-2", agents)
        
        # Test service orchestration
        self.assertEqual(unified_service.active_mode, MessagingMode.PYAUTOGUI)
        unified_service.set_mode(MessagingMode.CAMPAIGN)
        self.assertEqual(unified_service.active_mode, MessagingMode.CAMPAIGN)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
