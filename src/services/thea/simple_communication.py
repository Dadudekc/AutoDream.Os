#!/usr/bin/env python3
"""
Simple Thea Communication - Main Interface
==========================================

Main interface for Thea/ChatGPT communication system.
V2 Compliant: ≤100 lines, imports from modular components.

Features:
- Automated login detection and cookie persistence
- Selenium WebDriver integration
- Manual fallback modes
- Response detection and capture
- Comprehensive logging and analysis

Usage:
    from src.services.thea.simple_communication import SimpleTheaCommunication

    comm = SimpleTheaCommunication(username="user@example.com", password="password")
    comm.run_communication_cycle("Hello Thea!")
"""

# Import main components from modular files
from .communication_core import SimpleTheaCommunication, main

# Re-export main class for backward compatibility
__all__ = [
    "SimpleTheaCommunication",
    "main",
]


if __name__ == "__main__":
    import sys
    sys.exit(main())