"""Webcam filter system configuration utilities."""
from typing import Dict, Any


def default_webcam_config() -> Dict[str, Any]:
    """Default configuration for the webcam filter system."""
    return {
        "camera_index": 0,
        "frame_rate": 30,
        "resolution": (1280, 720),
        "quality": "high",
        "enable_preview": True,
        "preview_window_size": (640, 480),
        "filter_chain_max": 10,
        "auto_save_filtered": True,
        "save_directory": "/tmp/filtered_frames",
        "obs_integration": {
            "enabled": True,
            "output_resolution": (1920, 1080),
            "frame_rate": 30,
        },
    }
