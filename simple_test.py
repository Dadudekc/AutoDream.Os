#!/usr/bin/env python3
"""Simple test for V2 system."""

print("Starting V2 test...")

try:
    from simple_thea_communication import SimpleTheaCommunication
    print("✅ Import successful")

    comm = SimpleTheaCommunication(use_selenium=False)
    print("✅ Instance created")

    print("🎉 Test passed!")
except Exception as e:
    print(f"❌ Error: {e}")
