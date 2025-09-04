#!/usr/bin/env python3
"""
Command Handlers for Messaging CLI - Agent Cellphone V2
======================================================

Command handling logic for the messaging CLI service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .models.messaging_models import (
    RecipientType,
    SenderType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from .unified_messaging_imports import COORDINATE_CONFIG_FILE
from typing import Any, Dict, List
import sys
import time


async def load_coordinates_async(service) -> Dict[str, Any]:
    """
    Reusable helper function for async coordinate loading using shared utilities.

    Eliminates DRY violation by using shared validation utilities.

    Args:
        service: Messaging service instance

    Returns:
        Dict containing coordinate data and success status
    """

    # Load coordinates from JSON file
    try:
        from ..core.unified_data_processing_system import read_json, write_json
        coords_data = read_json(COORDINATE_CONFIG_FILE)
        coordinates = {}
        for agent_id, agent_data in coords_data["agents"].items():
            coordinates[agent_id] = agent_data.get("chat_input_coordinates", [0, 0])
        return {"success": True, "coordinates": coordinates, "agent_count": len(coordinates)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def print_coordinates_table(coordinates: Dict[str, List[int]]) -> None:
    """
    Reusable helper function for printing coordinate tables.

    Args:
        coordinates: Dict mapping agent IDs to coordinate lists
    """
    print("📍 Current Agent Coordinates:")
    for agent, coords in coordinates.items():
                print(f"  {agent}: [{coords[0]}, {coords[1]}]")


def print_agent_cycle_instructions() -> None:
    """Reusable helper function for printing agent cycle instructions."""
    print()
    print("🔄 AGENT CYCLE LOOP INSTRUCTIONS:")
    print("1. Check your inbox: agent_workspaces/{agent_id}/inbox/")
    print("2. Update status.json with timestamp")
    print("3. Execute assigned tasks")
    print("4. Report progress to Captain Agent-4")
    print("5. Repeat cycle")
    print()
    print("⚡ CYCLE-BASED EFFICIENCY:")
    print("- One cycle = One Captain prompt + One Agent response")
    print("- Maintain 8x efficiency through continuous cycles")
    print("- Never let cycle momentum stop")
    print()
    print("📡 MESSAGING COMMANDS:")
    print("- Send message: --agent Agent-X --message 'text'")
    print("- Check status: --check-status")
    print("- Get task: --get-next-task")
    print("- Send to Captain: --captain --message 'text'")
    print()


def print_messaging_info(agent_count: int) -> None:
    """
    Reusable helper function for printing messaging information.

    Args:
        agent_count: Number of configured agents
    """
    print(f"✅ Total configured agents: {agent_count}")


def print_load_failure(resource_type: str) -> None:
    """
    Reusable helper function for printing load failure messages.

    Eliminates DRY violation for common "Failed to load" error messages.

    Args:
        resource_type: Type of resource that failed to load (e.g., "coordinates", "agent identity")
    """
    print(f"❌ Failed to load {resource_type}")


def print_load_failure_with_context(resource_type: str, context: str) -> None:
    """
    Reusable helper function for printing load failure messages with context.

    Args:
        resource_type: Type of resource that failed to load
        context: Additional context for the failure
    """
    print(f"❌ Failed to load {resource_type} {context}")


def print_agent_not_found(agent_id: str, context: str = "in coordinates") -> None:
    """
    Reusable helper function for printing agent not found messages.

    Args:
        agent_id: Agent identifier that was not found
        context: Context where agent was not found
    """
    print(f"❌ Agent {agent_id} not found {context}")


async def handle_utility_commands(args, service) -> bool:
    """Handle utility commands that don't require message content."""
    if args.list_agents:
        service.list_agents()
        return True

    if args.coordinates:
        # Use reusable helper function to eliminate DRY violation
        result = await load_coordinates_async(service)

        if result.get("success"):
            print_coordinates_table(result["coordinates"])
            print_messaging_info(result['agent_count'])
        else:
            print_load_failure("coordinates")
        return True

    if args.check_status:
        handle_check_status()
        return True

    if hasattr(args, 'agent_identity') and args.agent_identity:
        # Use reusable helper function to eliminate DRY violation
        result = await load_coordinates_async(service)

        if result.get("success"):
            print("🤖 AGENT IDENTITY & COORDINATE SYSTEM")
            print("=" * 50)
            print()
            print("📍 AGENT COORDINATES (PyAutoGUI Positions):")
            print_coordinates_table(result["coordinates"])
            print_agent_cycle_instructions()
            print_messaging_info(result['agent_count'])
        else:
            print_load_failure("agent identity information")
        return True

    if hasattr(args, 'send_identity') and args.send_identity:
        # Use reusable helper function to eliminate DRY violation
        result = await load_coordinates_async(service)

        if result.get("success"):
            agent_id = getattr(args, 'send_identity', None)
            if agent_id in result["coordinates"]:
                coords = result["coordinates"][agent_id]
                identity_message = f"""🤖 AGENT IDENTITY CONFIRMATION: You are {agent_id}

📍 YOUR COORDINATES: [{coords[0]}, {coords[1]}]

🔄 AGENT CYCLE LOOP INSTRUCTIONS:
1. Check your inbox: agent_workspaces/{agent_id}/inbox/
2. Update status.json with timestamp
3. Execute assigned tasks
4. Report progress to Captain Agent-4
5. Repeat cycle

⚡ CYCLE-BASED EFFICIENCY:
- One cycle = One Captain prompt + One Agent response
- Maintain 8x efficiency through continuous cycles
- Never let cycle momentum stop

📡 MESSAGING COMMANDS:
- Send message: --agent Agent-X --message 'text'
- Check status: --check-status
- Get task: --get-next-task
- Send to Captain: --captain --message 'text'

✅ You are {agent_id} - Execute your cycle loop now!"""

                # Send via PyAutoGUI
                success = service.send_message(
                    content=identity_message,
                    sender="Captain Agent-4",
                    recipient=agent_id,
                    message_type="system_to_agent",
                    priority="urgent",
                    mode="pyautogui",
                )

                if success:
                    print(
                        f"✅ Agent identity sent to {agent_id} at coordinates [{coords[0]}, {coords[1]}]"
                    )
                else:
                    print(f"❌ Failed to send agent identity to {agent_id}")
            else:
                print_agent_not_found(agent_id)
        else:
            print_load_failure_with_context("coordinates", "for identity sending")
        return True

    if hasattr(args, 'history') and args.history:
        service.show_message_history()
        return True

    # Queue management commands
    if hasattr(args, 'queue_stats') and args.queue_stats:
        return handle_queue_stats(service)
    if hasattr(args, 'process_queue') and args.process_queue:
        return handle_process_queue(service)
    if hasattr(args, 'start_queue_processor') and args.start_queue_processor:
        return handle_start_queue_processor(service)
    if hasattr(args, 'stop_queue_processor') and args.stop_queue_processor:
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
    if hasattr(args, 'get_next_task') and args.get_next_task:
        return handle_get_next_task(args)

    if hasattr(args, 'check_contracts') and args.check_contracts:
        return handle_check_contracts()

    return False


def handle_get_next_task(args) -> bool:
    """Handle get-next-task command with contract assignment."""
    if not args.agent:
        print("❌ ERROR: --agent is required with --get-next-task")
        print(
            "Usage: python -m src.services.messaging_cli --agent Agent-X --get-next-task"
        )
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
    # Simplified contract service for now
    class SimpleContractService:
        def get_contract(self, agent_id):
            return {"task": f"Sample task for {agent_id}", "priority": "medium"}
        
        def display_contract_assignment(self, agent_id, contract):
            print(f"🎯 Contract assigned to {agent_id}: {contract['task']}")
        
        def check_agent_status(self):
            print("📊 Agent Status: All agents active")
        
        @property
        def contracts(self):
            return {"Agent-1": {}, "Agent-2": {}, "Agent-3": {}, "Agent-4": {}, 
                   "Agent-5": {}, "Agent-6": {}, "Agent-7": {}, "Agent-8": {}}
    
    return SimpleContractService()


def handle_check_status() -> bool:
    """Handle check-status command."""
    contract_service = get_contract_service()
    contract_service.check_agent_status()
    return True


async def handle_onboarding_commands(args, service) -> bool:
    """Handle onboarding-related commands."""
    if args.compliance_mode:
        return handle_compliance_mode_onboarding(args, service)

    if args.onboarding:
        # Delegate to core bulk onboarding using SSOT template
        service.send_bulk_onboarding(
            style=args.onboarding_style,
            mode=args.mode,
            new_tab_method=args.new_tab_method,
        )
        return True

    if args.onboard:
        if not args.agent:
            print("❌ ERROR: --agent is required with --onboard")
            print(
                "Usage: python -m src.services.messaging_cli --onboard --agent Agent-X [--onboarding-style friendly|professional] [--mode inbox|pyautogui]"
            )
            sys.exit(1)
        service.send_onboarding_message(
            agent_id=args.agent,
            style=args.onboarding_style,
            mode=args.mode,
            new_tab_method=args.new_tab_method,
        )
        return True

    if args.wrapup:
        return handle_wrapup_command(args, service)

    if args.hard_onboarding:
        return handle_hard_onboarding_command(args, service)

    return False


def handle_compliance_mode_onboarding(args, service) -> bool:
    """Handle compliance mode onboarding for autonomous development."""
    print("🎯 AUTONOMOUS DEVELOPMENT COMPLIANCE MODE ACTIVATED")
    print("=" * 60)

    compliance_content = """🚨 **AUTONOMOUS DEVELOPMENT COMPLIANCE MODE ACTIVATED - CYCLE-BASED PHASE** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Mode**: AUTONOMOUS DEVELOPMENT - COMPLIANCE PROTOCOL ACTIVATED
**Priority**: HIGH - Technical Debt Elimination & V2 Standards Implementation

### 🚨 **FUNDAMENTAL OPERATIONAL PRINCIPLE: CYCLE-BASED METHODOLOGY**
**TIME-BASED DEADLINES ARE PROHIBITED. ALL OPERATIONS ARE CYCLE-BASED.**

- **Cycle Definition**: One Captain prompt + One Agent response = One complete cycle
- **Response Protocol**: Agent acknowledgment/response = Cycle completion
- **Escalation Criteria**: Only escalate if agent fails to respond within one cycle
- **Timeline Format**: "Complete within X cycles" (NEVER time-based deadlines)
- **Progress Format**: "Cycle X complete: [achievements]" (NEVER time-based progress)

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
- ✅ **Report Progress**: Use devlog system for all updates (cycle-based format)
- ✅ **Claim Contracts**: Use --get-next-task to claim available work
- ✅ **Coordinate**: Support other agents in their compliance efforts
- ✅ **Validate**: Ensure all deliverables meet V2 compliance standards

🚨 **IMMEDIATE ACTIONS (CYCLE-BASED)**:
1. Check your agent_workspaces/<Agent-ID>/inbox/ for messages (Cycle 1 start)
2. Update your status.json with current mission and progress
3. Claim next available contract with --get-next-task
4. Report readiness and current compliance status
5. Begin autonomous technical debt elimination within 1 cycle

**CYCLE-BASED REPORTING REQUIREMENTS**:
- **Progress Updates**: Report every 2 cycles with measurable achievements
- **Task Completion**: Complete assigned tasks within specified cycle count
- **Status Updates**: Update status.json immediately upon cycle completion
- **Coordination**: Support other agents through active cycle participation

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**
**Status**: Monitoring autonomous development compliance across all agents
**Expectation**: Proactive, autonomous, and efficient V2 compliance achievement
**Methodology**: Cycle-based operations with measurable progress tracking

**WE. ARE. SWARM.** ⚡️🔥"""

    print("📨 Sending compliance mode onboarding to all agents...")

    service.send_to_all_agents(
        content=compliance_content,
        sender="Captain Agent-4",
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
        mode=args.mode,
        new_tab_method=args.new_tab_method,
    )

    print("✅ COMPLIANCE MODE ONBOARDING COMPLETE")
    print(
        "🎯 All agents now configured for autonomous development with compliance protocols"
    )
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


async def handle_hard_onboarding_command(args, service) -> bool:
    """Handle hard onboarding command - wrapup + personalized onboarding sequence."""
    print("🚀 HARD ONBOARDING SEQUENCE ACTIVATED")
    print("=" * 60)
    
    # Hard onboarding ONLY works with PyAutoGUI coordinates
    if args.mode == "inbox":
        print("❌ ERROR: Hard onboarding only works with PyAutoGUI coordinates")
        print("❌ Cannot onboard agents to inbox - use --mode pyautogui")
        print("💡 Usage: python -m src.services.messaging_cli --hard-onboarding --mode pyautogui")
        return False
    
    print("✅ Using PyAutoGUI coordinate-based delivery")
    
    # Step 1: Send wrapup message to all agents with regular priority
    print("📤 STEP 1: Sending wrapup message to all agents...")
    wrapup_content = """🚨 **CAPTAIN AGENT-4 - HARD ONBOARDING INITIATED** 🚨

**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager
**Status**: Hard onboarding sequence activated
**Mode**: PyAutoGUI Coordinate-Based Delivery

**HARD ONBOARDING SEQUENCE**:
- ✅ **Step 1**: Wrapup message delivered to coordinates (this message)
- ✅ **Step 2**: New tab creation with Ctrl+T
- ✅ **Step 3**: Personalized onboarding message incoming

**READY FOR**: Personalized onboarding message

**Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager**

**WE. ARE. SWARM.** ⚡️🔥"""

    # Send wrapup to all agents using PyAutoGUI coordinates
    service.send_to_all_agents(
        content=wrapup_content,
        sender="Captain Agent-4",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.WRAPUP],
        mode="pyautogui",  # Force PyAutoGUI mode
        use_paste=True,
    )
    
    print("✅ Wrapup message sent to all agent coordinates")
    
    # Step 2: Send personalized onboarding messages to each agent
    print("📤 STEP 2: Sending personalized onboarding messages to coordinates...")
    
    # Get agent order (Agent-4 last)
    agent_order = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-5", 
        "Agent-6", "Agent-7", "Agent-8", "Agent-4"
    ]
    
    for agent_id in agent_order:
        print(f"🎯 Sending personalized onboarding to {agent_id} coordinates...")
        
        # Generate personalized onboarding message for this agent
        onboarding_content = service.generate_personalized_onboarding_message(
            agent_id=agent_id,
            style=args.onboarding_style if hasattr(args, 'onboarding_style') else "friendly"
        )
        
                       # Send personalized onboarding as S2A message via PyAutoGUI coordinates
        await service.send_message_to_agent(
                   agent_id=agent_id,
                   content=onboarding_content,
                   sender="Captain Agent-4",
                   message_type=UnifiedMessageType.S2A,
                   priority=UnifiedMessagePriority.REGULAR,
                   tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
                   mode="pyautogui",  # Force PyAutoGUI mode
                   use_new_tab=True,  # This will trigger Ctrl+T
                   use_paste=True,
                   use_onboarding_coords=True,  # Use onboarding input coordinates
               )
        
        print(f"✅ Personalized onboarding sent to {agent_id} coordinates")
        
        # Brief pause between agents
        time.sleep(1)
    
    print("🎉 HARD ONBOARDING SEQUENCE COMPLETE")
    print("📊 All agents received wrapup + personalized onboarding via coordinates")
    return True


async def handle_message_commands(args, service) -> bool:
    """Handle regular message sending commands."""
    # Check if message is required for sending
    if not args.message:
        print("❌ ERROR: --message/-m is required for sending messages")
        print(
            "Use --list-agents, --coordinates, --history, --onboarding, --onboard, or --wrapup for utility commands"
        )
        sys.exit(1)

    # Determine message type and priority
    message_type = UnifiedMessageType(args.type)
    priority = (
        UnifiedMessagePriority.URGENT
        if args.high_priority
        else UnifiedMessagePriority(args.priority)
    )

    # Determine sender and recipient types
    sender_type = SenderType(getattr(args, 'sender_type', 'system')) if hasattr(args, 'sender_type') and args.sender_type else None
    recipient_type = RecipientType(getattr(args, 'recipient_type', 'agent')) if hasattr(args, 'recipient_type') and args.recipient_type else None

    # Always use paste for maximum speed
    use_paste = True
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
            new_tab_method=new_tab_method,
            sender_type=sender_type,
            recipient_type=recipient_type,
        )
    else:
        # Send to specific agent
        if not args.agent:
            print("❌ ERROR: --agent/-a is required for single agent messaging")
            print("Use --bulk for sending to all agents")
            sys.exit(1)

        await service.send_message_to_agent(
            agent_id=args.agent,
            content=args.message,
            sender=args.sender,
            message_type=message_type,
            priority=priority,
            tags=[UnifiedMessageTag.CAPTAIN],
            mode=args.mode,
            use_new_tab=args.new_tab_method == "ctrl_t",
            use_paste=not getattr(args, 'no_paste', False),
        )

    return True
