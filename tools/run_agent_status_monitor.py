#!/usr/bin/env python3
"""
Agent Status Monitor Runner
==========================

Starts the agent status monitor in daemon mode.

Usage:
    python tools/run_agent_status_monitor.py        # Default 10-minute intervals
    python tools/run_agent_status_monitor.py --interval 5  # 5-minute intervals
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run agent status monitor in daemon mode."""
    # Get arguments
    interval = 10
    timeout = 10
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interval":
        interval = int(sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3] == "--timeout":
        timeout = int(sys.argv[4])
    
    print(f"🔍 Starting Agent Status Monitor")
    print(f"   Check interval: {interval} minutes")
    print(f"   Timeout threshold: {timeout} minutes")
    print(f"   Press Ctrl+C to stop")
    print("="*80)
    
    # Run monitor
    cmd = [
        sys.executable,
        "tools/agent_status_monitor.py",
        "--daemon",
        "--interval", str(interval),
        "--timeout", str(timeout)
    ]
    
    subprocess.run(cmd)


if __name__ == "__main__":
    main()

