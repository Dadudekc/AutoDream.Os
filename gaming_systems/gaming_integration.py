"""
Gaming Systems Integration Module

Integrates gaming systems with core infrastructure for TASK 3C.
Connects gaming performance, alerts, and testing with unified systems.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3C - Gaming Systems Integration
V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""

import logging
import time
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Core infrastructure imports
from src.core.managers.performance_manager import PerformanceManager
from src.core.performance.alerts import AlertSeverity, AlertType
from src.core.testing.test_categories import TestCategories
from src.core.base_manager import BaseManager, ManagerStatus, ManagerPriority


@dataclass
class GamingPerformanceMetrics:
    """Gaming performance metrics for integration"""
    frame_rate: float
    response_time: float
    memory_usage: float
    cpu_usage: float
    gpu_usage: float
    network_latency: float
    game_state: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GamingAlert:
    """Gaming-specific alert for integration"""
    alert_id: str
    alert_type: str
    severity: AlertSeverity
    message: str
    game_context: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class GamingIntegrationManager(BaseManager):
    """
    Gaming Integration Manager - TASK 3C
    
    Integrates gaming systems with:
    - Performance monitoring infrastructure
    - Alert management system
    - Testing framework
    - Workspace management
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self, performance_manager: PerformanceManager):
        """Initialize gaming integration manager with BaseManager"""
        super().__init__(
            manager_id="gaming_integration_manager",
            name="Gaming Integration Manager",
            description="Integrates gaming systems with core infrastructure"
        )
        
        self.performance_manager = performance_manager
        
        # Gaming performance tracking
        self.gaming_metrics: List[GamingPerformanceMetrics] = []
        self.gaming_alerts: List[GamingAlert] = []
        
        # Integration status
        self.integration_active = False
        self.last_integration_check = None
        
        self.logger.info("Gaming Integration Manager initialized for TASK 3C")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize gaming integration system"""
        try:
            self.logger.info("Starting Gaming Integration Manager...")
            
            # Start integration
            if not self.start_integration():
                raise RuntimeError("Failed to start gaming integration")
            
            self.logger.info("Gaming Integration Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Gaming Integration Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup gaming integration system"""
        try:
            self.logger.info("Stopping Gaming Integration Manager...")
            
            # Stop integration
            self.stop_integration()
            
            # Clear data
            self.gaming_metrics.clear()
            self.gaming_alerts.clear()
            
            self.logger.info("Gaming Integration Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Gaming Integration Manager: {e}")
    
    def _on_heartbeat(self):
        """Gaming integration manager heartbeat"""
        try:
            # Check integration health
            if self.integration_active:
                self._check_integration_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize gaming integration resources"""
        try:
            # Initialize data structures
            self.gaming_metrics = []
            self.gaming_alerts = []
            
            # Set initial status
            self.integration_active = False
            self.last_integration_check = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup gaming integration resources"""
        try:
            # Clear data
            self.gaming_metrics.clear()
            self.gaming_alerts.clear()
            
            # Reset status
            self.integration_active = False
            self.last_integration_check = None
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Restart integration
            if self.integration_active:
                self.stop_integration()
                time.sleep(1)  # Brief pause
            
            if self.start_integration():
                self.logger.info("Recovery successful")
                return True
            else:
                self.logger.error("Recovery failed - could not restart integration")
                return False
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Gaming Integration Management Methods
    # ============================================================================
    
    def start_integration(self):
        """Start gaming systems integration"""
        try:
            self.integration_active = True
            self.last_integration_check = datetime.now()
            
            # Initialize performance monitoring for gaming
            self._setup_gaming_performance_monitoring()
            
            # Setup gaming alert thresholds
            self._setup_gaming_alert_thresholds()
            
            # Register gaming metrics with performance manager
            self._register_gaming_metrics()
            
            # Record operation
            self.record_operation("start_integration", True, 0.0)
            
            self.logger.info("Gaming systems integration started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start gaming integration: {e}")
            self.integration_active = False
            self.record_operation("start_integration", False, 0.0)
            return False
    
    def stop_integration(self):
        """Stop gaming systems integration"""
        try:
            self.integration_active = False
            
            # Record operation
            self.record_operation("stop_integration", True, 0.0)
            
            self.logger.info("Gaming systems integration stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop gaming integration: {e}")
            self.record_operation("stop_integration", False, 0.0)
            return False
    
    def _setup_gaming_performance_monitoring(self):
        """Setup gaming-specific performance monitoring"""
        try:
            # Add gaming-specific metrics to performance manager
            self.performance_manager.add_metric("gaming_frame_rate", 0.0, "fps", "gaming")
            self.performance_manager.add_metric("gaming_response_time", 0.0, "ms", "gaming")
            self.performance_manager.add_metric("gaming_memory_usage", 0.0, "MB", "gaming")
            self.performance_manager.add_metric("gaming_cpu_usage", 0.0, "percent", "gaming")
            self.performance_manager.add_metric("gaming_gpu_usage", 0.0, "percent", "gaming")
            self.performance_manager.add_metric("gaming_network_latency", 0.0, "ms", "gaming")
            
            self.logger.info("Gaming performance monitoring setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup gaming performance monitoring: {e}")
    
    def _setup_gaming_alert_thresholds(self):
        """Setup gaming-specific alert thresholds"""
        try:
            # Set gaming performance thresholds
            self.performance_manager.set_alert_threshold("gaming_frame_rate", "warning", 30.0)
            self.performance_manager.set_alert_threshold("gaming_frame_rate", "error", 15.0)
            self.performance_manager.set_alert_threshold("gaming_frame_rate", "critical", 5.0)
            
            self.performance_manager.set_alert_threshold("gaming_response_time", "warning", 100.0)
            self.performance_manager.set_alert_threshold("gaming_response_time", "error", 200.0)
            self.performance_manager.set_alert_threshold("gaming_response_time", "critical", 500.0)
            
            self.performance_manager.set_alert_threshold("gaming_memory_usage", "warning", 2048.0)
            self.performance_manager.set_alert_threshold("gaming_memory_usage", "error", 4096.0)
            self.performance_manager.set_alert_threshold("gaming_memory_usage", "critical", 8192.0)
            
            self.logger.info("Gaming alert thresholds setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup gaming alert thresholds: {e}")
    
    def _register_gaming_metrics(self):
        """Register gaming metrics with performance manager"""
        try:
            # Register custom gaming metrics
            self.performance_manager.add_metric("gaming_state_changes", 0, "count", "gaming")
            self.performance_manager.add_metric("gaming_ai_decisions", 0, "count", "gaming")
            self.performance_manager.add_metric("gaming_screen_analysis", 0, "count", "gaming")
            
            self.logger.info("Gaming metrics registration completed")
            
        except Exception as e:
            self.logger.error(f"Failed to register gaming metrics: {e}")
    
    def update_gaming_metrics(self, metrics: GamingPerformanceMetrics):
        """Update gaming performance metrics"""
        try:
            if not self.integration_active:
                self.logger.warning("Gaming integration not active, skipping metrics update")
                return False
            
            # Store metrics locally
            self.gaming_metrics.append(metrics)
            
            # Update performance manager
            self.performance_manager.add_metric("gaming_frame_rate", metrics.frame_rate, "fps", "gaming")
            self.performance_manager.add_metric("gaming_response_time", metrics.response_time, "ms", "gaming")
            self.performance_manager.add_metric("gaming_memory_usage", metrics.memory_usage, "MB", "gaming")
            self.performance_manager.add_metric("gaming_cpu_usage", metrics.cpu_usage, "percent", "gaming")
            self.performance_manager.add_metric("gaming_gpu_usage", metrics.gpu_usage, "percent", "gaming")
            self.performance_manager.add_metric("gaming_network_latency", metrics.network_latency, "ms", "gaming")
            
            # Check for alerts
            self._check_gaming_alerts(metrics)
            
            # Record operation
            self.record_operation("update_gaming_metrics", True, 0.0)
            
            self.logger.debug(f"Updated gaming metrics: {metrics.game_state} - {metrics.frame_rate}fps")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update gaming metrics: {e}")
            self.record_operation("update_gaming_metrics", False, 0.0)
            return False
    
    def _check_gaming_alerts(self, metrics: GamingPerformanceMetrics):
        """Check gaming metrics for alert conditions"""
        try:
            # Frame rate alerts
            if metrics.frame_rate < 5.0:
                self._create_gaming_alert("critical", "gaming_frame_rate", 
                                        f"Critical frame rate: {metrics.frame_rate}fps", metrics)
            elif metrics.frame_rate < 15.0:
                self._create_gaming_alert("error", "gaming_frame_rate", 
                                        f"Low frame rate: {metrics.frame_rate}fps", metrics)
            elif metrics.frame_rate < 30.0:
                self._create_gaming_alert("warning", "gaming_frame_rate", 
                                        f"Suboptimal frame rate: {metrics.frame_rate}fps", metrics)
            
            # Response time alerts
            if metrics.response_time > 500.0:
                self._create_gaming_alert("critical", "gaming_response_time", 
                                        f"Critical response time: {metrics.response_time}ms", metrics)
            elif metrics.response_time > 200.0:
                self._create_gaming_alert("error", "gaming_response_time", 
                                        f"High response time: {metrics.response_time}ms", metrics)
            elif metrics.response_time > 100.0:
                self._create_gaming_alert("warning", "gaming_response_time", 
                                        f"Elevated response time: {metrics.response_time}ms", metrics)
            
            # Memory usage alerts
            if metrics.memory_usage > 8192.0:
                self._create_gaming_alert("critical", "gaming_memory_usage", 
                                        f"Critical memory usage: {metrics.memory_usage}MB", metrics)
            elif metrics.memory_usage > 4096.0:
                self._create_gaming_alert("error", "gaming_memory_usage", 
                                        f"High memory usage: {metrics.memory_usage}MB", metrics)
            elif metrics.memory_usage > 2048.0:
                self._create_gaming_alert("warning", "gaming_memory_usage", 
                                        f"Elevated memory usage: {metrics.memory_usage}MB", metrics)
                
        except Exception as e:
            self.logger.error(f"Failed to check gaming alerts: {e}")
    
    def _create_gaming_alert(self, severity: str, alert_type: str, message: str, metrics: GamingPerformanceMetrics):
        """Create a gaming-specific alert"""
        try:
            alert = GamingAlert(
                alert_id=f"gaming_{int(time.time())}",
                alert_type=alert_type,
                severity=AlertSeverity(severity.upper()),
                message=message,
                game_context={
                    "game_state": metrics.game_state,
                    "frame_rate": metrics.frame_rate,
                    "response_time": metrics.response_time,
                    "memory_usage": metrics.memory_usage,
                    "timestamp": metrics.timestamp
                }
            )
            
            self.gaming_alerts.append(alert)
            self.logger.warning(f"Gaming alert created: {severity} - {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to create gaming alert: {e}")
    
    def get_gaming_performance_summary(self) -> Dict[str, Any]:
        """Get gaming performance summary"""
        try:
            if not self.gaming_metrics:
                return {"error": "No gaming metrics available"}
            
            latest_metrics = self.gaming_metrics[-1]
            
            summary = {
                "integration_status": "active" if self.integration_active else "inactive",
                "last_update": latest_metrics.timestamp,
                "current_metrics": {
                    "frame_rate": latest_metrics.frame_rate,
                    "response_time": latest_metrics.response_time,
                    "memory_usage": latest_metrics.memory_usage,
                    "cpu_usage": latest_metrics.cpu_usage,
                    "gpu_usage": latest_metrics.gpu_usage,
                    "network_latency": latest_metrics.network_latency,
                    "game_state": latest_metrics.game_state
                },
                "total_metrics_collected": len(self.gaming_metrics),
                "total_alerts_generated": len(self.gaming_alerts),
                "integration_duration": self._get_integration_duration()
            }
            
            # Record operation
            self.record_operation("get_gaming_performance_summary", True, 0.0)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get gaming performance summary: {e}")
            self.record_operation("get_gaming_performance_summary", False, 0.0)
            return {"error": str(e)}
    
    def _get_integration_duration(self) -> Optional[str]:
        """Get integration duration"""
        try:
            if self.last_integration_check:
                duration = datetime.now() - self.last_integration_check
                return str(duration)
            return None
        except Exception as e:
            self.logger.error(f"Failed to calculate integration duration: {e}")
            return None
    
    def run_gaming_integration_tests(self) -> Dict[str, Any]:
        """Run gaming integration tests"""
        try:
            test_results = {
                "performance_monitoring": self._test_performance_monitoring(),
                "alert_system": self._test_alert_system(),
                "metric_registration": self._test_metric_registration(),
                "integration_status": self._test_integration_status()
            }
            
            overall_success = all(result.get("success", False) for result in test_results.values())
            
            # Record operation
            self.record_operation("run_gaming_integration_tests", overall_success, 0.0)
            
            return {
                "overall_success": overall_success,
                "test_results": test_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to run gaming integration tests: {e}")
            self.record_operation("run_gaming_integration_tests", False, 0.0)
            return {"error": str(e), "overall_success": False}
    
    def _test_performance_monitoring(self) -> Dict[str, Any]:
        """Test performance monitoring integration"""
        try:
            # Test metric addition
            test_metric = GamingPerformanceMetrics(
                frame_rate=60.0,
                response_time=16.67,
                memory_usage=1024.0,
                cpu_usage=25.0,
                gpu_usage=30.0,
                network_latency=50.0,
                game_state="test"
            )
            
            success = self.update_gaming_metrics(test_metric)
            
            return {
                "success": success,
                "test_type": "performance_monitoring",
                "details": "Gaming metrics integration test"
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_type": "performance_monitoring",
                "error": str(e)
            }
    
    def _test_alert_system(self) -> Dict[str, Any]:
        """Test alert system integration"""
        try:
            # Test alert creation
            test_metrics = GamingPerformanceMetrics(
                frame_rate=2.0,  # Critical frame rate
                response_time=1000.0,  # Critical response time
                memory_usage=1024.0,
                cpu_usage=25.0,
                gpu_usage=30.0,
                network_latency=50.0,
                game_state="test"
            )
            
            self._check_gaming_alerts(test_metrics)
            
            alerts_generated = len([a for a in self.gaming_alerts if "test" in a.game_context.get("game_state", "")])
            
            return {
                "success": alerts_generated > 0,
                "test_type": "alert_system",
                "details": f"Generated {alerts_generated} test alerts"
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_type": "alert_system",
                "error": str(e)
            }
    
    def _test_metric_registration(self) -> Dict[str, Any]:
        """Test metric registration with performance manager"""
        try:
            # Test if gaming metrics are accessible
            summary = self.performance_manager.get_performance_summary()
            
            success = "gaming_frame_rate" in str(summary)
            
            return {
                "success": success,
                "test_type": "metric_registration",
                "details": "Gaming metrics registration verification"
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_type": "metric_registration",
                "error": str(e)
            }
    
    def _test_integration_status(self) -> Dict[str, Any]:
        """Test overall integration status"""
        try:
            return {
                "success": self.integration_active,
                "test_type": "integration_status",
                "details": f"Integration active: {self.integration_active}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_type": "integration_status",
                "error": str(e)
            }
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _check_integration_health(self):
        """Check integration health status"""
        try:
            # Check if performance manager is accessible
            if not hasattr(self.performance_manager, 'get_performance_summary'):
                self.logger.warning("Performance manager not accessible")
                return False
            
            # Check if metrics are being collected
            if len(self.gaming_metrics) == 0:
                self.logger.debug("No gaming metrics collected yet")
                return True
            
            # Check if recent metrics exist
            latest_metric = self.gaming_metrics[-1]
            metric_age = (datetime.now() - datetime.fromisoformat(latest_metric.timestamp)).total_seconds()
            
            if metric_age > 300:  # 5 minutes
                self.logger.warning(f"Gaming metrics are stale: {metric_age}s old")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to check integration health: {e}")
            return False

