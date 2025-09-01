#!/usr/bin/env python3
"""
Gaming Test Runner (V2 Compliant)
===============================

V2-compliant gaming test runner using modularized components.

Author: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

# Import modularized components
from .test_runner_core import GamingTestRunnerCore
from .test_runner_cli import create_parser, main as cli_main


class GamingTestRunner(GamingTestRunnerCore):
    """V2-compliant gaming test runner using modularized components."""
    
    def __init__(self, config=None):
        """Initialize the gaming test runner using core functionality."""
        super().__init__(config)


async def main():
    """Main entry point for backward compatibility."""
    await cli_main()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
