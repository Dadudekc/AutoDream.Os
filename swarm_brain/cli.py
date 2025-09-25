#!/usr/bin/env python3
"""
Swarm Brain CLI
===============

Command-line interface for swarm brain operations.
V2 Compliance: ≤400 lines, focused CLI functionality.
"""

import argparse
import json
import sys
import logging
from .db import SwarmBrain
from .ingest import Ingestor
from .retriever import Retriever

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def cmd_ingest(args):
    """Handle ingest command."""
    try:
        ingestor = Ingestor()
        tags = json.loads(args.tags)
        payload = json.loads(args.payload)
        
        if args.kind == "action":
            doc_id = ingestor.action(
                project=args.project, 
                agent_id=args.agent, 
                tags=tags, 
                title=args.title, 
                **payload
            )
        elif args.kind == "protocol":
            doc_id = ingestor.protocol(
                project=args.project, 
                agent_id=args.agent, 
                tags=tags, 
                title=args.title, 
                **payload
            )
        elif args.kind == "workflow":
            doc_id = ingestor.workflow(
                project=args.project, 
                agent_id=args.agent, 
                tags=tags, 
                title=args.title, 
                **payload
            )
        elif args.kind == "performance":
            doc_id = ingestor.performance(
                project=args.project, 
                agent_id=args.agent, 
                tags=tags, 
                title=args.title, 
                **payload
            )
        elif args.kind == "conversation":
            doc_id = ingestor.conversation(
                project=args.project, 
                agent_id=args.agent, 
                tags=tags, 
                title=args.title, 
                **payload
            )
        else:
            print(f"Unknown kind: {args.kind}")
            return 1
        
        print(f"OK - Document ID: {doc_id}")
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


def cmd_query(args):
    """Handle query command."""
    try:
        retriever = Retriever()
        kinds = args.kinds.split(",") if args.kinds else None
        
        results = retriever.search(
            args.q, 
            k=args.k, 
            project=args.project, 
            kinds=kinds, 
            agent_id=args.agent
        )
        
        print(json.dumps(results, indent=2))
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


def cmd_stats(args):
    """Handle stats command."""
    try:
        brain = SwarmBrain()
        
        if args.agent:
            stats = brain.get_agent_stats(args.agent)
            print(json.dumps(stats, indent=2))
        elif args.project:
            stats = brain.get_project_stats(args.project)
            print(json.dumps(stats, indent=2))
        else:
            print("ERROR: Must specify --agent or --project")
            return 1
        
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


def cmd_cleanup(args):
    """Handle cleanup command."""
    try:
        brain = SwarmBrain()
        cleaned = brain.cleanup_old_documents(args.max_age_days)
        print(f"Cleaned up {cleaned} old documents")
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser("swarm-brain", description="Swarm Brain CLI")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest data")
    ingest_parser.add_argument("--kind", required=True, 
                              choices=["action", "protocol", "workflow", "performance", "conversation"])
    ingest_parser.add_argument("--project", required=True, help="Project identifier")
    ingest_parser.add_argument("--agent", required=True, help="Agent identifier")
    ingest_parser.add_argument("--title", required=True, help="Document title")
    ingest_parser.add_argument("--tags", default="[]", help="JSON array of tags")
    ingest_parser.add_argument("--payload", required=True, help="JSON payload for kind-specific fields")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Search patterns")
    query_parser.add_argument("q", help="Search query")
    query_parser.add_argument("--project", help="Filter by project")
    query_parser.add_argument("--kinds", help="Comma-separated document kinds")
    query_parser.add_argument("--agent", help="Filter by agent")
    query_parser.add_argument("--k", type=int, default=10, help="Number of results")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get statistics")
    stats_parser.add_argument("--agent", help="Agent identifier")
    stats_parser.add_argument("--project", help="Project identifier")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Cleanup old data")
    cleanup_parser.add_argument("--max-age-days", type=int, default=30, help="Maximum age in days")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Route to appropriate command handler
    if args.cmd == "ingest":
        return cmd_ingest(args)
    elif args.cmd == "query":
        return cmd_query(args)
    elif args.cmd == "stats":
        return cmd_stats(args)
    elif args.cmd == "cleanup":
        return cmd_cleanup(args)
    else:
        print(f"Unknown command: {args.cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())




