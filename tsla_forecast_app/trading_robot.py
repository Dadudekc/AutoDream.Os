#!/usr/bin/env python3
"""
Tesla Trading Robot - Legacy Entry Point
======================================

Legacy entry point for Tesla Trading Robot.
Use trading_robot_main.py for the new V2-compliant version.

This file is maintained for backward compatibility only.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import sys
from trading_robot_main import main

if __name__ == "__main__":
    print("⚠️  Using legacy entry point. Consider using trading_robot_main.py")
    main()