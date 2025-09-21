#!/usr/bin/env python3
"""
Test script to verify .env file loading
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print("🔍 Testing .env file loading...")
print("=" * 50)

# Check Discord bot token
discord_token = os.getenv('DISCORD_BOT_TOKEN')
discord_channel = os.getenv('DISCORD_CHANNEL_ID')

print(f"Discord Bot Token: {'✅ Found' if discord_token else '❌ Not found'}")
print(f"Discord Channel ID: {'✅ Found' if discord_channel else '❌ Not found'}")

if discord_token:
    print(f"Token starts with: {discord_token[:10]}...")
if discord_channel:
    print(f"Channel ID: {discord_channel}")

print("\n🎯 Environment loading test complete!")
