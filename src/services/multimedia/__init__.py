#!/usr/bin/env python3
"""
Multimedia & Content Services Package
Real-time media processing, content management, and streaming capabilities
"""

from .media_processor_service import MediaProcessorService
from .video_capture_service import VideoCaptureService
from .audio_processing_service import AudioProcessingService
from .content_management_service import ContentManagementService
from .streaming_service import StreamingService

__all__ = [
    "MediaProcessorService",
    "VideoCaptureService",
    "AudioProcessingService",
    "ContentManagementService",
    "StreamingService",
]

__version__ = "1.0.0"
__author__ = "Multimedia & Content Specialist - Agent-3"
