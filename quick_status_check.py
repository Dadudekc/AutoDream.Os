#!/usr/bin/env python3
"""
Quick Debate Status Check
=========================

Simple status check that doesn't rely on complex XML parsing.
"""

def check_debate_file():
    """Simple file check."""
    import os

    debate_file = "swarm_debate_consolidation.xml"

    if not os.path.exists(debate_file):
        print(f"❌ Debate file not found: {debate_file}")
        return False

    # Get file size
    size = os.path.getsize(debate_file)
    print(f"📊 Debate file size: {size:,} bytes")

    # Read first few lines
    try:
        with open(debate_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            print("📋 First 10 lines:")
            for i, line in enumerate(lines, 1):
                print("2d")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Count some basic elements
    try:
        with open(debate_file, 'r', encoding='utf-8') as f:
            content = f.read()

        participant_count = content.count('<participant>')
        argument_count = content.count('<argument>')
        agent_count = content.count('Agent-')

        print(f"👥 Participants mentioned: {participant_count}")
        print(f"💬 Arguments found: {argument_count}")
        print(f"🤖 Agent references: {agent_count}")

        # Check for Agent-7 specifically
        agent7_count = content.count('Agent-7')
        print(f"🎯 Agent-7 references: {agent7_count}")

        if 'Agent-7' in content:
            print("✅ Agent-7 has participated in the debate")
        else:
            print("❌ Agent-7 has NOT participated yet")

    except Exception as e:
        print(f"❌ Error analyzing content: {e}")
        return False

    return True

if __name__ == "__main__":
    print("🐝 QUICK DEBATE STATUS CHECK")
    print("=" * 40)
    success = check_debate_file()
    if success:
        print("\n✅ Debate file analysis complete")
    else:
        print("\n❌ Debate file analysis failed")
