#!/usr/bin/env python3
"""
Triple-Check Protocols - V2 Compliance Wrapper
=============================================

V2 compliant wrapper for the modular check protocol system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/triple_check_protocols.py --competitive-mode
"""

import asyncio
import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from check_protocols.protocol_coordinator import ProtocolCoordinator


async def main():
    """Main entry point for triple-check protocols."""
    project_root = Path(".")
    coordinator = ProtocolCoordinator(project_root)

    # Run in competitive mode
    results = await coordinator.run_competitive_mode()

    # Print summary
    coordinator.print_summary(results)

    # Save results
    results_path = coordinator.save_results(results)
    print(f"\n📄 Results saved to: {results_path}")


if __name__ == "__main__":
    asyncio.run(main())
