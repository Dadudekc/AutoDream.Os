#!/usr/bin/env python3
"""
Simple Bot Status Indicator
===========================

Simple tool to check Discord bot status without Unicode issues.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_bot_status():
    """Check if the Discord bot is running and connected"""
    print("V2_SWARM Discord Bot Status Check")
    print("=" * 40)

    # Set token
    os.environ['DISCORD_BOT_TOKEN'] = 'MTLxNTQ5NTA3NzUxNzU5NDcxNA.GRbCPL.hfyDk7J3_PZ_6NDEqy-2n7pDdWX7XQGEgpN-NA'

    try:
        # Test bot connection
        result = subprocess.run([
            sys.executable,
            'scripts/execution/run_discord_agent_bot.py',
            '--test'
        ], capture_output=True, text=True, timeout=15)

        if result.returncode == 0:
            print("SUCCESS: Bot connection test passed!")
            print("The Discord bot is online and ready.")
            print("")
            print("Next steps:")
            print("1. Check your Discord server for 'DISCORD COMMANDER ONLINE' message")
            print("2. Try commands like !ping, !help, !summary1")
            print("3. The bot should respond to commands in Discord")
            print("")
            print("Available commands:")
            print("- !ping (test responsiveness)")
            print("- !help (show all commands)")
            print("- !agents (list agents)")
            print("- !summary1-4 (agent summaries)")
            return True
        else:
            print("FAILED: Bot connection test failed")
            print("Check your bot token and Discord permissions")
            return False

    except subprocess.TimeoutExpired:
        print("TIMEOUT: Bot test took too long")
        print("This might indicate a connection issue")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def show_invite_link():
    """Show the Discord bot invite link"""
    print("")
    print("Bot Invite Link:")
    print("https://discord.com/api/oauth2/authorize?client_id=1415495077517594714&permissions=414464658496&scope=bot%20applications.commands")
    print("")
    print("Copy and paste this link into your browser to invite the bot to your server.")

if __name__ == "__main__":
    success = check_bot_status()

    if success:
        print("")
        print("STATUS: ONLINE - Bot is connected and ready!")
        show_invite_link()
    else:
        print("")
        print("STATUS: OFFLINE - Bot has connection issues")
        print("Check your Discord bot token and try again")
        show_invite_link()
