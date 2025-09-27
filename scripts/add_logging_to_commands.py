#!/usr/bin/env python3
"""
Add Logging to Commands Script
===============================

Automatically adds comprehensive logging and error handling to all Discord commands.
"""

import os
import re
from pathlib import Path


def add_logging_to_command_file(file_path: str):
    """Add logging to a command file."""
    print(f"🔧 Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has logging imports
    if 'command_logger_decorator' in content:
        print(f"✅ {file_path} already has logging - skipping")
        return
    
    # Add imports
    import_pattern = r'(import discord\nfrom discord import app_commands)'
    if re.search(import_pattern, content):
        new_imports = """import discord
from discord import app_commands
import logging
from src.services.discord_bot.core.command_logger import command_logger_decorator, command_logger

logger = logging.getLogger(__name__)"""
        content = re.sub(import_pattern, new_imports, content)
    
    # Add decorator to all command functions
    command_pattern = r'(@bot\.tree\.command\([^)]+\)\s*\n\s*async def (\w+)\([^)]*\):)'
    
    def add_decorator_and_try_catch(match):
        decorator = match.group(1)
        func_name = match.group(2)
        
        # Add decorator
        new_decorator = f"@command_logger_decorator(command_logger)\n    {decorator}"
        
        return new_decorator
    
    # Apply decorator
    content = re.sub(command_pattern, add_decorator_and_try_catch, content)
    
    # Add try-catch blocks to command functions
    # This is more complex and would need careful parsing
    # For now, let's just add the imports and decorators
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Added logging to {file_path}")


def main():
    """Main function to add logging to all command files."""
    commands_dir = Path("src/services/discord_bot/commands")
    
    if not commands_dir.exists():
        print(f"❌ Commands directory not found: {commands_dir}")
        return
    
    command_files = list(commands_dir.glob("*.py"))
    
    print(f"🔍 Found {len(command_files)} command files:")
    for file_path in command_files:
        print(f"  - {file_path.name}")
    
    print("\n🚀 Adding logging to all command files...")
    
    for file_path in command_files:
        try:
            add_logging_to_command_file(str(file_path))
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n✅ Logging addition complete!")


if __name__ == "__main__":
    main()
