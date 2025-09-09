#!/usr/bin/env python3
"""
Test PyAutoGUI Messaging System
Send test message to Agent-2 (myself) and debug until received
"""

import sys
import os
import time
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pyautogui_messaging():
    """Test PyAutoGUI messaging by sending message to Agent-2."""
    try:
        # Import messaging system
        from src.services.messaging_pyautogui import PyAutoGUIMessagingDelivery
        from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        
        logger.info("🔍 Testing PyAutoGUI messaging system...")
        
        # Create messaging delivery instance
        messaging = PyAutoGUIMessagingDelivery()
        
        # Create test message to Agent-2 (myself)
        test_message = UnifiedMessage(
            content="🚨 TEST MESSAGE - PyAutoGUI messaging system test from Agent-2 to Agent-2",
            sender="Agent-2",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.COORDINATION],
            metadata={"delivery_method": "PYAUTOGUI", "test": True}
        )
        
        logger.info(f"📤 Sending test message: {test_message.content}")
        
        # Send message
        result = messaging.send_message(test_message)
        
        if result:
            logger.info("✅ Message sent successfully!")
            logger.info("🔍 Waiting for message to be received...")
            logger.info("📋 Check your inbox for the test message")
            return True
        else:
            logger.error("❌ Failed to send message")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.info("🔧 Installing required packages...")
        os.system("python -m pip install -q pyautogui pyperclip")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def debug_messaging_system():
    """Debug the messaging system step by step."""
    logger.info("🔧 Debugging PyAutoGUI messaging system...")
    
    # Check PyAutoGUI availability
    try:
        import pyautogui
        logger.info("✅ PyAutoGUI available")
    except ImportError:
        logger.error("❌ PyAutoGUI not available")
        logger.info("🔧 Installing PyAutoGUI...")
        os.system("python -m pip install -q pyautogui")
        return False
    
    # Check pyperclip availability
    try:
        import pyperclip
        logger.info("✅ Pyperclip available")
    except ImportError:
        logger.error("❌ Pyperclip not available")
        logger.info("🔧 Installing pyperclip...")
        os.system("python -m pip install -q pyperclip")
        return False
    
    # Check coordinate loader
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        agents = loader.get_all_agents()
        logger.info(f"✅ Coordinate loader working, agents: {agents}")
        
        # Check Agent-2 coordinates
        if "Agent-2" in agents:
            coords = loader.get_chat_coordinates("Agent-2")
            logger.info(f"✅ Agent-2 coordinates: {coords}")
        else:
            logger.error("❌ Agent-2 not found in coordinates")
            return False
            
    except Exception as e:
        logger.error(f"❌ Coordinate loader error: {e}")
        return False
    
    # Check messaging core
    try:
        from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority
        logger.info("✅ Messaging core available")
    except Exception as e:
        logger.error(f"❌ Messaging core error: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    logger.info("🚀 Starting PyAutoGUI messaging test...")
    
    # Debug first
    if not debug_messaging_system():
        logger.error("❌ Debug failed, cannot proceed")
        return False
    
    # Test messaging
    if test_pyautogui_messaging():
        logger.info("✅ Test completed successfully!")
        logger.info("🔍 Check your inbox for the test message")
        return True
    else:
        logger.error("❌ Test failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
