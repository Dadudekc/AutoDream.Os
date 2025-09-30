#!/usr/bin/env python3
"""
Test Discord Commander Message Formatting
==========================================

Test script to verify that A2A messages are properly formatted and displayed.
"""

import sys
from pathlib import Path
from test_message_formatting_core import test_message_formatting

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    success = test_message_formatting()
    sys.exit(0 if success else 1)
