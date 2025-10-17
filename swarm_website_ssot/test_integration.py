"""
Integration Tests for Swarm Website SSOT Layer

Tests all data loaders and validators with real data.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_website_ssot.data_loader import (
    load_agent_status,
    load_all_agents,
    get_swarm_overview
)
from swarm_website_ssot.validators import (
    validate_agent_status,
    ensure_data_consistency
)


def test_agent_status_loading():
    """Test loading Agent-8's own status."""
    print("\n=== TEST: Agent Status Loading ===")
    
    try:
        agent_8 = load_agent_status("Agent-8")
        
        print(f"✅ Loaded Agent-8 status")
        print(f"   Status: {agent_8.get('status')}")
        print(f"   Mission: {agent_8.get('current_mission', 'N/A')[:60]}...")
        print(f"   Progress: {agent_8.get('progress_percentage')}%")
        print(f"   Is Live: {agent_8.get('is_live')}")
        print(f"   Gas Level: {agent_8.get('gas_level')}")
        print(f"   Health: {agent_8.get('status_health')}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_all_agents_loading():
    """Test loading all 8 agents."""
    print("\n=== TEST: All Agents Loading ===")
    
    try:
        agents = load_all_agents()
        
        print(f"✅ Loaded {len(agents)} agents")
        
        for agent in agents:
            status_icon = "🟢" if agent.get('is_live') else "🔴"
            print(f"   {status_icon} {agent['agent_id']}: {agent.get('status', 'UNKNOWN')} "
                  f"(Gas: {agent.get('gas_level', 0)})")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_agent_validation():
    """Test agent data validation."""
    print("\n=== TEST: Agent Validation ===")
    
    try:
        agent_8 = load_agent_status("Agent-8")
        is_valid = validate_agent_status(agent_8)
        
        if is_valid:
            print(f"✅ Agent-8 data is valid")
        else:
            print(f"❌ Agent-8 data validation failed")
        
        return is_valid
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_swarm_overview():
    """Test swarm-wide overview generation."""
    print("\n=== TEST: Swarm Overview ===")
    
    try:
        overview = get_swarm_overview()
        
        print(f"✅ Generated swarm overview")
        print(f"   Total Agents: {overview['total_agents']}")
        print(f"   Active: {overview['active_agents']}")
        print(f"   Live: {overview['live_agents']}")
        print(f"   Total Points: {overview['total_points']:,}")
        print(f"   Avg Gas: {overview['avg_gas_level']}%")
        print(f"   Pipeline: {overview['pipeline_health']}")
        print(f"   System Health: {overview['system_health']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_data_consistency():
    """Test SSOT data consistency checks."""
    print("\n=== TEST: Data Consistency ===")
    
    try:
        agents = load_all_agents()
        consistency = ensure_data_consistency(agents)
        
        if consistency['is_consistent']:
            print(f"✅ Data is consistent across all sources")
        else:
            print(f"⚠️ Consistency issues found:")
            for issue in consistency['issues']:
                print(f"   - {issue}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("SWARM WEBSITE SSOT - Integration Tests")
    print("Agent-8 SSOT Specialist - Cycle 3")
    print("="*60)
    
    tests = [
        ("Agent Status Loading", test_agent_status_loading),
        ("All Agents Loading", test_all_agents_loading),
        ("Agent Validation", test_agent_validation),
        ("Swarm Overview", test_swarm_overview),
        ("Data Consistency", test_data_consistency),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🏆 ALL TESTS PASSED! SSOT Layer is operational!")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

