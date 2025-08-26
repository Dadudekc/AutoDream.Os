#!/usr/bin/env python3
"""
Simple test for performance system
"""

from src.core.performance import UnifiedPerformanceSystem

print("✅ Import successful!")

# Try to create instance
try:
    system = UnifiedPerformanceSystem()
    print("✅ Instance created successfully!")
except Exception as e:
    print(f"❌ Error creating instance: {e}")
    import traceback
    traceback.print_exc()
