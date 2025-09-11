"""
Thea Configuration Module - V2 Compliant
=========================================

Centralized configuration management for Thea services.
Single Source of Truth (SSOT) for all Thea-related settings.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

from .thea_config import TheaConfig, get_thea_config

__all__ = ['TheaConfig', 'get_thea_config']
