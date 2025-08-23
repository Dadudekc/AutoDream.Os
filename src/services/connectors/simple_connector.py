#!/usr/bin/env python3
"""Simple connector for the integration framework."""

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Log a message indicating the connector is operational."""
    logger.info("Simple Connector - Integration Framework Extension Working!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
