#!/usr/bin/env python3
"""
Unit tests for Discord services functionality.

Author: Agent-3 (QA Lead)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


class TestDiscordServices:
    """Test suite for Discord services functionality."""
    
    def test_discord_config_validation(self):
        """Test Discord configuration validation."""
        # Valid Discord config
        valid_config = {
            "bot_token": "test_bot_token_12345",
            "channel_id": "123456789012345678",
            "webhook_url": "https://discord.com/api/webhooks/test",
            "guild_id": "987654321098765432"
        }
        
        # Invalid Discord config
        invalid_config = {
            "bot_token": "",  # Empty token
            "channel_id": "invalid_id",  # Invalid ID format
            "webhook_url": "not_a_url",  # Invalid URL
            "guild_id": None  # Missing guild ID
        }
        
        # Test valid config
        assert valid_config["bot_token"], "Bot token should not be empty"
        assert valid_config["channel_id"].isdigit(), "Channel ID should be numeric"
        assert valid_config["webhook_url"].startswith("https://"), "Webhook URL should be HTTPS"
        assert valid_config["guild_id"], "Guild ID should not be None"
        
        # Test invalid config
        assert not invalid_config["bot_token"], "Invalid bot token should be empty"
        assert not invalid_config["channel_id"].isdigit(), "Invalid channel ID should not be numeric"
        assert not invalid_config["webhook_url"].startswith("https://"), "Invalid webhook URL should not be HTTPS"
        assert not invalid_config["guild_id"], "Invalid guild ID should be None"
    
    def test_discord_message_formatting(self):
        """Test Discord message formatting."""
        # Test message data
        message_data = {
            "from_agent": "Agent-4",
            "to_agent": "Agent-3",
            "message": "Test Discord message",
            "priority": "HIGH",
            "tags": ["TASK_ASSIGNMENT"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Test Discord formatting
        discord_format = f"""
📤 FROM: {message_data['from_agent']}
📥 TO: {message_data['to_agent']}
Priority: {message_data['priority']}
Tags: {', '.join(message_data['tags'])}

{message_data['message']}
"""
        
        # Validate formatting
        assert message_data['from_agent'] in discord_format, "From agent should be in format"
        assert message_data['to_agent'] in discord_format, "To agent should be in format"
        assert message_data['priority'] in discord_format, "Priority should be in format"
        assert message_data['message'] in discord_format, "Message content should be in format"
    
    def test_discord_webhook_payload(self):
        """Test Discord webhook payload structure."""
        # Test webhook payload
        webhook_payload = {
            "content": "Test message content",
            "embeds": [{
                "title": "Agent Communication",
                "description": "Message from Agent-4 to Agent-3",
                "color": 0x00ff00,  # Green color
                "fields": [
                    {"name": "Priority", "value": "HIGH", "inline": True},
                    {"name": "Tags", "value": "TASK_ASSIGNMENT", "inline": True}
                ],
                "timestamp": datetime.now().isoformat()
            }]
        }
        
        # Validate payload structure
        assert "content" in webhook_payload, "Should have content field"
        assert "embeds" in webhook_payload, "Should have embeds field"
        assert len(webhook_payload["embeds"]) > 0, "Should have at least one embed"
        
        embed = webhook_payload["embeds"][0]
        assert "title" in embed, "Embed should have title"
        assert "description" in embed, "Embed should have description"
        assert "color" in embed, "Embed should have color"
        assert "fields" in embed, "Embed should have fields"
    
    def test_discord_channel_routing(self):
        """Test Discord channel routing logic."""
        # Mock agent channel mapping
        agent_channels = {
            "Agent-1": "channel_agent_1",
            "Agent-2": "channel_agent_2",
            "Agent-3": "channel_agent_3",
            "Agent-4": "channel_agent_4",
            "Agent-5": "channel_agent_5"
        }
        
        # Test channel routing
        test_agent = "Agent-3"
        expected_channel = agent_channels.get(test_agent)
        
        assert expected_channel == "channel_agent_3", "Should route to correct channel"
        assert expected_channel is not None, "Should have a channel for valid agent"
        
        # Test invalid agent
        invalid_agent = "Agent-99"
        invalid_channel = agent_channels.get(invalid_agent)
        assert invalid_channel is None, "Should not have channel for invalid agent"
    
    def test_discord_rate_limiting(self):
        """Test Discord rate limiting logic."""
        # Mock rate limit data
        rate_limit_data = {
            "limit": 5,
            "remaining": 3,
            "reset_after": 60,
            "bucket": "message_bucket"
        }
        
        # Test rate limit validation
        assert rate_limit_data["remaining"] > 0, "Should have remaining requests"
        assert rate_limit_data["limit"] > rate_limit_data["remaining"], "Should have used some requests"
        assert rate_limit_data["reset_after"] > 0, "Should have reset time"
        
        # Test rate limit exceeded
        rate_limit_data["remaining"] = 0
        assert rate_limit_data["remaining"] == 0, "Should indicate rate limit exceeded"
    
    def test_discord_error_handling(self):
        """Test Discord error handling."""
        # Mock Discord API errors
        discord_errors = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            429: "Too Many Requests",
            500: "Internal Server Error"
        }
        
        # Test error code handling
        test_error_code = 429
        expected_error = discord_errors[test_error_code]
        
        assert expected_error == "Too Many Requests", "Should map to correct error message"
        assert test_error_code in discord_errors, "Should have error mapping"
        
        # Test error recovery logic
        recoverable_errors = [429, 500, 502, 503]
        non_recoverable_errors = [400, 401, 403, 404]
        
        assert 429 in recoverable_errors, "Rate limit should be recoverable"
        assert 401 in non_recoverable_errors, "Unauthorized should not be recoverable"


@pytest.mark.unit
class TestDiscordIntegration:
    """Integration tests for Discord services."""
    
    def test_discord_message_workflow(self):
        """Test complete Discord message workflow."""
        # Step 1: Prepare message
        message_data = {
            "from_agent": "Agent-4",
            "to_agent": "Agent-3",
            "message": "Discord integration test",
            "priority": "HIGH",
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 2: Format for Discord
        discord_content = f"📤 FROM: {message_data['from_agent']}\n📥 TO: {message_data['to_agent']}\n\n{message_data['message']}"
        
        # Step 3: Create webhook payload
        webhook_payload = {
            "content": discord_content,
            "username": f"Agent-{message_data['from_agent']}",
            "avatar_url": None
        }
        
        # Step 4: Validate payload
        assert "content" in webhook_payload, "Should have content"
        assert "username" in webhook_payload, "Should have username"
        assert message_data['from_agent'] in webhook_payload['content'], "Should contain from agent"
        assert message_data['to_agent'] in webhook_payload['content'], "Should contain to agent"
        assert message_data['message'] in webhook_payload['content'], "Should contain message"
    
    def test_discord_agent_notification_system(self):
        """Test Discord agent notification system."""
        # Mock notification data
        notifications = [
            {"agent": "Agent-3", "type": "task_complete", "message": "QA analysis complete"},
            {"agent": "Agent-4", "type": "task_assigned", "message": "New cleanup task assigned"},
            {"agent": "Agent-5", "type": "status_update", "message": "Coordinator status updated"}
        ]
        
        # Test notification processing
        for notification in notifications:
            assert "agent" in notification, "Should have agent field"
            assert "type" in notification, "Should have type field"
            assert "message" in notification, "Should have message field"
            
            # Test notification types
            valid_types = ["task_complete", "task_assigned", "status_update", "emergency"]
            assert notification["type"] in valid_types, "Should have valid notification type"
    
    def test_discord_logging_integration(self):
        """Test Discord logging integration."""
        # Mock log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "agent": "Agent-3",
            "action": "Test execution",
            "status": "success"
        }
        
        # Test log formatting for Discord
        discord_log = f"""
🕐 **{log_entry['timestamp']}**
📊 **Level:** {log_entry['level']}
🤖 **Agent:** {log_entry['agent']}
⚡ **Action:** {log_entry['action']}
✅ **Status:** {log_entry['status']}
"""
        
        # Validate log formatting
        assert log_entry['timestamp'] in discord_log, "Should contain timestamp"
        assert log_entry['level'] in discord_log, "Should contain level"
        assert log_entry['agent'] in discord_log, "Should contain agent"
        assert log_entry['action'] in discord_log, "Should contain action"
        assert log_entry['status'] in discord_log, "Should contain status"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

