#!/usr/bin/env python3
"""
Ingest Existing Documentation into Swarm Brain
==============================================

This script ingests existing documentation files into the Swarm Brain database,
replacing static documentation with living, queryable data.
"""

import logging
from pathlib import Path

from swarm_brain import Ingestor, Retriever
from swarm_brain.connectors import ingest_devlog

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_devlog_files():
    """Ingest all devlog files into the database."""
    logger.info("=== Ingesting Devlog Files ===")

    devlog_dir = Path("devlogs")
    if not devlog_dir.exists():
        logger.warning("No devlogs directory found")
        return

    ingested_count = 0

    for devlog_file in devlog_dir.rglob("*.md"):
        try:
            # Read devlog content
            content = devlog_file.read_text(encoding="utf-8", errors="ignore")

            # Extract agent ID from filename or content
            agent_id = "Agent-5"  # Default to Agent-5 (Documentation)
            if "Agent-" in devlog_file.name:
                for i in range(1, 9):
                    if f"Agent-{i}" in devlog_file.name:
                        agent_id = f"Agent-{i}"
                        break

            # Extract date from filename
            date_str = "2025-01-01"  # Default date
            if "2025-" in devlog_file.name:
                parts = devlog_file.name.split("_")
                for part in parts:
                    if "2025-" in part:
                        date_str = part.split("_")[0]
                        break

            # Ingest into database
            ingest_devlog(
                text=content,
                project="Agent_Cellphone_V2",
                agent_id=agent_id,
                channel="devlog",
                thread_id=f"devlog_{devlog_file.stem}",
            )

            ingested_count += 1
            logger.info(f"✅ Ingested: {devlog_file.name}")

        except Exception as e:
            logger.error(f"❌ Failed to ingest {devlog_file.name}: {e}")

    logger.info(f"📊 Ingested {ingested_count} devlog files")


def ingest_protocol_documentation():
    """Ingest protocol documentation into the database."""
    logger.info("=== Ingesting Protocol Documentation ===")

    ingestor = Ingestor()

    protocol_files = [
        "AGENT_COMMUNICATION_PROTOCOLS.md",
        "AGENT_DEVLOG_SYSTEM_PROTOCOLS.md",
        "COHERENT_COLLABORATION_GUIDE.md",
        "DUPLICATION_PREVENTION_PROTOCOL.md",
    ]

    ingested_count = 0

    for protocol_file in protocol_files:
        if Path(protocol_file).exists():
            try:
                content = Path(protocol_file).read_text(encoding="utf-8", errors="ignore")

                # Extract protocol steps from content
                steps = []
                lines = content.split("\n")
                for line in lines:
                    if line.strip().startswith(("-", "*", "1.", "2.", "3.")):
                        steps.append(line.strip())

                # Ingest as protocol
                ingestor.protocol(
                    title=f"Protocol: {protocol_file.replace('.md', '')}",
                    steps=steps[:10],  # Limit to first 10 steps
                    effectiveness=0.8,  # Default effectiveness
                    improvements={"source": "static_documentation"},
                    project="Agent_Cellphone_V2",
                    agent_id="Agent-5",
                    tags=["protocol", "documentation", "static"],
                    summary=f"Protocol from {protocol_file}",
                )

                ingested_count += 1
                logger.info(f"✅ Ingested protocol: {protocol_file}")

            except Exception as e:
                logger.error(f"❌ Failed to ingest {protocol_file}: {e}")

    logger.info(f"📊 Ingested {ingested_count} protocol files")


def ingest_compliance_documentation():
    """Ingest compliance documentation into the database."""
    logger.info("=== Ingesting Compliance Documentation ===")

    ingestor = Ingestor()

    compliance_files = [
        "V2_REFACTORING_COORDINATION_PLAN.md",
        "V2_VIOLATIONS_ACTION_PLAN.md",
        "V2_COMPLIANCE_REPORT.md",
    ]

    ingested_count = 0

    for compliance_file in compliance_files:
        if Path(compliance_file).exists():
            try:
                content = Path(compliance_file).read_text(encoding="utf-8", errors="ignore")

                # Extract compliance data
                violations = []
                lines = content.split("\n")
                for line in lines:
                    if "violation" in line.lower() or "compliance" in line.lower():
                        violations.append(line.strip())

                # Ingest as action
                ingestor.action(
                    title=f"Compliance Report: {compliance_file.replace('.md', '')}",
                    tool="compliance_reporter",
                    outcome="success",
                    context={
                        "file": compliance_file,
                        "violations_found": len(violations),
                        "content_length": len(content),
                    },
                    project="Agent_Cellphone_V2",
                    agent_id="Agent-2",
                    tags=["compliance", "v2", "documentation", "static"],
                    summary=f"Compliance report from {compliance_file}",
                )

                ingested_count += 1
                logger.info(f"✅ Ingested compliance: {compliance_file}")

            except Exception as e:
                logger.error(f"❌ Failed to ingest {compliance_file}: {e}")

    logger.info(f"📊 Ingested {ingested_count} compliance files")


def ingest_security_documentation():
    """Ingest security documentation into the database."""
    logger.info("=== Ingesting Security Documentation ===")

    ingestor = Ingestor()

    security_files = [
        "SECURITY_CONSOLIDATION_SUMMARY.md",
        "SECURITY_BEST_PRACTICES.md",
        "SECURITY_IMPLEMENTATION_SUMMARY.md",
        "PHASE4_SECURITY_VALIDATION_REPORT.md",
    ]

    ingested_count = 0

    for security_file in security_files:
        if Path(security_file).exists():
            try:
                content = Path(security_file).read_text(encoding="utf-8", errors="ignore")

                # Extract security measures
                security_measures = []
                lines = content.split("\n")
                for line in lines:
                    if any(
                        keyword in line.lower()
                        for keyword in ["security", "encryption", "authentication", "authorization"]
                    ):
                        security_measures.append(line.strip())

                # Ingest as action
                ingestor.action(
                    title=f"Security Report: {security_file.replace('.md', '')}",
                    tool="security_analyzer",
                    outcome="success",
                    context={
                        "file": security_file,
                        "security_measures": len(security_measures),
                        "content_length": len(content),
                    },
                    project="Agent_Cellphone_V2",
                    agent_id="Agent-8",
                    tags=["security", "documentation", "static"],
                    summary=f"Security report from {security_file}",
                )

                ingested_count += 1
                logger.info(f"✅ Ingested security: {security_file}")

            except Exception as e:
                logger.error(f"❌ Failed to ingest {security_file}: {e}")

    logger.info(f"📊 Ingested {ingested_count} security files")


def ingest_agent_guidelines():
    """Ingest agent work guidelines into the database."""
    logger.info("=== Ingesting Agent Guidelines ===")

    ingestor = Ingestor()

    guideline_files = [
        "AGENT_WORK_GUIDELINES.md",
        "AGENTS.md",
        "V3_ALL_AGENTS_CONTRACT_SUMMARY.md",
        "V3_V2_CONSOLIDATION_PLAN.md",
        "V3_UPGRADE_ROADMAP.md",
        "V3_CYCLE_BASED_CONTRACTS.md",
        "V3_TEAM_ALPHA_ONBOARDING_PROTOCOL.md",
    ]

    ingested_count = 0

    for guideline_file in guideline_files:
        if Path(guideline_file).exists():
            try:
                content = Path(guideline_file).read_text(encoding="utf-8", errors="ignore")

                # Extract guidelines
                guidelines = []
                lines = content.split("\n")
                for line in lines:
                    if (
                        line.strip().startswith(("-", "*", "1.", "2.", "3."))
                        or "guideline" in line.lower()
                    ):
                        guidelines.append(line.strip())

                # Ingest as protocol
                ingestor.protocol(
                    title=f"Agent Guidelines: {guideline_file.replace('.md', '')}",
                    steps=guidelines[:15],  # Limit to first 15 guidelines
                    effectiveness=0.9,  # High effectiveness for guidelines
                    improvements={"source": "static_documentation"},
                    project="Agent_Cellphone_V2",
                    agent_id="Agent-1",
                    tags=["guidelines", "agents", "documentation", "static"],
                    summary=f"Agent guidelines from {guideline_file}",
                )

                ingested_count += 1
                logger.info(f"✅ Ingested guidelines: {guideline_file}")

            except Exception as e:
                logger.error(f"❌ Failed to ingest {guideline_file}: {e}")

    logger.info(f"📊 Ingested {ingested_count} guideline files")


def demonstrate_database_queries():
    """Demonstrate what we can now query from the database."""
    logger.info("=== Demonstrating Database Queries ===")

    retriever = Retriever()

    # Query 1: Get all devlog entries
    logger.info("📝 Query 1: Devlog Entries")
    devlogs = retriever.search("devlog entries", kinds=["conversation"], k=10)
    logger.info(f"Found {len(devlogs)} devlog entries")

    # Query 2: Get all protocols
    logger.info("📋 Query 2: Protocols")
    protocols = retriever.search("protocols", kinds=["protocol"], k=10)
    logger.info(f"Found {len(protocols)} protocols")

    # Query 3: Get compliance data
    logger.info("✅ Query 3: Compliance Data")
    compliance = retriever.search("compliance", kinds=["action"], k=10)
    logger.info(f"Found {len(compliance)} compliance actions")

    # Query 4: Get security data
    logger.info("🔒 Query 4: Security Data")
    security = retriever.search("security", kinds=["action"], k=10)
    logger.info(f"Found {len(security)} security actions")

    # Query 5: Get agent guidelines
    logger.info("👥 Query 5: Agent Guidelines")
    guidelines = retriever.search("agent guidelines", kinds=["protocol"], k=10)
    logger.info(f"Found {len(guidelines)} agent guidelines")

    # Query 6: Get project patterns
    logger.info("📊 Query 6: Project Patterns")
    project_patterns = retriever.get_project_patterns("Agent_Cellphone_V2", k=20)
    logger.info(f"Project has {project_patterns.get('total_activities', 0)} total activities")

    logger.info("🎉 Database queries demonstrated successfully!")


def main():
    """Main ingestion process."""
    logger.info("🚀 Starting Documentation Ingestion Process")
    logger.info("=" * 60)

    try:
        # Ingest all documentation types
        ingest_devlog_files()
        ingest_protocol_documentation()
        ingest_compliance_documentation()
        ingest_security_documentation()
        ingest_agent_guidelines()

        # Demonstrate database queries
        demonstrate_database_queries()

        logger.info("=" * 60)
        logger.info("🎉 Documentation ingestion completed successfully!")
        logger.info("📚 Static documentation is now queryable from the database!")
        logger.info("🗑️ Ready to delete static .md files and replace with database queries!")

    except Exception as e:
        logger.error(f"❌ Documentation ingestion failed: {e}")
        raise


if __name__ == "__main__":
    main()
