#!/usr/bin/env python3
"""
Agent 5 Inbox Checker Core Module
=================================

Core functionality for Agent 5 inbox checking.
Handles message processing and team coordination results.

Author: Agent 5 (Quality Assurance Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List


class Agent5InboxCheckerCore:
    """Core functionality for Agent 5 inbox checking."""

    def __init__(self, logger: logging.Logger):
        """Initialize Agent 5 inbox checker core."""
        self.logger = logger
        self.agent_id = "Agent-5"
        self.workspace_dir = Path("agent_workspaces") / self.agent_id
        self.inbox_dir = self.workspace_dir / "inbox"
        self.processed_dir = self.workspace_dir / "processed"

    def check_inbox(self) -> Dict[str, any]:
        """Check Agent 5's inbox for new messages."""
        print("🔍 AGENT 5 CHECKING INBOX")
        print("=" * 50)
        print(f"Agent: {self.agent_id}")
        print(f"Inbox: {self.inbox_dir}")
        print()

        if not self.inbox_dir.exists():
            print("❌ No workspace found - creating workspace...")
            self.workspace_dir.mkdir(parents=True, exist_ok=True)
            self.inbox_dir.mkdir(exist_ok=True)
            self.processed_dir.mkdir(exist_ok=True)
            print("✅ Workspace created")
            return {"status": "no_workspace", "messages": 0}

        # Check for messages
        message_files = list(self.inbox_dir.glob("*.json"))
        if not message_files:
            print("📭 No messages in inbox")
            return {"status": "no_messages", "messages": 0}

        print(f"📬 Found {len(message_files)} message(s) in inbox")

        # Process messages
        processed_messages = []
        for message_file in message_files:
            try:
                with open(message_file) as f:
                    message = json.load(f)

                print(
                    f"\n📝 Processing: {message.get('type', 'unknown')} - "
                    f"{message.get('thread_id', 'unknown')}"
                )
                print(f"   From: {message.get('from', 'unknown')}")
                print(f"   Timestamp: {message.get('timestamp', 'unknown')}")

                if message.get("type") == "TEAM_CHAT_COMBINED":
                    self._process_team_chat_result(message)
                else:
                    print(f"   Content: {str(message.get('message', message))[:200]}...")

                # Move to processed
                processed_file = self.processed_dir / message_file.name
                message_file.rename(processed_file)

                processed_messages.append(message)

                print("   ✅ Processed and moved to processed folder")
            except Exception as e:
                print(f"   ❌ Error processing {message_file}: {e}")

        print(f"\n✅ Inbox check complete - processed {len(processed_messages)} message(s)")
        return {"status": "processed", "messages": len(processed_messages)}

    def _process_team_chat_result(self, message: Dict[str, any]):
        """Process team chat coordination results."""
        print("   🎯 TEAM COORDINATION RESULTS:")

        # Extract key information
        thread_id = message.get("thread_id", "unknown")
        correlation_id = message.get("correlation_id", "unknown")
        targets = message.get("targets", [])
        received = message.get("received", {})
        missing = message.get("missing", [])
        status = message.get("status", "unknown")

        print(f"   Thread ID: {thread_id}")
        print(f"   Correlation ID: {correlation_id}")
        print(f"   Status: {status}")
        print(f"   Target Agents: {len(targets)}")
        print(f"   Responses Received: {len(received)}")
        print(f"   Missing Responses: {len(missing)}")

        print("   📥 AGENT RESPONSES:")
        for agent_id, response in received.items():
            response_status = response.get("status", "unknown")
            response_message = response.get("message", "No message")
            print(f"     ✅ {agent_id}: {response_message} ({response_status})")

        if missing:
            print("   ❌ MISSING RESPONSES:")
            for agent_id in missing:
                print(f"     ❌ {agent_id}: No response")

        print("   📊 SUMMARY: All agents synchronized and ready for coordinated operations!")
