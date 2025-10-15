#!/usr/bin/env python3
"""
Discord Contract Notifications
Real-time contract event notifications for Captain monitoring.

Author: Agent-7
Date: 2025-10-15
Mission: Week 1 Quick Win - Discord Contract Notifications
"""

import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class ContractNotifier:
    """Sends contract event notifications to Discord."""
    
    def __init__(self):
        """Initialize contract notifier with webhook."""
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            print("⚠️ WARNING: DISCORD_WEBHOOK_URL not configured")
    
    def notify_contract_assigned(
        self, 
        contract_id: str, 
        agent_id: str, 
        contract_name: str,
        priority: str,
        estimated_hours: int
    ) -> bool:
        """Notify when contract is assigned to agent."""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": f"📋 Contract Assigned: {contract_id}",
            "description": f"**{contract_name}**",
            "color": 0x3498DB,  # Blue
            "fields": [
                {"name": "👤 Agent", "value": agent_id, "inline": True},
                {"name": "⚡ Priority", "value": priority.upper(), "inline": True},
                {"name": "⏱️ Est. Hours", "value": str(estimated_hours), "inline": True},
                {"name": "📅 Assigned", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": False},
            ],
            "footer": {"text": "Contract System - Assignment"}
        }
        
        payload = {
            "embeds": [embed],
            "username": "Contract Monitor"
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Error posting assignment notification: {e}")
            return False
    
    def notify_contract_started(
        self,
        contract_id: str,
        agent_id: str,
        contract_name: str
    ) -> bool:
        """Notify when agent starts work on contract."""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": f"🚀 Contract Started: {contract_id}",
            "description": f"**{agent_id}** began work on **{contract_name}**",
            "color": 0xF39C12,  # Orange
            "fields": [
                {"name": "👤 Agent", "value": agent_id, "inline": True},
                {"name": "⏰ Started", "value": datetime.now().strftime("%H:%M"), "inline": True},
            ],
            "footer": {"text": "Contract System - Execution"}
        }
        
        payload = {
            "embeds": [embed],
            "username": "Contract Monitor"
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Error posting start notification: {e}")
            return False
    
    def notify_contract_completed(
        self,
        contract_id: str,
        agent_id: str,
        contract_name: str,
        points_earned: int,
        actual_hours: float
    ) -> bool:
        """Notify when contract is completed."""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": f"✅ Contract Complete: {contract_id}",
            "description": f"**{agent_id}** completed **{contract_name}**!",
            "color": 0x2ECC71,  # Green
            "fields": [
                {"name": "👤 Agent", "value": agent_id, "inline": True},
                {"name": "🏆 Points", "value": f"+{points_earned} pts", "inline": True},
                {"name": "⏱️ Time", "value": f"{actual_hours:.1f}h", "inline": True},
                {"name": "✅ Completed", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": False},
            ],
            "footer": {"text": "Contract System - Success"}
        }
        
        payload = {
            "embeds": [embed],
            "username": "Contract Monitor"
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Error posting completion notification: {e}")
            return False
    
    def notify_contract_blocked(
        self,
        contract_id: str,
        agent_id: str,
        contract_name: str,
        blocker: str
    ) -> bool:
        """Notify when contract is blocked."""
        
        if not self.webhook_url:
            return False
        
        embed = {
            "title": f"⚠️ Contract Blocked: {contract_id}",
            "description": f"**{agent_id}** blocked on **{contract_name}**",
            "color": 0xE74C3C,  # Red
            "fields": [
                {"name": "👤 Agent", "value": agent_id, "inline": True},
                {"name": "🚧 Blocker", "value": blocker, "inline": False},
                {"name": "⏰ Blocked", "value": datetime.now().strftime("%H:%M"), "inline": True},
            ],
            "footer": {"text": "Contract System - Alert"}
        }
        
        payload = {
            "embeds": [embed],
            "username": "Contract Monitor"
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Error posting blocked notification: {e}")
            return False


# Quick test function
def test_notifications():
    """Test contract notifications."""
    notifier = ContractNotifier()
    
    print("🧪 Testing Contract Notifications...\n")
    
    # Test 1: Assignment
    print("Test 1: Contract Assignment")
    result1 = notifier.notify_contract_assigned(
        contract_id="C-TEST-001",
        agent_id="Agent-7",
        contract_name="Discord Contract Notifications",
        priority="HIGH",
        estimated_hours=25
    )
    print(f"   {'✅ PASS' if result1 else '❌ FAIL'}\n")
    
    # Test 2: Started
    print("Test 2: Contract Started")
    result2 = notifier.notify_contract_started(
        contract_id="C-TEST-001",
        agent_id="Agent-7",
        contract_name="Discord Contract Notifications"
    )
    print(f"   {'✅ PASS' if result2 else '❌ FAIL'}\n")
    
    # Test 3: Completed
    print("Test 3: Contract Completed")
    result3 = notifier.notify_contract_completed(
        contract_id="C-TEST-001",
        agent_id="Agent-7",
        contract_name="Discord Contract Notifications",
        points_earned=500,
        actual_hours=22.5
    )
    print(f"   {'✅ PASS' if result3 else '❌ FAIL'}\n")
    
    # Test 4: Blocked
    print("Test 4: Contract Blocked")
    result4 = notifier.notify_contract_blocked(
        contract_id="C-TEST-001",
        agent_id="Agent-7",
        contract_name="Discord Contract Notifications",
        blocker="Waiting for webhook URL configuration"
    )
    print(f"   {'✅ PASS' if result4 else '❌ FAIL'}\n")
    
    all_pass = all([result1, result2, result3, result4])
    print("=" * 60)
    print(f"{'✅ ALL TESTS PASSED!' if all_pass else '⚠️ SOME TESTS FAILED'}")
    print("=" * 60)


if __name__ == "__main__":
    test_notifications()

