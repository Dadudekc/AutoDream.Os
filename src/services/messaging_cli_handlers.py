#!/usr/bin/env python3
"""
Messaging CLI Handlers - V2 Compliant Refactored
=================================================

V2 compliance redirect to modular messaging CLI handlers system.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: V2 compliant modular messaging CLI handlers
"""

# V2 COMPLIANCE REDIRECT - see refactored modular system
from .handlers.messaging_cli_handlers import MessagingCLIHandlers, handle_contract_commands, handle_message_commands, handle_utility_commands, handle_onboarding_commands, handle_overnight_commands

# Backward compatibility - re-export everything
__all__ = ['MessagingCLIHandlers', 'handle_contract_commands', 'handle_message_commands', 'handle_utility_commands', 'handle_onboarding_commands', 'handle_overnight_commands']
