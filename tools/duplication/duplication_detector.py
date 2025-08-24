#!/usr/bin/env python3
"""
Duplication Detector - Agent Cellphone V2
=========================================

Main orchestrator for duplication detection system.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import difflib

from .duplication_types import DuplicationIssue, DuplicationSeverity, CodeBlock
from .code_analyzer import CodeAnalyzer


class DuplicationDetector:
    """Main duplication detection orchestrator"""
    
    def __init__(self, min_similarity: float = 0.8, min_block_size: int = 5):
        self.min_similarity = min_similarity
        self.min_block_size = min_block_size
        self.analyzer = CodeAnalyzer()
        self.logger = logging.getLogger(__name__)
        
        self.issues: List[DuplicationIssue] = []
        self.code_blocks: List[CodeBlock] = []
        self.file_hashes: Dict[str, str] = {}
    
    def analyze_codebase(self, root_path: str) -> List[DuplicationIssue]:
        """Analyze entire codebase for duplication issues"""
        self.logger.info(f"Analyzing codebase at: {root_path}")
        
        # Find all Python files
        python_files = list(Path(root_path).rglob("*.py"))
        self.logger.info(f"Found {len(python_files)} Python files")
        
        # Extract code blocks from all files
        for file_path in python_files:
            blocks = self.analyzer.extract_code_blocks(file_path)
            self.code_blocks.extend(blocks)
        
        # Detect various types of duplication
        self._detect_exact_duplicates()
        self._detect_similar_structures()
        self._detect_duplicate_imports()
        self._detect_backup_files()
        self._detect_repeated_patterns()
        
        self.logger.info(f"Found {len(self.issues)} duplication issues")
        return self.issues
    
    def _detect_exact_duplicates(self):
        """Detect exact duplicate code blocks"""
        hash_groups = defaultdict(list)
        
        for block in self.code_blocks:
            hash_groups[block.hash].append(block)
        
        for hash_val, blocks in hash_groups.items():
            if len(blocks) > 1 and blocks[0].length >= self.min_block_size:
                issue = DuplicationIssue(
                    issue_type="exact_duplicate",
                    severity=DuplicationSeverity.HIGH,
                    description=f"Exact duplicate of {blocks[0].length} lines",
                    files_involved=[b.file_path for b in blocks],
                    line_numbers=[(b.file_path, b.start_line) for b in blocks],
                    similarity_score=1.0,
                    suggested_action="Consider extracting to shared utility function",
                    code_blocks=blocks
                )
                self.issues.append(issue)
    
    def _detect_similar_structures(self):
        """Detect similar code structures"""
        for i, block1 in enumerate(self.code_blocks):
            for block2 in self.code_blocks[i+1:]:
                if (block1.block_type == block2.block_type and 
                    block1.length >= self.min_block_size and
                    block1.file_path != block2.file_path):
                    
                    similarity = self._calculate_similarity(block1, block2)
                    if similarity >= self.min_similarity:
                        issue = DuplicationIssue(
                            issue_type="similar_structure",
                            severity=DuplicationSeverity.MEDIUM,
                            description=f"Similar {block1.block_type.value} structure",
                            files_involved=[block1.file_path, block2.file_path],
                            line_numbers=[(block1.file_path, block1.start_line),
                                        (block2.file_path, block2.start_line)],
                            similarity_score=similarity,
                            suggested_action="Consider creating base class or template",
                            code_blocks=[block1, block2]
                        )
                        self.issues.append(issue)
    
    def _detect_duplicate_imports(self):
        """Detect duplicate import statements"""
        import_blocks = [b for b in self.code_blocks if b.block_type.value == "import"]
        import_groups = defaultdict(list)
        
        for block in import_blocks:
            import_groups[block.content.strip()].append(block)
        
        for import_content, blocks in import_groups.items():
            if len(blocks) > 1:
                issue = DuplicationIssue(
                    issue_type="duplicate_import",
                    severity=DuplicationSeverity.LOW,
                    description="Duplicate import statement",
                    files_involved=[b.file_path for b in blocks],
                    line_numbers=[(b.file_path, b.start_line) for b in blocks],
                    similarity_score=1.0,
                    suggested_action="Consolidate imports in shared module",
                    code_blocks=blocks
                )
                self.issues.append(issue)
    
    def _detect_backup_files(self):
        """Detect backup and temporary files"""
        backup_patterns = ['.bak', '.backup', '.tmp', '.old', '~']
        
        for block in self.code_blocks:
            file_path = Path(block.file_path)
            if any(pattern in file_path.name for pattern in backup_patterns):
                issue = DuplicationIssue(
                    issue_type="backup_file",
                    severity=DuplicationSeverity.LOW,
                    description="Backup or temporary file detected",
                    files_involved=[block.file_path],
                    line_numbers=[(block.file_path, block.start_line)],
                    similarity_score=1.0,
                    suggested_action="Remove backup file and use version control",
                    code_blocks=[block]
                )
                self.issues.append(issue)
    
    def _detect_repeated_patterns(self):
        """Detect repeated code patterns"""
        pattern_groups = defaultdict(list)
        
        for block in self.code_blocks:
            if block.length >= 10:  # Look for longer patterns
                pattern_key = self._extract_pattern_key(block.content)
                pattern_groups[pattern_key].append(block)
        
        for pattern_key, blocks in pattern_groups.items():
            if len(blocks) > 2:  # Multiple instances of same pattern
                issue = DuplicationIssue(
                    issue_type="repeated_pattern",
                    severity=DuplicationSeverity.MEDIUM,
                    description="Repeated code pattern detected",
                    files_involved=[b.file_path for b in blocks],
                    line_numbers=[(b.file_path, b.start_line) for b in blocks],
                    similarity_score=0.8,
                    suggested_action="Extract pattern to utility function or class",
                    code_blocks=blocks
                )
                self.issues.append(issue)
    
    def _calculate_similarity(self, block1: CodeBlock, block2: CodeBlock) -> float:
        """Calculate similarity between two code blocks"""
        return difflib.SequenceMatcher(None, block1.content, block2.content).ratio()
    
    def _extract_pattern_key(self, content: str) -> str:
        """Extract pattern key for grouping similar patterns"""
        # Simple pattern extraction - normalize whitespace and common variables
        import re
        normalized = re.sub(r'\s+', ' ', content.strip())
        normalized = re.sub(r'\b\w+\b', 'VAR', normalized)
        return normalized[:100]  # First 100 chars as pattern key
