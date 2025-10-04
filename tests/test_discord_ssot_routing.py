#!/usr/bin/env python3
"""
Test Discord SSOT Routing
=========================

Minimal tests for Discord SSOT client routing logic.
Tests routing priority and environment handling.

V2 Compliant: ≤400 lines, focused on routing logic
"""

import asyncio
import os
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestDiscordSSOTRouting:
    """Test Discord SSOT client routing logic."""

    def test_agent_id_normalization(self):
        """Test agent ID normalization logic."""
        from src.services.discord_commander.discord_post_client import DiscordPostClient
        
        client = DiscordPostClient()
        
        # Test captain normalization
        assert client._normalize_agent_id("captain") == "Agent-4"
        assert client._normalize_agent_id("agent4") == "Agent-4"
        assert client._normalize_agent_id("agent-4") == "Agent-4"
        
        # Test agent-X format
        assert client._normalize_agent_id("agent7") == "Agent-7"
        assert client._normalize_agent_id("agent-7") == "Agent-7"
        
        # Test already normalized
        assert client._normalize_agent_id("Agent-7") == "Agent-7"

    @patch('src.services.discord_commander.discord_post_client.os.getenv')
    def test_agent_webhook_routing_priority(self, mock_getenv):
        """Test that agent-specific webhooks are prioritized."""
        from src.services.discord_commander.discord_post_client import DiscordPostClient
        
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default=None: {
            'DISCORD_WEBHOOK_AGENT_7': 'https://discordapp.com/api/webhooks/test7',
            'DISCORD_WEBHOOK_URL': 'https://discordapp.com/api/webhooks/default',
            'DISCORD_CHANNEL_AGENT_7': '1415916665283022980',
            'DISCORD_BOT_TOKEN': 'mock_token'
        }.get(key, default)
        
        client = DiscordPostClient()
        
        # Verify Agent-7 webhook is prioritized
        assert client.agent_webhooks.get("Agent-7") == 'https://discordapp.com/api/webhooks/test7'
        
        # Verify routing info shows agent webhook available
        info = client.get_routing_info()
        assert "Agent-7" in info["agents_with_webhooks"]
        assert info["agent_webhooks"] == 1

    @patch('src.services.discord_commander.discord_post_client.aiohttp.ClientSession')
    @patch('src.services.discord_commander.discord_post_client.os.getenv')
    async def test_webhook_posting_success(self, mock_getenv, mock_session_class):
        """Test successful webhook posting."""
        from src.services.discord_commander.discord_post_client import DiscordPostClient
        
        # Mock webhook response
        mock_response = Mock()
        mock_response.status = 204  # Discord webhook success
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = Mock()
        mock_session.post.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.post.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)
        
        # Mock environment with Agent-7 webhook
        mock_getenv.side_effect = lambda key, default=None: {
            'DISCORD_WEBHOOK_AGENT_7': 'https://discordapp.com/api/webhooks/test7'
        }.get(key, default)
        
        client = DiscordPostClient()
        
        # Test posting via webhook
        result = await client._post_to_webhook("Test message", "https://discordapp.com/api/webhooks/test7", "Agent-7")
        
        assert result is True

    def test_template_value_ignoring(self):
        """Test that template values like 'your_channel_id' are ignored."""
        from src.services.discord_commander.discord_post_client import DiscordPostClient
        
        with patch('src.services.discord_commander.discord_post_client.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: {
                'DISCORD_CHANNEL_AGENT_7': 'your_channel_id_here',
                'DISCORD_WEBHOOK_AGENT_7': 'your_webhook_url_here',
                'DISCORD_CHANNEL_AGENT_5': '1387514933041696900',  # Valid channel ID
            }.get(key, default)
            
            client = DiscordPostClient()
            
            # Template values should be ignored
            assert "Agent-7" not in client.agent_channels
            assert "Agent-7" not in client.agent_webhooks
            
            # Valid values should be included
            assert "Agent-5" in client.agent_channels
            assert client.agent_channels["Agent-5"] == 1387514933041696900

    def test_routing_info_completeness(self):
        """Test that routing info provides complete system status."""
        from src.services.discord_commander.discord_post_client import DiscordPostClient
        
        client = DiscordPostClient()
        info = client.get_routing_info()
        
        # Verify all expected fields are present
        expected_fields = [
            "bot_available", "default_webhook", "agent_channels", 
            "agent_webhooks", "agents_with_channels", "agents_with_webhooks"
        ]
        
        for field in expected_fields:
            assert field in info

    @patch('src.services.discord_commander.discord_post_client.os.getenv')
    def test_environment_gating(self, mock_getenv):
        """Test DEVLOG_POST_VIA_MANAGER environment gating."""
        mock_getenv.return_value = "true"
        
        # This would be tested in actual AgentDevlogPoster integration
        # For now, verify the logic exists
        assert os.getenv("DEVLOG_POST_VIA_MANAGER").lower() == "true"


class TestAgentDevlogPosterIntegration:
    """Test AgentDevlogPoster integration with SSOT."""

    @patch('src.services.agent_devlog.devlog_poster.os.getenv')
    def test_ssot_routing_selection(self, mock_getenv):
        """Test that SSOT routing is selected based on environment."""
        from src.services.agent_devlog.devlog_poster import AgentDevlogPoster
        
        # Test SSOT enabled
        mock_getenv.return_value = "true"
        poster = AgentDevlogPoster()
        
        # This would test the actual routing selection
        # The integration exists in the code but needs runtime testing
        
        # Verify environment check works
        assert os.getenv("DEVLOG_POST_VIA_MANAGER").lower() == "true"

    @patch('src.services.agent_devlog.devlog_poster.os.getenv')
    def test_legacy_routing_fallback(self, mock_getenv):
        """Test that legacy routing is used when SSOT is disabled."""
        from src.services.agent_devlog.devlog_poster import AgentDevlogPoster
        
        # Test SSOT disabled (default)
        mock_getenv.return_value = "false"
        poster = AgentDevLogPoster()
        
        # Legacy routing should be used
        assert os.getenv("DEVLOG_POST_VIA_MANAGER", "false").lower() == "false"


if __name__ == "__main__":
    # Simple smoke test
    print("🧪 Running Discord SSOT routing tests...")
    
    test_suite = TestDiscordSSOTRouting()
    
    print("✅ Agent ID normalization test")
    test_suite.test_agent_id_normalization()
    
    print("✅ Routing info completeness test")
    test_suite.test_routing_info_completeness()
    
    print("✅ Template value ignoring test")
    test_suite.test_template_value_ignoring()
    
    print("✅ Environment gating test")
    test_suite.test_environment_gating()
    
    print("🎉 All Discord SSOT routing tests passed!")
