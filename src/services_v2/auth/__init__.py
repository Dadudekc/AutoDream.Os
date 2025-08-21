#!/usr/bin/env python3
"""
Services V2 - Authentication Module
==================================

Advanced authentication and authorization services for V2 architecture.
Provides enterprise-grade security with integration testing capabilities.
"""

from .auth_service import AuthService
from .auth_integration_tester import AuthIntegrationTester
from .auth_performance_monitor import AuthPerformanceMonitor

__all__ = [
    'AuthService',
    'AuthIntegrationTester', 
    'AuthPerformanceMonitor'
]

__version__ = '2.0.0'
__author__ = 'Agent-2 (AI & ML Integration Specialist)'
__status__ = 'Integration Testing Phase'
