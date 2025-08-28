#!/usr/bin/env python3
import sys
from pathlib import Path

BASE_PATH = Path(__file__).parent
sys.path.extend([
    str(BASE_PATH / "src"),
    str(BASE_PATH / "agent_workspaces" / "Agent-7"),
])

from contract_cleanup_validator import CleanupCLI

if __name__ == "__main__":
    cli = CleanupCLI()
    cli.run(sys.argv[1:])
