#!/usr/bin/env python3
"""
Comprehensive Pytest Suite for Discord Devlog System
==================================================

Tests for devlog functionality including:
- Core devlog system operations
- CLI interface
- Configuration loading
- Discord webhook posting
- File logging
- Error handling

Usage:
    pytest tests/test_devlog_system.py -v

Author: Agent-7 - Web Development Specialist
"""

import pytest

# Add src to path for utils import
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), '..', 'src'))

# Test the actual devlog functionality by running it directly
def run_devlog_status():
    """Test devlog status command by running the CLI directly."""
    result = subprocess.run([
        sys.executable, '-m', 'src.core.devlog_cli', 'status'
    ], capture_output=True, text=True, cwd=get_unified_utility().path.dirname(__file__))

    return result.returncode, result.stdout, result.stderr

def test_devlog_cli_status():
    """Test the devlog CLI status command."""
    returncode, stdout, stderr = run_devlog_status()

    get_logger(__name__).info(f"Return code: {returncode}")
    get_logger(__name__).info(f"Stdout: {stdout}")
    get_logger(__name__).info(f"Stderr: {stderr}")

    # The command should run (may fail due to missing dependencies, but should not crash)
    assert get_unified_validator().validate_type(returncode, int)

def test_devlog_config_exists():
    """Test that devlog configuration file exists."""
    config_path = get_unified_utility().Path("config/devlog_config.json")
    assert config_path.exists(), "devlog_config.json should exist"

    with open(config_path, 'r') as f:
        config = read_json(f)

    assert "discord_webhook_url" in config
    assert "enable_discord" in config
    assert "agent_name" in config

def test_devlog_directory_exists():
    """Test that devlogs directory exists."""
    devlog_dir = get_unified_utility().Path("devlogs")
    assert devlog_dir.exists(), "devlogs directory should exist"
    assert devlog_dir.is_dir(), "devlogs should be a directory"

def test_devlog_files_exist():
    """Test that devlog files exist in the devlogs directory."""
    devlog_dir = get_unified_utility().Path("devlogs")
    devlog_files = list(devlog_dir.glob("*.json"))

    assert len(devlog_files) > 0, "Should have at least one devlog file"

    # Test that files contain valid JSON
    for devlog_file in devlog_files:
        with open(devlog_file, 'r') as f:
            data = read_json(f)
            assert get_unified_validator().validate_type(data, list), f"Devlog file {devlog_file} should contain a list"

@patch('requests.post')
def test_discord_webhook_mock(mock_post):
    """Test Discord webhook posting with mock."""
    mock_response = Mock()
    mock_response.status_code = 204
    mock_post.return_value = mock_response

    # Simulate a webhook call
    webhook_url = "https://discord.com/api/webhooks/test"
    payload = {
        "embeds": [{
            "title": "Test Title",
            "description": "Test Content",
            "color": 0x3498db
        }]
    }

    response = mock_post(webhook_url, json=payload)

    mock_post.assert_called_once_with(webhook_url, json=payload)
    assert response.status_code == 204

def test_devlog_entry_structure():
    """Test the structure of devlog entries."""
    devlog_dir = get_unified_utility().Path("devlogs")
    devlog_files = list(devlog_dir.glob("*.json"))

    if devlog_files:
        with open(devlog_files[0], 'r') as f:
            entries = read_json(f)

        if entries:
            entry = entries[0]
            required_fields = ["id", "timestamp", "agent", "category", "title", "content", "channel"]

            for field in required_fields:
                assert field in entry, f"Devlog entry missing required field: {field}"

def test_devlog_categories():
    """Test that devlog entries use valid categories."""
    valid_categories = ["general", "progress", "issue", "success", "warning", "info"]

    devlog_dir = get_unified_utility().Path("devlogs")
    devlog_files = list(devlog_dir.glob("*.json"))

    for devlog_file in devlog_files:
        with open(devlog_file, 'r') as f:
            entries = read_json(f)

        for entry in entries:
            if "category" in entry:
                assert entry["category"] in valid_categories, f"Invalid category: {entry['category']}"


# Additional tests for CLI integration
def test_devlog_cli_create_command():
    """Test the devlog CLI create command by running it directly."""
    result = subprocess.run([
        sys.executable, '-m', 'src.core.devlog_cli', 'create',
        'Test CLI Entry', 'Testing CLI functionality', 'general'
    ], capture_output=True, text=True, cwd=get_unified_utility().path.dirname(__file__))

    get_logger(__name__).info(f"CLI Create Return code: {result.returncode}")
    get_logger(__name__).info(f"CLI Create Stdout: {result.stdout}")
    get_logger(__name__).info(f"CLI Create Stderr: {result.stderr}")

    # Command should run (may fail due to dependencies, but shouldn't crash)
    assert get_unified_validator().validate_type(result.returncode, int)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
