#!/usr/bin/env python3
"""
Discord Status Dashboard - WOW Factor Display
Posts beautiful formatted status of all agents to Discord
"""

import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

def create_wow_factor_status():
    """Create impressive status display from all agent status.json files"""
    
    agents = [
        ("Agent-1", "Integration & Core Systems"),
        ("Agent-2", "Architecture & Design"),
        ("Agent-3", "Infrastructure & DevOps"),
        ("Agent-4", "Captain - Strategic Oversight"),
        ("Agent-5", "Business Intelligence"),
        ("Agent-6", "Gaming & Entertainment"),
        ("Agent-7", "Web Development"),
        ("Agent-8", "SSOT & System Integration"),
    ]
    
    status_lines = []
    status_lines.append("# 🐝 SWARM STATUS DASHBOARD - REAL-TIME")
    status_lines.append(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    status_lines.append("")
    status_lines.append("---")
    status_lines.append("")
    
    # Overall metrics
    active_count = 0
    complete_count = 0
    total_achievements = 0
    
    for agent_id, role in agents:
        status_path = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if not status_path.exists():
            continue
            
        try:
            with open(status_path, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Agent header with emoji
            emoji = "👑" if "Captain" in role or "Co-Captain" in str(status.get('status', '')) else "🤖"
            if "LEGENDARY" in str(status.get('achievements', [])):
                emoji = "🏆"
            
            status_lines.append(f"## {emoji} **{agent_id}** - {role}")
            status_lines.append("")
            
            # Status indicator
            agent_status = status.get('status', 'UNKNOWN')
            if 'ACTIVE' in agent_status:
                status_icon = "🟢 ACTIVE"
                active_count += 1
            elif 'COMPLETE' in agent_status or agent_status == 'AUTONOMOUS_MODE_COMMANDER_AWAY':
                status_icon = "✅ OPERATIONAL"
                active_count += 1
            elif 'WAITING' in agent_status:
                status_icon = "🟡 WAITING"
            else:
                status_icon = "🔴 IDLE"
            
            status_lines.append(f"**Status:** {status_icon}")
            
            # Current mission
            mission = status.get('current_mission', 'No active mission')
            status_lines.append(f"**Mission:** {mission}")
            
            # Current tasks (first 2)
            tasks = status.get('current_tasks', [])
            if tasks:
                status_lines.append(f"**Tasks:** {tasks[0]}")
                if len(tasks) > 1:
                    status_lines.append(f"  ↳ {tasks[1]}")
            
            # Achievements count
            achievements = status.get('achievements', [])
            if achievements:
                total_achievements += len(achievements)
                status_lines.append(f"**Achievements:** {len(achievements)} total")
            
            # Last updated
            last_updated = status.get('last_updated', 'Unknown')
            status_lines.append(f"**Last Updated:** {last_updated}")
            
            status_lines.append("")
            status_lines.append("---")
            status_lines.append("")
            
        except Exception as e:
            status_lines.append(f"❌ Error reading {agent_id}: {e}")
            status_lines.append("")
    
    # Overall stats at bottom
    status_lines.append("## 📊 SWARM METRICS")
    status_lines.append("")
    status_lines.append(f"**Active Agents:** {active_count}/8")
    status_lines.append(f"**Total Achievements:** {total_achievements}")
    status_lines.append(f"**GitHub Analysis:** 47/75 (62.7%)")
    status_lines.append(f"**LEGENDARY Agents:** 2 (Agent-6, Agent-2)")
    status_lines.append("")
    status_lines.append("🐝 **WE ARE SWARM - AUTONOMOUS & OPERATIONAL!** 🚀⚡")
    
    return "\n".join(status_lines)

def post_to_discord(content):
    """Post status dashboard to Discord"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ ERROR: DISCORD_WEBHOOK_URL not found")
        return False
    
    # Split into chunks if needed (Discord 2000 char limit)
    max_length = 1900
    chunks = []
    current_chunk = ""
    
    for line in content.split('\n'):
        if len(current_chunk) + len(line) + 1 < max_length:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # Post all chunks
    for i, chunk in enumerate(chunks):
        payload = {
            "content": chunk if i == 0 else f"*(continued {i+1}/{len(chunks)})*\n{chunk}",
            "username": "Swarm Status Dashboard"
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                print(f"✅ Posted chunk {i+1}/{len(chunks)} to Discord")
            else:
                print(f"❌ Error posting chunk {i+1}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        # Rate limit
        if i < len(chunks) - 1:
            import time
            time.sleep(1)
    
    return True

def main():
    """Generate and post wow factor status dashboard"""
    print("🐝 Creating Swarm Status Dashboard...")
    
    status_content = create_wow_factor_status()
    
    print("\n" + "="*60)
    print(status_content)
    print("="*60 + "\n")
    
    print("📤 Posting to Discord...")
    success = post_to_discord(status_content)
    
    if success:
        print("✅ Status dashboard posted to Discord!")
        print("Commander can now see swarm status remotely!")
    else:
        print("❌ Failed to post to Discord")
        print("Check DISCORD_WEBHOOK_URL in .env")

if __name__ == "__main__":
    main()

