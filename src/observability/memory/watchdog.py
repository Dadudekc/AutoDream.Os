"""
Memory Watchdog System - V2_SWARM
=================================

Live monitoring watchdog with enforcement modes.
Monitors memory usage and enforces policies in real-time.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .detectors import ComprehensiveLeakDetector
from .ledger import PersistentLedgerManager
from .policies import MemoryPolicyManager

logger = logging.getLogger(__name__)


class EnforcementMode(Enum):
    """Watchdog enforcement modes"""
    
    OBSERVE = "observe"  # Monitor only, no action
    QUARANTINE = "quarantine"  # Alert and limit resources
    KILL = "kill"  # Terminate violating processes


@dataclass
class WatchdogAlert:
    """Watchdog alert data"""
    
    timestamp: float
    service_name: str
    alert_type: str  # warning, critical, emergency
    memory_mb: float
    budget_mb: float
    enforcement_action: str
    details: Dict[str, Any]


class MemoryWatchdog:
    """Live memory monitoring watchdog"""
    
    def __init__(self, policy_manager: MemoryPolicyManager, 
                 enforcement_mode: EnforcementMode = EnforcementMode.OBSERVE):
        """Initialize memory watchdog"""
        self.policy_manager = policy_manager
        self.enforcement_mode = enforcement_mode
        self.running = False
        self.alerts = []
        self.monitor_thread = None
        self.check_interval = 60  # seconds
    
    def start(self) -> bool:
        """Start watchdog monitoring"""
        if self.running:
            logger.warning("Watchdog already running")
            return False
        
        try:
            self.running = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                daemon=True
            )
            self.monitor_thread.start()
            logger.info(f"Memory watchdog started in {self.enforcement_mode.value} mode")
            return True
        except Exception as e:
            logger.error(f"Error starting watchdog: {e}")
            self.running = False
            return False
    
    def stop(self) -> bool:
        """Stop watchdog monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Memory watchdog stopped")
        return True
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.running:
            try:
                self._check_all_services()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in watchdog monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def _check_all_services(self) -> None:
        """Check all configured services"""
        snapshot = self.policy_manager.get_snapshot()
        if not snapshot:
            return
        
        # Check services against budgets
        services = ['messaging', 'autonomous_workflow', 'vector_database', 'agent_workspace']
        
        for service in services:
            result = self.policy_manager.check_service(service, snapshot.current_mb)
            
            if result.get('status') == 'warning':
                self._handle_warning(service, snapshot, result)
            elif result.get('status') == 'critical':
                self._handle_critical(service, snapshot, result)
    
    def _handle_warning(self, service: str, snapshot, result: Dict) -> None:
        """Handle warning threshold breach"""
        alert = WatchdogAlert(
            timestamp=snapshot.timestamp,
            service_name=service,
            alert_type='warning',
            memory_mb=snapshot.current_mb,
            budget_mb=result['budget_mb'],
            enforcement_action='none',
            details=result
        )
        
        self.alerts.append(alert)
        logger.warning(f"Memory warning for {service}: {snapshot.current_mb:.2f}MB")
    
    def _handle_critical(self, service: str, snapshot, result: Dict) -> None:
        """Handle critical threshold breach"""
        action = self._execute_enforcement(service, snapshot, result)
        
        alert = WatchdogAlert(
            timestamp=snapshot.timestamp,
            service_name=service,
            alert_type='critical',
            memory_mb=snapshot.current_mb,
            budget_mb=result['budget_mb'],
            enforcement_action=action,
            details=result
        )
        
        self.alerts.append(alert)
        logger.critical(f"Memory critical for {service}: {snapshot.current_mb:.2f}MB - Action: {action}")
    
    def _execute_enforcement(self, service: str, snapshot, result: Dict) -> str:
        """Execute enforcement action based on mode"""
        if self.enforcement_mode == EnforcementMode.OBSERVE:
            return "observe_only"
        
        elif self.enforcement_mode == EnforcementMode.QUARANTINE:
            return self._quarantine_service(service, snapshot)
        
        elif self.enforcement_mode == EnforcementMode.KILL:
            return self._kill_service(service, snapshot)
        
        return "none"
    
    def _quarantine_service(self, service: str, snapshot) -> str:
        """Quarantine service (limit resources)"""
        logger.warning(f"Quarantine mode: Limiting resources for {service}")
        # Hook for resource limiting
        return "quarantined"
    
    def _kill_service(self, service: str, snapshot) -> str:
        """Kill service (terminate process)"""
        logger.critical(f"Kill mode: Would terminate {service} (not implemented)")
        # Hook for process termination
        return "kill_requested"
    
    def get_recent_alerts(self, count: int = 10) -> List[WatchdogAlert]:
        """Get recent alerts"""
        return self.alerts[-count:]
    
    def clear_alerts(self) -> int:
        """Clear old alerts"""
        count = len(self.alerts)
        self.alerts = []
        return count


class IntegratedWatchdog:
    """Integrated watchdog with detectors and ledger"""
    
    def __init__(self, config_path: str = "config/memory_policy.yaml",
                 enforcement_mode: EnforcementMode = EnforcementMode.OBSERVE):
        """Initialize integrated watchdog"""
        self.policy_manager = MemoryPolicyManager(config_path)
        self.policy_manager.initialize()
        
        config = self.policy_manager.loader.config
        self.detector = ComprehensiveLeakDetector(config)
        self.ledger = PersistentLedgerManager(config)
        
        self.watchdog = MemoryWatchdog(self.policy_manager, enforcement_mode)
        self.monitoring_active = False
    
    def start_monitoring(self) -> bool:
        """Start integrated monitoring"""
        try:
            self.watchdog.start()
            self.monitoring_active = True
            logger.info("Integrated watchdog monitoring started")
            return True
        except Exception as e:
            logger.error(f"Error starting integrated monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop integrated monitoring"""
        try:
            self.watchdog.stop()
            self.policy_manager.shutdown()
            self.ledger.save_ledger()
            self.monitoring_active = False
            logger.info("Integrated watchdog monitoring stopped")
            return True
        except Exception as e:
            logger.error(f"Error stopping integrated monitoring: {e}")
            return False
    
    def run_full_check(self) -> Dict[str, Any]:
        """Run full memory check"""
        snapshot = self.policy_manager.get_snapshot()
        if not snapshot:
            return {'error': 'Failed to get snapshot'}
        
        # Add to detector
        self.detector.add_snapshot(snapshot)
        
        # Record to ledger
        self.ledger.record_snapshot('watchdog_check', snapshot)
        
        # Run leak detection
        detection_results = self.detector.run_full_detection()
        
        # Check budgets
        budget_results = {}
        for service in ['messaging', 'autonomous_workflow', 'vector_database', 'agent_workspace']:
            budget_results[service] = self.policy_manager.check_service(service, snapshot.current_mb)
        
        return {
            'snapshot': {
                'timestamp': snapshot.timestamp,
                'current_mb': snapshot.current_mb,
                'peak_mb': snapshot.peak_mb,
                'object_count': snapshot.object_count
            },
            'leak_detection': detection_results,
            'budget_checks': budget_results,
            'alerts': [
                {
                    'service': alert.service_name,
                    'type': alert.alert_type,
                    'memory_mb': alert.memory_mb,
                    'action': alert.enforcement_action
                }
                for alert in self.watchdog.get_recent_alerts(5)
            ]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get watchdog status"""
        return {
            'monitoring_active': self.monitoring_active,
            'enforcement_mode': self.watchdog.enforcement_mode.value,
            'alert_count': len(self.watchdog.alerts),
            'check_interval': self.watchdog.check_interval,
            'policy_initialized': self.policy_manager.initialized
        }


class WatchdogManager:
    """Manage watchdog lifecycle and configuration"""
    
    def __init__(self):
        """Initialize watchdog manager"""
        self.watchdogs = {}
        self.active_count = 0
    
    def create_watchdog(self, name: str, config_path: str = "config/memory_policy.yaml",
                       enforcement_mode: EnforcementMode = EnforcementMode.OBSERVE) -> IntegratedWatchdog:
        """Create and register watchdog"""
        watchdog = IntegratedWatchdog(config_path, enforcement_mode)
        self.watchdogs[name] = watchdog
        return watchdog
    
    def start_all(self) -> Dict[str, bool]:
        """Start all watchdogs"""
        results = {}
        for name, watchdog in self.watchdogs.items():
            results[name] = watchdog.start_monitoring()
            if results[name]:
                self.active_count += 1
        return results
    
    def stop_all(self) -> Dict[str, bool]:
        """Stop all watchdogs"""
        results = {}
        for name, watchdog in self.watchdogs.items():
            results[name] = watchdog.stop_monitoring()
            if results[name]:
                self.active_count = max(0, self.active_count - 1)
        return results
    
    def get_watchdog(self, name: str) -> Optional[IntegratedWatchdog]:
        """Get watchdog by name"""
        return self.watchdogs.get(name)
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get status of all watchdogs"""
        return {
            'watchdog_count': len(self.watchdogs),
            'active_count': self.active_count,
            'watchdogs': {
                name: watchdog.get_status()
                for name, watchdog in self.watchdogs.items()
            }
        }

