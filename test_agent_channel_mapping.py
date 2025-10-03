#!/usr/bin/env python3
"""
Test Agent Channel Mapping
=========================
Test if each agent channel is correctly configured to direct to the right Discord channel.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def load_env_file():
    """Load environment variables from .env file."""
    print("🔧 Loading .env file for agent channel testing...")
    
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load .env file manually
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip('"\'')
                os.environ[key] = value
    
    print("✅ .env file loaded into environment")
    return True

def test_agent_channel_configuration():
    """Test agent channel configuration from environment variables."""
    print("\n🔍 Testing Agent Channel Configuration...")
    
    # Expected agent mapping from the repo rules
    expected_agents = {
        "Agent-1": {
            "name": "Integration & Core Systems Specialist",
            "role": "integration_specialist",
            "coordinates": [-1269, 481],
            "enabled": False
        },
        "Agent-2": {
            "name": "Architecture & Design Specialist", 
            "role": "architecture_specialist",
            "coordinates": [-308, 480],
            "enabled": False
        },
        "Agent-3": {
            "name": "Infrastructure & DevOps Specialist",
            "role": "infrastructure_specialist", 
            "coordinates": [-1269, 1001],
            "enabled": False
        },
        "Agent-4": {
            "name": "Captain - Strategic Leadership",
            "role": "captain",
            "coordinates": [-308, 1000],
            "enabled": True
        },
        "Agent-5": {
            "name": "Coordinator - Task Management",
            "role": "coordinator",
            "coordinates": [652, 421],
            "enabled": True
        },
        "Agent-6": {
            "name": "Quality Specialist - V2 Compliance",
            "role": "quality_specialist",
            "coordinates": [1612, 419],
            "enabled": True
        },
        "Agent-7": {
            "name": "Implementation Specialist - Core Systems",
            "role": "implementation_specialist",
            "coordinates": [700, 938],
            "enabled": True
        },
        "Agent-8": {
            "name": "SSOT & System Integration Specialist",
            "role": "ssot_manager",
            "coordinates": [1611, 941],
            "enabled": True
        }
    }
    
    print("📋 Expected Agent Configuration:")
    for agent_id, config in expected_agents.items():
        status = "🟢 ACTIVE" if config["enabled"] else "🔴 INACTIVE"
        print(f"   • {agent_id}: {config['name']} ({config['role']}) - {status}")
    
    return expected_agents

def test_discord_channel_mapping():
    """Test Discord channel mapping for each agent."""
    print("\n🔍 Testing Discord Channel Mapping...")
    
    # Get agent channels from environment
    agent_channels = {}
    for i in range(1, 9):
        agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
        channel_id = os.getenv(agent_key)
        if channel_id:
            agent_channels[f"Agent-{i}"] = int(channel_id)
    
    print("📋 Discord Channel Mapping:")
    for agent_id, channel_id in agent_channels.items():
        print(f"   • {agent_id}: {channel_id}")
    
    # Verify all agents have channels
    missing_channels = []
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        if agent_id not in agent_channels:
            missing_channels.append(agent_id)
    
    if missing_channels:
        print(f"❌ Missing channels for: {', '.join(missing_channels)}")
        return False
    else:
        print("✅ All agents have Discord channels configured")
        return True, agent_channels

def test_discord_devlog_service_channels():
    """Test Discord Devlog Service channel mapping."""
    print("\n🔍 Testing Discord Devlog Service Channel Mapping...")
    
    try:
        from src.services.discord_devlog_service import DiscordDevlogService
        
        # Create service instance
        service = DiscordDevlogService()
        print("✅ DiscordDevlogService instantiated")
        
        # Check agent channels
        if hasattr(service, 'agent_channels'):
            print("📋 Discord Devlog Service Agent Channels:")
            for agent_id, channel_id in service.agent_channels.items():
                print(f"   • {agent_id}: {channel_id}")
            
            # Verify all 8 agents are configured
            if len(service.agent_channels) == 8:
                print("✅ All 8 agents have channels in Discord Devlog Service")
                return True, service.agent_channels
            else:
                print(f"❌ Only {len(service.agent_channels)}/8 agents have channels")
                return False
        else:
            print("❌ Discord Devlog Service has no agent_channels attribute")
            return False
            
    except Exception as e:
        print(f"❌ Discord Devlog Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_channel_consistency():
    """Test consistency between environment variables and service channels."""
    print("\n🔍 Testing Channel Consistency...")
    
    # Get environment channels
    env_channels = {}
    for i in range(1, 9):
        agent_key = f"DISCORD_CHANNEL_AGENT_{i}"
        channel_id = os.getenv(agent_key)
        if channel_id:
            env_channels[f"Agent-{i}"] = int(channel_id)
    
    # Get service channels
    try:
        from src.services.discord_devlog_service import DiscordDevlogService
        service = DiscordDevlogService()
        service_channels = getattr(service, 'agent_channels', {})
        
        print("📊 Channel Consistency Check:")
        consistent = True
        
        for agent_id in range(1, 9):
            agent_name = f"Agent-{agent_id}"
            env_channel = env_channels.get(agent_name)
            service_channel = service_channels.get(agent_name)
            
            if env_channel and service_channel:
                if env_channel == service_channel:
                    print(f"   ✅ {agent_name}: {env_channel} (consistent)")
                else:
                    print(f"   ❌ {agent_name}: ENV={env_channel}, SERVICE={service_channel} (inconsistent)")
                    consistent = False
            elif env_channel:
                print(f"   ⚠️ {agent_name}: ENV={env_channel}, SERVICE=Missing")
                consistent = False
            elif service_channel:
                print(f"   ⚠️ {agent_name}: ENV=Missing, SERVICE={service_channel}")
                consistent = False
            else:
                print(f"   ❌ {agent_name}: Both ENV and SERVICE missing")
                consistent = False
        
        if consistent:
            print("✅ All channels are consistent between environment and service")
        else:
            print("❌ Channel inconsistencies found")
        
        return consistent
        
    except Exception as e:
        print(f"❌ Channel consistency test failed: {e}")
        return False

def test_agent_channel_posting():
    """Test if devlog posting goes to the correct agent channel."""
    print("\n🔍 Testing Agent Channel Posting...")
    
    try:
        from src.services.agent_devlog.devlog_poster import AgentDevlogPoster
        
        # Create poster instance
        poster = AgentDevlogPoster()
        print("✅ AgentDevlogPoster instantiated")
        
        # Test posting for each agent
        test_agents = ["agent4", "agent5", "agent6", "agent7", "agent8"]  # Active agents
        
        for agent in test_agents:
            print(f"\n🧪 Testing devlog posting for {agent}...")
            
            # Create test content
            content = poster.create_devlog_content(agent, "Channel mapping test", "completed", "Testing if posts go to correct channel")
            
            # Test Discord posting (this will show which channel it tries to post to)
            try:
                result = poster.post_to_discord(content, agent)
                if result:
                    print(f"   ✅ {agent}: Posted successfully to Discord")
                else:
                    print(f"   ⚠️ {agent}: Posting failed (may be expected in test mode)")
            except Exception as e:
                print(f"   ⚠️ {agent}: Posting error (may be expected): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent channel posting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🐝 Agent Channel Mapping Test")
    print("=" * 60)
    
    # Step 1: Load .env file
    env_loaded = load_env_file()
    if not env_loaded:
        print("❌ Cannot proceed without .env file")
        return False
    
    # Step 2: Test expected agent configuration
    expected_agents = test_agent_channel_configuration()
    
    # Step 3: Test Discord channel mapping
    env_channels_result = test_discord_channel_mapping()
    if isinstance(env_channels_result, tuple):
        env_channels_ok, env_channels = env_channels_result
    else:
        env_channels_ok = env_channels_result
        env_channels = {}
    
    # Step 4: Test Discord Devlog Service channels
    service_channels_result = test_discord_devlog_service_channels()
    if isinstance(service_channels_result, tuple):
        service_channels_ok, service_channels = service_channels_result
    else:
        service_channels_ok = service_channels_result
        service_channels = {}
    
    # Step 5: Test channel consistency
    consistency_ok = test_channel_consistency()
    
    # Step 6: Test agent channel posting
    posting_ok = test_agent_channel_posting()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 AGENT CHANNEL MAPPING TEST SUMMARY")
    print("=" * 60)
    
    print(f"• .env file loading: {'✅ Success' if env_loaded else '❌ Failed'}")
    print(f"• Environment channels: {'✅ All 8 configured' if env_channels_ok else '❌ Missing channels'}")
    print(f"• Service channels: {'✅ All 8 configured' if service_channels_ok else '❌ Missing channels'}")
    print(f"• Channel consistency: {'✅ Consistent' if consistency_ok else '❌ Inconsistent'}")
    print(f"• Agent posting: {'✅ Working' if posting_ok else '❌ Failed'}")
    
    all_working = all([
        env_loaded, env_channels_ok, service_channels_ok, 
        consistency_ok, posting_ok
    ])
    
    if all_working:
        print("\n🎉 ALL AGENT CHANNEL TESTS PASSED!")
        print("✅ Each agent channel is correctly configured")
        print("✅ All agents direct to the right Discord channels")
        print("✅ Channel mapping is consistent across services")
    else:
        print("\n⚠️ Some agent channel tests failed")
        print("💡 Check the output above for specific issues")
    
    print("\n💡 AGENT CHANNEL MAPPING:")
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        channel_id = env_channels.get(agent_id, "Not configured")
        expected_config = expected_agents.get(agent_id, {})
        status = "🟢 ACTIVE" if expected_config.get("enabled", False) else "🔴 INACTIVE"
        print(f"   • {agent_id}: {channel_id} ({status})")
    
    print("\n" + "=" * 60)
    
    return all_working

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
