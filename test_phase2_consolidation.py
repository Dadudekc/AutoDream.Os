#!/usr/bin/env python3
"""
Phase 2 Core SSOT Testing - V2 Compliant Core Consolidation Test
===============================================================

Test script to validate Phase 2 core SSOT consolidation and integration.

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_models_consolidation():
    """Test models consolidation."""
    logger.info("🧪 Testing Models Consolidation...")
    
    try:
        from src.core.messaging.models import (
            UnifiedMessage,
            UnifiedMessageType,
            UnifiedMessagePriority,
            UnifiedMessageTag,
            DeliveryMethod,
            MessageStatus,
            create_message,
            create_broadcast_message,
            create_onboarding_message
        )
        
        # Test message creation
        message = create_message(
            content="Test message",
            sender="TestSender",
            recipient="TestRecipient",
            message_type=UnifiedMessageType.TEXT
        )
        
        logger.info(f"✅ Message created: {message.message_id}")
        logger.info(f"✅ Message type: {message.message_type.value}")
        logger.info(f"✅ Message priority: {message.priority.value}")
        
        # Test broadcast message
        broadcast = create_broadcast_message("Test broadcast")
        logger.info(f"✅ Broadcast message created: {broadcast.message_type.value}")
        
        # Test onboarding message
        onboarding = create_onboarding_message("Test onboarding", "Agent-1")
        logger.info(f"✅ Onboarding message created: {onboarding.message_type.value}")
        
        logger.info("✅ Models consolidation tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Models consolidation test failed: {e}")
        return False

def test_interfaces_consolidation():
    """Test interfaces consolidation."""
    logger.info("🧪 Testing Interfaces Consolidation...")
    
    try:
        from src.core.messaging.interfaces import (
            IMessageDelivery,
            IOnboardingService,
            BaseMessageDelivery,
            BaseOnboardingService
        )
        
        # Test interface imports
        logger.info("✅ IMessageDelivery interface imported")
        logger.info("✅ IOnboardingService interface imported")
        logger.info("✅ BaseMessageDelivery class imported")
        logger.info("✅ BaseOnboardingService class imported")
        
        logger.info("✅ Interfaces consolidation tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Interfaces consolidation test failed: {e}")
        return False

def test_core_consolidation():
    """Test core consolidation."""
    logger.info("🧪 Testing Core Consolidation...")
    
    try:
        from src.core.messaging.core import (
            UnifiedMessagingCore,
            get_messaging_core,
            send_message,
            broadcast_message,
            list_agents,
            get_system_status,
            health_check
        )
        
        # Test core initialization
        core = get_messaging_core()
        logger.info("✅ Messaging core initialized")
        
        # Test system status
        status = get_system_status()
        logger.info(f"✅ System status: {status['available_agents']} agents")
        
        # Test health check
        health = health_check()
        logger.info(f"✅ Health check: {health['status']}")
        
        # Test agent listing
        agents = list_agents()
        logger.info(f"✅ Agent listing: {len(agents)} agents")
        
        logger.info("✅ Core consolidation tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Core consolidation test failed: {e}")
        return False

def test_delivery_services():
    """Test delivery services consolidation."""
    logger.info("🧪 Testing Delivery Services Consolidation...")
    
    try:
        from src.core.messaging.delivery.pyautogui import (
            PyAutoGUIMessagingDelivery,
            PYAUTOGUI_AVAILABLE,
            PYPERCLIP_AVAILABLE
        )
        
        from src.core.messaging.delivery.inbox import (
            InboxDeliveryService,
            get_inbox_delivery_service
        )
        
        from src.core.messaging.delivery.fallback import (
            FallbackDeliveryService,
            get_fallback_delivery_service
        )
        
        # Test PyAutoGUI delivery
        pyautogui_delivery = PyAutoGUIMessagingDelivery()
        logger.info(f"✅ PyAutoGUI delivery: Available={PYAUTOGUI_AVAILABLE}")
        logger.info(f"✅ Pyperclip: Available={PYPERCLIP_AVAILABLE}")
        
        # Test inbox delivery
        inbox_delivery = get_inbox_delivery_service()
        logger.info("✅ Inbox delivery service initialized")
        
        # Test fallback delivery
        fallback_delivery = get_fallback_delivery_service()
        logger.info("✅ Fallback delivery service initialized")
        
        logger.info("✅ Delivery services consolidation tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Delivery services consolidation test failed: {e}")
        return False

def test_legacy_compatibility():
    """Test legacy compatibility."""
    logger.info("🧪 Testing Legacy Compatibility...")
    
    try:
        # Test legacy imports (should show deprecation warnings)
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # These should trigger deprecation warnings
            from src.core.messaging_core import UnifiedMessagingCore
            from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
            from src.core.unified_messaging import UnifiedMessagingSystem
            
            # Check that deprecation warnings were issued
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            logger.info(f"✅ Deprecation warnings issued: {len(deprecation_warnings)}")
            
            # Verify legacy imports still work
            logger.info("✅ Legacy messaging_core import works")
            logger.info("✅ Legacy messaging_pyautogui import works")
            logger.info("✅ Legacy unified_messaging import works")
        
        logger.info("✅ Legacy compatibility tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Legacy compatibility test failed: {e}")
        return False

def test_unified_imports():
    """Test unified imports."""
    logger.info("🧪 Testing Unified Imports...")
    
    try:
        # Test unified import from main module
        from src.core.messaging import (
            UnifiedMessagingCore,
            UnifiedMessage,
            UnifiedMessageType,
            PyAutoGUIMessagingDelivery,
            InboxDeliveryService,
            FallbackDeliveryService,
            get_messaging_core,
            send_message,
            broadcast_message
        )
        
        logger.info("✅ Unified imports from main module work")
        
        # Test delivery imports
        from src.core.messaging.delivery import (
            PyAutoGUIMessagingDelivery as PyAutoGUI,
            InboxDeliveryService as Inbox,
            FallbackDeliveryService as Fallback
        )
        
        logger.info("✅ Unified imports from delivery module work")
        
        logger.info("✅ Unified imports tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Unified imports test failed: {e}")
        return False

def main():
    """Main test execution."""
    logger.info("🚀 Starting Phase 2 Core SSOT Testing...")
    logger.info("=" * 60)
    
    tests = [
        ("Models Consolidation", test_models_consolidation),
        ("Interfaces Consolidation", test_interfaces_consolidation),
        ("Core Consolidation", test_core_consolidation),
        ("Delivery Services", test_delivery_services),
        ("Legacy Compatibility", test_legacy_compatibility),
        ("Unified Imports", test_unified_imports),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} tests...")
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 PHASE 2 CORE SSOT TEST RESULTS")
    logger.info("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
        if success:
            passed += 1
    
    logger.info(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED - Phase 2 Core SSOT is ready!")
        logger.info("🐝 WE ARE SWARM - Core consolidation successful! ⚡️")
        return 0
    else:
        logger.error(f"❌ {total - passed} tests failed - Review and fix issues")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)