#!/usr/bin/env python3
"""
Duplication Types - Agent Cellphone V2
=====================================

Shared data structures for the duplication detection system.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Tuple


class BlockType(Enum):
    """Types of code blocks that can be analyzed."""

    FUNCTION = "function"
    CLASS = "class"
    IMPORT = "import"
    BLOCK = "block"


@dataclass
class CodeBlock:
    """Represents a block of code extracted for analysis."""

    content: str
    hash: str
    file_path: str
    start_line: int
    end_line: int
    block_type: BlockType
    length: int
    tokens: Set[str] = field(default_factory=set)


class DuplicationSeverity(Enum):
    """Severity levels for duplication issues."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class DuplicationIssue:
    """Represents a detected duplication issue."""

    issue_type: str
    severity: DuplicationSeverity
    description: str
    files_involved: List[str]
    line_numbers: List[Tuple[str, int]]
    similarity_score: float
    suggested_action: str
    code_blocks: List[CodeBlock] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert issue to a serializable dictionary."""
        return {
            "issue_type": self.issue_type,
            "severity": self.severity.value,
            "description": self.description,
            "files_involved": self.files_involved,
            "line_numbers": self.line_numbers,
            "similarity_score": self.similarity_score,
            "suggested_action": self.suggested_action,
            "code_blocks": [
                {
                    "file_path": block.file_path,
                    "start_line": block.start_line,
                    "end_line": block.end_line,
                    "block_type": block.block_type.value,
                    "length": block.length,
                }
                for block in self.code_blocks
            ],
        }
