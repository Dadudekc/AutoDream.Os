#!/usr/bin/env python3
"""
Swarm Brain Integration Example
===============================

Example showing how to integrate the Swarm Brain into existing agent systems.
This demonstrates the key integration points for immediate deployment.
"""

import logging
from swarm_brain import SwarmBrain, Ingestor, Retriever
from swarm_brain.decorators import vectorized_action, vectorized_protocol
from swarm_brain.connectors import ingest_scan, ingest_devlog, ingest_discord, ingest_performance

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_project_scanner_integration():
    """Example: Integrate with project scanner."""
    logger.info("=== Project Scanner Integration ===")
    
    # Simulate project scanner result
    scan_result = {
        "compliance": {"v2_pass": 97.6, "violations": [{"file": "large_file.py", "rule": "len>400"}]},
        "refactoring": [{"pattern": "split-module", "files": ["large_file.py"]}],
        "summary": "V2 97.6%, 1 violation found",
        "files_analyzed": 603,
        "total_lines": 125000
    }
    
    # Ingest scanner results
    ingest_scan(scan_result, project="Agent_Cellphone_V2", agent_id="Agent-2")
    logger.info("✅ Project scanner results ingested")


def example_discord_integration():
    """Example: Integrate with Discord commander."""
    logger.info("=== Discord Integration ===")
    
    # Simulate Discord communication
    discord_message = "Agent-2 completed project scan. Found 1 V2 violation in large_file.py. Suggesting split-module refactor."
    thread_id = "coordination_thread_123"
    
    # Ingest Discord communication
    ingest_discord(
        message=discord_message,
        thread_id=thread_id,
        project="Agent_Cellphone_V2",
        agent_id="Agent-6",
        outcome="success"
    )
    logger.info("✅ Discord communication ingested")


def example_devlog_integration():
    """Example: Integrate with devlog system."""
    logger.info("=== Devlog Integration ===")
    
    # Simulate devlog entry
    devlog_text = """
    Agent-2 completed project analysis:
    - Analyzed 603 files
    - Found 1 V2 compliance violation
    - Generated refactoring suggestions
    - Ready for Agent-3 to implement fixes
    """
    
    # Ingest devlog
    ingest_devlog(
        text=devlog_text,
        project="Agent_Cellphone_V2",
        agent_id="Agent-2",
        channel="devlog"
    )
    logger.info("✅ Devlog entry ingested")


def example_performance_integration():
    """Example: Integrate with performance monitoring."""
    logger.info("=== Performance Integration ===")
    
    # Simulate performance data
    metrics = {
        "cpu_usage": 45.0,
        "memory_usage": 60.0,
        "response_time": 1.2,
        "active_agents": 8
    }
    
    anomalies = {
        "high_memory_usage": False,
        "slow_response": False
    }
    
    optimizations = {
        "cache_size": 1000,
        "parallel_processing": True
    }
    
    # Ingest performance data
    ingest_performance(
        metrics=metrics,
        anomalies=anomalies,
        optimizations=optimizations,
        project="Agent_Cellphone_V2",
        agent_id="Agent-8"
    )
    logger.info("✅ Performance data ingested")


def example_decorator_usage():
    """Example: Using decorators for automatic recording."""
    logger.info("=== Decorator Usage ===")
    
    # Example agent function with decorator
    @vectorized_action(
        tool="compliance_fixer",
        project="Agent_Cellphone_V2",
        agent_id="Agent-3",
        tags=["compliance", "refactor", "v2"]
    )
    def fix_v2_compliance(file_path: str, violation_type: str):
        """Fix V2 compliance violation."""
        logger.info(f"Fixing {violation_type} in {file_path}")
        
        # Simulate fix
        return {
            "success": True,
            "summary": f"Fixed {violation_type} in {file_path}",
            "lines_before": 450,
            "lines_after": 380
        }
    
    # Execute the function (automatically recorded)
    result = fix_v2_compliance("large_file.py", "length_violation")
    logger.info(f"✅ Function executed and recorded: {result['summary']}")


def example_query_usage():
    """Example: Querying the swarm brain."""
    logger.info("=== Query Usage ===")
    
    retriever = Retriever()
    
    # Query for V2 compliance patterns
    patterns = retriever.how_do_agents_do("V2 compliance refactoring", k=5)
    logger.info(f"Found {len(patterns)} V2 compliance patterns")
    
    for pattern in patterns[:3]:  # Show first 3
        logger.info(f"  - {pattern.get('title', 'No title')} by {pattern.get('agent_id', 'Unknown')}")
    
    # Query for similar problems
    similar = retriever.find_similar_problems("large file refactoring", k=3)
    logger.info(f"Found {len(similar)} similar problems")
    
    # Get agent expertise
    expertise = retriever.get_agent_expertise("Agent-2", k=10)
    logger.info(f"Agent-2 expertise: {expertise.get('total_patterns', 0)} patterns")
    
    # Get project patterns
    project_patterns = retriever.get_project_patterns("Agent_Cellphone_V2", k=10)
    logger.info(f"Project patterns: {project_patterns.get('total_activities', 0)} activities")


def example_cli_usage():
    """Example: Using the CLI interface."""
    logger.info("=== CLI Usage ===")
    
    import subprocess
    import json
    
    # Example CLI commands
    commands = [
        # Ingest an action
        [
            "python", "-m", "swarm_brain.cli", "ingest",
            "--kind", "action",
            "--project", "Agent_Cellphone_V2",
            "--agent", "Agent-2",
            "--title", "CLI Test Action",
            "--tags", '["test", "cli"]',
            "--payload", json.dumps({
                "tool": "test_tool",
                "outcome": "success",
                "context": {"test": True}
            })
        ],
        # Query for patterns
        [
            "python", "-m", "swarm_brain.cli", "query",
            "test patterns",
            "--project", "Agent_Cellphone_V2",
            "--k", "5"
        ]
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info(f"✅ CLI command succeeded: {' '.join(cmd[3:6])}")
            else:
                logger.warning(f"⚠️ CLI command failed: {result.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ CLI command error: {e}")


def main():
    """Run all integration examples."""
    logger.info("🚀 Swarm Brain Integration Examples")
    logger.info("=" * 50)
    
    try:
        # Initialize swarm brain
        brain = SwarmBrain()
        logger.info("✅ Swarm Brain initialized")
        
        # Run integration examples
        example_project_scanner_integration()
        example_discord_integration()
        example_devlog_integration()
        example_performance_integration()
        example_decorator_usage()
        
        # Query examples
        example_query_usage()
        
        # CLI examples
        example_cli_usage()
        
        logger.info("=" * 50)
        logger.info("🎉 All integration examples completed successfully!")
        logger.info("The Swarm Brain is ready for agent coordination!")
        
    except Exception as e:
        logger.error(f"❌ Integration example failed: {e}")
        raise


if __name__ == "__main__":
    main()




