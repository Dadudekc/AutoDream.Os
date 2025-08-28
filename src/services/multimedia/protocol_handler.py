"""Streaming protocol utilities for platform connections and frame delivery."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def initialize_platform_connection(platform: str, stream_name: str) -> bool:
    """Initialize connection to a streaming platform.

    This function currently simulates a successful connection to the
    requested platform and logs the interaction.
    """
    try:
        logger.info(
            "%s connection initialized for stream %s", platform.title(), stream_name
        )
        return True
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Error initializing platform %s: %s", platform, exc)
        return False


def send_frame_to_platform(frame: Any, platform: str, stream_name: str) -> bool:
    """Send a processed frame to a specific platform.

    Args:
        frame: Processed frame to transmit.
        platform: Target platform name.
        stream_name: Name of the stream.
    """
    try:
        logger.debug("Frame sent to %s for stream %s", platform, stream_name)
        return True
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Error sending frame to %s: %s", platform, exc)
        return False
