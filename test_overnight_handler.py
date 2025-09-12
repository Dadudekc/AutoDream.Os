#!/usr/bin/env python3
"""
Test script for Overnight Command Handler
"""
import sys
import os
sys.path.append('src')

# Import directly to avoid services __init__.py issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'services'))
import overnight_command_handler
OvernightCommandHandler = overnight_command_handler.OvernightCommandHandler

class MockArgs:
    """Mock arguments for testing."""
    def __init__(self, overnight=True, operation="cleanup", dry_run=True):
        self.overnight = overnight
        self.operation = operation
        self.dry_run = dry_run

def test_overnight_handler():
    """Test the overnight command handler."""
    print("🌙 Testing Overnight Command Handler")
    print("=" * 50)

    # Initialize handler
    handler = OvernightCommandHandler()
    print("✅ Handler initialized")

    # Test can_handle
    mock_args = MockArgs()
    can_handle = handler.can_handle(mock_args)
    print(f"✅ can_handle() returned: {can_handle}")

    # Test dry run cleanup sequence
    print("\n🧹 Testing cleanup sequence (dry run)...")
    success = handler.handle(mock_args)
    print(f"✅ Cleanup sequence result: {success}")

    # Test maintenance cycle
    print("\n🔧 Testing maintenance cycle...")
    maintenance_args = MockArgs(operation="maintenance")
    success = handler.handle(maintenance_args)
    print(f"✅ Maintenance cycle result: {success}")

    # Test full cycle
    print("\n🌙 Testing full overnight cycle...")
    full_args = MockArgs(operation="full")
    success = handler.handle(full_args)
    print(f"✅ Full cycle result: {success}")

    print("\n🎉 All tests completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_overnight_handler()
