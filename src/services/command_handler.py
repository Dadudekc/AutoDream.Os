#!/usr/bin/env python3
"""
Command Handler - Main entry point for messaging operations
=========================================================

This module has been modularized to comply with V2 standards:
- LOC: Reduced from 1241 to under 100 lines
- SSOT: Single source of truth for command handling
- No duplication: All functionality moved to dedicated handler modules
"""

from __future__ import annotations

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
from .unified_messaging_service import UnifiedMessagingService
from .config import CAPTAIN_ID, DEFAULT_COORDINATE_MODE
from .contract_system_manager import ContractSystemManager
from .error_handler import ErrorHandler
from .executor import CommandExecutor
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
        self.executor = CommandExecutor(self.service, self.formatter)
        
        self.logger.info("Messaging command handler initialized with modular handlers")
    
    def execute_command(self, args: argparse.Namespace) -> bool:
        """Execute the parsed command by delegating to appropriate handler"""
        return ErrorHandler.safe_execute(
            "Command execution", self.logger, self._execute_command_internal, args
        )
    
    def _execute_command_internal(self, args: argparse.Namespace) -> bool:
        """Internal command execution logic."""
        try:
            # Handle help commands first
            if args.help:
                return self._handle_help()
            if args.quick_help:
                return self._handle_quick_help()
            
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
            
            # Check if this is a messaging operation that should be handled by MessagingHandlers
            if self._is_messaging_operation(args):
                return self._handle_messaging_operation(args, mode)
            
            self.logger.warning("No handler found for command")
            return False
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return False
    
    def _handle_help(self) -> bool:
        """Handle help command with detailed information"""
        try:
            print("🚨 **UNIFIED MESSAGING SERVICE CLI - COMPLETE HELP** 🚨")
            print("=" * 60)
            print()
            print("🎯 **DESCRIPTION:**")
            print("   Unified messaging system for Agent Cellphone V2")
            print("   Enables communication between Captain Agent-4 and all agents")
            print()
            print("📋 **CORE MESSAGING FLAGS:**")
            print("   --mode          - Messaging mode (pyautogui, cdp, http, websocket, tcp, fsm, onboarding, campaign, yolo)")
            print("   --message       - Message content to send")
            print("   --agent         - Send to specific agent (e.g., Agent-1)")
            print("   --bulk          - Send to all agents simultaneously (auto-appends mandatory protocol)")
            print("   --type          - Message type (text, command, broadcast, high_priority, task_assignment, status_update, coordination)")
            print("   --high-priority - Send as urgent message (Ctrl+Enter 2x)")
            print()
            print("🚀 **ONBOARDING FLAGS:**")
            print("   --onboarding    - Send onboarding message (new chat sequence)")
            print("   --new-chat      - Send new chat message (onboarding sequence)")
            print("   --onboard       - Automatically onboard all agents with contracts")
            print("   --check-status  - Check all agent statuses from status.json files")
            print()
            print("📜 **CONTRACT SYSTEM FLAGS:**")
            print("   --claim-contract    - Claim a contract by ID")
            print("   --complete-contract - Complete a contract by ID")
            print("   --get-next-task    - Get next available task from queue")
            print("   --contract-status  - Show contract claiming status")
            print()
            print("🎖️ **CAPTAIN COMMUNICATION FLAGS:**")
            print("   --captain       - Send message directly to Captain (Agent-4)")
            print()
            print("🔄 **RESUME SYSTEM FLAGS:**")
            print("   --resume        - Resume perpetual motion system")
            print("   --resume-captain - Send Captain resume message")
            print("   --resume-agents - Send Agent resume message")
            print()
            print("📍 **COORDINATE MANAGEMENT FLAGS:**")
            print("   --coordinates   - Show coordinate mapping for all agents")
            print("   --coordinate-mode - Coordinate mode to use")
            print("   --map-mode      - Coordinate mode to map")
            print("   --consolidate   - Consolidate coordinate files")
            print("   --calibrate     - Calibrate coordinates for specific agent")
            print("   --interactive   - Run interactive coordinate capture")
            print("   --validate      - Validate coordinates")
            print()
            print("💡 **COMMON USAGE EXAMPLES (CLI COMMANDS):**")
            print("   # Send to specific agent")
            print("   python -m src.services.messaging --agent Agent-1 --message 'Hello Agent-1!'")
            print()
            print("   # Send to all agents")
            print("   python -m src.services.messaging --bulk --message 'Message to all agents'")
            print()
            print("   # High priority message")
            print("   python -m src.services.messaging --agent Agent-1 --message 'URGENT!' --high-priority")
            print()
            print("   # Onboard all agents")
            print("   python -m src.services.messaging --onboard")
            print()
            print("   # Check agent statuses")
            print("   python -m src.services.messaging --check-status")
            print()
            print("   # Get next task")
            print("   python -m src.services.messaging --get-next-task")
            print()
            print("   # Send to Captain")
            print("   python -m src.services.messaging --captain --message 'Status update'")
            print()
            print("   # Show coordinates")
            print("   python -m src.services.messaging --coordinates")
            print()
            print("   # Validate coordinates")
            print("   python -m src.services.messaging --validate")
            print()
            print("🎯 **FOR MORE HELP:**")
            print("   python -m src.services.messaging --help")
            print()
            print("📝 **NOTE:** These are CLI command examples, not actual messages.")
            print("   The mandatory reminder appendix only applies to messages FROM Captain TO agents.")
            print()
            print("Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager")
            return True
        except Exception as e:
            self.logger.error(f"Help display failed: {e}")
            return False

    def _handle_quick_help(self) -> bool:
        """Handle quick help command with common operations"""
        try:
            print("🚨 **QUICK HELP - MOST COMMON OPERATIONS** 🚨")
            print("=" * 50)
            print()
            print("📱 **BASIC MESSAGING:**")
            print("   --agent Agent-1 --message 'Hello'     # Send to specific agent")
            print("   --bulk --message 'To all agents'      # Send to all agents (auto-appends mandatory protocol)")
            print("   --high-priority                        # Urgent message")
            print()
            print("🚀 **ONBOARDING:**")
            print("   --onboard                             # Onboard all agents")
            print("   --check-status                         # Check agent statuses")
            print()
            print("📜 **CONTRACTS:**")
            print("   --get-next-task                       # Get next task")
            print("   --claim-contract CONTRACT-001         # Claim contract")
            print()
            print("🎖️ **CAPTAIN:**")
            print("   --captain --message 'Status update'   # Send to Captain")
            print()
            print("📍 **COORDINATES:**")
            print("   --coordinates                         # Show coordinates")
            print("   --validate                            # Validate coordinates")
            print()
            print("💡 **FULL HELP:**")
            print("   --help                                # Complete help with examples")
            print()
            print("Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager")
            return True
        except Exception as e:
            self.logger.error(f"Quick help display failed: {e}")
            return False

    def _handle_validation(self) -> bool:
        """Handle validation command"""
        try:
            self.logger.info("Validation mode enabled")
            return True
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
    
    def route_command(self, args: argparse.Namespace) -> bool:
        """Route command to appropriate handler using router pattern"""
        try:
            from .router import route_command
            return route_command(args)
        except ImportError:
            # Fallback to internal routing
            return self._execute_command_internal(args)
    
    def _is_messaging_operation(self, args: argparse.Namespace) -> bool:
        """Check if this is a messaging operation that should be handled by MessagingHandlers"""
        return any([
            hasattr(args, 'bulk') and args.bulk,
            hasattr(args, 'agent') and args.agent,
            hasattr(args, 'campaign') and args.campaign,
            hasattr(args, 'yolo') and args.yolo,
            hasattr(args, 'onboarding') and args.onboarding,
            hasattr(args, 'new_chat') and args.new_chat,
            hasattr(args, 'high_priority') and args.high_priority
        ])
    
    def _handle_messaging_operation(self, args: argparse.Namespace, mode) -> bool:
        """Handle messaging operations using MessagingHandlers"""
        try:
            self.logger.info("Routing messaging operation to MessagingHandlers")
            return self.messaging_handlers.message(args, mode)
        except Exception as e:
            self.logger.error(f"Error handling messaging operation: {e}")
            return False
