""""
Coordination System
===================

Modular coordination system using Repository, Factory, and Service Layer patterns.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
""""

from .services.coordination_service import CoordinationService
from .coordination_cli import CoordinationCLI

__all__ = ['CoordinationService', 'CoordinationCLI']'
