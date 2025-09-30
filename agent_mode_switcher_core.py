#!/usr/bin/env python3
"""
Core logic for agent mode switcher.
"""

import os
import yaml


class AgentModeSwitcher:
    """Agent Mode Switcher utility."""
    
    def __init__(self):
        """Initialize the switcher."""
        self.config_path = "config/unified_config.yaml"
    
    def load_config(self):
        """Load current configuration."""
        if not os.path.exists(self.config_path):
            print(f"❌ Configuration file not found: {self.config_path}")
            return None

        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def save_config(self, config):
        """Save configuration."""
        with open(self.config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    def switch_mode(self, mode_name):
        """Switch to specified agent mode."""
        config = self.load_config()
        if not config:
            return False

        # Check if mode exists
        if "agent_modes" not in config or mode_name not in config["agent_modes"]:
            print(f"❌ Unknown mode: {mode_name}")
            print(f"Available modes: {list(config.get('agent_modes', {}).keys())}")
            return False

        mode_config = config["agent_modes"][mode_name]

        # Update coordination mode
        config["coordination_mode"] = mode_name
        config["active_agents"] = len(mode_config["active_agents"])

        # Update agent enabled status
        for agent_id in config["agents"]:
            if agent_id in mode_config["active_agents"]:
                config["agents"][agent_id]["enabled"] = True
            else:
                config["agents"][agent_id]["enabled"] = False

        # Save configuration
        self.save_config(config)

        print(f"✅ Switched to {mode_config['name']}")
        print(f"📊 Active Agents: {len(mode_config['active_agents'])}")
        print(f"🎯 Mode: {mode_config['description']}")

        return True
    
    def show_status(self):
        """Show current mode status."""
        config = self.load_config()
        if not config:
            return

        current_mode = config.get("coordination_mode", "unknown")
        active_count = config.get("active_agents", 0)

        print("🤖 AGENT MODE STATUS")
        print("=" * 30)
        print(f"📊 Current Mode: {current_mode}")
        print(f"📈 Active Agents: {active_count}")

        if "agent_modes" in config and current_mode in config["agent_modes"]:
            mode_info = config["agent_modes"][current_mode]
            print(f"🎯 Team: {mode_info['name']}")
            print(f"📝 Description: {mode_info['description']}")

            print("\n✅ ACTIVE AGENTS:")
            for agent_id in mode_info["active_agents"]:
                agent = config["agents"][agent_id]
                name = agent["name"]
                role = agent["role"]
                coords = agent["coordinates"]
                print(f"  • {agent_id}: {name} ({role}) at {coords}")

            if mode_info["inactive_agents"]:
                print("\n💤 INACTIVE AGENTS:")
                for agent_id in mode_info["inactive_agents"]:
                    agent = config["agents"][agent_id]
                    name = agent["name"]
                    print(f"  • {agent_id}: {name}")

        print("\n🔄 AVAILABLE MODES:")
        for mode_name, mode_info in config.get("agent_modes", {}).items():
            status = "✅ CURRENT" if mode_name == current_mode else "🔄 Available"
            print(
                f"  {status} {mode_name}: {mode_info['name']} ({len(mode_info['active_agents'])} agents)"
            )
    
    def show_help(self):
        """Show help information."""
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
