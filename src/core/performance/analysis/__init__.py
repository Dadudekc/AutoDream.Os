#!/usr/bin/env python3
"""
Performance Analysis Package - V2 Modular Architecture
=====================================================

Modular analysis system for performance management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .performance_analyzer import PerformanceAnalyzer, PerformanceLevel

__all__ = [
    "PerformanceAnalyzer",
    "PerformanceLevel"
]
