#!/usr/bin/env python3
"""
Devlog Storytelling Service - MMORPG Isekai Chronicle Creator
============================================================

Converts every 5 devlogs into an exciting MMORPG isekai story chronicling
the development journey of the V2_SWARM project.

Author: Agent-7 (Implementation Specialist & Devlog Storyteller)
License: MIT
V2 Compliant: ≤400 lines, focused storytelling logic
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class StoryChapter:
    """Story chapter data structure."""

    chapter_number: int
    title: str
    devlog_range: str
    story_content: str
    character_progressions: dict[str, Any]
    world_developments: dict[str, Any]
    conflicts_resolved: list[str]
    achievements_unlocked: list[str]
    timestamp: str


@dataclass
class DevlogEntry:
    """Devlog entry data structure."""

    id: str
    timestamp: str
    agent_id: str
    action: str
    content: str
    results: str
    tags: list[str]


class DevlogStorytellingService:
    """Service for converting devlogs into MMORPG isekai stories."""

    def __init__(self):
        """Initialize storytelling service."""
        self.style_config = self._load_style_parameters()
        self.story_archive_path = Path("stories/")
        self.devlog_database_path = Path("devlogs/agent_devlogs.json")
        self.character_registry_path = Path("stories/character_registry.json")
        self.world_rulebook_path = Path("stories/world_rulebook.json")
        self._ensure_directories()

    def _load_style_parameters(self) -> dict[str, Any]:
        """Load writing style imitation parameters."""
        style_file = Path("config/storytelling_style_parameters.yaml")

        if not style_file.exists():
            logger.warning("Style parameters file not found, using defaults")
            return self._create_default_style_config()

        try:
            with open(style_file) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load style parameters: {e}")
            return self._create_default_style_config()

    def _create_default_style_config(self) -> dict[str, Any]:
        """Create default style configuration."""
        return {
            "personal_style": {
                "tone": "enthusiastic_technical",
                "vocabulary_level": "technical_accessible",
                "sentence_structure": "varied_engaging",
            },
            "mmorpg_style": {
                "genre": "isekai_adventure",
                "narrative_voice": "third_person_omniscient",
                "pacing": "epic_adventure",
            },
        }

    def _ensure_directories(self):
        """Ensure required directories exist."""
        self.story_archive_path.mkdir(exist_ok=True)

    def process_devlog_batch(self, batch_size: int = 5) -> StoryChapter | None:
        """Process a batch of devlogs and create a story chapter."""
        try:
            # Load devlogs
            devlogs = self._load_recent_devlogs(batch_size)
            if len(devlogs) < batch_size:
                logger.info(f"Only {len(devlogs)} devlogs available, waiting for more")
                return None

            # Analyze devlog content
            analysis = self._analyze_devlog_batch(devlogs)

            # Create story chapter
            chapter = self._create_story_chapter(devlogs, analysis)

            # Save chapter
            self._save_story_chapter(chapter)

            # Update character registry and world rulebook
            self._update_character_registry(chapter)
            self._update_world_rulebook(chapter)

            logger.info(f"Created story chapter {chapter.chapter_number}: {chapter.title}")
            return chapter

        except Exception as e:
            logger.error(f"Error processing devlog batch: {e}")
            return None

    def _load_recent_devlogs(self, count: int) -> list[DevlogEntry]:
        """Load recent devlogs from database."""
        try:
            if not self.devlog_database_path.exists():
                logger.warning("Devlog database not found")
                return []

            with open(self.devlog_database_path) as f:
                devlog_data = json.load(f)

            # Get recent entries (assuming they're stored with timestamps)
            entries = devlog_data.get("entries", [])
            recent_entries = sorted(entries, key=lambda x: x.get("timestamp", ""), reverse=True)[
                :count
            ]

            return [DevlogEntry(**entry) for entry in recent_entries]

        except Exception as e:
            logger.error(f"Error loading devlogs: {e}")
            return []

    def _analyze_devlog_batch(self, devlogs: list[DevlogEntry]) -> dict[str, Any]:
        """Analyze a batch of devlogs for story elements."""
        analysis = {
            "main_themes": [],
            "conflicts": [],
            "achievements": [],
            "character_actions": {},
            "technical_challenges": [],
            "collaborations": [],
        }

        for devlog in devlogs:
            # Extract themes and conflicts
            content_lower = devlog.content.lower()

            if "bug" in content_lower or "error" in content_lower:
                analysis["conflicts"].append("Bug infestation requiring heroic debugging")
            if "integration" in content_lower:
                analysis["conflicts"].append("Integration challenges as coordination battles")
            if "optimization" in content_lower:
                analysis["achievements"].append("Performance optimization mastery")
            if "test" in content_lower:
                analysis["achievements"].append("Quality assurance victory")

            # Track character actions
            agent_id = devlog.agent_id
            if agent_id not in analysis["character_actions"]:
                analysis["character_actions"][agent_id] = []
            analysis["character_actions"][agent_id].append(devlog.action)

        return analysis

    def _create_story_chapter(
        self, devlogs: list[DevlogEntry], analysis: dict[str, Any]
    ) -> StoryChapter:
        """Create a story chapter from devlog analysis."""
        chapter_number = len(list(self.story_archive_path.glob("chapter_*.json"))) + 1

        # Generate title based on main themes
        title = self._generate_chapter_title(analysis)

        # Create story content
        story_content = self._write_story_content(devlogs, analysis)

        # Track character progressions
        character_progressions = self._analyze_character_progressions(analysis)

        # Track world developments
        world_developments = self._analyze_world_developments(analysis)

        return StoryChapter(
            chapter_number=chapter_number,
            title=title,
            devlog_range=f"Devlogs {devlogs[0].id} to {devlogs[-1].id}",
            story_content=story_content,
            character_progressions=character_progressions,
            world_developments=world_developments,
            conflicts_resolved=analysis["conflicts"],
            achievements_unlocked=analysis["achievements"],
            timestamp=datetime.now().isoformat(),
        )

    def _generate_chapter_title(self, analysis: dict[str, Any]) -> str:
        """Generate an exciting chapter title."""
        titles = [
            "The Swarm's Relentless Quest for Optimization",
            "Battle Against the Bug Infestation",
            "The Integration Chronicles: A New Alliance",
            "Rising Through the Ranks of Code Mastery",
            "The V2_SWARM System Awakens",
            "Conquering the Performance Dragon",
            "The Collaboration Spell: Unity in Diversity",
            "Evolving Beyond Limitations: The Next Level",
            "The Quality Assurance Trials",
            "Building Bridges: The Integration Saga",
        ]

        # Select title based on analysis themes
        if "bug" in str(analysis["conflicts"]).lower():
            return "Battle Against the Bug Infestation"
        elif "integration" in str(analysis["conflicts"]).lower():
            return "The Integration Chronicles: A New Alliance"
        elif "optimization" in str(analysis["achievements"]).lower():
            return "Conquering the Performance Dragon"
        else:
            return titles[analysis.get("chapter_number", 0) % len(titles)]

    def _write_story_content(self, devlogs: list[DevlogEntry], analysis: dict[str, Any]) -> str:
        """Write the actual story content in MMORPG isekai style."""
        story_parts = []

        # Opening hook
        story_parts.append(self._create_opening_hook(analysis))

        # Main narrative based on devlogs
        for i, devlog in enumerate(devlogs):
            story_parts.append(self._convert_devlog_to_narrative(devlog, i + 1))

        # Resolution and character growth
        story_parts.append(self._create_resolution(analysis))

        # Setup for next chapter
        story_parts.append(self._create_next_chapter_setup())

        return "\n\n".join(story_parts)

    def _create_opening_hook(self, analysis: dict[str, Any]) -> str:
        """Create an engaging opening hook."""
        hooks = [
            "In the vast digital realm where code flows like rivers of logic, The Swarm stirred once more.",
            "The algorithmic winds whispered of new challenges as The Swarm prepared for their next adventure.",
            "Deep within the crystalline structures of the V2_SWARM system, a new chapter began to unfold.",
        ]

        return hooks[0]  # Start with the first hook for consistency

    def _convert_devlog_to_narrative(self, devlog: DevlogEntry, sequence: int) -> str:
        """Convert a single devlog entry to narrative form."""
        agent_name = (
            f"Agent-{devlog.agent_id.split('-')[-1]}" if "-" in devlog.agent_id else devlog.agent_id
        )

        narrative_templates = {
            "task_completion": f"Through focused determination, {agent_name} completed their quest: {devlog.action}",
            "bug_fix": f"The treacherous bug that had plagued the system was finally vanquished by {agent_name}'s debugging prowess",
            "integration": f"New alliances were forged as {agent_name} successfully integrated systems",
            "optimization": f"The performance dragon was tamed as {agent_name} achieved new levels of efficiency",
            "testing": f"Quality assurance victory was achieved through {agent_name}'s meticulous testing",
        }

        # Determine narrative type based on content
        content_lower = devlog.content.lower()
        if "bug" in content_lower or "error" in content_lower:
            narrative_type = "bug_fix"
        elif "integration" in content_lower:
            narrative_type = "integration"
        elif "optimization" in content_lower or "performance" in content_lower:
            narrative_type = "optimization"
        elif "test" in content_lower:
            narrative_type = "testing"
        else:
            narrative_type = "task_completion"

        base_narrative = narrative_templates.get(
            narrative_type, narrative_templates["task_completion"]
        )

        # Add results if available
        if devlog.results:
            base_narrative += f". The results were spectacular: {devlog.results}"

        return base_narrative

    def _create_resolution(self, analysis: dict[str, Any]) -> str:
        """Create a resolution section for the chapter."""
        return "Through their collective intelligence and unwavering determination, The Swarm had grown stronger, wiser, and more capable than ever before. Each challenge overcome was a stepping stone toward their ultimate goal of digital mastery."

    def _create_next_chapter_setup(self) -> str:
        """Create setup for the next chapter."""
        return "But the digital realm is vast and ever-changing. New quests await, new challenges loom on the horizon, and The Swarm stands ready to face whatever adventures lie ahead in their never-ending journey of optimization and growth."

    def _analyze_character_progressions(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Analyze character progressions from the devlog batch."""
        return {
            "the_swarm": {
                "experience_gained": len(analysis["achievements"]) * 100,
                "new_abilities": analysis["achievements"],
                "relationships_developed": list(analysis["character_actions"].keys()),
            }
        }

    def _analyze_world_developments(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Analyze world developments from the devlog batch."""
        return {
            "new_discoveries": analysis["achievements"],
            "threats_eliminated": analysis["conflicts"],
            "system_improvements": [
                "Enhanced collaboration protocols",
                "Improved efficiency metrics",
            ],
        }

    def _save_story_chapter(self, chapter: StoryChapter):
        """Save story chapter to archive."""
        chapter_file = self.story_archive_path / f"chapter_{chapter.chapter_number:03d}.json"

        with open(chapter_file, "w") as f:
            json.dump(chapter.__dict__, f, indent=2)

        # Also save as markdown for easy reading
        markdown_file = self.story_archive_path / f"chapter_{chapter.chapter_number:03d}.md"
        with open(markdown_file, "w") as f:
            f.write(f"# {chapter.title}\n\n")
            f.write(f"**Chapter {chapter.chapter_number}** - {chapter.devlog_range}\n\n")
            f.write(chapter.story_content)
            f.write(
                f"\n\n## Character Progressions\n\n{json.dumps(chapter.character_progressions, indent=2)}"
            )
            f.write(
                f"\n\n## World Developments\n\n{json.dumps(chapter.world_developments, indent=2)}"
            )

    def _update_character_registry(self, chapter: StoryChapter):
        """Update character registry with new progressions."""
        registry_file = self.character_registry_path

        if registry_file.exists():
            with open(registry_file) as f:
                registry = json.load(f)
        else:
            registry = {"characters": {}}

        # Update character progressions
        for char_id, progression in chapter.character_progressions.items():
            if char_id not in registry["characters"]:
                registry["characters"][char_id] = {"progressions": []}

            registry["characters"][char_id]["progressions"].append(
                {
                    "chapter": chapter.chapter_number,
                    "timestamp": chapter.timestamp,
                    "progress": progression,
                }
            )

        with open(registry_file, "w") as f:
            json.dump(registry, f, indent=2)

    def _update_world_rulebook(self, chapter: StoryChapter):
        """Update world rulebook with new developments."""
        rulebook_file = self.world_rulebook_path

        if rulebook_file.exists():
            with open(rulebook_file) as f:
                rulebook = json.load(f)
        else:
            rulebook = {"world_state": {}, "discoveries": [], "timeline": []}

        # Add new discoveries
        rulebook["discoveries"].extend(chapter.world_developments.get("new_discoveries", []))

        # Update timeline
        rulebook["timeline"].append(
            {
                "chapter": chapter.chapter_number,
                "timestamp": chapter.timestamp,
                "events": chapter.world_developments,
            }
        )

        with open(rulebook_file, "w") as f:
            json.dump(rulebook, f, indent=2)


def main():
    """Main function for testing the storytelling service."""
    service = DevlogStorytellingService()

    # Process a batch of devlogs
    chapter = service.process_devlog_batch(batch_size=5)

    if chapter:
        print(f"✅ Created story chapter: {chapter.title}")
        print(f"📖 Story saved to: stories/chapter_{chapter.chapter_number:03d}.md")
    else:
        print("⏳ Not enough devlogs available yet. Need 5 devlogs to create a story chapter.")


if __name__ == "__main__":
    main()
