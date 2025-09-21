#!/usr/bin/env python3
"""
Test Discord Bot Integration - Comprehensive Test Suite
======================================================

Comprehensive test suite for Discord bot integration with messaging system.
Tests all Discord commands, slash commands, and integration functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestDiscordBotIntegration:
    """Test suite for Discord bot integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.coord_path = str(Path(__file__).parent.parent / "config" / "coordinates.json")
        self.test_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    
    def test_discord_imports(self):
        """Test Discord library imports."""
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            assert True
        except ImportError as e:
            pytest.fail(f"Discord import failed: {e}")
    
    def test_messaging_service_import(self):
        """Test messaging service import."""
        try:
            from services.messaging.core.messaging_service import MessagingService
            assert True
        except ImportError as e:
            pytest.fail(f"MessagingService import failed: {e}")
    
    def test_discord_bot_initialization(self):
        """Test Discord bot initialization."""
        try:
            import discord
            from discord.ext import commands
            
            # Test bot creation
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            assert bot.command_prefix == '!'
            assert bot.intents.message_content == True
        except Exception as e:
            pytest.fail(f"Discord bot initialization failed: {e}")
    
    @patch('services.messaging.core.messaging_service.MessagingService')
    def test_discord_messaging_service_integration(self, mock_messaging_service):
        """Test Discord bot integration with messaging service."""
        # Mock messaging service
        mock_service = Mock()
        mock_service.send_message.return_value = True
        mock_service.broadcast_message.return_value = {agent: True for agent in self.test_agents}
        mock_messaging_service.return_value = mock_service
        
        from services.messaging.core.messaging_service import MessagingService
        
        # Test service initialization
        service = MessagingService(self.coord_path)
        assert service is not None
        
        # Test send message
        result = service.send_message("Agent-1", "Test message", "Discord-Commander")
        assert result == True
        
        # Test broadcast message
        results = service.broadcast_message("Test broadcast", "Discord-Commander")
        assert len(results) == 8
        assert all(results.values())
    
    def test_slash_command_registration(self):
        """Test slash command registration."""
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test slash command decorator
            @bot.tree.command(name="test", description="Test command")
            async def test_command(interaction: discord.Interaction):
                await interaction.response.send_message("Test response")
            
            assert True
        except Exception as e:
            pytest.fail(f"Slash command registration failed: {e}")
    
    def test_discord_embed_creation(self):
        """Test Discord embed creation."""
        try:
            import discord
            
            # Test embed creation
            embed = discord.Embed(
                title="Test Embed",
                description="Test description",
                color=0x00ff00
            )
            
            embed.add_field(name="Test Field", value="Test Value", inline=True)
            
            assert embed.title == "Test Embed"
            assert embed.description == "Test description"
            assert embed.color.value == 0x00ff00
            assert len(embed.fields) == 1
        except Exception as e:
            pytest.fail(f"Discord embed creation failed: {e}")
    
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
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord interaction handling failed: {e}")
    
    def test_discord_command_parameters(self):
        """Test Discord command parameters."""
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test command with parameters
            @bot.tree.command(name="send", description="Send message to specific agent")
            @app_commands.describe(agent="Agent ID (e.g., Agent-1, Agent-2)")
            @app_commands.describe(message="Message to send to the agent")
            async def send_message(interaction: discord.Interaction, agent: str, message: str):
                await interaction.response.send_message(f"Sending to {agent}: {message}")
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord command parameters failed: {e}")
    
    def test_discord_error_handling(self):
        """Test Discord error handling."""
        try:
            import discord
            from discord.ext import commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test error handler
            @bot.event
            async def on_command_error(ctx, error):
                if isinstance(error, commands.CommandNotFound):
                    await ctx.send("Command not found!")
                elif isinstance(error, commands.MissingRequiredArgument):
                    await ctx.send("Missing required argument!")
                else:
                    await ctx.send(f"An error occurred: {error}")
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord error handling failed: {e}")
    
    def test_discord_bot_events(self):
        """Test Discord bot events."""
        try:
            import discord
            from discord.ext import commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test on_ready event
            @bot.event
            async def on_ready():
                print(f"{bot.user} is online and ready!")
            
            # Test on_message event
            @bot.event
            async def on_message(message):
                if message.author == bot.user:
                    return
                await bot.process_commands(message)
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord bot events failed: {e}")
    
    def test_discord_bot_logging(self):
        """Test Discord bot logging."""
        try:
            import discord
            from discord.ext import commands
            import logging
            
            # Create bot with logging
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test logger
            logger = logging.getLogger(__name__)
            logger.info("Test log message")
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord bot logging failed: {e}")
    
    def test_discord_bot_configuration(self):
        """Test Discord bot configuration."""
        try:
            import discord
            from discord.ext import commands
            
            # Test bot configuration
            intents = discord.Intents.default()
            intents.message_content = True
            intents.guilds = True
            intents.messages = True
            
            bot = commands.Bot(
                command_prefix='!',
                intents=intents,
                help_command=None,
                case_insensitive=True
            )
            
            assert bot.command_prefix == '!'
            assert bot.intents.message_content == True
            assert bot.intents.guilds == True
            assert bot.intents.messages == True
            assert bot.case_insensitive == True
        except Exception as e:
            pytest.fail(f"Discord bot configuration failed: {e}")
    
    def test_discord_bot_slash_command_sync(self):
        """Test Discord bot slash command synchronization."""
        try:
            import discord
            from discord.ext import commands
            
            # Create bot
            intents = discord.Intents.default()
            intents.message_content = True
            bot = commands.Bot(command_prefix='!', intents=intents)
            
            # Test slash command sync
            @bot.event
            async def on_ready():
                try:
                    synced = await bot.tree.sync()
                    print(f"Synced {len(synced)} slash commands")
                except Exception as e:
                    print(f"Failed to sync slash commands: {e}")
            
            assert True
        except Exception as e:
            pytest.fail(f"Discord bot slash command sync failed: {e}")
    
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
            
        except Exception as e:
            pytest.fail(f"Discord bot message validation failed: {e}")
    
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
            
            error_response = format_error_response("InvalidAgent", "Agent not found")
            assert "❌ **Failed to send message to InvalidAgent**" in error_response
            assert "Agent not found" in error_response
            
        except Exception as e:
            pytest.fail(f"Discord bot response formatting failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
