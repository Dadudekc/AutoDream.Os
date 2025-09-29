#!/usr/bin/env python3
"""
Tests Package - Comprehensive Test Suite
========================================

Comprehensive test suite for the Agent Cellphone V2 project.
Provides full test coverage for all messaging and Discord integration functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"

# Test categories
TEST_CATEGORIES = [
    "messaging_integration",
    "discord_bot_integration",
    "coordinate_loader",
    "messaging_service",
]

# Test coverage targets
COVERAGE_TARGETS = {
    "messaging_integration": 95,
    "discord_bot_integration": 90,
    "coordinate_loader": 98,
    "messaging_service": 95,
}

# Test requirements
TEST_REQUIREMENTS = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "pytest-asyncio>=0.21.0",
]
