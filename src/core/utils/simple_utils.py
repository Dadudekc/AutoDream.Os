#!/usr/bin/env python3
"""
Simple Utils - KISS Compliant
=============================

Simple utility functions following KISS principles.
No overengineering, no complex patterns, just simple utilities.

Author: Agent-8 - SSOT & System Integration Specialist
Mission: KISS Simplification
"""

import os
from datetime import datetime


def read_file(filepath):
    """Read file content."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def write_file(filepath, content):

EXAMPLE USAGE:
==============

# Import the core component
from src.core.utils.simple_utils import Simple_Utils

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Simple_Utils(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

    """Write content to file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False


def list_files(directory, extension=None):
    """List files in directory."""
    try:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if extension is None or item.endswith(extension):
                    files.append(item_path)
        return files
    except Exception:
        return []


def get_timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_string(template, **kwargs):
    """Format string with variables."""
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def is_valid_path(path):
    """Check if path is valid."""
    try:
        return os.path.exists(path)
    except Exception:
        return False


def create_directory(path):
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False


def delete_file(filepath):
    """Delete file."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception:
        return False


def get_file_size(filepath):
    """Get file size in bytes."""
    try:
        return os.path.getsize(filepath)
    except Exception:
        return 0


def copy_file(source, destination):
    """Copy file from source to destination."""
    try:
        import shutil

        shutil.copy2(source, destination)
        return True
    except Exception:
        return False
