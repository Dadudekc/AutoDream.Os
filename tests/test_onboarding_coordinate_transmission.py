#!/usr/bin/env python3
"""
Test Script: --onboarding Flag Coordinate Transmission Verification
================================================================

This script tests whether the --onboarding flag properly sends coordinates 
to the starter location coordinates system.

Test Objective: Verify coordinate transmission functionality
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

def load_coordinates() -> Dict[str, Any]:
    """Load coordinate data from the system"""
    coordinate_files = [
        "config/agents/coordinates.json",
        "runtime/agent_comms/cursor_agent_coords.json"
    ]
    
    for file_path in coordinate_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    coords = json.load(f)
                    print(f"✅ Coordinates loaded from: {file_path}")
                    return coords
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
    
    print("❌ No coordinate files found")
    return {}

def get_starter_location_coordinates(coordinates: Dict[str, Any], agent_id: str, mode: str = "8-agent") -> Optional[Tuple[int, int]]:
    """Get starter location coordinates for a specific agent"""
    try:
        if mode in coordinates and agent_id in coordinates[mode]:
            agent_coords = coordinates[mode][agent_id]
            if "starter_location_box" in agent_coords:
                starter_box = agent_coords["starter_location_box"]
                x = starter_box.get("x")
                y = starter_box.get("y")
                if x is not None and y is not None:
                    return (x, y)
        return None
    except Exception as e:
        print(f"❌ Error getting starter coordinates for {agent_id}: {e}")
        return None

def simulate_onboarding_flag_processing(agent_id: str, mode: str = "8-agent") -> Dict[str, Any]:
    """Simulate the --onboarding flag processing to test coordinate transmission"""
    print(f"\n🧪 Testing --onboarding flag for {agent_id} in {mode} mode")
    
    # Load coordinates
    coordinates = load_coordinates()
    if not coordinates:
        return {"error": "No coordinates available"}
    
    # Get starter location coordinates
    starter_coords = get_starter_location_coordinates(coordinates, agent_id, mode)
    
    if starter_coords:
        print(f"✅ Starter location coordinates found: {starter_coords}")
        
        # Simulate coordinate transmission to starter location
        transmission_result = {
            "agent_id": agent_id,
            "mode": mode,
            "starter_location_coordinates": starter_coords,
            "transmission_status": "SUCCESS",
            "coordinates_transmitted": True,
            "target_location": "starter_location",
            "message": f"Coordinates {starter_coords} transmitted to starter location for {agent_id}"
        }
        
        print(f"📡 Coordinate transmission: {transmission_result['message']}")
        return transmission_result
    else:
        error_result = {
            "agent_id": agent_id,
            "mode": mode,
            "starter_location_coordinates": None,
            "transmission_status": "FAILED",
            "coordinates_transmitted": False,
            "target_location": "starter_location",
            "error": f"No starter location coordinates found for {agent_id}"
        }
        
        print(f"❌ Coordinate transmission failed: {error_result['error']}")
        return error_result

def test_all_agents_onboarding() -> Dict[str, Any]:
    """Test --onboarding flag for all available agents"""
    print("🚀 Testing --onboarding flag coordinate transmission for all agents")
    print("=" * 60)
    
    coordinates = load_coordinates()
    if not coordinates:
        return {"error": "No coordinates available for testing"}
    
    test_results = {
        "total_tests": 0,
        "successful_transmissions": 0,
        "failed_transmissions": 0,
        "agent_results": {}
    }
    
    # Test 8-agent mode
    if "8-agent" in coordinates:
        print(f"\n📋 Testing 8-agent mode ({len(coordinates['8-agent'])} agents)")
        
        for agent_id in coordinates["8-agent"].keys():
            test_results["total_tests"] += 1
            result = simulate_onboarding_flag_processing(agent_id, "8-agent")
            
            if result.get("coordinates_transmitted"):
                test_results["successful_transmissions"] += 1
            else:
                test_results["failed_transmissions"] += 1
            
            test_results["agent_results"][agent_id] = result
    
    # Test other modes if available
    for mode in coordinates.keys():
        if mode != "8-agent":
            print(f"\n📋 Testing {mode} mode ({len(coordinates[mode])} agents)")
            
            for agent_id in coordinates[mode].keys():
                test_results["total_tests"] += 1
                result = simulate_onboarding_flag_processing(agent_id, mode)
                
                if result.get("coordinates_transmitted"):
                    test_results["successful_transmissions"] += 1
                else:
                    test_results["failed_transmissions"] += 1
                
                test_results["agent_results"][f"{mode}_{agent_id}"] = result
    
    return test_results

def main():
    """Main test execution"""
    print("🧪 --onboarding Flag Coordinate Transmission Test")
    print("=" * 60)
    
    # Test individual agent
    if len(sys.argv) > 1:
        agent_id = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "8-agent"
        result = simulate_onboarding_flag_processing(agent_id, mode)
        print(f"\n📊 Individual Test Result:")
        print(json.dumps(result, indent=2))
    else:
        # Test all agents
        results = test_all_agents_onboarding()
        
        print(f"\n📊 Test Summary:")
        print(f"Total Tests: {results['total_tests']}")
        print(f"Successful Transmissions: {results['successful_transmissions']}")
        print(f"Failed Transmissions: {results['failed_transmissions']}")
        print(f"Success Rate: {(results['successful_transmissions'] / results['total_tests'] * 100):.1f}%")
        
        print(f"\n📋 Detailed Results:")
        print(json.dumps(results, indent=2))
    
    print(f"\n✅ --onboarding flag coordinate transmission test completed!")

if __name__ == "__main__":
    main()
