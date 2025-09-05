#!/usr/bin/env python3
"""
Message Validation Engine - V2 Compliance Module
===============================================

Backward compatibility wrapper for message validation engine.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .message_validation_engine_refactored import MessageValidationEngine

# Backward compatibility - export the refactored class
__all__ = ['MessageValidationEngine']
