#!/usr/bin/env python3
"""
Routing Manager - V2 Modular Architecture
========================================

Manages intelligent message routing strategies and optimization.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict
from pathlib import Path
import json

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from ...services.messaging import V2Message
from .models import Channel
from .types import CommunicationTypes, CommunicationConfig

logger = logging.getLogger(__name__)


class RoutingManager(BaseManager):
    """
    Routing Manager - Single responsibility: Intelligent message routing
    
    Manages:
    - Routing strategy selection
    - Load balancing algorithms
    - Priority-based routing
    - Predictive routing
    - Performance optimization
    """

    def __init__(self, config_path: str = "config/routing_manager.json"):
        """Initialize routing manager"""
        super().__init__(
            manager_name="RoutingManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.intelligent_routes: Dict[str, Dict[str, Any]] = {}
        self.routing_metrics: Dict[str, Dict[str, Any]] = {}
        self.performance_history: List[Dict[str, Any]] = []
        
        # Routing settings
        self.default_strategy = CommunicationTypes.RoutingStrategy.DIRECT
        self.enable_load_balancing = True
        self.enable_priority_routing = True
        self.enable_predictive_routing = True
        
        # Initialize routing system
        self._load_manager_config()
    
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.enable_load_balancing = config.get('enable_load_balancing', True)
                    self.enable_priority_routing = config.get('enable_priority_routing', True)
                    self.enable_predictive_routing = config.get('enable_predictive_routing', True)
            else:
                logger.warning(f"Routing config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load routing config: {e}")
    
    def create_intelligent_route(self, route_type: str, parameters: Dict[str, Any]) -> str:
        """Create an intelligent message routing strategy"""
        try:
            route_id = f"intelligent_route_{route_type}_{int(time.time())}"
            
            if route_type == CommunicationTypes.RoutingStrategy.LOAD_BALANCED.value:
                route_config = {
                    "id": route_id,
                    "type": CommunicationTypes.RoutingStrategy.LOAD_BALANCED.value,
                    "description": "Distribute messages across multiple channels for optimal performance",
                    "parameters": {
                        **parameters,
                        "distribution_strategy": parameters.get("strategy", "round_robin"),
                        "health_check_interval": parameters.get("health_check", 30),
                        "failover_enabled": parameters.get("failover", True)
                    }
                }
                
            elif route_type == CommunicationTypes.RoutingStrategy.PRIORITY_BASED.value:
                route_config = {
                    "id": route_id,
                    "type": CommunicationTypes.RoutingStrategy.PRIORITY_BASED.value,
                    "description": "Route messages based on priority and channel capabilities",
                    "parameters": {
                        **parameters,
                        "priority_mapping": parameters.get("priority_mapping", {}),
                        "channel_capabilities": parameters.get("capabilities", {}),
                        "fallback_channels": parameters.get("fallback", [])
                    }
                }
                
            elif route_type == CommunicationTypes.RoutingStrategy.PREDICTIVE.value:
                route_config = {
                    "id": route_id,
                    "type": CommunicationTypes.RoutingStrategy.PREDICTIVE.value,
                    "description": "Use ML to predict optimal routing based on historical patterns",
                    "parameters": {
                        **parameters,
                        "model_type": parameters.get("model", "simple"),
                        "training_data_hours": parameters.get("training_hours", 168),
                        "prediction_confidence": parameters.get("confidence", 0.8)
                    }
                }
                
            else:
                raise ValueError(f"Unknown route type: {route_type}")
            
            # Store route configuration
            self.intelligent_routes[route_id] = route_config
            
            # Initialize routing metrics
            self.routing_metrics[route_id] = {
                "total_routes": 0,
                "successful_routes": 0,
                "failed_routes": 0,
                "average_routing_time": 0.0,
                "last_used": None
            }
            
            self._emit_event("intelligent_route_created", {
                "route_id": route_id,
                "type": route_type
            })
            
            logger.info(f"Created intelligent message route: {route_id}")
            return route_id
            
        except Exception as e:
            logger.error(f"Failed to create intelligent message route: {e}")
            raise
    
    def execute_intelligent_routing(self, message: V2Message, route_id: str, 
                                  available_channels: List[Channel]) -> Dict[str, Any]:
        """Execute intelligent message routing strategy"""
        try:
            if route_id not in self.intelligent_routes:
                raise ValueError(f"Route configuration not found: {route_id}")
            
            route_config = self.intelligent_routes[route_id]
            route_type = route_config["type"]
            
            # Track routing start time
            start_time = datetime.now()
            
            routing_result = {
                "route_id": route_id,
                "route_type": route_type,
                "selected_channel": None,
                "routing_reason": "",
                "performance_metrics": {},
                "routing_success": False
            }
            
            if route_type == CommunicationTypes.RoutingStrategy.LOAD_BALANCED.value:
                # Select channel using load balancing
                healthy_channels = [
                    ch for ch in available_channels
                    if ch.status == CommunicationTypes.ChannelStatus.ACTIVE.value and ch.error_count < CommunicationConfig.HIGH_ERROR_THRESHOLD
                ]
                
                if healthy_channels:
                    # Simple round-robin selection
                    channel_index = len(self.performance_history) % len(healthy_channels)
                    selected_channel = healthy_channels[channel_index]
                    routing_result["selected_channel"] = selected_channel.id
                    routing_result["routing_reason"] = "Load balanced selection"
                    
            elif route_type == CommunicationTypes.RoutingStrategy.PRIORITY_BASED.value:
                # Select channel based on message priority
                message_priority = getattr(message, 'priority', CommunicationTypes.UnifiedMessagePriority.NORMAL.value)
                priority_mapping = route_config["parameters"]["priority_mapping"]
                
                if message_priority in priority_mapping:
                    target_channel_id = priority_mapping[message_priority]
                    target_channel = next(
                        (ch for ch in available_channels if ch.id == target_channel_id), None
                    )
                    if target_channel:
                        routing_result["selected_channel"] = target_channel_id
                        routing_result["routing_reason"] = f"Priority-based routing for {message_priority}"
                    
            elif route_type == CommunicationTypes.RoutingStrategy.PREDICTIVE.value:
                # Use predictive routing (simplified for now)
                # In real system, this would use ML model
                if self.performance_history:
                    # Select channel with best historical performance
                    best_channel = min(
                        available_channels,
                        key=lambda ch: sum(
                            perf["response_time"] for perf in self.performance_history
                            if perf.get("channel_id") == ch.id
                        ) or float('inf')
                    )
                    routing_result["selected_channel"] = best_channel.id
                    routing_result["routing_reason"] = "Predictive routing based on performance history"
            
            # Execute routing
            if routing_result["selected_channel"]:
                routing_result["routing_success"] = True
                
                # Update performance metrics
                routing_time = (datetime.now() - start_time).total_seconds()
                routing_result["performance_metrics"]["routing_time"] = routing_time
                routing_result["performance_metrics"]["channel_health"] = "good"
                
                # Update routing metrics
                if route_id in self.routing_metrics:
                    metrics = self.routing_metrics[route_id]
                    metrics["total_routes"] += 1
                    metrics["successful_routes"] += 1
                    metrics["last_used"] = datetime.now().isoformat()
                    
                    # Update average routing time
                    current_avg = metrics["average_routing_time"]
                    total_routes = metrics["total_routes"]
                    metrics["average_routing_time"] = (
                        (current_avg * (total_routes - 1) + routing_time) / total_routes
                    )
            
            logger.info(f"Intelligent routing executed: {route_id}")
            return routing_result
            
        except Exception as e:
            logger.error(f"Failed to execute intelligent routing: {e}")
            raise
    
    def analyze_communication_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze communication patterns for optimization insights"""
        try:
            # Get recent performance data
            recent_performance = [
                perf for perf in self.performance_history
                if perf.get("timestamp")
            ]
            
            pattern_analysis = {
                "total_routes": len(recent_performance),
                "channel_usage": {},
                "routing_strategies": {},
                "performance_metrics": {},
                "optimization_opportunities": []
            }
            
            if recent_performance:
                # Analyze channel usage
                for perf in recent_performance:
                    channel_id = perf.get("channel_id", "unknown")
                    if channel_id not in pattern_analysis["channel_usage"]:
                        pattern_analysis["channel_usage"][channel_id] = 0
                    pattern_analysis["channel_usage"][channel_id] += 1
                
                # Analyze routing strategies
                for perf in recent_performance:
                    strategy = perf.get("routing_strategy", "unknown")
                    if strategy not in pattern_analysis["routing_strategies"]:
                        pattern_analysis["routing_strategies"][strategy] = 0
                    pattern_analysis["routing_strategies"][strategy] += 1
                
                # Performance metrics
                response_times = [
                    perf.get("response_time", 0) for perf in recent_performance
                    if perf.get("response_time") is not None
                ]
                if response_times:
                    pattern_analysis["performance_metrics"]["average_response_time"] = sum(response_times) / len(response_times)
                    pattern_analysis["performance_metrics"]["min_response_time"] = min(response_times)
                    pattern_analysis["performance_metrics"]["max_response_time"] = max(response_times)
                
                # Identify optimization opportunities
                if pattern_analysis["performance_metrics"].get("average_response_time", 0) > 1.0:
                    pattern_analysis["optimization_opportunities"].append("High response time - investigate channel performance")
                
                # Check for channel bottlenecks
                for channel_id, count in pattern_analysis["channel_usage"].items():
                    if count > len(recent_performance) * 0.5:
                        pattern_analysis["optimization_opportunities"].append(f"Channel {channel_id} is overloaded - consider load balancing")
            
            logger.info(f"Communication pattern analysis completed")
            return pattern_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze communication patterns: {e}")
            return {"error": str(e)}
    
    def predict_communication_issues(self, time_horizon_hours: int = 6) -> List[Dict[str, Any]]:
        """Predict potential communication issues based on current patterns"""
        try:
            predictions = []
            pattern_analysis = self.analyze_communication_patterns(time_horizon_hours)
            
            # Check for performance degradation
            avg_response_time = pattern_analysis.get("performance_metrics", {}).get("average_response_time", 0)
            if avg_response_time > 2.0:
                prediction = {
                    "issue_type": "performance_degradation",
                    "probability": 0.8,
                    "estimated_time_to_issue": time_horizon_hours * 0.5,
                    "severity": "high" if avg_response_time > 5.0 else "medium",
                    "recommended_action": "Investigate channel health and routing efficiency"
                }
                predictions.append(prediction)
            
            # Check for channel overload
            for channel_id, message_count in pattern_analysis.get("channel_usage", {}).items():
                if message_count > 100:  # Threshold for overload
                    prediction = {
                        "issue_type": "channel_overload",
                        "channel_id": channel_id,
                        "probability": 0.7,
                        "estimated_time_to_issue": time_horizon_hours * 0.3,
                        "severity": "medium",
                        "recommended_action": f"Implement load balancing for channel {channel_id}"
                    }
                    predictions.append(prediction)
            
            # Check for routing strategy imbalances
            routing_strategies = pattern_analysis.get("routing_strategies", {})
            if len(routing_strategies) > 0:
                total_routes = sum(routing_strategies.values())
                for strategy, count in routing_strategies.items():
                    if count > total_routes * 0.7:  # 70% threshold
                        prediction = {
                            "issue_type": "routing_strategy_imbalance",
                            "strategy": strategy,
                            "probability": 0.6,
                            "estimated_time_to_issue": time_horizon_hours * 0.8,
                            "severity": "low",
                            "recommended_action": f"Review routing strategy {strategy} distribution"
                        }
                        predictions.append(prediction)
            
            logger.info(f"Communication issue prediction completed: {len(predictions)} issues identified")
            return predictions
            
        except Exception as e:
            logger.error(f"Failed to predict communication issues: {e}")
            return []
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing performance statistics"""
        try:
            total_routes = len(self.intelligent_routes)
            total_metrics = sum(
                metrics.get("total_routes", 0) 
                for metrics in self.routing_metrics.values()
            )
            successful_routes = sum(
                metrics.get("successful_routes", 0) 
                for metrics in self.routing_metrics.values()
            )
            failed_routes = sum(
                metrics.get("failed_routes", 0) 
                for metrics in self.routing_metrics.values()
            )
            
            success_rate = (successful_routes / total_metrics * 100) if total_metrics > 0 else 0
            
            return {
                "total_routes": total_routes,
                "total_metrics": total_metrics,
                "successful_routes": successful_routes,
                "failed_routes": failed_routes,
                "success_rate": success_rate,
                "routing_metrics": self.routing_metrics,
                "performance_history_count": len(self.performance_history)
            }
            
        except Exception as e:
            logger.error(f"Failed to get routing statistics: {e}")
            return {}

