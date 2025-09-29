#!/usr/bin/env python3
"""
Demonstrate Database Queries
============================

This script demonstrates what we can now query from the database
instead of reading static documentation files.
"""

import logging

from swarm_brain import Retriever

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demonstrate_devlog_queries():
    """Demonstrate devlog queries."""
    logger.info("=== DEVLOG QUERIES ===")

    retriever = Retriever()

    # Get all devlog entries
    devlogs = retriever.search("devlog entries", kinds=["conversation"], k=20)
    logger.info(f"📝 Found {len(devlogs)} devlog entries")

    # Get devlogs by agent
    agent_devlogs = {}
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        logs = retriever.search("", kinds=["conversation"], agent_id=agent_id, k=10)
        if logs:
            agent_devlogs[agent_id] = len(logs)
            logger.info(f"  {agent_id}: {len(logs)} devlog entries")

    # Get recent devlogs
    recent_devlogs = retriever.search("recent devlog entries", kinds=["conversation"], k=5)
    logger.info(f"📅 Recent devlogs: {len(recent_devlogs)} entries")

    return devlogs


def demonstrate_protocol_queries():
    """Demonstrate protocol queries."""
    logger.info("=== PROTOCOL QUERIES ===")

    retriever = Retriever()

    # Get all protocols
    protocols = retriever.search("protocols", kinds=["protocol"], k=20)
    logger.info(f"📋 Found {len(protocols)} protocols")

    # Get communication protocols
    comm_protocols = retriever.search("communication protocols", kinds=["protocol"], k=10)
    logger.info(f"💬 Communication protocols: {len(comm_protocols)}")

    # Get agent guidelines
    guidelines = retriever.search("agent guidelines", kinds=["protocol"], k=10)
    logger.info(f"👥 Agent guidelines: {len(guidelines)}")

    return protocols


def demonstrate_compliance_queries():
    """Demonstrate compliance queries."""
    logger.info("=== COMPLIANCE QUERIES ===")

    retriever = Retriever()

    # Get compliance actions
    compliance_actions = retriever.search("compliance", kinds=["action"], k=20)
    logger.info(f"✅ Found {len(compliance_actions)} compliance actions")

    # Get V2 compliance specifically
    v2_compliance = retriever.search("V2 compliance", kinds=["action"], k=10)
    logger.info(f"📏 V2 compliance actions: {len(v2_compliance)}")

    # Get refactoring patterns
    refactoring = retriever.search("refactoring patterns", kinds=["protocol", "action"], k=10)
    logger.info(f"🔧 Refactoring patterns: {len(refactoring)}")

    return compliance_actions


def demonstrate_security_queries():
    """Demonstrate security queries."""
    logger.info("=== SECURITY QUERIES ===")

    retriever = Retriever()

    # Get security actions
    security_actions = retriever.search("security", kinds=["action"], k=20)
    logger.info(f"🔒 Found {len(security_actions)} security actions")

    # Get security protocols
    security_protocols = retriever.search("security protocols", kinds=["protocol"], k=10)
    logger.info(f"🛡️ Security protocols: {len(security_protocols)}")

    # Get security implementations
    security_impl = retriever.search("security implementation", kinds=["action"], k=10)
    logger.info(f"⚙️ Security implementations: {len(security_impl)}")

    return security_actions


def demonstrate_agent_expertise():
    """Demonstrate agent expertise queries."""
    logger.info("=== AGENT EXPERTISE QUERIES ===")

    retriever = Retriever()

    # Get expertise for each agent
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        expertise = retriever.get_agent_expertise(agent_id, k=20)
        total_patterns = expertise.get("total_patterns", 0)
        logger.info(f"🧠 {agent_id}: {total_patterns} patterns")

        # Show tool expertise
        tool_expertise = expertise.get("tool_expertise", {})
        if tool_expertise:
            for tool, stats in tool_expertise.items():
                logger.info(
                    f"    {tool}: {stats.get('count', 0)} uses, {stats.get('success_rate', 0):.1%} success"
                )


def demonstrate_project_patterns():
    """Demonstrate project pattern queries."""
    logger.info("=== PROJECT PATTERN QUERIES ===")

    retriever = Retriever()

    # Get project patterns
    project_patterns = retriever.get_project_patterns("Agent_Cellphone_V2", k=50)

    total_activities = project_patterns.get("total_activities", 0)
    document_types = project_patterns.get("document_types", {})
    agent_participation = project_patterns.get("agent_participation", {})

    logger.info(f"📊 Project has {total_activities} total activities")
    logger.info(f"📄 Document types: {document_types}")
    logger.info(f"👥 Agent participation: {agent_participation}")

    return project_patterns


def demonstrate_semantic_search():
    """Demonstrate semantic search capabilities."""
    logger.info("=== SEMANTIC SEARCH DEMONSTRATIONS ===")

    retriever = Retriever()

    # Search queries
    search_queries = [
        "Discord commander test results",
        "V2 compliance violations",
        "agent coordination patterns",
        "security implementations",
        "devlog system updates",
        "quality assurance framework",
        "project scanner results",
        "performance monitoring",
    ]

    for query in search_queries:
        results = retriever.search(query, k=5)
        logger.info(f"🔍 '{query}': {len(results)} results")

        # Show top result
        if results:
            top_result = results[0]
            title = top_result.get("title", "No title")
            agent_id = top_result.get("agent_id", "Unknown")
            logger.info(f"    Top: {title} by {agent_id}")


def demonstrate_how_do_agents_do():
    """Demonstrate 'how do agents do' queries."""
    logger.info("=== HOW DO AGENTS DO QUERIES ===")

    retriever = Retriever()

    # Example queries
    queries = [
        "V2 compliance refactoring",
        "Discord coordination",
        "devlog posting",
        "security validation",
        "project scanning",
        "quality assurance",
    ]

    for query in queries:
        patterns = retriever.how_do_agents_do(query, k=5)
        logger.info(f"🎯 How do agents do '{query}': {len(patterns)} patterns")

        # Show successful patterns
        successful = [p for p in patterns if p.get("outcome") == "success"]
        if successful:
            logger.info(f"    ✅ {len(successful)} successful patterns")


def main():
    """Main demonstration."""
    logger.info("🚀 Swarm Brain Database Query Demonstrations")
    logger.info("=" * 60)

    try:
        # Run all demonstrations
        demonstrate_devlog_queries()
        demonstrate_protocol_queries()
        demonstrate_compliance_queries()
        demonstrate_security_queries()
        demonstrate_agent_expertise()
        demonstrate_project_patterns()
        demonstrate_semantic_search()
        demonstrate_how_do_agents_do()

        logger.info("=" * 60)
        logger.info("🎉 All database queries demonstrated successfully!")
        logger.info("📚 Static documentation is now fully replaceable with database queries!")
        logger.info("🗑️ Ready to delete static .md files!")

    except Exception as e:
        logger.error(f"❌ Query demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()
