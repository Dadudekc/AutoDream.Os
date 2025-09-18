#!/usr/bin/env python3
"""
V3 Validation Package
=====================

Modular validation system for V3 components.
V2 Compliance: All modules ≤400 lines, focused responsibilities.
"""

from .validation_framework_core import V3ValidationFrameworkCore
from .v3_directives_validator import V3DirectivesValidator
from .quality_gates_validator import QualityGatesValidator
from .contract_system_validator import ContractSystemValidator
from .integration_validator import IntegrationValidator
from .performance_validator import PerformanceValidator
from .security_validator import SecurityValidator
from .documentation_validator import DocumentationValidator
from .validation_utils import (
    load_json_file,
    save_json_file,
    check_file_exists,
    validate_required_fields,
    get_team_alpha_agents,
    format_validation_summary
)

__all__ = [
    "V3ValidationFrameworkCore",
    "V3DirectivesValidator",
    "QualityGatesValidator", 
    "ContractSystemValidator",
    "IntegrationValidator",
    "PerformanceValidator",
    "SecurityValidator",
    "DocumentationValidator",
    "load_json_file",
    "save_json_file",
    "check_file_exists",
    "validate_required_fields",
    "get_team_alpha_agents",
    "format_validation_summary"
]
