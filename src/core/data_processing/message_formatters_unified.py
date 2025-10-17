"""
Unified Message Formatters - DUP-008 Partial Consolidation
==========================================================

Note: This consolidates SOME format_message duplicates.
Full consolidation requires coordinating with message_formatters.py.

For now: Provides unified interface for new code.

Author: Agent-1 - Integration & Core Systems Specialist  
Mission: DUP-008 Data Processing Patterns Consolidation
License: MIT
"""

from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class UnifiedMessageFormatter:
    """
    Unified message formatting interface.
    
    Provides standard formatting methods used across:
    - message_formatters.py (existing full/compact/minimal)
    - messaging_protocol_models.py
    - message_task/schemas.py
    - message_identity_clarification.py
    """
    
    def __init__(self, default_template: str = "compact"):
        """
        Initialize formatter.
        
        Args:
            default_template: Default template to use (full, compact, minimal)
        """
        self.default_template = default_template
        self.logger = logging.getLogger(__name__)
    
    def format_message(self, message: Any, template: str = None) -> str:
        """
        Format message using specified or default template.
        
        Args:
            message: Message object or dict to format
            template: Template type (full, compact, minimal)
            
        Returns:
            Formatted message string
        """
        template = template or self.default_template
        
        # Delegate to existing formatters for backward compatibility
        try:
            from ..message_formatters import (
                format_message_full,
                format_message_compact,
                format_message_minimal
            )
            
            if template == "full":
                return format_message_full(message)
            elif template == "minimal":
                return format_message_minimal(message)
            else:  # compact (default)
                return format_message_compact(message)
                
        except ImportError as e:
            self.logger.warning(f"Could not import message formatters: {e}")
            return self._fallback_format(message)
    
    def _fallback_format(self, message: Any) -> str:
        """Fallback formatting if imports fail."""
        if hasattr(message, 'content'):
            return str(message.content)
        elif isinstance(message, dict) and 'content' in message:
            return str(message['content'])
        else:
            return str(message)


# Singleton for convenience
_formatter = UnifiedMessageFormatter()


def format_message(message: Any, template: str = "compact") -> str:
    """
    Convenience function for message formatting.
    
    Args:
        message: Message to format
        template: Template type
        
    Returns:
        Formatted message string
    """
    return _formatter.format_message(message, template)

