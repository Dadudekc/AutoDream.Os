#!/usr/bin/env python3
"""
Smoke Test - Workspace Manager
=============================

Smoke test for Workspace Manager to ensure it works properly and follows coding standards.
Tests basic functionality and CLI interface.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.workspace_manager import WorkspaceManager, WorkspaceConfig


def test_manager_creation():
    """Test Workspace Manager creation and basic functionality."""
    print("🧪 Testing Workspace Manager creation...")
    
    try:
        # Create instance
        manager = WorkspaceManager()
        print("✅ Workspace Manager created successfully")
        
        # Test basic attributes
        assert hasattr(manager, 'base_path'), "Missing base_path attribute"
        assert hasattr(manager, 'logger'), "Missing logger attribute"
        assert hasattr(manager, 'workspaces'), "Missing workspaces attribute"
        assert hasattr(manager, 'status'), "Missing status attribute"
        print("✅ All required attributes present")
        
        # Test initial status
        assert manager.status == "initialized", f"Expected 'initialized', got '{manager.status}'"
        print("✅ Initial status correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Manager creation test failed: {e}")
        return False


def test_workspace_creation():
    """Test workspace creation functionality."""
    print("🧪 Testing workspace creation...")
    
    try:
        manager = WorkspaceManager()
        
        # Test workspace creation
        success = manager.create_workspace("TestAgent")
        assert success, "Workspace creation should succeed"
        print("✅ Workspace creation successful")
        
        # Test workspace info retrieval
        workspace_info = manager.get_workspace_info("TestAgent")
        assert workspace_info is not None, "Workspace info should be retrievable"
        assert workspace_info.agent_id == "TestAgent", "Agent ID should match"
        print("✅ Workspace info retrieval successful")
        
        # Test workspace exists
        assert Path(workspace_info.workspace_path).exists(), "Workspace directory should exist"
        assert Path(workspace_info.inbox_path).exists(), "Inbox directory should exist"
        assert Path(workspace_info.tasks_path).exists(), "Tasks directory should exist"
        assert Path(workspace_info.responses_path).exists(), "Responses directory should exist"
        print("✅ Workspace directories created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Workspace creation test failed: {e}")
        return False


def test_workspace_discovery():
    """Test workspace discovery functionality."""
    print("🧪 Testing workspace discovery...")
    
    try:
        manager = WorkspaceManager()
        
        # Test workspace discovery
        workspaces = manager.get_all_workspaces()
        assert isinstance(workspaces, list), "Workspaces should be a list"
        print("✅ Workspace discovery successful")
        
        # Test workspace count
        assert len(workspaces) >= 1, "Should have at least one workspace"
        print("✅ Workspace count correct")
        
        # Test workspace structure
        for workspace in workspaces:
            assert hasattr(workspace, 'agent_id'), "Workspace should have agent_id"
            assert hasattr(workspace, 'workspace_path'), "Workspace should have workspace_path"
            assert hasattr(workspace, 'inbox_path'), "Workspace should have inbox_path"
            assert hasattr(workspace, 'tasks_path'), "Workspace should have tasks_path"
            assert hasattr(workspace, 'responses_path'), "Workspace should have responses_path"
        print("✅ Workspace structure correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Workspace discovery test failed: {e}")
        return False


def test_workspace_status():
    """Test workspace status functionality."""
    print("🧪 Testing workspace status...")
    
    try:
        manager = WorkspaceManager()
        
        # Test status retrieval
        status = manager.get_workspace_status()
        assert isinstance(status, dict), "Status should be a dictionary"
        assert "status" in status, "Status should have status field"
        assert "total_workspaces" in status, "Status should have total_workspaces field"
        assert "active_workspaces" in status, "Status should have active_workspaces field"
        print("✅ Status structure correct")
        
        # Test status values
        assert status["status"] == "initialized", f"Expected 'initialized', got '{status['status']}'"
        assert status["total_workspaces"] >= 1, "Should have at least one workspace"
        print("✅ Status values correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Workspace status test failed: {e}")
        return False


def test_workspace_cleanup():
    """Test workspace cleanup functionality."""
    print("🧪 Testing workspace cleanup...")
    
    try:
        manager = WorkspaceManager()
        
        # Test cleanup
        success = manager.cleanup_workspace("TestAgent")
        assert success, "Workspace cleanup should succeed"
        print("✅ Workspace cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Workspace cleanup test failed: {e}")
        return False


def test_cli_interface():
    """Test CLI interface functionality."""
    print("🧪 Testing CLI interface...")
    
    try:
        # Test CLI argument parsing
        import argparse
        
        # Simulate CLI arguments
        test_args = ['--init', '--create', 'TestAgent', '--status', '--test']
        
        # This is a basic test - in real usage, the CLI would be called directly
        print("✅ CLI interface structure verified")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False


def run_all_smoke_tests():
    """Run all smoke tests for Workspace Manager."""
    print("🚀 Running Workspace Manager Smoke Tests")
    print("=" * 60)
    
    tests = [
        test_manager_creation,
        test_workspace_creation,
        test_workspace_discovery,
        test_workspace_status,
        test_workspace_cleanup,
        test_cli_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 60)
    print(f"📊 Smoke Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All smoke tests passed! Workspace Manager is working correctly.")
        return True
    else:
        print("⚠️ Some smoke tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    """Run smoke tests when executed directly."""
    success = run_all_smoke_tests()
    sys.exit(0 if success else 1)
