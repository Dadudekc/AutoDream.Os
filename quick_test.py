#!/usr/bin/env python3
"""Quick test for the SWARM monitoring dashboard"""

import urllib.request
import json
import time

def test_dashboard():
    """Test the dashboard API"""
    print("🐝 Testing SWARM Simple Monitoring Dashboard...")

    try:
        # Test main page
        response = urllib.request.urlopen('http://localhost:8000/', timeout=5)
        html = response.read().decode('utf-8')
        if 'SWARM Monitoring Dashboard' in html:
            print("✅ Dashboard HTML page loaded successfully")
        else:
            print("❌ Dashboard HTML page missing expected content")
            return False

        # Test API
        response = urllib.request.urlopen('http://localhost:8000/api/agents/status', timeout=5)
        data = json.loads(response.read().decode('utf-8'))

        print("✅ Dashboard API responding")
        print(f"📊 Found {len(data.get('agents', []))} agents")
        print(f"🤖 Active agents: {data.get('active_agents', 0)}")

        # Show first few agents
        agents = data.get('agents', [])
        if agents:
            print("\n📋 Agent Status Sample:")
            for agent in agents[:3]:
                status = agent.get('status', 'UNKNOWN')
                tasks = agent.get('active_tasks', 0)
                print(f"  • {agent.get('agent_id', 'Unknown')}: {status} ({tasks} active tasks)")

        return True

    except urllib.error.URLError as e:
        print(f"❌ Dashboard not responding: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard()
    if success:
        print("\n🎉 SWARM Monitoring Dashboard is operational!")
        print("🌐 Access at: http://localhost:8000")
    else:
        print("\n❌ Dashboard test failed")
        exit(1)
