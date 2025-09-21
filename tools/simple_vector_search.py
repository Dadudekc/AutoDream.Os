#!/usr/bin/env python3
"""
Simple Vector Search Tool
========================

Simplified vector search tool that works with existing messaging system.
Provides basic knowledge search capabilities for agents.

Author: Agent-4 (Captain)
Date: 2025-01-15
V2 Compliance: ≤400 lines, modular design
"""

import sys
import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def search_message_history(query: str, agent_id: str = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Search message history for similar content."""
    try:
        # Search in agent workspaces for messages
        results = []
        agent_workspaces = Path("agent_workspaces")
        
        if not agent_workspaces.exists():
            return []
        
        # Search through agent inboxes
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                current_agent = agent_dir.name
                
                # Skip if looking for specific agent
                if agent_id and current_agent != agent_id:
                    continue
                
                inbox_dir = agent_dir / "inbox"
                if inbox_dir.exists():
                    for msg_file in inbox_dir.glob("*.md"):
                        try:
                            content = msg_file.read_text(encoding="utf-8")
                            
                            # Simple text matching
                            if query.lower() in content.lower():
                                # Extract message info
                                lines = content.split('\n')
                                from_agent = "Unknown"
                                to_agent = current_agent
                                timestamp = msg_file.stat().st_mtime
                                
                                for line in lines:
                                    if line.startswith("**From**: "):
                                        from_agent = line.replace("**From**: ", "").strip()
                                    elif line.startswith("**To**: "):
                                        to_agent = line.replace("**To**: ", "").strip()
                                
                                results.append({
                                    "content": content[:200] + "..." if len(content) > 200 else content,
                                    "from_agent": from_agent,
                                    "to_agent": to_agent,
                                    "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
                                    "similarity": 0.8,  # Simple match
                                    "priority": "NORMAL",
                                    "file": str(msg_file)
                                })
                                
                        except Exception as e:
                            continue
        
        # Sort by timestamp (newest first) and limit results
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:limit]
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []


def search_devlogs(query: str, agent_id: str = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Search devlogs for similar content."""
    try:
        results = []
        devlogs_dir = Path("devlogs")
        
        if not devlogs_dir.exists():
            return []
        
        # Search through devlogs
        for devlog_file in devlogs_dir.glob("*.md"):
            try:
                content = devlog_file.read_text(encoding="utf-8")
                
                # Simple text matching
                if query.lower() in content.lower():
                    # Extract devlog info
                    lines = content.split('\n')
                    title = devlog_file.stem
                    timestamp = devlog_file.stat().st_mtime
                    
                    # Try to extract agent from filename or content
                    agent = "Unknown"
                    if agent_id and agent_id in title:
                        agent = agent_id
                    elif "Agent-" in title:
                        for line in lines[:10]:  # Check first 10 lines
                            if "Agent-" in line:
                                agent = line.split("Agent-")[1].split()[0] if "Agent-" in line else "Unknown"
                                agent = f"Agent-{agent}"
                                break
                    
                    results.append({
                        "content": content[:200] + "..." if len(content) > 200 else content,
                        "title": title,
                        "agent": agent,
                        "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
                        "similarity": 0.8,  # Simple match
                        "type": "devlog",
                        "file": str(devlog_file)
                    })
                    
            except Exception as e:
                continue
        
        # Sort by timestamp (newest first) and limit results
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results[:limit]
        
    except Exception as e:
        print(f"❌ Devlog search failed: {e}")
        return []


def get_agent_status_summary(agent_id: str) -> Dict[str, Any]:
    """Get basic status summary for an agent."""
    try:
        agent_workspace = Path("agent_workspaces") / agent_id
        
        if not agent_workspace.exists():
            return {"error": f"Agent {agent_id} workspace not found"}
        
        # Count messages in inbox
        inbox_dir = agent_workspace / "inbox"
        message_count = len(list(inbox_dir.glob("*.md"))) if inbox_dir.exists() else 0
        
        # Check for task files
        working_tasks = agent_workspace / "working_tasks.json"
        future_tasks = agent_workspace / "future_tasks.json"
        
        working_tasks_count = 0
        future_tasks_count = 0
        
        if working_tasks.exists():
            try:
                with open(working_tasks) as f:
                    data = json.load(f)
                    working_tasks_count = len(data.get("tasks", []))
            except:
                pass
        
        if future_tasks.exists():
            try:
                with open(future_tasks) as f:
                    data = json.load(f)
                    future_tasks_count = len(data.get("tasks", []))
            except:
                pass
        
        return {
            "agent_id": agent_id,
            "workspace_exists": True,
            "message_count": message_count,
            "working_tasks": working_tasks_count,
            "future_tasks": future_tasks_count,
            "status": "active" if message_count > 0 or working_tasks_count > 0 else "inactive"
        }
        
    except Exception as e:
        return {"error": str(e)}


def print_search_results(results: List[Dict[str, Any]], query: str, search_type: str = "messages"):
    """Print search results in a readable format."""
    if not results:
        print(f"🔍 No {search_type} found for: '{query}'")
        return
    
    print(f"🔍 Found {len(results)} {search_type} for: '{query}'")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        similarity = result.get("similarity", 0)
        content = result.get("content", "")[:100] + "..." if len(result.get("content", "")) > 100 else result.get("content", "")
        timestamp = result.get("timestamp", "Unknown")
        
        if search_type == "messages":
            from_agent = result.get("from_agent", "Unknown")
            to_agent = result.get("to_agent", "Unknown")
            priority = result.get("priority", "NORMAL")
            
            print(f"\n{i}. Similarity: {similarity:.2f} | Priority: {priority}")
            print(f"   From: {from_agent} → To: {to_agent}")
            print(f"   Time: {timestamp}")
            print(f"   Content: {content}")
        else:  # devlogs
            title = result.get("title", "Unknown")
            agent = result.get("agent", "Unknown")
            
            print(f"\n{i}. Similarity: {similarity:.2f} | Agent: {agent}")
            print(f"   Title: {title}")
            print(f"   Time: {timestamp}")
            print(f"   Content: {content}")


def main():
    """Main function for simple vector search tool."""
    parser = argparse.ArgumentParser(description="Simple Vector Search Tool")
    parser.add_argument("--agent", help="Agent ID (e.g., Agent-1, Agent-2)")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results")
    parser.add_argument("--devlogs", action="store_true", help="Search devlogs instead of messages")
    parser.add_argument("--status", action="store_true", help="Get agent status summary")
    
    args = parser.parse_args()
    
    # Get agent status summary
    if args.status:
        if not args.agent:
            print("❌ Agent ID required for status summary")
            return
        
        summary = get_agent_status_summary(args.agent)
        print(f"📊 Status Summary for {args.agent}:")
        print(json.dumps(summary, indent=2))
        return
    
    # Search devlogs
    if args.devlogs:
        if not args.query:
            print("❌ Query required for devlog search. Use --query 'your search term'")
            return
        
        results = search_devlogs(args.query, args.agent, args.limit)
        print_search_results(results, args.query, "devlogs")
        return
    
    # Search messages
    if args.query:
        results = search_message_history(args.query, args.agent, args.limit)
        print_search_results(results, args.query, "messages")
    else:
        print("❌ Query required for message search. Use --query 'your search term'")
        print("\n📋 Available commands:")
        print("  python tools/simple_vector_search.py --query 'Discord bot' --limit 5")
        print("  python tools/simple_vector_search.py --agent Agent-4 --query 'consolidation' --devlogs")
        print("  python tools/simple_vector_search.py --agent Agent-4 --status")


if __name__ == "__main__":
    main()
