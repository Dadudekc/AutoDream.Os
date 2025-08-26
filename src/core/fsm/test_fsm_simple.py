#!/usr/bin/env python3
"""
Simple FSM Test Script - Quick Verification

Quick test to verify FSM Core V2 system is working correctly.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import sys
import os
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_fsm_import():
    """Test that FSM system can be imported."""
    try:
        from fsm_core_v2 import FSMCoreV2, StateDefinition, TransitionDefinition
        print("✅ FSM system imports successfully")
        return True
    except ImportError as e:
        print(f"❌ FSM import failed: {e}")
        return False

def test_fsm_creation():
    """Test FSM system creation."""
    try:
        from fsm_core_v2 import FSMCoreV2
        fsm = FSMCoreV2()
        print("✅ FSM system created successfully")
        return fsm
    except Exception as e:
        print(f"❌ FSM creation failed: {e}")
        return None

def test_fsm_initialization():
    """Test FSM system initialization."""
    try:
        fsm = test_fsm_creation()
        if not fsm:
            return False
        
        # Start system
        if fsm.start_system():
            print("✅ FSM system started successfully")
        else:
            print("❌ FSM system failed to start")
            return False
        
        # Check system status
        if fsm.is_running:
            print("✅ FSM system is running")
        else:
            print("❌ FSM system is not running")
            return False
        
        return fsm
        
    except Exception as e:
        print(f"❌ FSM initialization failed: {e}")
        return None

def test_basic_functionality():
    """Test basic FSM functionality."""
    try:
        fsm = test_fsm_initialization()
        if not fsm:
            return False
        
        # Create a simple state
        from fsm_core_v2 import StateDefinition
        test_state = StateDefinition(
            name="test_state",
            description="Test state for verification",
            entry_actions=["log_entry"],
            exit_actions=["log_exit"],
            timeout_seconds=10.0,
            retry_count=1,
            retry_delay=1.0,
            required_resources=[],
            dependencies=[],
            metadata={"test": True}
        )
        
        # Add state to FSM
        if fsm.add_state(test_state):
            print("✅ Test state added successfully")
        else:
            print("❌ Failed to add test state")
            return False
        
        # Create a simple workflow
        workflow_id = fsm.create_workflow("test_workflow", "test_state")
        if workflow_id:
            print(f"✅ Test workflow created: {workflow_id}")
        else:
            print("❌ Failed to create test workflow")
            return False
        
        # Get system stats
        stats = fsm.get_system_stats()
        print(f"✅ System stats: {stats['total_workflows']} workflows, {len(fsm.states)} states")
        
        # Stop system
        if fsm.stop_system():
            print("✅ FSM system stopped successfully")
        else:
            print("❌ FSM system failed to stop")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 FSM Core V2 Simple Test Suite")
    print("=" * 40)
    
    # Test 1: Import
    if not test_fsm_import():
        print("❌ Import test failed - cannot proceed")
        return False
    
    # Test 2: Creation
    if not test_fsm_creation():
        print("❌ Creation test failed - cannot proceed")
        return False
    
    # Test 3: Initialization
    if not test_fsm_initialization():
        print("❌ Initialization test failed - cannot proceed")
        return False
    
    # Test 4: Basic functionality
    if not test_basic_functionality():
        print("❌ Basic functionality test failed")
        return False
    
    print("\n🎉 All FSM tests passed successfully!")
    print("✅ FSM Core V2 system is ready for Phase 2 workflow management!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
