#!/usr/bin/env python3
"""
Backup & Disaster Recovery System - Module Initialization
========================================================

Advanced backup and disaster recovery system for Agent Cellphone V2.
Provides comprehensive backup, monitoring, and business continuity capabilities.

Author: Agent-8 (SSOT & System Integration Specialist)
Mission: Advanced Backup & Disaster Recovery System
License: MIT
"""

from .backup_cli import BackupCLI
from .backup_monitoring import BackupMonitoringSystem, create_backup_monitoring_system
from .backup_scheduler import BackupScheduler, create_backup_scheduler
from .backup_system_core import BackupSystemCore, create_backup_system
from .business_continuity_planner import (
    BusinessContinuityPlanner,
    DisasterType,
    RecoveryPriority,
    create_business_continuity_planner,
)

__all__ = [
    # Core backup system
    "BackupSystemCore",
    "create_backup_system",
    # Backup scheduler
    "BackupScheduler",
    "create_backup_scheduler",
    # Monitoring system
    "BackupMonitoringSystem",
    "create_backup_monitoring_system",
    # Business continuity planning
    "BusinessContinuityPlanner",
    "DisasterType",
    "RecoveryPriority",
    "create_business_continuity_planner",
    # CLI interface
    "BackupCLI",
]

__version__ = "1.0.0"
__author__ = "Agent-8 (SSOT & System Integration Specialist)"
__description__ = "Advanced Backup & Disaster Recovery System"
