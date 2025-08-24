"""
Unified Financial Services API - Cross-Agent Integration Layer
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides unified access to all financial services for cross-agent coordination.
"""

import asyncio
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid
import time

# Import all financial services
try:
    from .portfolio_management_service import (
        PortfolioManager,
        PortfolioPosition,
        PortfolioMetrics,
    )
    from .risk_management_service import (
        RiskManager,
        RiskMetric,
        RiskAlert,
        PortfolioRiskProfile,
    )
    from .market_data_service import MarketDataService, MarketData, HistoricalData
    from .trading_intelligence_service import (
        TradingIntelligenceService,
        TradingSignal,
        StrategyType,
    )
    from .options_trading_service import (
        OptionsTradingService,
        OptionContract,
        OptionsChain,
    )
    from .analytics import (
        FinancialAnalyticsService,
        BacktestResult,
        PerformanceMetrics,
    )
    from .market_sentiment_service import MarketSentimentService
    from .portfolio_optimization_service import (
        PortfolioOptimizationService,
        OptimizationResult,
    )
except ImportError:
    # Fallback for direct execution
    from portfolio_management_service import (
        PortfolioManager,
        PortfolioPosition,
        PortfolioMetrics,
    )
    from risk_management_service import (
        RiskManager,
        RiskMetric,
        RiskAlert,
        PortfolioRiskProfile,
    )
    from market_data_service import MarketDataService, MarketData, HistoricalData
    from trading_intelligence_service import (
        TradingIntelligenceService,
        TradingSignal,
        StrategyType,
    )
    from options_trading_service import (
        OptionsTradingService,
        OptionContract,
        OptionsChain,
    )
    from analytics import (
        FinancialAnalyticsService,
        BacktestResult,
        PerformanceMetrics,
    )
    from market_sentiment_service import MarketSentimentService
    from portfolio_optimization_service import (
        PortfolioOptimizationService,
        OptimizationResult,
    )

from .api_authentication import APIAuthenticator
from .api_router import RequestRouter
from .api_data_aggregator import DataAggregator
from .api_error_handler import APIErrorHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentRegistration:
    """Agent registration information"""

    agent_id: str
    agent_name: str
    agent_type: str
    required_services: List[str]
    registration_time: datetime
    last_heartbeat: datetime
    status: str  # ACTIVE, INACTIVE, ERROR
    performance_metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}


@dataclass
class CrossAgentRequest:
    """Cross-agent service request"""

    request_id: str
    source_agent: str
    target_service: str
    request_type: str
    request_data: Dict[str, Any]
    timestamp: datetime
    priority: str  # HIGH, MEDIUM, LOW
    status: str  # PENDING, PROCESSING, COMPLETED, ERROR

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class CrossAgentResponse:
    """Cross-agent service response"""

    request_id: str
    response_data: Any
    response_time: float
    status: str
    error_message: str = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SystemHealthMetrics:
    """Overall system health metrics"""

    total_agents: int
    active_agents: int
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    system_uptime: float
    last_updated: datetime

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class UnifiedFinancialAPI:
    """Unified API for all financial services with cross-agent coordination"""

    def __init__(
        self,
        data_dir: str = "unified_financial_api",
        authenticator: Optional[APIAuthenticator] = None,
        router: Optional[RequestRouter] = None,
        aggregator: Optional[DataAggregator] = None,
        error_handler: Optional[APIErrorHandler] = None,
    ):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Initialize all financial services
        self.portfolio_manager = PortfolioManager()
        self.risk_manager = RiskManager()
        self.market_data_service = MarketDataService()
        self.trading_intelligence = TradingIntelligenceService()
        self.options_trading = OptionsTradingService()
        self.financial_analytics = FinancialAnalyticsService()
        self.market_sentiment = MarketSentimentService()
        self.portfolio_optimization = PortfolioOptimizationService()

        # Service interfaces
        self.authenticator = authenticator or APIAuthenticator()
        self.request_router = router or RequestRouter(
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

        # Cross-agent coordination systems
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.active_requests: Dict[str, CrossAgentRequest] = {}
        self.request_history: List[CrossAgentRequest] = []
        self.performance_metrics: Dict[str, Dict[str, Any]] = {}

        # Data files
        self.agents_file = self.data_dir / "registered_agents.json"
        self.requests_file = self.data_dir / "request_history.json"
        self.performance_file = self.data_dir / "performance_metrics.json"

        # Load existing data
        self.load_data()

        # Start background tasks
        self.start_background_tasks()

        logger.info("Unified Financial API initialized successfully")

    def start_background_tasks(self):
        """Start background monitoring and maintenance tasks"""
        try:
            # Start heartbeat monitoring
            asyncio.create_task(self.monitor_agent_heartbeats())

            # Start performance monitoring
            asyncio.create_task(self.monitor_system_performance())

            # Start cleanup tasks
            asyncio.create_task(self.cleanup_old_data())

            logger.info("Background tasks started successfully")
        except Exception as e:
            logger.error(f"Error starting background tasks: {e}")

    async def monitor_agent_heartbeats(self):
        """Monitor agent heartbeats and update status"""
        while True:
            try:
                current_time = datetime.now()
                inactive_threshold = timedelta(minutes=5)

                for agent_id, agent in self.registered_agents.items():
                    if current_time - agent.last_heartbeat > inactive_threshold:
                        agent.status = "INACTIVE"
                        logger.warning(f"Agent {agent_id} marked as inactive")

                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in heartbeat monitoring: {e}")
                await asyncio.sleep(60)

    async def monitor_system_performance(self):
        """Monitor overall system performance"""
        while True:
            try:
                self.update_system_health_metrics()
                await asyncio.sleep(60)  # Update every minute
            except Exception as e:
                logger.error(f"Error in performance monitoring: {e}")
                await asyncio.sleep(120)

    async def cleanup_old_data(self):
        """Clean up old request history and performance data"""
        while True:
            try:
                # Keep only last 1000 requests
                if len(self.request_history) > 1000:
                    self.request_history = self.request_history[-1000:]

                # Clean up old performance metrics (keep last 7 days)
                cutoff_time = datetime.now() - timedelta(days=7)
                for agent_id in list(self.performance_metrics.keys()):
                    if "last_updated" in self.performance_metrics[agent_id]:
                        last_updated = datetime.fromisoformat(
                            self.performance_metrics[agent_id]["last_updated"]
                        )
                        if last_updated < cutoff_time:
                            del self.performance_metrics[agent_id]

                await asyncio.sleep(300)  # Clean up every 5 minutes
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(600)

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        required_services: List[str],
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

            # Initialize performance metrics for agent
            self.performance_metrics[agent_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_response_time": 0.0,
                "last_updated": datetime.now().isoformat(),
            }

            logger.info(f"Agent {agent_id} registered successfully")
            self.save_data()
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
    ) -> str:
        """Request a financial service through the unified API"""
        try:
            # Authorization handled by authenticator
            self.authenticator.authorize(
                source_agent, target_service, self.registered_agents
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
        try:
            if request_id not in self.active_requests:
                raise ValueError(f"Request {request_id} not found")

            request = self.active_requests[request_id]
            request.status = "PROCESSING"

            start_time = time.time()

            # Execute the requested service via router
            response_data = self.request_router.route(
                request.target_service, request.request_type, request.request_data
            )

            response_time = time.time() - start_time

            # Create response
            response = CrossAgentResponse(
                request_id=request_id,
                response_data=response_data,
                response_time=response_time,
                status="SUCCESS",
            )

            # Update request status
            request.status = "COMPLETED"

            # Update performance metrics
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
            logger.error(f"Error executing service request {request_id}: {e}")
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
            metrics = self.data_aggregator.aggregate_system_health(
                self.registered_agents, self.performance_metrics
            )
            return SystemHealthMetrics(
                **metrics,
                last_updated=datetime.now(),
            )
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

    def save_data(self):
        """Save all data to files"""
        try:
            # Save registered agents
            agents_data = {}
            for agent_id, agent in self.registered_agents.items():
                agents_data[agent_id] = asdict(agent)

            with open(self.agents_file, "w") as f:
                json.dump(agents_data, f, indent=2, default=str)

            # Save request history
            requests_data = [asdict(request) for request in self.request_history]
            with open(self.requests_file, "w") as f:
                json.dump(requests_data, f, indent=2, default=str)

            # Save performance metrics
            with open(self.performance_file, "w") as f:
                json.dump(self.performance_metrics, f, indent=2, default=str)

            logger.info("Unified Financial API data saved successfully")
        except Exception as e:
            logger.error(f"Error saving Unified Financial API data: {e}")

    def load_data(self):
        """Load data from files"""
        try:
            # Load registered agents
            if self.agents_file.exists():
                with open(self.agents_file, "r") as f:
                    agents_data = json.load(f)

                for agent_id, agent_dict in agents_data.items():
                    if "registration_time" in agent_dict:
                        agent_dict["registration_time"] = datetime.fromisoformat(
                            agent_dict["registration_time"]
                        )
                    if "last_heartbeat" in agent_dict:
                        agent_dict["last_heartbeat"] = datetime.fromisoformat(
                            agent_dict["last_heartbeat"]
                        )

                    agent_obj = AgentRegistration(**agent_dict)
                    self.registered_agents[agent_id] = agent_obj

                logger.info(f"Loaded {len(agents_data)} registered agents")

            # Load request history
            if self.requests_file.exists():
                with open(self.requests_file, "r") as f:
                    requests_data = json.load(f)

                for request_dict in requests_data:
                    if "timestamp" in request_dict:
                        request_dict["timestamp"] = datetime.fromisoformat(
                            request_dict["timestamp"]
                        )

                    request_obj = CrossAgentRequest(**request_dict)
                    self.request_history.append(request_obj)

                logger.info(f"Loaded {len(requests_data)} request history items")

            # Load performance metrics
            if self.performance_file.exists():
                with open(self.performance_file, "r") as f:
                    self.performance_metrics = json.load(f)

                logger.info(
                    f"Loaded performance metrics for {len(self.performance_metrics)} agents"
                )

        except Exception as e:
            logger.error(f"Error loading Unified Financial API data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create unified financial API
    api = UnifiedFinancialAPI()

    # Test agent registration
    success = api.register_agent(
        agent_id="AGENT_1",
        agent_name="Test Agent 1",
        agent_type="TESTING",
        required_services=["portfolio_management", "risk_management"],
    )

    print(f"Agent registration: {'SUCCESS' if success else 'FAILED'}")

    # Test service request
    if success:
        request_id = api.request_service(
            source_agent="AGENT_1",
            target_service="portfolio_management",
            request_type="get_portfolio",
            request_data={},
        )

        print(f"Service request created: {request_id}")

        # Execute request
        response = api.execute_service_request(request_id)
        print(f"Response status: {response.status}")

    print("Unified Financial API test completed")
