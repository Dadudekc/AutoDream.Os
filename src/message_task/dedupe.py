#!/usr/bin/env python3
"""
Task Deduplication
==================

Fingerprint-based task deduplication for idempotency.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import hashlib
import json
from typing import Any


def task_fingerprint(parsed_task_dict: dict[str, Any]) -> str:
    """
    Generate unique fingerprint for task deduplication.

    Uses SHA-1 hash of normalized task fields to detect duplicates.

    Args:
        parsed_task_dict: Dictionary with task fields

    Returns:
        40-character hex fingerprint
    """
    # Extract only deduplication-relevant fields
    dedup_keys = {
        "title": parsed_task_dict.get("title", ""),
        "description": parsed_task_dict.get("description", ""),
        "priority": parsed_task_dict.get("priority", "P3"),
        "assignee": parsed_task_dict.get("assignee"),
        "parent_id": parsed_task_dict.get("parent_id"),
        "due_timestamp": parsed_task_dict.get("due_timestamp"),
        "tags": sorted(parsed_task_dict.get("tags", [])),  # Normalize order
    }

    # Serialize to stable JSON
    blob = json.dumps(dedup_keys, sort_keys=True, ensure_ascii=False)

    # Hash with SHA-1 (sufficient for deduplication)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def normalize_priority(priority: str) -> str:
    """
    Normalize priority string to P0-P3 format.

    Args:
        priority: Raw priority string

    Returns:
        Normalized priority (P0, P1, P2, or P3)
    """
    priority = priority.upper().strip()

    # Map common variants
    priority_map = {
        "CRITICAL": "P0",
        "URGENT": "P0",
        "HIGH": "P1",
        "MEDIUM": "P2",
        "NORMAL": "P2",
        "LOW": "P3",
        "P0": "P0",
        "P1": "P1",
        "P2": "P2",
        "P3": "P3",
    }

    return priority_map.get(priority, "P3")


def extract_tags(text: str) -> list[str]:
    """
    Extract tags from text.

    Looks for #hashtags in text.

    Args:
        text: Text to extract tags from

    Returns:
        List of unique tags (without #)
    """
    import re

    tags = re.findall(r"#(\w+)", text)
    return sorted(set(tag.lower() for tag in tags))
