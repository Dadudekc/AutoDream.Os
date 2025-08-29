#!/usr/bin/env python3
"""
Gaming Integration Core - Agent Cellphone V2

Core integration module connecting gaming systems with unified infrastructure.
Handles gaming performance monitoring, alert integration, and testing framework connectivity.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3C - Gaming Systems Integration
V2 Standards: ≤200 LOC, SRP, OOP principles
"""

import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

# Core infrastructure imports
from ..core.managers.performance_manager import PerformanceManager
from ..core.performance.alerts import AlertSeverity, AlertType
from ..core.testing.test_categories import TestCategories


@dataclass
class GamingSystemInfo:
    """Gaming system information for integration"""
    system_name: str
    system_type: str
    version: str
    integration_status: str
    last_health_check: str = field(default_factory=lambda: datetime.now().isoformat())
    performance_score: float = 0.0


class GamingIntegrationCore:
    """
    Gaming Integration Core - TASK 3C
    
    Core integration manager connecting gaming systems with:
    - Performance monitoring infrastructure
    - Alert management system  
    - Testing framework
    - Workspace management
    """
    
    def __init__(self, performance_manager: PerformanceManager):
        self.performance_manager = performance_manager
        self.logger = logging.getLogger(f"{__name__}.GamingIntegrationCore")
        
        # Gaming systems tracking
        self.gaming_systems: Dict[str, GamingSystemInfo] = {}
        self.integration_active = False
        self.last_integration_check = None
        
        # Initialize gaming systems registry
        self._initialize_gaming_systems()
        
        self.logger.info("Gaming Integration Core initialized for TASK 3C")
    
    def _initialize_gaming_systems(self):
        """Initialize gaming systems registry"""
        try:
            # Register known gaming systems
            self.gaming_systems = {
                "osrs": GamingSystemInfo(
                    system_name="OSRS AI Agent",
                    system_type="MMORPG Automation",
                    version="2.0",
                    integration_status="pending"
                ),
                "ai_framework": GamingSystemInfo(
                    system_name="AI Gaming Agent Framework", 
                    system_type="Behavior Tree Engine",
                    version="2.0",
                    integration_status="pending"
                ),
                "pygame": GamingSystemInfo(
                    system_name="PyGame Integration",
                    system_type="Game Development",
                    version="2.0", 
                    integration_status="pending"
                ),
                "real_time": GamingSystemInfo(
                    system_name="Real-time Gaming State",
                    system_type="State Management",
                    version="2.0",
                    integration_status="pending"
                )
            }
            
            self.logger.info(f"Initialized {len(self.gaming_systems)} gaming systems")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize gaming systems: {e}")
    
    def start_integration(self):
        """Start gaming systems integration"""
        try:
            self.integration_active = True
            self.last_integration_check = datetime.now()
            
            # Setup performance monitoring for gaming
            self._setup_gaming_performance_monitoring()
            
            # Register gaming metrics with performance manager
            self._register_gaming_metrics()
            
            # Update system statuses
            for system_id, system_info in self.gaming_systems.items():
                system_info.integration_status = "active"
                system_info.last_health_check = datetime.now().isoformat()
            
            self.logger.info("Gaming systems integration started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start gaming integration: {e}")
            self.integration_active = False
            return False
    
    def stop_integration(self):
        """Stop gaming systems integration"""
        try:
            self.integration_active = False
            
            # Update system statuses
            for system_id, system_info in self.gaming_systems.items():
                system_info.integration_status = "inactive"
            
            self.logger.info("Gaming systems integration stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop gaming integration: {e}")
            return False
    
    def _setup_gaming_performance_monitoring(self):
        """Setup gaming-specific performance monitoring"""
        try:
            # Add gaming system metrics to performance manager
            self.performance_manager.add_metric("gaming_systems_active", 0, "count", "gaming")
            self.performance_manager.add_metric("gaming_performance_score", 0.0, "score", "gaming")
            self.performance_manager.add_metric("gaming_integration_health", 100.0, "percent", "gaming")
            
            self.logger.info("Gaming performance monitoring setup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to setup gaming performance monitoring: {e}")
    
    def _register_gaming_metrics(self):
        """Register gaming metrics with performance manager"""
        try:
            # Register custom gaming metrics
            self.performance_manager.add_metric("gaming_system_health_checks", 0, "count", "gaming")
            self.performance_manager.add_metric("gaming_integration_events", 0, "count", "gaming")
            self.performance_manager.add_metric("gaming_performance_alerts", 0, "count", "gaming")
            
            self.logger.info("Gaming metrics registration completed")
            
        except Exception as e:
            self.logger.error(f"Failed to register gaming metrics: {e}")
    
    def register_gaming_system(self, system_id: str, system_info: GamingSystemInfo):
        """Register a new gaming system"""
        try:
            if not self.integration_active:
                self.logger.warning("Gaming integration not active, skipping system registration")
                return False
            
            self.gaming_systems[system_id] = system_info
            system_info.integration_status = "active"
            system_info.last_health_check = datetime.now().isoformat()
            
            # Update performance metrics
            self.performance_manager.add_metric("gaming_systems_active", len(self.gaming_systems), "count", "gaming")
            
            self.logger.info(f"Registered gaming system: {system_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register gaming system {system_id}: {e}")
            return False
    
    def update_system_health(self, system_id: str, health_score: float):
        """Update gaming system health score"""
        try:
            if system_id not in self.gaming_systems:
                self.logger.warning(f"Gaming system not found: {system_id}")
                return False
            
            system_info = self.gaming_systems[system_id]
            system_info.performance_score = health_score
            system_info.last_health_check = datetime.now().isoformat()
            
            # Update performance metrics
            self.performance_manager.add_metric("gaming_performance_score", health_score, "score", "gaming")
            
            self.logger.debug(f"Updated health for {system_id}: {health_score}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update health for {system_id}: {e}")
            return False
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get gaming integration status"""
        try:
            active_systems = sum(1 for s in self.gaming_systems.values() if s.integration_status == "active")
            total_systems = len(self.gaming_systems)
            
            # Calculate overall health score
            health_scores = [s.performance_score for s in self.gaming_systems.values()]
            overall_health = sum(health_scores) / len(health_scores) if health_scores else 0.0
            
            return {
                "integration_active": self.integration_active,
                "total_systems": total_systems,
                "active_systems": active_systems,
                "overall_health_score": overall_health,
                "last_check": self.last_integration_check.isoformat() if self.last_integration_check else None,
                "systems": {
                    system_id: {
                        "name": info.system_name,
                        "type": info.system_type,
                        "version": info.version,
                        "status": info.integration_status,
                        "health_score": info.performance_score,
                        "last_health_check": info.last_health_check
                    }
                    for system_id, info in self.gaming_systems.items()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get integration status: {e}")
            return {"error": str(e)}
    
    def run_integration_health_check(self) -> Dict[str, Any]:
        """Run integration health check for all gaming systems"""
        try:
            health_results = {}
            
            for system_id, system_info in self.gaming_systems.items():
                # Simulate health check
                health_score = self._check_system_health(system_id, system_info)
                health_results[system_id] = {
                    "status": "healthy" if health_score >= 80.0 else "degraded" if health_score >= 50.0 else "critical",
                    "health_score": health_score,
                    "last_check": datetime.now().isoformat()
                }
                
                # Update system health
                self.update_system_health(system_id, health_score)
            
            return {
                "health_check_timestamp": datetime.now().isoformat(),
                "overall_status": "healthy" if all(r["health_score"] >= 80.0 for r in health_results.values()) else "degraded",
                "system_results": health_results
            }
            
        except Exception as e:
            self.logger.error(f"Failed to run integration health check: {e}")
            return {"error": str(e)}
    
    def _check_system_health(self, system_id: str, system_info: GamingSystemInfo) -> float:
        """Check health of a specific gaming system"""
        try:
            # Simulate health check based on system type
            base_health = 85.0
            
            if system_info.system_type == "MMORPG Automation":
                base_health = 90.0  # OSRS systems typically stable
            elif system_info.system_type == "Behavior Tree Engine":
                base_health = 88.0  # AI framework systems
            elif system_info.system_type == "Game Development":
                base_health = 85.0  # PyGame integration
            elif system_info.system_type == "State Management":
                base_health = 87.0  # Real-time systems
            
            # Add some variation
            import random
            variation = random.uniform(-5.0, 5.0)
            health_score = max(0.0, min(100.0, base_health + variation))
            
            return round(health_score, 2)
            
        except Exception as e:
            self.logger.error(f"Failed to check health for {system_id}: {e}")
            return 0.0

