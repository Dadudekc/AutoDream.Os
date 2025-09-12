#!/usr/bin/env python3
"""
Paths Constants - Repository Path Definitions

This module provides path-related constants for the V2 compliance system.

Uses unified utilities system for consistent path resolution across all
modules.

V2 COMPLIANCE: Single source of truth for path definitions
DRY ELIMINATION: Eliminates duplicate path resolution patterns

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Using Unified Utilities System
"""

from pathlib import Path

# ================================
# PROJECT PATHS
# ================================

# Project root directory - consolidated path resolution
ROOT_DIR = Path(__file__).resolve().parents[3]

# Health monitoring directories
HEALTH_REPORTS_DIR = ROOT_DIR / "health_reports"
HEALTH_CHARTS_DIR = ROOT_DIR / "health_charts"

# Agent workspaces
AGENT_WORKSPACES_DIR = ROOT_DIR / "agent_workspaces"
MONITORING_DIR = AGENT_WORKSPACES_DIR / "monitoring"

# Core directories
SRC_DIR = ROOT_DIR / "src"
CORE_DIR = SRC_DIR / "core"
SERVICES_DIR = SRC_DIR / "services"
CONFIG_DIR = ROOT_DIR / "config"
LOGS_DIR = ROOT_DIR / "logs"
DATA_DIR = ROOT_DIR / "data"
SCRIPTS_DIR = ROOT_DIR / "scripts"
DOCS_DIR = ROOT_DIR / "docs"
TESTS_DIR = ROOT_DIR / "tests"

# Vector database directories
UNIFIED_VECTOR_DB_DIR = ROOT_DIR / "unified_vector_db"
STATUS_EMBEDDINGS_FILE = UNIFIED_VECTOR_DB_DIR / "status_embeddings.json"

# ================================
# UTILITY FUNCTIONS
# ================================


def get_agent_workspace(agent_id: str) -> Path:
    """Get agent workspace directory path."""
    return AGENT_WORKSPACES_DIR / f"Agent-{agent_id}"


def get_agent_inbox(agent_id: str) -> Path:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.constants.paths import Paths

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Paths(config)

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

    """Get agent inbox directory path."""
    return get_agent_workspace(agent_id) / "inbox"


def get_agent_status_file(agent_id: str) -> Path:
    """Get agent status file path."""
    return get_agent_workspace(agent_id) / "status.json"


def ensure_path_exists(path: Path) -> bool:
    """Ensure path exists, create if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return True


# ================================
# LEGACY COMPATIBILITY
# ================================

LEGACY_ROOT_DIR = ROOT_DIR
LEGACY_HEALTH_REPORTS_DIR = HEALTH_REPORTS_DIR
LEGACY_HEALTH_CHARTS_DIR = HEALTH_CHARTS_DIR
LEGACY_MONITORING_DIR = MONITORING_DIR
