#!/usr/bin/env python3
"""
Vector Integration Monitor - V2 Compliant Refactored
====================================================

V2 compliance redirect to modular vector integration monitor system.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: V2 compliant modular vector integration monitor
"""

# V2 COMPLIANCE REDIRECT - see refactored modular system
from .vector_integration_monitor_refactored import VectorIntegrationMonitor
from .vector_integration_models import PerformanceAlert, PerformanceMetrics, IntegrationConfig, AlertLevel
from .vector_integration_monitor_engine import VectorIntegrationMonitorEngine

# Backward compatibility - re-export everything
__all__ = [
    'VectorIntegrationMonitor',
    'PerformanceAlert',
    'PerformanceMetrics',
    'IntegrationConfig',
    'AlertLevel',
    'VectorIntegrationMonitorEngine'
]