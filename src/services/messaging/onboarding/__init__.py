#!/usr/bin/env python3
"""
Onboarding Module - V2 Compliance
================================

Onboarding module for agent initialization and setup.

Author: Agent-2 (Security Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

from .onboarding_service import OnboardingService, onboarding_service

__all__ = ["OnboardingService", "onboarding_service"]
