#!/usr/bin/env python3
"""
V3-015: Monitoring Targets
==========================

Monitoring target management for production monitoring.
V2 compliant with focus on target health checking.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from v3.v3_015_monitoring_metrics import MonitorStatus, MonitorTarget


class HealthCheckType(Enum):
    """Health check types."""
    HTTP = "http"
    TCP = "tcp"
    PING = "ping"
    CUSTOM = "custom"


@dataclass
class HealthCheckResult:
    """Health check result."""
    target_id: str
    success: bool
    response_time_ms: float
    status_code: Optional[int]
    error_message: Optional[str]
    checked_at: datetime


class TargetManager:
    """Manages monitoring targets."""
    
    def __init__(self):
        self.targets = {}
        self.health_check_results = []
        self.check_interval = 30  # seconds
        self.timeout = 10  # seconds
    
    def register_target(self, target_id: str, name: str, endpoint: str,
                       check_interval: int = 30, timeout: int = 10) -> MonitorTarget:
        """Register monitoring target."""
        target = MonitorTarget(
            target_id=target_id,
            name=name,
            endpoint=endpoint,
            check_interval=check_interval,
            timeout=timeout,
            status=MonitorStatus.ACTIVE
        )
        
        self.targets[target_id] = target
        print(f"🎯 Registered target: {name} ({endpoint})")
        return target
    
    def get_target(self, target_id: str) -> Optional[MonitorTarget]:
        """Get target by ID."""
        return self.targets.get(target_id)
    
    def get_all_targets(self) -> List[MonitorTarget]:
        """Get all targets."""
        return list(self.targets.values())
    
    def get_active_targets(self) -> List[MonitorTarget]:
        """Get active targets."""
        return [t for t in self.targets.values() if t.status == MonitorStatus.ACTIVE]
    
    def update_target_status(self, target_id: str, status: MonitorStatus) -> bool:
        """Update target status."""
        if target_id in self.targets:
            self.targets[target_id].status = status
            print(f"🔄 Updated {target_id} status to {status.value}")
            return True
        return False
    
    def perform_health_check(self, target: MonitorTarget) -> HealthCheckResult:
        """Perform health check on target."""
        start_time = time.time()
        
        try:
            # Simulate health check (replace with actual implementation)
            if target.endpoint.startswith("http"):
                success, status_code, error = self._check_http_endpoint(target.endpoint)
            else:
                success, status_code, error = self._check_tcp_endpoint(target.endpoint)
            
            response_time = (time.time() - start_time) * 1000
            
            result = HealthCheckResult(
                target_id=target.target_id,
                success=success,
                response_time_ms=response_time,
                status_code=status_code,
                error_message=error,
                checked_at=datetime.now()
            )
            
            # Update target based on result
            if success:
                target.error_count = 0
                target.status = MonitorStatus.ACTIVE
            else:
                target.error_count += 1
                if target.error_count >= 3:
                    target.status = MonitorStatus.ERROR
            
            target.last_check = result.checked_at
            self.health_check_results.append(result)
            
            return result
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            result = HealthCheckResult(
                target_id=target.target_id,
                success=False,
                response_time_ms=response_time,
                status_code=None,
                error_message=str(e),
                checked_at=datetime.now()
            )
            
            target.error_count += 1
            target.last_check = result.checked_at
            self.health_check_results.append(result)
            
            return result
    
    def _check_http_endpoint(self, endpoint: str) -> tuple[bool, Optional[int], Optional[str]]:
        """Check HTTP endpoint (simplified)."""
        # In real implementation, use requests library
        # For now, simulate based on endpoint
        if "healthy" in endpoint or "status" in endpoint:
            return True, 200, None
        elif "error" in endpoint:
            return False, 500, "Simulated error"
        else:
            return True, 200, None
    
    def _check_tcp_endpoint(self, endpoint: str) -> tuple[bool, Optional[int], Optional[str]]:
        """Check TCP endpoint (simplified)."""
        # In real implementation, use socket library
        # For now, simulate based on endpoint
        if "localhost" in endpoint:
            return True, None, None
        else:
            return False, None, "Connection failed"
    
    def check_all_targets(self) -> List[HealthCheckResult]:
        """Check all active targets."""
        results = []
        active_targets = self.get_active_targets()
        
        for target in active_targets:
            result = self.perform_health_check(target)
            results.append(result)
        
        return results
    
    def get_target_health_summary(self) -> Dict[str, Any]:
        """Get target health summary."""
        active_targets = self.get_active_targets()
        total_targets = len(self.targets)
        
        if not active_targets:
            return {"error": "No active targets"}
        
        # Calculate health metrics
        healthy_count = sum(1 for t in active_targets if t.error_count == 0)
        unhealthy_count = total_targets - healthy_count
        
        # Get recent results
        recent_results = [r for r in self.health_check_results 
                         if r.checked_at > datetime.now() - timedelta(minutes=5)]
        
        avg_response_time = 0
        if recent_results:
            avg_response_time = sum(r.response_time_ms for r in recent_results) / len(recent_results)
        
        return {
            "total_targets": total_targets,
            "active_targets": len(active_targets),
            "healthy_targets": healthy_count,
            "unhealthy_targets": unhealthy_count,
            "health_percentage": (healthy_count / total_targets) * 100 if total_targets > 0 else 0,
            "average_response_time_ms": round(avg_response_time, 2),
            "recent_checks": len(recent_results),
            "last_check": max(r.checked_at for r in recent_results).isoformat() if recent_results else None
        }
    
    def get_target_by_status(self, status: MonitorStatus) -> List[MonitorTarget]:
        """Get targets by status."""
        return [t for t in self.targets.values() if t.status == status]
    
    def remove_target(self, target_id: str) -> bool:
        """Remove target."""
        if target_id in self.targets:
            del self.targets[target_id]
            print(f"🗑️ Removed target: {target_id}")
            return True
        return False


class HealthCheckScheduler:
    """Schedules and manages health checks."""
    
    def __init__(self, target_manager: TargetManager):
        self.target_manager = target_manager
        self.scheduler_active = False
        self.check_thread = None
    
    def start_scheduler(self):
        """Start health check scheduler."""
        self.scheduler_active = True
        print("⏰ Health check scheduler started")
    
    def stop_scheduler(self):
        """Stop health check scheduler."""
        self.scheduler_active = False
        print("⏹️ Health check scheduler stopped")
    
    def run_scheduled_checks(self) -> List[HealthCheckResult]:
        """Run scheduled health checks."""
        if not self.scheduler_active:
            return []
        
        return self.target_manager.check_all_targets()
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        return {
            "active": self.scheduler_active,
            "targets_monitored": len(self.target_manager.get_active_targets()),
            "check_interval": self.target_manager.check_interval,
            "timeout": self.target_manager.timeout
        }


def main():
    """Main execution function."""
    print("🎯 V3-015 Monitoring Targets - Testing...")
    
    # Initialize target manager
    target_manager = TargetManager()
    
    # Register sample targets
    target1 = target_manager.register_target("web_server", "Web Server", "http://localhost:8080/health")
    target2 = target_manager.register_target("api_server", "API Server", "http://localhost:3000/status")
    target3 = target_manager.register_target("db_server", "Database Server", "tcp://localhost:5432")
    
    # Perform health checks
    print("\n🏥 Performing health checks...")
    results = target_manager.check_all_targets()
    
    for result in results:
        status = "✅" if result.success else "❌"
        print(f"   {result.target_id}: {status} ({result.response_time_ms:.2f}ms)")
    
    # Get health summary
    summary = target_manager.get_target_health_summary()
    
    print(f"\n📊 Target Health Summary:")
    print(f"   Total Targets: {summary['total_targets']}")
    print(f"   Active Targets: {summary['active_targets']}")
    print(f"   Healthy Targets: {summary['healthy_targets']}")
    print(f"   Health Percentage: {summary['health_percentage']:.1f}%")
    print(f"   Avg Response Time: {summary['average_response_time_ms']}ms")
    
    # Test scheduler
    scheduler = HealthCheckScheduler(target_manager)
    scheduler.start_scheduler()
    
    scheduler_status = scheduler.get_scheduler_status()
    print(f"\n⏰ Scheduler Status:")
    print(f"   Active: {scheduler_status['active']}")
    print(f"   Targets Monitored: {scheduler_status['targets_monitored']}")
    
    print("\n✅ V3-015 Monitoring Targets completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

