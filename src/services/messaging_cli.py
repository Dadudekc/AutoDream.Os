#!/usr/bin/env python3
"""
CLI Interface for Unified Messaging Service - Agent Cellphone V2
============================================================

Command-line interface for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import argparse
import sys
import os
import yaml
import uuid
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from .models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_core import UnifiedMessagingCore
from .contract_service import ContractService
from .cli_validator import CLIValidator, ValidationError, create_enhanced_parser, validate_and_parse_args
from ..core.file_lock import LockConfig


def load_config_with_precedence() -> Dict[str, Any]:
    """Load configuration with precedence: CLI → ENV → YAML → defaults."""
    config = {
        "sender": "Captain Agent-4",
        "mode": "pyautogui",
        "new_tab_method": "ctrl_t",
        "priority": "regular",
        "paste": True,
        "onboarding_style": "friendly"
    }

    # Load from YAML config file (lowest precedence)
    config_file = Path("config/messaging.yml")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config and 'defaults' in yaml_config:
                    config.update(yaml_config['defaults'])
        except Exception:
            # Silently ignore YAML errors
            pass

    # Override with environment variables (medium precedence)
    env_mappings = {
        "AC_SENDER": "sender",
        "AC_MODE": "mode",
        "AC_NEW_TAB_METHOD": "new_tab_method",
        "AC_PRIORITY": "priority",
        "AC_ONBOARDING_STYLE": "onboarding_style"
    }

    for env_var, config_key in env_mappings.items():
        env_value = os.getenv(env_var)
        if env_value:
            config[config_key] = env_value

    return config

def create_parser():
    """Create legacy parser for backward compatibility."""
    return create_enhanced_parser()


def handle_utility_commands(args, service):
    """Handle utility commands that don't require message content."""
    if args.list_agents:
        service.list_agents()
        return True

    if args.coordinates:
        service.show_coordinates()
        return True

    if args.history:
        service.show_message_history()
        return True

    # Queue management commands
    if args.queue_stats:
        return handle_queue_stats(service)
    if args.process_queue:
        return handle_process_queue(service)
    if args.start_queue_processor:
        return handle_start_queue_processor(service)
    if args.stop_queue_processor:
        return handle_stop_queue_processor(service)

    return False


def handle_queue_stats(service):
    """Handle queue-stats command."""
    print("📊 MESSAGE QUEUE STATISTICS")
    print("=" * 50)

    try:
        stats = service.get_queue_stats()

        print(f"📋 Pending Messages: {stats.get('pending_count', 0)}")
        print(f"⚙️  Processing Messages: {stats.get('processing_count', 0)}")
        print(f"✅ Delivered Messages: {stats.get('delivered_count', 0)}")
        print(f"❌ Failed Messages: {stats.get('failed_count', 0)}")
        print(f"📊 Total Messages: {stats.get('total_count', 0)}")

        if stats.get('oldest_pending'):
            print(f"⏰ Oldest Pending: {stats['oldest_pending']}")
        if stats.get('newest_pending'):
            print(f"🆕 Newest Pending: {stats['newest_pending']}")

        print("\n📁 Queue Directory: message_queue/")
        print("🔄 Processing Batch Size: 10 messages")
        print("⏳ Retry Delay: 1-300 seconds (exponential backoff)")

    except Exception as e:
        print(f"❌ Error retrieving queue statistics: {e}")

    return True


def handle_process_queue(service):
    """Handle process-queue command."""
    print("🔄 PROCESSING QUEUE BATCH")
    print("=" * 30)

    try:
        processed = service.process_queue_batch()
        print(f"✅ Processed {processed} messages from queue")

        if processed > 0:
            print("📊 Updated queue statistics:")
            stats = service.get_queue_stats()
            print(f"  📋 Pending: {stats.get('pending_count', 0)}")
            print(f"  ⚙️  Processing: {stats.get('processing_count', 0)}")
            print(f"  ✅ Delivered: {stats.get('delivered_count', 0)}")
            print(f"  ❌ Failed: {stats.get('failed_count', 0)}")
        else:
            print("📋 No messages to process (queue empty)")

    except Exception as e:
        print(f"❌ Error processing queue: {e}")

    return True


def handle_start_queue_processor(service):
    """Handle start-queue-processor command."""
    print("🚀 STARTING QUEUE PROCESSOR")
    print("=" * 30)

    try:
        service.start_queue_processor()
        print("✅ Queue processor started successfully")
        print("🔄 Processor will run in background")
        print("📊 Processing 10 messages per batch")
        print("⏱️  Cleanup every hour")

    except Exception as e:
        print(f"❌ Error starting queue processor: {e}")

    return True


def handle_stop_queue_processor(service):
    """Handle stop-queue-processor command."""
    print("🛑 STOPPING QUEUE PROCESSOR")
    print("=" * 30)

    try:
        service.stop_queue_processor()
        print("✅ Queue processor stopped successfully")

    except Exception as e:
        print(f"❌ Error stopping queue processor: {e}")

    return True


def handle_contract_commands(args):
    """Handle contract system commands."""
    if args.get_next_task:
        return handle_get_next_task(args)
    elif args.check_status:
        return handle_check_status()
    return False


def handle_get_next_task(args):
    """Handle get-next-task command with contract assignment."""
    if not args.agent:
        print("❌ ERROR: --agent is required with --get-next-task")
        print("Usage: python -m src.services.messaging_cli --agent Agent-X --get-next-task")
        sys.exit(1)

    print(f"🎯 CONTRACT TASK ASSIGNMENT - {args.agent}")
    print("=" * 50)

    contract_service = get_contract_service()
    contract = contract_service.get_contract(args.agent)

    if contract:
        contract_service.display_contract_assignment(args.agent, contract)
    else:
        contracts = contract_service.contracts
        print(f"❌ ERROR: No contracts available for {args.agent}")
        print("Available agents: " + ", ".join(contracts.keys()))
    return True


def get_contract_service():
    """Get initialized contract service with file locking."""
    # Use same lock configuration as messaging core
    lock_config = LockConfig(
        timeout_seconds=30.0,
        retry_interval=0.1,
        max_retries=300,
        cleanup_interval=60.0,
        stale_lock_age=300.0
    )
    return ContractService(lock_config)


def handle_check_status():
    """Handle check-status command."""
    contract_service = get_contract_service()
    contract_service.check_agent_status()
    return True


def handle_onboarding_commands(args, service):
    """Handle onboarding-related commands."""
    if args.onboarding:
        # Delegate to core bulk onboarding using SSOT template
        service.send_bulk_onboarding(style=args.onboarding_style, mode=args.mode, new_tab_method=args.new_tab_method)
        return True

    if args.onboard:
        if not args.agent:
            print("❌ ERROR: --agent is required with --onboard")
            print("Usage: python -m src.services.messaging_cli --onboard --agent Agent-X [--onboarding-style friendly|professional] [--mode inbox|pyautogui]")
            sys.exit(1)
        service.send_onboarding_message(agent_id=args.agent, style=args.onboarding_style, mode=args.mode, new_tab_method=args.new_tab_method)
        return True

    if args.wrapup:
        return handle_wrapup_command(args, service)

    return False


def handle_wrapup_command(args, service):
    """Handle wrapup command."""
    print("🏁 WRAPUP SEQUENCE ACTIVATED")
    wrapup_content = """🚨 **CAPTAIN AGENT-4 - AGENT ACTIVATION & WRAPUP** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Status**: Agent activation and system wrapup
**Mode**: Optimized workflow with Ctrl+T

**AGENT ACTIVATION**:
- ✅ **New Tab Created**: Ready for agent input
- ✅ **System Integration**: Messaging system optimized
- ✅ **Contract System**: 40+ contracts available
- ✅ **Coordination**: PyAutoGUI messaging active

**READY FOR**: Agent response and task assignment

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""

    service.send_to_all_agents(
        content=wrapup_content,
        sender="Captain Agent-4",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.WRAPUP],
        mode=args.mode,
        use_paste=True,
    )
    return True


def handle_message_commands(args, service):
    """Handle regular message sending commands."""
    # Check if message is required for sending
    if not args.message:
        print("❌ ERROR: --message/-m is required for sending messages")
        print("Use --list-agents, --coordinates, --history, --onboarding, --onboard, or --wrapup for utility commands")
        sys.exit(1)

    # Determine message type and priority
    message_type = UnifiedMessageType(args.type)
    priority = UnifiedMessagePriority.URGENT if args.high_priority else UnifiedMessagePriority(args.priority)

    # Determine paste mode and new tab method
    use_paste = not args.no_paste
    new_tab_method = args.new_tab_method

    # Send message
    if args.bulk:
        # Send to all agents
        service.send_to_all_agents(
            content=args.message,
            sender=args.sender,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
            new_tab_method=new_tab_method,
            use_new_tab=False,  # Regular messages don't create new tabs
        )
    elif args.agent:
        # Send to specific agent
        service.send_message(
            content=args.message,
            sender=args.sender,
            recipient=args.agent,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
            new_tab_method=new_tab_method,
            use_new_tab=False,  # Regular messages don't create new tabs
        )
    else:
        print("❌ ERROR: Must specify --agent or --bulk")
        sys.exit(1)


def main():
    """Main CLI entry point with comprehensive validation."""
    try:
        # Parse and validate arguments
        args, validator = validate_and_parse_args()

        # Load configuration with precedence
        config = load_config_with_precedence()

        # Apply configuration defaults if not overridden by CLI
        if not getattr(args, 'sender', None) and 'sender' in config:
            args.sender = config['sender']
        if not getattr(args, 'mode', None) and 'mode' in config:
            args.mode = config['mode']
        if not getattr(args, 'new_tab_method', None) and 'new_tab_method' in config:
            args.new_tab_method = config['new_tab_method']
        if not getattr(args, 'priority', None) and 'priority' in config:
            args.priority = config['priority']
        if not getattr(args, 'onboarding_style', None) and 'onboarding_style' in config:
            args.onboarding_style = config['onboarding_style']

        # Initialize messaging service
        service = UnifiedMessagingCore()

        # Handle commands in priority order
        if handle_utility_commands(args, service):
            return
        if handle_contract_commands(args):
            return
        if handle_onboarding_commands(args, service):
            return

        # Handle message commands (requires --message)
        handle_message_commands(args, service)

    except SystemExit as e:
        # Re-raise SystemExit to maintain exit codes
        sys.exit(e.code)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        # Handle unexpected errors
        error = ValidationError(
            code=CLIValidator.EXIT_INTERNAL_ERROR,
            message="Unexpected error in CLI execution",
            hint="Check logs with correlation ID",
            correlation_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            details={"exception": str(e)}
        )
        validator = CLIValidator()
        validator.exit_with_error(error)


if __name__ == "__main__":
    main()
