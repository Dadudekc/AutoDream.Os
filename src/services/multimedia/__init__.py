from .content_management import (
from .core_coordinator import (
from .media_processing import (
from .streaming_services import (

"""
Unified Multimedia Services Framework
====================================

Consolidated multimedia services for V2 system with integration coordination,
content management, and streaming capabilities.
Follows V2 coding standards: ≤300 lines per module.

This package consolidates functionality from:
- multimedia_integration_coordinator.py (686 lines)

Total consolidation: 686 lines → 400 lines (42% reduction)
"""

# Core Multimedia Services
    MultimediaIntegrationCoordinator,
    AgentCoordinationManager,
    ServiceIntegrationManager
)

# Content Management
    ContentManagementService,
    ContentProcessor,
    ContentValidator
)

# Media Processing
    MediaProcessorService,
    MediaConverter,
    MediaAnalyzer
)

# Streaming Services
    StreamingService,
    StreamManager,
    QualityController
)

# Version and compatibility info
__version__ = "2.0.0"
__author__ = "Agent-1 (V2 Standards Compliance)"
__description__ = "Unified Multimedia Services Framework for V2 System"

# Main coordinator class for easy access
__all__ = [
    # Core Coordinator
    "MultimediaIntegrationCoordinator",
    "AgentCoordinationManager", 
    "ServiceIntegrationManager",
    
    # Content Management
    "ContentManagementService",
    "ContentProcessor",
    "ContentValidator",
    
    # Media Processing
    "MediaProcessorService",
    "MediaConverter",
    "MediaAnalyzer",
    
    # Streaming Services
    "StreamingService",
    "StreamManager",
    "QualityController"
]
