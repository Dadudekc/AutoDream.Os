#!/usr/bin/env python3
"""
Tesla Trading Robot - Launcher
==============================

Quick launcher for the advanced Tesla Trading Robot.

Author: Agent-1 (Trading Systems Specialist)
License: MIT
"""

import sys
import subprocess
import os
from pathlib import Path

def install_requirements():
    """Install trading robot requirements."""
    print("📦 Installing Trading Robot requirements...")
    try:
        requirements_file = Path(__file__).parent / "requirements_trading.txt"
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_trading_robot():
    """Run the Tesla Trading Robot."""
    print("🤖 Starting Tesla Trading Robot...")
    try:
        robot_file = Path(__file__).parent / "trading_robot.py"
        subprocess.run([sys.executable, str(robot_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run trading robot: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Trading Robot stopped by user")

def main():
    """Main launcher function."""
    print("🤖 TESLA TRADING ROBOT - ADVANCED TRADING SYSTEM")
    print("=" * 60)
    print("🐝 WE. ARE. SWARM. - Professional Trading Automation")
    print("=" * 60)
    
    print("\n🎯 Trading Robot Features:")
    print("   • Real-time Tesla stock data from multiple APIs")
    print("   • 3 Advanced Trading Strategies:")
    print("     - Moving Average Crossover")
    print("     - RSI Mean Reversion")
    print("     - Bollinger Bands")
    print("   • Automated trade execution")
    print("   • Risk management system")
    print("   • Portfolio tracking and P&L")
    print("   • Manual trading controls")
    print("   • Backtesting capabilities")
    print("   • Professional PyQt5 interface")
    
    print("\n📊 Trading Strategies:")
    print("   • Moving Average Crossover: Buy when short MA > long MA")
    print("   • RSI Mean Reversion: Buy when RSI < 30, Sell when RSI > 70")
    print("   • Bollinger Bands: Buy at lower band, Sell at upper band")
    
    print("\n🛡️ Risk Management:")
    print("   • Position size limits (max 10% of portfolio)")
    print("   • Stop loss protection (5% default)")
    print("   • Take profit targets (10% default)")
    print("   • Daily loss limits (2% default)")
    
    print("\n💰 Portfolio Features:")
    print("   • Real-time portfolio valuation")
    print("   • P&L tracking and performance metrics")
    print("   • Trade history and logging")
    print("   • Cash and shares management")
    
    print("\n🔧 Technical Features:")
    print("   • Multi-threaded data fetching")
    print("   • Real-time strategy analysis")
    print("   • Automated trade execution")
    print("   • Professional dark theme UI")
    print("   • Comprehensive logging system")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Exiting.")
        return
    
    print("\n⚠️  IMPORTANT DISCLAIMERS:")
    print("   • This is a DEMO trading robot for educational purposes")
    print("   • Use at your own risk - past performance doesn't guarantee future results")
    print("   • Always test strategies with paper trading first")
    print("   • Consider your risk tolerance before using real money")
    print("   • The robot uses mock data by default for safety")
    
    print("\n🎉 Ready to launch the Trading Robot!")
    print("   The robot will start in a new window...")
    print("   Press Ctrl+C to stop the robot")
    
    # Run the trading robot
    run_trading_robot()

if __name__ == "__main__":
    main()



