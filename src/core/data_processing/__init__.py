#!/usr/bin/env python3
"""
Data Processing Package - V2 Compliance Module
==============================================

Modular data processing system for V2 compliance.
Replaces monolithic unified_data_processing_system.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .data_processing_models import (
    ProcessingConfig,
    ProcessingResult,
    DataValidationResult,
)
from .data_processing_engine import DataProcessingEngine
from .data_processing_orchestrator import (
    UnifiedDataProcessingSystem,
    get_unified_data_processing,
    read_csv,
    write_csv,
    read_json,
    write_json,
    connect_sqlite,
    execute_query,
    make_request,
    validate_data_structure,
    clean_data,
)

__all__ = [
    'ProcessingConfig',
    'ProcessingResult',
    'DataValidationResult',
    'DataProcessingEngine',
    'UnifiedDataProcessingSystem',
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
]
