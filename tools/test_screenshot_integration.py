#!/usr/bin/env python3
"""
Test Screenshot Management Integration
====================================

Test the integrated screenshot management system.

Author: Agent-4 (Captain)
License: MIT
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from src.services.messaging_service import ConsolidatedMessagingService


def test_screenshot_integration():
    """Test screenshot management integration."""
    print("🧪 Testing Screenshot Management Integration")
    print("=" * 50)

    # Initialize messaging service
    messaging_service = ConsolidatedMessagingService()

    # Test cycle increment
    print("📈 Testing cycle increment...")
    for i in range(12):
        messaging_service.increment_messaging_cycle()
        print(f"  Cycle {messaging_service.screenshot_manager.current_cycle}")

    print("\n🔍 Testing screenshot triggers...")

    # Reset cycle counter for testing
    messaging_service.screenshot_manager.current_cycle = 0

    # Test coordination trigger (every 3 cycles)
    for cycle in range(1, 13):
        messaging_service.increment_messaging_cycle()
        should_take = messaging_service.check_screenshot_trigger("COORDINATION", "NORMAL")
        current_cycle = messaging_service.screenshot_manager.current_cycle
        if should_take:
            context = messaging_service.get_screenshot_context("COORDINATION")
            print(
                f"  ✅ Cycle {cycle} (current: {current_cycle}): Screenshot triggered - {context['expected_content']}"
            )
        else:
            print(f"  ⏭️  Cycle {cycle} (current: {current_cycle}): No screenshot needed")

    print("\n🚨 Testing critical event trigger...")
    should_take = messaging_service.check_screenshot_trigger("COORDINATION", "MAJOR_COMPLETION")
    if should_take:
        context = messaging_service.get_screenshot_context("MAJOR_COMPLETION")
        print(f"  ✅ Critical event: Screenshot triggered - {context['expected_content']}")

    print("\n📊 Screenshot Manager Status:")
    status = {
        "current_cycle": messaging_service.screenshot_manager.current_cycle,
        "triggers": {
            trigger_type: {"interval": trigger.cycle_interval, "enabled": trigger.enabled}
            for trigger_type, trigger in messaging_service.screenshot_manager.triggers.items()
        },
    }

    for trigger_type, config in status["triggers"].items():
        print(f"  {trigger_type}: Every {config['interval']} cycles, Enabled: {config['enabled']}")

    print("\n✅ Screenshot management integration test complete!")
    print("📸 System ready for automated visual coordination")


if __name__ == "__main__":
    test_screenshot_integration()
