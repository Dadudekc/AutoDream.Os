#!/usr/bin/env python3
"""
V2 Compliance Analysis CLI Tool - Wrapper
=========================================

Simple wrapper for the modular V2 compliance analysis tool.

This file maintains backward compatibility while using the new modular structure.
"""
<<<<<<< HEAD

=======
from __future__ import annotations
import logging
import ast
>>>>>>> origin/agent-3-v2-infrastructure-optimization
import sys
from pathlib import Path
<<<<<<< HEAD
=======
from typing import Dict, Any, Tuple
>>>>>>> origin/agent-3-v2-infrastructure-optimization

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Import and run the main CLI
from analysis.cli import main

if __name__ == "__main__":
    sys.exit(main())