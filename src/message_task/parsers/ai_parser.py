#!/usr/bin/env python3
"""
AI-Powered Message Parser
=========================

Flexible LLM-based parser for natural language task descriptions.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import re

from ..dedupe import extract_tags
from ..schemas import ParsedTask


class AIParser:
    """AI-powered flexible parser for natural language."""

    # Confidence threshold for accepting AI parse
    MIN_CONFIDENCE = 0.6

    @staticmethod
    def parse(content: str) -> ParsedTask | None:
        """
        Parse message using AI/heuristics.

        This is a lightweight implementation. Can be enhanced with actual LLM.

        Args:
            content: Message content

        Returns:
            ParsedTask or None if low confidence
        """
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        if not lines:
            return None

        # Heuristic: First line is likely the title
        title = lines[0]

        # Limit title length
        if len(title) > 200:
            title = title[:200] + "..."

        # Remaining lines form description
        description = "\n".join(lines[1:]) if len(lines) > 1 else ""
        if len(description) > 4000:
            description = description[:4000] + "..."

        # Try to extract priority from content
        priority = AIParser._extract_priority(content)

        # Try to extract assignee
        assignee = AIParser._extract_assignee(content)

        # Extract tags
        tags = extract_tags(content)

        # Confidence check: must have meaningful title
        if len(title) < 3 or not any(c.isalnum() for c in title):
            return None

        return ParsedTask(
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            tags=tags,
        )

    @staticmethod
    def _extract_priority(content: str) -> str:
        """Extract priority from content using patterns."""
        content_lower = content.lower()

        # Priority indicators
        if any(word in content_lower for word in ["critical", "urgent", "asap", "emergency"]):
            return "P0"
        if any(word in content_lower for word in ["high", "important", "soon"]):
            return "P1"
        if any(word in content_lower for word in ["medium", "normal"]):
            return "P2"
        if any(word in content_lower for word in ["low", "whenever", "nice to have"]):
            return "P3"

        # Default
        return "P2"

    @staticmethod
    def _extract_assignee(content: str) -> str | None:
        """Extract assignee from content using patterns."""
        # Look for @mentions or "assign to X" patterns
        mention_match = re.search(r"@(Agent-\d+|[\w\-\.]+)", content, re.IGNORECASE)
        if mention_match:
            return mention_match.group(1)

        assign_match = re.search(
            r"(?:assign(?:ed)?\s+to|for)\s+(Agent-\d+|[\w\-\.]+)", content, re.IGNORECASE
        )
        if assign_match:
            return assign_match.group(1)

        return None
