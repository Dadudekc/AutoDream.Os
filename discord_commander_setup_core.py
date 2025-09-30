"""
Discord Commander Setup Core - V2 Compliant
==========================================

Core Discord Commander setup functionality.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from discord_bot_config import config as discord_config
except ImportError:
    print("❌ Error: Cannot import discord_bot_config")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


class DiscordCommanderSetupCore:
    """Core Discord Commander setup functionality."""
    
    def __init__(self):
        """Initialize setup core."""
        self.env_file = Path(__file__).parent / ".env"
        self.template_file = Path(__file__).parent / ".env.template"
        self.env_vars = {}
    
    def welcome_message(self):
        """Display welcome message."""
        print("🐝 Discord Commander Setup Wizard - 5-Agent Mode")
        print("=" * 50)
        print("WE ARE SWARM - Discord Commander Configuration")
        print("5-Agent Mode: Agent-4, Agent-5, Agent-6, Agent-7, Agent-8")
        print("=" * 50)
        print()
        print("This wizard will help you configure your Discord Commander.")
        print("You'll need to set up a Discord bot first:")
        print()
        print("1. Go to https://discord.com/developers/applications")
        print("2. Create a new application")
        print("3. Go to the 'Bot' section and create a bot")
        print("4. Copy the bot token")
        print("5. Go to OAuth2 -> URL Generator")
        print("6. Select 'bot' scope and required permissions")
        print("7. Copy the generated URL and invite bot to your server")
        print()
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with optional default."""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    
    def create_env_file(self) -> bool:
        """Create .env file with user input."""
        try:
            print("\n📝 Creating .env file...")
            
            # Get Discord bot token
            bot_token = self.get_user_input("Enter your Discord bot token")
            if not bot_token:
                print("❌ Bot token is required!")
                return False
            
            # Get Discord channel ID
            channel_id = self.get_user_input("Enter your Discord channel ID")
            if not channel_id:
                print("❌ Channel ID is required!")
                return False
            
            # Get Discord guild ID
            guild_id = self.get_user_input("Enter your Discord guild ID")
            if not guild_id:
                print("❌ Guild ID is required!")
                return False
            
            # Create .env content
            env_content = f"""# Discord Commander Configuration
DISCORD_BOT_TOKEN={bot_token}
DISCORD_CHANNEL_ID={channel_id}
DISCORD_GUILD_ID={guild_id}

# Agent Configuration
AGENT_MODE=5-agent
ACTIVE_AGENTS=Agent-4,Agent-5,Agent-6,Agent-7,Agent-8

# System Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false
"""
            
            # Write .env file
            with open(self.env_file, 'w') as f:
                f.write(env_content)
            
            print(f"✅ .env file created at {self.env_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def validate_setup(self) -> bool:
        """Validate the setup configuration."""
        try:
            print("\n🔍 Validating setup...")
            
            # Check if .env file exists
            if not self.env_file.exists():
                print("❌ .env file not found!")
                return False
            
            # Check if required variables are set
            required_vars = ["DISCORD_BOT_TOKEN", "DISCORD_CHANNEL_ID", "DISCORD_GUILD_ID"]
            
            with open(self.env_file, 'r') as f:
                env_content = f.read()
            
            for var in required_vars:
                if var not in env_content:
                    print(f"❌ Required variable {var} not found in .env file!")
                    return False
            
            print("✅ Setup validation passed!")
            return True
            
        except Exception as e:
            print(f"❌ Error validating setup: {e}")
            return False
    
    def run_setup(self) -> bool:
        """Run the complete setup process."""
        try:
            self.welcome_message()
            
            # Create .env file
            if not self.create_env_file():
                return False
            
            # Validate setup
            if not self.validate_setup():
                return False
            
            print("\n🎉 Discord Commander setup complete!")
            print("You can now run the Discord Commander with:")
            print("python discord_commander.py")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
