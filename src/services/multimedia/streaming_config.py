
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration and constants for streaming services."""

from typing import Dict, Any

# Default streaming configuration
DEFAULT_STREAMING_CONFIG: Dict[str, Any] = {
    "max_streams": 5,
    "default_quality": "720p",
    "buffer_size": 1000,
    "auto_restart": True,
    "quality_presets": {
        "1080p": {"width": 1920, "height": 1080, "bitrate": 5000},
        "720p": {"width": 1280, "height": 720, "bitrate": 2500},
        "480p": {"width": 854, "height": 480, "bitrate": 1000},
    },
}

# Supported platforms and schedule types
VALID_PLATFORMS = ["youtube", "twitch", "facebook", "instagram", "tiktok", "custom"]
VALID_SCHEDULE_TYPES = ["once", "daily", "weekly", "monthly", "custom"]
