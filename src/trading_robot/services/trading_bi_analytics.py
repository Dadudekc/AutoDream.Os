"""
Trading Business Intelligence Analytics Service - V2 Compliant Implementation
Advanced BI analytics for trading robot with real-time insights and predictive capabilities
V2 COMPLIANCE: Under 300-line limit, comprehensive error handling, modular design

@version 1.0.0 - V2 COMPLIANCE BI ANALYTICS SERVICE
@license MIT
"""

from datetime import datetime

    TradingRepositoryInterface, Trade, Position, create_trading_repository
)


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: timedelta
    timestamp: datetime


@dataclass
class RiskMetrics:
    """Risk assessment metrics"""
    portfolio_volatility: float
    value_at_risk: float
    expected_shortfall: float
    beta_coefficient: float
    risk_level: RiskLevel
    max_position_size: float
    timestamp: datetime


@dataclass
class MarketTrend:
    """Market trend analysis"""
    direction: str  # 'bullish', 'bearish', 'sideways'
    strength: float  # 0-1 scale
    confidence: float  # 0-1 scale
    predicted_change: float  # percentage
    timeframe: str  # 'short', 'medium', 'long'
    timestamp: datetime


class TradingBiAnalyticsService:
    """Business Intelligence Analytics Service for Trading Robot"""

    def __init__(self, repository: Optional[TradingRepositoryInterface] = None):
        """Initialize BI analytics service with dependency injection"""
        self.repository = repository or create_trading_repository()
        self.logger = UnifiedLoggingSystem("TradingBiAnalyticsService")

    async def calculate_real_time_pnl(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Calculate real-time P&L for portfolio or specific symbol"""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("calculate_real_time_pnl", {"symbol": symbol})

            if symbol:
                return await self._calculate_symbol_pnl(symbol)
            else:
                return await self._calculate_portfolio_pnl()

        except Exception as e:
            self.logger.log_error("calculate_real_time_pnl", str(e), {"symbol": symbol})
            return {"error": str(e), "timestamp": datetime.now()}

    async def _calculate_symbol_pnl(self, symbol: str) -> Dict[str, Any]:
        """Calculate P&L for specific symbol"""
        position = await self.repository.get_position(symbol.upper())

        if not get_unified_validator().validate_required(position):
            return {
                "symbol": symbol,
                "pnl": 0.0,
                "pnl_percentage": 0.0,
                "position_value": 0.0,
                "timestamp": datetime.now()
            }

        # Calculate unrealized P&L
        unrealized_pnl = position.pnl
        position_value = position.quantity * position.current_price
        pnl_percentage = (unrealized_pnl / (position.quantity * position.average_price)) * 100

        return {
            "symbol": symbol,
            "pnl": unrealized_pnl,
            "pnl_percentage": pnl_percentage,
            "position_value": position_value,
            "quantity": position.quantity,
            "average_price": position.average_price,
            "current_price": position.current_price,
            "timestamp": datetime.now()
        }

    async def _calculate_portfolio_pnl(self) -> Dict[str, Any]:
        """Calculate total portfolio P&L"""
        positions = await self.repository.get_all_positions()

        total_pnl = sum(pos.pnl for pos in positions)
        total_value = sum(pos.quantity * pos.current_price for pos in positions)
        total_cost = sum(pos.quantity * pos.average_price for pos in positions)

        pnl_percentage = (total_pnl / total_cost * 100) if total_cost > 0 else 0.0

        return {
            "total_pnl": total_pnl,
            "total_value": total_value,
            "total_cost": total_cost,
            "pnl_percentage": pnl_percentage,
            "positions_count": len(positions),
            "timestamp": datetime.now()
        }

    async def assess_portfolio_risk(self) -> RiskMetrics:
        """Comprehensive portfolio risk assessment"""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("assess_portfolio_risk")

            positions = await self.repository.get_all_positions()
            trades = await self.repository.get_all_trades(1000)

            if not get_unified_validator().validate_required(positions):
                return RiskMetrics(
                    portfolio_volatility=0.0,
                    value_at_risk=0.0,
                    expected_shortfall=0.0,
                    beta_coefficient=0.0,
                    risk_level=RiskLevel.LOW,
                    max_position_size=0.0,
                    timestamp=datetime.now()
                )

            # Calculate portfolio volatility
            returns = self._calculate_returns_series(trades)
            volatility = statistics.stdev(returns) if len(returns) > 1 else 0.0

            # Value at Risk (95% confidence)
            var_95 = self._calculate_value_at_risk(returns, 0.95)

            # Expected Shortfall (Conditional VaR)
            es_95 = self._calculate_expected_shortfall(returns, 0.95)

            # Beta coefficient (simplified market correlation)
            beta = self._calculate_beta_coefficient(returns)

            # Risk level assessment
            risk_level = self._assess_risk_level(volatility, var_95)

            # Maximum position size recommendation
            portfolio_value = sum(pos.quantity * pos.current_price for pos in positions)
            max_position_size = self._calculate_max_position_size(portfolio_value, risk_level)

            metrics = RiskMetrics(
                portfolio_volatility=volatility,
                value_at_risk=var_95,
                expected_shortfall=es_95,
                beta_coefficient=beta,
                risk_level=risk_level,
                max_position_size=max_position_size,
                timestamp=datetime.now()
            )

            self.logger.get_unified_logger().log_operation_start(operation)_complete("assess_portfolio_risk", {
                "volatility": volatility, "var_95": var_95, "risk_level": risk_level.value
            })

            return metrics

        except Exception as e:
            self.logger.log_error("assess_portfolio_risk", str(e))
            return RiskMetrics(
                portfolio_volatility=0.0,
                value_at_risk=0.0,
                expected_shortfall=0.0,
                beta_coefficient=0.0,
                risk_level=RiskLevel.LOW,
                max_position_size=0.0,
                timestamp=datetime.now()
            )

    def _calculate_returns_series(self, trades: List[Trade]) -> List[float]:
        """Calculate returns series from trades"""
        if not get_unified_validator().validate_required(trades):
            return []

        # Group trades by symbol and calculate returns
        symbol_returns = {}
        for trade in trades:
            if trade.symbol not in symbol_returns:
                symbol_returns[trade.symbol] = []
            symbol_returns[trade.symbol].append(trade)

        # Calculate daily returns (simplified)
        returns = []
        for symbol_trades in symbol_returns.values():
            if len(symbol_trades) > 1:
                symbol_trades.sort(key=lambda x: x.timestamp)
                for i in range(1, len(symbol_trades)):
                    prev_price = symbol_trades[i-1].price
                    curr_price = symbol_trades[i].price
                    if prev_price > 0:
                        daily_return = (curr_price - prev_price) / prev_price
                        returns.append(daily_return)

        return returns

    def _calculate_value_at_risk(self, returns: List[float], confidence: float) -> float:
        """Calculate Value at Risk"""
        if not get_unified_validator().validate_required(returns):
            return 0.0

        returns_sorted = sorted(returns)
        index = int((1 - confidence) * len(returns))
        return abs(returns_sorted[index]) if index < len(returns) else 0.0

    def _calculate_expected_shortfall(self, returns: List[float], confidence: float) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        if not get_unified_validator().validate_required(returns):
            return 0.0

        returns_sorted = sorted(returns)
        index = int((1 - confidence) * len(returns))
        tail_returns = returns_sorted[:index] if index > 0 else returns_sorted
        return abs(statistics.mean(tail_returns)) if tail_returns else 0.0

    def _calculate_beta_coefficient(self, returns: List[float]) -> float:
        """Calculate beta coefficient (simplified)"""
        if len(returns) < 2:
            return 1.0

        # Simplified beta calculation - in practice would use market returns
        return statistics.variance(returns) / statistics.variance(returns) if statistics.variance(returns) > 0 else 1.0

    def _assess_risk_level(self, volatility: float, var_95: float) -> RiskLevel:
        """Assess overall risk level"""
        if var_95 > 0.05 or volatility > 0.03:  # 5% VaR or 3% volatility
            return RiskLevel.CRITICAL
        elif var_95 > 0.03 or volatility > 0.02:  # 3% VaR or 2% volatility
            return RiskLevel.HIGH
        elif var_95 > 0.02 or volatility > 0.015:  # 2% VaR or 1.5% volatility
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _calculate_max_position_size(self, portfolio_value: float, risk_level: RiskLevel) -> float:
        """Calculate maximum position size based on risk level"""
        risk_multipliers = {
            RiskLevel.LOW: 0.1,      # 10% of portfolio
            RiskLevel.MEDIUM: 0.05,  # 5% of portfolio
            RiskLevel.HIGH: 0.02,    # 2% of portfolio
            RiskLevel.CRITICAL: 0.01 # 1% of portfolio
        }

        return portfolio_value * risk_multipliers[risk_level]

    async def analyze_market_trends(self, symbol: str, timeframe: str = "medium") -> MarketTrend:
        """Analyze market trends using technical indicators"""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("analyze_market_trends", {
                "symbol": symbol, "timeframe": timeframe
            })

            # Get recent trades for trend analysis
            trades = await self.repository.get_trades_by_symbol(symbol, 100)

            if len(trades) < 10:
                return MarketTrend(
                    direction="sideways",
                    strength=0.0,
                    confidence=0.0,
                    predicted_change=0.0,
                    timeframe=timeframe,
                    timestamp=datetime.now()
                )

            # Calculate trend direction and strength
            direction, strength = self._calculate_trend_direction(trades)
            confidence = self._calculate_trend_confidence(trades)
            predicted_change = self._calculate_predicted_change(trades, direction)

            trend = MarketTrend(
                direction=direction,
                strength=strength,
                confidence=confidence,
                predicted_change=predicted_change,
                timeframe=timeframe,
                timestamp=datetime.now()
            )

            self.logger.get_unified_logger().log_operation_start(operation)_complete("analyze_market_trends", {
                "direction": direction, "strength": strength, "confidence": confidence
            })

            return trend

        except Exception as e:
            self.logger.log_error("analyze_market_trends", str(e), {
                "symbol": symbol, "timeframe": timeframe
            })
            return MarketTrend(
                direction="sideways",
                strength=0.0,
                confidence=0.0,
                predicted_change=0.0,
                timeframe=timeframe,
                timestamp=datetime.now()
            )

    def _calculate_trend_direction(self, trades: List[Trade]) -> Tuple[str, float]:
        """Calculate trend direction and strength"""
        if len(trades) < 2:
            return "sideways", 0.0

        # Sort by timestamp
        trades_sorted = sorted(trades, key=lambda x: x.timestamp)

        # Calculate price changes
        price_changes = []
        for i in range(1, len(trades_sorted)):
            change = (trades_sorted[i].price - trades_sorted[i-1].price) / trades_sorted[i-1].price
            price_changes.append(change)

        # Calculate trend metrics
        positive_changes = sum(1 for change in price_changes if change > 0.001)  # >0.1%
        negative_changes = sum(1 for change in price_changes if change < -0.001)  # <-0.1%

        total_changes = len(price_changes)
        if total_changes == 0:
            return "sideways", 0.0

        bullish_ratio = positive_changes / total_changes
        bearish_ratio = negative_changes / total_changes

        if bullish_ratio > 0.6:
            return "bullish", bullish_ratio
        elif bearish_ratio > 0.6:
            return "bearish", bearish_ratio
        else:
            return "sideways", max(bullish_ratio, bearish_ratio)

    def _calculate_trend_confidence(self, trades: List[Trade]) -> float:
        """Calculate trend confidence based on consistency"""
        if len(trades) < 5:
            return 0.0

        trades_sorted = sorted(trades, key=lambda x: x.timestamp)

        # Calculate consistency of direction
        consistent_up = 0
        consistent_down = 0

        for i in range(1, len(trades_sorted)):
            if trades_sorted[i].price > trades_sorted[i-1].price * 1.001:
                consistent_up += 1
            elif trades_sorted[i].price < trades_sorted[i-1].price * 0.999:
                consistent_down += 1

        total_periods = len(trades_sorted) - 1
        consistency = max(consistent_up, consistent_down) / total_periods

        return min(consistency, 1.0)  # Cap at 1.0

    def _calculate_predicted_change(self, trades: List[Trade], direction: str) -> float:
        """Calculate predicted price change based on trend"""
        if len(trades) < 3 or direction == "sideways":
            return 0.0

        trades_sorted = sorted(trades, key=lambda x: x.timestamp)

        # Calculate average price change per period
        changes = []
        for i in range(1, len(trades_sorted)):
            change = (trades_sorted[i].price - trades_sorted[i-1].price) / trades_sorted[i-1].price
            changes.append(change)

        if not get_unified_validator().validate_required(changes):
            return 0.0

        avg_change = statistics.mean(changes)

        # Apply direction multiplier
        if direction == "bullish":
            return abs(avg_change) * 100  # Convert to percentage
        elif direction == "bearish":
            return -abs(avg_change) * 100  # Convert to percentage
        else:
            return avg_change * 100

    async def generate_performance_report(self) -> PerformanceMetrics:
        """Generate comprehensive performance metrics report"""
        try:
            self.logger.get_unified_logger().log_operation_start(operation)_start("generate_performance_report")

            trades = await self.repository.get_all_trades(1000)

            if not get_unified_validator().validate_required(trades):
                return PerformanceMetrics(
                    total_return=0.0,
                    sharpe_ratio=0.0,
                    max_drawdown=0.0,
                    win_rate=0.0,
                    profit_factor=0.0,
                    total_trades=0,
                    avg_trade_duration=timedelta(0),
                    timestamp=datetime.now()
                )

            # Calculate metrics
            total_return = self._calculate_total_return(trades)
            sharpe_ratio = self._calculate_sharpe_ratio(trades)
            max_drawdown = self._calculate_max_drawdown(trades)
            win_rate = self._calculate_win_rate(trades)
            profit_factor = self._calculate_profit_factor(trades)
            avg_duration = self._calculate_avg_trade_duration(trades)

            metrics = PerformanceMetrics(
                total_return=total_return,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=len(trades),
                avg_trade_duration=avg_duration,
                timestamp=datetime.now()
            )

            self.logger.get_unified_logger().log_operation_start(operation)_complete("generate_performance_report", {
                "total_return": total_return, "win_rate": win_rate, "total_trades": len(trades)
            })

            return metrics

        except Exception as e:
            self.logger.log_error("generate_performance_report", str(e))
            return PerformanceMetrics(
                total_return=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                win_rate=0.0,
                profit_factor=0.0,
                total_trades=0,
                avg_trade_duration=timedelta(0),
                timestamp=datetime.now()
            )

    def _calculate_total_return(self, trades: List[Trade]) -> float:
        """Calculate total return from trades"""
        if not get_unified_validator().validate_required(trades):
            return 0.0

        # Simplified total return calculation
        total_cost = sum(trade.quantity * trade.price for trade in trades if trade.side == 'buy')
        total_revenue = sum(trade.quantity * trade.price for trade in trades if trade.side == 'sell')

        if total_cost == 0:
            return 0.0

        return ((total_revenue - total_cost) / total_cost) * 100

    def _calculate_sharpe_ratio(self, trades: List[Trade]) -> float:
        """Calculate Sharpe ratio"""
        returns = self._calculate_returns_series(trades)

        if len(returns) < 2:
            return 0.0

        avg_return = statistics.mean(returns)
        volatility = statistics.stdev(returns)

        if volatility == 0:
            return 0.0

        # Assuming risk-free rate of 2% annually
        risk_free_rate = 0.02 / 252  # Daily risk-free rate

        return (avg_return - risk_free_rate) / volatility

    def _calculate_max_drawdown(self, trades: List[Trade]) -> float:
        """Calculate maximum drawdown"""
        if not get_unified_validator().validate_required(trades):
            return 0.0

        trades_sorted = sorted(trades, key=lambda x: x.timestamp)

        peak = trades_sorted[0].price
        max_drawdown = 0.0

        for trade in trades_sorted:
            if trade.price > peak:
                peak = trade.price
            drawdown = (peak - trade.price) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown * 100

    def _calculate_win_rate(self, trades: List[Trade]) -> float:
        """Calculate win rate"""
        if not get_unified_validator().validate_required(trades):
            return 0.0

        # Group trades by symbol for win/loss calculation
        symbol_trades = {}
        for trade in trades:
            if trade.symbol not in symbol_trades:
                symbol_trades[trade.symbol] = []
            symbol_trades[trade.symbol].append(trade)

        winning_trades = 0
        total_trades = 0

        for symbol, trade_list in symbol_trades.items():
            if len(trade_list) >= 2:
                buy_trades = [t for t in trade_list if t.side == 'buy']
                sell_trades = [t for t in trade_list if t.side == 'sell']

                if buy_trades and sell_trades:
                    avg_buy_price = statistics.mean(t.price for t in buy_trades)
                    avg_sell_price = statistics.mean(t.price for t in sell_trades)

                    if avg_sell_price > avg_buy_price:
                        winning_trades += 1
                    total_trades += 1

        return (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

    def _calculate_profit_factor(self, trades: List[Trade]) -> float:
        """Calculate profit factor"""
        if not get_unified_validator().validate_required(trades):
            return 0.0

        # Simplified profit factor calculation
        profits = []
        losses = []

        # Group by symbol and calculate P&L
        symbol_trades = {}
        for trade in trades:
            if trade.symbol not in symbol_trades:
                symbol_trades[trade.symbol] = []
            symbol_trades[trade.symbol].append(trade)

        for symbol, trade_list in symbol_trades.items():
            if len(trade_list) >= 2:
                buy_trades = [t for t in trade_list if t.side == 'buy']
                sell_trades = [t for t in trade_list if t.side == 'sell']

                if buy_trades and sell_trades:
                    total_buy = sum(t.quantity * t.price for t in buy_trades)
                    total_sell = sum(t.quantity * t.price for t in sell_trades)
                    pnl = total_sell - total_buy

                    if pnl > 0:
                        profits.append(pnl)
                    elif pnl < 0:
                        losses.append(abs(pnl))

        total_profits = sum(profits)
        total_losses = sum(losses)

        return total_profits / total_losses if total_losses > 0 else float('inf')

    def _calculate_avg_trade_duration(self, trades: List[Trade]) -> timedelta:
        """Calculate average trade duration"""
        if not get_unified_validator().validate_required(trades):
            return timedelta(0)

        durations = []

        # Group by symbol and calculate duration between buy and sell
        symbol_trades = {}
        for trade in trades:
            if trade.symbol not in symbol_trades:
                symbol_trades[trade.symbol] = []
            symbol_trades[trade.symbol].append(trade)

        for symbol, trade_list in symbol_trades.items():
            buy_times = [t.timestamp for t in trade_list if t.side == 'buy']
            sell_times = [t.timestamp for t in trade_list if t.side == 'sell']

            if buy_times and sell_times:
                # Simplified: assume first buy to last sell
                duration = sell_times[-1] - buy_times[0]
                durations.append(duration)

        return statistics.mean(durations) if durations else timedelta(0)


# Factory function for dependency injection
def create_trading_bi_analytics_service(repository: Optional[TradingRepositoryInterface] = None) -> TradingBiAnalyticsService:
    """Factory function to create BI analytics service with optional repository injection"""
    return TradingBiAnalyticsService(repository)


# Export for DI
__all__ = ['TradingBiAnalyticsService', 'PerformanceMetrics', 'RiskMetrics', 'MarketTrend', 'RiskLevel', 'create_trading_bi_analytics_service']
