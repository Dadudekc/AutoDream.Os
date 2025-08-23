"""
Portfolio Management Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides comprehensive portfolio management, optimization, and tracking capabilities.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PortfolioPosition:
    """Individual portfolio position data"""

    symbol: str
    quantity: float
    avg_price: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
    sector: str = ""
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        self.update_pnl()

    def update_pnl(self):
        """Update P&L calculations"""
        self.market_value = self.quantity * self.current_price
        self.unrealized_pnl = self.market_value - (self.quantity * self.avg_price)
        if self.avg_price > 0:
            self.unrealized_pnl_pct = (
                self.unrealized_pnl / (self.quantity * self.avg_price)
            ) * 100


@dataclass
class PortfolioMetrics:
    """Portfolio performance metrics"""

    total_value: float
    total_cost: float
    total_pnl: float
    total_pnl_pct: float
    daily_pnl: float
    daily_pnl_pct: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    beta: float
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class PortfolioManager:
    """Advanced portfolio management and optimization system"""

    def __init__(
        self, portfolio_name: str = "default", data_dir: str = "portfolio_data"
    ):
        self.portfolio_name = portfolio_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.positions: Dict[str, PortfolioPosition] = {}
        self.metrics: PortfolioMetrics = None
        self.portfolio_file = self.data_dir / f"{portfolio_name}_portfolio.json"
        self.history_file = self.data_dir / f"{portfolio_name}_history.json"

        self.load_portfolio()
        self.calculate_metrics()

    def add_position(
        self, symbol: str, quantity: float, price: float, sector: str = ""
    ) -> bool:
        """Add or update portfolio position"""
        try:
            if symbol in self.positions:
                # Update existing position
                pos = self.positions[symbol]
                total_quantity = pos.quantity + quantity
                total_cost = (pos.quantity * pos.avg_price) + (quantity * price)
                new_avg_price = total_cost / total_quantity

                pos.quantity = total_quantity
                pos.avg_price = new_avg_price
                pos.sector = sector or pos.sector
            else:
                # Create new position
                self.positions[symbol] = PortfolioPosition(
                    symbol=symbol,
                    quantity=quantity,
                    avg_price=price,
                    current_price=price,
                    sector=sector,
                )

            self.save_portfolio()
            self.calculate_metrics()
            logger.info(f"Position updated: {symbol} - Qty: {quantity}, Price: {price}")
            return True

        except Exception as e:
            logger.error(f"Error adding position {symbol}: {e}")
            return False

    def remove_position(self, symbol: str, quantity: float = None) -> bool:
        """Remove or reduce position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"Position {symbol} not found")
                return False

            pos = self.positions[symbol]

            if quantity is None or quantity >= pos.quantity:
                # Remove entire position
                del self.positions[symbol]
                logger.info(f"Position removed: {symbol}")
            else:
                # Reduce position
                pos.quantity -= quantity
                logger.info(f"Position reduced: {symbol} by {quantity}")

            self.save_portfolio()
            self.calculate_metrics()
            return True

        except Exception as e:
            logger.error(f"Error removing position {symbol}: {e}")
            return False

    def update_prices(self, price_updates: Dict[str, float]) -> None:
        """Update current prices for positions"""
        try:
            for symbol, price in price_updates.items():
                if symbol in self.positions:
                    self.positions[symbol].current_price = price
                    self.positions[symbol].update_pnl()

            self.calculate_metrics()
            logger.info(f"Updated prices for {len(price_updates)} symbols")

        except Exception as e:
            logger.error(f"Error updating prices: {e}")

    def calculate_metrics(self) -> PortfolioMetrics:
        """Calculate comprehensive portfolio metrics"""
        try:
            if not self.positions:
                self.metrics = PortfolioMetrics(
                    total_value=0,
                    total_cost=0,
                    total_pnl=0,
                    total_pnl_pct=0,
                    daily_pnl=0,
                    daily_pnl_pct=0,
                    sharpe_ratio=0,
                    max_drawdown=0,
                    volatility=0,
                    beta=1.0,
                )
                return self.metrics

            total_value = sum(pos.market_value for pos in self.positions.values())
            total_cost = sum(
                pos.quantity * pos.avg_price for pos in self.positions.values()
            )
            total_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())

            total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0

            # Calculate sector allocation
            sector_allocation = self.get_sector_allocation()

            # Calculate risk metrics (simplified)
            volatility = self.calculate_volatility()
            beta = self.calculate_beta()
            sharpe_ratio = self.calculate_sharpe_ratio()
            max_drawdown = self.calculate_max_drawdown()

            self.metrics = PortfolioMetrics(
                total_value=total_value,
                total_cost=total_cost,
                total_pnl=total_pnl,
                total_pnl_pct=total_pnl_pct,
                daily_pnl=0,  # Would need historical data for daily P&L
                daily_pnl_pct=0,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                volatility=volatility,
                beta=beta,
            )

            return self.metrics

        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return None

    def get_sector_allocation(self) -> Dict[str, float]:
        """Get portfolio sector allocation"""
        sector_values = {}
        total_value = sum(pos.market_value for pos in self.positions.values())

        for pos in self.positions.values():
            sector = pos.sector or "Unknown"
            if sector not in sector_values:
                sector_values[sector] = 0
            sector_values[sector] += pos.market_value

        # Convert to percentages
        if total_value > 0:
            sector_allocation = {
                sector: (value / total_value) * 100
                for sector, value in sector_values.items()
            }
        else:
            sector_allocation = {}

        return sector_allocation

    def calculate_volatility(self) -> float:
        """Calculate portfolio volatility (simplified)"""
        # This is a simplified calculation - real implementation would use historical returns
        if len(self.positions) < 2:
            return 0.0

        # Use position weights and assume correlation of 0.5 for simplicity
        weights = [
            pos.market_value / self.metrics.total_value
            for pos in self.positions.values()
        ]
        return (
            np.sqrt(np.sum(np.array(weights) ** 2)) * 0.15
        )  # Assume 15% individual volatility

    def calculate_beta(self) -> float:
        """Calculate portfolio beta (simplified)"""
        # Simplified beta calculation - real implementation would use market data
        if not self.positions:
            return 1.0

        # Assume average beta of 1.0 for simplicity
        return 1.0

    def calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio (simplified)"""
        # Simplified calculation - real implementation would use historical returns and risk-free rate
        if self.metrics and self.metrics.volatility > 0:
            return (
                self.metrics.total_pnl_pct - 2.0
            ) / self.metrics.volatility  # Assume 2% risk-free rate
        return 0.0

    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown (simplified)"""
        # Simplified calculation - real implementation would use historical data
        if self.metrics and self.metrics.total_pnl_pct < 0:
            return abs(self.metrics.total_pnl_pct)
        return 0.0

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        try:
            return {
                "portfolio_name": self.portfolio_name,
                "total_positions": len(self.positions),
                "total_value": self.metrics.total_value if self.metrics else 0.0,
                "total_cost": self.metrics.total_cost if self.metrics else 0.0,
                "total_pnl": self.metrics.total_pnl if self.metrics else 0.0,
                "total_pnl_pct": self.metrics.total_pnl_pct if self.metrics else 0.0,
                "positions": {
                    symbol: asdict(pos) for symbol, pos in self.positions.items()
                },
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}

    def get_portfolio(self) -> Dict[str, Any]:
        """Get portfolio data for unified API integration"""
        try:
            return {
                "portfolio_name": self.portfolio_name,
                "positions": {
                    symbol: asdict(pos) for symbol, pos in self.positions.items()
                },
                "metrics": asdict(self.metrics) if self.metrics else {},
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting portfolio: {e}")
            return {}

    def get_top_positions(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get top positions by market value"""
        sorted_positions = sorted(
            self.positions.values(), key=lambda x: x.market_value, reverse=True
        )

        return [asdict(pos) for pos in sorted_positions[:count]]

    def save_portfolio(self) -> None:
        """Save portfolio to persistent storage"""
        try:
            portfolio_data = {
                "portfolio_name": self.portfolio_name,
                "positions": {
                    symbol: asdict(pos) for symbol, pos in self.positions.items()
                },
                "last_saved": datetime.now().isoformat(),
            }

            with open(self.portfolio_file, "w") as f:
                json.dump(portfolio_data, f, indent=2, default=str)

            logger.info(f"Portfolio saved to {self.portfolio_file}")

        except Exception as e:
            logger.error(f"Error saving portfolio: {e}")

    def load_portfolio(self) -> None:
        """Load portfolio from persistent storage"""
        try:
            if self.portfolio_file.exists():
                with open(self.portfolio_file, "r") as f:
                    portfolio_data = json.load(f)

                # Load positions
                for symbol, pos_data in portfolio_data.get("positions", {}).items():
                    # Convert string datetime back to datetime object
                    if "last_updated" in pos_data:
                        pos_data["last_updated"] = datetime.fromisoformat(
                            pos_data["last_updated"]
                        )

                    self.positions[symbol] = PortfolioPosition(**pos_data)

                logger.info(f"Portfolio loaded from {self.portfolio_file}")
            else:
                logger.info("No existing portfolio found, starting fresh")

        except Exception as e:
            logger.error(f"Error loading portfolio: {e}")
            logger.info("Starting with empty portfolio")

    def export_to_csv(self, filename: str = None) -> str:
        """Export portfolio to CSV format"""
        try:
            if filename is None:
                filename = f"{self.portfolio_name}_portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            filepath = self.data_dir / filename

            # Prepare data for export
            export_data = []
            for pos in self.positions.values():
                export_data.append(
                    {
                        "Symbol": pos.symbol,
                        "Quantity": pos.quantity,
                        "Avg_Price": pos.avg_price,
                        "Current_Price": pos.current_price,
                        "Market_Value": pos.market_value,
                        "Unrealized_PnL": pos.unrealized_pnl,
                        "Unrealized_PnL_Pct": pos.unrealized_pnl_pct,
                        "Sector": pos.sector,
                        "Last_Updated": pos.last_updated,
                    }
                )

            df = pd.DataFrame(export_data)
            df.to_csv(filepath, index=False)

            logger.info(f"Portfolio exported to {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error exporting portfolio: {e}")
            return ""


# Example usage and testing
if __name__ == "__main__":
    # Create portfolio manager
    pm = PortfolioManager("test_portfolio")

    # Add some test positions
    pm.add_position("AAPL", 100, 150.0, "Technology")
    pm.add_position("MSFT", 50, 300.0, "Technology")
    pm.add_position("JPM", 200, 140.0, "Financial")

    # Update prices
    pm.update_prices({"AAPL": 155.0, "MSFT": 310.0, "JPM": 145.0})

    # Get summary
    summary = pm.get_portfolio_summary()
    print("Portfolio Summary:")
    print(json.dumps(summary, indent=2))

    # Export to CSV
    csv_file = pm.export_to_csv()
    print(f"\nPortfolio exported to: {csv_file}")
