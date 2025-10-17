#!/usr/bin/env python3
"""
Error Class Consolidation
=========================

Consolidates duplicate error/exception classes across src/core.

Created by: Agent-3 (Infrastructure & DevOps Specialist)
Mission: DUP-005 Error Consolidation
Status: IN PROGRESS - Silent execution mode
"""


class ValidationError(Exception):
    """Base validation error - consolidates validation exceptions."""
    
    def __init__(self, message: str, field: str = None, errors: list = None):
        self.field = field
        self.errors = errors or []
        super().__init__(message)


class ConfigurationError(Exception):
    """Base configuration error - consolidates config exceptions."""
    
    def __init__(self, message: str, config_key: str = None):
        self.config_key = config_key
        super().__init__(message)


class IntegrationError(Exception):
    """Base integration error - consolidates integration exceptions."""
    
    def __init__(self, message: str, service: str = None):
        self.service = service
        super().__init__(message)


class DataProcessingError(Exception):
    """Base data processing error - consolidates processing exceptions."""
    
    def __init__(self, message: str, data_type: str = None):
        self.data_type = data_type
        super().__init__(message)


# Consolidating error classes from src/core - provides SSOT for exception handling

