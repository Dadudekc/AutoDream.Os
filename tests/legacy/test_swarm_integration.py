#!/usr/bin/env python3
"""
Swarm Integration Test
=====================

Test script to validate the role/mode system integration.
"""

import json
import sys
from pathlib import Path

def test_config_files():
    """Test that all configuration files exist and are valid."""
    print("🔍 Testing Configuration Files...")
    
    config_files = [
        "config/coordinates/coords-8.json",
        "config/roles.json",
        "config/mode_presets/mode-2.json",
        "config/mode_presets/mode-4.json",
        "config/mode_presets/mode-5.json",
        "config/mode_presets/mode-6.json",
        "config/mode_presets/mode-8.json"
    ]
    
    results = []
    for config_file in config_files:
        path = Path(config_file)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                results.append(f"✅ {config_file} - Valid JSON")
            except json.JSONDecodeError as e:
                results.append(f"❌ {config_file} - Invalid JSON: {e}")
        else:
            results.append(f"❌ {config_file} - Missing")
    
    for result in results:
        print(f"   {result}")
    
    return all("✅" in result for result in results)

def test_agent_workspaces():
    """Test that all agent workspaces exist."""
    print("\n🏠 Testing Agent Workspaces...")
    
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    results = []
    
    for agent in agents:
        workspace_path = Path(f"agent_workspaces/{agent}")
        inbox_path = workspace_path / "inbox"
        status_path = workspace_path / "status.json"
        
        if workspace_path.exists() and inbox_path.exists():
            if status_path.exists():
                try:
                    with open(status_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    results.append(f"✅ {agent} - Complete workspace with valid status")
                except json.JSONDecodeError:
                    results.append(f"⚠️ {agent} - Workspace exists but invalid status.json")
            else:
                results.append(f"⚠️ {agent} - Workspace exists but missing status.json")
        else:
            results.append(f"❌ {agent} - Missing workspace or inbox")
    
    for result in results:
        print(f"   {result}")
    
    return all("✅" in result for result in results)

def test_coordinate_validation():
    """Test coordinate validation logic."""
    print("\n🎯 Testing Coordinate Validation...")
    
    # Test canonical coordinates
    coords_path = Path("config/coordinates/coords-8.json")
    if coords_path.exists():
        with open(coords_path, 'r', encoding='utf-8') as f:
            coords = json.load(f)
        
        print(f"   ✅ Loaded canonical coordinates for {len(coords)} agents")
        
        # Validate coordinate format
        valid_coords = True
        for agent_id, coord in coords.items():
            if isinstance(coord, list) and len(coord) == 2:
                x, y = coord
                if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                    print(f"   ✅ Agent {agent_id}: ({x}, {y})")
                else:
                    print(f"   ❌ Agent {agent_id}: Invalid coordinate types")
                    valid_coords = False
            else:
                print(f"   ❌ Agent {agent_id}: Invalid coordinate format")
                valid_coords = False
        
        return valid_coords
    else:
        print("   ❌ Canonical coordinates file missing")
        return False

def test_mode_presets():
    """Test mode preset configurations."""
    print("\n🔄 Testing Mode Presets...")
    
    modes = [2, 4, 5, 6, 8]
    results = []
    
    for mode in modes:
        preset_path = Path(f"config/mode_presets/mode-{mode}.json")
        if preset_path.exists():
            try:
                with open(preset_path, 'r', encoding='utf-8') as f:
                    preset = json.load(f)
                
                # Validate preset structure
                if all(key in preset for key in ["mode", "mapping", "include"]):
                    if preset["mode"] == mode:
                        print(f"   ✅ Mode {mode}: Valid preset with {len(preset['include'])} agents")
                        results.append(True)
                    else:
                        print(f"   ❌ Mode {mode}: Mode mismatch in preset")
                        results.append(False)
                else:
                    print(f"   ❌ Mode {mode}: Missing required keys")
                    results.append(False)
            except json.JSONDecodeError as e:
                print(f"   ❌ Mode {mode}: Invalid JSON - {e}")
                results.append(False)
        else:
            print(f"   ❌ Mode {mode}: Missing preset file")
            results.append(False)
    
    return all(results)

def test_role_catalog():
    """Test role catalog configuration."""
    print("\n👥 Testing Role Catalog...")
    
    roles_path = Path("config/roles.json")
    if roles_path.exists():
        try:
            with open(roles_path, 'r', encoding='utf-8') as f:
                roles_config = json.load(f)
            
            if "roles" in roles_config:
                roles = roles_config["roles"]
                print(f"   ✅ Loaded {len(roles)} roles")
                
                # Check required roles
                required_roles = ["captain", "co_captain", "qc_v2", "system_integrator", "devlog_manager"]
                for role in required_roles:
                    if role in roles:
                        role_info = roles[role]
                        if all(key in role_info for key in ["description", "extra_procedures"]):
                            print(f"   ✅ Role '{role}': Complete definition")
                        else:
                            print(f"   ⚠️ Role '{role}': Missing required fields")
                    else:
                        print(f"   ❌ Role '{role}': Missing from catalog")
                
                return True
            else:
                print("   ❌ Missing 'roles' key in configuration")
                return False
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON in roles configuration: {e}")
            return False
    else:
        print("   ❌ Roles configuration file missing")
        return False

def main():
    """Run all tests."""
    print("🚀 SWARM INTEGRATION TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Configuration Files", test_config_files),
        ("Agent Workspaces", test_agent_workspaces),
        ("Coordinate Validation", test_coordinate_validation),
        ("Mode Presets", test_mode_presets),
        ("Role Catalog", test_role_catalog)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Swarm integration is ready!")
        return 0
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())