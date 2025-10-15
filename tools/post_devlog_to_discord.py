#!/usr/bin/env python3
"""Quick script to post devlog to Discord."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment
load_dotenv()

def post_devlog_to_discord(devlog_file: str) -> bool:
    """Post devlog content to Discord webhook."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ ERROR: DISCORD_WEBHOOK_URL not found in environment")
        return False
    
    # Read devlog content
    devlog_path = Path(devlog_file)
    if not devlog_path.exists():
        print(f"❌ ERROR: Devlog file not found: {devlog_file}")
        return False
    
    content = devlog_path.read_text(encoding='utf-8')
    
    # Create Discord message
    payload = {
        "content": f"# 📊 REPO ANALYSIS DEVLOG\n\n{content[:1900]}...",  # Discord limit
        "username": "Agent-5 BI Analyst",
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print(f"✅ SUCCESS: Devlog posted to Discord!")
            print(f"   File: {devlog_file}")
            return True
        else:
            print(f"❌ ERROR: Discord API returned {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR posting to Discord: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_devlog_to_discord.py <devlog_file>")
        sys.exit(1)
    
    devlog_file = sys.argv[1]
    success = post_devlog_to_discord(devlog_file)
    sys.exit(0 if success else 1)

