#!/usr/bin/env python3
"""
Logic Pattern Scanner - Logic Consolidation System
================================================

Scans the codebase for duplicate logic patterns using AST parsing.

Author: Agent-8 (Integration Enhancement Optimization Manager)
License: MIT
"""

import os
import logging
import ast
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

from consolidation_models import LogicPattern

logger = logging.getLogger(__name__)


class LogicPatternScanner:
    """Scans the codebase for duplicate logic patterns."""

    def __init__(self):
        self.logic_patterns = {
            'validate': [],
            'process': [],
            'initialize': [],
            'cleanup': [],
            'consolidate': [],
            'generate': [],
            'scan': [],
            'create': []
        }
        self.total_duplicates_found = 0

    def scan_for_logic_patterns(self) -> Dict[str, List[LogicPattern]]:
        """Scan the codebase for duplicate logic patterns."""
        logger.info("🔍 Scanning for duplicate logic patterns...")

        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    
                    # Skip certain directories
                    if any(skip_dir in file_path for skip_dir in ['__pycache__', 'venv', 'node_modules', '.git']):
                        continue

                    try:
                        logic_patterns = self._extract_logic_patterns(file_path)
                        for pattern in logic_patterns:
                            self.logic_patterns[pattern.function_type].append(pattern)
                    except Exception as e:
                        logger.warning(f"Could not analyze {file_path}: {e}")

        # Count duplicates
        for pattern_type, patterns in self.logic_patterns.items():
            if len(patterns) > 1:
                self.total_duplicates_found += len(patterns) - 1
                logger.info(f"Found {len(patterns)} {pattern_type} logic patterns")

        return self.logic_patterns

    def _extract_logic_patterns(self, file_path: str) -> List[LogicPattern]:
        """Extract logic patterns from a Python file using AST parsing."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            patterns = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if this is a logic pattern function
                    function_name = node.name.lower()
                    
                    for pattern_type in self.logic_patterns.keys():
                        if pattern_type in function_name:
                            # Extract function signature
                            args = [arg.arg for arg in node.args.args]
                            signature = f"{function_name}({', '.join(args)})"
                            
                            # Extract docstring
                            docstring = ast.get_docstring(node) or ""
                            
                            # Calculate complexity (simple line count)
                            complexity = len(ast.unparse(node).split('\n'))
                            
                            pattern = LogicPattern(
                                name=node.name,
                                file_path=file_path,
                                line_number=node.lineno,
                                function_type=pattern_type,
                                signature=signature,
                                docstring=docstring,
                                complexity=complexity
                            )
                            patterns.append(pattern)
                            break

            return patterns
        except Exception as e:
            logger.warning(f"Error parsing {file_path}: {e}")
            return []

    def get_duplicate_logic(self) -> Dict[str, List[List[LogicPattern]]]:
        """Identify duplicate logic patterns based on function signatures."""
        logger.info("🔍 Identifying duplicate logic patterns...")
        
        duplicate_logic = defaultdict(list)
        
        for pattern_type, patterns in self.logic_patterns.items():
            if len(patterns) < 2:
                continue

            # Group patterns by signature similarity
            signature_groups = defaultdict(list)
            for pattern in patterns:
                # Normalize signature for comparison
                normalized_sig = self._normalize_signature(pattern.signature)
                signature_groups[normalized_sig].append(pattern)

            # Find groups with multiple patterns (duplicates)
            for signature, group in signature_groups.items():
                if len(group) > 1:
                    duplicate_logic[pattern_type].append(group)
                    logger.info(f"Found {len(group)} duplicate {pattern_type} patterns with signature: {signature}")

        return duplicate_logic

    def _normalize_signature(self, signature: str) -> str:
        """Normalize function signature for comparison."""
        # Remove function name and keep only parameter structure
        import re
        normalized = re.sub(r'^[a-zA-Z_][a-zA-Z0-9_]*\(', 'func(', signature)
        return normalized
