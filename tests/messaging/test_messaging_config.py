#!/usr/bin/env python3
"""
Unit Tests for Messaging Configuration - Agent Cellphone V2
==========================================================

Tests for messaging configuration management.
V2 Compliance: SSOT implementation and centralized configuration.

Author: Agent-6 (Gaming & Entertainment Specialist)
"""

from src.services.utils.agent_registry import AGENTS, list_agents


class TestMessagingConfiguration:
    """Test cases for MessagingConfiguration class."""

    def test_initialization_creates_default_config(self):
        """Test that initialization creates default configuration."""
        config = MessagingConfiguration()

        assert get_unified_validator().validate_hasattr(config, 'agents')
        assert get_unified_validator().validate_hasattr(config, 'inbox_paths')
        assert get_unified_validator().validate_type(config.agents, dict)
        assert get_unified_validator().validate_type(config.inbox_paths, dict)

    def test_default_agents_configuration(self):
        """Test default agent configuration structure."""
        config = MessagingConfiguration()

        # Check that all expected agents are present
        expected_agents = list_agents()
        for agent in expected_agents:
            assert agent in config.agents
            assert 'description' in config.agents[agent]
            assert 'coords' in config.agents[agent]

    def test_default_inbox_paths_configuration(self):
        """Test default inbox paths configuration."""
        config = MessagingConfiguration()

        # Check that inbox paths are configured for all agents
        expected_agents = list_agents()
        for agent in expected_agents:
            expected_path = f"agent_workspaces/{agent}/inbox"
            assert config.inbox_paths[agent] == expected_path

    def test_agent_coordinates_structure(self):
        """Test that agent coordinates are properly structured."""
        config = MessagingConfiguration()

        for agent, agent_config in config.agents.items():
            coords = agent_config['coords']
            assert get_unified_validator().validate_type(coords, tuple)
            assert len(coords) == 2
            assert all(get_unified_validator().validate_type(coord, int) for coord in coords)

    @patch('src.utils.config_core.get_config')
    def test_centralized_config_integration(self, mock_get_config):
        """Test integration with centralized configuration system."""
        # Mock the centralized config calls
        mock_get_config.side_effect = lambda key, default=None: {
            "AGENT_COUNT": 8,
            "CAPTAIN_ID": "Agent-4"
        }.get(key, default)

        config = MessagingConfiguration()

        # Verify that get_config was called
        assert mock_get_config.called

    @patch('src.services.messaging_config.get_unified_utility().path.exists')
    @patch('src.services.messaging_config.open', new_callable=mock_open)
    @patch('src.services.messaging_config.json.load')
    def test_config_file_loading(self, mock_json_load, mock_file, mock_exists):
        """Test loading configuration from JSON file."""
        mock_exists.return_value = True
        mock_json_load.return_value = {
            'agents': {
                'Agent-9': {'description': 'Test Agent', 'coords': [100, 200]}
            },
            'inbox_paths': {
                'Agent-9': 'custom/path'
            }
        }

        config = MessagingConfiguration()

        # Verify file operations were attempted
        mock_exists.assert_called_with("config/messaging_config.json")
        mock_file.assert_called()

    @patch('src.services.messaging_config.get_unified_utility().path.exists')
    def test_config_file_not_found_handling(self, mock_exists):
        """Test graceful handling when config file doesn't exist."""
        mock_exists.return_value = False

        config = MessagingConfiguration()

        # Should not raise exception, should use defaults
        assert len(config.agents) == 8  # Default agent count
        assert len(config.inbox_paths) == 8

    @patch('src.services.messaging_config.get_unified_utility().path.exists')
    @patch('src.services.messaging_config.open', new_callable=mock_open)
    @patch('src.services.messaging_config.json.load')
    def test_config_file_partial_override(self, mock_json_load, mock_file, mock_exists):
        """Test that config file can partially override defaults."""
        mock_exists.return_value = True
        mock_json_load.return_value = {
            'agents': {
                'Agent-1': {'description': 'Updated Agent', 'coords': [999, 999]}
            }
        }

        config = MessagingConfiguration()

        # Agent-1 should be updated
        assert config.agents['Agent-1']['description'] == 'Updated Agent'
        assert config.agents['Agent-1']['coords'] == [999, 999]

        # Other agents should retain defaults
        assert config.agents['Agent-2']['description'] == 'Architecture & Design Specialist'

    def test_agent_description_accuracy(self):
        """Test that agent descriptions are accurate."""
        config = MessagingConfiguration()

        expected_descriptions = {agent: info['description'] for agent, info in AGENTS.items()}

        for agent, expected_desc in expected_descriptions.items():
            assert config.agents[agent]['description'] == expected_desc

    def test_coordinate_uniqueness(self):
        """Test that all agent coordinates are unique."""
        config = MessagingConfiguration()

        coords = []
        for agent_config in config.agents.values():
            coord_tuple = tuple(agent_config['coords'])
            assert coord_tuple not in coords, f"Duplicate coordinates found: {coord_tuple}"
            coords.append(coord_tuple)

    def test_inbox_path_format_consistency(self):
        """Test that inbox paths follow consistent format."""
        config = MessagingConfiguration()

        for agent, path in config.inbox_paths.items():
            assert path.startswith('agent_workspaces/')
            assert path.endswith('/inbox')
            assert agent in path

    @patch('src.utils.config_core.get_config')
    def test_error_handling_in_config_loading(self, mock_get_config):
        """Test error handling when config loading fails."""
        mock_get_config.side_effect = Exception("Config loading failed")

        # Should not raise exception, should fall back to defaults
        config = MessagingConfiguration()

        # Should still have default configuration
        assert len(config.agents) > 0
        assert len(config.inbox_paths) > 0

    def test_configuration_immutability(self):
        """Test that configuration objects are properly isolated."""
        config1 = MessagingConfiguration()
        config2 = MessagingConfiguration()

        # Modifying one should not affect the other
        original_desc = config1.agents['Agent-1']['description']
        config1.agents['Agent-1']['description'] = 'Modified'

        assert config2.agents['Agent-1']['description'] == original_desc


if __name__ == "__main__":
    pytest.main([__file__])
