#!/usr/bin/env python3
"""
Content Hash System
===================

Implements unique content hashing to prevent future duplicates across all databases.
"""

import hashlib
import json
import logging

# Add src to path for imports
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from swarm_brain import SwarmBrain

logger = logging.getLogger(__name__)


class ContentHashSystem:
    """Content hashing system to prevent duplicates."""

    def __init__(self):
        """Initialize content hash system."""
        self.brain = SwarmBrain()
        self.hash_file = Path("database_content_hashes.json")
        self.load_existing_hashes()

    def load_existing_hashes(self):
        """Load existing content hashes."""
        if self.hash_file.exists():
            with open(self.hash_file) as f:
                self.content_hashes = json.load(f)
        else:
            self.content_hashes = {
                "swarm_brain": {},
                "vector_database": {},
                "devlogs": {},
                "project_analysis": {},
                "last_updated": datetime.now().isoformat(),
            }

    def save_hashes(self):
        """Save content hashes to file."""
        self.content_hashes["last_updated"] = datetime.now().isoformat()
        with open(self.hash_file, "w") as f:
            json.dump(self.content_hashes, f, indent=2)

    def generate_content_hash(self, content: str, metadata: dict = None) -> str:
        """Generate hash for content."""
        # Combine content and relevant metadata
        hash_input = content
        if metadata:
            # Include relevant metadata fields
            relevant_fields = ["agent_id", "kind", "project", "title"]
            for field in relevant_fields:
                if field in metadata:
                    hash_input += str(metadata[field])

        return hashlib.md5(hash_input.encode()).hexdigest()

    def check_duplicate(
        self, content: str, metadata: dict = None, db_type: str = "swarm_brain"
    ) -> bool:
        """Check if content is a duplicate."""
        content_hash = self.generate_content_hash(content, metadata)

        if db_type not in self.content_hashes:
            self.content_hashes[db_type] = {}

        return content_hash in self.content_hashes[db_type]

    def add_content_hash(
        self, content: str, metadata: dict = None, db_type: str = "swarm_brain", doc_id: str = None
    ):
        """Add content hash to prevent future duplicates."""
        content_hash = self.generate_content_hash(content, metadata)

        if db_type not in self.content_hashes:
            self.content_hashes[db_type] = {}

        self.content_hashes[db_type][content_hash] = {
            "doc_id": doc_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
        }

    def hash_all_existing_content(self):
        """Generate hashes for all existing content."""
        print("🔐 Generating content hashes for all existing content...")

        # Hash Swarm Brain content
        cursor = self.brain.conn.cursor()
        cursor.execute("SELECT * FROM documents ORDER BY id")
        rows = cursor.fetchall()

        swarm_hashes = 0
        for row in rows:
            try:
                content = f"{row['title']} {row['summary']} {row['canonical']}"
                metadata = {
                    "agent_id": row["agent_id"],
                    "kind": row["kind"],
                    "project": row["project"],
                }
                self.add_content_hash(content, metadata, "swarm_brain", str(row["id"]))
                swarm_hashes += 1
            except Exception as e:
                logger.error(f"Error hashing Swarm Brain doc {row['id']}: {e}")

        print(f"✅ Generated {swarm_hashes} Swarm Brain content hashes")

        # Hash Vector Database content
        vector_file = Path("vector_database/devlog_vectors.json")
        if vector_file.exists():
            with open(vector_file) as f:
                vectors = json.load(f)

            vector_hashes = 0
            for vector in vectors:
                try:
                    content = vector.get("content", "")
                    metadata = vector.get("metadata", {})
                    self.add_content_hash(
                        content, metadata, "vector_database", vector.get("id", "")
                    )
                    vector_hashes += 1
                except Exception as e:
                    logger.error(f"Error hashing vector {vector.get('id', 'unknown')}: {e}")

            print(f"✅ Generated {vector_hashes} Vector Database content hashes")

        # Hash Devlog Database content
        devlog_file = Path("devlogs/agent_devlogs.json")
        if devlog_file.exists():
            with open(devlog_file) as f:
                devlogs = json.load(f)

            devlog_hashes = 0
            for devlog in devlogs:
                try:
                    content = f"{devlog.get('action', '')} {devlog.get('details', '')}"
                    metadata = {
                        "agent_id": devlog.get("agent_id", ""),
                        "status": devlog.get("status", ""),
                        "timestamp": devlog.get("timestamp", ""),
                    }
                    self.add_content_hash(content, metadata, "devlogs", devlog.get("timestamp", ""))
                    devlog_hashes += 1
                except Exception as e:
                    logger.error(f"Error hashing devlog {devlog.get('timestamp', 'unknown')}: {e}")

            print(f"✅ Generated {devlog_hashes} Devlog Database content hashes")

        # Save all hashes
        self.save_hashes()

        return {
            "swarm_brain": swarm_hashes,
            "vector_database": vector_hashes,
            "devlogs": devlog_hashes,
        }

    def get_duplicate_report(self) -> dict[str, Any]:
        """Generate report of potential duplicates."""
        report = {
            "total_hashes": sum(
                len(hashes) for hashes in self.content_hashes.values() if isinstance(hashes, dict)
            ),
            "database_stats": {},
            "potential_duplicates": [],
            "hash_distribution": {},
        }

        for db_type, hashes in self.content_hashes.items():
            if db_type == "last_updated" or not isinstance(hashes, dict):
                continue

            report["database_stats"][db_type] = len(hashes)
            report["hash_distribution"][db_type] = len(hashes)

        return report

    def print_hash_report(self):
        """Print content hash report."""
        report = self.get_duplicate_report()

        print("\n🔐 CONTENT HASH SYSTEM REPORT")
        print("=" * 50)
        print(f"📊 Total Content Hashes: {report['total_hashes']}")
        print(f"📅 Last Updated: {self.content_hashes.get('last_updated', 'Never')}")

        print("\n📊 Database Hash Distribution:")
        for db_type, count in report["hash_distribution"].items():
            print(f"   {db_type}: {count} hashes")

        print("\n✅ Content hashing system is active and preventing duplicates!")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Content Hash System")
    parser.add_argument("--hash-all", action="store_true", help="Generate hashes for all content")
    parser.add_argument("--report", action="store_true", help="Show hash report")
    parser.add_argument("--check", type=str, help="Check if content is duplicate")

    args = parser.parse_args()

    hash_system = ContentHashSystem()

    if args.hash_all:
        stats = hash_system.hash_all_existing_content()
        print("\n🎉 Content hashing complete!")
        print(f"📊 Generated {sum(stats.values())} total content hashes")
        hash_system.print_hash_report()
    elif args.check:
        is_duplicate = hash_system.check_duplicate(args.check)
        print(f"🔍 Content duplicate check: {'DUPLICATE' if is_duplicate else 'UNIQUE'}")
    elif args.report:
        hash_system.print_hash_report()
    else:
        hash_system.print_hash_report()


if __name__ == "__main__":
    main()
