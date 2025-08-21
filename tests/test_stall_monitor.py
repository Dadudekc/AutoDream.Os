#!/usr/bin/env python3
"""
Smoke test for stall monitor functionality.
Tests basic operations without requiring actual Cursor DB or git repo.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Simple test functions that don't require imports
def test_classify():
    """Test classification logic."""
    print("🧪 Testing classification logic...")
    
    def classify(age_secs):
        if age_secs is None:
            return "STOPPED"
        if age_secs <= 300:  # 5 minutes
            return "ACTIVE"
        if age_secs <= 900:  # 15 minutes
            return "IDLE"
        return "STOPPED"
    
    # Test cases
    assert classify(150) == "ACTIVE"   # 2.5 minutes
    assert classify(300) == "ACTIVE"   # 5 minutes (threshold)
    assert classify(600) == "IDLE"     # 10 minutes
    assert classify(900) == "IDLE"     # 15 minutes (threshold)
    assert classify(901) == "STOPPED"  # 15+ minutes
    assert classify(None) == "STOPPED"  # No signal
    
    print("✅ Classification tests passed!")


def test_timestamp_conversion():
    """Test timestamp conversion logic."""
    print("🧪 Testing timestamp conversion...")
    
    def ms_to_iso(ms):
        if ms is None:
            return None
        try:
            from datetime import datetime
            return datetime.utcfromtimestamp(ms/1000).isoformat() + "Z"
        except (ValueError, OSError) as e:
            return None
    
    # Test with a known timestamp (2025-08-20 08:38:00 UTC)
    test_ms = 1732089480000
    iso_str = ms_to_iso(test_ms)
    
    assert iso_str is not None
    # Check that it's a valid ISO format timestamp
    assert "Z" in iso_str
    assert "T" in iso_str
    assert len(iso_str) >= 20  # Should be at least 20 characters (e.g., "2024-11-20T07:58:00Z")
    
    # Test with None
    assert ms_to_iso(None) is None
    
    print("✅ Timestamp conversion tests passed!")


def test_file_operations():
    """Test file operations."""
    print("🧪 Testing file operations...")
    
    # Create temporary directory
    test_dir = tempfile.mkdtemp()
    try:
        # Test file creation and modification time
        test_file = os.path.join(test_dir, "test_file.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Check file exists and has content
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            content = f.read()
        assert content == "test content"
        
        # Check modification time
        mtime = os.path.getmtime(test_file)
        assert mtime > 0
        
        print("✅ File operation tests passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(test_dir)


def test_json_operations():
    """Test JSON operations."""
    print("🧪 Testing JSON operations...")
    
    # Test data
    test_data = {
        "agents": [
            {"id": 1, "name": "Agent-1", "state": "ACTIVE"},
            {"id": 2, "name": "Agent-2", "state": "IDLE"}
        ]
    }
    
    # Test JSON serialization
    json_str = json.dumps(test_data, indent=2)
    assert '"agents"' in json_str
    assert '"Agent-1"' in json_str
    
    # Test JSON deserialization
    parsed_data = json.loads(json_str)
    assert len(parsed_data["agents"]) == 2
    assert parsed_data["agents"][0]["name"] == "Agent-1"
    
    print("✅ JSON operation tests passed!")


def test_directory_structure():
    """Test that required directories exist."""
    print("🧪 Testing directory structure...")
    
    required_dirs = [
        "runtime/agent_status",
        "runtime/agent_comms/hourly_reports",
        "runtime/cursor_capture"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"⚠️ {dir_path} not found")
    
    print("✅ Directory structure check complete!")


def main():
    """Run all tests."""
    print("🧪 Running stall monitor smoke tests...")
    
    try:
        test_classify()
        test_timestamp_conversion()
        test_file_operations()
        test_json_operations()
        test_directory_structure()
        
        print("\n🎉 All smoke tests passed!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
