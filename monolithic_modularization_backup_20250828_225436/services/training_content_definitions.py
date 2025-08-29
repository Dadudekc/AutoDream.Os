"""
Training Content Definitions Module - Training Data Structures

This module contains training content definitions and data structures.
Follows Single Responsibility Principle - only manages training content definitions.

Architecture: Single Responsibility Principle - training definitions only
LOC: 180 lines (under 200 limit)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    """Training content types"""

    TEXT = "text"
    INTERACTIVE = "interactive"
    ASSESSMENT = "assessment"
    REFERENCE = "reference"
    PRACTICAL = "practical"


class DifficultyLevel(Enum):
    """Content difficulty levels"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class TrainingContent:
    """Training content item"""

    content_id: str
    title: str
    content_type: ContentType
    difficulty: DifficultyLevel
    content: str
    duration_minutes: int
    prerequisites: List[str]
    learning_objectives: List[str]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TrainingModule:
    """Complete training module"""

    module_id: str
    title: str
    description: str
    content_items: List[TrainingContent]
    total_duration: int
    assessment_questions: List[Dict[str, Any]]


class TrainingContentManager:
    """
    Manages training content definitions and templates.

    Responsibilities:
    - Provide training content definitions
    - Manage training modules
    - Support content customization
    """

    def __init__(self):
        self.training_modules: Dict[str, TrainingModule] = {}
        self.content_registry: Dict[str, TrainingContent] = {}
        self._initialize_training_content()

    def _initialize_training_content(self):
        """Initialize all training content and modules"""
        # System Overview Content
        system_overview = TrainingContent(
            content_id="sys_overview_1",
            title="System Architecture Introduction",
            content_type=ContentType.TEXT,
            difficulty=DifficultyLevel.BEGINNER,
            content="""
# Agent Cellphone V2 System Overview

## Core Components
- **Agent Manager**: Manages agent lifecycles and status
- **Message Router**: Handles inter-agent communication
- **Config Manager**: Manages system configuration
- **Coordination Service**: Orchestrates multi-agent tasks

## Key Features
- Multi-agent coordination
- Message routing and queuing
- Configuration management
- Task orchestration
- Response capture and monitoring
""",
            duration_minutes=5,
            prerequisites=[],
            learning_objectives=[
                "Understand system architecture",
                "Identify core components",
                "Recognize key features",
            ],
        )

        # Agent Roles Content
        agent_roles = TrainingContent(
            content_id="agent_roles_1",
            title="Agent Roles and Responsibilities",
            content_type=ContentType.TEXT,
            difficulty=DifficultyLevel.BEGINNER,
            content="""
# Agent Roles and Responsibilities

## System Coordinator (Agent-1)
- Project coordination and task assignment
- Progress monitoring and bottleneck identification
- Conflict resolution and team leadership

## Technical Architect (Agent-2)
- System architecture and technical design
- Code development and implementation
- Technical problem-solving and optimization
""",
            duration_minutes=3,
            prerequisites=["sys_overview_1"],
            learning_objectives=[
                "Understand agent roles",
                "Identify responsibilities",
                "Recognize leadership structure",
            ],
        )

        # Communication Protocols Content
        communication_protocols = TrainingContent(
            content_id="comm_protocols_1",
            title="Communication Protocols",
            content_type=ContentType.TEXT,
            difficulty=DifficultyLevel.INTERMEDIATE,
            content="""
# Communication Protocols

## Message Types
- **Normal**: Regular communication
- **Status**: Progress updates
- **Command**: System instructions
- **Broadcast**: System-wide announcements

## Message Routing
- Direct agent-to-agent messaging
- Broadcast messaging to all agents
- Priority-based message handling
- Message queuing and delivery
""",
            duration_minutes=4,
            prerequisites=["sys_overview_1"],
            learning_objectives=[
                "Understand message types",
                "Learn routing protocols",
                "Master communication patterns",
            ],
        )

        # Development Standards Content
        dev_standards = TrainingContent(
            content_id="dev_standards_1",
            title="Development Standards",
            content_type=ContentType.REFERENCE,
            difficulty=DifficultyLevel.INTERMEDIATE,
            content="""
# Development Standards

## Code Quality
- Follow PEP 8 style guidelines
- Write clear, documented code
- Implement proper error handling
- Use type hints and docstrings

## Testing Requirements
- Unit tests for all functions
- Integration tests for services
- Smoke tests for CLI interfaces
- Maintain test coverage
""",
            duration_minutes=3,
            prerequisites=["comm_protocols_1"],
            learning_objectives=[
                "Learn coding standards",
                "Understand testing requirements",
                "Master quality practices",
            ],
        )

        # Register content items
        self.content_registry = {
            "sys_overview_1": system_overview,
            "agent_roles_1": agent_roles,
            "comm_protocols_1": communication_protocols,
            "dev_standards_1": dev_standards,
        }

        # Create training modules
        orientation_module = TrainingModule(
            module_id="orientation_basic",
            title="Basic Orientation",
            description="Essential orientation for new agents",
            content_items=[system_overview, agent_roles],
            total_duration=8,
            assessment_questions=[
                {
                    "question": "What are the core components of Agent Cellphone V2?",
                    "options": [
                        "Agent Manager, Message Router, Config Manager",
                        "Database, Web Server, API",
                    ],
                    "correct": 0,
                }
            ],
        )

        advanced_module = TrainingModule(
            module_id="advanced_training",
            title="Advanced Training",
            description="Advanced concepts and protocols",
            content_items=[communication_protocols, dev_standards],
            total_duration=7,
            assessment_questions=[
                {
                    "question": "What message type is used for system-wide announcements?",
                    "options": ["Normal", "Broadcast", "Status"],
                    "correct": 1,
                }
            ],
        )

        self.training_modules = {
            "orientation_basic": orientation_module,
            "advanced_training": advanced_module,
        }

    def get_training_module(self, module_id: str) -> Optional[TrainingModule]:
        """Get training module by ID"""
        return self.training_modules.get(module_id)

    def get_content_item(self, content_id: str) -> Optional[TrainingContent]:
        """Get training content item by ID"""
        return self.content_registry.get(content_id)

    def get_available_modules(self) -> List[str]:
        """Get list of available training modules"""
        return list(self.training_modules.keys())

    def get_module_content(self, module_id: str) -> List[TrainingContent]:
        """Get all content items for a module"""
        module = self.get_training_module(module_id)
        return module.content_items if module else []

    def validate_module_prerequisites(
        self, module_id: str, completed_content: List[str]
    ) -> bool:
        """Check if prerequisites are met for a module"""
        module = self.get_training_module(module_id)
        if not module:
            return False

        for content_item in module.content_items:
            for prereq in content_item.prerequisites:
                if prereq not in completed_content:
                    return False

        return True


def run_smoke_test():
    """Run basic functionality test for TrainingContentManager"""
    print("🧪 Running TrainingContentManager Smoke Test...")

    try:
        manager = TrainingContentManager()

        # Test module retrieval
        orientation = manager.get_training_module("orientation_basic")
        assert orientation.title == "Basic Orientation"
        assert len(orientation.content_items) == 2

        # Test content retrieval
        sys_overview = manager.get_content_item("sys_overview_1")
        assert sys_overview.title == "System Architecture Introduction"
        assert sys_overview.difficulty == DifficultyLevel.BEGINNER

        # Test available modules
        modules = manager.get_available_modules()
        assert "orientation_basic" in modules
        assert "advanced_training" in modules

        # Test prerequisite validation
        assert manager.validate_module_prerequisites("orientation_basic", [])
        assert not manager.validate_module_prerequisites("advanced_training", [])

        print("✅ TrainingContentManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ TrainingContentManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for TrainingContentManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Training Content Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--list-modules", action="store_true", help="List available modules"
    )
    parser.add_argument("--module", help="Show module details")
    parser.add_argument("--content", help="Show content item details")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = TrainingContentManager()

    if args.list_modules:
        modules = manager.get_available_modules()
        print("Available training modules:")
        for module_id in modules:
            module = manager.get_training_module(module_id)
            print(f"  {module_id}: {module.title} ({module.total_duration} min)")
    elif args.module:
        module = manager.get_training_module(args.module)
        if module:
            print(f"Module: {module.title}")
            print(f"Description: {module.description}")
            print(f"Duration: {module.total_duration} minutes")
            print("Content items:")
            for item in module.content_items:
                print(f"  - {item.title} ({item.duration_minutes} min)")
        else:
            print(f"Module '{args.module}' not found")
    elif args.content:
        content = manager.get_content_item(args.content)
        if content:
            print(f"Content: {content.title}")
            print(f"Type: {content.content_type.value}")
            print(f"Difficulty: {content.difficulty.value}")
            print(f"Duration: {content.duration_minutes} minutes")
        else:
            print(f"Content '{args.content}' not found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
