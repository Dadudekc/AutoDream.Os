#!/usr/bin/env python3
"""
Command Handlers for Messaging CLI - Agent Cellphone V2
======================================================

Command handling logic for the messaging CLI service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
from typing import Any

from .models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .contract_service import ContractService
from ..core.file_lock import LockConfig


def handle_utility_commands(args, service) -> bool:
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


def handle_queue_stats(service) -> bool:
    """Handle queue statistics command."""
    try:
        stats = service.get_queue_stats()
        print("📊 MESSAGE QUEUE STATISTICS")
        print("=" * 30)
        print(f"Total messages: {stats.get('total', 0)}")
        print(f"Pending messages: {stats.get('pending', 0)}")
        print(f"Processed messages: {stats.get('processed', 0)}")
        print(f"Failed messages: {stats.get('failed', 0)}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to get queue stats: {e}")
        return False


def handle_process_queue(service) -> bool:
    """Handle process queue command."""
    try:
        processed = service.process_message_queue()
        print(f"✅ Processed {processed} messages from queue")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to process queue: {e}")
        return False


def handle_start_queue_processor(service) -> bool:
    """Handle start queue processor command."""
    try:
        service.start_queue_processor()
        print("✅ Queue processor started")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to start queue processor: {e}")
        return False


def handle_stop_queue_processor(service) -> bool:
    """Handle stop queue processor command."""
    try:
        service.stop_queue_processor()
        print("✅ Queue processor stopped")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to stop queue processor: {e}")
        return False


def handle_contract_commands(args) -> bool:
    """Handle contract-related commands."""
    if args.get_next_task:
        return handle_get_next_task(args)
    
    if args.check_status:
        return handle_check_status()
    
    return False


def handle_get_next_task(args) -> bool:
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


def handle_check_status() -> bool:
    """Handle check-status command."""
    contract_service = get_contract_service()
    contract_service.check_agent_status()
    return True


def handle_onboarding_commands(args, service) -> bool:
    """Handle onboarding-related commands."""
    if args.compliance_mode:
        return handle_compliance_mode_onboarding(args, service)

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


def handle_compliance_mode_onboarding(args, service) -> bool:
    """Handle compliance mode onboarding for autonomous development."""
    print("🎯 AUTONOMOUS DEVELOPMENT COMPLIANCE MODE ACTIVATED")
    print("=" * 60)
    
    compliance_content = """🚨 **AUTONOMOUS DEVELOPMENT COMPLIANCE MODE ACTIVATED** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Mode**: AUTONOMOUS DEVELOPMENT - COMPLIANCE PROTOCOL ACTIVATED
**Priority**: HIGH - Technical Debt Elimination & V2 Standards Implementation

🎯 **AUTONOMOUS DEVELOPMENT PROTOCOLS**:
- ✅ **Equally Capable Agents**: All agents are equally capable across domains
- ✅ **Captain Assignment**: Captain can assign any open agent to any task
- ✅ **Discord Devlog**: Mandatory progress reporting via devlog system
- ✅ **Inbox Monitoring**: Check agent_workspaces/<Agent-X>/inbox/ regularly
- ✅ **System Utilization**: Full utilization of swarm coordination system

🔧 **COMPLIANCE MODE OBJECTIVES**:
- ✅ **Technical Debt Elimination**: Zero tolerance for code duplication and monoliths
- ✅ **V2 Standards Implementation**: Domain-specific compliance (Python 300-line limit vs JavaScript standards)
- ✅ **8x Efficiency**: Maintain optimized workflow throughout all operations
- ✅ **Modular Architecture**: Repository pattern, DI, clean separation of concerns
- ✅ **Cross-Agent Validation**: Support and validate other agents' work

📊 **OPERATIONAL REQUIREMENTS**:
- ✅ **Check Inbox FIRST**: Always review inbox before responding to Captain
- ✅ **Report Progress**: Use devlog system for all updates
- ✅ **Claim Contracts**: Use --get-next-task to claim available work
- ✅ **Coordinate**: Support other agents in their compliance efforts
- ✅ **Validate**: Ensure all deliverables meet V2 compliance standards

🚨 **IMMEDIATE ACTIONS**:
1. Check your agent_workspaces/<Agent-ID>/inbox/ for messages
2. Update your status.json with current mission and progress
3. Claim next available contract with --get-next-task
4. Report readiness and current compliance status
5. Begin autonomous technical debt elimination

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**
**Status**: Monitoring autonomous development compliance across all agents
**Expectation**: Proactive, autonomous, and efficient V2 compliance achievement

**WE. ARE. SWARM.** ⚡️🔥"""

    print("📨 Sending compliance mode onboarding to all agents...")
    
    service.send_to_all_agents(
        content=compliance_content,
        sender="Captain Agent-4",
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
        mode=args.mode,
        new_tab_method=args.new_tab_method
    )
    
    print("✅ COMPLIANCE MODE ONBOARDING COMPLETE")
    print("🎯 All agents now configured for autonomous development with compliance protocols")
    return True


def handle_wrapup_command(args, service) -> bool:
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


def handle_message_commands(args, service) -> bool:
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
        )
    else:
        # Send to specific agent
        if not args.agent:
            print("❌ ERROR: --agent/-a is required for single agent messaging")
            print("Use --bulk for sending to all agents")
            sys.exit(1)
        
        service.send_message(
            content=args.message,
            recipient=args.agent,
            sender=args.sender,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_paste=use_paste,
            new_tab_method=new_tab_method,
        )
    
    return True
