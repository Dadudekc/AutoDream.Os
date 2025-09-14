#!/usr/bin/env python3
"""
Phase 3 Service Layer Testing - V2 Compliant Service Integration Test
====================================================================

Test script to validate Phase 3 service layer consolidation and integration.

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

def test_unified_messaging_service():
    """Test unified messaging service."""
    logger.info("🧪 Testing Unified Messaging Service...")
    
    try:
        from src.services.messaging.unified_service import (
            get_unified_messaging_service,
            send_message_to_agent,
            broadcast_to_swarm,
            get_messaging_status
        )
        
        # Test service initialization
        service = get_unified_messaging_service()
        logger.info("✅ Unified messaging service initialized")
        
        # Test status check
        status = get_messaging_status()
        logger.info(f"✅ Service status: {status['service_available']}")
        
        # Test agent listing
        agents = service.list_available_agents()
        logger.info(f"✅ Available agents: {len(agents)}")
        
        # Test metrics
        metrics = service.get_metrics()
        logger.info(f"✅ Metrics retrieved: {metrics}")
        
        logger.info("✅ Unified Messaging Service tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Unified Messaging Service test failed: {e}")
        return False

def test_onboarding_service():
    """Test onboarding service."""
    logger.info("🧪 Testing Onboarding Service...")
    
    try:
        from src.services.messaging.onboarding.onboarding_service import (
            get_onboarding_service,
            onboard_agent,
            onboard_swarm
        )
        
        # Test service initialization
        service = get_onboarding_service()
        logger.info("✅ Onboarding service initialized")
        
        # Test status check
        status = service.get_onboarding_status()
        logger.info(f"✅ Onboarding status: {status['total_agents']} agents")
        
        # Test history
        history = service.get_onboarding_history()
        logger.info(f"✅ Onboarding history: {len(history)} entries")
        
        logger.info("✅ Onboarding Service tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Onboarding Service test failed: {e}")
        return False

def test_message_generator():
    """Test message generator."""
    logger.info("🧪 Testing Message Generator...")
    
    try:
        from src.services.messaging.onboarding.message_generator import (
            get_message_generator,
            generate_onboarding_message,
            generate_coordination_message,
            MessageStyle
        )
        
        # Test service initialization
        generator = get_message_generator()
        logger.info("✅ Message generator initialized")
        
        # Test onboarding message generation
        message = generate_onboarding_message("Agent-1", MessageStyle.STANDARD)
        logger.info(f"✅ Onboarding message generated: {len(message)} characters")
        
        # Test coordination message generation
        coord_message = generate_coordination_message("Agent-1", "Test task", "normal")
        logger.info(f"✅ Coordination message generated: {len(coord_message)} characters")
        
        logger.info("✅ Message Generator tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Message Generator test failed: {e}")
        return False

def test_broadcast_service():
    """Test broadcast service."""
    logger.info("🧪 Testing Broadcast Service...")
    
    try:
        from src.services.messaging.broadcast.broadcast_service import (
            get_broadcast_service,
            broadcast_message,
            broadcast_emergency_alert,
            BroadcastType,
            BroadcastPriority
        )
        
        # Test service initialization
        service = get_broadcast_service()
        logger.info("✅ Broadcast service initialized")
        
        # Test metrics
        metrics = service.get_broadcast_metrics()
        logger.info(f"✅ Broadcast metrics: {metrics}")
        
        # Test history
        history = service.get_broadcast_history(limit=10)
        logger.info(f"✅ Broadcast history: {len(history)} entries")
        
        logger.info("✅ Broadcast Service tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Broadcast Service test failed: {e}")
        return False

def test_coordination_service():
    """Test coordination service."""
    logger.info("🧪 Testing Coordination Service...")
    
    try:
        from src.services.messaging.broadcast.coordination_service import (
            get_coordination_service,
            assign_task,
            complete_task,
            TaskPriority
        )
        
        # Test service initialization
        service = get_coordination_service()
        logger.info("✅ Coordination service initialized")
        
        # Test agent status
        status = service.get_agent_status()
        logger.info(f"✅ Agent status: {status['total_agents']} agents")
        
        # Test task status
        task_status = service.get_task_status()
        logger.info(f"✅ Task status: {task_status['active_tasks']} active tasks")
        
        # Test metrics
        metrics = service.get_coordination_metrics()
        logger.info(f"✅ Coordination metrics: {metrics}")
        
        logger.info("✅ Coordination Service tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Coordination Service test failed: {e}")
        return False

def test_cli_integration():
    """Test CLI integration."""
    logger.info("🧪 Testing CLI Integration...")
    
    try:
        from src.services.messaging.cli.messaging_cli import UnifiedMessagingCLI
        
        # Test CLI initialization
        cli = UnifiedMessagingCLI()
        logger.info("✅ CLI initialized")
        
        # Test parser creation
        parser = cli._create_parser()
        logger.info("✅ CLI parser created")
        
        logger.info("✅ CLI Integration tests passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ CLI Integration test failed: {e}")
        return False

def main():
    """Main test execution."""
    logger.info("🚀 Starting Phase 3 Service Layer Testing...")
    logger.info("=" * 60)
    
    tests = [
        ("Unified Messaging Service", test_unified_messaging_service),
        ("Onboarding Service", test_onboarding_service),
        ("Message Generator", test_message_generator),
        ("Broadcast Service", test_broadcast_service),
        ("Coordination Service", test_coordination_service),
        ("CLI Integration", test_cli_integration),
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
    logger.info("📊 PHASE 3 SERVICE LAYER TEST RESULTS")
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
        logger.info("🎉 ALL TESTS PASSED - Phase 3 Service Layer is ready!")
        logger.info("🐝 WE ARE SWARM - Service consolidation successful! ⚡️")
        return 0
    else:
        logger.error(f"❌ {total - passed} tests failed - Review and fix issues")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)