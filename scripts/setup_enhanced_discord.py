#!/usr/bin/env python3
"""
Enhanced Discord Integration Setup Script
==========================================

Setup script for Agent-1 to configure the enhanced Discord integration
with individual agent channels.

Usage:
    python scripts/setup_enhanced_discord.py

Author: Agent-3 (DevOps Specialist) - Discord Expansion Coordinator
License: MIT
"""

import json
from pathlib import Path


class EnhancedDiscordSetup:
    """Setup class for enhanced Discord integration."""

    def __init__(self):
        """Initialize setup class."""
        self.config_dir = Path("config")
        self.scripts_dir = Path("scripts")
        self.discord_dir = Path("src/discord_commander")

        self.template_file = self.config_dir / "discord_channels_template.json"
        self.config_file = self.config_dir / "discord_channels.json"
        self.coordination_file = Path("AGENT-1_DISCORD_COORDINATION.md")

    def run_setup(self) -> bool:
        """Run the complete setup process."""
        print("🎯 Enhanced Discord Integration Setup")
        print("=" * 60)
        print("Setting up individual agent channels for V2_SWARM")
        print()

        # Check prerequisites
        if not self.check_prerequisites():
            return False

        # Create configuration
        if not self.create_configuration():
            return False

        # Setup coordination
        if not self.setup_coordination():
            return False

        # Create helper scripts
        if not self.create_helper_scripts():
            return False

        # Final instructions
        self.show_final_instructions()

        return True

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        print("📋 Checking Prerequisites...")

        prerequisites_ok = True

        # Check directories
        required_dirs = [self.config_dir, self.scripts_dir, self.discord_dir]
        for dir_path in required_dirs:
            if dir_path.exists():
                print(f"✅ {dir_path} exists")
            else:
                print(f"❌ {dir_path} missing - creating...")
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {dir_path} created")

        # Check enhanced integration file
        enhanced_file = self.discord_dir / "enhanced_discord_integration.py"
        if enhanced_file.exists():
            print("✅ Enhanced Discord integration file exists")
        else:
            print("❌ Enhanced Discord integration file missing")
            print("   Please ensure Agent-3 has created the enhanced integration")
            prerequisites_ok = False

        # Check template file
        if self.template_file.exists():
            print("✅ Discord channels template exists")
        else:
            print("❌ Discord channels template missing")
            print("   Please ensure the template file has been created")
            prerequisites_ok = False

        # Check coordination file
        if self.coordination_file.exists():
            print("✅ Agent-1 coordination file exists")
        else:
            print("⚠️  Agent-1 coordination file not found")
            print("   This is normal if Agent-3 hasn't created it yet")

        print()
        return prerequisites_ok

    def create_configuration(self) -> bool:
        """Create the Discord channels configuration."""
        print("⚙️  Creating Discord Channels Configuration...")

        try:
            # Load template
            with open(self.template_file) as f:
                template_config = json.load(f)

            # Check if config already exists
            if self.config_file.exists():
                print("⚠️  Discord channels config already exists")
                overwrite = input("Overwrite existing configuration? (y/N): ").lower().strip()
                if overwrite != "y":
                    print("✅ Keeping existing configuration")
                    return True

            # Create configuration from template
            config = template_config.copy()

            # Save configuration
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)

            print("✅ Discord channels configuration created")
            print(f"   Location: {self.config_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to create configuration: {e}")
            return False

    def setup_coordination(self) -> bool:
        """Setup coordination with Agent-3."""
        print("🤝 Setting up Agent Coordination...")

        try:
            # Create agent inbox coordination
            inbox_dir = Path("agent_workspaces/Agent-1/inbox")
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create coordination message for Agent-1
            coordination_message = f"""# 🚨 ENHANCED DISCORD INTEGRATION COORDINATION

## From: Agent-3 (DevOps Specialist)
## To: Agent-1 (Integration Specialist)
## Priority: HIGH

### **COORDINATION STATUS: ACTIVE**

Enhanced Discord integration has been implemented with individual agent channels.

### **REQUIRED ACTIONS:**

1. **Discord Server Setup:**
   - Create channels: #agent-1, #agent-2, #agent-3, #agent-4, #agent-5, #agent-6, #agent-7, #agent-8
   - Create channels: #swarm-general, #swarm-coordination, #swarm-alerts
   - Create webhooks for each channel

2. **Configuration:**
   - Update `{self.config_file}` with webhook URLs
   - Test each channel connection

3. **Integration Testing:**
   - Run test script: `python scripts/test_enhanced_discord.py`
   - Verify agent-to-agent communication

### **CONTACT:**
- Respond via Discord channels once configured
- Use Agent-3's inbox: `agent_workspaces/Agent-3/inbox/`

**🐝 WE ARE SWARM - Ready for Discord channel integration!**
"""

            # Save coordination message
            coord_file = inbox_dir / "AGENT-3_DISCORD_COORDINATION.md"
            with open(coord_file, "w", encoding="utf-8") as f:
                f.write(coordination_message)

            print("✅ Agent coordination setup complete")
            print(f"   Coordination message: {coord_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to setup coordination: {e}")
            return False

    def create_helper_scripts(self) -> bool:
        """Create helper scripts for Agent-1."""
        print("🔧 Creating Helper Scripts...")

        try:
            # Create webhook configuration helper
            webhook_config_script = '''#!/usr/bin/env python3
"""
Discord Webhook Configuration Helper
====================================

Helper script to configure Discord webhooks for agent channels.

Usage:
    python scripts/configure_discord_webhooks.py
"""

import json
from pathlib import Path

def configure_webhooks():
    """Configure webhooks for all channels."""
    config_file = Path("config/discord_channels.json")

    if not config_file.exists():
        print("❌ Configuration file not found")
        return False

    print("🔧 Discord Webhook Configuration")
    print("=" * 40)

    # Load current config
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Configure each channel
    for channel_name, channel_config in config.items():
        print(f"\n📺 Configuring {channel_name}...")
        print(f"   Description: {channel_config.get('description', 'N/A')}")

        current_webhook = channel_config.get('webhook_url')
        if current_webhook:
            print(f"   Current webhook: {current_webhook[:50]}...")
            change = input("   Change webhook? (y/N): ").lower().strip()
            if change != 'y':
                continue

        # Get new webhook URL
        webhook_url = input(f"   Enter webhook URL for {channel_name}: ").strip()
        if webhook_url:
            config[channel_name]['webhook_url'] = webhook_url
            print("   ✅ Webhook configured")
        else:
            print("   ⚠️  Skipped webhook configuration")

    # Save updated config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print("\n✅ Webhook configuration complete!")
    return True

if __name__ == "__main__":
    configure_webhooks()
'''

            # Save webhook configuration script
            webhook_script_path = self.scripts_dir / "configure_discord_webhooks.py"
            with open(webhook_script_path, "w", encoding="utf-8") as f:
                f.write(webhook_config_script)

            print("✅ Webhook configuration helper created")
            print(f"   Location: {webhook_script_path}")
            return True

        except Exception as e:
            print(f"❌ Failed to create helper scripts: {e}")
            return False

    def show_final_instructions(self) -> None:
        """Show final setup instructions."""
        print("\n🎉 Enhanced Discord Integration Setup Complete!")
        print("=" * 60)
        print()
        print("📋 NEXT STEPS FOR AGENT-1:")
        print()
        print("1. 🎮 Create Discord Channels:")
        print("   - Individual: #agent-1 through #agent-8")
        print("   - Swarm: #swarm-general, #swarm-coordination, #swarm-alerts")
        print()
        print("2. 🔗 Create Webhooks:")
        print("   - Generate webhook URLs for each channel")
        print("   - Note down all webhook URLs")
        print()
        print("3. ⚙️ Configure Webhooks:")
        print("   python scripts/configure_discord_webhooks.py")
        print()
        print("4. 🧪 Test Integration:")
        print("   python scripts/test_enhanced_discord.py")
        print()
        print("5. 🤝 Coordinate with Agent-3:")
        print("   - Use configured Discord channels")
        print("   - Confirm successful integration")
        print()
        print("📁 Configuration Files:")
        print(f"   - Template: {self.template_file}")
        print(f"   - Config: {self.config_file}")
        print(f"   - Coordination: {self.coordination_file}")
        print()
        print("🐝 WE ARE SWARM - Discord channels ready for integration!")


def main():
    """Main setup function."""
    setup = EnhancedDiscordSetup()
    success = setup.run_setup()

    if success:
        print("\n✅ Setup completed successfully!")
        print("Agent-1 can now proceed with Discord server configuration.")
    else:
        print("\n❌ Setup failed!")
        print("Please check the error messages above and try again.")

    return success


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
