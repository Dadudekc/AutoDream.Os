#!/usr/bin/env python3
"""
Devlog Storytelling Service Package
==================================

Comprehensive storytelling system for converting devlogs into MMORPG isekai adventures.
V2 Compliant: ≤400 lines, focused storytelling functionality.

Author: Agent-7 (Implementation Specialist & Devlog Storyteller)
License: MIT
"""

from .core.devlog_reader import DevlogReader
from .core.story_compiler import StoryCompiler
from .core.character_tracker import CharacterTracker
from .core.world_builder import WorldBuilder
from .core.story_validator import StoryValidator
from .processors.batch_processor import BatchProcessor
from .processors.style_analyzer import StyleAnalyzer
from .processors.archive_manager import ArchiveManager
from .integration.devlog_integration import DevlogIntegration
from .integration.role_integration import RoleIntegration

__version__ = "1.0.0"
__author__ = "Agent-7"

# Main service class that agents will use
class DevlogStorytellingService:
    """Main storytelling service that agents can import and use."""
    
    def __init__(self):
        """Initialize the storytelling service with all components."""
        self.devlog_reader = DevlogReader()
        self.story_compiler = StoryCompiler()
        self.character_tracker = CharacterTracker()
        self.world_builder = WorldBuilder()
        self.story_validator = StoryValidator()
        self.batch_processor = BatchProcessor()
        self.style_analyzer = StyleAnalyzer()
        self.archive_manager = ArchiveManager()
        self.devlog_integration = DevlogIntegration()
        self.role_integration = RoleIntegration()
    
    def process_devlog_batch(self, batch_size: int = 5) -> dict:
        """Main method that agents will call to process devlog batches."""
        try:
            # Read devlogs
            devlogs = self.devlog_reader.read_recent_devlogs(batch_size)
            if len(devlogs) < batch_size:
                return {"status": "insufficient_devlogs", "count": len(devlogs)}
            
            # Process batch
            story_chapter = self.batch_processor.process_batch(devlogs)
            
            # Validate story
            validation_result = self.story_validator.validate_story(story_chapter)
            
            # Save to archive
            self.archive_manager.save_chapter(story_chapter)
            
            # Update character and world tracking
            self.character_tracker.update_progressions(story_chapter)
            self.world_builder.update_world_state(story_chapter)
            
            return {
                "status": "success",
                "chapter": story_chapter,
                "validation": validation_result
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Convenience functions for agents
def create_story_from_devlogs(batch_size: int = 5) -> dict:
    """Convenience function for agents to create stories."""
    service = DevlogStorytellingService()
    return service.process_devlog_batch(batch_size)

def get_storytelling_tools() -> dict:
    """Return available storytelling tools for agent discovery."""
    return {
        "main_service": "DevlogStorytellingService",
        "core_tools": [
            "DevlogReader",
            "StoryCompiler", 
            "CharacterTracker",
            "WorldBuilder",
            "StoryValidator"
        ],
        "processor_tools": [
            "BatchProcessor",
            "StyleAnalyzer",
            "ArchiveManager"
        ],
        "integration_tools": [
            "DevlogIntegration",
            "RoleIntegration"
        ],
        "convenience_functions": [
            "create_story_from_devlogs",
            "get_storytelling_tools"
        ]
    }
