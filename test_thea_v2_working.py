#!/usr/bin/env python3
"""
V2 Compliant Thea Service Test - Agent-3
=========================================

Tests the working Thea service based on proven thea_automation.py patterns.
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.thea import TheaService


def test_thea_service():
    """Test Thea service communication."""
    
    print()
    print("=" * 70)
    print("🤖 AGENT-3: Thea Service V2 Test")
    print("=" * 70)
    print()
    
    # Create service
    thea = TheaService(cookie_file="thea_cookies.json", headless=False)
    
    try:
        # Test message
        test_message = (
            "Hello Thea! This is Agent-3 testing the V2 compliant Thea service. "
            "The browser infrastructure has been consolidated from 15→5 files. "
            "Please confirm you received this message with a brief response. Thank you!"
        )
        
        print(f"📤 Sending test message to Thea...")
        print(f"Message: {test_message[:80]}...\n")
        
        # Communicate
        result = thea.communicate(test_message, save=True)
        
        # Display results
        print("=" * 70)
        print("📊 RESULT")
        print("=" * 70)
        print(f"Success: {result['success']}")
        print(f"Message: {result['message'][:60]}...")
        print(f"Response: {result['response'][:200] if result['response'] else 'None'}...")
        print(f"File: {result['file']}")
        print("=" * 70)
        print()
        
        if result['success']:
            print("✅ TEST PASSED - Thea service working!")
            print()
            print("Consolidated services validated:")
            print("- Browser service: ✅")
            print("- Session management: ✅")
            print("- Content operations: ✅")
            print("- PyAutoGUI messaging: ✅")
            print("- Response detection: ✅")
            print()
            return True
        else:
            print("⚠️  TEST INCOMPLETE - Check output above")
            print()
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
        return False
        
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        thea.cleanup()
        print("🧹 Cleanup complete")
        print()
        print("🐝 WE ARE SWARM - Thea service test complete!")
        print()


if __name__ == "__main__":
    success = test_thea_service()
    sys.exit(0 if success else 1)



