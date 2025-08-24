import logging
import time
from datetime import datetime
from typing import Any, Dict

from .models import CrossAgentResponse, SystemHealthMetrics
from .unified_financial_api_responses import create_success_response

logger = logging.getLogger(__name__)


class UnifiedFinancialAPIProcessorMixin:
    """Request execution and health metrics helpers."""

    def execute_service_request(self, request_id: str) -> CrossAgentResponse:
        """Execute a service request and return response."""
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
            response = create_success_response(request_id, response_data, response_time)
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
                self.performance_metrics[source_agent]["last_updated"] = (
                    datetime.now().isoformat()
                )
            logger.info(f"Service request {request_id} executed successfully")
            return response
        except Exception as e:
            response_time = time.time() - start_time
            request.status = "ERROR"
            source_agent = request.source_agent
            if source_agent in self.performance_metrics:
                self.performance_metrics[source_agent]["failed_requests"] += 1
                self.performance_metrics[source_agent]["last_updated"] = (
                    datetime.now().isoformat()
                )
            return self.error_handler.handle(
                request_id,
                e,
                request,
                self.performance_metrics,
                CrossAgentResponse,
            )

    def get_system_health_metrics(self) -> SystemHealthMetrics:
        """Get overall system health metrics."""
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

    def update_system_health_metrics(self) -> None:
        """Update system health metrics."""
        try:
            self.system_health_metrics = self.get_system_health_metrics()
        except Exception as e:
            logger.error(f"Error updating system health metrics: {e}")
