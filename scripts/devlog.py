#!/usr/bin/env python3
"""
Devlog Wrapper Script - Agent Cellphone V2
==========================================

Simple wrapper script for agents to create and manage devlogs.
Uses the existing devlog CLI system and existing architecture.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def main():
    """Main entry point for devlog wrapper"""
    try:
        from src.core.devlog_cli import DevlogCLI
        
        # Create CLI instance and run
        cli = DevlogCLI()
        return cli.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the project root directory")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
