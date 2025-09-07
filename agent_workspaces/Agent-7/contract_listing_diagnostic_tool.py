#!/usr/bin/env python3
"""
Contract Listing Diagnostic Tool - Agent-7 Enhancement
====================================================

Diagnoses contract listing discrepancies and synchronization issues.
Part of the contract claiming enhancement system.

Author: Agent-7 - Quality Completion Optimization Manager
"""

import json
import subprocess
import sys
from datetime import datetime

def diagnose_contract_listing():
    """Diagnose contract listing issues"""
    print("CONTRACT LISTING DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Get stats
    stats_result = subprocess.run([
        sys.executable,
        "agent_workspaces/meeting/contract_claiming_system.py",
        "--stats"
    ], capture_output=True, text=True, timeout=10)
    
    if stats_result.returncode == 0:
        print("OK Stats command successful")
        print(f"Output: {stats_result.stdout.strip()}")
    else:
        print("ERROR Stats command failed")
        print(f"Error: {stats_result.stderr.strip()}")
    
    # Get listing
    list_result = subprocess.run([
        sys.executable,
        "agent_workspaces/meeting/contract_claiming_system.py",
        "--list"
    ], capture_output=True, text=True, timeout=10)
    
    if list_result.returncode == 0:
        print("OK Listing command successful")
        print(f"Output: {list_result.stdout.strip()}")
    else:
        print("ERROR Listing command failed")
        print(f"Error: {list_result.stderr.strip()}")
    
    print(f"\nDiagnostic completed at: {datetime.now()}")

if __name__ == "__main__":
    diagnose_contract_listing()
