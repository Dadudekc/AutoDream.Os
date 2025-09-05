#!/usr/bin/env python3
"""
Unified Data Processing System - V2 Compliance Module
===================================================

Centralized data processing utilities for the messaging system.

V2 Compliance: < 300 lines, single responsibility, data processing.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def read_json(file_path: str) -> Dict[str, Any]:
    """
    Read JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary containing JSON data or empty dict on error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {}
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    except Exception:
        return {}


def write_json(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Write data to JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception:
        return False


def ensure_directory(dir_path: str) -> bool:
    """
    Ensure directory exists.
    
    Args:
        dir_path: Directory path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def resolve_path(path: str) -> Path:
    """
    Resolve path to absolute path.
    
    Args:
        path: Path to resolve
        
    Returns:
        Resolved Path object
    """
    return Path(path).resolve()


def write_file(file_path: str, content: str) -> bool:
    """
    Write content to file with error handling.
    
    Args:
        file_path: Path to file
        content: Content to write
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    except Exception:
        return False