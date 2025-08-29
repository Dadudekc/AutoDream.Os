<<<<<<< HEAD
#!/usr/bin/env python3
"""
Command Handler - Main entry point for messaging operations
=========================================================

This module has been modularized to comply with V2 standards:
- LOC: Reduced from 1241 to under 100 lines
- SSOT: Single source of truth for command handling
- No duplication: All functionality moved to dedicated handler modules
"""

import argparse
import logging
=======
from __future__ import annotations

import argparse
import logging

>>>>>>> origin/codex/add-parser,-router,-executor-submodules
from .interfaces import MessagingMode
from .output_formatter import OutputFormatter
from .command_handlers import (
    CoordinateCommandHandler,
    ContractCommandHandler,
    CaptainCommandHandler,
    ResumeCommandHandler,
    OnboardingCommandHandler
)
from .unified_messaging_service import UnifiedMessagingService
<<<<<<< HEAD
from .config import CAPTAIN_ID, DEFAULT_COORDINATE_MODE
from .contract_system_manager import ContractSystemManager
from .error_handler import ErrorHandler
from .handlers.messaging_handlers import MessagingHandlers


class CommandHandler:
    """Main command handler that delegates to specialized handlers"""
    
    def __init__(self, formatter: OutputFormatter | None = None):
        self.formatter = formatter or OutputFormatter()
        self.logger = logging.getLogger(__name__)
        
        # Initialize specialized handlers
        self.handlers = [
            CoordinateCommandHandler(formatter),
            ContractCommandHandler(formatter),
            CaptainCommandHandler(formatter),
            ResumeCommandHandler(formatter),
            OnboardingCommandHandler(formatter)
        ]
        
        # Initialize additional services
        self.service = UnifiedMessagingService()
        self.contract_manager = ContractSystemManager()
        self.messaging_handlers = MessagingHandlers(self.service, self.formatter)
        
        self.logger.info("Messaging command handler initialized with modular handlers")
    
    def execute_command(self, args: argparse.Namespace) -> bool:
        """Execute the parsed command by delegating to appropriate handler"""
        return ErrorHandler.safe_execute(
            "Command execution", self.logger, self._execute_command_internal, args
        )
    
    def _execute_command_internal(self, args: argparse.Namespace) -> bool:
        """Internal command execution logic."""
        try:
            # Set mode for all handlers
            mode = MessagingMode(args.mode)
            for handler in self.handlers:
                handler.set_mode(mode)
            
            # Handle validation separately
            if args.validate:
                return self._handle_validation()
            
            # Find and use appropriate handler
            for handler in self.handlers:
                if handler.can_handle(args):
                    return handler.handle(args)
            
            self.logger.warning("No handler found for command")
            return False
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return False
    
    def _handle_validation(self) -> bool:
        """Handle validation command"""
        try:
            self.logger.info("Validation mode enabled")
            return True
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
=======
from .router import route_command
from .executor import CommandExecutor


logger = logging.getLogger(__name__)


class CommandHandler:
    """Wire together command parsing, routing and execution."""

    def __init__(self, formatter: OutputFormatter | None = None) -> None:
        service = UnifiedMessagingService()
        self.executor = CommandExecutor(service, formatter or OutputFormatter())
        logger.info("Messaging command handler initialized")

    def execute_command(self, args: argparse.Namespace) -> bool:
        """Route the command to the appropriate executor method."""
        try:
            mode = MessagingMode(args.mode)
            self.executor.service.set_mode(mode)
            action = route_command(args)
            if not action:
                return False
            handler = getattr(self.executor, action)
            return handler(args)
        except Exception as exc:  # pragma: no cover - defensive programming
            logger.error("Error executing command: %s", exc)
>>>>>>> origin/codex/add-parser,-router,-executor-submodules
            return False
