#!/usr/bin/env python3
"""
Agent Devlog Posting Service
============================

Main entry point for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused CLI interface
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.services.agent_devlog.cli import main

if __name__ == "__main__":
    asyncio.run(main())
