#!/usr/bin/env python3
"""Test script to verify real coordinates are loaded"""

from src.services import UnifiedMessagingService


def test_coordinates():
    print("Testing real coordinates loading...")

    # Initialize system
    mq = UnifiedMessagingService()
    print("System initialized")

    # Check coordinates
    print("\nReal coordinates loaded:")
    for agent_id, info in mq.agent_registry.items():
        coords = info["coordinates"]
        print(f"  {agent_id}: x={coords['x']}, y={coords['y']}")

    # Verify these are not dummy coordinates
    dummy_coords = [
        {"x": 100, "y": 100},
        {"x": 200, "y": 100},
        {"x": 300, "y": 100},
        {"x": 400, "y": 100},
    ]
    has_real_coords = False

    for agent_id, info in mq.agent_registry.items():
        coords = info["coordinates"]
        if coords not in dummy_coords:
            has_real_coords = True
            break

    if has_real_coords:
        print("\n✅ Real coordinates loaded successfully!")
        print("   (Not using dummy coordinates anymore)")
    else:
        print("\n❌ Still using dummy coordinates!")

    # Stop system
    mq.stop_system()
    print("System stopped")


if __name__ == "__main__":
    test_coordinates()
