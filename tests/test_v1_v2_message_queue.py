#!/usr/bin/env python3
"""Simple test for V1-V2 Message Queue System"""

import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from services.v1_v2_message_queue_system import V1V2MessageQueueSystem, MessagePriority
    print("✅ Successfully imported V1V2MessageQueueSystem")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_simple():
    """Simple test of the message queue system"""
    print("🚀 Testing V1-V2 Message Queue System")
    print("=" * 50)
    
    # Initialize the system
    system = V1V2MessageQueueSystem(use_cdp=True, use_pyautogui=True)
    
    # Register test agents
    print("📝 Registering test agents...")
    system.register_agent("agent_1", coordinates=(100, 200), preferred_method="pyautogui")
    system.register_agent("agent_2", coordinates=(300, 200), preferred_method="cdp", cdp_target=0)
    
    # Start processing
    print("▶️  Starting message processing...")
    system.start_processing()
    
    try:
        # Send a test message to Agent-2
        print("\n📤 Sending test message to Agent-2...")
        message_id = system.send_message(
            "coordinator", 
            "agent_2", 
            "Agent-2: Test message - please acknowledge receipt.",
            MessagePriority.NORMAL
        )
        print(f"✅ Message queued with ID: {message_id}")
        
        # Wait for processing
        print("\n⏳ Waiting for message processing...")
        time.sleep(3)
        
        # Check status
        print("\n📊 System status:")
        status = system.get_system_status()
        print(f"  Agents registered: {status['agents_registered']}")
        print(f"  Processing active: {status['processing_active']}")
        print(f"  CDP available: {status['cdp_available']}")
        print(f"  PyAutoGUI available: {status['pyautogui_available']}")
        
        print("\n�� Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Stop the system
        print("\n⏹️  Stopping message processing...")
        system.stop_processing()
        print("✅ System stopped")

if __name__ == "__main__":
    test_simple()
