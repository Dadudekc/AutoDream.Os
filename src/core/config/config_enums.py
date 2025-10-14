#!/usr/bin/env python3
"""
Configuration Enums - V2 Compliance Module
==========================================

Enum types for unified configuration system.
Extracted from config_ssot.py for better modularity.

V2 Compliance: Single Responsibility Principle
SOLID Principles: Open-Closed Principle

Author: Agent-2 (Architecture & Design Specialist) - ROI 32.26 Task
Extracted from: Agent-7's config_ssot.py consolidation
Created: 2025-10-13
License: MIT
"""

from enum import Enum


class ConfigEnvironment(str, Enum):
    """Configuration environment types."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    STAGING = "staging"


class ConfigSource(str, Enum):
    """Configuration source types."""

    ENVIRONMENT = "environment"
    FILE = "file"
    DEFAULT = "default"
    RUNTIME = "runtime"


class ReportFormat(str, Enum):
    """Report output formats."""

    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    CONSOLE = "console"


__all__ = [
    "ConfigEnvironment",
    "ConfigSource",
    "ReportFormat",
]
