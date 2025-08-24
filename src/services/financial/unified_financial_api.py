"""
Unified Financial Services API - Cross-Agent Integration Layer
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides unified access to all financial services for cross-agent coordination.
"""

import asyncio
import json
import logging
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
    from .market_sentiment_service import (
        MarketSentimentService,
        SentimentData,
        SentimentAggregate,
    )
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
    from market_sentiment_service import (
        MarketSentimentService,
        SentimentData,
        SentimentAggregate,
    )
    from portfolio_optimization_service import (
        PortfolioOptimizationService,
        OptimizationResult,
    )

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

    def __init__(self, data_dir: str = "unified_financial_api"):
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
            # Validate source agent
            if source_agent not in self.registered_agents:
                raise ValueError(f"Agent {source_agent} not registered")

            # Validate target service
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
        try:
            if request_id not in self.active_requests:
                raise ValueError(f"Request {request_id} not found")

            request = self.active_requests[request_id]
            request.status = "PROCESSING"

            start_time = time.time()

            # Execute the requested service
            response_data = self._execute_service(
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

            # Update request status
            if request_id in self.active_requests:
                self.active_requests[request_id].status = "ERROR"

            # Update performance metrics
            if request_id in self.active_requests:
                source_agent = self.active_requests[request_id].source_agent
                if source_agent in self.performance_metrics:
                    self.performance_metrics[source_agent]["failed_requests"] += 1
                    self.performance_metrics[source_agent][
                        "last_updated"
                    ] = datetime.now().isoformat()

            # Return error response
            return CrossAgentResponse(
                request_id=request_id,
                response_data=None,
                response_time=0.0,
                status="ERROR",
                error_message=str(e),
            )

    def _execute_service(
        self, target_service: str, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute the actual financial service"""
        try:
            if target_service == "portfolio_management":
                return self._execute_portfolio_service(request_type, request_data)
            elif target_service == "risk_management":
                return self._execute_risk_service(request_type, request_data)
            elif target_service == "market_data":
                return self._execute_market_data_service(request_type, request_data)
            elif target_service == "trading_intelligence":
                return self._execute_trading_intelligence_service(
                    request_type, request_data
                )
            elif target_service == "options_trading":
                return self._execute_options_trading_service(request_type, request_data)
            elif target_service == "financial_analytics":
                return self._execute_financial_analytics_service(
                    request_type, request_data
                )
            elif target_service == "market_sentiment":
                return self._execute_market_sentiment_service(
                    request_type, request_data
                )
            elif target_service == "portfolio_optimization":
                return self._execute_portfolio_optimization_service(
                    request_type, request_data
                )
            else:
                raise ValueError(f"Unknown service: {target_service}")
        except Exception as e:
            logger.error(f"Error executing service {target_service}: {e}")
            raise

    def _execute_portfolio_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute portfolio management service"""
        try:
            if request_type == "get_portfolio":
                return self.portfolio_manager.get_portfolio()
            elif request_type == "add_position":
                return self.portfolio_manager.add_position(**request_data)
            elif request_type == "update_position":
                return self.portfolio_manager.update_position(**request_data)
            elif request_type == "remove_position":
                return self.portfolio_manager.remove_position(**request_data)
            elif request_type == "get_portfolio_metrics":
                return self.portfolio_manager.get_portfolio_metrics()
            else:
                raise ValueError(f"Unknown portfolio request type: {request_type}")
        except Exception as e:
            logger.error(f"Error executing portfolio service: {e}")
            raise

    def _execute_risk_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute risk management service"""
        try:
            if request_type == "calculate_portfolio_risk":
                return self.risk_manager.calculate_portfolio_risk(**request_data)
            elif request_type == "get_risk_metrics":
                return self.risk_manager.get_risk_metrics()
            elif request_type == "add_risk_alert":
                return self.risk_manager.add_risk_alert(**request_data)
            else:
                raise ValueError(f"Unknown risk request type: {request_type}")
        except Exception as e:
            logger.error(f"Error executing risk service: {e}")
            raise

    def _execute_market_data_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute market data service"""
        try:
            if request_type == "get_real_time_data":
                symbols = request_data.get("symbols", [])
                return self.market_data_service.get_real_time_data(symbols)
            elif request_type == "get_historical_data":
                symbol = request_data.get("symbol")
                period = request_data.get("period", "1y")
                interval = request_data.get("interval", "1d")
                return self.market_data_service.get_historical_data(
                    symbol, period, interval
                )
            else:
                raise ValueError(f"Unknown market data request type: {request_type}")
        except Exception as e:
            logger.error(f"Error executing market data service: {e}")
            raise

    def _execute_trading_intelligence_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute trading intelligence service"""
        try:
            if request_type == "generate_signals":
                symbols = request_data.get("symbols", [])
                return self.trading_intelligence.generate_trading_signals(symbols)
            elif request_type == "analyze_market_conditions":
                return self.trading_intelligence.analyze_market_conditions()
            else:
                raise ValueError(
                    f"Unknown trading intelligence request type: {request_type}"
                )
        except Exception as e:
            logger.error(f"Error executing trading intelligence service: {e}")
            raise

    def _execute_options_trading_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute options trading service"""
        try:
            if request_type == "get_options_chain":
                symbol = request_data.get("symbol")
                expiration = request_data.get("expiration", "30d")  # Default to 30 days
                return self.options_trading.analyze_options_chain(symbol, expiration)
            elif request_type == "calculate_option_price":
                # Use the correct method for option pricing
                return self.options_trading.calculate_black_scholes(**request_data)
            else:
                raise ValueError(
                    f"Unknown options trading request type: {request_type}"
                )
        except Exception as e:
            logger.error(f"Error executing options trading service: {e}")
            raise

    def _execute_financial_analytics_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute financial analytics service"""
        try:
            if request_type == "run_backtest":
                return self.financial_analytics.run_backtest(**request_data)
            elif request_type == "calculate_performance_metrics":
                return self.financial_analytics.calculate_performance_metrics(
                    **request_data
                )
            else:
                raise ValueError(
                    f"Unknown financial analytics request type: {request_type}"
                )
        except Exception as e:
            logger.error(f"Error executing financial analytics service: {e}")
            raise

    def _execute_market_sentiment_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute market sentiment service"""
        try:
            if request_type == "analyze_text_sentiment":
                text = request_data.get("text", "")
                return self.market_sentiment.analyze_text_sentiment(text)
            elif request_type == "get_sentiment_signals":
                symbol = request_data.get("symbol")
                return self.market_sentiment.get_sentiment_signals(symbol)
            elif request_type == "calculate_market_psychology":
                symbols = request_data.get("symbols", [])
                return self.market_sentiment.calculate_market_psychology(symbols)
            else:
                raise ValueError(
                    f"Unknown market sentiment request type: {request_type}"
                )
        except Exception as e:
            logger.error(f"Error executing market sentiment service: {e}")
            raise

    def _execute_portfolio_optimization_service(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Any:
        """Execute portfolio optimization service"""
        try:
            if request_type == "optimize_portfolio_sharpe":
                symbols = request_data.get("symbols", [])
                current_weights = request_data.get("current_weights")
                constraints = request_data.get("constraints")
                return self.portfolio_optimization.optimize_portfolio_sharpe(
                    symbols, current_weights, constraints
                )
            elif request_type == "generate_rebalancing_signals":
                current_portfolio = request_data.get("current_portfolio", {})
                target_weights = request_data.get("target_weights", {})
                return self.portfolio_optimization.generate_rebalancing_signals(
                    current_portfolio, target_weights
                )
            else:
                raise ValueError(
                    f"Unknown portfolio optimization request type: {request_type}"
                )
        except Exception as e:
            logger.error(f"Error executing portfolio optimization service: {e}")
            raise

    def get_system_health_metrics(self) -> SystemHealthMetrics:
        """Get overall system health metrics"""
        try:
            total_agents = len(self.registered_agents)
            active_agents = sum(
                1
                for agent in self.registered_agents.values()
                if agent.status == "ACTIVE"
            )

            total_requests = sum(
                metrics["total_requests"]
                for metrics in self.performance_metrics.values()
            )
            successful_requests = sum(
                metrics["successful_requests"]
                for metrics in self.performance_metrics.values()
            )
            failed_requests = sum(
                metrics["failed_requests"]
                for metrics in self.performance_metrics.values()
            )

            # Calculate average response time
            response_times = [
                metrics["average_response_time"]
                for metrics in self.performance_metrics.values()
                if metrics["average_response_time"] > 0
            ]
            average_response_time = (
                sum(response_times) / len(response_times) if response_times else 0.0
            )

            # Calculate system uptime (simplified)
            system_uptime = 99.9  # Placeholder - would calculate from actual start time

            return SystemHealthMetrics(
                total_agents=total_agents,
                active_agents=active_agents,
                total_requests=total_requests,
                successful_requests=successful_requests,
                failed_requests=failed_requests,
                average_response_time=average_response_time,
                system_uptime=system_uptime,
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
