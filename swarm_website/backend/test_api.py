#!/usr/bin/env python3
"""
API Endpoint Tests
==================

Quick test to verify all 9 endpoints work.
Created by: Agent-3 (Cycle 10 - Testing phase)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all API endpoints."""
    endpoints = [
        "/",
        "/api/agents",
        "/api/leaderboard",
        "/api/swarm-status",
        "/api/github-book",
        "/api/debates",
        "/api/swarm-brain",
        "/api/gas-pipeline",
        "/api/partnerships",
    ]
    
    print("🧪 Testing Swarm Website API Endpoints\n")
    print("="*60)
    
    results = []
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            results.append((endpoint, status))
            print(f"{status} - {endpoint}")
        except requests.exceptions.ConnectionError:
            results.append((endpoint, "⚠️  Server not running"))
            print(f"⚠️  Server not running - {endpoint}")
        except Exception as e:
            results.append((endpoint, f"❌ ERROR: {str(e)[:50]}"))
            print(f"❌ ERROR - {endpoint}: {str(e)[:50]}")
    
    print("="*60)
    passed = sum(1 for _, status in results if "PASS" in status)
    total = len(results)
    print(f"\nResult: {passed}/{total} endpoints working")
    
    if passed == total:
        print("\n🎉 ALL ENDPOINTS WORKING! Backend API OPERATIONAL!")
        return 0
    elif passed > 0:
        print(f"\n⚠️  {total - passed} endpoints need attention")
        return 1
    else:
        print("\n❌ Server may not be running. Start with: python main.py")
        return 1

if __name__ == "__main__":
    exit(test_endpoints())

