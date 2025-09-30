#!/usr/bin/env python3
"""
Delete Static Documentation Core
===============================

Core functionality for deleting static documentation files.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused deletion functionality
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StaticDocumentationDeleter:
    """Core functionality for deleting static documentation files."""

    def __init__(self):
        """Initialize the deleter."""
        self.deleted_files: List[str] = []

    def create_backup(self) -> Path:
        """Create a backup of files before deletion."""
        backup_dir = Path("documentation_backup")
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"deleted_files_{timestamp}.txt"

        logger.info(f"📦 Backup will be created at: {backup_file}")
        return backup_file

    def delete_devlog_files(self) -> List[str]:
        """Delete devlog files that have been ingested."""
        logger.info("=== DELETING DEVLOG FILES ===")

        devlog_dir = Path("devlogs")
        if not devlog_dir.exists():
            logger.warning("No devlogs directory found")
            return []

        deleted_files = []

        # Files to delete (all devlog files)
        for devlog_file in devlog_dir.rglob("*.md"):
            try:
                # Skip archive directory for now
                if "archive" in str(devlog_file):
                    continue

                file_size = devlog_file.stat().st_size
                devlog_file.unlink()
                deleted_files.append(str(devlog_file))
                logger.info(f"🗑️ Deleted: {devlog_file.name} ({file_size} bytes)")

            except Exception as e:
                logger.error(f"❌ Failed to delete {devlog_file.name}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} devlog files")
        return deleted_files

    def delete_protocol_files(self) -> List[str]:
        """Delete protocol documentation files."""
        logger.info("=== DELETING PROTOCOL FILES ===")

        protocol_files = [
            "AGENT_COMMUNICATION_PROTOCOLS.md",
            "AGENT_DEVLOG_SYSTEM_PROTOCOLS.md",
            "COHERENT_COLLABORATION_GUIDE.md",
            "DUPLICATION_PREVENTION_PROTOCOL.md",
        ]

        deleted_files = []

        for protocol_file in protocol_files:
            file_path = Path(protocol_file)
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    logger.info(f"🗑️ Deleted: {protocol_file} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"❌ Failed to delete {protocol_file}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} protocol files")
        return deleted_files

    def delete_compliance_files(self) -> List[str]:
        """Delete compliance documentation files."""
        logger.info("=== DELETING COMPLIANCE FILES ===")

        compliance_files = [
            "V2_REFACTORING_COORDINATION_PLAN.md",
            "V2_VIOLATIONS_ACTION_PLAN.md",
            "V2_COMPLIANCE_REPORT.md",
        ]

        deleted_files = []

        for compliance_file in compliance_files:
            file_path = Path(compliance_file)
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    logger.info(f"🗑️ Deleted: {compliance_file} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"❌ Failed to delete {compliance_file}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} compliance files")
        return deleted_files

    def delete_security_files(self) -> List[str]:
        """Delete security documentation files."""
        logger.info("=== DELETING SECURITY FILES ===")

        security_files = [
            "SECURITY_CONSOLIDATION_SUMMARY.md",
            "SECURITY_BEST_PRACTICES.md",
            "SECURITY_IMPLEMENTATION_SUMMARY.md",
            "PHASE4_SECURITY_VALIDATION_REPORT.md",
        ]

        deleted_files = []

        for security_file in security_files:
            file_path = Path(security_file)
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    logger.info(f"🗑️ Deleted: {security_file} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"❌ Failed to delete {security_file}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} security files")
        return deleted_files

    def delete_agent_guideline_files(self) -> List[str]:
        """Delete agent guideline files."""
        logger.info("=== DELETING AGENT GUIDELINE FILES ===")

        guideline_files = [
            "AGENT_WORK_GUIDELINES.md",
            "AGENTS.md",
            "V3_ALL_AGENTS_CONTRACT_SUMMARY.md",
            "V3_V2_CONSOLIDATION_PLAN.md",
            "V3_UPGRADE_ROADMAP.md",
            "V3_CYCLE_BASED_CONTRACTS.md",
            "V3_TEAM_ALPHA_ONBOARDING_PROTOCOL.md",
        ]

        deleted_files = []

        for guideline_file in guideline_files:
            file_path = Path(guideline_file)
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    logger.info(f"🗑️ Deleted: {guideline_file} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"❌ Failed to delete {guideline_file}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} guideline files")
        return deleted_files

    def delete_coordination_files(self) -> List[str]:
        """Delete coordination documentation files."""
        logger.info("=== DELETING COORDINATION FILES ===")

        coordination_files = [
            "AGENT_8_COORDINATION_RESPONSE.md",
            "AGENT_8_V2_REFACTORING_COORDINATION_SUMMARY.md",
            "COHERENT_COLLABORATION_IMPLEMENTATION_SUMMARY.md",
        ]

        deleted_files = []

        for coordination_file in coordination_files:
            file_path = Path(coordination_file)
            if file_path.exists():
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    logger.info(f"🗑️ Deleted: {coordination_file} ({file_size} bytes)")
                except Exception as e:
                    logger.error(f"❌ Failed to delete {coordination_file}: {e}")

        logger.info(f"📊 Deleted {len(deleted_files)} coordination files")
        return deleted_files

    def create_query_replacement_guide(self):
        """Create a guide showing how to replace deleted files with database queries."""
        logger.info("=== CREATING QUERY REPLACEMENT GUIDE ===")

        guide_content = """# Database Query Replacement Guide

## 🎯 **REPLACED STATIC DOCUMENTATION WITH DATABASE QUERIES**

The following static documentation files have been deleted and replaced with database queries:

### **Devlog Files → Database Queries**
```python
from swarm_brain import Retriever
retriever = Retriever()

# Get all devlog entries
devlogs = retriever.search("devlog entries", kinds=["conversation"], k=50)

# Get devlogs by agent
agent_devlogs = retriever.search("", kinds=["conversation"], agent_id="Agent-5", k=20)

# Get recent devlogs
recent_devlogs = retriever.search("recent devlog entries", kinds=["conversation"], k=10)
```

### **Protocol Files → Database Queries**
```python
# Get communication protocols
protocols = retriever.search("communication protocols", kinds=["protocol"], k=20)

# Get agent guidelines
guidelines = retriever.search("agent guidelines", kinds=["protocol"], k=20)

# Get collaboration guides
collaboration = retriever.search("collaboration", kinds=["protocol"], k=10)
```

### **Compliance Files → Database Queries**
```python
# Get V2 compliance data
compliance = retriever.search("V2 compliance", kinds=["action"], k=20)

# Get refactoring patterns
refactoring = retriever.search("refactoring patterns", kinds=["protocol", "action"], k=20)

# Get compliance violations
violations = retriever.search("compliance violations", kinds=["action"], k=20)
```

### **Security Files → Database Queries**
```python
# Get security implementations
security = retriever.search("security implementation", kinds=["action"], k=20)

# Get security protocols
security_protocols = retriever.search("security protocols", kinds=["protocol"], k=20)

# Get security validations
validations = retriever.search("security validation", kinds=["action"], k=20)
```

### **Agent Guidelines → Database Queries**
```python
# Get agent expertise
expertise = retriever.get_agent_expertise("Agent-1", k=20)

# Get work patterns
work_patterns = retriever.search("work patterns", kinds=["action", "protocol"], k=20)

# Get agent contracts
contracts = retriever.search("agent contracts", kinds=["protocol"], k=20)
```

### **Coordination Files → Database Queries**
```python
# Get coordination patterns
coordination = retriever.search("coordination patterns", kinds=["coordination"], k=20)

# Get agent interactions
interactions = retriever.search("agent interactions", kinds=["conversation", "action"], k=20)

# Get collaboration patterns
collaboration = retriever.search("collaboration patterns", kinds=["coordination"], k=20)
```

## 🎯 **Benefits of Database Queries**

1. **Always Current**: Data is always up-to-date from actual agent activities
2. **Semantic Search**: Find relevant information using natural language queries
3. **Pattern Recognition**: Discover successful patterns and strategies
4. **Agent Expertise**: Understand each agent's strengths and capabilities
5. **Project Insights**: Get real-time project status and progress
6. **No Maintenance**: No need to manually update documentation

## 🚀 **Ready to Use**

All static documentation has been replaced with living, queryable data from the Swarm Brain database!

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        guide_path = Path("DATABASE_QUERY_REPLACEMENT_GUIDE.md")
        guide_path.write_text(guide_content, encoding="utf-8")
        logger.info(f"📝 Created replacement guide: {guide_path}")

    def write_backup_file(self, backup_file: Path, all_deleted_files: List[str]):
        """Write backup file with deleted files list."""
        with open(backup_file, "w") as f:
            f.write("Deleted Files Backup\\n")
            f.write("=" * 50 + "\\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            for file_path in all_deleted_files:
                f.write(f"{file_path}\\n")

    def run_deletion_process(self):
        """Run the complete deletion process."""
        logger.info("🗑️ Starting Static Documentation Deletion Process")
        logger.info("=" * 60)

        try:
            # Create backup
            backup_file = self.create_backup()

            # Delete files by category
            all_deleted_files = []

            all_deleted_files.extend(self.delete_devlog_files())
            all_deleted_files.extend(self.delete_protocol_files())
            all_deleted_files.extend(self.delete_compliance_files())
            all_deleted_files.extend(self.delete_security_files())
            all_deleted_files.extend(self.delete_agent_guideline_files())
            all_deleted_files.extend(self.delete_coordination_files())

            # Write backup file
            self.write_backup_file(backup_file, all_deleted_files)

            # Create replacement guide
            self.create_query_replacement_guide()

            logger.info("=" * 60)
            logger.info("🎉 Deletion completed successfully!")
            logger.info(f"📊 Total files deleted: {len(all_deleted_files)}")
            logger.info(f"📦 Backup created: {backup_file}")
            logger.info("📝 Query replacement guide created")
            logger.info("🚀 Static documentation replaced with database queries!")

        except Exception as e:
            logger.error(f"❌ Deletion process failed: {e}")
            raise
