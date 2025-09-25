#!/usr/bin/env python3
"""
Workflow CLI Entry Point
========================

Command-line interface for the modular workflow system.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.workflow.manager import main

if __name__ == "__main__":
    main()
