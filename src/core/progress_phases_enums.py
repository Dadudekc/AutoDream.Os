#!/usr/bin/env python3
"""
Progress Phases and Enums - Progress Phase Definitions
====================================================

Progress phase and benchmark enum definitions for the progress tracking system.
Part of the modularization of unified_progress_tracking.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from enum import Enum


class ProgressPhase(Enum):
    """Architecture consolidation phases."""

    ANALYSIS = "analysis"
    PLANNING = "planning"
    CONSOLIDATION = "consolidation"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"
    COMPLETION = "completion"


class SuperiorityBenchmark(Enum):
    """Superiority benchmark categories."""

    CONSOLIDATION_EFFICIENCY = "consolidation_efficiency"
    QC_COMPLIANCE = "qc_compliance"
    INTEGRATION_SUCCESS = "integration_success"
    PROGRESS_VELOCITY = "progress_velocity"
    BLOCKER_RESOLUTION = "blocker_resolution"

