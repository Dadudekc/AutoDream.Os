"""
Options Trading Automation Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides options chain analysis, strategy execution, and automated options trading.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptionType(Enum):
    """Option types"""

    CALL = "CALL"
    PUT = "PUT"


class OptionStrategy(Enum):
    """Options trading strategies"""

    LONG_CALL = "LONG_CALL"
    LONG_PUT = "LONG_PUT"
    COVERED_CALL = "COVERED_CALL"
    PROTECTIVE_PUT = "PROTECTIVE_PUT"
    BULL_SPREAD = "BULL_SPREAD"
    BEAR_SPREAD = "BEAR_SPREAD"
    IRON_CONDOR = "IRON_CONDOR"
    BUTTERFLY = "BUTTERFLY"
    STRANGLE = "STRANGLE"
    STRADDLE = "STRADDLE"


class Greeks(Enum):
    """Option Greeks"""

    DELTA = "DELTA"
    GAMMA = "GAMMA"
    THETA = "THETA"
    VEGA = "VEGA"
    RHO = "RHO"


@dataclass
class OptionContract:
    """Individual option contract data"""

    symbol: str
    strike: float
    expiration: datetime
    option_type: OptionType
    last_price: float
    bid: float
    ask: float
    volume: int
    open_interest: int
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    underlying_price: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @property
    def mid_price(self) -> float:
        """Calculate mid price"""
        return (self.bid + self.ask) / 2

    @property
    def bid_ask_spread(self) -> float:
        """Calculate bid-ask spread"""
        return self.ask - self.bid

    @property
    def time_to_expiration(self) -> float:
        """Calculate time to expiration in years"""
        return (self.expiration - datetime.now()).days / 365.25


@dataclass
class OptionsChain:
    """Complete options chain for a symbol"""

    symbol: str
    underlying_price: float
    expiration_dates: List[datetime]
    call_options: Dict[float, OptionContract]
    put_options: Dict[float, OptionContract]
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()

    def get_atm_options(
        self, expiration: datetime = None
    ) -> Tuple[Optional[OptionContract], Optional[OptionContract]]:
        """Get at-the-money call and put options"""
        if expiration is None:
            expiration = min(self.expiration_dates)

        # Find closest strike to underlying price
        strikes = list(self.call_options.keys())
        if not strikes:
            return None, None

        atm_strike = min(strikes, key=lambda x: abs(x - self.underlying_price))

        call = self.call_options.get(atm_strike)
        put = self.put_options.get(atm_strike)

        return call, put

    def get_implied_volatility_smile(
        self, expiration: datetime = None
    ) -> Dict[str, List[float]]:
        """Get implied volatility smile data"""
        if expiration is None:
            expiration = min(self.expiration_dates)

        strikes = []
        call_ivs = []
        put_ivs = []

        for strike in sorted(self.call_options.keys()):
            if strike in self.call_options and strike in self.put_options:
                call = self.call_options[strike]
                put = self.put_options[strike]

                if call.expiration == expiration and put.expiration == expiration:
                    strikes.append(strike)
                    call_ivs.append(call.implied_volatility)
                    put_ivs.append(put.implied_volatility)

        return {"strikes": strikes, "call_ivs": call_ivs, "put_ivs": put_ivs}


@dataclass
class OptionsStrategy:
    """Options trading strategy"""

    strategy_type: OptionStrategy
    symbol: str
    contracts: List[OptionContract]
    entry_price: float
    max_profit: float
    max_loss: float
    break_even_points: List[float]
    probability_profit: float
    risk_reward_ratio: float
    greeks_exposure: Dict[str, float]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class OptionsTradingService:
    """Advanced options trading and automation service"""

    def __init__(self, market_data_service=None, data_dir: str = "options_trading"):
        self.market_data_service = market_data_service
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.options_chains: Dict[str, OptionsChain] = {}
        self.active_strategies: List[OptionsStrategy] = []
        self.strategy_performance: Dict[OptionStrategy, Dict[str, Any]] = {}

        self.chains_file = self.data_dir / "options_chains.json"
        self.strategies_file = self.data_dir / "active_strategies.json"
        self.performance_file = self.data_dir / "strategy_performance.json"

        # Strategy parameters
        self.strategy_params = {
            OptionStrategy.LONG_CALL: {
                "max_capital_risk": 0.02,  # 2% of portfolio
                "min_delta": 0.3,
                "max_theta": -0.05,
            },
            OptionStrategy.COVERED_CALL: {
                "min_premium": 0.02,  # 2% of underlying
                "max_delta": -0.3,
                "min_days_to_expiry": 30,
            },
            OptionStrategy.IRON_CONDOR: {
                "max_width": 0.1,  # 10% of underlying
                "min_premium": 0.01,  # 1% of underlying
                "max_risk": 0.05,  # 5% of portfolio
            },
        }

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
        """Calculate Black-Scholes option pricing and Greeks"""
        try:
            # Black-Scholes formula
            d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            if option_type == OptionType.CALL:
                price = S * self.normal_cdf(d1) - K * np.exp(-r * T) * self.normal_cdf(
                    d2
                )
                delta = self.normal_cdf(d1)
            else:  # PUT
                price = K * np.exp(-r * T) * self.normal_cdf(-d2) - S * self.normal_cdf(
                    -d1
                )
                delta = self.normal_cdf(d1) - 1

            # Greeks
            gamma = self.normal_pdf(d1) / (S * sigma * np.sqrt(T))
            theta = (-S * sigma * self.normal_pdf(d1)) / (
                2 * np.sqrt(T)
            ) - r * K * np.exp(-r * T) * self.normal_cdf(d2)
            vega = S * np.sqrt(T) * self.normal_pdf(d1)
            rho = K * T * np.exp(-r * T) * self.normal_cdf(d2)

            return {
                "price": price,
                "delta": delta,
                "gamma": gamma,
                "theta": theta,
                "vega": vega,
                "rho": rho,
            }

        except Exception as e:
            logger.error(f"Error calculating Black-Scholes: {e}")
            return {}

    def normal_cdf(self, x: float) -> float:
        """Standard normal cumulative distribution function"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def normal_pdf(self, x: float) -> float:
        """Standard normal probability density function"""
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)

    def calculate_implied_volatility(
        self,
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: OptionType,
    ) -> float:
        """Calculate implied volatility using Newton-Raphson method"""
        try:
            sigma = 0.5  # Initial guess
            tolerance = 1e-5
            max_iterations = 100

            for i in range(max_iterations):
                price = self.calculate_black_scholes(
                    S, K, T, r, sigma, option_type
                ).get("price", 0)
                vega = self.calculate_black_scholes(S, K, T, r, sigma, option_type).get(
                    "vega", 0
                )

                if abs(price - market_price) < tolerance:
                    return sigma

                if abs(vega) < 1e-10:
                    break

                sigma = sigma - (price - market_price) / vega
                sigma = max(0.001, min(5.0, sigma))  # Bounds

            return sigma

        except Exception as e:
            logger.error(f"Error calculating implied volatility: {e}")
            return 0.0

    def analyze_options_chain(
        self, symbol: str, expiration: datetime = None
    ) -> Optional[OptionsChain]:
        """Analyze options chain for opportunities"""
        try:
            if symbol not in self.options_chains:
                logger.warning(f"Options chain not found for {symbol}")
                return None

            chain = self.options_chains[symbol]

            if expiration is None:
                expiration = min(chain.expiration_dates)

            # Get ATM options
            atm_call, atm_put = chain.get_atm_options(expiration)
            if not atm_call or not atm_put:
                return None

            # Analyze volatility skew
            iv_smile = chain.get_implied_volatility_smile(expiration)

            # Find opportunities
            opportunities = []

            # 1. Volatility arbitrage
            if atm_call.implied_volatility != atm_put.implied_volatility:
                opportunities.append(
                    {
                        "type": "Volatility Arbitrage",
                        "description": f"Call IV: {atm_call.implied_volatility:.3f}, Put IV: {atm_put.implied_volatility:.3f}",
                        "action": "Consider straddle or strangle if IV difference > 0.05",
                    }
                )

            # 2. High IV opportunities
            if atm_call.implied_volatility > 0.5:  # 50% IV
                opportunities.append(
                    {
                        "type": "High IV Opportunity",
                        "description": f"High implied volatility: {atm_call.implied_volatility:.1%}",
                        "action": "Consider selling premium strategies",
                    }
                )

            # 3. Low IV opportunities
            if atm_call.implied_volatility < 0.2:  # 20% IV
                opportunities.append(
                    {
                        "type": "Low IV Opportunity",
                        "description": f"Low implied volatility: {atm_call.implied_volatility:.1%}",
                        "action": "Consider buying options or volatility strategies",
                    }
                )

            # 4. Time decay analysis
            if atm_call.time_to_expiration < 30 / 365.25:  # Less than 30 days
                opportunities.append(
                    {
                        "type": "Time Decay",
                        "description": f"High theta: {atm_call.theta:.4f}",
                        "action": "Consider selling short-term options",
                    }
                )

            return {
                "chain": chain,
                "opportunities": opportunities,
                "atm_call": atm_call,
                "atm_put": atm_put,
                "iv_smile": iv_smile,
            }

        except Exception as e:
            logger.error(f"Error analyzing options chain: {e}")
            return None

    def create_long_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        underlying_price: float,
        option_price: float,
    ) -> Optional[OptionsStrategy]:
        """Create long call strategy"""
        try:
            # Calculate strategy metrics
            max_loss = option_price
            max_profit = float("inf")  # Unlimited upside
            break_even = strike + option_price

            # Calculate probability of profit (simplified)
            # Using normal distribution assumption
            time_to_expiry = (expiration - datetime.now()).days / 365.25
            if time_to_expiry > 0:
                volatility = 0.3  # Assume 30% volatility
                d2 = (
                    np.log(underlying_price / strike)
                    + (0.02 - 0.5 * volatility**2) * time_to_expiry
                ) / (volatility * np.sqrt(time_to_expiry))
                probability_profit = 1 - self.normal_cdf(d2)
            else:
                probability_profit = 0.5

            # Risk-reward ratio
            risk_reward_ratio = max_profit / max_loss if max_loss > 0 else 0

            # Greeks exposure
            greeks_exposure = {
                "delta": 1.0,  # Long call has positive delta
                "gamma": 1.0,  # Long call has positive gamma
                "theta": -1.0,  # Long call has negative theta
                "vega": 1.0,  # Long call has positive vega
            }

            # Create option contract
            option_contract = OptionContract(
                symbol=symbol,
                strike=strike,
                expiration=expiration,
                option_type=OptionType.CALL,
                last_price=option_price,
                bid=option_price * 0.95,
                ask=option_price * 1.05,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=0.6,
                gamma=0.02,
                theta=-0.05,
                vega=0.1,
                rho=0.01,
                underlying_price=underlying_price,
            )

            strategy = OptionsStrategy(
                strategy_type=OptionStrategy.LONG_CALL,
                symbol=symbol,
                contracts=[option_contract],
                entry_price=option_price,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[break_even],
                probability_profit=probability_profit,
                risk_reward_ratio=risk_reward_ratio,
                greeks_exposure=greeks_exposure,
            )

            return strategy

        except Exception as e:
            logger.error(f"Error creating long call strategy: {e}")
            return None

    def create_covered_call_strategy(
        self,
        symbol: str,
        strike: float,
        expiration: datetime,
        underlying_price: float,
        option_price: float,
        shares_owned: int = 100,
    ) -> Optional[OptionsStrategy]:
        """Create covered call strategy"""
        try:
            # Calculate strategy metrics
            max_profit = (strike - underlying_price + option_price) * shares_owned
            max_loss = (underlying_price - option_price) * shares_owned
            break_even = underlying_price - option_price

            # Probability of profit (simplified)
            if strike > underlying_price:
                probability_profit = 0.6  # Higher probability when OTM
            else:
                probability_profit = 0.4  # Lower probability when ITM

            # Risk-reward ratio
            risk_reward_ratio = max_profit / abs(max_loss) if max_loss < 0 else 0

            # Greeks exposure
            greeks_exposure = {
                "delta": 0.4,  # Reduced delta due to short call
                "gamma": -0.02,  # Negative gamma from short call
                "theta": 0.05,  # Positive theta from short call
                "vega": -0.1,  # Negative vega from short call
            }

            # Create option contract
            option_contract = OptionContract(
                symbol=symbol,
                strike=strike,
                expiration=expiration,
                option_type=OptionType.CALL,
                last_price=option_price,
                bid=option_price * 0.95,
                ask=option_price * 1.05,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=0.6,
                gamma=0.02,
                theta=-0.05,
                vega=0.1,
                rho=0.01,
                underlying_price=underlying_price,
            )

            strategy = OptionsStrategy(
                strategy_type=OptionStrategy.COVERED_CALL,
                symbol=symbol,
                contracts=[option_contract],
                entry_price=option_price,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[break_even],
                probability_profit=probability_profit,
                risk_reward_ratio=risk_reward_ratio,
                greeks_exposure=greeks_exposure,
            )

            return strategy

        except Exception as e:
            logger.error(f"Error creating covered call strategy: {e}")
            return None

    def create_iron_condor_strategy(
        self,
        symbol: str,
        short_call_strike: float,
        long_call_strike: float,
        short_put_strike: float,
        long_put_strike: float,
        expiration: datetime,
        underlying_price: float,
        net_premium: float,
    ) -> Optional[OptionsStrategy]:
        """Create iron condor strategy"""
        try:
            # Validate strikes
            if not (
                long_put_strike
                < short_put_strike
                < underlying_price
                < short_call_strike
                < long_call_strike
            ):
                raise ValueError("Invalid strike order for iron condor")

            # Calculate strategy metrics
            max_profit = net_premium
            max_loss = (short_call_strike - long_call_strike) - net_premium

            # Break-even points
            break_even_upper = short_call_strike + net_premium
            break_even_lower = short_put_strike - net_premium

            # Probability of profit (simplified)
            # Iron condor profits when underlying stays between short strikes
            width = short_call_strike - short_put_strike
            probability_profit = 0.7  # High probability for defined risk strategy

            # Risk-reward ratio
            risk_reward_ratio = max_profit / abs(max_loss) if max_loss < 0 else 0

            # Greeks exposure (neutral strategy)
            greeks_exposure = {
                "delta": 0.0,  # Neutral delta
                "gamma": -0.01,  # Negative gamma
                "theta": 0.03,  # Positive theta
                "vega": -0.05,  # Negative vega
            }

            # Create option contracts
            contracts = []

            # Short call
            short_call = OptionContract(
                symbol=symbol,
                strike=short_call_strike,
                expiration=expiration,
                option_type=OptionType.CALL,
                last_price=0.02,
                bid=0.015,
                ask=0.025,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=0.3,
                gamma=0.02,
                theta=-0.02,
                vega=0.05,
                rho=0.01,
                underlying_price=underlying_price,
            )
            contracts.append(short_call)

            # Long call
            long_call = OptionContract(
                symbol=symbol,
                strike=long_call_strike,
                expiration=expiration,
                option_type=OptionType.CALL,
                last_price=0.01,
                bid=0.008,
                ask=0.012,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=0.1,
                gamma=0.01,
                theta=-0.01,
                vega=0.02,
                rho=0.005,
                underlying_price=underlying_price,
            )
            contracts.append(long_call)

            # Short put
            short_put = OptionContract(
                symbol=symbol,
                strike=short_put_strike,
                expiration=expiration,
                option_type=OptionType.PUT,
                last_price=0.02,
                bid=0.015,
                ask=0.025,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=-0.3,
                gamma=0.02,
                theta=-0.02,
                vega=0.05,
                rho=-0.01,
                underlying_price=underlying_price,
            )
            contracts.append(short_put)

            # Long put
            long_put = OptionContract(
                symbol=symbol,
                strike=long_put_strike,
                expiration=expiration,
                option_type=OptionType.PUT,
                last_price=0.01,
                bid=0.008,
                ask=0.012,
                volume=100,
                open_interest=1000,
                implied_volatility=0.3,
                delta=-0.1,
                gamma=0.01,
                theta=-0.01,
                vega=0.02,
                rho=-0.005,
                underlying_price=underlying_price,
            )
            contracts.append(long_put)

            strategy = OptionsStrategy(
                strategy_type=OptionStrategy.IRON_CONDOR,
                symbol=symbol,
                contracts=contracts,
                entry_price=net_premium,
                max_profit=max_profit,
                max_loss=max_loss,
                break_even_points=[break_even_lower, break_even_upper],
                probability_profit=probability_profit,
                risk_reward_ratio=risk_reward_ratio,
                greeks_exposure=greeks_exposure,
            )

            return strategy

        except Exception as e:
            logger.error(f"Error creating iron condor strategy: {e}")
            return None

    def scan_for_opportunities(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """Scan for options trading opportunities"""
        try:
            opportunities = []

            for symbol in symbols:
                # Analyze options chain
                analysis = self.analyze_options_chain(symbol)
                if not analysis:
                    continue

                chain = analysis["chain"]
                atm_call = analysis["atm_call"]
                atm_put = analysis["atm_put"]

                # Strategy recommendations
                recommendations = []

                # 1. Long call for bullish outlook
                if atm_call and atm_call.implied_volatility < 0.3:
                    long_call_strategy = self.create_long_call_strategy(
                        symbol,
                        atm_call.strike,
                        atm_call.expiration,
                        chain.underlying_price,
                        atm_call.mid_price,
                    )
                    if long_call_strategy:
                        recommendations.append(
                            {
                                "strategy": long_call_strategy,
                                "reason": "Low IV, bullish outlook",
                                "risk_level": "MODERATE",
                            }
                        )

                # 2. Covered call for income
                if atm_call and atm_call.implied_volatility > 0.25:
                    covered_call_strategy = self.create_covered_call_strategy(
                        symbol,
                        atm_call.strike,
                        atm_call.expiration,
                        chain.underlying_price,
                        atm_call.mid_price,
                    )
                    if covered_call_strategy:
                        recommendations.append(
                            {
                                "strategy": covered_call_strategy,
                                "reason": "High IV, income generation",
                                "risk_level": "LOW",
                            }
                        )

                # 3. Iron condor for range-bound markets
                if len(chain.expiration_dates) > 0:
                    expiration = min(chain.expiration_dates)
                    strikes = sorted(chain.call_options.keys())
                    if len(strikes) >= 4:
                        # Find suitable strikes for iron condor
                        mid_strikes = [
                            s
                            for s in strikes
                            if 0.8 * chain.underlying_price
                            < s
                            < 1.2 * chain.underlying_price
                        ]
                        if len(mid_strikes) >= 4:
                            short_call = mid_strikes[len(mid_strikes) // 2]
                            long_call = short_call + (short_call * 0.05)  # 5% above
                            short_put = mid_strikes[len(mid_strikes) // 2 - 1]
                            long_put = short_put - (short_put * 0.05)  # 5% below

                            iron_condor = self.create_iron_condor_strategy(
                                symbol,
                                short_call,
                                long_call,
                                short_put,
                                long_put,
                                expiration,
                                chain.underlying_price,
                                0.02,
                            )
                            if iron_condor:
                                recommendations.append(
                                    {
                                        "strategy": iron_condor,
                                        "reason": "Range-bound market, defined risk",
                                        "risk_level": "MODERATE",
                                    }
                                )

                if recommendations:
                    opportunities.append(
                        {
                            "symbol": symbol,
                            "underlying_price": chain.underlying_price,
                            "analysis": analysis,
                            "recommendations": recommendations,
                        }
                    )

            return opportunities

        except Exception as e:
            logger.error(f"Error scanning for opportunities: {e}")
            return []

    def execute_strategy(self, strategy: OptionsStrategy) -> bool:
        """Execute options trading strategy"""
        try:
            # Validate strategy
            if not strategy.contracts:
                logger.error("Strategy has no contracts")
                return False

            # Check risk limits
            if strategy.max_loss > 0.05:  # 5% max loss
                logger.warning(f"Strategy exceeds risk limit: {strategy.max_loss:.2%}")
                return False

            # Add to active strategies
            self.active_strategies.append(strategy)

            # Update performance tracking
            if strategy.strategy_type not in self.strategy_performance:
                self.strategy_performance[strategy.strategy_type] = {
                    "total_trades": 0,
                    "winning_trades": 0,
                    "total_pnl": 0.0,
                    "max_drawdown": 0.0,
                }

            self.strategy_performance[strategy.strategy_type]["total_trades"] += 1

            # Save data
            self.save_data()

            logger.info(
                f"Strategy executed: {strategy.strategy_type.value} for {strategy.symbol}"
            )
            return True

        except Exception as e:
            logger.error(f"Error executing strategy: {e}")
            return False

    def monitor_strategies(self) -> List[Dict[str, Any]]:
        """Monitor active strategies"""
        try:
            updates = []

            for strategy in self.active_strategies:
                # Check expiration
                if strategy.contracts[0].expiration <= datetime.now():
                    updates.append(
                        {
                            "strategy_id": id(strategy),
                            "action": "EXPIRED",
                            "message": "Strategy has expired",
                        }
                    )
                    continue

                # Check profit targets and stop losses
                current_underlying_price = strategy.contracts[0].underlying_price

                for break_even in strategy.break_even_points:
                    if strategy.strategy_type in [
                        OptionStrategy.LONG_CALL,
                        OptionStrategy.LONG_PUT,
                    ]:
                        # Long strategies
                        if current_underlying_price > break_even * 1.05:  # 5% profit
                            updates.append(
                                {
                                    "strategy_id": id(strategy),
                                    "action": "PROFIT_TARGET",
                                    "message": f"Profit target reached: {current_underlying_price:.2f}",
                                }
                            )
                        elif current_underlying_price < break_even * 0.95:  # 5% loss
                            updates.append(
                                {
                                    "strategy_id": id(strategy),
                                    "action": "STOP_LOSS",
                                    "message": f"Stop loss triggered: {current_underlying_price:.2f}",
                                }
                            )

                # Check Greeks exposure
                if abs(strategy.greeks_exposure.get("delta", 0)) > 0.8:
                    updates.append(
                        {
                            "strategy_id": id(strategy),
                            "action": "GREEKS_WARNING",
                            "message": f"High delta exposure: {strategy.greeks_exposure['delta']:.2f}",
                        }
                    )

            return updates

        except Exception as e:
            logger.error(f"Error monitoring strategies: {e}")
            return []

    def save_data(self):
        """Save options trading data"""
        try:
            # Save options chains
            chains_data = {}
            for symbol, chain in self.options_chains.items():
                chains_data[symbol] = asdict(chain)

            with open(self.chains_file, "w") as f:
                json.dump(chains_data, f, indent=2, default=str)

            # Save active strategies
            strategies_data = [asdict(strategy) for strategy in self.active_strategies]
            with open(self.strategies_file, "w") as f:
                json.dump(strategies_data, f, indent=2, default=str)

            # Save performance data
            with open(self.performance_file, "w") as f:
                json.dump(self.strategy_performance, f, indent=2, default=str)

            logger.info("Options trading data saved successfully")

        except Exception as e:
            logger.error(f"Error saving options trading data: {e}")

    def load_data(self):
        """Load options trading data"""
        try:
            # Load options chains
            if self.chains_file.exists():
                with open(self.chains_file, "r") as f:
                    chains_data = json.load(f)

                for symbol, chain_data in chains_data.items():
                    # Convert datetime strings back to datetime objects
                    if "last_updated" in chain_data:
                        chain_data["last_updated"] = datetime.fromisoformat(
                            chain_data["last_updated"]
                        )

                    # Convert expiration dates
                    if "expiration_dates" in chain_data:
                        chain_data["expiration_dates"] = [
                            datetime.fromisoformat(exp)
                            for exp in chain_data["expiration_dates"]
                        ]

                    # Convert option contracts
                    if "call_options" in chain_data:
                        for strike, contract_data in chain_data["call_options"].items():
                            if "timestamp" in contract_data:
                                contract_data["timestamp"] = datetime.fromisoformat(
                                    contract_data["timestamp"]
                                )
                            if "expiration" in contract_data:
                                contract_data["expiration"] = datetime.fromisoformat(
                                    contract_data["expiration"]
                                )

                    if "put_options" in chain_data:
                        for strike, contract_data in chain_data["put_options"].items():
                            if "timestamp" in contract_data:
                                contract_data["timestamp"] = datetime.fromisoformat(
                                    contract_data["timestamp"]
                                )
                            if "expiration" in contract_data:
                                contract_data["expiration"] = datetime.fromisoformat(
                                    contract_data["expiration"]
                                )

                logger.info(f"Loaded {len(chains_data)} options chains")

            # Load active strategies
            if self.strategies_file.exists():
                with open(self.strategies_file, "r") as f:
                    strategies_data = json.load(f)

                for strategy_data in strategies_data:
                    if "timestamp" in strategy_data:
                        strategy_data["timestamp"] = datetime.fromisoformat(
                            strategy_data["timestamp"]
                        )

                    # Convert contracts
                    if "contracts" in strategy_data:
                        for contract_data in strategy_data["contracts"]:
                            if "timestamp" in contract_data:
                                contract_data["timestamp"] = datetime.fromisoformat(
                                    contract_data["timestamp"]
                                )
                            if "expiration" in contract_data:
                                contract_data["expiration"] = datetime.fromisoformat(
                                    contract_data["expiration"]
                                )

                logger.info(f"Loaded {len(strategies_data)} active strategies")

        except Exception as e:
            logger.error(f"Error loading options trading data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create options trading service
    ots = OptionsTradingService()

    # Test Black-Scholes calculation
    bs_result = ots.calculate_black_scholes(100, 100, 0.25, 0.02, 0.3, OptionType.CALL)
    print("Black-Scholes Result:", bs_result)

    # Test implied volatility calculation
    iv = ots.calculate_implied_volatility(5.0, 100, 100, 0.25, 0.02, OptionType.CALL)
    print("Implied Volatility:", f"{iv:.3f}")

    # Test strategy creation
    long_call = ots.create_long_call_strategy(
        "AAPL", 150, datetime.now() + timedelta(days=30), 155, 8.0
    )
    if long_call:
        print("Long Call Strategy:", asdict(long_call))

    print("Options Trading Service initialized successfully")
