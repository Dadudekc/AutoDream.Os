"""
Templates Package
=================

Package for SWARM system templates including onboarding roles and devlog templates.
"""

from .onboarding_roles import ROLES, build_role_message

__all__ = [
    "ROLES",
    "build_role_message"
]
