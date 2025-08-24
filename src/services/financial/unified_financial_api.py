"""Unified Financial Services API orchestrator."""

import logging
from typing import Any, Dict, List, Optional

from .api_authentication import APIAuthenticator
from .api_data_aggregator import DataAggregator
from .api_error_handler import APIErrorHandler
from .api_background_tasks import BackgroundTasks
from .api_persistence import PersistenceManager
from .api_router import RequestRouter
from .authentication_service import AuthenticationService
from .models import (
    AgentRegistration,
    CrossAgentRequest,
    CrossAgentResponse,
    SystemHealthMetrics,
)
from .unified_financial_api_config import UnifiedFinancialAPIConfig
from .unified_financial_api_processor import UnifiedFinancialAPIProcessorMixin
from .unified_financial_api_router import UnifiedFinancialAPIRouterMixin

# Import optional financial services
try:  # pragma: no cover - optional dependencies
    from .portfolio_management_service import (
        PortfolioManager,
        PortfolioPosition,
        PortfolioMetrics,
    )
except Exception:  # pragma: no cover
    PortfolioManager = PortfolioPosition = PortfolioMetrics = None

try:  # pragma: no cover - optional dependencies
    from .risk_management_service import (
        RiskManager,
        RiskMetric,
        RiskAlert,
        PortfolioRiskProfile,
    )
except Exception:  # pragma: no cover
    RiskManager = RiskMetric = RiskAlert = PortfolioRiskProfile = None

try:  # pragma: no cover - optional dependencies
    from .market_data_service import MarketDataService, MarketData, HistoricalData
except Exception:  # pragma: no cover
    MarketDataService = MarketData = HistoricalData = None

try:  # pragma: no cover - optional dependencies
    from .trading_intelligence_service import (
        TradingIntelligenceService,
        TradingSignal,
        StrategyType,
    )
except Exception:  # pragma: no cover
    TradingIntelligenceService = TradingSignal = StrategyType = None

try:  # pragma: no cover - optional dependencies
    from .options_trading_service import (
        OptionsTradingService,
        OptionContract,
        OptionsChain,
    )
except Exception:  # pragma: no cover
    OptionsTradingService = OptionContract = OptionsChain = None

try:  # pragma: no cover - optional dependencies
    from .analytics import (
        FinancialAnalyticsService,
        BacktestResult,
        PerformanceMetrics,
    )
except Exception:  # pragma: no cover
    FinancialAnalyticsService = BacktestResult = PerformanceMetrics = None

try:  # pragma: no cover - optional dependencies
    from .market_sentiment_service import MarketSentimentService
except Exception:  # pragma: no cover
    MarketSentimentService = None

try:  # pragma: no cover - optional dependencies
    from .portfolio_optimization_service import (
        PortfolioOptimizationService,
        OptimizationResult,
    )
except Exception:  # pragma: no cover
    PortfolioOptimizationService = OptimizationResult = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedFinancialAPI(
    UnifiedFinancialAPIRouterMixin, UnifiedFinancialAPIProcessorMixin
):
    """Unified API for all financial services with cross-agent coordination."""

    def __init__(
        self,
        data_dir: str = "unified_financial_api",
        authenticator: Optional[APIAuthenticator] = None,
        router: Optional[Any] = None,
        aggregator: Optional[DataAggregator] = None,
        error_handler: Optional[APIErrorHandler] = None,
    ) -> None:
        self.config = UnifiedFinancialAPIConfig(data_dir)

        self.portfolio_manager = PortfolioManager() if PortfolioManager else None
        self.risk_manager = RiskManager() if RiskManager else None
        self.market_data_service = (
            MarketDataService() if MarketDataService else None
        )
        self.trading_intelligence = (
            TradingIntelligenceService() if TradingIntelligenceService else None
        )
        self.options_trading = (
            OptionsTradingService() if OptionsTradingService else None
        )
        self.financial_analytics = (
            FinancialAnalyticsService() if FinancialAnalyticsService else None
        )
        self.market_sentiment = (
            MarketSentimentService() if MarketSentimentService else None
        )
        try:
            self.portfolio_optimization = (
                PortfolioOptimizationService() if PortfolioOptimizationService else None
            )
        except Exception:  # pragma: no cover - optional dependency may fail
            self.portfolio_optimization = None

        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.active_requests: Dict[str, CrossAgentRequest] = {}
        self.request_history: List[CrossAgentRequest] = []
        self.performance_metrics: Dict[str, Dict[str, Any]] = {}

        self.auth_service = authenticator or AuthenticationService()
        self.router = router or RequestRouter(
            self.portfolio_manager,
            self.risk_manager,
            self.market_data_service,
            self.trading_intelligence,
            self.options_trading,
            self.financial_analytics,
            self.market_sentiment,
            self.portfolio_optimization,
        )
        self.data_aggregator = aggregator or DataAggregator()
        self.error_handler = error_handler or APIErrorHandler()

        self.persistence = PersistenceManager(
            self.config.agents_file,
            self.config.requests_file,
            self.config.performance_file,
        )
        self.persistence.load(
            self.registered_agents, self.request_history, self.performance_metrics
        )

        self.background = BackgroundTasks(self)
        self.background.start()

        logger.info("Unified Financial API initialized successfully")
