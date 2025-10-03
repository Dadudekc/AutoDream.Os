#!/usr/bin/env python3
"""
Quick fix script to add safe_command decorator and error handling to all Discord commands
"""

import os
import re
from pathlib import Path

# List of command modules to fix
COMMAND_MODULES = [
    "src/services/discord_bot/commands/messaging_commands.py",
    "src/services/discord_bot/commands/devlog_commands.py", 
    "src/services/discord_bot/commands/system_commands.py",
    "src/services/discord_bot/commands/project_update_core_commands.py",
    "src/services/discord_bot/commands/project_update_specialized_commands.py",
    "src/services/discord_bot/commands/project_update_management_commands.py",
    "src/services/discord_bot/commands/onboarding_commands.py",
    "src/services/discord_bot/commands/messaging_advanced_commands.py"
]

def fix_command_module(file_path):
    """Fix a single command module by adding safe_command decorator and error handling."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already fixed
    if "from src.services.discord_bot.commands.basic_commands import safe_command" in content:
        print(f"Already fixed: {file_path}")
        return
    
    # Add imports
    if "import logging" not in content:
        content = content.replace(
            "import discord\nfrom discord import app_commands",
            "import discord\nfrom discord import app_commands\nimport logging\nfrom src.services.discord_bot.commands.basic_commands import safe_command"
        )
    else:
        content = content.replace(
            "import discord\nfrom discord import app_commands",
            "import discord\nfrom discord import app_commands\nfrom src.services.discord_bot.commands.basic_commands import safe_command"
        )
    
    # Add logger
    if "logger = logging.getLogger(__name__)" not in content:
        content = content.replace(
            "def setup_",
            "logger = logging.getLogger(__name__)\n\n\ndef setup_"
        )
    
    # Add @safe_command decorator to all command functions
    # Pattern: @bot.tree.command(...) followed by async def
    pattern = r'(@bot\.tree\.command\([^)]+\))\s*\n\s*(@app_commands\.describe\([^)]+\)\s*\n\s*)?async def (\w+)'
    replacement = r'\1\n    @safe_command\n    \2async def \3'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Also handle commands without @app_commands.describe
    pattern2 = r'(@bot\.tree\.command\([^)]+\))\s*\n\s*async def (\w+)'
    replacement2 = r'\1\n    @safe_command\n    async def \2'
    content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {file_path}")

def main():
    """Fix all command modules."""
    print("Fixing Discord command modules...")
    
    for module_path in COMMAND_MODULES:
        fix_command_module(module_path)
    
    print("Done! All command modules have been updated with safe_command decorator.")

if __name__ == "__main__":
    main()
