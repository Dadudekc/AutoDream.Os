#!/usr/bin/env python3
"""
Post Captain's Announcement to Discord - Agent Cellphone V2
==========================================================

Actually posts the Captain's announcement to Discord using webhook.
This is the real implementation that will send the message to Discord.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

def post_to_discord_webhook(webhook_url: str, content: str) -> bool:
    """Post message to Discord webhook"""
    try:
        # Discord webhook payload
        payload = {
            "content": content,
            "username": "Captain Agent-1",
            "avatar_url": "https://cdn.discordapp.com/emojis/🎖️.png",
            "tts": False
        }
        
        # Send POST request to Discord webhook
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print("✅ Message successfully posted to Discord!")
            return True
        else:
            print(f"❌ Failed to post to Discord. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error posting to Discord: {e}")
        return False
    except Exception as e:
        print(f"❌ Error posting to Discord: {e}")
        return False

def main():
    """Main function to post Captain's announcement to Discord"""
    print("🎖️  POSTING CAPTAIN'S ANNOUNCEMENT TO DISCORD")
    print("="*60)
    
    # Check if Captain's announcement exists
    announcement_file = Path("logs/captain_announcement.md")
    if not announcement_file.exists():
        print("❌ Captain's announcement file not found!")
        print("   Run 'python scripts/generate_captain_announcement.py' first")
        return False
    
    # Load the announcement
    with open(announcement_file, 'r', encoding='utf-8') as f:
        announcement_content = f.read()
    
    print(f"✅ Loaded Captain's announcement ({len(announcement_content)} characters)")
    
    # Get Discord webhook URL
    print("\n📱 DISCORD WEBHOOK CONFIGURATION:")
    print("="*40)
    
    # Check for environment variable first
    import os
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if webhook_url:
        print(f"✅ Found webhook URL from environment variable")
    else:
        print("❌ No DISCORD_WEBHOOK_URL environment variable found")
        print("\n💡 You can:")
        print("   1. Set DISCORD_WEBHOOK_URL environment variable")
        print("   2. Enter the webhook URL manually below")
        print("   3. Create a webhook in your Discord server")
        
        webhook_url = input("\n🔗 Enter Discord webhook URL (or press Enter to skip): ").strip()
        
        if not webhook_url:
            print("❌ No webhook URL provided. Cannot post to Discord.")
            print("💡 The announcement is saved in logs/captain_announcement.md")
            print("   Copy and paste it manually to your Discord devlog channel")
            return False
    
    # Validate webhook URL format (handle both discord.com and discordapp.com)
    if not (webhook_url.startswith("https://discord.com/api/webhooks/") or 
            webhook_url.startswith("https://discordapp.com/api/webhooks/")):
        print("❌ Invalid Discord webhook URL format!")
        print("   Expected: https://discord.com/api/webhooks/[id]/[token]")
        print("   Or: https://discordapp.com/api/webhooks/[id]/[token]")
        return False
    
    print(f"✅ Webhook URL validated: {webhook_url[:50]}...")
    
    # Show preview of what will be posted
    print("\n📢 PREVIEW OF DISCORD MESSAGE:")
    print("="*40)
    print(announcement_content[:500] + "..." if len(announcement_content) > 500 else announcement_content)
    print("="*40)
    
    # Confirm before posting
    confirm = input("\n🚨 Type 'POST' to send this announcement to Discord: ")
    if confirm != "POST":
        print("❌ Discord posting cancelled")
        return False
    
    # Post to Discord
    print("\n📡 POSTING TO DISCORD...")
    success = post_to_discord_webhook(webhook_url, announcement_content)
    
    if success:
        print("\n🎉 CAPTAIN'S ANNOUNCEMENT SUCCESSFULLY POSTED TO DISCORD!")
        print("📢 The project chronicle has been officially announced!")
        print("🚨 Project naming discussion is now open!")
        print("🎖️  Captain Agent-1 has completed the mission!")
        
        # Save success log
        success_log = Path("logs/discord_posting_success.md")
        success_log.parent.mkdir(exist_ok=True)
        
        with open(success_log, 'w', encoding='utf-8') as f:
            f.write(f"# Discord Posting Success Log\n\n")
            f.write(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Status**: SUCCESS\n")
            f.write(f"**Webhook**: {webhook_url[:50]}...\n")
            f.write(f"**Message**: Captain's announcement posted\n")
            f.write(f"**Characters**: {len(announcement_content)}\n")
        
        print(f"\n✅ Success log saved to: {success_log}")
        
    else:
        print("\n❌ FAILED TO POST TO DISCORD!")
        print("💡 The announcement is still saved in logs/captain_announcement.md")
        print("   Copy and paste it manually to your Discord devlog channel")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
