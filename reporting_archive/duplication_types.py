#!/usr/bin/env python3
"""
Duplication Types - Agent Cellphone V2
======================================

Data types and enums for duplication detection system.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Set
from enum import Enum


class DuplicationSeverity(Enum):
    """Duplication severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BlockType(Enum):
    """Code block types"""
    FUNCTION = "function"
    CLASS = "class"
    IMPORT = "import"
    BLOCK = "block"
    METHOD = "method"


@dataclass
class CodeBlock:
    """Represents a code block for analysis"""
    content: str
    hash: str
    file_path: str
    start_line: int
    end_line: int
    block_type: BlockType
    length: int
    tokens: Set[str] = field(default_factory=set)


@dataclass
class DuplicationIssue:
    """Represents a duplication issue found in the codebase"""
    issue_type: str
    severity: DuplicationSeverity
    description: str
    files_involved: List[str]
    line_numbers: List[Tuple[str, int]]
    similarity_score: float
    suggested_action: str
    code_blocks: List[CodeBlock] = field(default_factory=list)


@dataclass
class DuplicationReport:
    """Complete duplication analysis report"""
    timestamp: str
    total_files_analyzed: int
    total_issues_found: int
    issues_by_severity: dict
    summary: str
    recommendations: List[str] = field(default_factory=list)

