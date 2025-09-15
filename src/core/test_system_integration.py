#!/usr/bin/env python3
"""
Test System Integration - Autonomous Loop System Integration Test
================================================================

Test script for autonomous loop system integration with existing infrastructure.
Part of the autonomous loop system integration implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.autonomous_loop_system_integration import AutonomousLoopSystemIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_messaging_callback(message: str) -> bool:
    """Test messaging callback function."""
    logger.info(f"Messaging callback received: {message}")
    return True


def test_coordinate_callback(coordinates: str) -> bool:
    """Test coordinate callback function."""
    logger.info(f"Coordinate callback received: {coordinates}")
    return True


def test_swarm_callback(swarm_data: str) -> bool:
    """Test swarm coordination callback function."""
    logger.info(f"Swarm callback received: {swarm_data}")
    return True


def test_autonomous_loop_system_integration():
    """Test autonomous loop system integration functionality."""
    logger.info("Testing autonomous loop system integration...")
    
    try:
        # Initialize system integration
        system_integration = AutonomousLoopSystemIntegration("Agent-2")
        
        # Set integration callbacks
        system_integration.set_messaging_callback(test_messaging_callback)
        system_integration.set_coordinate_callback(test_coordinate_callback)
        system_integration.set_swarm_callback(test_swarm_callback)
        
        # Test individual integrations
        autonomous_loop_result = system_integration.integrate_autonomous_loop()
        logger.info(f"Autonomous loop integration: {autonomous_loop_result}")
        
        continuous_autonomy_result = system_integration.integrate_continuous_autonomy()
        logger.info(f"Continuous autonomy integration: {continuous_autonomy_result}")
        
        validator_result = system_integration.integrate_validator()
        logger.info(f"Validator integration: {validator_result}")
        
        messaging_result = system_integration.integrate_messaging_system()
        logger.info(f"Messaging system integration: {messaging_result}")
        
        coordinate_result = system_integration.integrate_coordinate_system()
        logger.info(f"Coordinate system integration: {coordinate_result}")
        
        swarm_result = system_integration.integrate_swarm_coordination()
        logger.info(f"Swarm coordination integration: {swarm_result}")
        
        # Test full integration
        full_integration_results = system_integration.execute_full_integration()
        logger.info(f"Full integration results: {full_integration_results}")
        
        # Test integration status
        status = system_integration.get_integration_status()
        logger.info(f"Integration status: {status}")
        
        # Test autonomous operation start/stop
        start_result = system_integration.start_autonomous_operation()
        logger.info(f"Autonomous operation start: {start_result}")
        
        if start_result:
            # Let it run for a few seconds
            time.sleep(3)
            
            # Stop autonomous operation
            stop_result = system_integration.stop_autonomous_operation()
            logger.info(f"Autonomous operation stop: {stop_result}")
        
        logger.info("✅ Autonomous loop system integration test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Autonomous loop system integration test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting autonomous loop system integration tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Autonomous Loop System Integration", test_autonomous_loop_system_integration()))
    
    # Report results
    logger.info("\n📊 Test Results Summary:")
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info(f"\n🎯 Overall Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Autonomous loop system integration is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
