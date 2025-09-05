#!/usr/bin/env python3
"""
Emergency Intervention Engine - V2 Compliance Module
===================================================

Backward compatibility wrapper for emergency intervention engine.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .emergency_intervention_engine_refactored import EmergencyInterventionEngine

# Backward compatibility - export the refactored class
__all__ = ['EmergencyInterventionEngine']