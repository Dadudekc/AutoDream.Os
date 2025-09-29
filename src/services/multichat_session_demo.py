#!/usr/bin/env python3
"""
Multichat Session Persistence Demo
=================================

Demonstration of V2-compliant multichat session persistence
Shows how to maintain chat sessions across Python processes
V2 Compliant: ≤200 lines, focused demo application
"""

import time
import uuid
from datetime import datetime

from multichat_session_persistence import ChatMessage, SessionPersistence


class MultichatSessionDemo:
    """V2-compliant multichat session demo"""

    def __init__(self):
        self.persistence = SessionPersistence(storage_type="json", storage_path="demo_sessions")
        self.session_id = str(uuid.uuid4())

    def create_demo_session(self):
        """Create demo chat session"""
        print("🚀 Creating demo multichat session...")

        # Create session with multiple agents
        session = self.persistence.create_session(
            session_id=self.session_id, participants=["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        )

        print(f"✅ Session created: {session.session_id}")
        print(f"👥 Participants: {', '.join(session.participants)}")
        return session

    def simulate_chat_messages(self):
        """Simulate chat messages between agents"""
        print("\n💬 Simulating chat messages...")

        # Agent-1 starts conversation
        self.add_message("Agent-1", "Agent-2", "Hello Agent-2! Ready for coordination?")
        time.sleep(0.5)

        # Agent-2 responds
        self.add_message("Agent-2", "Agent-1", "Yes! I'm ready. What's the task?")
        time.sleep(0.5)

        # Agent-1 provides task details
        self.add_message("Agent-1", "Agent-2", "We need to implement V2 compliance refactoring.")
        time.sleep(0.5)

        # Agent-3 joins
        self.add_message("Agent-3", "Agent-1", "I can help with the refactoring strategy!")
        time.sleep(0.5)

        # Agent-4 coordinates
        self.add_message("Agent-4", "All", "I'll coordinate the refactoring process.")
        time.sleep(0.5)

        # Agent-2 confirms
        self.add_message("Agent-2", "Agent-4", "Perfect! Let's start with critical files.")

        print("✅ Chat simulation complete!")

    def add_message(self, sender: str, recipient: str, content: str):
        """Add message to session"""
        message = ChatMessage(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            content=content,
            timestamp=time.time(),
            session_id=self.session_id,
        )

        self.persistence.add_message(message)
        timestamp = datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S")
        print(f"[{timestamp}] {sender} → {recipient}: {content}")

    def demonstrate_persistence(self):
        """Demonstrate session persistence across processes"""
        print("\n🔄 Demonstrating session persistence...")

        # Save current session
        session = self.persistence.get_session(self.session_id)
        if session:
            print("📊 Session Status:")
            print(f"   • Session ID: {session.session_id}")
            print(f"   • Participants: {len(session.participants)}")
            print(f"   • Messages: {session.message_count}")
            print(f"   • Last Activity: {datetime.fromtimestamp(session.last_activity)}")

        # Retrieve messages
        messages = self.persistence.get_messages(self.session_id, limit=10)
        print(f"\n📝 Recent Messages ({len(messages)}):")
        for msg in messages:
            timestamp = datetime.fromtimestamp(msg.timestamp).strftime("%H:%M:%S")
            print(f"   [{timestamp}] {msg.sender} → {msg.recipient}: {msg.content}")

    def demonstrate_storage_options(self):
        """Demonstrate different storage options"""
        print("\n💾 Storage Options Demo:")

        # JSON Storage
        print("1. JSON Storage (Default)")
        json_persistence = SessionPersistence(storage_type="json", storage_path="json_sessions")
        json_session = json_persistence.create_session("json-demo", ["Agent-1", "Agent-2"])
        print(f"   ✅ JSON session created: {json_session.session_id}")

        # SQLite Storage
        print("2. SQLite Storage")
        sqlite_persistence = SessionPersistence(
            storage_type="sqlite", storage_path="sqlite_sessions"
        )
        sqlite_session = sqlite_persistence.create_session("sqlite-demo", ["Agent-1", "Agent-2"])
        print(f"   ✅ SQLite session created: {sqlite_session.session_id}")

        # Memory Storage
        print("3. Memory Storage")
        memory_persistence = SessionPersistence(storage_type="memory")
        memory_session = memory_persistence.create_session("memory-demo", ["Agent-1", "Agent-2"])
        print(f"   ✅ Memory session created: {memory_session.session_id}")

        # Cleanup
        json_persistence.close()
        sqlite_persistence.close()

    def demonstrate_cleanup(self):
        """Demonstrate session cleanup"""
        print("\n🧹 Session Cleanup Demo:")

        # Create old session
        old_session = self.persistence.create_session("old-session", ["Agent-1"])
        old_message = ChatMessage(
            id=str(uuid.uuid4()),
            sender="Agent-1",
            recipient="Agent-2",
            content="This is an old message",
            timestamp=time.time() - (35 * 24 * 60 * 60),  # 35 days ago
            session_id="old-session",
        )
        self.persistence.add_message(old_message)

        print(f"   📅 Created old session: {old_session.session_id}")

        # Cleanup sessions older than 30 days
        self.persistence.cleanup_old_sessions(days=30)
        print("   🗑️ Cleaned up sessions older than 30 days")

        # Verify cleanup
        cleaned_session = self.persistence.get_session("old-session")
        if cleaned_session is None:
            print("   ✅ Old session successfully removed")
        else:
            print("   ⚠️ Old session still exists")

    def run_demo(self):
        """Run complete demo"""
        print("🚀 Multichat Session Persistence Demo")
        print("=" * 50)

        try:
            # Create demo session
            self.create_demo_session()

            # Simulate chat
            self.simulate_chat_messages()

            # Demonstrate persistence
            self.demonstrate_persistence()

            # Show storage options
            self.demonstrate_storage_options()

            # Demonstrate cleanup
            self.demonstrate_cleanup()

            print("\n✅ Demo completed successfully!")
            print("\n📋 Usage Instructions:")
            print("1. Import SessionPersistence from multichat_session_persistence")
            print("2. Create persistence instance with desired storage type")
            print("3. Create sessions and add messages")
            print("4. Retrieve sessions and messages across process restarts")
            print("5. Use cleanup_old_sessions() for maintenance")

        except Exception as e:
            print(f"❌ Demo failed: {e}")
        finally:
            self.persistence.close()


def main():
    """Main demo function"""
    demo = MultichatSessionDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
