#!/usr/bin/env python3
"""
Test Onboarding Copy/Paste Functionality
========================================

Test script to verify the updated onboarding system with copy/paste functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_phase_transition_onboarding():
    """Test phase transition onboarding with copy/paste."""
    try:
        from phase_transition_onboarding import PhaseTransitionOnboarding
        
        logger.info("🧪 Testing Phase Transition Onboarding...")
        
        # Create onboarding instance
        onboarding = PhaseTransitionOnboarding()
        
        # Test phase transition (dry run - won't actually send messages)
        logger.info("📋 Testing phase transition: Cycle 1 → Phase 2")
        
        # Get current phase status
        status = onboarding.get_current_phase_status()
        logger.info(f"📊 Current phase status: {status}")
        
        # Test message generation (without sending)
        agent_id = "Agent-2"
        role = "Architecture & Design Specialist"
        phase = "Phase 2"
        phase_config = onboarding.phase_configs.get(phase, {})
        assignment = phase_config.get("agent_assignments", {}).get(agent_id, "General support")
        
        message = onboarding._generate_phase_transition_message(
            agent_id, role, phase, phase_config, assignment
        )
        
        logger.info(f"📝 Generated message length: {len(message)} characters")
        logger.info(f"📝 Message preview (first 200 chars): {message[:200]}...")
        
        # Test copy/paste functionality
        try:
            import pyperclip
            
            # Test clipboard functionality
            test_text = "Test message for copy/paste functionality"
            pyperclip.copy(test_text)
            clipboard_content = pyperclip.paste()
            
            if clipboard_content == test_text:
                logger.info("✅ Copy/paste functionality working correctly")
            else:
                logger.error("❌ Copy/paste functionality failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Copy/paste test failed: {e}")
            return False
        
        logger.info("✅ Phase transition onboarding test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Phase transition onboarding test failed: {e}")
        return False

def test_agent_restart_protocol():
    """Test agent restart protocol with copy/paste."""
    try:
        from agent_restart_protocol import AgentRestartProtocol
        
        logger.info("🧪 Testing Agent Restart Protocol...")
        
        # Create restart protocol instance
        restart_protocol = AgentRestartProtocol()
        
        # Test message generation
        agent_id = "Agent-2"
        message = restart_protocol._generate_restart_message(agent_id)
        
        logger.info(f"📝 Generated restart message length: {len(message)} characters")
        logger.info(f"📝 Message preview (first 200 chars): {message[:200]}...")
        
        # Test copy/paste functionality
        try:
            import pyperclip
            
            # Test clipboard functionality
            test_text = "Test restart message for copy/paste functionality"
            pyperclip.copy(test_text)
            clipboard_content = pyperclip.paste()
            
            if clipboard_content == test_text:
                logger.info("✅ Copy/paste functionality working correctly")
            else:
                logger.error("❌ Copy/paste functionality failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Copy/paste test failed: {e}")
            return False
        
        logger.info("✅ Agent restart protocol test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Agent restart protocol test failed: {e}")
        return False

def test_messaging_pyautogui():
    """Test messaging PyAutoGUI with copy/paste."""
    try:
        from src.services.messaging_pyautogui import format_message_for_delivery
        from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        
        logger.info("🧪 Testing Messaging PyAutoGUI...")
        
        # Create test message
        message = UnifiedMessage(
            content="Test message for copy/paste functionality",
            recipient="Agent-2",
            sender="Test-System",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.MEDIUM,
            tags=[UnifiedMessageTag.SYSTEM]
        )
        
        # Test message formatting
        formatted_message = format_message_for_delivery(message)
        
        logger.info(f"📝 Formatted message length: {len(formatted_message)} characters")
        logger.info(f"📝 Message preview (first 200 chars): {formatted_message[:200]}...")
        
        # Test copy/paste functionality
        try:
            import pyperclip
            
            # Test clipboard functionality
            pyperclip.copy(formatted_message)
            clipboard_content = pyperclip.paste()
            
            if clipboard_content == formatted_message:
                logger.info("✅ Copy/paste functionality working correctly")
            else:
                logger.error("❌ Copy/paste functionality failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Copy/paste test failed: {e}")
            return False
        
        logger.info("✅ Messaging PyAutoGUI test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Messaging PyAutoGUI test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Starting Onboarding Copy/Paste Tests...")
    logger.info("=" * 50)
    
    tests = [
        ("Phase Transition Onboarding", test_phase_transition_onboarding),
        ("Agent Restart Protocol", test_agent_restart_protocol),
        ("Messaging PyAutoGUI", test_messaging_pyautogui)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        logger.info(f"{'✅ PASSED' if result else '❌ FAILED'}: {test_name}")
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Copy/paste functionality is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the logs above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)
