"""Unified Financial Services API - Cross-Agent Integration Layer."""

import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import

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

# Import all financial services
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedFinancialAPI:
    """Unified API for all financial services with cross-agent coordination"""

    def __init__(
        self,
        data_dir: str = "unified_financial_api",
        authenticator: Optional[APIAuthenticator] = None,
        router: Optional[Any] = None,
        aggregator: Optional[DataAggregator] = None,
        error_handler: Optional[APIErrorHandler] = None,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize all financial services (optional modules may be missing)
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
        self.portfolio_optimization = (
            PortfolioOptimizationService() if PortfolioOptimizationService else None
        )

        # Cross-agent coordination systems
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.active_requests: Dict[str, CrossAgentRequest] = {}
        self.request_history: List[CrossAgentRequest] = []
        self.performance_metrics: Dict[str, Dict[str, Any]] = {}

        # Core components
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

        # Data persistence
        self.agents_file = self.data_dir / "registered_agents.json"
        self.requests_file = self.data_dir / "request_history.json"
        self.performance_file = self.data_dir / "performance_metrics.json"
        self.persistence = PersistenceManager(
            self.agents_file, self.requests_file, self.performance_file
        )
        self.persistence.load(
            self.registered_agents, self.request_history, self.performance_metrics
        )

        # Start background tasks
        self.background = BackgroundTasks(self)
        self.background.start()

        logger.info("Unified Financial API initialized successfully")

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        required_services: List[str],
        api_token: str = "",
    ) -> bool:
        """Register a new agent with the unified API"""
        try:
            # Validate required services
            available_services = [
                "portfolio_management",
                "risk_management",
                "market_data",
                "trading_intelligence",
                "options_trading",
                "financial_analytics",
                "market_sentiment",
                "portfolio_optimization",
            ]

            for service in required_services:
                if service not in available_services:
                    logger.error(f"Invalid service requested: {service}")
                    return False

            # Create agent registration
            agent_reg = AgentRegistration(
                agent_id=agent_id,
                agent_name=agent_name,
                agent_type=agent_type,
                required_services=required_services,
                registration_time=datetime.now(),
                last_heartbeat=datetime.now(),
                status="ACTIVE",
            )

            self.registered_agents[agent_id] = agent_reg
            if hasattr(self.auth_service, "register_agent"):
                self.auth_service.register_agent(agent_id, api_token)

            # Initialize performance metrics for agent
            self.performance_metrics[agent_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
                "last_updated": datetime.now().isoformat(),
            }

            logger.info(f"Agent {agent_id} registered successfully")
            self.persistence.save(
                self.registered_agents, self.request_history, self.performance_metrics
            )
            return True

        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")
            return False

    def update_agent_heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        try:
            if agent_id in self.registered_agents:
                self.registered_agents[agent_id].last_heartbeat = datetime.now()
                self.registered_agents[agent_id].status = "ACTIVE"
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating heartbeat for agent {agent_id}: {e}")
            return False

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of an agent"""
        try:
            if agent_id in self.registered_agents:
                agent = self.registered_agents[agent_id]
                return {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.agent_name,
                    "agent_type": agent.agent_type,
                    "status": agent.status,
                    "required_services": agent.required_services,
                    "registration_time": agent.registration_time.isoformat(),
                    "last_heartbeat": agent.last_heartbeat.isoformat(),
                    "performance_metrics": self.performance_metrics.get(agent_id, {}),
                }
            return None
        except Exception as e:
            logger.error(f"Error getting agent status for {agent_id}: {e}")
            return None

    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """Get status of all registered agents"""
        try:
            return [
                self.get_agent_status(agent_id)
                for agent_id in self.registered_agents.keys()
            ]
        except Exception as e:
            logger.error(f"Error getting all agents status: {e}")
            return []

    def request_service(
        self,
        source_agent: str,
        target_service: str,
        request_type: str,
        request_data: Dict[str, Any],
        priority: str = "MEDIUM",
        api_token: str = "",
    ) -> str:
        """Request a financial service through the unified API"""
        try:
            # Validate source agent
            if source_agent not in self.registered_agents:
                raise ValueError(f"Agent {source_agent} not registered")

            if hasattr(self.auth_service, "authorize"):
                self.auth_service.authorize(
                    source_agent, target_service, self.registered_agents
                )
            else:
                if not self.auth_service.authenticate(source_agent, api_token):
                    raise PermissionError("Authentication failed")
                if (
                    target_service
                    not in self.registered_agents[source_agent].required_services
                ):
                    raise ValueError(
                        f"Service {target_service} not available for agent {source_agent}"
                    )

            # Create request
            request_id = str(uuid.uuid4())
            request = CrossAgentRequest(
                request_id=request_id,
                source_agent=source_agent,
                target_service=target_service,
                request_type=request_type,
                request_data=request_data,
                timestamp=datetime.now(),
                priority=priority,
                status="PENDING",
            )

            # Store request
            self.active_requests[request_id] = request
            self.request_history.append(request)

            # Update performance metrics
            self.performance_metrics[source_agent]["total_requests"] += 1

            logger.info(f"Service request {request_id} created for {source_agent}")
            return request_id

        except Exception as e:
            logger.error(f"Error creating service request: {e}")
            raise

    def execute_service_request(self, request_id: str) -> CrossAgentResponse:
        """Execute a service request and return response"""
        if request_id not in self.active_requests:
            raise ValueError(f"Request {request_id} not found")

        request = self.active_requests[request_id]
        request.status = "PROCESSING"
        start_time = time.time()

        try:
            response_data = self.router.route(
                request.target_service, request.request_type, request.request_data
            )
            response_time = time.time() - start_time
            response = CrossAgentResponse(
                request_id=request_id,
                response_data=response_data,
                response_time=response_time,
                status="SUCCESS",
            )
            request.status = "COMPLETED"
            source_agent = request.source_agent
            if source_agent in self.performance_metrics:
                self.performance_metrics[source_agent]["successful_requests"] += 1
                current_avg = self.performance_metrics[source_agent][
                    "average_response_time"
                ]
                total_successful = self.performance_metrics[source_agent][
                    "successful_requests"
                ]
                new_avg = (
                    (current_avg * (total_successful - 1)) + response_time
                ) / total_successful
                self.performance_metrics[source_agent][
                    "average_response_time"
                ] = new_avg
                self.performance_metrics[source_agent][
                    "last_updated"
                ] = datetime.now().isoformat()
            logger.info(f"Service request {request_id} executed successfully")
            return response
        except Exception as e:
            response_time = time.time() - start_time
            request.status = "ERROR"
            source_agent = request.source_agent
            if source_agent in self.performance_metrics:
                self.performance_metrics[source_agent]["failed_requests"] += 1
                self.performance_metrics[source_agent][
                    "last_updated"
                ] = datetime.now().isoformat()
            return self.error_handler.handle(
                request_id,
                e,
                request,
                self.performance_metrics,
                CrossAgentResponse,
            )

    def get_system_health_metrics(self) -> SystemHealthMetrics:
        """Get overall system health metrics"""
        try:
            data = self.data_aggregator.aggregate_system_health(
                self.registered_agents, self.performance_metrics
            )
            return SystemHealthMetrics(**data)
        except Exception as e:
            logger.error(f"Error getting system health metrics: {e}")
            return SystemHealthMetrics(
                total_agents=0,
                active_agents=0,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_response_time=0.0,
                system_uptime=0.0,
                last_updated=datetime.now(),
            )

    def update_system_health_metrics(self):
        """Update system health metrics"""
        try:
            self.system_health_metrics = self.get_system_health_metrics()
        except Exception as e:
            logger.error(f"Error updating system health metrics: {e}")

