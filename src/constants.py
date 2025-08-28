"""Centralized constants for health monitoring modules."""
from pathlib import Path

# Repository root (two levels up from this file)
ROOT_DIR = Path(__file__).resolve().parents[1]

# Directories used by monitoring utilities
HEALTH_REPORTS_DIR = ROOT_DIR / "health_reports"
HEALTH_CHARTS_DIR = ROOT_DIR / "health_charts"
MONITORING_DIR = ROOT_DIR / "agent_workspaces" / "monitoring"
