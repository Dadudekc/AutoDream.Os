"""
Options Trading Automation Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides options chain analysis, strategy execution, and automated options trading.
Now uses modular architecture for better maintainability.
"""

import asyncio
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
import math

# Import the new modular components
from .options import (
    OptionsPricingEngine,
    OptionsRiskManager,
    OptionsStrategyEngine,
    OptionsMarketDataManager,
    OptionType,
    OptionStrategy,
    Greeks,
    OptionContract,
    OptionsChain,
    OptionsStrategy as Strategy,
    RiskMetrics
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptionsTradingService:
    """Advanced options trading and automation service using modular architecture"""

    def __init__(self, market_data_service=None, data_dir: str = "options_trading"):
        self.market_data_service = market_data_service
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(f"{__name__}.OptionsTradingService")

        # Initialize modular components
        self.pricing_engine = OptionsPricingEngine()
        self.risk_manager = OptionsRiskManager()
        self.strategy_engine = OptionsStrategyEngine()
        self.market_data_manager = OptionsMarketDataManager(data_dir)

        # Strategy tracking
        self.active_strategies: List[Strategy] = []
        self.strategy_performance: Dict[OptionStrategy, Dict[str, Any]] = {}

        # Data files
        self.strategies_file = self.data_dir / "active_strategies.json"
        self.performance_file = self.data_dir / "strategy_performance.json"

        # Load existing data
        self.load_data()

    def calculate_black_scholes(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: OptionType,
    ) -> Dict[str, float]:
        """Calculate Black-Scholes option pricing and Greeks using pricing engine"""
        return self.pricing_engine.calculate_black_scholes(S, K, T, r, sigma, option_type)

    def calculate_implied_volatility(
        self,
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: OptionType,
    ) -> float:
        """Calculate implied volatility using pricing engine"""
        return self.pricing_engine.calculate_implied_volatility(market_price, S, K, T, r, option_type)

    def create_long_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        premium: float,
        quantity: int = 1,
    ) -> Strategy:
        """Create a long call strategy using strategy engine"""
        return self.strategy_engine.create_long_call_strategy(symbol, strike, expiration, premium, quantity)

    def create_covered_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        premium: float,
        underlying_quantity: int = 100,
    ) -> Strategy:
        """Create a covered call strategy using strategy engine"""
        return self.strategy_engine.create_covered_call_strategy(symbol, strike, expiration, premium, underlying_quantity)

    def create_iron_condor_strategy(
        self,
        symbol: str,
        short_call_strike: float,
        long_call_strike: float,
        short_put_strike: float,
        long_put_strike: float,
        expiration: datetime,
        call_premium: float,
        put_premium: float,
        quantity: int = 1,
    ) -> Strategy:
        """Create an iron condor strategy using strategy engine"""
        return self.strategy_engine.create_iron_condor_strategy(
            symbol, short_call_strike, long_call_strike, short_put_strike, long_put_strike,
            expiration, call_premium, put_premium, quantity
        )

    def validate_strategy(
        self,
        strategy: Strategy,
        portfolio_value: float,
        underlying_price: float,
    ) -> Dict[str, Any]:
        """Validate strategy using strategy engine"""
        return self.strategy_engine.validate_strategy(strategy, portfolio_value, underlying_price)

    def calculate_strategy_payoff(
        self,
        strategy: Strategy,
        underlying_price: float,
    ) -> Dict[str, float]:
        """Calculate strategy payoff using strategy engine"""
        return self.strategy_engine.calculate_strategy_payoff(strategy, underlying_price)

    def get_strategy_summary(
        self,
        strategy: Strategy,
        underlying_price: float,
    ) -> Dict[str, Any]:
        """Get strategy summary using strategy engine"""
        return self.strategy_engine.get_strategy_summary(strategy, underlying_price)

    def calculate_position_risk(
        self,
        contracts: List[Dict[str, Any]],
        underlying_price: float,
        portfolio_value: float,
    ) -> RiskMetrics:
        """Calculate position risk using risk manager"""
        return self.risk_manager.calculate_position_risk(contracts, underlying_price, portfolio_value)

    def check_risk_limits(
        self,
        risk_metrics: RiskMetrics,
        portfolio_value: float,
    ) -> Dict[str, bool]:
        """Check risk limits using risk manager"""
        return self.risk_manager.check_risk_limits(risk_metrics, portfolio_value)

    def get_risk_summary(
        self,
        risk_metrics: RiskMetrics,
        portfolio_value: float,
    ) -> Dict[str, Any]:
        """Get risk summary using risk manager"""
        return self.risk_manager.get_risk_summary(risk_metrics, portfolio_value)

    def update_options_chain(
        self,
        symbol: str,
        chain_data: Dict[str, Any],
    ) -> bool:
        """Update options chain using market data manager"""
        return self.market_data_manager.update_options_chain(symbol, chain_data)

    def get_options_chain(self, symbol: str) -> Optional[OptionsChain]:
        """Get options chain using market data manager"""
        return self.market_data_manager.get_options_chain(symbol)

    def get_atm_options(
        self,
        symbol: str,
        expiration: datetime = None,
    ) -> Tuple[Optional[OptionContract], Optional[OptionContract]]:
        """Get at-the-money options using market data manager"""
        return self.market_data_manager.get_atm_options(symbol, expiration)

    def get_implied_volatility_smile(
        self,
        symbol: str,
        expiration: datetime = None,
    ) -> Dict[str, List[float]]:
        """Get implied volatility smile using market data manager"""
        return self.market_data_manager.get_implied_volatility_smile(symbol, expiration)

    def add_strategy(self, strategy: Strategy):
        """Add a new trading strategy"""
        try:
            self.active_strategies.append(strategy)
            self.logger.info(f"Added {strategy.strategy_type.value} strategy for {strategy.symbol}")
            self.save_data()
        except Exception as e:
            self.logger.error(f"Error adding strategy: {e}")

    def remove_strategy(self, strategy_id: str):
        """Remove a trading strategy"""
        try:
            self.active_strategies = [s for s in self.active_strategies if s.timestamp.isoformat() != strategy_id]
            self.logger.info(f"Removed strategy {strategy_id}")
            self.save_data()
        except Exception as e:
            self.logger.error(f"Error removing strategy: {e}")

    def get_all_strategies(self) -> List[Strategy]:
        """Get all active strategies"""
        return self.active_strategies

    def get_strategy_by_symbol(self, symbol: str) -> List[Strategy]:
        """Get strategies for a specific symbol"""
        return [s for s in self.active_strategies if s.symbol == symbol]

    def update_strategy_performance(self, strategy: Strategy, performance_data: Dict[str, Any]):
        """Update strategy performance metrics"""
        try:
            strategy_type = strategy.strategy_type.value
            if strategy_type not in self.strategy_performance:
                self.strategy_performance[strategy_type] = {}
            
            self.strategy_performance[strategy_type].update(performance_data)
            self.logger.info(f"Updated performance for {strategy_type} strategy")
            self.save_data()
        except Exception as e:
            self.logger.error(f"Error updating strategy performance: {e}")

    def get_strategy_performance(self, strategy_type: OptionStrategy = None) -> Dict[str, Any]:
        """Get strategy performance data"""
        if strategy_type:
            return self.strategy_performance.get(strategy_type.value, {})
        return self.strategy_performance

    def save_data(self):
        """Save all data to files"""
        try:
            # Save strategies
            strategies_data = []
            for strategy in self.active_strategies:
                strategy_dict = {
                    "strategy_type": strategy.strategy_type.value,
                    "symbol": strategy.symbol,
                    "contracts": strategy.contracts,
                    "entry_price": strategy.entry_price,
                    "max_profit": strategy.max_profit,
                    "max_loss": strategy.max_loss,
                    "break_even_points": strategy.break_even_points,
                    "probability_profit": strategy.probability_profit,
                    "risk_reward_ratio": strategy.risk_reward_ratio,
                    "greeks_exposure": strategy.greeks_exposure,
                    "timestamp": strategy.timestamp.isoformat(),
                }
                strategies_data.append(strategy_dict)
            
            with open(self.strategies_file, 'w') as f:
                json.dump(strategies_data, f, indent=2)
            
            # Save performance data
            with open(self.performance_file, 'w') as f:
                json.dump(self.strategy_performance, f, indent=2)
            
            # Save market data
            self.market_data_manager.save_data()
            
            self.logger.info("Saved all options trading data")
            
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")

    def load_data(self):
        """Load data from files"""
        try:
            # Load strategies
            if self.strategies_file.exists():
                with open(self.strategies_file, 'r') as f:
                    strategies_data = json.load(f)
                
                for strategy_data in strategies_data:
                    try:
                        # Reconstruct strategy object
                        strategy = Strategy(
                            strategy_type=OptionStrategy(strategy_data["strategy_type"]),
                            symbol=strategy_data["symbol"],
                            contracts=strategy_data["contracts"],
                            entry_price=strategy_data["entry_price"],
                            max_profit=strategy_data["max_profit"],
                            max_loss=strategy_data["max_loss"],
                            break_even_points=strategy_data["break_even_points"],
                            probability_profit=strategy_data["probability_profit"],
                            risk_reward_ratio=strategy_data["risk_reward_ratio"],
                            greeks_exposure=strategy_data["greeks_exposure"],
                            timestamp=datetime.fromisoformat(strategy_data["timestamp"]),
                        )
                        self.active_strategies.append(strategy)
                    except Exception as e:
                        self.logger.error(f"Error loading strategy: {e}")
            
            # Load performance data
            if self.performance_file.exists():
                with open(self.performance_file, 'r') as f:
                    self.strategy_performance = json.load(f)
            
            # Load market data
            self.market_data_manager.load_data()
            
            self.logger.info("Loaded all options trading data")
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")

    def get_service_summary(self) -> Dict[str, Any]:
        """Get comprehensive service summary"""
        try:
            return {
                "total_strategies": len(self.active_strategies),
                "strategy_types": list(set(s.strategy_type.value for s in self.active_strategies)),
                "symbols": list(set(s.symbol for s in self.active_strategies)),
                "total_performance_metrics": len(self.strategy_performance),
                "market_data_summary": self.market_data_manager.get_data_summary(),
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error generating service summary: {e}")
            return {}
