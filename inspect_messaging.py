#!/usr/bin/env python3
"""
Inspect MessagingGateway configuration and core
"""
import os
import sys

sys.path.append("src")

from integration.messaging_gateway import MessagingGateway


def inspect_gateway():
    print("🔧 Inspecting MessagingGateway Configuration")
    print("=" * 50)

    # Create gateway
    gateway = MessagingGateway()

    print(f"Backend: {gateway.backend_name}")
    print(f"Core type: {type(gateway.core)}")
    print(f"Available agents: {list(gateway.agent_coordinates.keys())}")

    # Check core methods
    core_methods = [method for method in dir(gateway.core) if not method.startswith("_")]
    print(f"Core methods: {core_methods}")

    # Check if send_message exists
    has_send = hasattr(gateway.core, "send_message")
    print(f"Core has send_message: {has_send}")

    # Test coordinate resolution
    try:
        agent_4_coords = gateway._normalize_target("Agent-4")
        print(f"Agent-4 coordinates: {agent_4_coords}")
    except Exception as e:
        print(f"❌ Coordinate resolution failed: {e}")

    # Test dry run mode
    print(f"Dry run mode: {gateway.dry_run}")

    return gateway


if __name__ == "__main__":
    inspect_gateway()
    print("✅ Inspection completed")
