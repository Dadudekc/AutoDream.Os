"""
Command Handlers Package - Modular command processing
===================================================

This package provides modular command handling for messaging operations,
breaking down the large command_handler.py into focused, maintainable modules.

Modules:
- base: Base command handler class
- coordinate: Coordinate-related commands
- contract: Contract management commands
- captain: Captain communication commands
- resume: Resume system commands
- onboarding: Agent onboarding commands
"""

from .base import BaseCommandHandler
from .coordinate import CoordinateCommandHandler
from .contract import ContractCommandHandler
from .captain import CaptainCommandHandler
from .resume import ResumeCommandHandler
from .onboarding import OnboardingCommandHandler

__all__ = [
    'BaseCommandHandler',
    'CoordinateCommandHandler', 
    'ContractCommandHandler',
    'CaptainCommandHandler',
    'ResumeCommandHandler',
    'OnboardingCommandHandler'
]
