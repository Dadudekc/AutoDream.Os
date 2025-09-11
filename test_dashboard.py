#!/usr/bin/env python3
"""Simple test script for the SWARM monitoring dashboard"""

import urllib.request
import json
import sys

def test_dashboard():
    """Test the dashboard API endpoints"""
    try:
        print("🐝 Testing SWARM Monitoring Dashboard...")

        # Test main endpoint
        response = urllib.request.urlopen('http://localhost:8000/api/agents/status', timeout=5)
        data = json.loads(response.read().decode('utf-8'))

        print("✅ Dashboard API responding")
        print(f"📊 Agents found: {len(data.get('agents', []))}")
        print(f"🤖 Active agents: {data.get('active_agents', 0)}")
        print(f"📅 Last update: {data.get('timestamp', 'Unknown')}")

        # Show sample agent data
        agents = data.get('agents', [])
        if agents:
            print("\n📋 Sample Agent Status:")
            for agent in agents[:3]:  # Show first 3 agents
                print(f"  • {agent['agent_id']}: {agent['status']} - {agent.get('current_mission', 'No mission')[:50]}...")

        return True

    except urllib.error.URLError as e:
        print(f"❌ Dashboard not responding: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard()
    sys.exit(0 if success else 1)
