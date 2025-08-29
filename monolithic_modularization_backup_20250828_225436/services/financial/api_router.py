from typing import Any, Dict
import logging

from .portfolio_management_service import PortfolioPosition
from __future__ import annotations


"""Request routing component for UnifiedFinancialAPI."""



logger = logging.getLogger(__name__)


class RequestRouter:
    """Routes requests to the appropriate financial service."""

    def __init__(
        self,
        portfolio_manager,
        risk_manager,
        market_data_service,
        trading_intelligence,
        options_trading,
        financial_analytics,
        market_sentiment,
        portfolio_optimization,
    ) -> None:
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.market_data_service = market_data_service
        self.trading_intelligence = trading_intelligence
        self.options_trading = options_trading
        self.financial_analytics = financial_analytics
        self.market_sentiment = market_sentiment
        self.portfolio_optimization = portfolio_optimization

    def route(
        self, target_service: str, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Route a request to the appropriate service."""
        if target_service == "portfolio_management":
            return self._execute_portfolio_service(request_type, request_data)
        if target_service == "risk_management":
            return self._execute_risk_service(request_type, request_data)
        if target_service == "market_data":
            return self._execute_market_data_service(request_type, request_data)
        if target_service == "trading_intelligence":
            return self._execute_trading_intelligence_service(request_type, request_data)
        if target_service == "options_trading":
            return self._execute_options_trading_service(request_type, request_data)
        if target_service == "financial_analytics":
            return self._execute_financial_analytics_service(request_type, request_data)
        if target_service == "market_sentiment":
            return self._execute_market_sentiment_service(request_type, request_data)
        if target_service == "portfolio_optimization":
            return self._execute_portfolio_optimization_service(request_type, request_data)
        raise ValueError(f"Unknown service: {target_service}")

    def _execute_portfolio_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "get_portfolio":
                return self.portfolio_manager.get_portfolio()
            if request_type == "add_position":
                return self.portfolio_manager.add_position(**request_data)
            if request_type == "get_metrics":
                return self.portfolio_manager.get_portfolio_metrics()
            raise ValueError(
                f"Unknown portfolio management request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing portfolio management service: {e}")
            raise

    def _execute_risk_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "get_risk_metrics":
                portfolio = request_data.get("portfolio", {})
                return self.risk_manager.calculate_portfolio_risk(portfolio)
            if request_type == "monitor_risk":
                portfolio = request_data.get("portfolio", {})
                return self.risk_manager.monitor_risk_metrics(portfolio)
            raise ValueError(
                f"Unknown risk management request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing risk management service: {e}")
            raise

    def _execute_market_data_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "get_quote":
                symbol = request_data.get("symbol")
                return self.market_data_service.get_market_data(symbol)
            if request_type == "get_historical_data":
                symbol = request_data.get("symbol")
                start_date = request_data.get("start_date")
                end_date = request_data.get("end_date")
                return self.market_data_service.get_historical_data(
                    symbol, start_date, end_date
                )
            raise ValueError(
                f"Unknown market data request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing market data service: {e}")
            raise

    def _execute_trading_intelligence_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "generate_signals":
                symbols = request_data.get("symbols", [])
                return self.trading_intelligence.generate_trading_signals(symbols)
            if request_type == "analyze_market_conditions":
                return self.trading_intelligence.analyze_market_conditions()
            raise ValueError(
                f"Unknown trading intelligence request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing trading intelligence service: {e}")
            raise

    def _execute_options_trading_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "get_options_chain":
                symbol = request_data.get("symbol")
                expiration = request_data.get("expiration", "30d")
                return self.options_trading.analyze_options_chain(symbol, expiration)
            if request_type == "calculate_option_price":
                return self.options_trading.calculate_black_scholes(**request_data)
            raise ValueError(
                f"Unknown options trading request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing options trading service: {e}")
            raise

    def _execute_financial_analytics_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "run_backtest":
                return self.financial_analytics.run_backtest(**request_data)
            if request_type == "calculate_performance_metrics":
                return self.financial_analytics.calculate_performance_metrics(
                    **request_data
                )
            raise ValueError(
                f"Unknown financial analytics request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing financial analytics service: {e}")
            raise

    def _execute_market_sentiment_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "analyze_text_sentiment":
                text = request_data.get("text", "")
                return self.market_sentiment.analyze_text_sentiment(text)
            if request_type == "get_sentiment_signals":
                symbol = request_data.get("symbol")
                return self.market_sentiment.get_sentiment_signals(symbol)
            if request_type == "calculate_market_psychology":
                symbols = request_data.get("symbols", [])
                return self.market_sentiment.calculate_market_psychology(symbols)
            raise ValueError(
                f"Unknown market sentiment request type: {request_type}"
            )
        except Exception as e:
            logger.error(f"Error executing market sentiment service: {e}")
            raise

    def _execute_portfolio_optimization_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        try:
            if request_type == "optimize_portfolio_sharpe":
                symbols = request_data.get("symbols", [])
                current_weights = request_data.get("current_weights")
                constraints = request_data.get("constraints")
                return self.portfolio_optimization.optimize_portfolio_sharpe(
                    symbols, current_weights, constraints
                )
            if request_type == "generate_rebalancing_signals":
                current_portfolio = request_data.get("current_portfolio", {})
                target_weights = request_data.get("target_weights", {})
                return self.portfolio_optimization.generate_rebalancing_signals(
                    current_portfolio, target_weights
                )
            raise ValueError(
                f"Unknown portfolio optimization request type: {request_type}"
            )
        except Exception as e:
            logger.error(
                f"Error executing portfolio optimization service: {e}"
            )
            raise
