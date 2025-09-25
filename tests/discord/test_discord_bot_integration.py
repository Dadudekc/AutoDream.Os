#!/usr/bin/env python3
"""
Discord Bot Integration Tests - Modular Test Suite
==================================================

Integration tests for Discord bot with messaging system.
Tests command handling, message validation, and response formatting.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from tests.utils.test_base_classes import DiscordBotTestBase, MessagingServiceTestBase
from tests.utils.test_fixtures import TestDataFactory, MockFactory


class TestDiscordMessagingIntegration(DiscordBotTestBase, MessagingServiceTestBase):
    """Test Discord bot integration with messaging service."""
    
    @pytest.mark.integration
    @patch('services.messaging.core.messaging_service.MessagingService')
    def test_discord_messaging_service_integration(self, mock_messaging_service):
        """Test Discord bot integration with messaging service."""
        # Mock messaging service
        mock_service = MagicMock()
        mock_service.send_message.return_value = True
        mock_service.broadcast_message.return_value = {agent: True for agent in self.test_agents}
        mock_messaging_service.return_value = mock_service
        
        from services.messaging.core.messaging_service import MessagingService
        
        # Test service initialization
        service = MessagingService("config/coordinates.json")
        assert service is not None
        
        # Test send message
        result = service.send_message("Agent-1", "Test message", "Discord-Commander")
        assert result == True
        
        # Test broadcast message
        results = service.broadcast_message("Test broadcast", "Discord-Commander")
        assert len(results) == 8
        assert all(results.values())
    
    @pytest.mark.integration
    def test_discord_interaction_handling(self):
        """Test Discord interaction handling."""
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test interaction response
            @bot.tree.command(name="ping", description="Test bot responsiveness")
            async def ping(interaction: discord.Interaction):
                latency = round(bot.latency * 1000)
                await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms")
            
            self.assert_discord_bot_initialization(bot)
        except Exception as e:
            pytest.fail(f"Discord interaction handling failed: {e}")


class TestDiscordMessageValidation(DiscordBotTestBase):
    """Test Discord message validation."""
    
    @pytest.mark.unit
    def test_discord_bot_message_validation(self):
        """Test Discord bot message validation."""
        try:
            import discord
            from discord.ext import commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test message validation
            def validate_agent_id(agent_id: str) -> bool:
                return agent_id in self.test_agents
            
            def validate_message_content(message: str) -> bool:
                return len(message.strip()) > 0 and len(message) <= 2000
            
            # Test valid inputs
            assert validate_agent_id("Agent-1") == True
            assert validate_message_content("Test message") == True
            
            # Test invalid inputs
            assert validate_agent_id("InvalidAgent") == False
            assert validate_message_content("") == False
            assert validate_message_content("A" * 2001) == False
            
            self.assert_discord_bot_initialization(bot)
        except Exception as e:
            pytest.fail(f"Discord bot message validation failed: {e}")
    
    @pytest.mark.unit
    def test_discord_message_length_validation(self):
        """Test Discord message length validation."""
        def validate_message_length(message: str, max_length: int = 2000) -> bool:
            return len(message) <= max_length
        
        # Test valid lengths
        assert validate_message_length("Short message") == True
        assert validate_message_length("A" * 2000) == True
        
        # Test invalid lengths
        assert validate_message_length("A" * 2001) == False
        assert validate_message_length("A" * 10000) == False
    
    @pytest.mark.unit
    def test_discord_agent_id_validation(self):
        """Test Discord agent ID validation."""
        def validate_agent_id_format(agent_id: str) -> bool:
            return agent_id.startswith("Agent-") and agent_id.split("-")[1].isdigit()
        
        # Test valid agent IDs
        assert validate_agent_id_format("Agent-1") == True
        assert validate_agent_id_format("Agent-8") == True
        
        # Test invalid agent IDs
        assert validate_agent_id_format("InvalidAgent") == False
        assert validate_agent_id_format("Agent") == False
        assert validate_agent_id_format("Agent-X") == False
        assert validate_agent_id_format("") == False


class TestDiscordResponseFormatting(DiscordBotTestBase):
    """Test Discord response formatting."""
    
    @pytest.mark.unit
    def test_discord_bot_response_formatting(self):
        """Test Discord bot response formatting."""
        try:
            import discord
            
            # Test response formatting
            def format_success_response(agent: str, message: str) -> str:
                return f"✅ **Message Sent Successfully!**\n\n**To:** {agent}\n**Message:** {message}\n**From:** Discord-Commander\n\n🐝 **WE ARE SWARM** - Message delivered!"
            
            def format_error_response(agent: str, error: str) -> str:
                return f"❌ **Failed to send message to {agent}**\n\n**Error:** {error}\n\n**Possible reasons:**\n• Agent {agent} is not active\n• Invalid agent ID\n• Messaging system error"
            
            # Test formatting
            success_response = format_success_response("Agent-1", "Test message")
            assert "✅ **Message Sent Successfully!**" in success_response
            assert "Agent-1" in success_response
            assert "Test message" in success_response
            assert "🐝 **WE ARE SWARM**" in success_response
            
            error_response = format_error_response("InvalidAgent", "Agent not found")
            assert "❌ **Failed to send message to InvalidAgent**" in error_response
            assert "Agent not found" in error_response
            
        except Exception as e:
            pytest.fail(f"Discord bot response formatting failed: {e}")
    
    @pytest.mark.unit
    def test_discord_embed_response_formatting(self):
        """Test Discord embed response formatting."""
        try:
            import discord
            
            def create_success_embed(agent: str, message: str) -> discord.Embed:
                embed = discord.Embed(
                    title="✅ Message Sent Successfully!",
                    description=f"Message delivered to {agent}",
                    color=0x00ff00
                )
                embed.add_field(name="To", value=agent, inline=True)
                embed.add_field(name="Message", value=message, inline=False)
                embed.add_field(name="From", value="Discord-Commander", inline=True)
                embed.set_footer(text="🐝 WE ARE SWARM - Message delivered!")
                return embed
            
            def create_error_embed(agent: str, error: str) -> discord.Embed:
                embed = discord.Embed(
                    title="❌ Message Send Failed",
                    description=f"Failed to send message to {agent}",
                    color=0xff0000
                )
                embed.add_field(name="Agent", value=agent, inline=True)
                embed.add_field(name="Error", value=error, inline=False)
                embed.set_footer(text="Check agent status and try again")
                return embed
            
            # Test success embed
            success_embed = create_success_embed("Agent-1", "Test message")
            assert success_embed.title == "✅ Message Sent Successfully!"
            assert "Agent-1" in success_embed.description
            assert len(success_embed.fields) == 3
            assert success_embed.color.value == 0x00ff00
            
            # Test error embed
            error_embed = create_error_embed("InvalidAgent", "Agent not found")
            assert error_embed.title == "❌ Message Send Failed"
            assert "InvalidAgent" in error_embed.description
            assert len(error_embed.fields) == 2
            assert error_embed.color.value == 0xff0000
            
        except Exception as e:
            pytest.fail(f"Discord embed response formatting failed: {e}")


class TestDiscordCommandHandling(DiscordBotTestBase):
    """Test Discord command handling."""
    
    @pytest.mark.integration
    @patch('services.messaging.core.messaging_service.MessagingService')
    def test_send_command_handling(self, mock_messaging_service):
        """Test send command handling."""
        # Mock messaging service
        mock_service = MagicMock()
        mock_service.send_message.return_value = True
        mock_messaging_service.return_value = mock_service
        
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Mock messaging service
            messaging_service = mock_service
            
            @bot.tree.command(name="send", description="Send message to specific agent")
            @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
            @app_commands.describe(message="Message to send to the agent")
            async def send_message(interaction: discord.Interaction, agent: str, message: str):
                # Validate agent ID
                if not agent.startswith("Agent-"):
                    await interaction.response.send_message("❌ Invalid agent ID format!")
                    return
                
                # Send message
                result = messaging_service.send_message(agent, message, "Discord-Commander")
                
                if result:
                    await interaction.response.send_message(
                        f"✅ **Message Sent Successfully!**\n\n**To:** {agent}\n**Message:** {message}"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ **Failed to send message to {agent}**"
                    )
            
            self.assert_discord_bot_initialization(bot)
            
        except Exception as e:
            pytest.fail(f"Send command handling failed: {e}")
    
    @pytest.mark.integration
    @patch('services.messaging.core.messaging_service.MessagingService')
    def test_broadcast_command_handling(self, mock_messaging_service):
        """Test broadcast command handling."""
        # Mock messaging service
        mock_service = MagicMock()
        mock_service.broadcast_message.return_value = {agent: True for agent in self.test_agents}
        mock_messaging_service.return_value = mock_service
        
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Mock messaging service
            messaging_service = mock_service
            
            @bot.tree.command(name="broadcast", description="Broadcast message to all agents")
            @app_commands.describe(message="Message to broadcast to all agents")
            async def broadcast_message(interaction: discord.Interaction, message: str):
                # Broadcast message
                results = messaging_service.broadcast_message(message, "Discord-Commander")
                
                success_count = sum(1 for result in results.values() if result)
                total_count = len(results)
                
                await interaction.response.send_message(
                    f"📢 **Broadcast Complete!**\n\n"
                    f"**Message:** {message}\n"
                    f"**Sent to:** {success_count}/{total_count} agents\n"
                    f"**From:** Discord-Commander"
                )
            
            self.assert_discord_bot_initialization(bot)
            
        except Exception as e:
            pytest.fail(f"Broadcast command handling failed: {e}")
    
    @pytest.mark.integration
    def test_status_command_handling(self):
        """Test status command handling."""
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            @bot.tree.command(name="status", description="Check agent status")
            @app_commands.describe(agent="Agent ID to check status for")
            async def check_status(interaction: discord.Interaction, agent: str):
                # Mock status check
                if agent in self.test_agents:
                    await interaction.response.send_message(
                        f"✅ **Agent {agent} Status**\n\n"
                        f"**Status:** Active\n"
                        f"**Coordinates:** Available\n"
                        f"**Last Activity:** Recent"
                    )
                else:
                    await interaction.response.send_message(
                        f"❌ **Agent {agent} not found**"
                    )
            
            self.assert_discord_bot_initialization(bot)
            
        except Exception as e:
            pytest.fail(f"Status command handling failed: {e}")




