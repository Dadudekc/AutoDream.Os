#!/usr/bin/env python3
"""
Caching Engine - V2 Compliance Module
===================================

Handles intelligent caching for analytics processing.
Extracted from vector_analytics_processor.py for V2 compliance.

Responsibilities:
- Intelligent caching system
- Cache performance optimization
- Cache statistics tracking
- Memory management

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-7 - Web Development
License: MIT
"""

import time
import logging
from functools import lru_cache, wraps
from typing import Any, Dict, List, Callable, Optional
from datetime import datetime, timedelta


class CachingEngine:
    """
    Intelligent caching engine for analytics processing.
    
    Provides LRU caching with performance optimization and
    intelligent cache management.
    """
    
    def __init__(self, config):
        """Initialize caching engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Cache statistics
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }
        
        # Cache configuration
        self.cache_size = config.cache_size
        self.enable_caching = config.enable_intelligent_caching
        
        # Initialize caching system
        self._setup_caching_system()
    
    def _setup_caching_system(self):
        """Setup intelligent caching system."""
        if self.enable_caching:
            # Create cached versions of processing functions
            self.insight_cache = lru_cache(maxsize=self.cache_size)(self._process_insight_uncached)
            self.pattern_cache = lru_cache(maxsize=self.cache_size // 2)(self._detect_patterns_uncached)
            self.prediction_cache = lru_cache(maxsize=self.cache_size // 4)(self._generate_prediction_uncached)
            
            # Add cache statistics tracking
            self.insight_cache = self._add_cache_stats(self.insight_cache, 'insight')
            self.pattern_cache = self._add_cache_stats(self.pattern_cache, 'pattern')
            self.prediction_cache = self._add_cache_stats(self.prediction_cache, 'prediction')
        else:
            # Use uncached versions
            self.insight_cache = self._process_insight_uncached
            self.pattern_cache = self._detect_patterns_uncached
            self.prediction_cache = self._generate_prediction_uncached
    
    def _add_cache_stats(self, cached_func: Callable, cache_type: str) -> Callable:
        """Add cache statistics tracking to cached function."""
        @wraps(cached_func)
        def wrapper(*args, **kwargs):
            self.cache_stats['total_requests'] += 1
            
            # Check if result is in cache
            cache_info = cached_func.cache_info()
            was_cached = cache_info.hits > 0
            
            if was_cached:
                self.cache_stats['hits'] += 1
            else:
                self.cache_stats['misses'] += 1
            
            return cached_func(*args, **kwargs)
        
        return wrapper
    
    def _process_insight_uncached(self, data: Dict[str, Any]) -> Optional[Any]:
        """Process insight without caching (placeholder)."""
        # This would be replaced with actual processing logic
        return {'type': 'insight', 'data': data, 'timestamp': datetime.now()}
    
    def _detect_patterns_uncached(self, data: List[Any]) -> List[Any]:
        """Detect patterns without caching (placeholder)."""
        # This would be replaced with actual pattern detection logic
        return [{'type': 'pattern', 'data': data, 'timestamp': datetime.now()}]
    
    def _generate_prediction_uncached(self, data: Dict[str, Any]) -> Optional[Any]:
        """Generate prediction without caching (placeholder)."""
        # This would be replaced with actual prediction logic
        return {'type': 'prediction', 'data': data, 'timestamp': datetime.now()}
    
    def get_cached_insight(self, data: Dict[str, Any]) -> Optional[Any]:
        """Get cached insight result."""
        if not self.enable_caching:
            return self._process_insight_uncached(data)
        
        try:
            return self.insight_cache(data)
        except Exception as e:
            self.logger.error(f"Error getting cached insight: {e}")
            return None
    
    def get_cached_patterns(self, data: List[Any]) -> List[Any]:
        """Get cached pattern detection result."""
        if not self.enable_caching:
            return self._detect_patterns_uncached(data)
        
        try:
            return self.pattern_cache(data)
        except Exception as e:
            self.logger.error(f"Error getting cached patterns: {e}")
            return []
    
    def get_cached_prediction(self, data: Dict[str, Any]) -> Optional[Any]:
        """Get cached prediction result."""
        if not self.enable_caching:
            return self._generate_prediction_uncached(data)
        
        try:
            return self.prediction_cache(data)
        except Exception as e:
            self.logger.error(f"Error getting cached prediction: {e}")
            return None
    
    def clear_cache(self, cache_type: Optional[str] = None):
        """Clear cache or specific cache type."""
        if not self.enable_caching:
            return
        
        try:
            if cache_type is None or cache_type == 'insight':
                self.insight_cache.cache_clear()
            if cache_type is None or cache_type == 'pattern':
                self.pattern_cache.cache_clear()
            if cache_type is None or cache_type == 'prediction':
                self.prediction_cache.cache_clear()
            
            self.logger.info(f"Cache cleared: {cache_type or 'all'}")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information."""
        if not self.enable_caching:
            return {'caching_enabled': False}
        
        try:
            insight_info = self.insight_cache.cache_info()
            pattern_info = self.pattern_cache.cache_info()
            prediction_info = self.prediction_cache.cache_info()
            
            return {
                'caching_enabled': True,
                'insight_cache': {
                    'hits': insight_info.hits,
                    'misses': insight_info.misses,
                    'current_size': insight_info.currsize,
                    'max_size': insight_info.maxsize
                },
                'pattern_cache': {
                    'hits': pattern_info.hits,
                    'misses': pattern_info.misses,
                    'current_size': pattern_info.currsize,
                    'max_size': pattern_info.maxsize
                },
                'prediction_cache': {
                    'hits': prediction_info.hits,
                    'misses': prediction_info.misses,
                    'current_size': prediction_info.currsize,
                    'max_size': prediction_info.maxsize
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting cache info: {e}")
            return {'caching_enabled': False, 'error': str(e)}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total_requests if total_requests > 0 else 0.0
        
        return {
            'cache_hits': self.cache_stats['hits'],
            'cache_misses': self.cache_stats['misses'],
            'hit_rate': hit_rate,
            'total_requests': total_requests,
            'evictions': self.cache_stats['evictions']
        }
    
    def optimize_cache(self):
        """Optimize cache performance."""
        if not self.enable_caching:
            return
        
        try:
            # Clear least recently used items if cache is getting full
            cache_info = self.get_cache_info()
            
            for cache_type in ['insight_cache', 'pattern_cache', 'prediction_cache']:
                if cache_type in cache_info:
                    cache_data = cache_info[cache_type]
                    utilization = cache_data['current_size'] / cache_data['max_size']
                    
                    if utilization > 0.9:  # 90% full
                        self.logger.info(f"Optimizing {cache_type} - utilization: {utilization:.2%}")
                        # In a real implementation, we might adjust cache size or clear old items
                        
        except Exception as e:
            self.logger.error(f"Error optimizing cache: {e}")
    
    def is_caching_enabled(self) -> bool:
        """Check if caching is enabled."""
        return self.enable_caching
