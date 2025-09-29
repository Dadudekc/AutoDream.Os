#!/usr/bin/env python3
"""
Role Integration for Devlog Storytelling
=======================================

Integrates storytelling tools with the role assignment system.
V2 Compliant: ≤400 lines, focused role integration.

Author: Agent-7 (Implementation Specialist & Devlog Storyteller)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class RoleIntegration:
    """Integrates storytelling tools with the role assignment system."""
    
    def __init__(self):
        """Initialize role integration."""
        self.role_protocol_path = Path("config/protocols/devlog_storyteller.json")
        self.agent_capabilities_path = Path("config/agent_capabilities.json")
        self.tool_discovery_path = Path("config/storytelling/tool_discovery.json")
        
    def register_storytelling_tools(self) -> bool:
        """Register storytelling tools with the role system."""
        try:
            # Create tool discovery configuration
            tool_discovery = {
                "storytelling_tools": {
                    "main_service": "src.services.devlog_storytelling.DevlogStorytellingService",
                    "core_tools": {
                        "devlog_reader": "src.services.devlog_storytelling.core.devlog_reader.DevlogReader",
                        "story_compiler": "src.services.devlog_storytelling.core.story_compiler.StoryCompiler",
                        "character_tracker": "src.services.devlog_storytelling.core.character_tracker.CharacterTracker",
                        "world_builder": "src.services.devlog_storytelling.core.world_builder.WorldBuilder",
                        "story_validator": "src.services.devlog_storytelling.core.story_validator.StoryValidator"
                    },
                    "processor_tools": {
                        "batch_processor": "src.services.devlog_storytelling.processors.batch_processor.BatchProcessor",
                        "style_analyzer": "src.services.devlog_storytelling.processors.style_analyzer.StyleAnalyzer",
                        "archive_manager": "src.services.devlog_storytelling.processors.archive_manager.ArchiveManager"
                    },
                    "integration_tools": {
                        "devlog_integration": "src.services.devlog_storytelling.integration.devlog_integration.DevlogIntegration",
                        "role_integration": "src.services.devlog_storytelling.integration.role_integration.RoleIntegration"
                    },
                    "cli_tools": {
                        "storyteller_cli": "tools.devlog_storyteller_cli.DevlogStorytellerCLI"
                    }
                },
                "usage_examples": {
                    "basic_story_creation": {
                        "description": "Create story from recent devlogs",
                        "code": "from src.services.devlog_storytelling import create_story_from_devlogs\nresult = create_story_from_devlogs(batch_size=5)"
                    },
                    "full_service_usage": {
                        "description": "Use full storytelling service",
                        "code": "from src.services.devlog_storytelling import DevlogStorytellingService\nservice = DevlogStorytellingService()\nresult = service.process_devlog_batch(5)"
                    },
                    "individual_tool_usage": {
                        "description": "Use individual tools",
                        "code": "from src.services.devlog_storytelling.core.devlog_reader import DevlogReader\nreader = DevlogReader()\ndevlogs = reader.read_recent_devlogs(5)"
                    }
                },
                "role_specific_commands": {
                    "DEVLOG_STORYTELLER": {
                        "primary_command": "python tools/devlog_storyteller_cli.py --create-story",
                        "batch_processing": "python tools/devlog_storyteller_cli.py --auto-process",
                        "story_validation": "python tools/devlog_storyteller_cli.py --validate-chapters",
                        "character_tracking": "python tools/devlog_storyteller_cli.py --update-characters",
                        "world_building": "python tools/devlog_storyteller_cli.py --update-world"
                    }
                }
            }
            
            # Save tool discovery configuration
            self.tool_discovery_path.parent.mkdir(exist_ok=True)
            with open(self.tool_discovery_path, 'w') as f:
                json.dump(tool_discovery, f, indent=2)
            
            logger.info("✅ Storytelling tools registered with role system")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register storytelling tools: {e}")
            return False
    
    def get_available_tools_for_role(self, role: str) -> Dict[str, Any]:
        """Get available tools for a specific role."""
        try:
            if not self.tool_discovery_path.exists():
                self.register_storytelling_tools()
                
            with open(self.tool_discovery_path, 'r') as f:
                tool_discovery = json.load(f)
            
            if role == "DEVLOG_STORYTELLER":
                return tool_discovery["storytelling_tools"]
            else:
                return {}
                
        except Exception as e:
            logger.error(f"❌ Failed to get tools for role {role}: {e}")
            return {}
    
    def create_role_tool_guide(self) -> str:
        """Create a tool guide for the DEVLOG_STORYTELLER role."""
        guide = """
# 🎭 DEVLOG_STORYTELLER Role Tool Guide

## Available Tools

### Main Service
```python
from src.services.devlog_storytelling import DevlogStorytellingService
service = DevlogStorytellingService()
result = service.process_devlog_batch(5)
```

### Core Tools
```python
# Devlog Reading
from src.services.devlog_storytelling.core.devlog_reader import DevlogReader
reader = DevlogReader()
devlogs = reader.read_recent_devlogs(5)

# Story Compilation
from src.services.devlog_storytelling.core.story_compiler import StoryCompiler
compiler = StoryCompiler()
story = compiler.compile_story(devlogs)

# Character Tracking
from src.services.devlog_storytelling.core.character_tracker import CharacterTracker
tracker = CharacterTracker()
tracker.update_progressions(story_chapter)
```

### CLI Tools
```bash
# Create story from recent devlogs
python tools/devlog_storyteller_cli.py --create-story

# Auto-process every 5 devlogs
python tools/devlog_storyteller_cli.py --auto-process

# Validate existing stories
python tools/devlog_storyteller_cli.py --validate-chapters
```

### Configuration Files
- `config/storytelling_style_parameters.yaml` - Writing style parameters
- `config/storytelling/character_profiles.yaml` - Character definitions
- `config/storytelling/world_rules.yaml` - World building rules

## Role-Specific Workflow

1. **Check for new devlogs** - Use DevlogReader to get recent entries
2. **Process batch** - Use BatchProcessor when 5+ devlogs available
3. **Create story** - Use StoryCompiler to generate narrative
4. **Validate quality** - Use StoryValidator for coherence checks
5. **Update tracking** - Use CharacterTracker and WorldBuilder
6. **Archive results** - Use ArchiveManager to save stories

## Integration Points
- **Devlog System**: Reads from `devlogs/agent_devlogs.json`
- **Vector Database**: Searches for patterns and context
- **Role Assignment**: Receives assignments from Captain Agent-4
- **Messaging**: Reports progress via PyAutoGUI messaging
"""
        return guide
    
    def update_agent_tool_registry(self) -> bool:
        """Update the agent tool registry with storytelling tools."""
        try:
            # This would integrate with the main agent tool discovery system
            # For now, we'll create a local registry
            
            registry = {
                "storytelling_tools": {
                    "discovered_at": "2025-09-29T07:44:00Z",
                    "tools": [
                        {
                            "name": "DevlogStorytellingService",
                            "path": "src.services.devlog_storytelling",
                            "description": "Main storytelling service for MMORPG isekai story creation",
                            "capabilities": ["devlog_processing", "story_compilation", "character_tracking"],
                            "role_availability": ["DEVLOG_STORYTELLER"]
                        }
                    ]
                }
            }
            
            registry_path = Path("agent_workspaces/Agent-7/tool_registry.json")
            registry_path.parent.mkdir(exist_ok=True)
            
            with open(registry_path, 'w') as f:
                json.dump(registry, f, indent=2)
            
            logger.info("✅ Updated Agent-7 tool registry with storytelling tools")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update tool registry: {e}")
            return False
