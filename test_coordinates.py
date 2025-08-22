#!/usr/bin/env python3
"""
Test Coordinate Loading
======================

This script tests the coordinate loading to see what's actually being loaded.
"""

import json
from pathlib import Path

def test_coordinate_loading():
    """Test coordinate loading from file"""
    print("🧪 TESTING COORDINATE LOADING")
    print("="*50)
    
    # Test loading the file directly
    config_path = Path("config/cursor_agent_coords.json")
    if config_path.exists():
        print(f"✅ Found coordinate file: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 File contains layouts: {list(data.keys())}")
        
        # Check 8-agent layout
        layout_8 = data.get("8-agent", {})
        if layout_8:
            print(f"\n🎯 8-Agent Layout Found:")
            print(f"   Total agents: {len(layout_8)}")
            
            for agent_id, agent_info in layout_8.items():
                input_box = agent_info.get("input_box", {})
                starter_box = agent_info.get("starter_location_box", {})
                
                print(f"\n   📍 {agent_id}:")
                print(f"      Input Box: ({input_box.get('x', 'N/A')}, {input_box.get('y', 'N/A')})")
                print(f"      Starter Box: ({starter_box.get('x', 'N/A')}, {starter_box.get('y', 'N/A')})")
                
                # Check if coordinates are valid
                if input_box.get('x') is not None and input_box.get('y') is not None:
                    print(f"      ✅ Valid input coordinates")
                else:
                    print(f"      ❌ Invalid input coordinates")
                    
                if starter_box.get('x') is not None and starter_box.get('y') is not None:
                    print(f"      ✅ Valid starter coordinates")
                else:
                    print(f"      ❌ Invalid starter coordinates")
        else:
            print("❌ 8-agent layout not found!")
            
    else:
        print(f"❌ Coordinate file not found: {config_path}")
    
    print("\n" + "="*50)
    print("🎯 Coordinate loading test complete!")

if __name__ == "__main__":
    test_coordinate_loading()

