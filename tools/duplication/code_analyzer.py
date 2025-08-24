#!/usr/bin/env python3
"""
Code Analyzer - Agent Cellphone V2
==================================

Code analysis and block extraction for duplication detection.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import ast
import hashlib
import logging
from pathlib import Path
from typing import List, Set
from .duplication_types import CodeBlock, BlockType


class CodeAnalyzer:
    """Analyzes Python code and extracts code blocks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_code_blocks(self, file_path: Path) -> List[CodeBlock]:
        """Extract code blocks from a Python file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            blocks = []
            
            # Extract functions
            blocks.extend(self._extract_functions(content, file_path))
            
            # Extract classes
            blocks.extend(self._extract_classes(content, file_path))
            
            # Extract imports
            blocks.extend(self._extract_imports(content, file_path))
            
            # Extract code blocks
            blocks.extend(self._extract_general_blocks(content, file_path))
            
            self.logger.info(f"Extracted {len(blocks)} code blocks from {file_path}")
            return blocks
            
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return []
    
    def _extract_functions(self, content: str, file_path: Path) -> List[CodeBlock]:
        """Extract function definitions"""
        blocks = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    block = CodeBlock(
                        content=ast.unparse(node),
                        hash=self._hash_content(ast.unparse(node)),
                        file_path=str(file_path),
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        block_type=BlockType.FUNCTION,
                        length=node.end_lineno - node.lineno + 1 if node.end_lineno else 1,
                        tokens=self._extract_tokens(ast.unparse(node))
                    )
                    blocks.append(block)
        except Exception as e:
            self.logger.warning(f"Error extracting functions from {file_path}: {e}")
        
        return blocks
    
    def _extract_classes(self, content: str, file_path: Path) -> List[CodeBlock]:
        """Extract class definitions"""
        blocks = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    block = CodeBlock(
                        content=ast.unparse(node),
                        hash=self._hash_content(ast.unparse(node)),
                        file_path=str(file_path),
                        start_line=node.lineno,
                        end_line=node.end_lineno or node.lineno,
                        block_type=BlockType.CLASS,
                        length=node.end_lineno - node.lineno + 1 if node.end_lineno else 1,
                        tokens=self._extract_tokens(ast.unparse(node))
                    )
                    blocks.append(block)
        except Exception as e:
            self.logger.warning(f"Error extracting classes from {file_path}: {e}")
        
        return blocks
    
    def _extract_imports(self, content: str, file_path: Path) -> List[CodeBlock]:
        """Extract import statements"""
        blocks = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    block = CodeBlock(
                        content=ast.unparse(node),
                        hash=self._hash_content(ast.unparse(node)),
                        file_path=str(file_path),
                        start_line=node.lineno,
                        end_line=node.lineno,
                        block_type=BlockType.IMPORT,
                        length=1,
                        tokens=self._extract_tokens(ast.unparse(node))
                    )
                    blocks.append(block)
        except Exception as e:
            self.logger.warning(f"Error extracting imports from {file_path}: {e}")
        
        return blocks
    
    def _extract_general_blocks(self, content: str, file_path: Path) -> List[CodeBlock]:
        """Extract general code blocks"""
        blocks = []
        lines = content.split('\n')
        
        # Extract blocks of 5+ lines with similar structure
        for i in range(len(lines) - 4):
            block_lines = lines[i:i+5]
            block_content = '\n'.join(block_lines)
            
            if len(block_content.strip()) > 20:  # Minimum meaningful content
                block = CodeBlock(
                    content=block_content,
                    hash=self._hash_content(block_content),
                    file_path=str(file_path),
                    start_line=i + 1,
                    end_line=i + 5,
                    block_type=BlockType.BLOCK,
                    length=5,
                    tokens=self._extract_tokens(block_content)
                )
                blocks.append(block)
        
        return blocks
    
    def _hash_content(self, content: str) -> str:
        """Generate hash for content"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _extract_tokens(self, content: str) -> Set[str]:
        """Extract meaningful tokens from content"""
        # Simple tokenization - split on whitespace and punctuation
        import re
        tokens = re.findall(r'\b\w+\b', content.lower())
        return set(tokens)
