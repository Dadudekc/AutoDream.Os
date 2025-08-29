"""
Multimedia & Content Processing Module
Agent_Cellphone_V2_Repository TDD Integration Project

This module provides comprehensive multimedia processing capabilities including:
- Real-time video/audio processing
- Webcam filter systems
- Content management and auto-blogging
- Streaming and distribution services
- OBS Virtual Camera integration
"""

__version__ = "1.0.0"
__author__ = "Multimedia & Content Specialist"
__status__ = "Development"

from .core import MultimediaCore
from .webcam_filters import WebcamFilterSystem
from .content_management import ContentManagementSystem
from .streaming import StreamingService
from .obs_integration import OBSVirtualCameraIntegration

__all__ = [
    "MultimediaCore",
    "WebcamFilterSystem",
    "ContentManagementSystem",
    "StreamingService",
    "OBSVirtualCameraIntegration",
]
