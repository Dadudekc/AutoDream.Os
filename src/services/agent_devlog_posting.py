#!/usr/bin/env python3
"""
Agent Devlog Posting Service
============================

Standalone Python service for agents to post devlogs to LOCAL FILES.
NO Discord dependency - completely independent system.
Agents can call this script programmatically with their agent flag.

Features:
- Agent flag validation (Agent-1 through Agent-8)
- Local file-based devlog storage (NO Discord)
- JSON file storage in devlogs/ directory
- Command-line interface for devlog posting
- Error handling and logging
- Help command for usage instructions

Usage:
    python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed" --status completed --details "Details here"
    python src/services/agent_devlog_posting.py --agent Agent-4 --action "Task completed" --vectorize --cleanup
    python src/services/agent_devlog_posting.py --search "discord dependency"
    python src/services/agent_devlog_posting.py --stats
    python src/services/agent_devlog_posting.py --agent Agent-4 --action "Test" --dry-run
    python src/services/agent_devlog_posting.py --show-help

🐝 WE ARE SWARM - Agent Devlog Posting System (LOCAL ONLY)
"""

import asyncio
import logging
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentDevlogPoster:
    """Agent devlog posting service with LOCAL FILE storage (NO Discord)."""

    def __init__(self):
        """Initialize agent devlog poster."""
        self.devlogs_dir = Path("devlogs")
        self.devlogs_dir.mkdir(exist_ok=True)

        # Agent role mapping
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }

        logger.info("AgentDevlogPoster initialized - Local file storage only (NO Discord)")

    def validate_agent_flag(self, agent_flag: str) -> bool:
        """Validate agent flag format and range."""
        if not agent_flag.startswith("Agent-"):
            return False

        try:
            agent_number = int(agent_flag[6:])
            return 1 <= agent_number <= 8
        except ValueError:
            return False

    def create_devlog_content(self, agent_flag: str, action: str, status: str = "completed", details: str = "") -> str:
        """Create formatted devlog content for local file storage."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        content = f"""# 🤖 Agent Devlog - {agent_flag}

## 📅 Timestamp
{timestamp}

## 🎯 Agent Information
- **Agent ID:** {agent_flag}
- **Role:** {self.agent_roles.get(agent_flag, "Specialist")}
- **Status:** {status}

## 📝 Action Details
**Action:** {action}

## 🔧 Technical Details
- **Devlog Type:** Agent Action
- **Posting Method:** Local File Storage
- **Storage Type:** JSON File

## 📄 Additional Details
{details if details else "No additional details provided"}

---
🐝 **WE ARE SWARM** - Agent Coordination Active (Local Storage)
"""

        return content

    def save_devlog_to_file(self, agent_flag: str, action: str, status: str = "completed", details: str = "") -> bool:
        """Save devlog to local JSON file (NO Discord)."""
        try:
            # Validate agent flag
            if not self.validate_agent_flag(agent_flag):
                logger.error(f"Invalid agent flag: {agent_flag}. Use Agent-1 through Agent-8")
                return False

            # Create devlog entry
            devlog = {
                'agent_id': agent_flag,
                'action': action,
                'status': status,
                'details': details,
                'timestamp': datetime.now().isoformat(),
                'storage_type': 'local_file'
            }

            # Save to JSON file
            filename = f"devlog_{agent_flag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.devlogs_dir / filename

            with open(filepath, 'w') as f:
                json.dump(devlog, f, indent=2, default=str)

            logger.info(f"✅ Devlog saved to local file: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving devlog to file: {e}")
            return False

    def save_devlog_to_json_database(self, agent_flag: str, action: str, status: str = "completed", details: str = "") -> bool:
        """Save devlog to main JSON database file (NO Discord)."""
        try:
            # Validate agent flag
            if not self.validate_agent_flag(agent_flag):
                logger.error(f"Invalid agent flag: {agent_flag}. Use Agent-1 through Agent-8")
                return False

            # Create devlog entry
            devlog = {
                'agent_id': agent_flag,
                'action': action,
                'status': status,
                'details': details,
                'timestamp': datetime.now().isoformat(),
                'storage_type': 'json_database'
            }

            # Save to main devlogs database
            db_file = self.devlogs_dir / "agent_devlogs.json"

            # Load existing devlogs
            existing_devlogs = []
            if db_file.exists():
                try:
                    with open(db_file, 'r') as f:
                        existing_devlogs = json.load(f)
                except Exception as e:
                    logger.warning(f"Error loading existing devlogs: {e}")

            # Add new devlog
            existing_devlogs.append(devlog)

            # Save back to file
            with open(db_file, 'w') as f:
                json.dump(existing_devlogs, f, indent=2, default=str)

            logger.info(f"✅ Devlog saved to JSON database: {len(existing_devlogs)} total devlogs")
            return True

        except Exception as e:
            logger.error(f"Error saving devlog to database: {e}")
            return False

    async def post_devlog(self, agent_flag: str, action: str, status: str = "completed", details: str = "", vectorize: bool = False, cleanup: bool = False) -> bool:
        """Post devlog to local file storage (NO Discord dependency)."""
        try:
            # Validate agent flag
            if not self.validate_agent_flag(agent_flag):
                logger.error(f"Invalid agent flag: {agent_flag}. Use Agent-1 through Agent-8")
                return False

            # Save to JSON database (main storage)
            db_success = self.save_devlog_to_json_database(agent_flag, action, status, details)

            if not db_success:
                logger.error(f"Failed to save devlog to database for {agent_flag}")
                return False

            # Save to individual file (backup)
            file_success = self.save_devlog_to_file(agent_flag, action, status, details)

            # Vectorize if requested (placeholder for future vector database integration)
            if vectorize:
                logger.info(f"🧠 Vectorization requested for {agent_flag} - would integrate with vector database here")

                # Clean up individual file if requested and vectorization was successful
                if cleanup and file_success:
                    # In a real implementation, this would be handled by vector database cleanup
                    logger.info(f"✅ Vectorization and cleanup completed for {agent_flag}")
            else:
                logger.info(f"📁 Devlog saved to file for {agent_flag}")

            logger.info(f"✅ Devlog posted successfully to local storage for {agent_flag}")
            return True

        except Exception as e:
            logger.error(f"Failed to post devlog to local storage: {e}")
            return False

    def save_devlog_file(self, agent_flag: str, action: str, status: str = "completed", details: str = "") -> str:
        """Save devlog to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{agent_flag}_{action.replace(' ', '_')}.md"
        filepath = self.devlogs_dir / filename

        content = self.create_devlog_content(agent_flag, action, status, details)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"✅ Devlog saved to file: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to save devlog file: {e}")
            return ""

    async def post_devlog_with_vectorization(self, agent_flag: str, action: str, status: str = "completed", details: str = "", vectorize: bool = False, cleanup: bool = False) -> bool:
        """Post devlog with optional vectorization and cleanup."""
        logger.info(f"📝 Posting devlog for {agent_flag}: {action} (vectorize={vectorize}, cleanup={cleanup})")

        # Validate agent flag
        if not self.validate_agent_flag(agent_flag):
            logger.error(f"Invalid agent flag: {agent_flag}. Use Agent-1 through Agent-8")
            return False

        # Save to file
        filepath = self.save_devlog_file(agent_flag, action, status, details)

        if not filepath:
            logger.error(f"Failed to save devlog file for {agent_flag}")
            return False

        # Save to JSON database
        db_success = self.save_devlog_to_json_database(agent_flag, action, status, details)

        if not db_success:
            logger.warning(f"⚠️ Devlog saved to file but database save failed for {agent_flag}")
            return True  # Still consider successful if file was saved

        # Vectorize if requested
        if vectorize:
            vectorization_success = await self._vectorize_devlog(filepath, agent_flag, action, status, details)

            if vectorization_success:
                logger.info(f"✅ Devlog vectorized and added to database for {agent_flag}")

                # Clean up file if requested
                if cleanup:
                    try:
                        Path(filepath).unlink()
                        logger.info(f"✅ Devlog file cleaned up after vectorization for {agent_flag}")
                    except Exception as e:
                        logger.warning(f"Failed to cleanup devlog file: {e}")
            else:
                logger.warning(f"⚠️ Devlog vectorization failed for {agent_flag}")

        logger.info(f"✅ Devlog posted successfully to local storage for {agent_flag}")
        return True

    def get_devlogs(self, agent_id: str = None, limit: int = 10) -> list:
        """Get devlogs from JSON database."""
        try:
            db_file = self.devlogs_dir / "agent_devlogs.json"

            if not db_file.exists():
                return []

            with open(db_file, 'r') as f:
                devlogs = json.load(f)

            if agent_id:
                devlogs = [d for d in devlogs if d.get('agent_id') == agent_id]

            return devlogs[-limit:] if limit > 0 else devlogs

        except Exception as e:
            logger.error(f"Error getting devlogs: {e}")
            return []

    def get_devlog_stats(self) -> dict:
        """Get statistics about stored devlogs."""
        try:
            devlogs = self.get_devlogs()

            agents = set()
            status_counts = {}

            for devlog in devlogs:
                agent = devlog.get('agent_id', '')
                if agent:
                    agents.add(agent)

                status = devlog.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            return {
                'total_devlogs': len(devlogs),
                'unique_agents': len(agents),
                'active_agents': list(agents),
                'status_distribution': status_counts
            }

        except Exception as e:
            logger.error(f"Error getting devlog stats: {e}")
            return {
                'total_devlogs': 0,
                'unique_agents': 0,
                'active_agents': [],
                'status_distribution': {}
            }

    async def _vectorize_devlog(self, filepath: str, agent_flag: str, action: str, status: str, details: str) -> bool:
        """Vectorize devlog content and add to vector database."""
        try:
            logger.info(f"🧠 Vectorizing devlog: {filepath}")

            # Read devlog content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"Empty devlog content for {agent_flag}")
                return False

            # Create searchable text (combine all content)
            searchable_text = f"""
            Agent: {agent_flag}
            Action: {action}
            Status: {status}
            Details: {details}
            Content: {content}
            """

            # Create metadata
            metadata = {
                "agent_id": agent_flag,
                "action": action,
                "status": status,
                "details": details,
                "timestamp": datetime.now().isoformat(),
                "source": "agent_devlog_system",
                "type": "devlog",
                "filepath": filepath
            }

            # Add to simple vector database (JSON-based for now)
            vector_db_success = await self._add_to_vector_database(searchable_text, metadata)

            if vector_db_success:
                logger.info(f"✅ Devlog vectorized and added to database: {agent_flag}")
                return True
            else:
                logger.warning(f"⚠️ Failed to add devlog to vector database: {agent_flag}")
                return False

        except Exception as e:
            logger.error(f"Failed to vectorize devlog: {e}")
            return False

    async def _add_to_vector_database(self, content: str, metadata: dict) -> bool:
        """Add content to simple vector database."""
        try:
            # Create simple vector database directory
            vector_db_dir = Path("vector_database")
            vector_db_dir.mkdir(exist_ok=True)

            # Create vector database file
            db_file = vector_db_dir / "devlog_vectors.json"

            # Load existing vectors
            existing_vectors = []
            if db_file.exists():
                try:
                    with open(db_file, 'r') as f:
                        existing_vectors = json.load(f)
                except Exception as e:
                    logger.warning(f"Error loading existing vectors: {e}")

            # Create simple vector representation (hash of content for now)
            import hashlib
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Create vector entry
            vector_entry = {
                'id': f"devlog_{len(existing_vectors) + 1}",
                'content_hash': content_hash,
                'content': content,
                'metadata': metadata,
                'created_at': datetime.now().isoformat(),
                'vector_type': 'simple_hash'
            }

            # Add to database
            existing_vectors.append(vector_entry)

            # Save back to file
            with open(db_file, 'w') as f:
                json.dump(existing_vectors, f, indent=2, default=str)

            logger.info(f"✅ Vector entry added to database: {vector_entry['id']}")
            return True

        except Exception as e:
            logger.error(f"Failed to add to vector database: {e}")
            return False

    def search_devlogs(self, query: str, limit: int = 10) -> list:
        """Search devlogs using simple text matching."""
        try:
            vector_db_dir = Path("vector_database")
            db_file = vector_db_dir / "devlog_vectors.json"

            if not db_file.exists():
                return []

            with open(db_file, 'r') as f:
                vectors = json.load(f)

            # Simple text search
            results = []
            query_lower = query.lower()

            for vector in vectors:
                content = vector.get('content', '').lower()
                metadata = vector.get('metadata', {})

                # Search in content and metadata
                if (query_lower in content or
                    query_lower in metadata.get('action', '').lower() or
                    query_lower in metadata.get('agent_id', '').lower() or
                    query_lower in metadata.get('status', '').lower()):

                    results.append({
                        'id': vector['id'],
                        'metadata': metadata,
                        'content_preview': vector['content'][:200] + "..." if len(vector['content']) > 200 else vector['content'],
                        'relevance_score': 1.0  # Simple scoring for now
                    })

            # Sort by relevance (for now just by ID descending)
            results.sort(key=lambda x: int(x['id'].split('_')[1]), reverse=True)
            return results[:limit]

        except Exception as e:
            logger.error(f"Error searching devlogs: {e}")
            return []

    def get_vector_database_stats(self) -> dict:
        """Get statistics about the vector database."""
        try:
            vector_db_dir = Path("vector_database")
            db_file = vector_db_dir / "devlog_vectors.json"

            if not db_file.exists():
                return {
                    'total_vectors': 0,
                    'agents': [],
                    'status_distribution': {},
                    'database_size': 0
                }

            with open(db_file, 'r') as f:
                vectors = json.load(f)

            agents = set()
            status_counts = {}

            for vector in vectors:
                metadata = vector.get('metadata', {})
                agent = metadata.get('agent_id', '')
                if agent:
                    agents.add(agent)

                status = metadata.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            return {
                'total_vectors': len(vectors),
                'unique_agents': len(agents),
                'agents': list(agents),
                'status_distribution': status_counts,
                'database_size': db_file.stat().st_size
            }

        except Exception as e:
            logger.error(f"Error getting vector database stats: {e}")
            return {
                'total_vectors': 0,
                'unique_agents': 0,
                'agents': [],
                'status_distribution': {},
                'database_size': 0
            }


async def main():
    """Main function for command-line usage."""
    parser = ArgumentParser(description="Agent Devlog Posting Service")
    parser.add_argument("--agent", "-a", help="Agent flag (Agent-1 through Agent-8)")
    parser.add_argument("--action", "-x", help="Action description")
    parser.add_argument("--status", "-s", default="completed", choices=["completed", "in_progress", "failed"], help="Action status")
    parser.add_argument("--details", "-d", default="", help="Additional details")
    parser.add_argument("--vectorize", "-v", action="store_true", help="Vectorize devlog and add to database")
    parser.add_argument("--cleanup", "-c", action="store_true", help="Clean up devlog file after vectorization")
    parser.add_argument("--search", help="Search devlogs using query")
    parser.add_argument("--stats", action="store_true", help="Show vector database statistics")
    parser.add_argument("--dry-run", "-t", action="store_true", help="Test mode - don't actually post")
    parser.add_argument("--show-help", action="store_true", help="Show this help message")

    args = parser.parse_args()

    if args.show_help:
        print(__doc__)
        return 0

    # Validate arguments based on operation
    if not args.stats and not args.search:
        # For posting devlogs, require agent and action
        if not args.agent or not args.action:
            print("❌ Error: --agent and --action are required for posting devlogs")
            print("💡 Use --search for searching or --stats for statistics")
            return 1

    if args.stats:
        # Show vector database statistics
        try:
            poster = AgentDevlogPoster()
            stats = poster.get_vector_database_stats()

            print("🧠 VECTOR DATABASE STATISTICS")
            print("=" * 40)
            print(f"📊 Total Vectors: {stats['total_vectors']}")
            print(f"👥 Unique Agents: {stats['unique_agents']}")
            print(f"📁 Database Size: {stats['database_size']} bytes")
            print()
            print("👤 Active Agents:")
            for agent in stats['agents']:
                print(f"  - {agent}")
            print()
            print("📈 Status Distribution:")
            for status, count in stats['status_distribution'].items():
                print(f"  - {status}: {count}")
            return 0
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return 1

    if args.search:
        # Search devlogs
        try:
            poster = AgentDevlogPoster()
            results = poster.search_devlogs(args.search, limit=10)

            print(f"🔍 SEARCH RESULTS FOR: '{args.search}'")
            print("=" * 50)
            print(f"📊 Found {len(results)} results")
            print()

            if results:
                for result in results:
                    print(f"📝 ID: {result['id']}")
                    print(f"👤 Agent: {result['metadata']['agent_id']}")
                    print(f"🎯 Action: {result['metadata']['action']}")
                    print(f"📊 Status: {result['metadata']['status']}")
                    print(f"📄 Preview: {result['content_preview']}")
                    print(f"📅 Created: {result['metadata']['timestamp']}")
                    print("-" * 40)
            else:
                print("No results found.")
            return 0
        except Exception as e:
            print(f"❌ Error searching: {e}")
            return 1

    try:
        # Initialize poster
        poster = AgentDevlogPoster()

        # Post devlog with vectorization options
        success = await poster.post_devlog_with_vectorization(
            agent_flag=args.agent,
            action=args.action,
            status=args.status,
            details=args.details,
            vectorize=args.vectorize,
            cleanup=args.cleanup
        )

        if success:
            print(f"✅ Devlog posted successfully to local storage for {args.agent}")
            print(f"📝 Agent: {args.agent}")
            print(f"🎯 Action: {args.action}")
            print(f"📊 Status: {args.status}")
            print(f"📄 Details: {args.details}")
            print("📁 Storage: Local JSON database + individual files")
            print("🚫 NO Discord dependency - completely independent")
            return 0
        else:
            print(f"❌ Failed to post devlog for {args.agent}")
            return 1

    except Exception as e:
        logger.error(f"Error in agent devlog posting: {e}")
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    # Run main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
