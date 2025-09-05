"""
Messaging CLI Handlers - V2 Compliant Module
============================================

Main handler coordinator for messaging CLI commands.
Coordinates all handler modules and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import sys
from typing import Any, Dict, List, Optional

from .overnight_handler import OvernightHandler
from .utility_handler import UtilityHandler
from .contract_handler import ContractHandler
from .onboarding_handler import OnboardingHandler
from .message_handler import MessageHandler


class MessagingCLIHandlers:
    """
    Main handler coordinator for messaging CLI commands.
    
    Coordinates all handler modules and provides unified interface
    for messaging CLI operations.
    """
    
    def __init__(self):
        """Initialize messaging CLI handlers."""
        self.overnight_handler = OvernightHandler()
        self.utility_handler = UtilityHandler()
        self.contract_handler = ContractHandler()
        self.onboarding_handler = OnboardingHandler()
        self.message_handler = MessageHandler()
    
    def handle_overnight_commands(self, args) -> bool:
        """Handle overnight autonomous system commands."""
        return self.overnight_handler.handle_overnight_commands(args)
    
    def handle_utility_commands(self, args) -> bool:
        """Handle utility-related commands."""
        return self.utility_handler.handle_utility_commands(args)
    
    def handle_contract_commands(self, args) -> bool:
        """Handle contract-related commands."""
        return self.contract_handler.handle_contract_commands(args)
    
    def handle_onboarding_commands(self, args) -> bool:
        """Handle onboarding-related commands."""
        return self.onboarding_handler.handle_onboarding_commands(args)
    
    def handle_message_commands(self, args) -> bool:
        """Handle message-related commands."""
        return self.message_handler.handle_message_commands(args)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "overnight": self.overnight_handler.get_cycle_status(),
            "utility": self.utility_handler.get_utility_status(),
            "contract": self.contract_handler.get_contract_status(),
            "onboarding": self.onboarding_handler.get_onboarding_status(),
            "message": self.message_handler.get_message_status()
        }
    
    def reset_all_handlers(self):
        """Reset all handlers to initial state."""
        self.overnight_handler.reset_cycle()
        self.utility_handler.clear_history()
        self.contract_handler.reset_contracts()
        self.onboarding_handler.reset_onboarding()
        self.message_handler.reset_stats()
    
    def get_handler_metrics(self) -> Dict[str, Any]:
        """Get metrics from all handlers."""
        return {
            "overnight_cycles": self.overnight_handler.cycle_count,
            "utility_agents": len(self.utility_handler.list_agents()),
            "contract_tasks": self.contract_handler.get_contract_metrics(),
            "onboarded_agents": len(self.onboarding_handler.get_onboarded_agents()),
            "message_stats": self.message_handler.get_message_stats()
        }


# Global instance for backward compatibility
_handlers = MessagingCLIHandlers()

def handle_overnight_commands(args):
    """Handle overnight autonomous system commands."""
    return _handlers.handle_overnight_commands(args)

def handle_utility_commands(args):
    """Handle utility-related commands."""
    return _handlers.handle_utility_commands(args)

def handle_contract_commands(args):
    """Handle contract-related commands."""
    return _handlers.handle_contract_commands(args)

def handle_onboarding_commands(args):
    """Handle onboarding-related commands."""
    return _handlers.handle_onboarding_commands(args)

def handle_message_commands(args):
    """Handle message-related commands."""
    return _handlers.handle_message_commands(args)

def get_messaging_cli_handlers():
    """Get messaging CLI handlers instance."""
    return _handlers
