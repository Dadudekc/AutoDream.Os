#!/usr/bin/env python3
"""
Coordinate Validator - Validate Agent Coordinates Before Operations
Ensures all agent coordinates are valid before PyAutoGUI operations.
"""

import sys
import json
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


def load_coordinates() -> dict:
    """Load coordinates from cursor_agent_coords.json."""
    coords_file = repo_root / "cursor_agent_coords.json"
    
    if not coords_file.exists():
        print(f"❌ Coordinates file not found: {coords_file}")
        return {}
    
    with open(coords_file, 'r') as f:
        return json.load(f)


def validate_coordinate(agent_id: str, coord_type: str, coords: list) -> dict:
    """Validate a single coordinate."""
    issues = []
    
    # Check format
    if not isinstance(coords, list):
        issues.append(f"Not a list: {type(coords)}")
        return {'valid': False, 'issues': issues}
    
    if len(coords) < 2:
        issues.append(f"Invalid length: {len(coords)} (need 2)")
        return {'valid': False, 'issues': issues}
    
    x, y = coords[0], coords[1]
    
    # Check types
    if not isinstance(x, (int, float)):
        issues.append(f"X coordinate not numeric: {type(x)}")
    
    if not isinstance(y, (int, float)):
        issues.append(f"Y coordinate not numeric: {type(y)}")
    
    # Check bounds (reasonable screen coordinates)
    if isinstance(x, (int, float)):
        if x < -3840 or x > 3840:  # Support ultra-wide monitors
            issues.append(f"X coordinate out of bounds: {x}")
    
    if isinstance(y, (int, float)):
        if y < -2160 or y > 2160:  # Support 4K monitors
            issues.append(f"Y coordinate out of bounds: {y}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'x': x,
        'y': y
    }


def main():
    """Validate all agent coordinates."""
    
    print(f"🎯 COORDINATE VALIDATION")
    print(f"=" * 70)
    print()
    
    coords_data = load_coordinates()
    
    if not coords_data:
        return 1
    
    total_agents = 0
    total_coords = 0
    invalid_coords = 0
    
    for agent_id, agent_coords in coords_data.items():
        if not agent_id.startswith('Agent-'):
            continue
        
        total_agents += 1
        print(f"🤖 {agent_id}")
        print(f"-" * 70)
        
        # Validate chat coordinates
        if 'chat' in agent_coords:
            total_coords += 1
            result = validate_coordinate(agent_id, 'chat', agent_coords['chat'])
            
            if result['valid']:
                print(f"  ✅ Chat: ({result['x']}, {result['y']})")
            else:
                invalid_coords += 1
                print(f"  ❌ Chat: INVALID")
                for issue in result['issues']:
                    print(f"     - {issue}")
        
        # Validate onboarding coordinates
        if 'onboarding' in agent_coords:
            total_coords += 1
            result = validate_coordinate(agent_id, 'onboarding', agent_coords['onboarding'])
            
            if result['valid']:
                print(f"  ✅ Onboarding: ({result['x']}, {result['y']})")
            else:
                invalid_coords += 1
                print(f"  ❌ Onboarding: INVALID")
                for issue in result['issues']:
                    print(f"     - {issue}")
        
        print()
    
    # Summary
    print(f"=" * 70)
    print(f"📊 VALIDATION SUMMARY")
    print(f"=" * 70)
    print(f"Agents validated: {total_agents}")
    print(f"Total coordinates: {total_coords}")
    print(f"Valid coordinates: {total_coords - invalid_coords}")
    print(f"Invalid coordinates: {invalid_coords}")
    print()
    
    if invalid_coords == 0:
        print("✅ All coordinates are valid!")
        return 0
    else:
        print(f"❌ Found {invalid_coords} invalid coordinates!")
        print("\nFix these in cursor_agent_coords.json before running PyAutoGUI operations.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

