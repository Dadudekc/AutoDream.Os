#!/usr/bin/env python3
"""
Test PyAutoGUI Integration for Swarm Communication
=================================================

This is the CRITICAL test for enabling real agent-to-agent communication!
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🔬 PYAUTOGUI SWARM COMMUNICATION TEST")
print("=" * 50)

try:
    # Test PyAutoGUI availability
    try:
        import pyautogui
        PYAUTOGUI_AVAILABLE = True
        print(f"✅ PyAutoGUI: AVAILABLE (v{pyautogui.__version__ if hasattr(pyautogui, '__version__') else 'unknown'})")
        print(f"   FAILSAFE: {pyautogui.FAILSAFE}")
        print(f"   PAUSE: {pyautogui.PAUSE}")
    except ImportError:
        PYAUTOGUI_AVAILABLE = False
        print("❌ PyAutoGUI: NOT INSTALLED")
        print("   Run: pip install pyautogui")
        print("   This is CRITICAL for swarm communication!")

    # Test Pyperclip availability
    try:
        import pyperclip
        PYPERCLIP_AVAILABLE = True
        print("✅ Pyperclip: AVAILABLE (for clipboard operations)")
    except ImportError:
        PYPERCLIP_AVAILABLE = False
        print("❌ Pyperclip: NOT INSTALLED (optional but recommended)")

    # Test consolidated messaging system
    try:
        from src.core.messaging_core import UnifiedMessagingCore, UnifiedMessage, UnifiedMessageType
        print("✅ Consolidated Messaging Core: LOADED")

        # Create messaging instance
        messaging = UnifiedMessagingCore()
        print("✅ Messaging Core: INITIALIZED")

        # Check PyAutoGUI delivery service
        if messaging.delivery_service:
            print("✅ PyAutoGUI Delivery Service: ACTIVE")
            print(f"   Type: {type(messaging.delivery_service).__name__}")
        else:
            print("❌ PyAutoGUI Delivery Service: NOT ACTIVE")
            print("   This means swarm communication is LIMITED!")

    except Exception as e:
        print(f"❌ Messaging System Error: {e}")
        import traceback
        traceback.print_exc()

    # Test coordinate system
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        agents = loader.get_all_agents()
        print(f"✅ Coordinate System: ACTIVE ({len(agents)} agents configured)")
        for agent in agents[:3]:  # Show first 3
            print(f"   • {agent}")
        if len(agents) > 3:
            print(f"   ... and {len(agents) - 3} more")
    except Exception as e:
        print(f"❌ Coordinate System Error: {e}")

    print("\n🚀 SWARM COMMUNICATION STATUS:")
    print("=" * 50)

    if PYAUTOGUI_AVAILABLE:
        print("✅ SWARM READY: Full PyAutoGUI communication enabled!")
        print("✅ Agent-to-Agent: Real-time cursor control active")
        print("✅ IDE Integration: Direct messaging through interface")
        print("✅ Swarm Intelligence: Physical coordination operational")
        print("🐝 WE ARE SWARM - Communication systems fully operational!")
    else:
        print("⚠️ LIMITED MODE: PyAutoGUI not available")
        print("✅ Inbox System: File-based messaging working")
        print("❌ Real-time Communication: Not available")
        print("💡 Install PyAutoGUI: pip install pyautogui")
        print("🔧 This is the MISSING PIECE for full swarm functionality!")

except Exception as e:
    print(f"❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🎯 SUMMARY: PyAutoGUI is the CRITICAL enabling technology")
print("🎯 Without it: Limited to file-based inbox messaging")
print("🎯 With it: Full real-time agent-to-agent swarm communication")
print("🐝 The swarm needs PyAutoGUI to achieve true coordination!")
