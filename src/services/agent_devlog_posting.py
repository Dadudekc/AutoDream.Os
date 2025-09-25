#!/usr/bin/env python3
"""
Agent Devlog Posting Service
============================

REFACTORED: Now uses modular design with focused components
V2 Compliant: ≤400 lines, imports from agent_devlog package

This file now serves as the main entry point and maintains backward compatibility
while delegating to the modular agent_devlog package.

Standalone Python service for agents to post devlogs to LOCAL FILES.
NO Discord dependency - completely independent system.

🐝 WE ARE SWARM - Agent Devlog Posting System (LOCAL ONLY)
"""

import asyncio
import sys
from .agent_devlog import AgentDevlogPoster, AgentDevlogCLI

# Re-export for backward compatibility
__all__ = ["AgentDevlogPoster", "AgentDevlogCLI"]

# Main execution function for backward compatibility
async def main():
    """Main execution function"""
    print("🤖 Agent Devlog Posting Service (Refactored)")
    print("📦 Using modular agent_devlog package")
    
    # Create CLI and run
    cli = AgentDevlogCLI()
    parser = cli.create_parser()
    args = parser.parse_args()
    
    await cli.run(args)

if __name__ == "__main__":
    asyncio.run(main())