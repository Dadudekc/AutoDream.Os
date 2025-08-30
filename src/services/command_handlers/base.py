#!/usr/bin/env python3
"""
Base Command Handler - Common functionality for all command handlers
==================================================================

Provides the base class and common functionality for all command handlers.
"""

import argparse
import logging
from abc import ABC, abstractmethod
from ..interfaces import MessagingMode, MessageType
from ..unified_messaging_service import UnifiedMessagingService
from ..output_formatter import OutputFormatter


class BaseCommandHandler(ABC):
    """Base class for all command handlers"""
    
    def __init__(self, formatter: OutputFormatter | None = None):
        self.service = UnifiedMessagingService()
        self.formatter = formatter or OutputFormatter()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"{self.__class__.__name__} initialized")
    
    def set_mode(self, mode: MessagingMode):
        """Set the messaging mode"""
        self.service.set_mode(mode)
    
    @abstractmethod
    def can_handle(self, args: argparse.Namespace) -> bool:
        """Check if this handler can handle the given arguments"""
        pass
    
    @abstractmethod
    def handle(self, args: argparse.Namespace) -> bool:
        """Handle the command"""
        pass
    
    def _log_success(self, message: str):
        """Log a success message"""
        self.logger.info(f"✅ {message}")
    
    def _log_error(self, message: str, error: Exception = None):
        """Log an error message"""
        if error:
            self.logger.error(f"❌ {message}: {error}")
        else:
            self.logger.error(f"❌ {message}")
    
    def _log_info(self, message: str):
        """Log an info message"""
        self.logger.info(f"ℹ️ {message}")
