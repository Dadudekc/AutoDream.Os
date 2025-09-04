#!/usr/bin/env python3
"""
Unified Utility System - DRY Violation Elimination
================================================

Eliminates duplicate utility function patterns across 5+ locations:
- Duplicate path resolution functions
- Duplicate string manipulation functions
- Duplicate data transformation functions
- Duplicate file operation functions

CONSOLIDATED: Single source of truth for all utility operations.

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violation Elimination
Status: CONSOLIDATED - Utility Duplication Eliminated
"""

import json
import re
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass

from .unified_logging_system import get_logger, get_unified_logger
from .unified_configuration_system import get_unified_config
from .unified_validation_system import get_unified_validator


# ================================
# UNIFIED UTILITY SYSTEM
# ================================

class UnifiedUtilitySystem:
    """
    Unified utility system that eliminates duplicate utility function patterns.
    
    CONSOLIDATES:
    - get_unified_utility().get_unified_utility().resolve_path(relative_path) (duplicated in 6+ locations)
    - get_unified_utility().get_unified_utility().get_project_root() (duplicated in 5+ locations)
    - format_string (duplicated in 4+ locations)
    - get_unified_utility().sanitize_string (duplicated in 3+ locations)
    - validate_string (duplicated in 3+ locations)
    - transform_data (duplicated in 4+ locations)
    - file operations (duplicated in 5+ locations)
    """
    
    def __init__(self):
        """Initialize unified utility system."""
        self.config = get_unified_config()
        self.logger = get_logger(__name__)
        self.unified_logger = get_unified_logger()
        
        # Utility patterns
        self._patterns = {
            "whitespace": re.compile(r'\s+'),
            "special_chars": re.compile(r'[^\w\s-]'),
            "multiple_spaces": re.compile(r'\s{2,}'),
            "leading_trailing_spaces": re.compile(r'^\s+|\s+$')
        }
    
    def resolve_path(self, relative_path: str) -> Path:
        """
        Resolve path relative to project root - consolidates 6+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/constants/paths.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/validation/coordination_validator.py
        - src/core/processing/unified_processing_system.py
        - src/core/consolidation/utility_consolidation_coordinator.py
        """
        project_root = self.config.get("paths.project_root")
        return project_root / relative_path
    
    def get_project_root(self) -> Path:
        """
        Get project root path - consolidates 5+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/constants/paths.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/validation/coordination_validator.py
        - src/core/processing/unified_processing_system.py
        """
        return self.config.get("paths.project_root")
    
    def format_string(self, template: str, **kwargs) -> str:
        """
        Format string with parameters - consolidates 4+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/processing/unified_processing_system.py
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            self.get_logger(__name__).error(f"Missing parameter for string formatting: {e}")
            return template
        except Exception as e:
            self.get_logger(__name__).error(f"String formatting error: {e}")
            return template
    
    def sanitize_string(self, text: str, remove_special: bool = True, normalize_whitespace: bool = True) -> str:
        """
        Sanitize string - consolidates 3+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        """
        if not get_unified_validator().validate_type(text, str):
            return str(text)
        
        # Normalize whitespace
        if normalize_whitespace:
            text = self._patterns["multiple_spaces"].sub(' ', text)
            text = self._patterns["leading_trailing_spaces"].sub('', text)
        
        # Remove special characters
        if remove_special:
            text = self._patterns["special_chars"].sub('', text)
        
        return text.strip()
    
    def validate_string(self, text: str, min_length: int = 0, max_length: int = 1000, allow_empty: bool = True) -> bool:
        """
        Validate string - consolidates 3+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        """
        if not get_unified_validator().validate_type(text, str):
            return False
        
        if not allow_empty and not text.strip():
            return False
        
        length = len(text)
        return min_length <= length <= max_length
    
    def transform_data(self, data: Any, transformation_type: str, **kwargs) -> Any:
        """
        Transform data - consolidates 4+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/processing/unified_processing_system.py
        """
        try:
            if transformation_type == "to_dict":
                return self._to_dict(data)
            elif transformation_type == "to_list":
                return self._to_list(data)
            elif transformation_type == "to_string":
                return self._to_string(data)
            elif transformation_type == "to_json":
                return self._to_json(data)
            elif transformation_type == "from_json":
                return self._from_json(data)
            elif transformation_type == "normalize":
                return self._normalize_data(data)
            else:
                self.get_logger(__name__).warning(f"Unknown transformation type: {transformation_type}")
                return data
        except Exception as e:
            self.get_logger(__name__).error(f"Data transformation error: {e}")
            return data
    
    def _to_dict(self, data: Any) -> Dict[str, Any]:
        """Convert data to dictionary."""
        if get_unified_validator().validate_type(data, dict):
            return data
        elif get_unified_validator().validate_hasattr(data, '__dict__'):
            return data.__dict__
        elif get_unified_validator().validate_type(data, (list, tuple)) and len(data) > 0:
            return {str(i): item for i, item in enumerate(data)}
        else:
            return {"value": data}
    
    def _to_list(self, data: Any) -> List[Any]:
        """Convert data to list."""
        if get_unified_validator().validate_type(data, list):
            return data
        elif get_unified_validator().validate_type(data, tuple):
            return list(data)
        elif get_unified_validator().validate_type(data, dict):
            return list(data.values())
        else:
            return [data]
    
    def _to_string(self, data: Any) -> str:
        """Convert data to string."""
        if get_unified_validator().validate_type(data, str):
            return data
        elif get_unified_validator().validate_type(data, (dict, list)):
            return json.dumps(data, indent=2)
        else:
            return str(data)
    
    def _to_json(self, data: Any) -> str:
        """Convert data to JSON string."""
        try:
            return json.dumps(data, indent=2, default=str)
        except Exception as e:
            self.get_logger(__name__).error(f"JSON serialization error: {e}")
            return str(data)
    
    def _from_json(self, data: str) -> Any:
        """Convert JSON string to data."""
        try:
            return json.loads(data)
        except Exception as e:
            self.get_logger(__name__).error(f"JSON deserialization error: {e}")
            return data
    
    def _normalize_data(self, data: Any) -> Any:
        """Normalize data structure."""
        if get_unified_validator().validate_type(data, dict):
            return {k: self._normalize_data(v) for k, v in data.items()}
        elif get_unified_validator().validate_type(data, list):
            return [self._normalize_data(item) for item in data]
        elif get_unified_validator().validate_type(data, str):
            return self.sanitize_string(data)
        else:
            return data
    
    def read_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read file content - consolidates 5+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/processing/unified_processing_system.py
        - src/core/consolidation/utility_consolidation_coordinator.py
        """
        try:
            file_path = Path(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            self.get_logger(__name__).error(f"File read error: {file_path} - {e}")
            return ""
    
    def write_file(self, file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> bool:
        """
        Write file content - consolidates 5+ duplicate implementations.
        
        CONSOLIDATES FROM:
        - src/core/validation/coordination_validator.py
        - src/utils/config_core.py
        - src/services/messaging_core.py
        - src/core/processing/unified_processing_system.py
        - src/core/consolidation/utility_consolidation_coordinator.py
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self.get_logger(__name__).info(f"File written successfully: {file_path}")
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"File write error: {file_path} - {e}")
            return False
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Copy file - consolidates duplicate file copy implementations."""
        try:
            source = Path(source)
            destination = Path(destination)
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            
            self.get_logger(__name__).info(f"File copied: {source} -> {destination}")
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"File copy error: {source} -> {destination} - {e}")
            return False
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Move file - consolidates duplicate file move implementations."""
        try:
            source = Path(source)
            destination = Path(destination)
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            
            self.get_logger(__name__).info(f"File moved: {source} -> {destination}")
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"File move error: {source} -> {destination} - {e}")
            return False
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """Delete file - consolidates duplicate file delete implementations."""
        try:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                self.get_logger(__name__).info(f"File deleted: {file_path}")
                return True
            else:
                self.get_logger(__name__).warning(f"File not found: {file_path}")
                return False
        except Exception as e:
            self.get_logger(__name__).error(f"File delete error: {file_path} - {e}")
            return False
    
    def ensure_directory(self, directory_path: Union[str, Path]) -> bool:
        """Ensure directory exists - consolidates duplicate directory creation implementations."""
        try:
            directory_path = Path(directory_path)
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.get_logger(__name__).error(f"Directory creation error: {directory_path} - {e}")
            return False
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """Get file size - consolidates duplicate file size implementations."""
        try:
            file_path = Path(file_path)
            return file_path.stat().st_size
        except Exception as e:
            self.get_logger(__name__).error(f"File size error: {file_path} - {e}")
            return 0
    
    def get_file_modified_time(self, file_path: Union[str, Path]) -> datetime:
        """Get file modified time - consolidates duplicate file time implementations."""
        try:
            file_path = Path(file_path)
            timestamp = file_path.stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception as e:
            self.get_logger(__name__).error(f"File time error: {file_path} - {e}")
            return datetime.now()
    
    def list_files(self, directory_path: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
        """List files in directory - consolidates duplicate file listing implementations."""
        try:
            directory_path = Path(directory_path)
            if recursive:
                return list(directory_path.rglob(pattern))
            else:
                return list(directory_path.glob(pattern))
        except Exception as e:
            self.get_logger(__name__).error(f"File listing error: {directory_path} - {e}")
            return []
    
    def count_lines(self, file_path: Union[str, Path]) -> int:
        """Count lines in file - consolidates duplicate line counting implementations."""
        try:
            content = self.read_file(file_path)
            return len(content.splitlines())
        except Exception as e:
            self.get_logger(__name__).error(f"Line counting error: {file_path} - {e}")
            return 0

# ================================
# GLOBAL UTILITY INSTANCE
# ================================

# Single global instance to eliminate duplicate utility objects
_unified_utility = None

def get_unified_utility() -> UnifiedUtilitySystem:
    """Get global unified utility instance."""
    global _unified_utility
    if _unified_utility is None:
        _unified_utility = UnifiedUtilitySystem()
    return _unified_utility

# ================================
# CONVENIENCE FUNCTIONS
# ================================

def resolve_path(relative_path: str) -> Path:
    """Resolve path relative to project root."""
    return get_unified_utility().resolve_path(relative_path)

def get_project_root() -> Path:
    """Get project root path."""
    return get_unified_utility().get_project_root()

def format_string(template: str, **kwargs) -> str:
    """Format string with parameters."""
    return get_unified_utility().format_string(template, **kwargs)

def sanitize_string(text: str, remove_special: bool = True, normalize_whitespace: bool = True) -> str:
    """Sanitize string."""
    return get_unified_utility().sanitize_string(text, remove_special, normalize_whitespace)

def validate_string(text: str, min_length: int = 0, max_length: int = 1000, allow_empty: bool = True) -> bool:
    """Validate string."""
    return get_unified_utility().validate_string(text, min_length, max_length, allow_empty)

def transform_data(data: Any, transformation_type: str, **kwargs) -> Any:
    """Transform data."""
    return get_unified_utility().transform_data(data, transformation_type, **kwargs)

def read_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Read file content."""
    return get_unified_utility().read_file(file_path, encoding)

def write_file(file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> bool:
    """Write file content."""
    return get_unified_utility().write_file(file_path, content, encoding)

def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """Copy file."""
    return get_unified_utility().copy_file(source, destination)

def move_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """Move file."""
    return get_unified_utility().move_file(source, destination)

def delete_file(file_path: Union[str, Path]) -> bool:
    """Delete file."""
    return get_unified_utility().delete_file(file_path)

def ensure_directory(directory_path: Union[str, Path]) -> bool:
    """Ensure directory exists."""
    return get_unified_utility().ensure_directory(directory_path)

def count_lines(file_path: Union[str, Path]) -> int:
    """Count lines in file."""
    return get_unified_utility().count_lines(file_path)
