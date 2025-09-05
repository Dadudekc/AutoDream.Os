"""
Route Analyzer - V2 Compliant Module
===================================

Analyzes route options and calculates scores.
Extracted from messaging_protocol_router.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from ..messaging_protocol_models import (
    MessageRoute, ProtocolOptimizationStrategy, RouteOptimization,
    DeliveryResult, OptimizationConfig, create_route_optimization,
    create_delivery_result, create_default_config, ROUTE_PRIORITY_ORDER
)
from ...models.messaging_models import UnifiedMessage, UnifiedMessagePriority


class RouteAnalyzer:
    """
    Analyzes route options and calculates scores.
    
    Handles route analysis, scoring, and selection logic
    for message routing decisions.
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize route analyzer."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        self.route_performance: Dict[str, List[float]] = {}
        self.route_usage_counts: Dict[str, int] = {}
    
    def analyze_route_options(
        self, 
        message: UnifiedMessage, 
        strategies: List[ProtocolOptimizationStrategy],
        route_cache: Dict[str, RouteOptimization],
        failed_routes: Dict[str, datetime]
    ) -> MessageRoute:
        """Analyze and select best route option."""
        
        # Priority-based routing for urgent messages
        if message.priority == UnifiedMessagePriority.URGENT:
            if ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION in strategies:
                return self._select_fastest_route(message, route_cache)
            return MessageRoute.DIRECT
        
        # Strategy-based routing
        route_scores = {}
        
        for route in ROUTE_PRIORITY_ORDER:
            score = self._calculate_route_score(
                message, route, strategies, route_cache, failed_routes
            )
            route_scores[route] = score
        
        # Select route with highest score
        best_route = max(route_scores.items(), key=lambda x: x[1])[0]
        return best_route
    
    def _select_fastest_route(
        self, 
        message: UnifiedMessage, 
        route_cache: Dict[str, RouteOptimization]
    ) -> MessageRoute:
        """Select fastest available route for urgent messages."""
        route_key = self._generate_route_key(message)
        
        # Check if we have performance data for this route
        if route_key in self.route_performance:
            latencies = self.route_performance[route_key]
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                if avg_latency < 100:  # Less than 100ms
                    return MessageRoute.CACHED if route_key in route_cache else MessageRoute.DIRECT
        
        return MessageRoute.DIRECT
    
    def _calculate_route_score(
        self, 
        message: UnifiedMessage, 
        route: MessageRoute,
        strategies: List[ProtocolOptimizationStrategy],
        route_cache: Dict[str, RouteOptimization],
        failed_routes: Dict[str, datetime]
    ) -> float:
        """Calculate score for route option."""
        score = 0.0
        
        # Base route scores
        base_scores = {
            MessageRoute.CACHED: 10.0,
            MessageRoute.DIRECT: 8.0,
            MessageRoute.OPTIMIZED: 7.0,
            MessageRoute.BATCHED: 6.0,
            MessageRoute.LOAD_BALANCED: 5.0,
            MessageRoute.QUEUED: 4.0
        }
        score += base_scores.get(route, 0.0)
        
        # Strategy compatibility bonuses
        if route == MessageRoute.BATCHED and ProtocolOptimizationStrategy.MESSAGE_BATCHING in strategies:
            score += 3.0
        
        if route == MessageRoute.LOAD_BALANCED and ProtocolOptimizationStrategy.LOAD_BALANCING in strategies:
            score += 2.0
        
        if route == MessageRoute.CACHED and ProtocolOptimizationStrategy.CACHING in strategies:
            score += 4.0
        
        # Performance-based adjustments
        route_key = self._generate_route_key(message)
        if route_key in route_cache:
            route_opt = route_cache[route_key]
            score += route_opt.success_rate * 2.0  # Up to 2 points for success rate
            score -= (route_opt.latency_ms / 100.0)  # Penalty for high latency
        
        # Load balancing adjustment
        if self.config.enable_load_balancing:
            usage_count = self.route_usage_counts.get(route.value, 0)
            # Slight preference for less used routes
            score += max(0, 1.0 - (usage_count / 100.0))
        
        return score
    
    def _generate_route_key(self, message: UnifiedMessage) -> str:
        """Generate cache key for route decision."""
        return f"{message.sender}:{message.recipient}:{message.priority.value}:{message.type.value}"
    
    def update_route_performance(self, route_key: str, latency_ms: float, success: bool):
        """Update route performance metrics."""
        if route_key not in self.route_performance:
            self.route_performance[route_key] = []
        
        self.route_performance[route_key].append(latency_ms)
        
        # Keep only recent performance data
        if len(self.route_performance[route_key]) > 1000:
            self.route_performance[route_key] = self.route_performance[route_key][-500:]
        
        # Update usage count
        route_type = route_key.split(':')[0]  # Extract route type
        self.route_usage_counts[route_type] = self.route_usage_counts.get(route_type, 0) + 1
    
    def get_route_performance_summary(self) -> Dict[str, Any]:
        """Get route performance summary."""
        summary = {}
        
        for route_key, latencies in self.route_performance.items():
            if latencies:
                summary[route_key] = {
                    'average_latency_ms': sum(latencies) / len(latencies),
                    'min_latency_ms': min(latencies),
                    'max_latency_ms': max(latencies),
                    'sample_count': len(latencies)
                }
        
        return summary
    
    def get_route_usage_stats(self) -> Dict[str, int]:
        """Get route usage statistics."""
        return self.route_usage_counts.copy()
    
    def clear_performance_data(self):
        """Clear all performance data."""
        self.route_performance.clear()
        self.route_usage_counts.clear()
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """Get analyzer status."""
        return {
            'tracked_routes': len(self.route_performance),
            'usage_counts': self.route_usage_counts,
            'performance_summary': self.get_route_performance_summary()
        }
