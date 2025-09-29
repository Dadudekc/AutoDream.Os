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
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import with fallback
try:
    from services.agent_devlog import AgentDevlogCLI, AgentDevlogPoster
except ImportError:
    try:
        from .agent_devlog import AgentDevlogCLI, AgentDevlogPoster
    except ImportError:
        # Fallback to direct implementation if modular package doesn't exist
        from src.services.agent_devlog_service import DiscordDevlogService

        class AgentDevlogPoster:
            def __init__(self):
                self.devlog_service = DiscordDevlogService()

            async def post_devlog(
                self, agent_flag: str, action: str, status: str = "completed", details: str = ""
            ):
                return await self.devlog_service.create_and_post_devlog(
                    agent_id=agent_flag,
                    action=action,
                    status=status,
                    details={"details": details},
                    post_to_discord=False,
                )


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
