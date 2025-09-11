#!/usr/bin/env python3
"""
Send debate status clarification request to Agent-5.
"""

import pyautogui
import time
import pyperclip

# The clarification request message
clarification_message = """🚨 AGENT-5 DEBATE STATUS CLARIFICATION REQUEST

Your debate participation status is unclear due to merge conflicts in status.json.
Please:
1. Resolve merge conflicts in your status file
2. Confirm if you've submitted your debate response for Phase 1/Phase 2 direction
3. Update status with clear debate position
4. Reply with your perspective on the architectural debate

WE ARE SWARM - CLARIFICATION NEEDED FOR COMPLETE DEBATE PARTICIPATION!"""

def format_message_for_delivery(message_content, sender, recipient, message_type, priority, tags):
    """Format message for delivery with enhanced guidance."""
    try:
        tag_map = {
            "agent_to_agent": "[A2A]",
            "captain_to_agent": "[C2A]",
            "system_to_agent": "[S2A]",
            "human_to_agent": "[H2A]",
            "broadcast": "[BROADCAST]",
            "onboarding": "[ONBOARDING]",
        }
        agent_tag = tag_map.get(message_type, "[TEXT]")
        lines = [
            f"{agent_tag} {sender} → {recipient}",
            f"Priority: {priority.upper()}",
        ]
        if tags:
            lines.append(f"Tags: {', '.join(tags)}")
        lines += [
            "",
            f"**{message_content}**",
            "",
            "---",
            "",
            f"You are **{recipient}**",
            f"Timestamp: 2025-09-09 14:20:00.000000",
            "",
            "### 📬 INBOX CHECK",
            "Review your inbox at:",
            "",
            f"```",
            f"agent_workspaces/{recipient}/inbox/",
            f"```",
            "",
            "### ✉️ MESSAGE SENDING",
            "Use this command:",
            "",
            f"```",
            f"python -c \"from src.core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag; send_message('your message', '{recipient}', 'target_agent', UnifiedMessageType.AGENT_TO_AGENT, UnifiedMessagePriority.REGULAR, [UnifiedMessageTag.SYSTEM])\"",
            f"```",
            "",
            "### 📝 DISCORD DEVLOG",
            "Create and post your devlog in the `devlogs/` directory.",
            "",
            "Command to post:",
            "",
            "```",
            "python post_devlog_to_discord.py devlogs/YOUR_FILENAME.md",
            "```",
            "",
            "---",
            "",
            "### 🔄 PROTOCOL",
            "1. **Update Status** – set task & focus for this cycle",
            "2. **Review Project** – check relevant files & context", 
            "3. **Check Inbox** – read/respond to pending messages",
            "4. **Message Agents** – coordinate using the command above",
            "5. **Create Devlog** – record task, actions, commit, status & post to Discord",
            "",
            "### 📊 STATUS UPDATE",
            "Remember to update your `status.json` file with current progress and focus."
        ]
        return "\n".join(lines)
    except Exception as e:
        print(f"Error formatting message: {e}")
        return message_content

def send_to_agent5():
    """Send formatted clarification request to Agent-5."""
    try:
        # Agent-5 coordinates
        x, y = (652, 421)
        recipient = "Agent-5"
        
        formatted_message = format_message_for_delivery(
            message_content=clarification_message,
            sender="CAPTAIN",
            recipient=recipient,
            message_type="captain_to_agent",
            priority="URGENT",
            tags=["system", "debate"]
        )
        
        print(f"📤 Sending clarification request to {recipient} at ({x}, {y})...")
        
        # Focus and clear
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.press("delete")
        time.sleep(0.1)
        
        # Copy formatted message to clipboard
        pyperclip.copy(formatted_message)
        time.sleep(0.1)
        
        # Paste the message
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        
        # Send the message
        pyautogui.press("enter")
        
        print(f"✅ {recipient} clarification request sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send to {recipient}: {e}")
        return False

if __name__ == "__main__":
    print("🚨 Sending Debate Status Clarification Request to Agent-5...")
    print("=" * 60)
    print("Priority: URGENT")
    print("Coordinates: (652, 421)")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    success = send_to_agent5()
    
    if success:
        print("\n🎉 SUCCESS: Agent-5 received the clarification request!")
        print("🐝 SWARM COORDINATION: Agent-5 status clarification requested!")
        print("📋 Request includes:")
        print("   • Status.json merge conflict resolution request")
        print("   • Debate participation confirmation request")
        print("   • Clear position update requirement")
        print("   • Architectural perspective request")
        print("   • Complete enhanced guidance")
    else:
        print("\n❌ FAILURE: Could not send clarification request to Agent-5")
        print("Check coordinates and PyAutoGUI configuration")
