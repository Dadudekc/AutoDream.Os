#!/usr/bin/env python3
"""
Data Processing Orchestrator - V2 Compliance Module
===================================================

Main coordination logic for data processing operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .data_processing_models import ProcessingConfig
from .data_processing_engine import DataProcessingEngine


class UnifiedDataProcessingSystem:
    """Main orchestrator for data processing operations."""

    def __init__(self, config: ProcessingConfig = None):
        """Initialize unified data processing system."""
        self.config = config or ProcessingConfig()
        self.engine = DataProcessingEngine(self.config)

    # ================================
    # FILE PROCESSING
    # ================================

    def read_csv(self, file_path: Union[str, Path], **kwargs) -> List[Dict[str, Any]]:
        """Read CSV file with unified error handling."""
        return self.engine.read_csv(file_path, **kwargs)

    def write_csv(
        self, data: List[Dict[str, Any]], file_path: Union[str, Path], **kwargs
    ) -> bool:
        """Write CSV file with unified error handling."""
        return self.engine.write_csv(data, file_path, **kwargs)

    def read_json(self, file_path: Union[str, Path], **kwargs) -> Any:
        """Read JSON file with unified error handling."""
        return self.engine.read_json(file_path, **kwargs)

    def write_json(self, data: Any, file_path: Union[str, Path], **kwargs) -> bool:
        """Write JSON file with unified error handling."""
        return self.engine.write_json(data, file_path, **kwargs)

    # ================================
    # DATABASE PROCESSING
    # ================================

    def connect_sqlite(self, db_path: Union[str, Path]) -> sqlite3.Connection:
        """Connect to SQLite database with unified error handling."""
        return self.engine.connect_sqlite(db_path)

    def execute_query(
        self, conn: sqlite3.Connection, query: str, params: tuple = ()
    ) -> List[Dict[str, Any]]:
        """Execute SQL query with unified error handling."""
        return self.engine.execute_query(conn, query, params)

    # ================================
    # HTTP PROCESSING
    # ================================

    def make_request(
        self, url: str, method: str = "GET", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make HTTP request with unified error handling."""
        return self.engine.make_request(url, method, **kwargs)

    # ================================
    # DATA VALIDATION
    # ================================

    def validate_data_structure(self, data: Any, required_fields: List[str]) -> bool:
        """Validate data structure with unified error handling."""
        result = self.engine.validate_data_structure(data, required_fields)
        return result.is_valid

    def clean_data(
        self, data: List[Dict[str, Any]], remove_empty: bool = True
    ) -> List[Dict[str, Any]]:
        """Clean data with unified error handling."""
        return self.engine.clean_data(data, remove_empty)

    # ================================
    # UTILITY METHODS
    # ================================

    def get_processing_info(self) -> Dict[str, Any]:
        """Get information about processing capabilities."""
        return {
            "pandas_available": self.engine.pandas_available,
            "numpy_available": self.engine.numpy_available,
            "requests_available": self.engine.requests_available,
            "config": {
                "default_encoding": self.config.default_encoding,
                "max_file_size_mb": self.config.max_file_size_mb,
                "timeout_seconds": self.config.timeout_seconds,
                "retry_attempts": self.config.retry_attempts,
            },
        }


# ================================
# GLOBAL INSTANCE
# ================================

_unified_data_processing = None


def get_unified_data_processing() -> UnifiedDataProcessingSystem:
    """Get the global unified data processing system instance."""
    global _unified_data_processing
    if _unified_data_processing is None:
        _unified_data_processing = UnifiedDataProcessingSystem()
    return _unified_data_processing


# ================================
# CONVENIENCE FUNCTIONS
# ================================


def read_csv(file_path: Union[str, Path], **kwargs) -> List[Dict[str, Any]]:
    """Convenience function to read CSV file."""
    return get_unified_data_processing().read_csv(file_path, **kwargs)


def write_csv(
    data: List[Dict[str, Any]], file_path: Union[str, Path], **kwargs
) -> bool:
    """Convenience function to write CSV file."""
    return get_unified_data_processing().write_csv(data, file_path, **kwargs)


def read_json(file_path: Union[str, Path], **kwargs) -> Any:
    """Convenience function to read JSON file."""
    return get_unified_data_processing().read_json(file_path, **kwargs)


def write_json(data: Any, file_path: Union[str, Path], **kwargs) -> bool:
    """Convenience function to write JSON file."""
    return get_unified_data_processing().write_json(data, file_path, **kwargs)


def connect_sqlite(db_path: Union[str, Path]) -> sqlite3.Connection:
    """Convenience function to connect to SQLite database."""
    return get_unified_data_processing().connect_sqlite(db_path)


def execute_query(
    conn: sqlite3.Connection, query: str, params: tuple = ()
) -> List[Dict[str, Any]]:
    """Convenience function to execute SQL query."""
    return get_unified_data_processing().execute_query(conn, query, params)


def make_request(url: str, method: str = "GET", **kwargs) -> Optional[Dict[str, Any]]:
    """Convenience function to make HTTP request."""
    return get_unified_data_processing().make_request(url, method, **kwargs)


def validate_data_structure(data: Any, required_fields: List[str]) -> bool:
    """Convenience function to validate data structure."""
    return get_unified_data_processing().validate_data_structure(data, required_fields)


def clean_data(
    data: List[Dict[str, Any]], remove_empty: bool = True
) -> List[Dict[str, Any]]:
    """Convenience function to clean data."""
    return get_unified_data_processing().clean_data(data, remove_empty)
