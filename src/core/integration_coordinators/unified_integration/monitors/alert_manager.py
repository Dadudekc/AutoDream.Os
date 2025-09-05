"""
Alert Manager
=============

Specialized component for managing monitoring alerts.
Extracted from monitor.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from typing import Dict, List, Callable, Any
from datetime import datetime

from ..models import IntegrationType, IntegrationMetrics


class AlertManager:
    """Manages monitoring alerts and notifications."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize alert manager."""
        self.config = config
        self.alert_thresholds = {
            'error_rate': 0.1,  # 10%
            'response_time': 5.0,  # 5 seconds
            'throughput': 0.5  # 0.5 requests per second
        }
        self.monitoring_callbacks: List[Callable] = []
        
    def add_callback(self, callback: Callable) -> None:
        """Add monitoring callback."""
        try:
            if callback not in self.monitoring_callbacks:
                self.monitoring_callbacks.append(callback)
        except Exception as e:
            print(f"Error adding callback: {e}")
    
    def remove_callback(self, callback: Callable) -> None:
        """Remove monitoring callback."""
        try:
            if callback in self.monitoring_callbacks:
                self.monitoring_callbacks.remove(callback)
        except Exception as e:
            print(f"Error removing callback: {e}")
    
    def check_alerts(self, metrics: IntegrationMetrics) -> List[Dict[str, Any]]:
        """Check metrics against alert thresholds."""
        alerts = []
        
        try:
            # Check error rate
            if metrics.error_rate > self.alert_thresholds['error_rate']:
                alerts.append({
                    'type': 'error_rate',
                    'integration_type': metrics.integration_type,
                    'current_value': metrics.error_rate,
                    'threshold': self.alert_thresholds['error_rate'],
                    'severity': 'high' if metrics.error_rate > 0.2 else 'medium',
                    'timestamp': datetime.now()
                })
            
            # Check response time
            if metrics.average_response_time > self.alert_thresholds['response_time']:
                alerts.append({
                    'type': 'response_time',
                    'integration_type': metrics.integration_type,
                    'current_value': metrics.average_response_time,
                    'threshold': self.alert_thresholds['response_time'],
                    'severity': 'high' if metrics.average_response_time > 10.0 else 'medium',
                    'timestamp': datetime.now()
                })
            
            # Check throughput (low throughput alert)
            if metrics.throughput < self.alert_thresholds['throughput']:
                alerts.append({
                    'type': 'throughput',
                    'integration_type': metrics.integration_type,
                    'current_value': metrics.throughput,
                    'threshold': self.alert_thresholds['throughput'],
                    'severity': 'medium',
                    'timestamp': datetime.now()
                })
            
        except Exception as e:
            print(f"Error checking alerts: {e}")
        
        return alerts
    
    def trigger_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """Trigger alert callbacks for detected alerts."""
        try:
            for alert in alerts:
                for callback in self.monitoring_callbacks:
                    try:
                        callback(alert)
                    except Exception as e:
                        print(f"Error in alert callback: {e}")
        except Exception as e:
            print(f"Error triggering alerts: {e}")
    
    def set_threshold(self, threshold_type: str, value: float) -> None:
        """Set alert threshold value."""
        try:
            if threshold_type in self.alert_thresholds:
                self.alert_thresholds[threshold_type] = value
        except Exception as e:
            print(f"Error setting threshold: {e}")
    
    def get_thresholds(self) -> Dict[str, float]:
        """Get current alert thresholds."""
        return self.alert_thresholds.copy()
    
    def get_alert_status(self) -> Dict[str, Any]:
        """Get alert manager status."""
        try:
            return {
                "thresholds": self.alert_thresholds,
                "callbacks_count": len(self.monitoring_callbacks),
                "active": True
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def cleanup(self) -> None:
        """Cleanup alert manager resources."""
        try:
            self.monitoring_callbacks.clear()
        except Exception as e:
            print(f"Alert manager cleanup failed: {e}")
