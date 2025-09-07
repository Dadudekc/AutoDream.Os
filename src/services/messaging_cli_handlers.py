#!/usr/bin/env python3
"""
Messaging CLI Handlers - SOLID Compliant Registry (V2 Compliant)
================================================================

🎯 SOLID REFACTORING COMPLETE: Massive file split into focused modules
✅ V2 Compliance: Registry file under 400 line limit
✅ SOLID SRP: Each handler has single responsibility in separate files
✅ SOLID OCP: Extension without modification through registry
✅ SOLID LSP: Subtypes honor base contracts
✅ SOLID ISP: Focused interfaces in each handler
✅ SOLID DIP: Dependency injection throughout

This file contains:
- CommandHandler: Abstract protocol for all handlers
- CommandHandlerRegistry: OCP-compliant handler registry
- MessagingCLICommandHandlers: Facade for backward compatibility
- Legacy wrapper functions: Backward compatibility layer

🔄 REFACTORING HISTORY:
- messaging_cli_handlers.py (761 lines) → Split into focused modules:
  - utility_command_handler.py (SRP: utility commands only)
  - contract_command_handler.py (SRP: contract commands only)
  - onboarding_command_handler.py (SRP: onboarding commands only)
  - message_command_handler.py (SRP: message commands only)
  - overnight_command_handler.py (SRP: overnight commands only)

Author: Agent-1 (SOLID Sentinel) - SOLID Enforcement
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional, Tuple, Protocol

# SOLID REFACTORING: Import focused handlers from separate files
from .utility_command_handler import UtilityCommandHandler, ICoordinateManager, CoordinateManager
from .contract_command_handler import ContractCommandHandler
from .onboarding_command_handler import OnboardingCommandHandler
from .message_command_handler import MessageCommandHandler
from .overnight_command_handler import OvernightCommandHandler
from .role_command_handler import RoleCommandHandler

logger = logging.getLogger(__name__)


# ===============================================
# SOLID PRINCIPLES IMPLEMENTATION
# ===============================================

# DIP: Abstract interface for command handlers (ISP: Segregated interface)
class CommandHandler(Protocol):
    """Abstract interface for command handlers."""

    def can_handle(self, args: Any) -> bool:
        """Check if this handler can process the given arguments."""
        ...

    def handle(self, args: Any) -> bool:
        """Handle the command with given arguments."""
        ...


# OCP: Registry allows extension without modifying core
class CommandHandlerRegistry:
    """Registry for command handlers - Open-Closed Principle compliant."""

    def __init__(self):
        """Initialize registry with default handlers."""
        self.handlers: List[CommandHandler] = [
            UtilityCommandHandler(),
            ContractCommandHandler(),
            OnboardingCommandHandler(),
            MessageCommandHandler(),
            OvernightCommandHandler(),
            RoleCommandHandler()
        ]

    def register_handler(self, handler: CommandHandler) -> None:
        """Register a new command handler (OCP: Extension without modification)."""
        self.handlers.append(handler)

    def find_handler(self, args: Any) -> Optional[CommandHandler]:
        """Find the appropriate handler for the given arguments."""
        for handler in self.handlers:
            if handler.can_handle(args):
                return handler
        return None

    def handle_command(self, args: Any) -> bool:
        """Handle command using appropriate handler."""
        handler = self.find_handler(args)
        if handler:
            return handler.handle(args)
        return False


# LSP: MessagingCLICommandHandlers honors the expected interface contracts
class MessagingCLICommandHandlers:
    """Unified command handler facade - SOLID Compliant."""

    def __init__(self, registry: Optional[CommandHandlerRegistry] = None):
        """Initialize with dependency injection."""
        # DIP: Inject registry or use default
        self.registry = registry or CommandHandlerRegistry()

    def handle_utility_commands(self, args: Any) -> bool:
        """Handle utility commands (legacy interface)."""
        return self.registry.handle_command(args)

    def handle_contract_commands(self, args: Any) -> bool:
        """Handle contract commands (legacy interface)."""
        return self.registry.handle_command(args)

    def handle_onboarding_commands(self, args: Any) -> bool:
        """Handle onboarding commands (legacy interface)."""
        return self.registry.handle_command(args)

    def handle_message_commands(self, args: Any) -> bool:
        """Handle message commands (legacy interface)."""
        return self.registry.handle_command(args)

    def handle_overnight_commands(self, args: Any) -> bool:
        """Handle overnight commands (legacy interface)."""
        return self.registry.handle_command(args)


# ===============================================
# LEGACY SUPPORT (Backward Compatibility)
# ===============================================

# Global registry instance for backward compatibility
_default_registry = None

def get_default_registry() -> CommandHandlerRegistry:
    """Get the default registry instance (singleton pattern)."""
    global _default_registry
    if _default_registry is None:
        _default_registry = CommandHandlerRegistry()
    return _default_registry

def handle_utility_commands(args: Any) -> bool:
    """Legacy utility commands handler."""
    return get_default_registry().handle_command(args)

def handle_contract_commands(args: Any) -> bool:
    """Legacy contract commands handler."""
    return get_default_registry().handle_command(args)

def handle_onboarding_commands(args: Any) -> bool:
    """Legacy onboarding commands handler."""
    return get_default_registry().handle_command(args)

def handle_message_commands(args: Any) -> bool:
    """Legacy message commands handler."""
    return get_default_registry().handle_command(args)

def handle_overnight_commands(args: Any) -> bool:
    """Legacy overnight commands handler."""
    return get_default_registry().handle_command(args)


# ===============================================
# MODULE EXPORTS
# ===============================================

__all__ = [
    'CommandHandler',
    'CommandHandlerRegistry',
    'MessagingCLICommandHandlers',
    'get_default_registry',
    'handle_utility_commands',
    'handle_contract_commands',
    'handle_onboarding_commands',
    'handle_message_commands',
    'handle_overnight_commands'
]
