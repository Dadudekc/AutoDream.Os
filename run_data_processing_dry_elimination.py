#!/usr/bin/env python3
"""
Data Processing DRY Elimination Runner
=====================================

Executes the data processing DRY elimination system for Agent-5.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.core.data_processing_dry_eliminator import main

if __name__ == "__main__":
    main()
