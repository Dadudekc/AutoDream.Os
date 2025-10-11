#!/usr/bin/env python3
"""
Tesla Stock App - Legacy Entry Point
===================================

Legacy entry point for Tesla Stock Forecast App.
Use tesla_stock_app_main.py for the new V2-compliant version.

This file is maintained for backward compatibility only.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""

import sys
from tesla_stock_app_main import main

if __name__ == "__main__":
    print("⚠️  Using legacy entry point. Consider using tesla_stock_app_main.py")
    main()