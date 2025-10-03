#!/usr/bin/env python3
"""
Devlog Storytelling Service
==========================
Agent-6 refactored devlog storytelling service
V2 Compliant: ≤400 lines, focused storytelling logic
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class StoryElement:
    """Individual story element"""

    element_type: str
    content: str
    metadata: dict[str, Any]
    timestamp: str


@dataclass
class DevlogStory:
    """Complete devlog story structure"""

    title: str
    summary: str
    timeline: list[StoryElement]
    key_achievements: list[str]
    challenges_overcome: list[str]
    lessons_learned: list[str]
    next_steps: list[str]
    metadata: dict[str, Any]


class DevlogStorytellingService:
    """V2 compliant devlog storytelling service"""

    def __init__(self, stories_dir: str = "devlog_stories"):
        self.stories_dir = Path(stories_dir)
        self.stories_dir.mkdir(exist_ok=True)

        # Story templates
        self.story_templates = {
            "task_completion": self._create_task_completion_story,
            "bug_fix": self._create_bug_fix_story,
            "feature_implementation": self._create_feature_story,
            "system_optimization": self._create_optimization_story,
        }

    def create_story_from_devlog(self, devlog_file: Path, story_type: str = "auto") -> DevlogStory:
        """Create a story from devlog file"""
        try:
            with open(devlog_file, encoding="utf-8") as f:
                content = f.read()

            # Parse devlog content
            parsed_content = self._parse_devlog_content(content)

            # Determine story type if auto
            if story_type == "auto":
                story_type = self._determine_story_type(parsed_content)

            # Create story using appropriate template
            if story_type in self.story_templates:
                story = self.story_templates[story_type](parsed_content)
            else:
                story = self._create_generic_story(parsed_content)

            return story

        except Exception as e:
            return self._create_error_story(str(e))

    def _parse_devlog_content(self, content: str) -> dict[str, Any]:
        """Parse devlog content into structured data"""
        parsed = {
            "title": "",
            "agent_id": "",
            "action": "",
            "status": "",
            "details": "",
            "timestamp": "",
            "metadata": {},
        }

        # Extract title
        title_match = re.search(r"# 🤖 Agent Devlog - (.+)", content)
        if title_match:
            parsed["title"] = title_match.group(1)

        # Extract agent ID
        agent_match = re.search(r"- \*\*Agent ID:\*\* (.+)", content)
        if agent_match:
            parsed["agent_id"] = agent_match.group(1)

        # Extract action
        action_match = re.search(r"\*\*Action:\*\* (.+)", content)
        if action_match:
            parsed["action"] = action_match.group(1)

        # Extract status
        status_match = re.search(r"- \*\*Status:\*\* (.+)", content)
        if status_match:
            parsed["status"] = status_match.group(1)

        # Extract timestamp
        timestamp_match = re.search(r"## 📅 Timestamp\n(.+)", content)
        if timestamp_match:
            parsed["timestamp"] = timestamp_match.group(1)

        # Extract details
        details_match = re.search(r"## 📋 Additional Details\n(.+?)(?=##|$)", content, re.DOTALL)
        if details_match:
            parsed["details"] = details_match.group(1).strip()

        return parsed

    def _determine_story_type(self, parsed_content: dict[str, Any]) -> str:
        """Determine story type from content"""
        action = parsed_content.get("action", "").lower()

        if any(word in action for word in ["fix", "bug", "error", "issue"]):
            return "bug_fix"
        elif any(word in action for word in ["implement", "create", "add", "build"]):
            return "feature_implementation"
        elif any(word in action for word in ["optimize", "improve", "enhance", "performance"]):
            return "system_optimization"
        else:
            return "task_completion"

    def _create_task_completion_story(self, content: dict[str, Any]) -> DevlogStory:
        """Create task completion story"""
        return DevlogStory(
            title=f"Task Completed: {content.get('action', 'Unknown Task')}",
            summary=f"Successfully completed task assigned to {content.get('agent_id', 'Unknown Agent')}",
            timeline=[
                StoryElement("start", "Task assigned", {}, content.get("timestamp", "")),
                StoryElement(
                    "progress", content.get("action", ""), {}, content.get("timestamp", "")
                ),
                StoryElement(
                    "completion", "Task completed successfully", {}, content.get("timestamp", "")
                ),
            ],
            key_achievements=[
                f"Completed: {content.get('action', 'Task')}",
                f"Status: {content.get('status', 'Unknown')}",
            ],
            challenges_overcome=[],
            lessons_learned=[],
            next_steps=["Continue with next assigned task"],
            metadata=content.get("metadata", {}),
        )

    def _create_bug_fix_story(self, content: dict[str, Any]) -> DevlogStory:
        """Create bug fix story"""
        return DevlogStory(
            title=f"Bug Fix: {content.get('action', 'Unknown Issue')}",
            summary="Identified and resolved critical bug affecting system stability",
            timeline=[
                StoryElement("discovery", "Bug discovered", {}, content.get("timestamp", "")),
                StoryElement(
                    "investigation", "Root cause analysis", {}, content.get("timestamp", "")
                ),
                StoryElement(
                    "fix",
                    content.get("action", "Bug fix applied"),
                    {},
                    content.get("timestamp", ""),
                ),
                StoryElement(
                    "verification", "Fix verified and tested", {}, content.get("timestamp", "")
                ),
            ],
            key_achievements=[
                f"Fixed: {content.get('action', 'Bug')}",
                "System stability restored",
                "Prevented potential data loss",
            ],
            challenges_overcome=["Complex debugging process", "Minimizing system downtime"],
            lessons_learned=[
                "Importance of thorough testing",
                "Value of systematic debugging approach",
            ],
            next_steps=["Monitor system stability", "Implement preventive measures"],
            metadata=content.get("metadata", {}),
        )

    def _create_feature_story(self, content: dict[str, Any]) -> DevlogStory:
        """Create feature implementation story"""
        return DevlogStory(
            title=f"Feature Implemented: {content.get('action', 'New Feature')}",
            summary="Successfully implemented new feature to enhance system capabilities",
            timeline=[
                StoryElement(
                    "planning", "Feature requirements defined", {}, content.get("timestamp", "")
                ),
                StoryElement("design", "Architecture designed", {}, content.get("timestamp", "")),
                StoryElement(
                    "implementation",
                    content.get("action", "Feature implemented"),
                    {},
                    content.get("timestamp", ""),
                ),
                StoryElement(
                    "testing", "Feature tested and validated", {}, content.get("timestamp", "")
                ),
                StoryElement(
                    "deployment", "Feature deployed successfully", {}, content.get("timestamp", "")
                ),
            ],
            key_achievements=[
                f"Implemented: {content.get('action', 'Feature')}",
                "Enhanced system functionality",
                "Improved user experience",
            ],
            challenges_overcome=["Complex integration requirements", "Performance optimization"],
            lessons_learned=["Importance of modular design", "Value of iterative development"],
            next_steps=[
                "Monitor feature performance",
                "Gather user feedback",
                "Plan future enhancements",
            ],
            metadata=content.get("metadata", {}),
        )

    def _create_optimization_story(self, content: dict[str, Any]) -> DevlogStory:
        """Create system optimization story"""
        return DevlogStory(
            title=f"System Optimized: {content.get('action', 'Performance Improvement')}",
            summary="Successfully optimized system performance and efficiency",
            timeline=[
                StoryElement(
                    "analysis",
                    "Performance bottlenecks identified",
                    {},
                    content.get("timestamp", ""),
                ),
                StoryElement(
                    "planning", "Optimization strategy developed", {}, content.get("timestamp", "")
                ),
                StoryElement(
                    "implementation",
                    content.get("action", "Optimizations applied"),
                    {},
                    content.get("timestamp", ""),
                ),
                StoryElement(
                    "measurement",
                    "Performance improvements measured",
                    {},
                    content.get("timestamp", ""),
                ),
            ],
            key_achievements=[
                f"Optimized: {content.get('action', 'System')}",
                "Improved performance metrics",
                "Reduced resource consumption",
            ],
            challenges_overcome=[
                "Identifying performance bottlenecks",
                "Maintaining system stability during optimization",
            ],
            lessons_learned=[
                "Importance of performance monitoring",
                "Value of systematic optimization approach",
            ],
            next_steps=[
                "Continue monitoring performance",
                "Identify additional optimization opportunities",
            ],
            metadata=content.get("metadata", {}),
        )

    def _create_generic_story(self, content: dict[str, Any]) -> DevlogStory:
        """Create generic story for unknown types"""
        return DevlogStory(
            title=f"Activity: {content.get('action', 'Unknown Activity')}",
            summary=f"Completed activity by {content.get('agent_id', 'Unknown Agent')}",
            timeline=[
                StoryElement(
                    "activity",
                    content.get("action", "Activity performed"),
                    {},
                    content.get("timestamp", ""),
                )
            ],
            key_achievements=[content.get("action", "Activity completed")],
            challenges_overcome=[],
            lessons_learned=[],
            next_steps=["Continue with assigned tasks"],
            metadata=content.get("metadata", {}),
        )

    def _create_error_story(self, error_message: str) -> DevlogStory:
        """Create error story for failed parsing"""
        return DevlogStory(
            title="Story Creation Failed",
            summary=f"Failed to create story due to error: {error_message}",
            timeline=[
                StoryElement("error", f"Error: {error_message}", {}, datetime.now().isoformat())
            ],
            key_achievements=[],
            challenges_overcome=[],
            lessons_learned=["Need to improve error handling in story creation"],
            next_steps=["Fix story creation process"],
            metadata={"error": True},
        )

    def save_story(self, story: DevlogStory, filename: str = None) -> Path:
        """Save story to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"story_{timestamp}.json"

        story_file = self.stories_dir / filename

        # Convert story to dict for JSON serialization
        story_dict = {
            "title": story.title,
            "summary": story.summary,
            "timeline": [
                {
                    "element_type": element.element_type,
                    "content": element.content,
                    "metadata": element.metadata,
                    "timestamp": element.timestamp,
                }
                for element in story.timeline
            ],
            "key_achievements": story.key_achievements,
            "challenges_overcome": story.challenges_overcome,
            "lessons_learned": story.lessons_learned,
            "next_steps": story.next_steps,
            "metadata": story.metadata,
            "created_at": datetime.now().isoformat(),
        }

        with open(story_file, "w", encoding="utf-8") as f:
            json.dump(story_dict, f, indent=2)

        return story_file

    def load_story(self, story_file: Path) -> DevlogStory:
        """Load story from file"""
        with open(story_file, encoding="utf-8") as f:
            story_dict = json.load(f)

        # Reconstruct timeline
        timeline = [
            StoryElement(
                element["element_type"],
                element["content"],
                element["metadata"],
                element["timestamp"],
            )
            for element in story_dict["timeline"]
        ]

        return DevlogStory(
            title=story_dict["title"],
            summary=story_dict["summary"],
            timeline=timeline,
            key_achievements=story_dict["key_achievements"],
            challenges_overcome=story_dict["challenges_overcome"],
            lessons_learned=story_dict["lessons_learned"],
            next_steps=story_dict["next_steps"],
            metadata=story_dict["metadata"],
        )

    def get_story_statistics(self) -> dict[str, Any]:
        """Get statistics about created stories"""
        story_files = list(self.stories_dir.glob("*.json"))

        return {
            "total_stories": len(story_files),
            "stories_dir": str(self.stories_dir),
            "latest_story": max(story_files, key=lambda f: f.stat().st_mtime).name
            if story_files
            else None,
        }


def main():
    """Main function for testing"""
    service = DevlogStorytellingService()

    # Test with a sample devlog
    test_devlog = Path("test_devlog.md")
    with open(test_devlog, "w") as f:
        f.write(
            """# 🤖 Agent Devlog - Agent-7

## 📅 Timestamp
2025-10-02 21:45:00 UTC

## 🎯 Agent Information
- **Agent ID:** Agent-7
- **Role:** Implementation Specialist
- **Status:** completed

## 📝 Action Details
**Action:** Fixed Discord Commander bot functionality

## 📋 Additional Details
Successfully resolved Discord bot startup issues and command handling problems.
"""
        )

    # Create story
    story = service.create_story_from_devlog(test_devlog)
    print(f"Created story: {story.title}")

    # Save story
    story_file = service.save_story(story)
    print(f"Saved story to: {story_file}")

    # Get statistics
    stats = service.get_story_statistics()
    print(f"Story statistics: {stats}")

    # Clean up
    test_devlog.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
