#!/usr/bin/env python3
"""
Tesla Stock Forecast App - PyQt5 Desktop Application
===================================================

REFACTORED: Now uses modular design with focused components
V2 Compliant: ≤400 lines, imports from modules package

This file now serves as the main entry point and maintains backward compatibility
while delegating to the modular modules package.

Fast desktop application for Tesla stock forecasting with PyQt5.
Simple, fast, and effective for rapid prototyping.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""


from dotenv import load_dotenv

from .modules import main

# Load environment variables from .env file
load_dotenv()

# Re-export for backward compatibility
__all__ = ["main"]

if __name__ == "__main__":
    main()
