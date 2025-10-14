#!/usr/bin/env python3
"""
Fallback Regex Parser
=====================

Safety net parser - simple keyword detection.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import re

from ..dedupe import extract_tags
from ..schemas import ParsedTask


class FallbackRegexParser:
    """Fallback parser using simple regex patterns."""

    # Patterns for task detection
    TASK_PATTERNS = [
        re.compile(r"^\s*(?:todo|task)\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*(?:fix|bug)\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*(?:feature|add)\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\s*(?:implement|create)\s*[:\-]?\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    ]

    @staticmethod
    def parse(content: str) -> ParsedTask | None:
        """
        Parse using fallback regex patterns.

        This is the safety net - should almost always match something.

        Args:
            content: Message content

        Returns:
            ParsedTask or None (rarely None)
        """
        # Try each pattern
        for pattern in FallbackRegexParser.TASK_PATTERNS:
            match = pattern.search(content)
            if match:
                title = match.group(1).strip()

                # Limit title length
                if len(title) > 200:
                    title = title[:200] + "..."

                # Extract any remaining text as description
                description = content.replace(match.group(0), "").strip()
                if len(description) > 4000:
                    description = description[:4000] + "..."

                # Extract tags
                tags = extract_tags(content)

                return ParsedTask(
                    title=title,
                    description=description,
                    tags=tags,
                )

        # Ultimate fallback: use first line as title
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if lines:
            title = lines[0]
            if len(title) > 200:
                title = title[:200] + "..."

            description = "\n".join(lines[1:]) if len(lines) > 1 else ""
            if len(description) > 4000:
                description = description[:4000] + "..."

            tags = extract_tags(content)

            return ParsedTask(
                title=title,
                description=description,
                tags=tags,
            )

        return None
