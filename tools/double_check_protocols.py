import logging

logger = logging.getLogger(__name__)
"""
Double-Check Protocols - V2 Compliance Wrapper
=============================================

V2 compliant wrapper for the modular check protocol system.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Usage: python tools/double_check_protocols.py
"""
import asyncio
import sys
from pathlib import Path

tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))
from check_protocols.protocol_coordinator import ProtocolCoordinator


async def main():
    """Main entry point for double-check protocols."""
    project_root = Path(".")
    coordinator = ProtocolCoordinator(project_root)
    results = await coordinator.execute_protocols()
    coordinator.print_summary(results)
    results_path = coordinator.save_results(results)
    logger.info(f"\n📄 Results saved to: {results_path}")


if __name__ == "__main__":
    asyncio.run(main())
