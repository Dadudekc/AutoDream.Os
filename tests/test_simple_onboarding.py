#!/usr/bin/env python3
"""
Test Simple Onboarding UI Flow
==============================

Smoke test for the simple onboarding system to ensure UI path is chosen correctly.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.simple_onboarding import SimpleOnboarding, SIMPLE_ROLES_DEFAULT


class TestSimpleOnboarding(unittest.TestCase):
    """Test cases for SimpleOnboarding UI flow."""
    
    def test_simple_onboarding_initialization(self):
        """Test SimpleOnboarding initialization with default roles."""
        onboarding = SimpleOnboarding()
        
        self.assertEqual(len(onboarding.role_map), 8)
        self.assertIn("Agent-1", onboarding.role_map)
        self.assertIn("Agent-8", onboarding.role_map)
        self.assertEqual(onboarding.role_map["Agent-1"], "SSOT")
        self.assertEqual(onboarding.role_map["Agent-7"], "CLI-Orchestrator")
        self.assertFalse(onboarding.dry_run)
    
    def test_simple_onboarding_dry_run(self):
        """Test SimpleOnboarding dry run mode."""
        onboarding = SimpleOnboarding(dry_run=True)
        
        self.assertTrue(onboarding.dry_run)
        self.assertEqual(len(onboarding.role_map), 8)
    
    def test_simple_onboarding_custom_roles(self):
        """Test SimpleOnboarding with custom role map."""
        custom_roles = {"Agent-1": "CustomRole", "Agent-2": "AnotherRole"}
        onboarding = SimpleOnboarding(role_map=custom_roles)
        
        self.assertEqual(onboarding.role_map, custom_roles)
        self.assertEqual(len(onboarding.role_map), 2)
    
    def test_wrap_up_message_generation(self):
        """Test wrap-up message generation."""
        onboarding = SimpleOnboarding()
        
        wrap_msg = onboarding._wrap_up_msg("Agent-7", "CLI-Orchestrator")
        
        self.assertIn("Agent-7", wrap_msg)
        self.assertIn("CLI-Orchestrator", wrap_msg)
        self.assertIn("WRAP-UP REQUEST", wrap_msg)
        self.assertIn("Timestamp:", wrap_msg)
    
    def test_onboarding_message_generation(self):
        """Test onboarding message generation."""
        onboarding = SimpleOnboarding()
        
        ob_msg = onboarding._onboarding_msg("Agent-7", "CLI-Orchestrator")
        
        self.assertIn("Agent-7", ob_msg)
        self.assertIn("CLI-Orchestrator", ob_msg)
        self.assertIn("AGENT IDENTITY CONFIRMATION", ob_msg)
        self.assertIn("PRIMARY RESPONSIBILITIES", ob_msg)
        self.assertIn("--get-next-task", ob_msg)
    
    @patch('services.simple_onboarding.pg')
    def test_dry_run_execution(self, mock_pg):
        """Test dry run execution without UI side effects."""
        onboarding = SimpleOnboarding(dry_run=True)
        
        # Mock coordinate loading
        with patch.object(onboarding, '_load_coordinates') as mock_load_coords:
            mock_load_coords.return_value = {
                "Agent-1": {"chat_input": [100, 200], "onboarding_input": [300, 400]},
                "Agent-2": {"chat_input": [150, 250], "onboarding_input": [350, 450]}
            }
            
            result = onboarding.execute()
            
            # Should succeed in dry run
            self.assertTrue(result["success"])
            self.assertEqual(result["total_count"], 8)
            self.assertGreater(result["success_count"], 0)
            
            # PyAutoGUI should not be called in dry run
            mock_pg.click.assert_not_called()
            mock_pg.hotkey.assert_not_called()
            mock_pg.write.assert_not_called()
    
    def test_coordinate_loading_failure(self):
        """Test handling of coordinate loading failure."""
        onboarding = SimpleOnboarding()
        
        with patch.object(onboarding, '_load_coordinates') as mock_load_coords:
            mock_load_coords.return_value = None
            
            result = onboarding.execute()
            
            self.assertFalse(result["success"])
            self.assertIn("error", result)
    
    def test_agent_onboarding_missing_coordinates(self):
        """Test agent onboarding with missing coordinates."""
        onboarding = SimpleOnboarding()
        
        with patch.object(onboarding, '_load_coordinates') as mock_load_coords:
            mock_load_coords.return_value = {
                "Agent-1": {"chat_input": [0, 0], "onboarding_input": [0, 0]}
            }
            
            result = onboarding.execute()
            
            # Should fail due to missing coordinates
            self.assertFalse(result["success"])
            self.assertEqual(result["success_count"], 0)


class TestSimpleOnboardingIntegration(unittest.TestCase):
    """Integration tests for SimpleOnboarding."""
    
    def test_simple_ui_smoke(self):
        """Smoke test to ensure simple UI path is chosen correctly."""
        # This test ensures the simple onboarding path works
        # without requiring the full hard onboarding dependencies
        
        onboarding = SimpleOnboarding(dry_run=True)
        
        # Should be able to initialize without errors
        self.assertIsNotNone(onboarding)
        self.assertEqual(len(onboarding.role_map), 8)
        
        # Should have all expected roles
        expected_roles = ["SSOT", "SOLID", "DRY", "KISS", "TDD", 
                         "Observability", "CLI-Orchestrator", "Docs-Governor"]
        actual_roles = list(onboarding.role_map.values())
        
        for role in expected_roles:
            self.assertIn(role, actual_roles)


if __name__ == '__main__':
    unittest.main()
