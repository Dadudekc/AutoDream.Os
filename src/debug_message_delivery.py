#!/usr/bin/env python3
"""
Debug Message Delivery Process
"""

import sys
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import

sys.path.append("src")

try:
    from services.messaging import UnifiedMessagingService as V2MessageDeliveryService  # Backward compatibility alias

    print("🐛 DEBUGGING MESSAGE DELIVERY PROCESS")
    print("=" * 60)

    # Initialize service
    service = V2MessageDeliveryService()

    print("✅ Service initialized")
    print(f"Initial delivery_status: {len(service.status_tracker.get_all_status())} entries")
    print(
        f"Agent-3 coordinates: {service.coordinate_manager.get_agent_coordinates('agent_3') or 'NOT_FOUND'}"
    )

    # Test 1: Direct message delivery
    print("\n🧪 TEST 1: Direct Message Delivery")
    print("-" * 40)

    # Create message data manually
    message_data = {
        "agent_id": "agent_3",
        "type": "debug_test",
        "content": "🎬 Agent-3 Self-Test: Testing message delivery to Multimedia & Content Specialist",
        "timestamp": time.time(),
    }

    print(f"Message data: {message_data}")

    # Call delivery method directly
    print("\n📤 Calling _deliver_message directly...")
    service._deliver_message(message_data)

    print(f"After delivery - delivery_status: {len(service.status_tracker.get_all_status())} entries")
    if service.status_tracker.get_all_status():
        print(f"agent_3 status: {service.status_tracker.get_agent_status('agent_3') or 'NOT_FOUND'}")

    # Test 2: Check raw status
    print("\n🧪 TEST 2: Raw Status Check")
    print("-" * 40)

    raw_status = service.get_delivery_status()
    print(f"Raw delivery_status keys: {list(raw_status['delivery_status'].keys())}")

    # Test 3: Check if PyAutoGUI is working
    print("\n🧪 TEST 3: PyAutoGUI Status")
    print("-" * 40)

    try:
        import pyautogui

        print(f"PyAutoGUI imported: ✅")
        print(f"PyAutoGUI available: {hasattr(service, 'PYAUTOGUI_AVAILABLE')}")
        print(
            f"Service PYAUTOGUI_AVAILABLE: {getattr(service, 'PYAUTOGUI_AVAILABLE', 'NOT_FOUND')}"
        )
    except ImportError:
        print("PyAutoGUI not available: ❌")

    # Test 4: Check agent coordinates
    print("\n🧪 TEST 4: Agent Coordinates")
    print("-" * 40)

    agent_3_coords = service.coordinate_manager.get_agent_coordinates("agent_3")
    if agent_3_coords:
        print(
            f"Agent-3 coordinates: ({agent_3_coords['input_x']}, {agent_3_coords['input_y']})"
        )
        print(f"Agent-3 status: {agent_3_coords['status']}")
        print(f"Last delivery: {agent_3_coords['last_delivery']}")
    else:
        print("Agent-3 not found in coordinates")

    print("\n🔍 DEBUG SUMMARY")
    print("=" * 60)
    print(f"Service delivery_status: {len(service.status_tracker.get_all_status())} entries")
    print(f"Get status delivery_status: {len(raw_status['delivery_status'])} entries")
    print(f"Message queue size: {raw_status['queue_size']}")

except Exception as e:
    print(f"❌ Debug failed: {e}")
    import traceback

    traceback.print_exc()
