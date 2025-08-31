#!/usr/bin/env python3
"""
Paths Constants - Repository Path Definitions

This module provides path-related constants.

Agent: Agent-6 (Performance Optimization Manager)
Mission: Autonomous Cleanup - V2 Compliance
Status: SSOT Consolidation in Progress
"""

from pathlib import Path

# Repository paths
ROOT_DIR = Path(__file__).resolve().parents[3]
HEALTH_REPORTS_DIR = ROOT_DIR / "health_reports"
HEALTH_CHARTS_DIR = ROOT_DIR / "health_charts"
MONITORING_DIR = ROOT_DIR / "agent_workspaces" / "monitoring"
