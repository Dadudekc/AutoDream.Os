#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to Python path
script_dir = Path(__file__).parent.parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from src.services.messaging.cli import main

if __name__ == "__main__":
    main()
