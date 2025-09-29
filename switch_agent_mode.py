#!/usr/bin/env python3
"""
Agent Mode Switcher
==================

Simple utility to switch between different agent modes using the 8-agent framework.

Usage:
    python switch_agent_mode.py four_agent_mode_a    # Switch to Infrastructure & Core Team
    python switch_agent_mode.py four_agent_mode_b    # Switch to Foundation Team  
    python switch_agent_mode.py five_agent           # Switch to Quality Focus Team
    python switch_agent_mode.py eight_agent          # Switch to Full Swarm
    python switch_agent_mode.py --status             # Show current mode

Author: Agent-8 (Integration Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

import argparse
import yaml
import os
from pathlib import Path

def load_config():
    """Load current configuration"""
    config_path = "config/unified_config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_config(config):
    """Save configuration"""
    config_path = "config/unified_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

def switch_mode(mode_name):
    """Switch to specified agent mode"""
    config = load_config()
    if not config:
        return False
    
    # Check if mode exists
    if 'agent_modes' not in config or mode_name not in config['agent_modes']:
        print(f"❌ Unknown mode: {mode_name}")
        print(f"Available modes: {list(config.get('agent_modes', {}).keys())}")
        return False
    
    mode_config = config['agent_modes'][mode_name]
    
    # Update coordination mode
    config['coordination_mode'] = mode_name
    config['active_agents'] = len(mode_config['active_agents'])
    
    # Update agent enabled status
    for agent_id in config['agents']:
        if agent_id in mode_config['active_agents']:
            config['agents'][agent_id]['enabled'] = True
        else:
            config['agents'][agent_id]['enabled'] = False
    
    # Save configuration
    save_config(config)
    
    print(f"✅ Switched to {mode_config['name']}")
    print(f"📊 Active Agents: {len(mode_config['active_agents'])}")
    print(f"🎯 Mode: {mode_config['description']}")
    
    return True

def show_status():
    """Show current mode status"""
    config = load_config()
    if not config:
        return
    
    current_mode = config.get('coordination_mode', 'unknown')
    active_count = config.get('active_agents', 0)
    
    print("🤖 AGENT MODE STATUS")
    print("=" * 30)
    print(f"📊 Current Mode: {current_mode}")
    print(f"📈 Active Agents: {active_count}")
    
    if 'agent_modes' in config and current_mode in config['agent_modes']:
        mode_info = config['agent_modes'][current_mode]
        print(f"🎯 Team: {mode_info['name']}")
        print(f"📝 Description: {mode_info['description']}")
        
        print(f"\n✅ ACTIVE AGENTS:")
        for agent_id in mode_info['active_agents']:
            agent = config['agents'][agent_id]
            name = agent['name']
            role = agent['role']
            coords = agent['coordinates']
            print(f"  • {agent_id}: {name} ({role}) at {coords}")
        
        if mode_info['inactive_agents']:
            print(f"\n💤 INACTIVE AGENTS:")
            for agent_id in mode_info['inactive_agents']:
                agent = config['agents'][agent_id]
                name = agent['name']
                print(f"  • {agent_id}: {name}")
    
    print(f"\n🔄 AVAILABLE MODES:")
    for mode_name, mode_info in config.get('agent_modes', {}).items():
        status = "✅ CURRENT" if mode_name == current_mode else "🔄 Available"
        print(f"  {status} {mode_name}: {mode_info['name']} ({len(mode_info['active_agents'])} agents)")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Agent Mode Switcher")
    parser.add_argument('mode', nargs='?', help='Mode to switch to')
    parser.add_argument('--status', action='store_true', help='Show current status')
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
    elif args.mode:
        switch_mode(args.mode)
    else:
        print("🤖 AGENT MODE SWITCHER")
        print("=" * 30)
        print()
        print("USAGE:")
        print("  python switch_agent_mode.py [MODE]")
        print("  python switch_agent_mode.py --status")
        print()
        print("AVAILABLE MODES:")
        print("  four_agent_mode_a  - Infrastructure & Core Team (Agent-3,4,7,8)")
        print("  four_agent_mode_b  - Foundation Team (Agent-1,2,3,4)")
        print("  five_agent         - Quality Focus Team (Agent-4,5,6,7,8)")
        print("  eight_agent        - Full Swarm (All 8 agents)")
        print()
        print("EXAMPLES:")
        print("  python switch_agent_mode.py four_agent_mode_a")
        print("  python switch_agent_mode.py --status")

if __name__ == "__main__":
    main()
