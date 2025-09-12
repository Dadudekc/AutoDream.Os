#!/usr/bin/env python3
"""
Discord Commander Security Policies Unit Tests - V2 Compliance Module
======================================================================

Comprehensive unit tests for Discord security policy enforcement.

Features:
- Channel access control testing
- Guild restriction validation
- User permission checking
- Environment variable parsing
- Security policy edge cases

Author: Agent-7 (Web Interface Specialist) - Test Coverage Enhancement
License: MIT
"""

import os
import pytest
from unittest.mock import patch, MagicMock

try:
    from src.discord_commander.security_policies import (
        allow_guild, allow_channel, allow_user,
        ALLOWED_GUILDS, ALLOWED_CHANNELS, ALLOWED_USERS
    )
except ImportError:
    # Fallback for direct execution
    from discord_commander.security_policies import (
        allow_guild, allow_channel, allow_user,
        ALLOWED_GUILDS, ALLOWED_CHANNELS, ALLOWED_USERS
    )


class TestSecurityPolicyEnvironmentParsing:
    """Test cases for environment variable parsing in security policies."""

    @patch.dict(os.environ, {}, clear=True)
    def test_empty_environment_variables(self):
        """Test behavior when no environment variables are set."""
        # Reload the module to pick up new environment
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        # When no env vars are set, all should be empty sets
        assert len(sp.ALLOWED_GUILDS) == 0
        assert len(sp.ALLOWED_CHANNELS) == 0
        assert len(sp.ALLOWED_USERS) == 0

    @patch.dict(os.environ, {
        'ALLOWED_GUILD_IDS': '123456789,987654321',
        'ALLOWED_CHANNEL_IDS': '111111111,222222222',
        'ALLOWED_USER_IDS': '333333333,444444444'
    })
    def test_environment_variable_parsing(self):
        """Test parsing of comma-separated environment variables."""
        # Reload the module to pick up new environment
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert 123456789 in sp.ALLOWED_GUILDS
        assert 987654321 in sp.ALLOWED_GUILDS
        assert 111111111 in sp.ALLOWED_CHANNELS
        assert 222222222 in sp.ALLOWED_CHANNELS
        assert 333333333 in sp.ALLOWED_USERS
        assert 444444444 in sp.ALLOWED_USERS

    @patch.dict(os.environ, {
        'ALLOWED_CHANNEL_IDS': '1412461118970138714,  123456789  ,987654321   '
    })
    def test_environment_variable_whitespace_handling(self):
        """Test that whitespace in environment variables is handled correctly."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert 1412461118970138714 in sp.ALLOWED_CHANNELS
        assert 123456789 in sp.ALLOWED_CHANNELS
        assert 987654321 in sp.ALLOWED_CHANNELS

    @patch.dict(os.environ, {
        'ALLOWED_GUILD_IDS': 'invalid,text,123,also_invalid,456'
    })
    def test_environment_variable_invalid_values(self):
        """Test handling of invalid (non-numeric) values in environment variables."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        # Should only contain valid numeric IDs
        assert 123 in sp.ALLOWED_GUILDS
        assert 456 in sp.ALLOWED_GUILDS
        assert len(sp.ALLOWED_GUILDS) == 2  # Only the valid ones

    @patch.dict(os.environ, {'ALLOWED_CHANNEL_IDS': ''})
    def test_empty_environment_variable_string(self):
        """Test handling of empty environment variable strings."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert len(sp.ALLOWED_CHANNELS) == 0


class TestAllowGuildPolicy:
    """Test cases for guild access control."""

    @patch.dict(os.environ, {}, clear=True)
    def test_allow_guild_no_restrictions(self):
        """Test that all guilds are allowed when no restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_guild(123456789) is True
        assert sp.allow_guild(987654321) is True
        assert sp.allow_guild(0) is True

    @patch.dict(os.environ, {'ALLOWED_GUILD_IDS': '123456789,987654321'})
    def test_allow_guild_with_restrictions(self):
        """Test guild filtering when restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_guild(123456789) is True
        assert sp.allow_guild(987654321) is True
        assert sp.allow_guild(111111111) is False  # Not in allowed list

    def test_allow_guild_none_value(self):
        """Test allow_guild with None value."""
        # Should handle None gracefully (though this shouldn't happen in practice)
        result = allow_guild(None)
        # Result depends on current ALLOWED_GUILDS state, but shouldn't crash
        assert isinstance(result, bool)


class TestAllowChannelPolicy:
    """Test cases for channel access control."""

    @patch.dict(os.environ, {}, clear=True)
    def test_allow_channel_no_restrictions(self):
        """Test that all channels are allowed when no restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_channel(123456789) is True
        assert sp.allow_channel(987654321) is True

    @patch.dict(os.environ, {'ALLOWED_CHANNEL_IDS': '111111111,222222222'})
    def test_allow_channel_with_restrictions(self):
        """Test channel filtering when restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_channel(111111111) is True
        assert sp.allow_channel(222222222) is True
        assert sp.allow_channel(333333333) is False  # Not in allowed list

    def test_allow_channel_none_value(self):
        """Test allow_channel with None value."""
        result = allow_channel(None)
        assert isinstance(result, bool)


class TestAllowUserPolicy:
    """Test cases for user access control."""

    @patch.dict(os.environ, {}, clear=True)
    def test_allow_user_no_restrictions(self):
        """Test that all users are allowed when no restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_user(123456789) is True
        assert sp.allow_user(987654321) is True

    @patch.dict(os.environ, {'ALLOWED_USER_IDS': '333333333,444444444'})
    def test_allow_user_with_restrictions(self):
        """Test user filtering when restrictions are set."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert sp.allow_user(333333333) is True
        assert sp.allow_user(444444444) is True
        assert sp.allow_user(555555555) is False  # Not in allowed list

    def test_allow_user_none_value(self):
        """Test allow_user with None value."""
        result = allow_user(None)
        assert isinstance(result, bool)


class TestSecurityPolicyIntegration:
    """Integration tests for combined security policy behavior."""

    @patch.dict(os.environ, {}, clear=True)
    def test_all_policies_allow_by_default(self):
        """Test that all policies allow access by default."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        # All should allow when no restrictions are set
        assert sp.allow_guild(123) is True
        assert sp.allow_channel(456) is True
        assert sp.allow_user(789) is True

    @patch.dict(os.environ, {
        'ALLOWED_GUILD_IDS': '111',
        'ALLOWED_CHANNEL_IDS': '222',
        'ALLOWED_USER_IDS': '333'
    })
    def test_combined_policy_restrictions(self):
        """Test combined behavior when all policies have restrictions."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        # Test allowed combinations
        assert sp.allow_guild(111) is True
        assert sp.allow_channel(222) is True
        assert sp.allow_user(333) is True

        # Test denied combinations
        assert sp.allow_guild(999) is False
        assert sp.allow_channel(999) is False
        assert sp.allow_user(999) is False

    @patch.dict(os.environ, {
        'ALLOWED_CHANNEL_IDS': '1412461118970138714,123456789012345678'
    })
    def test_realistic_channel_ids(self):
        """Test with realistic Discord channel IDs."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        # Test with realistic Discord snowflake IDs
        assert sp.allow_channel(1412461118970138714) is True
        assert sp.allow_channel(123456789012345678) is True
        assert sp.allow_channel(987654321098765432) is False


class TestSecurityPolicyEdgeCases:
    """Test cases for edge cases and error conditions."""

    def test_security_policy_module_import(self):
        """Test that the security policy module can be imported."""
        try:
            import discord_commander.security_policies as sp
            assert hasattr(sp, 'allow_guild')
            assert hasattr(sp, 'allow_channel')
            assert hasattr(sp, 'allow_user')
            assert hasattr(sp, 'ALLOWED_GUILDS')
            assert hasattr(sp, 'ALLOWED_CHANNELS')
            assert hasattr(sp, 'ALLOWED_USERS')
        except ImportError:
            pytest.fail("Security policies module should be importable")

    def test_security_policy_constants_are_sets(self):
        """Test that the security policy constants are sets."""
        import discord_commander.security_policies as sp

        assert isinstance(sp.ALLOWED_GUILDS, set)
        assert isinstance(sp.ALLOWED_CHANNELS, set)
        assert isinstance(sp.ALLOWED_USERS, set)

    @patch.dict(os.environ, {'ALLOWED_CHANNEL_IDS': '0,1,2,3,4,5'})
    def test_large_number_of_allowed_ids(self):
        """Test handling of many allowed IDs."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        assert len(sp.ALLOWED_CHANNELS) == 6
        for i in range(6):
            assert i in sp.ALLOWED_CHANNELS
            assert sp.allow_channel(i) is True

    def test_security_policy_functions_are_callable(self):
        """Test that all security policy functions are callable."""
        assert callable(allow_guild)
        assert callable(allow_channel)
        assert callable(allow_user)


class TestSecurityPolicyConcurrency:
    """Test cases for concurrent access to security policies."""

    @patch.dict(os.environ, {'ALLOWED_CHANNEL_IDS': '100,200,300'})
    def test_concurrent_policy_access(self):
        """Test that security policies work correctly under concurrent access."""
        import importlib
        import discord_commander.security_policies as sp
        importlib.reload(sp)

        import threading
        import time

        results = []

        def check_policies():
            results.append(sp.allow_channel(100))
            results.append(sp.allow_channel(150))
            time.sleep(0.01)  # Small delay to encourage race conditions
            results.append(sp.allow_channel(200))

        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=check_policies)
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All results should be correct
        assert all(results)  # All should be True for allowed channels or False for denied

        # Count expected results: 5 threads * 3 checks each = 15 total
        assert len(results) == 15
