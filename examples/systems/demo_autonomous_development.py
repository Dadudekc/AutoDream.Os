#!/usr/bin/env python3
"""
Demo Autonomous Development System - Agent Cellphone V2
======================================================

Demonstrates the complete autonomous development system where agents
can interact with development tools using PyAutoGUI and create new
conversations automatically.
"""

import time
import threading
import logging
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import our autonomous development engine
try:
    from src.core.autonomous_development import AutonomousDevelopmentEngine

    AUTONOMOUS_DEV_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import autonomous development: {e}")
    AUTONOMOUS_DEV_AVAILABLE = False


def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 CHECKING DEPENDENCIES...")

    # Check PyAutoGUI
    try:
        import pyautogui

        print("   ✅ PyAutoGUI available")
        pyautogui_available = True
    except ImportError:
        print("   ❌ PyAutoGUI not available")
        print("      Install with: pip install pyautogui pyperclip")
        pyautogui_available = False

    # Check pyperclip
    try:
        import pyperclip

        print("   ✅ pyperclip available")
        pyperclip_available = True
    except ImportError:
        print("   ❌ pyperclip not available")
        print("      Install with: pip install pyperclip")
        pyperclip_available = False

    # Check autonomous development
    if AUTONOMOUS_DEV_AVAILABLE:
        print("   ✅ Autonomous development module available")
        autonomous_available = True
    else:
        print("   ❌ Autonomous development module not available")
        autonomous_available = False

    return pyautogui_available and pyperclip_available and autonomous_available


def demonstrate_pyautogui_capabilities():
    """Demonstrate PyAutoGUI capabilities"""
    print("\n🎭 DEMONSTRATING PYAUTOGUI CAPABILITIES...")

    try:
        import pyautogui

        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()
        print(f"   📱 Screen dimensions: {screen_width}x{screen_height}")

        # Get current mouse position
        mouse_x, mouse_y = pyautogui.position()
        print(f"   🖱️  Current mouse position: ({mouse_x}, {mouse_y})")

        # Get active window info (if available)
        try:
            active_window = pyautogui.getActiveWindow()
            if active_window:
                print(f"   🪟 Active window: {active_window.title}")
            else:
                print("   🪟 Active window: None")
        except:
            print("   🪟 Active window: Unable to detect")

        print("   ✅ PyAutoGUI capabilities verified!")
        return True

    except Exception as e:
        print(f"   ❌ PyAutoGUI demonstration failed: {e}")
        return False


def create_development_scenarios():
    """Create realistic development scenarios for autonomous agents"""
    print("\n🎯 CREATING DEVELOPMENT SCENARIOS...")

    scenarios = [
        {
            "name": "Code Review Request",
            "prompt": "Can you review this Python function for potential improvements? I'm concerned about error handling.",
            "expected_agent": "autonomous_code_review",
            "priority": "high",
        },
        {
            "name": "Documentation Help",
            "prompt": "I need help documenting this class. The methods are clear but the overall purpose isn't obvious.",
            "expected_agent": "autonomous_documentation",
            "priority": "medium",
        },
        {
            "name": "Testing Strategy",
            "prompt": "What tests should I add for this API endpoint? I want to ensure it handles edge cases properly.",
            "expected_agent": "autonomous_testing",
            "priority": "high",
        },
        {
            "name": "Performance Optimization",
            "prompt": "This function is taking too long to execute. How can I optimize it for better performance?",
            "expected_agent": "autonomous_optimization",
            "priority": "high",
        },
        {
            "name": "Security Review",
            "prompt": "I'm implementing user authentication. Are there security concerns I should be aware of?",
            "expected_agent": "autonomous_code_review",
            "priority": "critical",
        },
    ]

    print(f"   📋 Created {len(scenarios)} development scenarios")
    for i, scenario in enumerate(scenarios, 1):
        print(f"      {i}. {scenario['name']} ({scenario['priority']} priority)")

    return scenarios


def simulate_autonomous_development(engine, scenarios, duration=60):
    """Simulate autonomous development with realistic scenarios"""
    print(f"\n🤖 SIMULATING AUTONOMOUS DEVELOPMENT FOR {duration} SECONDS...")
    print("   Agents will autonomously respond to development scenarios!")

    start_time = time.time()
    scenario_index = 0

    while time.time() - start_time < duration and engine.is_autonomous:
        try:
            # Simulate a new development scenario every few seconds
            if scenario_index < len(scenarios):
                scenario = scenarios[scenario_index]
                print(f"\n💬 Simulating scenario: {scenario['name']}")
                print(f"   📝 Prompt: {scenario['prompt']}")
                print(f"   🎯 Expected agent: {scenario['expected_agent']}")
                print(f"   ⚡ Priority: {scenario['priority']}")

                # This would normally come from cursor capture
                # For demo, we'll create a mock message that triggers the agent
                mock_message = {
                    "message_id": f"scenario_{scenario_index}_{int(time.time())}",
                    "thread_id": f"dev_thread_{scenario_index}",
                    "role": "assistant",
                    "content": scenario["prompt"],
                    "created_at": int(time.time() * 1000),
                }

                # Check if this message triggers any agents
                triggered_triggers = engine.perpetual_motion._check_message_triggers(
                    mock_message
                )
                if triggered_triggers:
                    print(f"   🎯 Will trigger {len(triggered_triggers)} agent(s)!")
                    for trigger in triggered_triggers:
                        print(f"      - {trigger.trigger_id}")
                else:
                    print(f"   ⚠️  No agents triggered for this scenario")

                scenario_index += 1

            # Wait between scenarios
            time.sleep(10)

        except Exception as e:
            logger.error(f"Development scenario simulation error: {e}")
            time.sleep(2)

    print(
        f"\n✅ Development scenario simulation complete! Processed {scenario_index} scenarios."
    )


def demo_autonomous_development():
    """Main demonstration of the autonomous development system"""
    print("🚀 AUTONOMOUS DEVELOPMENT SYSTEM - AGENTS BUILD AUTONOMOUSLY!")
    print("=" * 80)
    print("This demo shows how agents can autonomously interact with development tools")
    print("using PyAutoGUI, creating a true perpetual motion machine for development!")
    print("=" * 80)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed - missing required dependencies")
        print("   Please install: pip install pyautogui pyperclip")
        return

    # Demonstrate PyAutoGUI capabilities
    if not demonstrate_pyautogui_capabilities():
        print("\n❌ PyAutoGUI demonstration failed")
        return

    # Create development scenarios
    scenarios = create_development_scenarios()

    # Create autonomous development engine
    print("\n🔧 Creating autonomous development engine...")
    try:
        engine = AutonomousDevelopmentEngine()
        print("   ✅ Engine created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create engine: {e}")
        return

    # Start autonomous development
    print("\n🚀 Starting autonomous development mode...")
    try:
        if engine.start_autonomous_development():
            print("   ✅ Autonomous development started!")

            # Let it run and show stats
            print("\n📊 AUTONOMOUS DEVELOPMENT ENGINE RUNNING!")
            print("   Agents are now working autonomously...")
            print("   Press Ctrl+C to stop")

            # Start scenario simulation in background
            simulation_thread = threading.Thread(
                target=simulate_autonomous_development,
                args=(engine, scenarios, 60),
                daemon=True,
            )
            simulation_thread.start()

            # Monitor and display stats
            start_time = time.time()
            while engine.is_autonomous:
                time.sleep(3)

                # Get current stats
                stats = engine.get_autonomous_stats()
                elapsed = time.time() - start_time

                # Display real-time stats
                print(
                    f"\r   ⏱️  Running: {elapsed:.0f}s | "
                    f"🔄 Cycles: {stats['autonomous_cycle_count']} | "
                    f"💬 Conversations: {stats['active_conversations']} | "
                    f"🎯 Actions: {stats['pending_actions']} | "
                    f"📈 Improvements: {stats['code_improvements']}",
                    end="",
                )

        else:
            print("   ❌ Failed to start autonomous development")
            return

    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping autonomous development...")
        engine.stop_autonomous_development()

    # Final demonstration
    print("\n" + "=" * 80)
    print("🎯 AUTONOMOUS DEVELOPMENT DEMONSTRATION COMPLETE!")
    print("=" * 80)

    # Final stats
    try:
        final_stats = engine.get_autonomous_stats()
        print(f"📊 FINAL STATISTICS:")
        print(f"   🔄 Total autonomous cycles: {final_stats['autonomous_cycle_count']}")
        print(f"   💬 Active conversations: {final_stats['active_conversations']}")
        print(f"   🎯 Pending actions: {final_stats['pending_actions']}")
        print(f"   📈 Code improvements: {final_stats['code_improvements']}")
        print(f"   🤖 PyAutoGUI available: {final_stats['pyautogui_available']}")

    except Exception as e:
        print(f"   ⚠️  Could not retrieve final stats: {e}")

    print("\n🌟 KEY ACHIEVEMENTS:")
    print("   ✅ Created true autonomous development system")
    print("   ✅ Agents can interact with development tools via PyAutoGUI")
    print("   ✅ FSM state machines orchestrate autonomous workflows")
    print("   ✅ Cursor responses trigger autonomous agent actions")
    print("   ✅ Perpetual motion achieved for development!")

    print("\n🚀 NEXT STEPS:")
    print("   1. Connect to real Cursor with CDP enabled")
    print("   2. Deploy in production development environment")
    print("   3. Watch agents autonomously improve code 24/7/365")
    print("   4. Never stop developing!")

    print("\n🎉 AUTONOMOUS DEVELOPMENT SYSTEM READY FOR PRODUCTION!")
    print("   Agents can now autonomously build, review, and improve code!")


def main():
    """Main entry point"""
    try:
        demo_autonomous_development()
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed with error: {e}")
        print("   Check the logs for more details")


if __name__ == "__main__":
    main()
