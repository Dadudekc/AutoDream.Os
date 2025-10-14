#!/usr/bin/env python3
"""
Structured Message Parser
=========================

Strict format parser for structured task messages.

Format:
    TASK: <title>
    DESC: <description>
    PRIORITY: <P0-P3>
    ASSIGNEE: <agent-id>

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import re

from ..dedupe import extract_tags, normalize_priority
from ..schemas import ParsedTask


class StructuredParser:
    """Parser for structured task messages."""

    # Regex pattern for structured format
    PATTERN = re.compile(
        r"""
        ^\s*TASK:\s*(?P<title>.+?)\s*$
        (?:.*?^\s*DESC(?:RIPTION)?:\s*(?P<desc>.+?)\s*$)?
        (?:.*?^\s*PRIORITY:\s*(?P<prio>\w+)\s*$)?
        (?:.*?^\s*ASSIGNEE:\s*(?P<assignee>[\w\-\.]+)\s*$)?
        (?:.*?^\s*TAGS:\s*(?P<tags>.+?)\s*$)?
        (?:.*?^\s*PARENT:\s*(?P<parent>[\w\-]+)\s*$)?
        """,
        re.MULTILINE | re.DOTALL | re.VERBOSE | re.IGNORECASE,
    )

    @staticmethod
    def parse(content: str) -> ParsedTask | None:
        """
        Parse structured message format.

        Args:
            content: Message content

        Returns:
            ParsedTask or None if format not matched
        """
        match = StructuredParser.PATTERN.search(content)
        if not match:
            return None

        groups = match.groupdict()

        # Extract title (required)
        title = (groups.get("title") or "").strip()
        if not title:
            return None

        # Extract description
        description = (groups.get("desc") or "").strip()

        # Extract and normalize priority
        priority_raw = (groups.get("prio") or "P3").strip()
        priority = normalize_priority(priority_raw)

        # Extract assignee
        assignee = groups.get("assignee")
        if assignee:
            assignee = assignee.strip()

        # Extract tags
        tags_raw = groups.get("tags") or ""
        if tags_raw:
            # Parse comma-separated or space-separated tags
            tags = [t.strip().lstrip("#") for t in re.split(r"[,\s]+", tags_raw) if t.strip()]
        else:
            # Extract hashtags from title and description
            tags = extract_tags(title + " " + description)

        # Extract parent task ID
        parent_id = groups.get("parent")
        if parent_id:
            parent_id = parent_id.strip()

        return ParsedTask(
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            tags=tags,
            parent_id=parent_id,
        )
