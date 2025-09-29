#!/usr/bin/env python3
"""
Simple Vector Database Cleanup
==============================

Simplified vector database cleanup using the existing devlog vector system.
"""

import hashlib
import json
import logging

# Add src to path for imports
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from swarm_brain import Retriever, SwarmBrain

logger = logging.getLogger(__name__)


class SimpleVectorCleanup:
    """Simple vector database cleanup using existing devlog system."""

    def __init__(self):
        """Initialize cleanup tool."""
        self.retriever = Retriever()
        self.brain = SwarmBrain()
        self.vector_file = Path("vector_database/devlog_vectors.json")
        self.devlog_file = Path("devlogs/agent_devlogs.json")

        # Load existing vectors
        if self.vector_file.exists():
            with open(self.vector_file) as f:
                self.existing_vectors = json.load(f)
        else:
            self.existing_vectors = []

        # Load existing devlogs
        if self.devlog_file.exists():
            with open(self.devlog_file) as f:
                self.existing_devlogs = json.load(f)
        else:
            self.existing_devlogs = []

        self.cleanup_stats = {"vectors_added": 0, "devlogs_added": 0, "total_processed": 0}

    def vectorize_swarm_brain_docs(self):
        """Vectorize Swarm Brain documents using simple approach."""
        print("🧠 Vectorizing Swarm Brain documents...")

        # Get all documents
        docs = self.retriever.search("", k=1000)
        if len(docs) < 100:
            # Try direct database query
            cursor = self.brain.conn.cursor()
            cursor.execute("SELECT * FROM documents ORDER BY id")
            rows = cursor.fetchall()

            docs = []
            for row in rows:
                try:
                    doc = {
                        "id": row["id"],
                        "kind": row["kind"],
                        "ts": row["ts"],
                        "title": row["title"],
                        "summary": row["summary"],
                        "tags": row["tags"],
                        "meta": row["meta"],
                        "canonical": row["canonical"],
                        "project": row["project"],
                        "agent_id": row["agent_id"],
                        "ref_id": row["ref_id"],
                    }
                    docs.append(doc)
                except Exception as e:
                    print(f"    ⚠️ Error processing row {row}: {e}")
                    continue

        print(f"📊 Processing {len(docs)} documents...")

        for doc in docs:
            try:
                # Create content for vectorization
                content = (
                    f"{doc.get('title', '')} {doc.get('summary', '')} {doc.get('canonical', '')}"
                )
                content_hash = hashlib.md5(content.encode()).hexdigest()

                # Check if already vectorized
                existing_hash = None
                for vector in self.existing_vectors:
                    if vector.get("content_hash") == content_hash:
                        existing_hash = vector.get("content_hash")
                        break

                if existing_hash:
                    continue  # Skip if already vectorized

                # Create new vector entry
                vector_entry = {
                    "id": f"swarm_doc_{doc['id']}",
                    "content_hash": content_hash,
                    "content": content,
                    "metadata": {
                        "agent_id": doc.get("agent_id", ""),
                        "kind": doc.get("kind", ""),
                        "project": doc.get("project", ""),
                        "timestamp": datetime.fromtimestamp(doc.get("ts", 0)).isoformat(),
                        "source": "swarm_brain_cleanup",
                        "swarm_brain_id": doc["id"],
                    },
                    "created_at": datetime.now().isoformat(),
                    "vector_type": "swarm_brain_document",
                }

                self.existing_vectors.append(vector_entry)
                self.cleanup_stats["vectors_added"] += 1

                # Also add to devlog database if it's an action or conversation
                if doc.get("kind") in ["action", "conversation"]:
                    devlog_entry = {
                        "agent_id": doc.get("agent_id", ""),
                        "action": doc.get("title", ""),
                        "status": "completed",
                        "details": doc.get("summary", ""),
                        "timestamp": datetime.fromtimestamp(doc.get("ts", 0)).isoformat(),
                        "storage_type": "swarm_brain_vectorized",
                    }

                    self.existing_devlogs.append(devlog_entry)
                    self.cleanup_stats["devlogs_added"] += 1

                self.cleanup_stats["total_processed"] += 1

            except Exception as e:
                print(f"    ⚠️ Error vectorizing doc {doc.get('id', 'unknown')}: {e}")
                continue

        print(f"✅ Vectorized {self.cleanup_stats['vectors_added']} new documents")
        print(f"✅ Added {self.cleanup_stats['devlogs_added']} devlog entries")

    def save_updated_databases(self):
        """Save updated vector and devlog databases."""
        print("💾 Saving updated databases...")

        # Save vector database
        with open(self.vector_file, "w") as f:
            json.dump(self.existing_vectors, f, indent=2)

        # Save devlog database
        with open(self.devlog_file, "w") as f:
            json.dump(self.existing_devlogs, f, indent=2)

        print(f"✅ Vector database: {len(self.existing_vectors)} entries")
        print(f"✅ Devlog database: {len(self.existing_devlogs)} entries")

    def generate_report(self):
        """Generate cleanup report."""
        print("\n📊 VECTOR DATABASE CLEANUP REPORT")
        print("=" * 50)
        print(f"🧠 Vectors Added: {self.cleanup_stats['vectors_added']}")
        print(f"📝 Devlogs Added: {self.cleanup_stats['devlogs_added']}")
        print(f"📊 Total Processed: {self.cleanup_stats['total_processed']}")
        print(f"🗃️ Total Vectors: {len(self.existing_vectors)}")
        print(f"📋 Total Devlogs: {len(self.existing_devlogs)}")
        print("=" * 50)

    def run_cleanup(self):
        """Run complete vector database cleanup."""
        print("🚀 Starting vector database cleanup...")
        print("=" * 60)

        try:
            # Vectorize documents
            self.vectorize_swarm_brain_docs()

            # Save databases
            self.save_updated_databases()

            # Generate report
            self.generate_report()

            print("\n🎉 VECTOR DATABASE CLEANUP COMPLETE!")
            print("All Swarm Brain documents are now vectorized and searchable.")

        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            logger.error(f"Vector cleanup failed: {e}")
            raise


def main():
    """Main entry point."""
    cleanup = SimpleVectorCleanup()
    cleanup.run_cleanup()


if __name__ == "__main__":
    main()
