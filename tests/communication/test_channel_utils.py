import re

from src.core.communication.channel_utils import create_channel, default_channel_stats
from src.core.communication.channels import ChannelType


def test_create_channel_defaults():
    channel = create_channel("chan1", "Test", ChannelType.HTTP, "http://example.com")
    assert channel.id == "chan1"
    assert channel.name == "Test"
    assert channel.type == ChannelType.HTTP
    assert channel.url == "http://example.com"
    assert channel.status == "active"
    assert channel.message_count == 0
    assert channel.error_count == 0
    assert channel.config == {}
    # ISO timestamp pattern for created_at/last_used
    iso_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:")
    assert iso_pattern.match(channel.created_at)
    assert iso_pattern.match(channel.last_used)


def test_default_channel_stats():
    stats = default_channel_stats()
    assert stats["total_messages"] == 0
    assert stats["successful_messages"] == 0
    assert stats["failed_messages"] == 0
    assert "last_activity" in stats
    assert stats["uptime_percentage"] == 100.0
    assert stats["average_response_time"] == 0.0
    assert stats["error_rate"] == 0.0
