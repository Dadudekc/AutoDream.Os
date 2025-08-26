#!/usr/bin/env python3
"""
Simple FSM Compliance Integration Test - Quick Validation

Quick validation script to check if the FSM compliance integration
module can be imported and basic functionality works.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_fsm_compliance_integration():
    """Test basic FSM compliance integration functionality."""
    try:
        print("🧪 Testing FSM Compliance Integration...")
        
        # Test import
        from fsm_compliance_integration import FSMComplianceIntegration
        print("✅ FSMComplianceIntegration imported successfully")
        
        # Test creation
        integration = FSMComplianceIntegration()
        print("✅ FSMComplianceIntegration created successfully")
        
        # Test health check
        health = integration.get_integration_health()
        print(f"✅ Integration health: {health['overall_health']}")
        
        # Test system status
        print(f"   FSM System: {health['fsm_system']['status']}")
        print(f"   Compliance System: {health['compliance_system']['status']}")
        print(f"   Integration Active: {health['integration']['active']}")
        
        # Test workflow listing
        workflows = integration.list_compliance_workflows()
        print(f"✅ Current workflows: {len(workflows)}")
        
        # Test report export
        report = integration.export_integration_report()
        if report:
            print("✅ Integration report exported successfully")
        else:
            print("❌ Failed to export integration report")
        
        print("🎉 FSM Compliance Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ FSM Compliance Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fsm_system_integration():
    """Test FSM system integration."""
    try:
        print("\n🧪 Testing FSM System Integration...")
        
        # Test FSM system import
        from fsm_core_v2 import FSMCoreV2, StateDefinition, TransitionDefinition, WorkflowPriority, TransitionType
        print("✅ FSM Core V2 imported successfully")
        
        # Test FSM system creation
        fsm = FSMCoreV2()
        print("✅ FSM Core V2 created successfully")
        
        # Test FSM system start
        if fsm.start_system():
            print("✅ FSM system started successfully")
        else:
            print("❌ Failed to start FSM system")
            return False
        
        # Test state creation with correct parameters - add start state first
        start_state = StateDefinition(
            name="start",
            description="Starting state for workflow",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        
        test_state = StateDefinition(
            name="test_state",
            description="Test state for integration",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        
        # Add states first
        if fsm.add_state(start_state):
            print("✅ Start state added successfully")
        else:
            print("❌ Failed to add start state")
            return False
        
        if fsm.add_state(test_state):
            print("✅ Test state added successfully")
        else:
            print("❌ Failed to add test state")
            return False
        
        # Now add transition between existing states
        transition = TransitionDefinition(
            from_state="start",
            to_state="test_state",
            transition_type=TransitionType.AUTOMATIC,
            condition=None,
            priority=1,
            timeout_seconds=None,
            actions=[],
            metadata={}
        )
        
        if fsm.add_transition(transition):
            print("✅ Transition added successfully")
        else:
            print("❌ Failed to add transition")
            return False
        
        # Test workflow creation
        workflow_id = fsm.create_workflow("test_workflow", "start", WorkflowPriority.NORMAL)
        if workflow_id:
            print("✅ Workflow created successfully")
        else:
            print("❌ Failed to create workflow")
            return False
        
        # Test workflow start
        if fsm.start_workflow(workflow_id):
            print("✅ Workflow started successfully")
        else:
            print("❌ Failed to start workflow")
            return False
        
        # Get system stats
        stats = fsm.get_system_stats()
        print(f"✅ System stats: {stats['total_workflows']} workflows, {len(fsm.states)} states")
        
        # Stop FSM system
        fsm.stop_system()
        print("✅ FSM system stopped successfully")
        
        print("🎉 FSM System Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ FSM System Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_compliance_system_integration():
    """Test compliance monitoring system integration."""
    try:
        print("\n🧪 Testing Compliance System Integration...")
        
        # Test compliance system import (will use mock if not available)
        from fsm_compliance_integration import ComplianceMonitoringSystem
        print("✅ ComplianceMonitoringSystem imported successfully")
        
        # Test compliance system creation
        compliance = ComplianceMonitoringSystem()
        print("✅ ComplianceMonitoringSystem created successfully")
        
        # Test agent progress tracking
        progress_data = {
            "percentage": 25.0,
            "phase": "TESTING",
            "deliverables": {"test": "IN_PROGRESS"},
            "code_changes": ["Test integration"],
            "devlog_entries": ["Testing compliance system"]
        }
        
        compliance.track_agent_progress("Agent-1", "TEST_TASK", progress_data)
        print("✅ Agent progress tracked successfully")
        
        # Test compliance report
        report = compliance.get_compliance_report()
        print(f"✅ Compliance report generated: {report['total_checks']} checks")
        
        print("🎉 Compliance System Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Compliance System Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("🚀 FSM Compliance Integration Validation Test Suite")
    print("=" * 60)
    
    # Run tests
    test1 = test_fsm_compliance_integration()
    test2 = test_fsm_system_integration()
    test3 = test_compliance_system_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if test1 and test2 and test3:
        print("🎉 ALL TESTS PASSED - FSM Compliance Integration is fully operational!")
        print("✅ FSM Compliance Integration: PASSED")
        print("✅ FSM System Integration: PASSED")
        print("✅ Compliance System Integration: PASSED")
        return True
    else:
        print("❌ SOME TESTS FAILED - FSM Compliance Integration needs attention")
        print(f"   FSM Compliance Integration: {'✅ PASSED' if test1 else '❌ FAILED'}")
        print(f"   FSM System Integration: {'✅ PASSED' if test2 else '❌ FAILED'}")
        print(f"   Compliance System Integration: {'✅ PASSED' if test3 else '❌ FAILED'}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
