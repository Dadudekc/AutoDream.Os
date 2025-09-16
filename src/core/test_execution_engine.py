#!/usr/bin/env python3
"""
Test Execution Engine - Self-Validation Execution Engine Test
============================================================

Test script for self-validation execution engine.
Part of the self-validation protocol implementation.

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

from src.core.self_validation_execution_engine import SelfValidationExecutionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_execution_engine_initialization():
    """Test execution engine initialization."""
    logger.info("Testing execution engine initialization...")
    
    try:
        # Initialize execution engine
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Verify initialization
        assert engine.agent_id == "Agent-2"
        assert engine.workspace_path.name == "Agent-2"
        assert len(engine.validation_protocol.validation_rules) > 0
        
        # Check execution metrics
        metrics = engine.execution_metrics
        assert metrics["total_executions"] == 0
        assert metrics["successful_validations"] == 0
        assert metrics["failed_validations"] == 0
        
        logger.info("✅ Execution engine initialization test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Execution engine initialization test failed: {e}")
        return False


def test_current_task_validation():
    """Test current task validation."""
    logger.info("Testing current task validation...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Test with no working tasks file
        result = engine.validate_current_task()
        assert "success" in result
        assert "message" in result
        assert "details" in result
        
        logger.info("✅ Current task validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Current task validation test failed: {e}")
        return False


def test_v2_compliance_validation():
    """Test V2 compliance validation."""
    logger.info("Testing V2 compliance validation...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
            # Create a V2 compliant file
            for i in range(50):
                temp_file.write(f"# Line {i+1}\n")
            compliant_file_path = temp_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
            # Create a V2 violation file
            for i in range(500):
                temp_file.write(f"# Line {i+1}\n")
            violation_file_path = temp_file.name
        
        compliant_path = Path(compliant_file_path)
        violation_path = Path(violation_file_path)
        
        # Add custom V2 compliance rules
        from src.core.self_validation_protocol import FileSizeRule
        engine.validation_protocol.add_rule(FileSizeRule(compliant_path, max_size=100))
        engine.validation_protocol.add_rule(FileSizeRule(violation_path, max_size=100))
        
        # Test V2 compliance validation
        result = engine.validate_v2_compliance()
        
        assert "success" in result
        assert "message" in result
        assert "details" in result
        
        # Clean up
        compliant_path.unlink()
        violation_path.unlink()
        
        logger.info("✅ V2 compliance validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ V2 compliance validation test failed: {e}")
        return False


def test_file_system_validation():
    """Test file system validation."""
    logger.info("Testing file system validation...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Create temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("test content")
            temp_file_path = temp_file.name
        
        temp_path = Path(temp_file_path)
        
        # Add custom file existence rule
        from src.core.self_validation_protocol import FileExistenceRule
        engine.validation_protocol.add_rule(FileExistenceRule(temp_path))
        
        # Test file system validation
        result = engine.validate_file_system_integrity()
        
        assert "success" in result
        assert "message" in result
        assert "details" in result
        
        # Clean up
        temp_path.unlink()
        
        logger.info("✅ File system validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ File system validation test failed: {e}")
        return False


def test_comprehensive_validation():
    """Test comprehensive validation execution."""
    logger.info("Testing comprehensive validation execution...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Execute comprehensive validation
        result = engine.execute_comprehensive_validation()
        
        # Verify result structure
        assert "overall_success" in result
        assert "execution_timestamp" in result
        assert "execution_duration" in result
        assert "validation_domains" in result
        assert "summary" in result
        
        # Verify validation domains
        domains = result["validation_domains"]
        assert "current_task" in domains
        assert "v2_compliance" in domains
        assert "file_system" in domains
        assert "protocol" in domains
        
        # Check execution metrics update
        metrics = engine.execution_metrics
        assert metrics["total_executions"] == 1
        
        logger.info("✅ Comprehensive validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Comprehensive validation test failed: {e}")
        return False


def test_execution_report():
    """Test execution report generation."""
    logger.info("Testing execution report generation...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Execute validation to generate history
        engine.execute_comprehensive_validation()
        
        # Generate report
        report = engine.generate_execution_report()
        
        # Verify report content
        assert "SELF-VALIDATION EXECUTION ENGINE REPORT" in report
        assert "Agent-2" in report
        assert "Total Executions: 1" in report
        
        logger.info("✅ Execution report test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Execution report test failed: {e}")
        return False


def test_execution_status():
    """Test execution status retrieval."""
    logger.info("Testing execution status retrieval...")
    
    try:
        engine = SelfValidationExecutionEngine("Agent-2")
        
        # Get execution status
        status = engine.get_execution_status()
        
        # Verify status structure
        assert "agent_id" in status
        assert "execution_metrics" in status
        assert "validation_rules_count" in status
        assert "last_execution" in status
        assert "status" in status
        
        assert status["agent_id"] == "Agent-2"
        assert status["status"] == "operational"
        
        logger.info("✅ Execution status test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Execution status test failed: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🚀 Starting self-validation execution engine tests...")
    
    test_results = []
    
    # Run tests
    test_results.append(("Execution Engine Initialization", test_execution_engine_initialization()))
    test_results.append(("Current Task Validation", test_current_task_validation()))
    test_results.append(("V2 Compliance Validation", test_v2_compliance_validation()))
    test_results.append(("File System Validation", test_file_system_validation()))
    test_results.append(("Comprehensive Validation", test_comprehensive_validation()))
    test_results.append(("Execution Report", test_execution_report()))
    test_results.append(("Execution Status", test_execution_status()))
    
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
        logger.info("🎉 All tests passed! Self-validation execution engine is ready.")
        return 0
    else:
        logger.error("💥 Some tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())





