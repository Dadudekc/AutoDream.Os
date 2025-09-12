#!/usr/bin/env python3
"""
Alpaca Trading Robot - Main Entry Point
"""
import asyncio
import signal
import sys
from pathlib import Path

from loguru import logger

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import config
from core.trading_engine import TradingEngine
from web.dashboard import TradingDashboard


class TradingRobot:
    """Main Trading Robot Application"""

    def __init__(self):
        self.trading_engine = None
        self.dashboard = None
        self.running = False

    async def initialize(self):
        """Initialize the trading robot components"""
        try:
            logger.info("🚀 Initializing Alpaca Trading Robot...")

            # Initialize trading engine
            self.trading_engine = TradingEngine()
            await self.trading_engine.initialize()

            # Initialize web dashboard if enabled
            if config.enable_dashboard:
                self.dashboard = TradingDashboard(self.trading_engine)
                await self.dashboard.start()

            logger.info("✅ Trading Robot initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize trading robot: {e}")
            raise

    async def start(self):
        """Start the trading robot"""
        try:
            logger.info("🎯 Starting Alpaca Trading Robot...")

            # Start trading engine
            await self.trading_engine.start()

            self.running = True
            logger.info("🎯 Trading Robot started successfully")

            # Keep running until stopped
            while self.running:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"❌ Error during trading robot operation: {e}")
            await self.stop()

    async def stop(self):
        """Stop the trading robot"""
        try:
            logger.info("🛑 Stopping Alpaca Trading Robot...")

            self.running = False

            # Stop trading engine
            if self.trading_engine:
                await self.trading_engine.stop()

            # Stop dashboard
            if self.dashboard:
                await self.dashboard.stop()

            logger.info("✅ Trading Robot stopped successfully")

        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")


async def main():
    """Main entry point"""
    # Setup signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        robot.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize and start trading robot
    robot = TradingRobot()

    try:
        await robot.initialize()
        await robot.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await robot.stop()


if __name__ == "__main__":
    # Setup logging
    logger.add(
        config.log_file,
        rotation="1 day",
        retention="30 days",
        level=config.log_level
    )

    # Run the trading robot
    asyncio.run(main())

    print()  # Line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡🔥")  # Completion indicator
