#!/usr/bin/env python3
"""
Simple FSM-Discord Integration Demo - Agent Cellphone V2
=======================================================

Simplified demo showing basic FSM-Discord integration.
Tests core functionality without complex dependencies.

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import sys
import json
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demo_simple_integration():
    """Simple integration demo"""
    print("🚀 Simple FSM-Discord Integration Demo")
    print("=" * 50)
    
    try:
        # Test 1: Discord Service
        print("\n📱 Test 1: Discord Integration Service")
        print("-" * 40)
        
        from services.discord_integration_service import DiscordIntegrationService
        
        discord_service = DiscordIntegrationService()
        discord_service.configure_discord(
            webhook_url="https://discord.com/api/webhooks/demo",
            guild_id="demo_guild"
        )
        
        # Register test agents
        agents = [
            ("agent-1", "Foundation Specialist", ["testing", "coordination"]),
            ("agent-2", "Quality Analyzer", ["automation", "monitoring"])
        ]
        
        for agent_id, name, capabilities in agents:
            success = discord_service.register_agent(agent_id, name, capabilities)
            print(f"{'✅' if success else '❌'} {name} registered")
        
        # Send test messages
        discord_service.send_message("system", "test", "Integration test message")
        discord_service.send_message("agent-1", "status", "Agent 1 is ready")
        
        print("✅ Discord service test completed")
        
        # Test 2: FSM-Discord Bridge
        print("\n🔗 Test 2: FSM-Discord Bridge")
        print("-" * 40)
        
        from core.fsm_discord_bridge import FSMDiscordBridge
        
        bridge = FSMDiscordBridge()
        
        # Test command processing
        test_commands = [
            ("!help", [], "test_user", "general"),
            ("!fsm_status", [], "test_user", "fsm_status")
        ]
        
        for command, args, user, channel in test_commands:
            response = bridge.process_discord_command(command, args, user, channel)
            print(f"🔧 {command}: {response[:50]}...")
        
        # Get bridge status
        status = bridge.get_bridge_status()
        print(f"📊 Bridge Status: {status['fsm_enabled']} FSM, {status['decision_enabled']} Decision, {status['discord_enabled']} Discord")
        
        print("✅ Bridge test completed")
        
        # Test 3: Integration Status
        print("\n📊 Test 3: Integration Status")
        print("-" * 40)
        
        discord_status = discord_service.get_status()
        bridge_status = bridge.get_bridge_status()
        
        print("📱 Discord Service:")
        print(f"  Messages: {discord_status['messages_sent']}")
        print(f"  Agents: {discord_status['agents_registered']}")
        print(f"  FSM Integration: {discord_status['fsm_integration']}")
        
        print("\n🔗 Bridge Status:")
        print(f"  FSM Enabled: {bridge_status['fsm_enabled']}")
        print(f"  Decision Enabled: {bridge_status['decision_enabled']}")
        print(f"  Discord Enabled: {bridge_status['discord_enabled']}")
        
        print("✅ Integration status test completed")
        
        # Final Results
        print("\n🎉 Simple Integration Demo Completed!")
        print("=" * 50)
        
        final_results = {
            "discord_messages": discord_status['messages_sent'],
            "agents_registered": discord_status['agents_registered'],
            "bridge_operational": True,
            "integration_status": "BASIC OPERATIONAL"
        }
        
        print("📊 Final Results:")
        print(json.dumps(final_results, indent=2))
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    print("🤖 Agent Cellphone V2 - Simple FSM-Discord Integration Demo")
    print("=" * 70)
    
    success = demo_simple_integration()
    
    if success:
        print("\n✅ Simple Integration Demo: SUCCESS")
        print("\n🚀 Next Steps:")
        print("1. Configure Discord webhook for real integration")
        print("2. Test with actual FSM core when available")
        print("3. Deploy decision engine integration")
    else:
        print("\n❌ Simple Integration Demo: FAILED")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

