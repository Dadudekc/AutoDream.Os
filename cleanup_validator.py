#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))
from core.task_management.contract_cleanup_validator import CleanupCLI
if __name__ == "__main__":
    cli = CleanupCLI()
