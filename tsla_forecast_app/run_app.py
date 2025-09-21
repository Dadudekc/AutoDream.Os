#!/usr/bin/env python3
"""
Tesla Stock Forecast App - Quick Launcher
========================================

Quick launcher for the PyQt5 Tesla Stock Forecast App.

Author: Agent-1 (Backend API & Data Integration)
License: MIT
"""

import sys
import subprocess
import os
from pathlib import Path

def install_requirements():
    """Install PyQt5 requirements."""
    print("📦 Installing PyQt5 requirements...")
    try:
        requirements_file = Path(__file__).parent / "requirements_pyqt5.txt"
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_app():
    """Run the Tesla Stock Forecast App."""
    print("🚀 Starting Tesla Stock Forecast App...")
    try:
        app_file = Path(__file__).parent / "tesla_stock_app.py"
        subprocess.run([sys.executable, str(app_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")

def main():
    """Main launcher function."""
    print("🚀 TESLA STOCK FORECAST APP - PYQT5 VERSION")
    print("=" * 50)
    print("🐝 WE. ARE. SWARM. - Fast PyQt5 Development")
    print("=" * 50)
    
    print("\n🎯 App Features:")
    print("   • Real-time Tesla stock data (mock data)")
    print("   • Interactive dashboard with live updates")
    print("   • Price forecasting with confidence levels")
    print("   • Technical analysis indicators")
    print("   • ASCII charts and data visualization")
    print("   • Dark theme with Tesla branding")
    print("   • Fast PyQt5 desktop application")
    
    print("\n📊 App Tabs:")
    print("   • Dashboard - Current price and company info")
    print("   • Charts - Historical price charts")
    print("   • Forecast - Price predictions")
    print("   • Technical - RSI, MACD, Bollinger Bands")
    
    print("\n🔧 Technical Details:")
    print("   • PyQt5 desktop application")
    print("   • Multi-threaded data updates")
    print("   • Mock data generation")
    print("   • Real-time UI updates")
    print("   • Professional dark theme")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Exiting.")
        return
    
    print("\n🎉 Ready to launch!")
    print("   The app will start in a new window...")
    print("   Press Ctrl+C to stop the app")
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main()



