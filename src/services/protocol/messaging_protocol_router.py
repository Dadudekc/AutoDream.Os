"""
Messaging Protocol Router - V2 Compliant Module
==============================================

Main router for messaging protocol optimization.
Coordinates all routing components and provides unified interface.

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
from .route_analyzer import RouteAnalyzer
from .route_cache import RouteCache


class MessagingProtocolRouter:
    """
    Main router for messaging protocol optimization.
    
    Coordinates route analysis, caching, and selection
    for intelligent message routing decisions.
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize protocol router."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        
        # Initialize components
        self.route_analyzer = RouteAnalyzer(config)
        self.route_cache = RouteCache(config)
        
        # Validate configuration
        try:
            if self.config.max_cache_size <= 0:
                raise ValueError("max_cache_size must be positive")
            if self.config.cache_ttl_seconds <= 0:
                raise ValueError("cache_ttl_seconds must be positive")
        except Exception as e:
            self.logger.error(f"Invalid configuration: {e}")
            raise
    
    def route_message(
        self, 
        message: UnifiedMessage, 
        strategies: List[ProtocolOptimizationStrategy]
    ) -> Tuple[MessageRoute, DeliveryResult]:
        """Route message using intelligent routing system."""
        start_time = time.time()
        
        try:
            # Check cache first
            cached_route = self.route_cache.get_route_decision(message, strategies)
            
            if cached_route:
                self.logger.debug(f"Using cached route: {cached_route.value}")
                route = cached_route
            else:
                # Analyze route options
                route = self.route_analyzer.analyze_route_options(
                    message, strategies, self.route_cache.route_cache, self.route_cache.failed_routes
                )
                
                # Cache the decision
                self.route_cache.cache_route_decision(message, route, strategies)
            
            # Create delivery result
            routing_time = (time.time() - start_time) * 1000  # Convert to ms
            delivery_result = create_delivery_result(
                success=True,
                route_used=route,
                latency_ms=routing_time,
                optimization_applied=strategies[0] if strategies else ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION,
                cache_hit=cached_route is not None
            )
            
            return route, delivery_result
            
        except Exception as e:
            self.logger.error(f"Error routing message: {e}")
            
            # Fallback to direct route
            fallback_route = MessageRoute.DIRECT
            routing_time = (time.time() - start_time) * 1000
            
            delivery_result = create_delivery_result(
                success=False,
                route_used=fallback_route,
                latency_ms=routing_time,
                optimization_applied=ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION,
                cache_hit=False,
                error_message=str(e)
            )
            
            return fallback_route, delivery_result
    
    def update_route_performance(
        self, 
        message: UnifiedMessage, 
        success: bool, 
        latency_ms: float
    ):
        """Update route performance metrics."""
        self.route_cache.update_route_performance(message, success, latency_ms)
        self.route_analyzer.update_route_performance(
            self.route_analyzer._generate_route_key(message), latency_ms, success
        )
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get comprehensive routing statistics."""
        cache_stats = self.route_cache.get_cache_stats()
        analyzer_stats = self.route_analyzer.get_analyzer_status()
        
        return {
            'cache_stats': cache_stats,
            'analyzer_stats': analyzer_stats,
            'total_routes_analyzed': len(analyzer_stats.get('tracked_routes', [])),
            'cache_hit_rate': self._calculate_cache_hit_rate(),
            'average_route_performance': self._calculate_average_performance()
        }
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        # This would need to be tracked over time
        # For now, return a placeholder
        return 0.0
    
    def _calculate_average_performance(self) -> Dict[str, float]:
        """Calculate average route performance."""
        performance_summary = self.route_analyzer.get_route_performance_summary()
        
        if not performance_summary:
            return {'average_latency_ms': 0.0, 'total_routes': 0}
        
        total_latency = sum(route['average_latency_ms'] for route in performance_summary.values())
        total_routes = len(performance_summary)
        
        return {
            'average_latency_ms': total_latency / total_routes if total_routes > 0 else 0.0,
            'total_routes': total_routes
        }
    
    def optimize_routes(self):
        """Perform route optimization maintenance."""
        self.route_cache.optimize_routes()
        self.logger.info("Route optimization completed")
    
    def clear_all_caches(self):
        """Clear all caches and performance data."""
        self.route_cache.clear_cache()
        self.route_analyzer.clear_performance_data()
        self.logger.info("All caches cleared")
    
    def get_router_status(self) -> Dict[str, Any]:
        """Get router status."""
        return {
            'cache_status': self.route_cache.get_cache_status(),
            'analyzer_status': self.route_analyzer.get_analyzer_status(),
            'routing_stats': self.get_routing_stats(),
            'configuration': {
                'max_cache_size': self.config.max_cache_size,
                'cache_ttl_seconds': self.config.cache_ttl_seconds,
                'enable_load_balancing': self.config.enable_load_balancing
            }
        }
    
    def get_best_routes_for_recipient(self, recipient: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get best performing routes for specific recipient."""
        return self.route_cache.get_best_routes_for_recipient(recipient, limit)
    
    def shutdown(self):
        """Shutdown router and cleanup resources."""
        self.clear_all_caches()
        self.logger.info("Messaging protocol router shutdown")
