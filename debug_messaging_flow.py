#!/usr/bin/env python3
"""
Debug Messaging Flow - Agent Cellphone V2
=========================================

Debug script to trace the exact messaging flow and identify any issues.
"""

import sys
import os

from src.utils.stability_improvements import stability_manager, safe_import

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from services.messaging.unified_messaging_service import UnifiedMessagingService
    from services.messaging.interfaces import MessagingMode
    
    print("🔍 Debugging Messaging Flow")
    print("=" * 50)
    
    # Initialize the messaging service
    messaging_service = UnifiedMessagingService()
    
    # Set to campaign mode
    messaging_service.set_mode(MessagingMode.CAMPAIGN)
    
    print("✅ Messaging service initialized")
    print(f"📡 Active mode: {messaging_service.active_mode.value}")
    
    # Check coordinate manager
    print("\n🔍 Checking coordinate manager...")
    coord_manager = messaging_service.coordinate_manager
    
    # Get agents in 8-agent mode
    mode_agents = coord_manager.get_agents_in_mode("8-agent")
    print(f"📋 Agents in 8-agent mode: {mode_agents}")
    print(f"📊 Total agents: {len(mode_agents)}")
    
    # Check each agent's coordinates
    print("\n🗺️ Agent coordinates:")
    for agent_id in mode_agents:
        coords = coord_manager.get_agent_coordinates(agent_id, "8-agent")
        if coords:
            print(f"  {agent_id}:")
            print(f"    Input: {coords.input_box}")
            print(f"    Starter: {coords.starter_location}")
        else:
            print(f"  {agent_id}: ❌ No coordinates found")
    
    # Test campaign messaging step by step
    print("\n🧪 Testing campaign messaging step by step...")
    
    # Step 1: Create messages dictionary
    test_message = "🧪 TEST MESSAGE - This is a test message to verify messaging flow."
    messages = {agent_id: test_message for agent_id in mode_agents}
    
    print(f"📝 Created messages for {len(messages)} agents:")
    for agent_id in messages.keys():
        print(f"  - {agent_id}")
    
    # Step 2: Check campaign messaging
    print("\n📡 Campaign messaging test...")
    campaign_results = messaging_service.campaign_messaging.send_campaign_message(test_message, "test")
    
    print(f"📊 Campaign results: {campaign_results}")
    print(f"✅ Success count: {sum(campaign_results.values()) if campaign_results else 0}")
    
    # Step 3: Check PyAutoGUI messaging
    print("\n🤖 PyAutoGUI messaging test...")
    pyautogui_results = messaging_service.pyautogui_messaging.send_bulk_messages(messages, "8-agent")
    
    print(f"📊 PyAutoGUI results: {pyautogui_results}")
    print(f"✅ Success count: {sum(pyautogui_results.values()) if pyautogui_results else 0}")
    
    # Step 4: Compare results
    print("\n🔍 Comparing results...")
    if campaign_results == pyautogui_results:
        print("✅ Results match - no duplication detected")
    else:
        print("⚠️  Results differ - potential duplication detected")
        print(f"Campaign: {campaign_results}")
        print(f"PyAutoGUI: {pyautogui_results}")
    
    print("\n" + "=" * 50)
    print("🔍 Messaging flow debug complete!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Please check the messaging system dependencies")
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Please check the system configuration")

