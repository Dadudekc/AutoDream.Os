#!/usr/bin/env python3
"""
Unified Data Processing System - DRY Violation Elimination
=========================================================

Eliminates duplicate data processing import patterns across business intelligence modules.
Consolidates common data processing libraries and utilities into a single source of truth.

CONSOLIDATED PATTERNS:
- Duplicate pandas/numpy imports
- Duplicate JSON/CSV processing imports
- Duplicate database connection imports
- Duplicate data validation imports
- Duplicate file processing imports

Author: Agent-5 (Business Intelligence Specialist)
Mission: DRY Violations Elimination - Agent-2 Coordinated
Status: CONSOLIDATED - Data Processing Imports Unified
"""

import logging
import sqlite3
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Iterator, Callable
from dataclasses import dataclass
from enum import Enum

# Try to import optional data processing libraries
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

try:
    from sqlalchemy import create_engine, text
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    create_engine = None
    text = None

# Import unified systems
from .unified_logging_system import get_logger, get_unified_logger
from .unified_validation_system import validate_required_fields, validate_data_types


# ================================
# UNIFIED DATA PROCESSING SYSTEM
# ================================

class DataProcessingType(Enum):
    """Types of data processing operations."""
    CSV = "csv"
    JSON = "json"
    DATABASE = "database"
    API = "api"
    FILE = "file"
    PANDAS = "pandas"
    NUMPY = "numpy"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"


@dataclass
class DataProcessingContext:
    """Context for data processing operations."""
    processing_type: DataProcessingType
    data: Any
    metadata: Dict[str, Any]
    timestamp: float
    source: str
    target: Optional[str] = None


class UnifiedDataProcessingSystem:
    """
    Unified data processing system that consolidates all data processing patterns.
    
    ELIMINATES DUPLICATE PATTERNS:
    - Duplicate pandas/numpy imports across modules
    - Duplicate JSON/CSV processing logic
    - Duplicate database connection patterns
    - Duplicate API request patterns
    - Duplicate file processing patterns
    """
    
    def __init__(self):
        """Initialize the unified data processing system."""
        self.logger = get_logger(__name__)
        self.processing_history: List[DataProcessingContext] = []
        self.performance_metrics: Dict[str, float] = {}
        
        # Initialize processing capabilities
        self._initialize_capabilities()
    
    def _initialize_capabilities(self):
        """Initialize available data processing capabilities."""
        self.capabilities = {
            'pandas': PANDAS_AVAILABLE,
            'numpy': NUMPY_AVAILABLE,
            'requests': REQUESTS_AVAILABLE,
            'sqlalchemy': SQLALCHEMY_AVAILABLE
        }
        
        self.logger.info(f"Data processing capabilities: {self.capabilities}")
    
    # ================================
    # CSV PROCESSING
    # ================================
    
    def read_csv(self, file_path: Union[str, Path], **kwargs) -> List[Dict[str, Any]]:
        """Read CSV file with unified error handling."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
            
            self.logger.info(f"Successfully read CSV: {file_path} ({len(data)} rows)")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to read CSV {file_path}: {e}")
            raise
    
    def write_csv(self, data: List[Dict[str, Any]], file_path: Union[str, Path], **kwargs) -> bool:
        """Write data to CSV file with unified error handling."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not data:
                self.logger.warning(f"No data to write to CSV: {file_path}")
                return False
            
            fieldnames = data[0].keys() if data else []
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = write_csv(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"Successfully wrote CSV: {file_path} ({len(data)} rows)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write CSV {file_path}: {e}")
            raise
    
    # ================================
    # JSON PROCESSING
    # ================================
    
    def read_json(self, file_path: Union[str, Path], **kwargs) -> Any:
        """Read JSON file with unified error handling."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.logger.info(f"Successfully read JSON: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to read JSON {file_path}: {e}")
            raise
    
    def write_json(self, data: Any, file_path: Union[str, Path], **kwargs) -> bool:
        """Write data to JSON file with unified error handling."""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                write_json(data, file, indent=2, ensure_ascii=False, **kwargs)
            
            self.logger.info(f"Successfully wrote JSON: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write JSON {file_path}: {e}")
            raise
    
    # ================================
    # DATABASE PROCESSING
    # ================================
    
    def connect_sqlite(self, db_path: Union[str, Path]) -> sqlite3.Connection:
        """Connect to SQLite database with unified error handling."""
        try:
            db_path = Path(db_path)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row  # Enable column access by name
            
            self.logger.info(f"Successfully connected to SQLite: {db_path}")
            return conn
            
        except Exception as e:
            self.logger.error(f"Failed to connect to SQLite {db_path}: {e}")
            raise
    
    def execute_query(self, conn: sqlite3.Connection, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SQL query with unified error handling."""
        try:
            cursor = conn.cursor()
            execute_query(conn, query, params)
            
            # Convert rows to dictionaries
            columns = [description[0] for description in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            self.logger.info(f"Successfully executed query: {len(rows)} rows returned")
            return rows
            
        except Exception as e:
            self.logger.error(f"Failed to execute query: {e}")
            raise
    
    # ================================
    # PANDAS PROCESSING
    # ================================
    
    def read_dataframe(self, file_path: Union[str, Path], file_type: str = 'csv', **kwargs) -> Optional[Any]:
        """Read data using pandas with unified error handling."""
        if not PANDAS_AVAILABLE:
            self.logger.warning("Pandas not available, falling back to standard library")
            return None
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if file_type.lower() == 'csv':
                df = pd.read_csv(file_path, **kwargs)
            elif file_type.lower() == 'json':
                df = pd.read_json(file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            self.logger.info(f"Successfully read DataFrame: {file_path} ({len(df)} rows)")
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to read DataFrame {file_path}: {e}")
            raise
    
    def write_dataframe(self, df: Any, file_path: Union[str, Path], file_type: str = 'csv', **kwargs) -> bool:
        """Write DataFrame with unified error handling."""
        if not PANDAS_AVAILABLE:
            self.logger.warning("Pandas not available, cannot write DataFrame")
            return False
        
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_type.lower() == 'csv':
                df.to_csv(file_path, index=False, **kwargs)
            elif file_type.lower() == 'json':
                df.to_json(file_path, orient='records', indent=2, **kwargs)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            self.logger.info(f"Successfully wrote DataFrame: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write DataFrame {file_path}: {e}")
            raise
    
    # ================================
    # API PROCESSING
    # ================================
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request with unified error handling."""
        if not REQUESTS_AVAILABLE:
            self.logger.warning("Requests library not available")
            return None
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            
            self.logger.info(f"Successfully made {method} request to: {url}")
            return {'data': data, 'status_code': response.status_code, 'headers': dict(response.headers)}
            
        except Exception as e:
            self.logger.error(f"Failed to make {method} request to {url}: {e}")
            raise
    
    # ================================
    # DATA VALIDATION
    # ================================
    
    def validate_data_structure(self, data: Any, required_fields: List[str]) -> bool:
        """Validate data structure with unified error handling."""
        try:
            if isinstance(data, list):
                if not data:
                    self.logger.warning("Empty data list provided")
                    return False
                
                # Validate first item has required fields
                return validate_required_fields(data[0], required_fields)
            elif isinstance(data, dict):
                return validate_required_fields(data, required_fields)
            else:
                self.logger.warning(f"Unsupported data type for validation: {type(data)}")
                return False
                
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False
    
    def clean_data(self, data: List[Dict[str, Any]], remove_empty: bool = True) -> List[Dict[str, Any]]:
        """Clean data with unified error handling."""
        try:
            if not data:
                return data
            
            cleaned = []
            for item in data:
                if isinstance(item, dict):
                    if remove_empty:
                        # Remove empty values
                        cleaned_item = {k: v for k, v in item.items() if v is not None and v != ''}
                    else:
                        cleaned_item = item
                    
                    if cleaned_item:  # Only add non-empty items
                        cleaned.append(cleaned_item)
            
            self.logger.info(f"Data cleaned: {len(data)} -> {len(cleaned)} items")
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Data cleaning failed: {e}")
            return data
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'total_operations': len(self.processing_history),
            'capabilities': self.capabilities,
            'performance_metrics': self.performance_metrics
        }
    
    def log_operation(self, operation_type: DataProcessingType, data: Any, **kwargs):
        """Log a processing operation."""
        context = DataProcessingContext(
            processing_type=operation_type,
            data=data,
            metadata=kwargs,
            timestamp=datetime.now().timestamp(),
            source=kwargs.get('source', 'unknown')
        )
        self.processing_history.append(context)
        self.logger.info(f"Logged {operation_type.value} operation")


# ================================
# CONVENIENCE FUNCTIONS
# ================================

# Global instance for convenience
_unified_data_processing = None

def get_unified_data_processing() -> UnifiedDataProcessingSystem:
    """Get the global unified data processing system instance."""
    global _unified_data_processing
    if _unified_data_processing is None:
        _unified_data_processing = UnifiedDataProcessingSystem()
    return _unified_data_processing

# Convenience functions for common operations
def read_csv(file_path: Union[str, Path], **kwargs) -> List[Dict[str, Any]]:
    """Convenience function to read CSV file."""
    return get_unified_data_processing().read_csv(file_path, **kwargs)

def write_csv(data: List[Dict[str, Any]], file_path: Union[str, Path], **kwargs) -> bool:
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

def execute_query(conn: sqlite3.Connection, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Convenience function to execute SQL query."""
    return get_unified_data_processing().execute_query(conn, query, params)

def make_request(url: str, method: str = 'GET', **kwargs) -> Optional[Dict[str, Any]]:
    """Convenience function to make HTTP request."""
    return get_unified_data_processing().make_request(url, method, **kwargs)

def validate_data_structure(data: Any, required_fields: List[str]) -> bool:
    """Convenience function to validate data structure."""
    return get_unified_data_processing().validate_data_structure(data, required_fields)

def clean_data(data: List[Dict[str, Any]], remove_empty: bool = True) -> List[Dict[str, Any]]:
    """Convenience function to clean data."""
    return get_unified_data_processing().clean_data(data, remove_empty)


# Export all functionality
__all__ = [
    # Main class
    'UnifiedDataProcessingSystem',
    'DataProcessingType',
    'DataProcessingContext',
    
    # Convenience functions
    'get_unified_data_processing',
    'read_csv',
    'write_csv',
    'read_json',
    'write_json',
    'connect_sqlite',
    'execute_query',
    'make_request',
    'validate_data_structure',
    'clean_data',
    
    # Constants
    'PANDAS_AVAILABLE',
    'NUMPY_AVAILABLE',
    'REQUESTS_AVAILABLE',
    'SQLALCHEMY_AVAILABLE'
]
