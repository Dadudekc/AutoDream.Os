#!/usr/bin/env python3
"""
Monitoring Service
=================

Performance monitoring and system health tracking for benchmarking.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

from .models import SystemHealth


class MonitoringService:
    """Performance monitoring and system health tracking service"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.health_history: List[SystemHealth] = []
        self.max_history_size = 100
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def start_performance_monitoring(self) -> Dict[str, Any]:
        """Start continuous performance monitoring"""
        if self.is_monitoring:
            return {"error": "Performance monitoring already active"}
        
        self.is_monitoring = True
        self.logger.info("Starting performance monitoring...")
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._performance_monitor_loop, daemon=True)
        self.monitoring_thread.start()
        
        return {"success": True, "message": "Performance monitoring started"}
    
    def stop_performance_monitoring(self) -> Dict[str, Any]:
        """Stop performance monitoring"""
        self.is_monitoring = False
        self.logger.info("Stopping performance monitoring...")
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        return {"success": True, "message": "Performance monitoring stopped"}
    
    def _performance_monitor_loop(self):
        """Main performance monitoring loop"""
        while self.is_monitoring:
            try:
                # Perform system health check
                system_health = self._check_system_health()
                
                # Store health data
                self._store_health_data(system_health)
                
                # Log if issues detected
                if system_health.status != "healthy":
                    self.logger.warning(f"System health issue: {system_health}")
                
                # Sleep before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Performance monitor error: {e}")
                time.sleep(120)  # Wait longer on error
    
    def _check_system_health(self) -> SystemHealth:
        """Check overall system health"""
        try:
            # Check memory usage
            memory_usage = self._get_memory_usage()
            memory_status = "healthy" if memory_usage < 1000 else "warning"  # 1GB threshold
            
            # Check CPU usage
            cpu_usage = self._get_cpu_usage()
            cpu_status = "healthy" if cpu_usage < 80 else "warning"  # 80% threshold
            
            # Overall status
            overall_status = "healthy"
            if memory_status == "warning" or cpu_status == "warning":
                overall_status = "warning"
            
            return SystemHealth(
                status=overall_status,
                memory={"usage": memory_usage, "status": memory_status},
                cpu={"usage": cpu_usage, "status": cpu_status},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return SystemHealth(
                status="error",
                memory={"usage": 0, "status": "unknown"},
                cpu={"usage": 0, "status": "unknown"},
                timestamp=datetime.now(),
                error=str(e)
            )
    
    def _store_health_data(self, health: SystemHealth):
        """Store health data in history"""
        self.health_history.append(health)
        
        # Maintain history size limit
        if len(self.health_history) > self.max_history_size:
            self.health_history.pop(0)
    
    def get_system_health(self) -> SystemHealth:
        """Get current system health status"""
        return self._check_system_health()
    
    def get_health_history(self, limit: Optional[int] = None) -> List[SystemHealth]:
        """Get system health history"""
        if limit is None:
            return self.health_history.copy()
        else:
            return self.health_history[-limit:] if self.health_history else []
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health monitoring summary"""
        if not self.health_history:
            return {"status": "no_data", "message": "No health data available"}
        
        recent_health = self.health_history[-10:]  # Last 10 checks
        
        # Calculate statistics
        healthy_count = sum(1 for h in recent_health if h.status == "healthy")
        warning_count = sum(1 for h in recent_health if h.status == "warning")
        error_count = sum(1 for h in recent_health if h.status == "error")
        
        # Calculate average memory and CPU usage
        memory_usage = [h.memory["usage"] for h in recent_health if "usage" in h.memory]
        cpu_usage = [h.cpu["usage"] for h in recent_health if "usage" in h.cpu]
        
        avg_memory = sum(memory_usage) / len(memory_usage) if memory_usage else 0
        avg_cpu = sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0
        
        return {
            "monitoring_status": "active" if self.is_monitoring else "inactive",
            "recent_checks": len(recent_health),
            "health_distribution": {
                "healthy": healthy_count,
                "warning": warning_count,
                "error": error_count
            },
            "average_usage": {
                "memory_mb": round(avg_memory, 2),
                "cpu_percent": round(avg_cpu, 2)
            },
            "last_check": recent_health[-1].timestamp.isoformat() if recent_health else None
        }
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0
        except Exception:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0
    
    def cleanup(self):
        """Cleanup monitoring resources"""
        self.stop_performance_monitoring()
