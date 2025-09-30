"""
Tesla Trading Robot Main
V2 Compliant main entry point
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tsla_forecast_app.trading_robot_core import TradingRobot
from tsla_forecast_app.trading_strategies import MovingAverageStrategy, RSITradingStrategy


def main():
    """Main entry point"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Initialize trading robot
    robot = TradingRobot("TSLA")
    
    # Add strategies
    robot.add_strategy(MovingAverageStrategy(20, 50))
    robot.add_strategy(RSITradingStrategy(14, 30, 70))
    
    logger.info("Tesla Trading Robot initialized")
    logger.info(f"Portfolio summary: {robot.get_portfolio_summary()}")
    logger.info(f"Performance metrics: {robot.get_performance_metrics()}")
    
    # In a real implementation, this would run the trading loop
    logger.info("Trading robot ready for operation")


if __name__ == "__main__":
    main()
