#!/usr/bin/env python3
"""Integration test for connector modules using logging."""

import logging
import sys
from importlib import import_module
from pathlib import Path

logger = logging.getLogger(__name__)

CONNECTORS = [
    "simple_connector",
    "rest_api_connector",
    "discord_connector",
    "file_system_connector",
    "auth_connector",
    "monitoring_connector",
]


def main() -> None:
    """Run all connector modules and log their output."""
    logging.basicConfig(level=logging.INFO)
    connector_path = Path(__file__).resolve().parent
    sys.path.append(str(connector_path))

    logger.info("=== INTEGRATION FRAMEWORK EXTENSION TEST ===")
    logger.info("Testing all connectors in the integration framework...")

    for name in CONNECTORS:
        logger.info("Testing %s...", name)
        module = import_module(name)
        try:
            module.run()
            logger.info("  ✅ %s: Success", name)
        except Exception:  # pragma: no cover - error path logging
            logger.exception("  ❌ %s: Failed", name)

    logger.info("\n=== INTEGRATION TEST COMPLETE ===")


if __name__ == "__main__":
    main()
