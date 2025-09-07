#!/usr/bin/env python3
"""
CLI Entry Point for V2 Message Delivery Service
Replaces the old monolith file CLI functionality
"""

import sys
import os

from src.utils.stability_improvements import stability_manager, safe_import

# Add the services directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from cli_interface import main

if __name__ == "__main__":
    exit(main())

