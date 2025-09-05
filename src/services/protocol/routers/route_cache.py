"""
Route Cache - V2 Compliant Module
================================

Manages route caching and optimization.
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


class RouteCache:
    """
    Manages route caching and optimization.
    
    Handles route caching, validation, and maintenance
    for message routing optimization.
    """
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize route cache."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        self.route_cache: Dict[str, RouteOptimization] = {}
        self.failed_routes: Dict[str, datetime] = {}
    
    def get_route_decision(
        self, 
        message: UnifiedMessage, 
        strategies: List[ProtocolOptimizationStrategy]
    ) -> Optional[MessageRoute]:
        """Get cached route decision if available and valid."""
        route_key = self._generate_route_key(message)
        
        if route_key in self.route_cache:
            route_opt = self.route_cache[route_key]
            if self._is_route_valid(route_opt):
                # Update usage statistics
                route_opt.usage_count += 1
                route_opt.last_used = datetime.now()
                return route_opt.route
            else:
                # Remove invalid route from cache
                del self.route_cache[route_key]
        
        return None
    
    def cache_route_decision(
        self, 
        message: UnifiedMessage, 
        route: MessageRoute, 
        strategies: List[ProtocolOptimizationStrategy]
    ):
        """Cache route decision for future use."""
        route_key = self._generate_route_key(message)
        
        # Create route optimization record
        route_opt = create_route_optimization(
            route=route,
            strategy=strategies[0] if strategies else ProtocolOptimizationStrategy.ROUTE_OPTIMIZATION,
            source=message.sender,
            destination=message.recipient,
            success_rate=1.0,  # Initial success rate
            latency_ms=0.0,    # Will be updated with actual performance
            usage_count=1,
            last_used=datetime.now()
        )
        
        # Check cache size limit
        if len(self.route_cache) >= self.config.max_cache_size:
            self._evict_oldest_route()
        
        self.route_cache[route_key] = route_opt
        self.logger.debug(f"Cached route decision: {route_key} -> {route.value}")
    
    def update_route_performance(
        self, 
        message: UnifiedMessage, 
        success: bool, 
        latency_ms: float
    ):
        """Update route performance metrics."""
        route_key = self._generate_route_key(message)
        
        if route_key in self.route_cache:
            route_opt = self.route_cache[route_key]
            
            # Update success rate (simple moving average)
            if success:
                route_opt.success_rate = min(1.0, route_opt.success_rate + 0.1)
            else:
                route_opt.success_rate = max(0.0, route_opt.success_rate - 0.1)
            
            # Update latency (exponential moving average)
            if route_opt.latency_ms == 0.0:
                route_opt.latency_ms = latency_ms
            else:
                route_opt.latency_ms = (route_opt.latency_ms * 0.8) + (latency_ms * 0.2)
            
            # Mark as failed if success rate is too low
            if route_opt.success_rate < 0.3:
                self._mark_route_failed(route_key)
        else:
            # Mark route as failed if not in cache
            self._mark_route_failed(route_key)
    
    def _generate_route_key(self, message: UnifiedMessage) -> str:
        """Generate cache key for route decision."""
        return f"{message.sender}:{message.recipient}:{message.priority.value}:{message.type.value}"
    
    def _is_route_valid(self, route_opt: RouteOptimization) -> bool:
        """Check if cached route is still valid."""
        # Check if route hasn't failed recently
        route_key = f"{route_opt.source}:{route_opt.destination}"
        if route_key in self.failed_routes:
            failure_time = self.failed_routes[route_key]
            if datetime.now() - failure_time < timedelta(minutes=5):  # 5 min cooldown
                return False
        
        # Check if route performance is acceptable
        if route_opt.success_rate < 0.8:  # 80% success rate threshold
            return False
        
        # Check cache TTL
        cache_age = (datetime.now() - route_opt.last_used).total_seconds()
        return cache_age < self.config.cache_ttl_seconds
    
    def _evict_oldest_route(self):
        """Evict oldest route from cache."""
        if not self.route_cache:
            return
        
        oldest_key = min(
            self.route_cache.keys(),
            key=lambda k: self.route_cache[k].last_used
        )
        del self.route_cache[oldest_key]
        self.logger.debug(f"Evicted oldest route from cache: {oldest_key}")
    
    def _mark_route_failed(self, route_key: str):
        """Mark route as failed."""
        self.failed_routes[route_key] = datetime.now()
        self.logger.debug(f"Marked route as failed: {route_key}")
    
    def optimize_routes(self):
        """Perform route optimization maintenance."""
        try:
            # Clean up old failed routes
            cutoff_time = datetime.now() - timedelta(hours=1)
            expired_failures = [k for k, v in self.failed_routes.items() if v < cutoff_time]
            for key in expired_failures:
                del self.failed_routes[key]
            
            # Remove underperforming routes from cache
            poor_routes = []
            for route_key, route_opt in self.route_cache.items():
                if route_opt.success_rate < 0.5 and route_opt.usage_count > 10:
                    poor_routes.append(route_key)
            
            for route_key in poor_routes:
                del self.route_cache[route_key]
                self.logger.info(f"Removed poor performing route from cache: {route_key}")
            
            self.logger.debug("Route optimization maintenance completed")
            
        except Exception as e:
            self.logger.error(f"Error during route optimization: {e}")
    
    def clear_cache(self):
        """Clear all route caches."""
        self.route_cache.clear()
        self.failed_routes.clear()
        self.logger.info("Route cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'total_cached_routes': len(self.route_cache),
            'failed_routes_count': len(self.failed_routes),
            'cache_utilization': len(self.route_cache) / self.config.max_cache_size,
            'average_success_rate': sum(opt.success_rate for opt in self.route_cache.values()) / max(len(self.route_cache), 1),
            'average_latency': sum(opt.latency_ms for opt in self.route_cache.values()) / max(len(self.route_cache), 1)
        }
    
    def get_best_routes_for_recipient(self, recipient: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get best performing routes for specific recipient."""
        recipient_routes = []
        
        for route_key, route_opt in self.route_cache.items():
            if route_opt.destination == recipient:
                recipient_routes.append({
                    'route_key': route_key,
                    'strategy': route_opt.strategy.value,
                    'success_rate': route_opt.success_rate,
                    'average_latency_ms': route_opt.latency_ms,
                    'usage_count': route_opt.usage_count,
                    'last_used': route_opt.last_used.isoformat()
                })
        
        # Sort by success rate and latency
        recipient_routes.sort(key=lambda x: (x['success_rate'], -x['average_latency_ms']), reverse=True)
        
        return recipient_routes[:limit]
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get cache status."""
        return {
            'cache_size': len(self.route_cache),
            'failed_routes': len(self.failed_routes),
            'stats': self.get_cache_stats()
        }
