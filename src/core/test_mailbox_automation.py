#!/usr/bin/env python3
"""
Test Mailbox Automation - Mailbox Processing Automation Test
===========================================================

Test script for mailbox processing automation system.
Part of the mailbox processing automation implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.mailbox_processing_automation import MailboxProcessor, MailboxMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_mailbox_processor_initialization():
    """Test mailbox processor initialization."""
    logger.info("Testing mailbox processor initialization...")
    
    try:
        # Initialize processor
        processor = MailboxProcessor("Agent-2")
        
        # Verify initialization
        assert processor.agent_id == "Agent-2"
        assert processor.workspace_path.name == "Agent-2"
        assert processor.inbox_path.exists()
        assert processor.processed_path.exists()
        
        # Check metrics
        metrics = processor.get_metrics()
        assert metrics["total_processed"] == 0
        assert metrics["successful_processing"] == 0
        assert metrics["failed_processing"] == 0
        
        logger.info("✅ Mailbox processor initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Mailbox processor initialization test failed: {e}")
        return False


def test_mailbox_message():
    """Test mailbox message functionality."""
    logger.info("Testing mailbox message functionality...")
    
    try:
        # Create test message
        test_path = Path("test_message.md")
        test_content = "Test message content"
        message = MailboxMessage(test_path, test_content)
        
        # Verify message properties
        assert message.file_path == test_path
        assert message.content == test_content
        assert message.processed_at is None
        assert message.processing_result is None
        
        # Mark as processed
        message.mark_processed("success")
        assert message.processed_at is not None
        assert message.processing_result == "success"
        
        # Test to_dict conversion
        message_dict = message.to_dict()
        assert message_dict["file_path"] == str(test_path)
        assert message_dict["content"] == test_content
        assert message_dict["processing_result"] == "success"
        
        logger.info("✅ Mailbox message test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Mailbox message test failed: {e}")
        return False


def test_message_processing():
    """Test message processing functionality."""
    logger.info("Testing message processing functionality...")
    
    try:
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test inbox and processed directories
            inbox_dir = temp_path / "inbox"
            processed_dir = temp_path / "inbox" / "processed"
            inbox_dir.mkdir(parents=True)
            processed_dir.mkdir()
            
            # Create test message files
            a2a_message = """============================================================
[A2A] MESSAGE
============================================================
FROM: Agent-1
TO: Agent-2
Priority: NORMAL
Tags: GENERAL
------------------------------------------------------------
Test A2A message for processing
------------------------------------------------------------
"""
            
            directive_message = """DIRECTIVE: Test directive message
This is a test directive message for processing automation.
"""
            
            # Write test messages
            a2a_file = inbox_dir / "a2a_message.md"
            directive_file = inbox_dir / "directive_message.md"
            
            a2a_file.write_text(a2a_message)
            directive_file.write_text(directive_message)
            
            # Initialize processor with temporary path
            processor = MailboxProcessor("Agent-2")
            processor.inbox_path = inbox_dir
            processor.processed_path = processed_dir
            
            # Test scanning inbox
            messages = processor.scan_inbox()
            assert len(messages) == 2
            
            # Test message processing
            results = processor.process_all_messages()
            assert results["success"] == True
            assert results["messages_processed"] == 2
            assert results["messages_failed"] == 0
            
            # Verify messages moved to processed
            assert not a2a_file.exists()
            assert not directive_file.exists()
            assert (processed_dir / "a2a_message.md").exists()
            assert (processed_dir / "directive_message.md").exists()
            
        logger.info("✅ Message processing test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Message processing test failed: {e}")
        return False


def test_message_info_extraction():
    """Test message information extraction."""
    logger.info("Testing message information extraction...")
    
    try:
        processor = MailboxProcessor("Agent-2")
        
        # Test A2A message extraction
        a2a_content = """============================================================
[A2A] MESSAGE
============================================================
FROM: Agent-1
TO: Agent-2
Priority: HIGH
Tags: COORDINATION WORKFLOW
------------------------------------------------------------
Test A2A message content
------------------------------------------------------------
"""
        
        info = processor._extract_message_info(a2a_content)
        assert info["type"] == "A2A"
        assert info["from_agent"] == "Agent-1"
        assert info["to_agent"] == "Agent-2"
        assert info["priority"] == "HIGH"
        assert "COORDINATION" in info["tags"]
        assert "WORKFLOW" in info["tags"]
        
        # Test directive message extraction
        directive_content = "DIRECTIVE: Test directive message"
        info = processor._extract_message_info(directive_content)
        assert info["type"] == "DIRECTIVE"
        
        # Test coordination message extraction
        coord_content = "COORDINATION: Test coordination message"
        info = processor._extract_message_info(coord_content)
        assert info["type"] == "COORDINATION"
        
        logger.info("✅ Message information extraction test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Message information extraction test failed: {e}")
        return False


def test_processing_metrics():
    """Test processing metrics functionality."""
    logger.info("Testing processing metrics functionality...")
    
    try:
        processor = MailboxProcessor("Agent-2")
        
        # Initial metrics
        metrics = processor.get_metrics()
        assert metrics["total_processed"] == 0
        assert metrics["successful_processing"] == 0
        assert metrics["failed_processing"] == 0
        assert metrics["last_processing"] is None
        
        # Test report generation
        report = processor.generate_report()
        assert "MAILBOX PROCESSING AUTOMATION REPORT" in report
        assert "Agent-2" in report
        assert "Total Processed: 0" in report
        
        logger.info("✅ Processing metrics test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Processing metrics test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting mailbox processing automation tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Mailbox Processor Initialization", test_mailbox_processor_initialization()))
    test_results.append(("Mailbox Message Functionality", test_mailbox_message()))
    test_results.append(("Message Processing", test_message_processing()))
    test_results.append(("Message Information Extraction", test_message_info_extraction()))
    test_results.append(("Processing Metrics", test_processing_metrics()))
    
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
        logger.info("🎉 All tests passed! Mailbox processing automation is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
