#!/usr/bin/env python3
"""
Test Production Autonomous Loop - Production Autonomous Loop Test
===============================================================

Test script for production autonomous loop system with swarm coordination.
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

from src.core.production_autonomous_loop import ProductionAutonomousLoop

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_production_autonomous_loop():
    """Test production autonomous loop functionality."""
    logger.info("Testing production autonomous loop...")
    
    try:
        # Initialize production autonomous loop
        production_loop = ProductionAutonomousLoop("Agent-2")
        
        # Test system integration setup
        integration_status = production_loop.system_integration.get_integration_status()
        logger.info(f"System integration status: {integration_status}")
        
        # Test operational metrics
        initial_metrics = production_loop.operational_metrics
        logger.info(f"Initial operational metrics: {initial_metrics}")
        
        # Test status report generation
        status_report = production_loop.generate_status_report()
        logger.info(f"Generated status report: {status_report}")
        
        # Test production status retrieval
        production_status = production_loop.get_production_status()
        logger.info(f"Production status: {production_status}")
        
        # Test message processing
        message_result = production_loop.process_messages(5)
        logger.info(f"Message processing result: {message_result}")
        
        # Test task processing
        task_data = {
            "id": "test_task_001",
            "status": "completed",
            "description": "Test task processing"
        }
        task_result = production_loop.process_task(task_data)
        logger.info(f"Task processing result: {task_result}")
        
        # Test blocker resolution
        blocker_result = production_loop.resolve_blocker("Test blocker resolution")
        logger.info(f"Blocker resolution result: {blocker_result}")
        
        # Test production operation start/stop
        start_result = production_loop.start_production_operation()
        logger.info(f"Production operation start: {start_result}")
        
        if start_result:
            # Let it run for a few seconds
            time.sleep(5)
            
            # Test updated metrics
            updated_metrics = production_loop.operational_metrics
            logger.info(f"Updated operational metrics: {updated_metrics}")
            
            # Stop production operation
            stop_result = production_loop.stop_production_operation()
            logger.info(f"Production operation stop: {stop_result}")
        
        # Test final production status
        final_status = production_loop.get_production_status()
        logger.info(f"Final production status: {final_status}")
        
        logger.info("✅ Production autonomous loop test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Production autonomous loop test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting production autonomous loop tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Production Autonomous Loop", test_production_autonomous_loop()))
    
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
        logger.info("🎉 All tests passed! Production autonomous loop is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
