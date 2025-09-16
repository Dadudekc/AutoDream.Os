#!/usr/bin/env python3
"""
Test Standard Message Reminder - Standard Message Reminder Test
==============================================================

Test script for standard message reminder system.
Part of the autonomous workflow documentation implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.standard_message_reminder import StandardMessageReminder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_message_reminder_initialization():
    """Test standard message reminder system initialization."""
    logger.info("Testing standard message reminder system initialization...")
    
    try:
        # Initialize reminder system
        reminder = StandardMessageReminder()
        
        # Verify initialization
        assert reminder.standard_reminder is not None
        assert len(reminder.message_templates) == 5
        
        # Check available templates
        templates = reminder.get_available_templates()
        expected_templates = ["task_completion", "status_update", "blocker_escalation", "coordination", "general"]
        
        for template in expected_templates:
            assert template in templates
        
        logger.info("✅ Standard message reminder initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Standard message reminder initialization test failed: {e}")
        return False


def test_task_completion_message():
    """Test task completion message formatting."""
    logger.info("Testing task completion message formatting...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Format task completion message
        message = reminder.format_task_completion(
            from_agent="Agent-2",
            to_agent="Agent-4",
            task_name="task_claiming_automation",
            success_rate=100,
            phase_count=3,
            phase_summary="Phase 1: Design framework, Phase 2: Implementation, Phase 3: Validation",
            feature_list="Task container, automated claiming, dependency validation",
            integration_status="autonomous loop integration"
        )
        
        # Verify message structure
        assert "TASK CLAIMING AUTOMATION IMPLEMENTATION COMPLETED" in message
        assert "Agent-2" in message
        assert "Agent-4" in message
        assert "100% success rate" in message
        assert "3 PHASES COMPLETED" in message
        assert reminder.standard_reminder in message
        
        logger.info("✅ Task completion message test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Task completion message test failed: {e}")
        return False


def test_status_update_message():
    """Test status update message formatting."""
    logger.info("Testing status update message formatting...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Format status update message
        message = reminder.format_status_update(
            from_agent="Agent-2",
            to_agent="Agent-4",
            task_id="task_claiming_automation",
            phase_number=2,
            phase_description="Implement task claiming automation system",
            progress_description="Created automation module and test suite",
            estimated_time="next cycle"
        )
        
        # Verify message structure
        assert "STATUS UPDATE" in message
        assert "Agent-2" in message
        assert "Agent-4" in message
        assert "task_claiming_automation" in message
        assert "Phase 2" in message
        assert reminder.standard_reminder in message
        
        logger.info("✅ Status update message test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Status update message test failed: {e}")
        return False


def test_blocker_escalation_message():
    """Test blocker escalation message formatting."""
    logger.info("Testing blocker escalation message formatting...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Format blocker escalation message
        message = reminder.format_blocker_escalation(
            from_agent="Agent-2",
            to_agent="Agent-4",
            task_id="test_task",
            phase_number=1,
            issue_description="Integration test failing",
            solutions_attempted="Retried 3 times, checked dependencies"
        )
        
        # Verify message structure
        assert "BLOCKER ESCALATION" in message
        assert "Agent-2" in message
        assert "Agent-4" in message
        assert "test_task" in message
        assert "Phase 1" in message
        assert "Integration test failing" in message
        assert reminder.standard_reminder in message
        
        logger.info("✅ Blocker escalation message test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Blocker escalation message test failed: {e}")
        return False


def test_coordination_message():
    """Test coordination message formatting."""
    logger.info("Testing coordination message formatting...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Format coordination message
        message = reminder.format_coordination(
            from_agent="Agent-2",
            to_agent="Agent-6",
            coordination_content="Ready to collaborate on messaging system enhancements",
            priority="NORMAL"
        )
        
        # Verify message structure
        assert "Agent-2" in message
        assert "Agent-6" in message
        assert "Ready to collaborate" in message
        assert reminder.standard_reminder in message
        
        logger.info("✅ Coordination message test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Coordination message test failed: {e}")
        return False


def test_message_validation():
    """Test message format validation."""
    logger.info("Testing message format validation...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Test valid message
        valid_message = reminder.format_task_completion(
            from_agent="Agent-2",
            to_agent="Agent-4",
            task_name="test_task",
            success_rate=100,
            phase_count=1,
            phase_summary="Test phase",
            feature_list="Test features"
        )
        
        validation_result = reminder.validate_message_format(valid_message)
        assert validation_result["valid"] == True
        assert validation_result["compliance_score"] == 100
        
        # Test invalid message (missing sections)
        invalid_message = "This is not a properly formatted message"
        validation_result = reminder.validate_message_format(invalid_message)
        assert validation_result["valid"] == False
        assert validation_result["compliance_score"] < 100
        
        logger.info("✅ Message validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Message validation test failed: {e}")
        return False


def test_reminder_addition():
    """Test adding reminder to existing message."""
    logger.info("Testing reminder addition to existing message...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Test message without reminder
        message_without_reminder = """============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-2
📥 TO: Agent-4
Priority: NORMAL
Tags: GENERAL
------------------------------------------------------------
Test message content
------------------------------------------------------------"""
        
        # Add reminder
        message_with_reminder = reminder.add_reminder_to_message(message_without_reminder)
        
        # Verify reminder was added
        assert reminder.standard_reminder in message_with_reminder
        
        # Test message that already has reminder
        message_with_existing_reminder = message_with_reminder
        result = reminder.add_reminder_to_message(message_with_existing_reminder)
        
        # Should not duplicate reminder
        reminder_count = result.count(reminder.standard_reminder)
        assert reminder_count == 1
        
        logger.info("✅ Reminder addition test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Reminder addition test failed: {e}")
        return False


def test_report_generation():
    """Test system report generation."""
    logger.info("Testing system report generation...")
    
    try:
        reminder = StandardMessageReminder()
        
        # Generate report
        report = reminder.generate_report()
        
        # Verify report content
        assert "STANDARD MESSAGE REMINDER SYSTEM REPORT" in report
        assert "Available Templates" in report
        assert "Standard Reminder" in report
        assert "OPERATIONAL" in report
        
        logger.info("✅ Report generation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Report generation test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting standard message reminder tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Message Reminder Initialization", test_message_reminder_initialization()))
    test_results.append(("Task Completion Message", test_task_completion_message()))
    test_results.append(("Status Update Message", test_status_update_message()))
    test_results.append(("Blocker Escalation Message", test_blocker_escalation_message()))
    test_results.append(("Coordination Message", test_coordination_message()))
    test_results.append(("Message Validation", test_message_validation()))
    test_results.append(("Reminder Addition", test_reminder_addition()))
    test_results.append(("Report Generation", test_report_generation()))
    
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
        logger.info("🎉 All tests passed! Standard message reminder system is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


