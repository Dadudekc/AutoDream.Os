#!/usr/bin/env python3
"""
Thea Consultation Launcher
=========================
Quick launcher for Thea strategic consultation system.
V2 Compliant: ≤400 lines, focused launcher functionality

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    # Run the CLI using subprocess
    import subprocess

    thea_dir = project_root / "src" / "services" / "thea"
    cli_script = thea_dir / "strategic_consultation_cli.py"

    # Pass through all command line arguments
    cmd = [sys.executable, str(cli_script)] + sys.argv[1:]

    try:
        sys.exit(subprocess.run(cmd, cwd=str(thea_dir)).returncode)
    except Exception as e:
        print(f"❌ Error running Thea consultation: {e}")
        sys.exit(1)
