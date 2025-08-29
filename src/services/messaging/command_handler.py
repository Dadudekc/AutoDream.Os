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
from .interfaces import MessagingMode
from .output_formatter import OutputFormatter
from .command_handlers import (
    CoordinateCommandHandler,
    ContractCommandHandler,
    CaptainCommandHandler,
    ResumeCommandHandler,
    OnboardingCommandHandler
)


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
        
        self.logger.info("Messaging command handler initialized with modular handlers")
    
    def execute_command(self, args: argparse.Namespace) -> bool:
        """Execute the parsed command by delegating to appropriate handler"""
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
            self.logger.error(f"Error executing command: {e}")
            return False
    
    def _handle_validation(self) -> bool:
        """Handle coordinate validation"""
        try:
            # Use the first handler that can validate
            for handler in self.handlers:
                if hasattr(handler, 'validate_coordinates'):
                    results = handler.validate_coordinates()
                    self.formatter.validation_results(results)
                    return True
            
            self.logger.error("No validation handler found")
            return False
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False
