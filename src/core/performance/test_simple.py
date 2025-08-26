#!/usr/bin/env python3
"""
Simple test for performance system
"""

from src.core.unified_performance_system import UnifiedPerformanceSystem

print("✅ Import successful!")

# Try to create instance
try:
    system = UnifiedPerformanceSystem()
    started = system.start_system()
    system.stop_system()
    print(f"✅ Orchestrator functional: start -> {started}")
except Exception as e:
    print(f"❌ Error creating instance: {e}")
    import traceback
    traceback.print_exc()
