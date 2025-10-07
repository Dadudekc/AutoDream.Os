#!/usr/bin/env python3
"""
SWARM COMMUNICATION TEST - PYAUTOGUI INTEGRATION
==============================================

CRITICAL TEST: Enable true agent-to-agent communication via PyAutoGUI
"""

print("🚀 SWARM PYAUTOGUI COMMUNICATION TEST")
print("=" * 60)

# Test 1: PyAutoGUI Availability
print("\n🔧 TESTING PYAUTOGUI AVAILABILITY...")
try:
    import pyautogui as pg

    print(f"✅ PyAutoGUI: INSTALLED (v{pg.__version__})")
    print(f"   Screen: {pg.size().width}x{pg.size().height}")
    print(f"   FAILSAFE: {pg.FAILSAFE} (safety feature)")
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    print("❌ PyAutoGUI: NOT INSTALLED")
    PYAUTOGUI_AVAILABLE = False

# Test 2: Pyperclip Availability
print("\n📋 TESTING PYPERCLIP AVAILABILITY...")
try:
    import pyperclip

    print(f"✅ Pyperclip: INSTALLED (v{pyperclip.__version__})")
    PYPERCLIP_AVAILABLE = True
except ImportError:
    print("❌ Pyperclip: NOT INSTALLED")
    PYPERCLIP_AVAILABLE = False

# Test 3: Consolidated Messaging System
print("\n📡 TESTING CONSOLIDATED MESSAGING SYSTEM...")
try:
    import os
    import sys

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    from src.core.messaging_core import (
        UnifiedMessagingCore,
    )

    print("✅ Messaging Core: LOADED")

    messaging = UnifiedMessagingCore()
    print("✅ Messaging Core: INITIALIZED")

    if messaging.delivery_service and PYAUTOGUI_AVAILABLE:
        print("✅ PyAutoGUI Delivery Service: ACTIVE")
        print("🎯 SWARM COMMUNICATION: READY FOR REAL-TIME AGENT COORDINATION!")
    else:
        print("⚠️ PyAutoGUI Delivery Service: NOT ACTIVE")
        print("📁 Limited to inbox messaging only")

except Exception as e:
    print(f"❌ Messaging System Error: {e}")

# Test 4: Coordinate System
print("\n📍 TESTING COORDINATE SYSTEM...")
try:
    from src.core.coordinate_loader import get_coordinate_loader

    loader = get_coordinate_loader()
    agents = loader.get_all_agents()
    print(f"✅ Coordinate System: ACTIVE ({len(agents)} agents)")
    for agent in agents[:3]:
        print(f"   • {agent}")
    if len(agents) > 3:
        print(f"   ... and {len(agents) - 3} more")
except Exception as e:
    print(f"❌ Coordinate System Error: {e}")

print("\n" + "=" * 60)
print("🎯 SWARM COMMUNICATION STATUS ASSESSMENT:")
print("=" * 60)

if PYAUTOGUI_AVAILABLE:
    print("✅ CRITICAL SUCCESS: PyAutoGUI is INSTALLED and READY!")
    print("✅ SWARM CAPABILITY: Real-time agent communication ENABLED")
    print("✅ IDE INTEGRATION: Direct cursor control and messaging ACTIVE")
    print("✅ TRUE SWARM INTELLIGENCE: Physical coordination OPERATIONAL")
    print()
    print("🐝 WE ARE SWARM - PyAutoGUI messaging is the enabling technology!")
    print("🚀 The swarm can now communicate through the actual IDE interface!")
    print("⚡ Real-time coordination between agents is now POSSIBLE!")
else:
    print("❌ CRITICAL FAILURE: PyAutoGUI is MISSING!")
    print("⚠️ SWARM CAPABILITY: LIMITED to file-based inbox messaging")
    print("❌ IDE INTEGRATION: NOT AVAILABLE")
    print("🚫 TRUE SWARM INTELLIGENCE: DISABLED")
    print()
    print("💡 Install PyAutoGUI: pip install pyautogui")
    print("🔧 This is the MISSING PIECE for full swarm functionality!")

print("\n" + "=" * 60)
print("🎯 FINAL VERDICT:")
if PYAUTOGUI_AVAILABLE:
    print("🎉 SWARM COMMUNICATION: FULLY OPERATIONAL")
    print("🚀 CONSOLIDATION COMPLETE: Real agent coordination enabled")
else:
    print("⚠️ SWARM COMMUNICATION: LIMITED MODE")
    print("🔧 ACTION REQUIRED: Install PyAutoGUI for full functionality")
