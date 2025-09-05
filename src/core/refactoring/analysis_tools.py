#!/usr/bin/env python3
"""
Architecture Analysis Tools - KISS Simplified
=============================================

Simplified architecture analysis tools for V2 compliance.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined analysis tools.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import os
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class ArchitecturePattern:
    """Represents an identified architecture pattern - simplified."""
    name: str
    pattern_type: str
    files: List[str]
    confidence: float
    description: str


@dataclass
class FileAnalysis:
    """Analysis results for a single file - simplified."""
    file_path: str
    line_count: int
    classes: List[str]
    functions: List[str]
    imports: List[str]
    complexity_score: float
    v2_compliance: bool


@dataclass
class DuplicateFile:
    """Represents duplicate file information - simplified."""
    original_file: str
    duplicate_files: List[str]
    similarity_score: float
    duplicate_type: str


def analyze_file_for_extraction(file_path: str) -> FileAnalysis:
    """Analyze file for extraction - simplified."""
    try:
        if not os.path.exists(file_path):
            return FileAnalysis(
                file_path=file_path,
                line_count=0,
                classes=[],
                functions=[],
                imports=[],
                complexity_score=0.0,
                v2_compliance=False
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Basic analysis
        line_count = len(lines)
        classes = _extract_classes(content)
        functions = _extract_functions(content)
        imports = _extract_imports(content)
        complexity_score = _calculate_complexity(content)
        v2_compliance = line_count < 300

        return FileAnalysis(
            file_path=file_path,
            line_count=line_count,
            classes=classes,
            functions=functions,
            imports=imports,
            complexity_score=complexity_score,
            v2_compliance=v2_compliance
        )

    except Exception as e:
        logger.error(f"Error analyzing file {file_path}: {e}")
        return FileAnalysis(
            file_path=file_path,
            line_count=0,
            classes=[],
            functions=[],
            imports=[],
            complexity_score=0.0,
            v2_compliance=False
        )


def _extract_classes(content: str) -> List[str]:
    """Extract class names - simplified."""
    try:
        classes = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('class ') and ':' in line:
                class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                classes.append(class_name)
        return classes
    except Exception:
        return []


def _extract_functions(content: str) -> List[str]:
    """Extract function names - simplified."""
    try:
        functions = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('def ') and ':' in line:
                func_name = line.split('def ')[1].split('(')[0].strip()
                functions.append(func_name)
        return functions
    except Exception:
        return []


def _extract_imports(content: str) -> List[str]:
    """Extract import statements - simplified."""
    try:
        imports = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('import ', 'from ')):
                imports.append(line)
        return imports
    except Exception:
        return []


def _calculate_complexity(content: str) -> float:
    """Calculate complexity score - simplified."""
    try:
        lines = content.split('\n')
        complexity = 0.0
        
        for line in lines:
            line = line.strip()
            if line.startswith(('if ', 'for ', 'while ', 'try:', 'except', 'with ')):
                complexity += 1.0
            elif line.startswith(('def ', 'class ')):
                complexity += 0.5
        
        return min(complexity, 10.0)  # Cap at 10
    except Exception:
        return 0.0


def find_duplicate_files(directory: str) -> List[DuplicateFile]:
    """Find duplicate files - simplified."""
    try:
        file_hashes = {}
        duplicates = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_hash = _calculate_file_hash(file_path)
                    
                    if file_hash in file_hashes:
                        # Found duplicate
                        original = file_hashes[file_hash]
                        duplicate = DuplicateFile(
                            original_file=original,
                            duplicate_files=[file_path],
                            similarity_score=1.0,
                            duplicate_type="exact"
                        )
                        duplicates.append(duplicate)
                    else:
                        file_hashes[file_hash] = file_path
        
        return duplicates
    except Exception as e:
        logger.error(f"Error finding duplicate files: {e}")
        return []


def _calculate_file_hash(file_path: str) -> str:
    """Calculate file hash - simplified."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""


def detect_architecture_patterns(directory: str) -> List[ArchitecturePattern]:
    """Detect architecture patterns - simplified."""
    try:
        patterns = []
        
        # Basic pattern detection
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    analysis = analyze_file_for_extraction(file_path)
                    
                    # Detect patterns based on file structure
                    if analysis.line_count > 300:
                        pattern = ArchitecturePattern(
                            name="Large File Pattern",
                            pattern_type="violation",
                            files=[file_path],
                            confidence=0.9,
                            description="File exceeds V2 compliance threshold"
                        )
                        patterns.append(pattern)
                    
                    if len(analysis.classes) > 5:
                        pattern = ArchitecturePattern(
                            name="Multiple Classes Pattern",
                            pattern_type="complexity",
                            files=[file_path],
                            confidence=0.7,
                            description="File contains multiple classes"
                        )
                        patterns.append(pattern)
        
        return patterns
    except Exception as e:
        logger.error(f"Error detecting architecture patterns: {e}")
        return []


def generate_refactoring_recommendations(analysis: FileAnalysis) -> List[str]:
    """Generate refactoring recommendations - simplified."""
    recommendations = []
    
    try:
        if not analysis.v2_compliance:
            recommendations.append(f"File {analysis.file_path} exceeds 300 lines - consider splitting")
        
        if analysis.complexity_score > 5.0:
            recommendations.append(f"File {analysis.file_path} has high complexity - consider refactoring")
        
        if len(analysis.classes) > 3:
            recommendations.append(f"File {analysis.file_path} has many classes - consider separation")
        
        if len(analysis.functions) > 10:
            recommendations.append(f"File {analysis.file_path} has many functions - consider grouping")
        
        return recommendations
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return []


def analyze_directory_structure(directory: str) -> Dict[str, Any]:
    """Analyze directory structure - simplified."""
    try:
        stats = {
            "total_files": 0,
            "python_files": 0,
            "v2_compliant_files": 0,
            "large_files": 0,
            "total_lines": 0
        }
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                stats["total_files"] += 1
                if file.endswith('.py'):
                    stats["python_files"] += 1
                    file_path = os.path.join(root, file)
                    analysis = analyze_file_for_extraction(file_path)
                    stats["total_lines"] += analysis.line_count
                    
                    if analysis.v2_compliance:
                        stats["v2_compliant_files"] += 1
                    else:
                        stats["large_files"] += 1
        
        return stats
    except Exception as e:
        logger.error(f"Error analyzing directory structure: {e}")
        return {"error": str(e)}