"""
Consolidated_Messaging Module

This module provides script functionality for the swarm system.

Component Type: Script
Priority: Medium
Dependencies: src.services.messaging


EXAMPLE USAGE:
==============

# Run the script directly
python consolidated_messaging.py --input-file data.json --output-dir ./results

# Or import and use programmatically
from scripts.consolidated_messaging import main

# Execute with custom arguments
import sys
sys.argv = ['script', '--verbose', '--config', 'config.json']
main()

# Advanced usage with custom configuration
from scripts.consolidated_messaging import ScriptRunner

runner = ScriptRunner(config_file='custom_config.json')
runner.execute_all_operations()

"""
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
