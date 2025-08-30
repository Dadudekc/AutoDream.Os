#!/usr/bin/env python3
"""
Simple entry point for the messaging system
Fixes module path issues by running from the correct directory
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Now import and run the messaging CLI
try:
    from src.services.messaging.cli_interface import MessagingCLI
    
    def main():
        """Main entry point for the messaging service"""
        try:
            cli = MessagingCLI()
            success = cli.run()
            sys.exit(0 if success else 1)
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Current Python path:")
    for path in sys.path:
        print(f"  {path}")
    sys.exit(1)
