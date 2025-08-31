#!/usr/bin/env python3
"""
Test script for the new prompt loader system
"""

import sys
import os

# Add the src directory to the path so we can import the prompt loader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.messaging.prompt_loader import PromptLoader

def test_prompt_loader():
    """Test the prompt loader functionality"""
    print("🧪 **TESTING PROMPT LOADER SYSTEM**")
    
    try:
        # Initialize prompt loader
        loader = PromptLoader()
        print("✅ Prompt loader initialized successfully")
        
        # Test captain onboarding
        print("\n📋 Testing Captain Onboarding:")
        captain_prompt = loader.load_captain_onboarding("Agent-4", "Test custom message")
        print(f"Captain prompt length: {len(captain_prompt)} characters")
        print("First 100 chars:", captain_prompt[:100])
        
        # Test agent onboarding
        print("\n📋 Testing Agent Onboarding:")
        agent_prompt = loader.load_agent_onboarding("Agent-1", 1, "CONTRACT-001: Test Contract", "Test custom message")
        print(f"Agent prompt length: {len(agent_prompt)} characters")
        print("First 100 chars:", agent_prompt[:100])
        
        # Test role mapping
        print("\n🎭 Testing Role Mapping:")
        role_1 = loader.get_agent_role(1)
        role_2 = loader.get_agent_role(2)
        print(f"Agent-1 role: {role_1}")
        print(f"Agent-2 role: {role_2}")
        
        print("\n✅ **ALL TESTS PASSED!** Prompt loader working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ **TEST FAILED:** {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prompt_loader()
    sys.exit(0 if success else 1)
