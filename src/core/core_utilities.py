#!/usr/bin/env python3
"""
Core Utilities - Consolidated Utility Functions
==============================================

Consolidated utility functions providing unified utility functionality for:
- File operations
- Data processing
- String manipulation
- Date/time operations
- Mathematical operations

This module consolidates utility functions for better organization and reduced complexity.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ============================================================================
# FILE OPERATIONS
# ============================================================================

def read_file(file_path: str | Path, encoding: str = "utf-8") -> str | None:
    """Read file content."""
    try:
        with open(file_path, encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to read file {file_path}: {e}")
        return None


def write_file(file_path: str | Path, content: str, encoding: str = "utf-8") -> bool:
    """Write content to file."""
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Failed to write file {file_path}: {e}")
        return False


def copy_file(src: str | Path, dst: str | Path) -> bool:
    """Copy file from source to destination."""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        logging.error(f"Failed to copy file {src} to {dst}: {e}")
        return False


def move_file(src: str | Path, dst: str | Path) -> bool:
    """Move file from source to destination."""
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        logging.error(f"Failed to move file {src} to {dst}: {e}")
        return False


def delete_file(file_path: str | Path) -> bool:
    """Delete file."""
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        logging.error(f"Failed to delete file {file_path}: {e}")
        return False


def list_files(directory: str | Path, pattern: str = "*") -> list[Path]:
    """List files in directory matching pattern."""
    try:
        directory = Path(directory)
        if not directory.exists():
            return []

        return list(directory.glob(pattern))
    except Exception as e:
        logging.error(f"Failed to list files in {directory}: {e}")
        return []


def get_file_size(file_path: str | Path) -> int:
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logging.error(f"Failed to get file size for {file_path}: {e}")
        return 0


def get_file_hash(file_path: str | Path, algorithm: str = "md5") -> str | None:
    """Get file hash."""
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logging.error(f"Failed to get file hash for {file_path}: {e}")
        return None


def create_directory(directory: str | Path) -> bool:
    """Create directory."""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {directory}: {e}")
        return False


def directory_exists(directory: str | Path) -> bool:
    """Check if directory exists."""
    return Path(directory).exists() and Path(directory).is_dir()


def file_exists(file_path: str | Path) -> bool:
    """Check if file exists."""
    return Path(file_path).exists() and Path(file_path).is_file()


# ============================================================================
# DATA PROCESSING
# ============================================================================

def to_json(data: Any, indent: int = 2) -> str | None:
    """Convert data to JSON string."""
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False, default=str)
    except Exception as e:
        logging.error(f"Failed to convert to JSON: {e}")
        return None


def from_json(json_str: str) -> Any | None:
    """Parse JSON string to data."""
    try:
        return json.loads(json_str)
    except Exception as e:
        logging.error(f"Failed to parse JSON: {e}")
        return None


def save_json(data: Any, file_path: str | Path, indent: int = 2) -> bool:
    """Save data as JSON file."""
    try:
        json_str = to_json(data, indent)
        if json_str:
            return write_file(file_path, json_str)
        return False
    except Exception as e:
        logging.error(f"Failed to save JSON to {file_path}: {e}")
        return False


def load_json(file_path: str | Path) -> Any | None:
    """Load data from JSON file."""
    try:
        content = read_file(file_path)
        if content:
            return from_json(content)
        return None
    except Exception as e:
        logging.error(f"Failed to load JSON from {file_path}: {e}")
        return None


def merge_dicts(*dicts: dict[str, Any]) -> dict[str, Any]:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def flatten_dict(data: dict[str, Any], separator: str = ".") -> dict[str, Any]:
    """Flatten nested dictionary."""
    def _flatten(obj, parent_key="", sep="."):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.extend(_flatten(v, new_key, sep).items())
        else:
            items.append((parent_key, obj))
        return dict(items)

    return _flatten(data, "", separator)


def deep_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """Get value from nested dictionary using dot notation."""
    keys = key.split(".")
    value = data

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value


def deep_set(data: dict[str, Any], key: str, value: Any) -> bool:
    """Set value in nested dictionary using dot notation."""
    try:
        keys = key.split(".")
        current = data

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        return True
    except Exception as e:
        logging.error(f"Failed to set nested key {key}: {e}")
        return False


# ============================================================================
# STRING MANIPULATION
# ============================================================================

def sanitize_string(text: str, max_length: int = None) -> str:
    """Sanitize string by removing special characters and limiting length."""
    if not isinstance(text, str):
        text = str(text)

    # Remove special characters
    sanitized = "".join(c for c in text if c.isalnum() or c in " .-_")

    # Limit length
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized.strip()


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length with suffix."""
    if not isinstance(text, str):
        text = str(text)

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def format_string(template: str, **kwargs) -> str:
    """Format string template with keyword arguments."""
    try:
        return template.format(**kwargs)
    except Exception as e:
        logging.error(f"Failed to format string: {e}")
        return template


def extract_numbers(text: str) -> list[int | float]:
    """Extract numbers from string."""
    import re

    numbers = []
    for match in re.finditer(r'-?\d+\.?\d*', text):
        try:
            if '.' in match.group():
                numbers.append(float(match.group()))
            else:
                numbers.append(int(match.group()))
        except ValueError:
            continue

    return numbers


def clean_whitespace(text: str) -> str:
    """Clean whitespace in string."""
    if not isinstance(text, str):
        text = str(text)

    # Replace multiple whitespace with single space
    import re
    cleaned = re.sub(r'\s+', ' ', text)

    return cleaned.strip()


# ============================================================================
# DATE/TIME OPERATIONS
# ============================================================================

def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().isoformat()


def get_timestamp_utc() -> str:
    """Get current UTC timestamp as string."""
    return datetime.utcnow().isoformat()


def parse_timestamp(timestamp: str) -> datetime | None:
    """Parse timestamp string to datetime object."""
    try:
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except Exception as e:
        logging.error(f"Failed to parse timestamp {timestamp}: {e}")
        return None


def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime object to string."""
    try:
        return dt.strftime(format_str)
    except Exception as e:
        logging.error(f"Failed to format timestamp: {e}")
        return str(dt)


def add_timedelta(dt: datetime, **kwargs) -> datetime:
    """Add timedelta to datetime."""
    try:
        return dt + timedelta(**kwargs)
    except Exception as e:
        logging.error(f"Failed to add timedelta: {e}")
        return dt


def time_difference(start: datetime, end: datetime) -> timedelta:
    """Calculate time difference between two datetimes."""
    try:
        return end - start
    except Exception as e:
        logging.error(f"Failed to calculate time difference: {e}")
        return timedelta(0)


def is_weekend(dt: datetime) -> bool:
    """Check if datetime is weekend."""
    return dt.weekday() >= 5


def is_business_hours(dt: datetime, start_hour: int = 9, end_hour: int = 17) -> bool:
    """Check if datetime is during business hours."""
    return start_hour <= dt.hour < end_hour and not is_weekend(dt)


# ============================================================================
# MATHEMATICAL OPERATIONS
# ============================================================================

def clamp(value: int | float, min_value: int | float, max_value: int | float) -> int | float:
    """Clamp value between min and max."""
    return max(min_value, min(value, max_value))


def lerp(a: int | float, b: int | float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def normalize(value: int | float, min_value: int | float, max_value: int | float) -> float:
    """Normalize value to range [0, 1]."""
    if max_value == min_value:
        return 0.0
    return (value - min_value) / (max_value - min_value)


def denormalize(value: float, min_value: int | float, max_value: int | float) -> float:
    """Denormalize value from range [0, 1] to [min_value, max_value]."""
    return min_value + value * (max_value - min_value)


def round_to_nearest(value: int | float, nearest: int | float) -> int | float:
    """Round value to nearest multiple."""
    return round(value / nearest) * nearest


def percentage(value: int | float, total: int | float) -> float:
    """Calculate percentage of value relative to total."""
    if total == 0:
        return 0.0
    return (value / total) * 100


def average(values: list[int | float]) -> float:
    """Calculate average of values."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values: list[int | float]) -> float:
    """Calculate median of values."""
    if not values:
        return 0.0

    sorted_values = sorted(values)
    n = len(sorted_values)

    if n % 2 == 0:
        return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        return sorted_values[n // 2]


# ============================================================================
# IDENTIFIER GENERATION
# ============================================================================

def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate unique identifier."""
    if prefix:
        return f"{prefix}_{uuid.uuid4().hex[:length]}"
    return uuid.uuid4().hex[:length]


def generate_short_id(length: int = 6) -> str:
    """Generate short unique identifier."""
    return uuid.uuid4().hex[:length]


def generate_uuid() -> str:
    """Generate full UUID."""
    return str(uuid.uuid4())


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def is_valid_email(email: str) -> bool:
    """Validate email address."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Validate URL."""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def is_valid_phone(phone: str) -> bool:
    """Validate phone number."""
    import re
    pattern = r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'
    return bool(re.match(pattern, phone))


def is_numeric(value: Any) -> bool:
    """Check if value is numeric."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_positive(value: Any) -> bool:
    """Check if value is positive."""
    return is_numeric(value) and float(value) > 0


def is_negative(value: Any) -> bool:
    """Check if value is negative."""
    return is_numeric(value) and float(value) < 0


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("Core Utilities - Consolidated Utility Functions")
    print("=" * 50)

    # Test file operations
    test_file = "test_utilities.txt"
    test_content = "This is a test file for utilities."

    if write_file(test_file, test_content):
        print(f"File written successfully: {test_file}")

        content = read_file(test_file)
        if content:
            print(f"File read successfully: {len(content)} characters")

        file_size = get_file_size(test_file)
        print(f"File size: {file_size} bytes")

        file_hash = get_file_hash(test_file)
        if file_hash:
            print(f"File hash: {file_hash}")

        delete_file(test_file)
        print("Test file cleaned up")

    # Test data processing
    test_data = {"name": "Agent-2", "type": "consolidation", "active": True}
    json_str = to_json(test_data)
    if json_str:
        print(f"JSON conversion successful: {len(json_str)} characters")

        parsed_data = from_json(json_str)
        if parsed_data:
            print(f"JSON parsing successful: {parsed_data}")

    # Test string manipulation
    test_string = "  This   is   a   test   string  "
    cleaned = clean_whitespace(test_string)
    print(f"String cleaned: '{cleaned}'")

    truncated = truncate_string(cleaned, 20)
    print(f"String truncated: '{truncated}'")

    # Test date/time operations
    timestamp = get_timestamp()
    print(f"Current timestamp: {timestamp}")

    # Test mathematical operations
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    avg = average(values)
    med = median(values)
    print(f"Average: {avg}, Median: {med}")

    # Test identifier generation
    test_id = generate_id("test", 8)
    print(f"Generated ID: {test_id}")

    # Test validation
    test_email = "agent2@swarm.ai"
    print(f"Email validation: {is_valid_email(test_email)}")

    print("\nCore Utilities initialization complete!")


if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
