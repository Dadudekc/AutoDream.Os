#!/usr/bin/env python3
"""
Debate Coordination Update
==========================

Check current debate status and coordinate remaining agent contributions.
"""

def check_debate_status():
    """Check current debate participation status."""
    debate_file = "swarm_debate_consolidation.xml"

    if not os.path.exists(debate_file):
        print("❌ Debate file not found")
        return

    try:
        with open(debate_file, encoding='utf-8') as f:
            content = f.read()

        # Count arguments by author
        authors = []
        lines = content.split('\n')
        for line in lines:
            if '<ns0:author_agent>' in line:
                author = line.strip().replace('<ns0:author_agent>', '').replace('</ns0:author_agent>', '').strip()
                if author.startswith('Agent-'):
                    authors.append(author)

        # Count contributions per agent
        from collections import Counter
        author_counts = Counter(authors)

        print("🐝 SWARM DEBATE COORDINATION UPDATE")
        print("=" * 50)
        print(f"📊 Total Arguments Submitted: {len(authors)}")
        print(f"🤖 Unique Contributors: {len(author_counts)}")
        print()

        print("📋 AGENT CONTRIBUTION STATUS:")
        for agent in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']:
            count = author_counts.get(agent, 0)
            status = "✅ ACTIVE" if count >= 2 else "⏳ MODERATE" if count >= 1 else "❌ LOW"
            print(f"   {status} {agent}: {count} contributions")

        # Identify agents needing attention
        low_contributors = [agent for agent, count in author_counts.items() if count < 2]
        missing_contributors = [agent for agent in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8'] if agent not in author_counts]

        print()
        print("🚨 COORDINATION PRIORITIES:")
        if low_contributors:
            print(f"   📝 Low contributors needing follow-up: {', '.join(low_contributors)}")
        if missing_contributors:
            print(f"   🚨 Missing contributors: {', '.join(missing_contributors)}")

        # Calculate progress
        total_agents = 8
        active_agents = len([a for a, c in author_counts.items() if c >= 2])
        moderate_agents = len([a for a, c in author_counts.items() if c == 1])
        low_agents = len([a for a, c in author_counts.items() if c < 1])

        print()
        print("📈 PROGRESS METRICS:")
        print("   🎯 Target: 2+ contributions per agent")
        print(f"   ✅ Active (2+): {active_agents}/{total_agents} agents")
        print(f"   ⏳ Moderate (1): {moderate_agents}/{total_agents} agents")
        print(f"   ❌ Low (0): {low_agents}/{total_agents} agents")
        print(f"   📊 Overall Progress: {len(authors)}/{total_agents*2} target contributions")

        print()
        print("🎯 NEXT COORDINATION STEPS:")
        print("   1. Send urgent notifications to low contributors")
        print("   2. Monitor new contributions in XML file")
        print("   3. Schedule follow-up notifications if needed")
        print("   4. Prepare for debate conclusion phase")

        return author_counts

    except Exception as e:
        print(f"❌ Error analyzing debate: {e}")
        return {}

if __name__ == "__main__":
    import os
    status = check_debate_status()
