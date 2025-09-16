#!/usr/bin/env python3
"""
Configuration Management Package - V2 Compliant
==============================================

Modularized configuration management system extracted from consolidated_config_management.py
for V2 compliance (≤400 lines per module).

Modules:
- config_scanner: Configuration pattern scanning
- config_validator: Configuration validation and verification
- config_consolidator: Configuration consolidation and management

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from .config_scanner import (
    ConfigPattern,
    ConfigurationScanner,
    EnvironmentVariableScanner,
    JSONConfigScanner,
    YAMLConfigScanner,
    ConfigFileScanner,
    ConfigurationScannerRegistry
)

from .config_validator import (
    ConfigValidationResult,
    ConfigurationValidator
)

from .config_consolidator import (
    ConfigConsolidationResult,
    ConfigurationConsolidator
)

__all__ = [
    # Scanner classes
    "ConfigPattern",
    "ConfigurationScanner",
    "EnvironmentVariableScanner",
    "JSONConfigScanner",
    "YAMLConfigScanner",
    "ConfigFileScanner",
    "ConfigurationScannerRegistry",
    
    # Validator classes
    "ConfigValidationResult",
    "ConfigurationValidator",
    
    # Consolidator classes
    "ConfigConsolidationResult",
    "ConfigurationConsolidator"
]

__version__ = "1.0.0"
__author__ = "Agent-3 (Infrastructure & DevOps Specialist)"
