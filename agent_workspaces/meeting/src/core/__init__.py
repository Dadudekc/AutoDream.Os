#!/usr/bin/env python3
"""
Core Package - Agent Cellphone V2
================================

Core system modules including async coordination, parallel initialization,
and batch registration systems.

Author: Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
License: MIT
"""

# Async Coordination System
from .async_coordination_core import AsyncCoordinationSystem
from .async_coordination_models import (
    CoordinationTask, TaskResult, TaskStatus, TaskType,
    CoordinationMode, TaskPriority, PerformanceMetrics, CoordinationConfig
)
from .async_coordination_executor import TaskExecutor
from .async_coordination_metrics import MetricsManager
from .async_coordination_benchmark import benchmark_async_coordination

# Parallel Initialization System
from .parallel_initialization import ParallelInitializationSystem

# Batch Registration System  
from .batch_registration import BatchRegistrationSystem

# Event-Driven Monitoring System
from .event_driven_monitoring import EventDrivenMonitoringSystem

# COORD-012 Integration & Testing Suite
from .coord_012_integration_suite import COORD012IntegrationSuite

# COORD-012 Performance Validation
from .coord_012_performance_validation import COORD012PerformanceValidator

__version__ = "2.0.0"
__author__ = "Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)"
__description__ = "Core coordination and optimization systems for Agent Cellphone V2"

__all__ = [
    # Async Coordination
    "AsyncCoordinationSystem",
    "CoordinationTask",
    "TaskResult", 
    "TaskStatus",
    "TaskType",
    "CoordinationMode",
    "TaskPriority",
    "PerformanceMetrics",
    "CoordinationConfig",
    "TaskExecutor",
    "MetricsManager",
    "benchmark_async_coordination",
    
    # Parallel Initialization
    "ParallelInitializationSystem",
    
    # Batch Registration
    "BatchRegistrationSystem",
    
    # Event-Driven Monitoring
    "EventDrivenMonitoringSystem",
    
    # COORD-012 Integration & Testing
    "COORD012IntegrationSuite",
    "COORD012PerformanceValidator"
]
