#!/usr/bin/env python3
"""
Test Autonomous Loop - Autonomous Loop Integration Test
=====================================================

Test script for autonomous loop integration and continuous autonomy behavior.
Part of the autonomous loop integration implementation.

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

from src.core.autonomous_loop_integration import AutonomousLoopIntegration
from src.core.continuous_autonomy_behavior import ContinuousAutonomyBehavior
from src.core.autonomous_loop_validator import AutonomousLoopValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_autonomous_loop_integration():
    """Test autonomous loop integration functionality."""
    logger.info("Testing autonomous loop integration...")
    
    try:
        # Initialize autonomous loop
        autonomous_loop = AutonomousLoopIntegration("Agent-2")
        
        # Test mailbox checking
        messages = autonomous_loop.check_mailbox()
        logger.info(f"Found {len(messages)} messages in mailbox")
        
        # Test task management
        current_task = autonomous_loop.get_current_task()
        available_tasks = autonomous_loop.get_available_tasks()
        pending_tasks = autonomous_loop.get_pending_tasks()
        
        logger.info(f"Current task: {current_task}")
        logger.info(f"Available tasks: {len(available_tasks)}")
        logger.info(f"Pending tasks: {len(pending_tasks)}")
        
        # Test autonomous cycle
        cycle_results = autonomous_loop.autonomous_loop_cycle()
        logger.info(f"Cycle results: {cycle_results}")
        
        logger.info("✅ Autonomous loop integration test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Autonomous loop integration test failed: {e}")
        return False


def test_continuous_autonomy_behavior():
    """Test continuous autonomy behavior functionality."""
    logger.info("Testing continuous autonomy behavior...")
    
    try:
        # Initialize continuous autonomy
        continuous_autonomy = ContinuousAutonomyBehavior("Agent-2")
        
        # Test status retrieval
        status = continuous_autonomy.get_status()
        logger.info(f"Initial status: {status}")
        
        # Test configuration
        continuous_autonomy.set_cycle_interval(30)
        continuous_autonomy.set_max_idle_cycles(3)
        
        # Test start/stop
        start_success = continuous_autonomy.start()
        logger.info(f"Start result: {start_success}")
        
        if start_success:
            # Let it run for a few seconds
            time.sleep(3)
            
            # Check status while running
            running_status = continuous_autonomy.get_status()
            logger.info(f"Running status: {running_status}")
            
            # Stop
            stop_success = continuous_autonomy.stop()
            logger.info(f"Stop result: {stop_success}")
        
        logger.info("✅ Continuous autonomy behavior test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Continuous autonomy behavior test failed: {e}")
        return False


def test_autonomous_loop_validator():
    """Test autonomous loop validator functionality."""
    logger.info("Testing autonomous loop validator...")
    
    try:
        # Initialize validator
        validator = AutonomousLoopValidator("Agent-2")
        
        # Test integration validation
        integration_results = validator.validate_integration()
        logger.info(f"Integration validation: {integration_results}")
        
        # Test behavior validation
        behavior_results = validator.validate_behavior()
        logger.info(f"Behavior validation: {behavior_results}")
        
        # Test full validation
        full_results = validator.run_full_validation()
        logger.info(f"Full validation: {full_results}")
        
        # Get validation report
        report = validator.get_validation_report()
        logger.info(f"Validation report: {report}")
        
        logger.info("✅ Autonomous loop validator test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Autonomous loop validator test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting autonomous loop integration tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Autonomous Loop Integration", test_autonomous_loop_integration()))
    test_results.append(("Continuous Autonomy Behavior", test_continuous_autonomy_behavior()))
    test_results.append(("Autonomous Loop Validator", test_autonomous_loop_validator()))
    
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
        logger.info("🎉 All tests passed! Autonomous loop integration is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
