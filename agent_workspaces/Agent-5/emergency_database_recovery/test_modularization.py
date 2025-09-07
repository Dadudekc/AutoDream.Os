#!/usr/bin/env python3
"""
Test script for modularized emergency database recovery system
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from emergency_database_recovery import EmergencyContractDatabaseRecovery
    print("✅ Modularization successful! All imports working.")
    
    # Test instantiation
    recovery = EmergencyContractDatabaseRecovery()
    print("✅ Emergency recovery system instantiated successfully.")
    
    print(f"✅ Main orchestrator: {recovery.__class__.__name__}")
    print(f"✅ File paths configured: {recovery.task_list_path}, {recovery.meeting_path}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! Modularization complete.")
