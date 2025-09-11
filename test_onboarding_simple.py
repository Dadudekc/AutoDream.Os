#!/usr/bin/env python3
"""
Simple Onboarding Copy/Paste Test
=================================

Simple test to verify copy/paste functionality in onboarding system.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_copy_paste_functionality():
    """Test basic copy/paste functionality."""
    try:
        import pyperclip
        
        logger.info("🧪 Testing copy/paste functionality...")
        
        # Test basic copy/paste
        test_message = """🎯 **PHASE TRANSITION ONBOARDING - CONSOLIDATION EXECUTION**

**Agent Identity:** Agent-2 - Architecture & Design Specialist
**Phase:** Consolidation Execution
**Status:** ACTIVE - READY FOR CONSOLIDATION ASSIGNMENT

**Phase Description:**
Active consolidation of identified opportunities

**Phase Targets:**
• Core modules
• Services  
• Web interface
• Utilities

**Your Specific Assignment:**
Chunk 001 (Core) - 50→15 files (70% reduction)

🐝 **WE ARE SWARM - WELCOME TO CONSOLIDATION EXECUTION PHASE!**

Best regards,
Captain Agent-4 (QA & Coordination)"""
        
        # Copy to clipboard
        pyperclip.copy(test_message)
        logger.info(f"📋 Copied message to clipboard ({len(test_message)} characters)")
        
        # Paste from clipboard
        clipboard_content = pyperclip.paste()
        logger.info(f"📋 Retrieved message from clipboard ({len(clipboard_content)} characters)")
        
        # Verify content matches
        if clipboard_content == test_message:
            logger.info("✅ Copy/paste functionality working correctly")
            return True
        else:
            logger.error("❌ Clipboard content does not match original")
            logger.error(f"Original length: {len(test_message)}")
            logger.error(f"Clipboard length: {len(clipboard_content)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Copy/paste test failed: {e}")
        return False

def test_phase_transition_onboarding():
    """Test phase transition onboarding functionality."""
    try:
        from phase_transition_onboarding import PhaseTransitionOnboarding
        
        logger.info("🧪 Testing Phase Transition Onboarding...")
        
        # Create onboarding instance
        onboarding = PhaseTransitionOnboarding()
        
        # Test message generation
        agent_id = "Agent-2"
        role = "Architecture & Design Specialist"
        phase = "Phase 2"
        phase_config = onboarding.phase_configs.get(phase, {})
        assignment = phase_config.get("agent_assignments", {}).get(agent_id, "General support")
        
        message = onboarding._generate_phase_transition_message(
            agent_id, role, phase, phase_config, assignment
        )
        
        logger.info(f"📝 Generated message length: {len(message)} characters")
        
        # Test copy/paste with generated message
        import pyperclip
        pyperclip.copy(message)
        clipboard_content = pyperclip.paste()
        
        if clipboard_content == message:
            logger.info("✅ Phase transition message copy/paste working correctly")
            return True
        else:
            logger.error("❌ Phase transition message copy/paste failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Phase transition onboarding test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Starting Simple Onboarding Copy/Paste Tests...")
    logger.info("=" * 50)
    
    tests = [
        ("Basic Copy/Paste", test_copy_paste_functionality),
        ("Phase Transition Onboarding", test_phase_transition_onboarding)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        logger.info(f"{'✅ PASSED' if result else '❌ FAILED'}: {test_name}")
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Copy/paste functionality is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the logs above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)
