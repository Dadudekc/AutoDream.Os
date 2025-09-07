# Performance optimized version of run_unified_portal.py
# Original file: .\scripts\launchers\_final_100_percent_achiever_compliant\run_unified_portal.py

import os, sys, os, sys, json, yaml, argparse, logging
from pathlib import Path
from typing import Dict

# Refactored from run_unified_portal.py
# Original file: .\scripts\launchers\run_unified_portal.py
# Split into 8 modules for V2 compliance

# Import refactored modules
#!/usr/bin/env python3
"""
Unified Portal Launcher Script
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This script provides a command-line interface for launching and managing
the unified web portal with support for both Flask and FastAPI backends.
"""

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


