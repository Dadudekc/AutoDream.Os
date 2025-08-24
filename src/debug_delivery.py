#!/usr/bin/env python3
"""
Debug Message Delivery Status Tracking
"""

import sys
import time
import json

from src.utils.stability_improvements import stability_manager, safe_import

sys.path.append("src")

try:
    from services.messaging import UnifiedMessagingService as V2MessageDeliveryService  # Backward compatibility alias

    print("🐛 DEBUGGING MESSAGE DELIVERY STATUS TRACKING")
    print("=" * 60)

    # Initialize service
    service = V2MessageDeliveryService()

    print("✅ Service initialized")
    print(f"Initial delivery_status: {len(service.status_tracker.get_all_status())} entries")

    # Test 1: Send message directly
    print("\n🧪 TEST 1: Direct message send")
    print("-" * 40)

    success = service.send_message("agent_1", "debug_test", "Debug test message")
    print(f"Message send result: {success}")

    # Wait for processing
    time.sleep(2)

    print(f"After send - delivery_status: {len(service.status_tracker.get_all_status())} entries")
    if service.status_tracker.get_all_status():
        print(f"agent_1 status: {service.status_tracker.get_agent_status('agent_1') or 'NOT_FOUND'}")

    # Test 2: Check raw status
    print("\n🧪 TEST 2: Raw status check")
    print("-" * 40)

    raw_status = service.get_delivery_status()
    print(f"Raw delivery_status keys: {list(raw_status['delivery_status'].keys())}")

    # Test 3: Force status update
    print("\n🧪 TEST 3: Force status update")
    print("-" * 40)

    # Manually add some status data
    service.status_tracker.record_successful_delivery("agent_1", "debug_test")

    print(
        f"After manual update - delivery_status: {len(service.status_tracker.get_all_status())} entries"
    )

    # Test 4: Check status again
    print("\n🧪 TEST 4: Status after manual update")
    print("-" * 40)

    final_status = service.get_delivery_status()
    print(f"Final delivery_status: {len(final_status['delivery_status'])} entries")

    if final_status["delivery_status"]:
        agent1_status = final_status["delivery_status"]["agent_1"]
        print(f"Agent 1 status: {agent1_status}")

    print("\n🔍 DEBUG SUMMARY")
    print("=" * 60)
    print(f"Service delivery_status: {len(service.status_tracker.get_all_status())} entries")
    print(f"Get status delivery_status: {len(final_status['delivery_status'])} entries")
    print(f"Message queue size: {final_status['queue_size']}")

except Exception as e:
    print(f"❌ Debug failed: {e}")
    import traceback

    traceback.print_exc()
