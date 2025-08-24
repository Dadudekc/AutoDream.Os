from typing import Dict, Any
from datetime import datetime


class DataAggregator:
    """Aggregate system metrics for the Unified Financial API."""

    def aggregate(self, registered_agents: Dict[str, Any], performance_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        total_agents = len(registered_agents)
        active_agents = sum(1 for agent in registered_agents.values() if getattr(agent, "status", "") == "ACTIVE")

        total_requests = sum(m["total_requests"] for m in performance_metrics.values())
        successful_requests = sum(m["successful_requests"] for m in performance_metrics.values())
        failed_requests = sum(m["failed_requests"] for m in performance_metrics.values())

        response_times = [m["average_response_time"] for m in performance_metrics.values() if m["average_response_time"] > 0]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0.0

        system_uptime = 99.9

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "average_response_time": average_response_time,
            "system_uptime": system_uptime,
            "last_updated": datetime.now(),
        }
