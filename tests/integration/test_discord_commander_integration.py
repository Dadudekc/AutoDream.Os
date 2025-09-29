#!/usr/bin/env python3
"""
Discord Commander Integration Tests
===================================

Comprehensive integration tests for the modular Discord Commander system.
Tests the complete Discord bot lifecycle and command execution.
"""

import asyncio
import os
import sys
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.services.discord_commander import (
    AgentCommands,
    CommandManager,
    DiscordCommanderBot,
    DiscordCommandRegistry,
    DiscordConfig,
    DiscordEventManager,
    DiscordStatusMonitor,
    SwarmCommands,
    SystemCommands,
)


class TestDiscordConfigIntegration:
    """Test Discord configuration integration."""

    def test_config_creation_and_validation(self):
        """Test Discord config creation and validation."""
        # Test with valid environment variables
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            config = DiscordConfig()

            assert config.token == "test_token"
            assert config.guild_id == "123456789"
            assert config.command_prefix == "!"

            # Test validation
            issues = config.validate()
            assert len(issues) == 0

    def test_config_validation_with_missing_vars(self):
        """Test config validation with missing environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            config = DiscordConfig()

            issues = config.validate()
            assert len(issues) > 0
            assert "DISCORD_BOT_TOKEN not set" in issues
            assert "DISCORD_GUILD_ID not set" in issues

    def test_config_intents_creation(self):
        """Test Discord intents creation."""
        config = DiscordConfig()
        intents = config._get_intents()

        # Should return None if discord is not available
        # or a valid Intents object if available
        assert intents is None or hasattr(intents, "message_content")


class TestDiscordCommandRegistryIntegration:
    """Test Discord command registry integration."""

    def test_command_registration_and_retrieval(self):
        """Test command registration and retrieval."""
        registry = DiscordCommandRegistry()

        # Mock command handler
        handler = Mock()

        # Register command
        registry.register_command("test_command", handler, "Test command description")

        # Retrieve command
        retrieved_handler = registry.get_command("test_command")
        assert retrieved_handler == handler

        # List commands
        commands = registry.list_commands()
        assert "test_command" in commands

        # Unregister command
        assert registry.unregister_command("test_command")
        assert registry.get_command("test_command") is None

    def test_multiple_command_registration(self):
        """Test registration of multiple commands."""
        registry = DiscordCommandRegistry()

        handlers = [Mock() for _ in range(5)]

        for i, handler in enumerate(handlers):
            registry.register_command(f"command_{i}", handler, f"Command {i}")

        commands = registry.list_commands()
        assert len(commands) == 5

        for i in range(5):
            assert f"command_{i}" in commands


class TestDiscordEventManagerIntegration:
    """Test Discord event manager integration."""

    def test_event_handler_registration_and_triggering(self):
        """Test event handler registration and triggering."""
        event_manager = DiscordEventManager()

        # Mock handlers
        handler1 = Mock()
        handler2 = Mock()

        # Register handlers
        event_manager.register_event_handler("test_event", handler1)
        event_manager.register_event_handler("test_event", handler2)

        # Trigger event
        asyncio.run(event_manager.trigger_event("test_event", "arg1", "arg2"))

        # Check handlers were called
        handler1.assert_called_once_with("arg1", "arg2")
        handler2.assert_called_once_with("arg1", "arg2")

    def test_async_event_handler(self):
        """Test async event handler."""
        event_manager = DiscordEventManager()

        async def async_handler(arg1, arg2):
            return f"{arg1}_{arg2}"

        event_manager.register_event_handler("async_event", async_handler)

        # Trigger async event
        result = asyncio.run(event_manager.trigger_event("async_event", "test", "handler"))

        # Should complete without error
        assert result is None

    def test_event_handler_error_handling(self):
        """Test event handler error handling."""
        event_manager = DiscordEventManager()

        def error_handler():
            raise ValueError("Test error")

        event_manager.register_event_handler("error_event", error_handler)

        # Should not raise exception
        asyncio.run(event_manager.trigger_event("error_event"))


class TestDiscordStatusMonitorIntegration:
    """Test Discord status monitor integration."""

    def test_status_monitoring(self):
        """Test status monitoring functionality."""
        monitor = DiscordStatusMonitor()

        # Record various events
        monitor.record_heartbeat()
        monitor.record_message()
        monitor.record_command()
        monitor.record_error()

        # Get status
        status = monitor.get_status()

        assert status["messages_received"] == 1
        assert status["commands_executed"] == 1
        assert status["errors"] == 1
        assert status["status"] == "healthy"
        assert "uptime_seconds" in status
        assert "uptime_formatted" in status

    def test_health_check(self):
        """Test health check functionality."""
        monitor = DiscordStatusMonitor()

        # Initially healthy
        assert monitor.is_healthy()

        # Add many errors
        for _ in range(60):
            monitor.record_error()

        # Should be unhealthy
        assert not monitor.is_healthy()


class TestDiscordCommandsIntegration:
    """Test Discord commands integration."""

    @pytest.fixture
    def mock_messaging_service(self):
        """Create mock messaging service."""
        service = Mock()
        service.send_message = AsyncMock(return_value={"success": True})
        return service

    @pytest.fixture
    def mock_ctx(self):
        """Create mock Discord context."""
        ctx = Mock()
        ctx.author = Mock()
        ctx.author.name = "TestUser"
        ctx.guild = Mock()
        ctx.guild.name = "TestGuild"
        return ctx

    def test_agent_commands_integration(self, mock_messaging_service, mock_ctx):
        """Test agent commands integration."""
        agent_commands = AgentCommands(mock_messaging_service)

        # Test agent status
        result = asyncio.run(agent_commands.agent_status(mock_ctx, "Agent-1"))
        assert isinstance(result, str)
        assert "Agent-1" in result

        # Test send message
        result = asyncio.run(agent_commands.send_message(mock_ctx, "Agent-1", "Test message"))
        assert "Message sent" in result
        mock_messaging_service.send_message.assert_called()

    def test_system_commands_integration(self, mock_ctx):
        """Test system commands integration."""
        system_commands = SystemCommands()

        # Test system status
        result = asyncio.run(system_commands.system_status(mock_ctx))
        assert isinstance(result, str)
        assert "System Status" in result
        assert "python_version" in result

        # Test project info
        result = asyncio.run(system_commands.project_info(mock_ctx))
        assert isinstance(result, str)
        assert "Project Information" in result

    def test_swarm_commands_integration(self, mock_messaging_service, mock_ctx):
        """Test swarm commands integration."""
        swarm_commands = SwarmCommands(mock_messaging_service)

        # Test swarm status
        result = asyncio.run(swarm_commands.swarm_status(mock_ctx))
        assert isinstance(result, str)
        assert "Swarm Status" in result

        # Test swarm coordination
        result = asyncio.run(swarm_commands.swarm_coordinate(mock_ctx, "Test coordination"))
        assert isinstance(result, str)
        assert "Swarm Coordination Results" in result


class TestCommandManagerIntegration:
    """Test command manager integration."""

    def test_command_manager_initialization(self, mock_messaging_service):
        """Test command manager initialization."""
        manager = CommandManager(mock_messaging_service)

        # Check that commands are registered
        commands = manager.list_commands()
        assert len(commands) > 0

        # Check specific commands
        expected_commands = [
            "agent_status",
            "send_message",
            "agent_coordinates",
            "system_status",
            "project_info",
            "swarm_status",
            "swarm_coordinate",
        ]

        for cmd in expected_commands:
            assert cmd in commands

    def test_command_handler_retrieval(self, mock_messaging_service):
        """Test command handler retrieval."""
        manager = CommandManager(mock_messaging_service)

        # Get handler
        handler = manager.get_command_handler("agent_status")
        assert handler is not None
        assert callable(handler)

        # Test non-existent command
        handler = manager.get_command_handler("non_existent_command")
        assert handler is None


class TestDiscordCommanderBotIntegration:
    """Test Discord Commander Bot integration."""

    @pytest.fixture
    def mock_discord_bot(self):
        """Create mock Discord bot."""
        bot = Mock()
        bot.user = Mock()
        bot.user.name = "TestBot"
        bot.guilds = [Mock()]
        bot.is_closed.return_value = False
        return bot

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    def test_bot_initialization(self):
        """Test bot initialization."""
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Check components are initialized
            assert bot.config is not None
            assert bot.connection_manager is not None
            assert bot.event_manager is not None
            assert bot.status_monitor is not None
            assert bot.command_manager is not None

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    def test_bot_status_monitoring(self):
        """Test bot status monitoring."""
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Get status
            status = bot.get_status()

            assert "uptime_seconds" in status
            assert "command_count" in status
            assert "config_valid" in status

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    def test_bot_health_check(self):
        """Test bot health check."""
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Initially healthy
            assert bot.is_healthy()


class TestDiscordCommanderEndToEndIntegration:
    """Test complete end-to-end Discord Commander integration."""

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    @patch("discord.ext.commands.Bot")
    def test_complete_bot_lifecycle(self, mock_bot_class):
        """Test complete bot lifecycle."""
        # Mock bot instance
        mock_bot = Mock()
        mock_bot.user = Mock()
        mock_bot.user.name = "TestBot"
        mock_bot.guilds = [Mock()]
        mock_bot.is_closed.return_value = False
        mock_bot_class.return_value = mock_bot

        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Test initialization
            init_result = asyncio.run(bot.initialize())
            assert init_result

            # Test status
            status = bot.get_status()
            assert status["config_valid"]

            # Test health
            assert bot.is_healthy()

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", False)
    def test_bot_without_discord(self):
        """Test bot behavior when Discord is not available."""
        bot = DiscordCommanderBot()

        # Should still initialize components
        assert bot.config is not None
        assert bot.event_manager is not None
        assert bot.status_monitor is not None

        # Config validation should fail
        issues = bot.config.validate()
        assert "discord.py not installed" in issues


class TestDiscordCommanderPerformanceIntegration:
    """Test Discord Commander performance integration."""

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    def test_command_execution_performance(self):
        """Test command execution performance."""
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Measure command registration time
            start_time = datetime.now()
            commands = bot.command_manager.list_commands()
            end_time = datetime.now()

            execution_time = (end_time - start_time).total_seconds()
            assert execution_time < 1.0  # Should be very fast
            assert len(commands) > 0

    @patch("src.services.discord_commander.core.DISCORD_AVAILABLE", True)
    def test_status_monitoring_performance(self):
        """Test status monitoring performance."""
        with patch.dict(
            os.environ, {"DISCORD_BOT_TOKEN": "test_token", "DISCORD_GUILD_ID": "123456789"}
        ):
            bot = DiscordCommanderBot()

            # Record many events
            start_time = datetime.now()
            for _ in range(1000):
                bot.status_monitor.record_message()
                bot.status_monitor.record_command()

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            # Should handle 1000 events quickly
            assert execution_time < 0.1

            # Status should still be accurate
            status = bot.status_monitor.get_status()
            assert status["messages_received"] == 1000
            assert status["commands_executed"] == 1000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
