#!/usr/bin/env python3
"""
Config SSOT Validation Tests
============================

Comprehensive test suite for the unified configuration SSOT.
Tests all configuration sections, validation, and backward compatibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import pytest

from src.core.config_ssot import (
    ConfigEnvironment,
    ConfigSource,
    UnifiedConfigManager,
    get_agent_config,
    get_browser_config,
    get_config,
    get_file_pattern_config,
    get_threshold_config,
    get_timeout_config,
    get_unified_config,
    reload_config,
    validate_config,
)


class TestConfigSSOT:
    """Test suite for unified configuration SSOT."""

    def test_unified_config_manager_initialization(self):
        """Test UnifiedConfigManager initializes correctly."""
        manager = UnifiedConfigManager()
        assert manager is not None
        assert manager.timeouts is not None
        assert manager.agents is not None
        assert manager.browser is not None
        assert manager.thresholds is not None
        assert manager.file_patterns is not None

    def test_timeout_config(self):
        """Test TimeoutConfig dataclass."""
        config = get_timeout_config()
        assert config.scrape_timeout == 30.0
        assert config.response_wait_timeout == 120.0
        assert config.quality_check_interval == 30.0
        assert config.browser_timeout == 30.0
        assert config.test_timeout == 300.0

    def test_agent_config(self):
        """Test AgentConfig dataclass."""
        config = get_agent_config()
        assert config.agent_count == 8
        assert config.captain_id == "Agent-4"
        assert config.default_mode == "pyautogui"
        assert len(config.agent_ids) == 8
        assert "Agent-1" in config.agent_ids
        assert "Agent-8" in config.agent_ids

    def test_browser_config(self):
        """Test BrowserConfig dataclass."""
        config = get_browser_config()
        assert "chatgpt.com" in config.gpt_url
        assert config.input_selector is not None
        assert config.driver_type == "chrome"
        assert config.max_scrape_retries == 3
        assert len(config.input_fallback_selectors) > 0

    def test_threshold_config(self):
        """Test ThresholdConfig dataclass."""
        config = get_threshold_config()
        assert config.coverage_threshold == 85.0
        assert config.response_time_target == 100.0
        assert config.throughput_target == 1000.0

        # Test alert rules
        alert_rules = config.alert_rules
        assert "test_failure" in alert_rules
        assert "performance_degradation" in alert_rules

        # Test benchmark targets
        benchmarks = config.benchmark_targets
        assert "response_time" in benchmarks
        assert "throughput" in benchmarks

    def test_file_pattern_config(self):
        """Test FilePatternConfig dataclass."""
        config = get_file_pattern_config()
        assert config.test_file_pattern == "test_*.py"
        assert config.architecture_files is not None

        # Test project patterns
        patterns = config.project_patterns
        assert "architecture_files" in patterns
        assert "test_files" in patterns

    def test_get_config_basic(self):
        """Test basic get_config functionality."""
        # Test with defaults
        value = get_config("AGENT_COUNT", 8)
        assert value == 8

        # Test with non-existent key
        value = get_config("NON_EXISTENT_KEY", "default")
        assert value == "default"

    def test_config_validation(self):
        """Test configuration validation."""
        errors = validate_config()
        # Should return empty list if all valid
        assert isinstance(errors, list)

    def test_get_unified_config(self):
        """Test get_unified_config returns manager instance."""
        manager = get_unified_config()
        assert isinstance(manager, UnifiedConfigManager)
        assert hasattr(manager, "timeouts")
        assert hasattr(manager, "agents")
        assert hasattr(manager, "browser")

    def test_reload_config(self):
        """Test config reload functionality."""
        # Should not raise exception
        reload_config()

        # Config should still be accessible
        config = get_agent_config()
        assert config is not None

    def test_backward_compatibility_config_core(self):
        """Test backward compatibility with config_core imports."""
        from src.core.config_core import get_agent_config as core_get_agent
        from src.core.config_core import get_config as core_get_config

        # Should work identically
        agent_config = core_get_agent()
        assert agent_config.agent_count == 8

        value = core_get_config("AGENT_COUNT", 8)
        assert value == 8

    def test_backward_compatibility_unified_config(self):
        """Test backward compatibility with unified_config imports."""
        from src.core.unified_config import get_agent_config as unified_get_agent

        # Should work identically
        agent_config = unified_get_agent()
        assert agent_config.agent_count == 8

    def test_backward_compatibility_config_browser(self):
        """Test backward compatibility with config_browser imports."""
        from src.core.config_browser import BrowserConfig as ImportedBrowserConfig

        # Should import successfully
        assert ImportedBrowserConfig is not None

    def test_backward_compatibility_config_thresholds(self):
        """Test backward compatibility with config_thresholds imports."""
        from src.core.config_thresholds import ThresholdConfig as ImportedThresholdConfig

        # Should import successfully
        assert ImportedThresholdConfig is not None

    def test_backward_compatibility_shared_utils(self):
        """Test backward compatibility with shared_utils/config imports."""
        from src.shared_utils.config import get_setting, get_workspace_root

        # Should import successfully
        assert get_setting is not None
        assert get_workspace_root is not None

        # get_workspace_root should work
        root = get_workspace_root()
        assert root.exists()

    def test_services_config_imports(self):
        """Test services/config.py still works."""
        from src.services.config import AGENT_COUNT, CAPTAIN_ID, DEFAULT_MODE

        assert AGENT_COUNT == 8
        assert CAPTAIN_ID == "Agent-4"
        assert DEFAULT_MODE in ["pyautogui", "coordinated"]

    def test_config_environment_enum(self):
        """Test ConfigEnvironment enum."""
        assert ConfigEnvironment.DEVELOPMENT == "development"
        assert ConfigEnvironment.TESTING == "testing"
        assert ConfigEnvironment.PRODUCTION == "production"

    def test_config_source_enum(self):
        """Test ConfigSource enum."""
        assert ConfigSource.ENVIRONMENT == "environment"
        assert ConfigSource.DEFAULT == "default"
        assert ConfigSource.FILE == "file"


class TestConfigSSOTIntegration:
    """Integration tests for config SSOT."""

    def test_all_config_sections_accessible(self):
        """Test all config sections can be accessed."""
        manager = get_unified_config()

        # All sections should be accessible
        assert manager.timeouts.scrape_timeout > 0
        assert manager.agents.agent_count > 0
        assert manager.browser.gpt_url is not None
        assert manager.thresholds.coverage_threshold > 0
        assert manager.file_patterns.test_file_pattern is not None

    def test_config_consistency(self):
        """Test config values are consistent across access methods."""
        # Get through manager
        manager = get_unified_config()
        agent_count_1 = manager.agents.agent_count

        # Get through helper function
        agent_config = get_agent_config()
        agent_count_2 = agent_config.agent_count

        # Should be identical
        assert agent_count_1 == agent_count_2

    def test_no_circular_imports(self):
        """Test there are no circular import issues."""
        # Should be able to import all at once
        # And from shims
        from src.core.config_core import get_agent_config
        from src.core.config_ssot import get_config
        from src.core.unified_config import get_timeout_config

        # All should work
        assert get_config is not None
        assert get_agent_config is not None
        assert get_timeout_config is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
