"""Messaging-related handler functions separated from command handler."""

from __future__ import annotations

import argparse
import logging

from ..interfaces import MessagingMode, MessageType
from ..config import DEFAULT_COORDINATE_MODE, AGENT_COUNT, CAPTAIN_ID
from ..contract_system_manager import ContractSystemManager
from ..error_handler import ErrorHandler
from ..prompt_loader import PromptLoader
# Message queue system is now consolidated into UnifiedMessagingService

logger = logging.getLogger(__name__)


class MessagingHandlers:
    """Encapsulates messaging operations for the CLI."""

    def __init__(self, service, formatter) -> None:
        self.service = service
        self.formatter = formatter
        self.contract_manager = ContractSystemManager()
        self.prompt_loader = PromptLoader()

    def message(self, args: argparse.Namespace, mode: MessagingMode) -> bool:
        """Route message commands based on arguments."""
        message_type = MessageType(args.type)
        if args.bulk:
            return self.bulk_messaging(args, mode, message_type)
        if args.campaign:
            return self.campaign_messaging(args)
        if args.yolo:
            return self.yolo_messaging(args)
        if args.agent:
            return self.single_agent_messaging(args, mode, message_type)
        print("❌ No message operation specified. Use --help for options.")
        return False

    def onboarding(self, args: argparse.Namespace) -> bool:
        """Handle onboarding messages."""
        return ErrorHandler.safe_execute(
            "Onboarding", logger, self._onboarding_internal, args
        )

    def _onboarding_internal(self, args: argparse.Namespace) -> bool:
        """Generate comprehensive onboarding messages with agent identity and responsibilities"""
        contracts = self.contract_manager.list_available_contracts()
        messages: dict[str, str] = {}
        
        for i in range(1, AGENT_COUNT + 1):
            agent_id = f"Agent-{i}"
            
            # Determine agent role and responsibilities
            if agent_id == "Agent-4":  # Captain
                base = self._generate_captain_onboarding(agent_id, args.message)
            else:  # Regular agents
                base = self._generate_agent_onboarding(agent_id, i, contracts, args.message)
            
            messages[agent_id] = base
        
        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, MessageType.ONBOARDING_START, True
        )
        self.formatter.generic_results("📊 Onboarding Results:", results)
        return True
    
    def _generate_captain_onboarding(self, agent_id: str, custom_message: str = None) -> str:
        """Generate comprehensive onboarding message for Captain (Agent-4)"""
        return self.prompt_loader.load_captain_onboarding(agent_id, custom_message)
    
    def _generate_agent_onboarding(self, agent_id: str, agent_number: int, contracts: list, custom_message: str = None) -> str:
        """Generate comprehensive onboarding message for regular agents"""
        
        # Get assigned contract if available
        contract_info = ""
        if agent_number - 1 < len(contracts):
            c = contracts[agent_number - 1]
            contract_info = f"{c['contract_id']}: {c['title']}"
        
        return self.prompt_loader.load_agent_onboarding(agent_id, agent_number, contract_info, custom_message)

    def _send_comprehensive_onboarding(self, args: argparse.Namespace) -> bool:
        """Send comprehensive onboarding messages to all agents with identity and responsibilities"""
        try:
            print("🚀 **COMPREHENSIVE ONBOARDING INITIATED**")
            print("📋 Generating agent-specific onboarding messages...")
            
            # Use the same comprehensive onboarding logic
            contracts = self.contract_manager.list_available_contracts()
            messages: dict[str, str] = {}
            
            for i in range(1, AGENT_COUNT + 1):
                agent_id = f"Agent-{i}"
                
                # Determine agent role and responsibilities
                if agent_id == "Agent-4":  # Captain
                    base = self._generate_captain_onboarding(agent_id, args.message)
                else:  # Regular agents
                    base = self._generate_agent_onboarding(agent_id, i, contracts, args.message)
                
                messages[agent_id] = base
                print(f"✅ {agent_id}: {agent_id.split('-')[1]} onboarding message generated")
            
            print("📤 Sending comprehensive onboarding messages to all agents...")
            results = self.service.send_bulk_messages(
                messages, DEFAULT_COORDINATE_MODE, MessageType.ONBOARDING_START, True
            )
            
            if results:
                print("✅ **COMPREHENSIVE ONBOARDING COMPLETED SUCCESSFULLY!**")
                print("🎯 All agents now know their identity, role, and responsibilities!")
                return True
            else:
                print("❌ **COMPREHENSIVE ONBOARDING FAILED!**")
                return False
                
        except Exception as e:
            print(f"❌ Error in comprehensive onboarding: {e}")
            return False

    def captain_message(self, args: argparse.Namespace) -> bool:
        """Handle captain message."""
        return ErrorHandler.safe_execute(
            "Captain message", logger, self._captain_message_internal, args
        )

    def _captain_message_internal(self, args: argparse.Namespace) -> bool:
        content = args.message or "Hello Captain"
        success = self.service.send_message(
            CAPTAIN_ID, content, MessageType(args.type), self.service.active_mode
        )
        print("✅ Captain message sent" if success else "❌ Captain message failed")
        return success

    def resume_system(self, args: argparse.Namespace) -> bool:
        """Handle system resume."""
        return ErrorHandler.safe_execute(
            "System resume", logger, self._resume_system_internal, args
        )

    def _resume_system_internal(self, args: argparse.Namespace) -> bool:
        content = args.message or "Resuming system operations"
        messages = {f"Agent-{i}": content for i in range(1, AGENT_COUNT + 1)}
        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, MessageType.TEXT, False
        )
        self.formatter.generic_results("📊 Resume Results:", results)
        return True

    def resume_captain(self, args: argparse.Namespace) -> bool:
        """Handle captain resume."""
        return ErrorHandler.safe_execute(
            "Captain resume", logger, self._resume_captain_internal, args
        )

    def _resume_captain_internal(self, args: argparse.Namespace) -> bool:
        content = args.message or "Captain, please resume oversight"
        success = self.service.send_message(
            CAPTAIN_ID, content, MessageType.TEXT, self.service.active_mode
        )
        print("✅ Captain resume message sent" if success else "❌ Captain resume failed")
        return success

    def resume_agents(self, args: argparse.Namespace) -> bool:
        """Handle agents resume."""
        return ErrorHandler.safe_execute(
            "Agents resume", logger, self._resume_agents_internal, args
        )

    def _resume_agents_internal(self, args: argparse.Namespace) -> bool:
        content = args.message or "Agents, resume your workflows"
        messages = {
            f"Agent-{i}": content
            for i in range(1, AGENT_COUNT + 1)
            if f"Agent-{i}" != CAPTAIN_ID
        }
        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, MessageType.TEXT, False
        )
        self.formatter.generic_results("📊 Agent Resume Results:", results)
        return True

    def status_check(self) -> bool:
        """Handle status check."""
        return ErrorHandler.safe_execute(
            "Status check", logger, self._status_check_internal
        )

    def _status_check_internal(self) -> bool:
        """Check status using the unified messaging service"""
        try:
            # Get status from the unified service
            statuses = self.service.get_all_agent_statuses()
            print("📊 **AGENT STATUS CHECK**")
            print("=" * 40)
            
            for agent_id, state in statuses.items():
                status_emoji = {
                    "idle": "🟡",
                    "working": "🟢", 
                    "waiting": "🟠",
                    "completed": "✅",
                    "error": "🔴"
                }.get(state.status.value, "❓")
                
                print(f"{status_emoji} {agent_id}: {state.status.value}")
                if state.current_task:
                    print(f"   📋 Task: {state.current_task}")
                if state.last_activity:
                    import time
                    time_since = time.time() - state.last_activity
                    print(f"   ⏰ Last Activity: {time_since:.1f}s ago")
            
            return True
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return False

    def bulk_messaging(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        """Send a message to all agents."""
        return ErrorHandler.safe_execute(
            "Bulk messaging", logger, self._bulk_messaging_internal, args, mode, message_type
        )

    def _bulk_messaging_internal(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        print(f"📡 Bulk messaging to all agents via {mode.value}...")

        # Check if this is onboarding - if so, use comprehensive onboarding messages
        if args.onboarding:
            print("🚀 COMPREHENSIVE ONBOARDING messages detected - using agent identity and responsibility messages!")
            return self._send_comprehensive_onboarding(args)
        
        # Regular bulk messaging
        messages = {f"Agent-{i}": args.message for i in range(1, AGENT_COUNT + 1)}

        new_chat = False
        if args.new_chat:
            new_chat = True
            print("🆕 NEW CHAT messages detected - using new chat sequence!")

        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, message_type, new_chat
        )

        if results:
            print("✅ Bulk messaging completed successfully")
            return True
        print("❌ Bulk messaging failed")
        return False

    def campaign_messaging(self, args: argparse.Namespace) -> bool:
        """Handle campaign messaging."""
        return ErrorHandler.safe_execute(
            "Campaign messaging", logger, self._campaign_messaging_internal, args
        )

    def _campaign_messaging_internal(self, args: argparse.Namespace) -> bool:
        results = self.service.send_campaign_message(args.message)
        self.formatter.generic_results("📊 Campaign Results:", results)
        return True

    def yolo_messaging(self, args: argparse.Namespace) -> bool:
        """Handle YOLO messaging."""
        return ErrorHandler.safe_execute(
            "YOLO messaging", logger, self._yolo_messaging_internal, args
        )

    def _yolo_messaging_internal(self, args: argparse.Namespace) -> bool:
        results = self.service.activate_yolo_mode(args.message)
        self.formatter.generic_results("📊 YOLO Results:", results)
        return True

    def single_agent_messaging(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        """Send a message to a single agent."""
        return ErrorHandler.safe_execute(
            "Agent messaging",
            logger,
            self._single_agent_messaging_internal,
            args,
            mode,
            message_type,
        )

    def _single_agent_messaging_internal(
        self, args: argparse.Namespace, mode: MessagingMode, message_type: MessageType
    ) -> bool:
        print(f"🤖 Agent messaging via {mode.value}...")
        coord_mode = getattr(args, "coordinate_mode", DEFAULT_COORDINATE_MODE)
        validation = self.service.validate_agent_coordinates(args.agent, coord_mode)
        if not validation.get("valid", False):
            print(
                f"❌ Coordinate validation failed for {args.agent}: {validation.get('error')}"
            )
            return False

        if args.high_priority:
            message_type = MessageType.HIGH_PRIORITY

        new_chat = args.onboarding or args.new_chat
        success = self.service.send_message(
            args.agent, args.message, message_type, mode, new_chat
        )
        print("✅ Agent message sent" if success else "❌ Agent message failed")
        return success
