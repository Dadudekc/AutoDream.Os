#!/usr/bin/env python3
"""
Strategic Oversight Engine - V2 Compliant Redirect
=================================================

V2 compliance redirect to modular strategic oversight engine.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular strategic oversight engine
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .engine_core import StrategicOversightEngineCore
from .engine_services import StrategicOversightEngineServices

# Backward compatibility - create main engine class
class StrategicOversightEngine:
    """Main strategic oversight engine - V2 compliant wrapper."""
    
    def __init__(self):
        """Initialize strategic oversight engine."""
        self.core = StrategicOversightEngineCore()
        self.services = StrategicOversightEngineServices(self.core)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the engine."""
        try:
            if not self.core.initialize():
                return False
            if not self.services.initialize():
                return False
            
            self.is_initialized = True
            return True
        except Exception as e:
            return False
    
    # Delegate core methods
    def add_report(self, report):
        return self.core.add_report(report)
    
    def get_report(self, report_id):
        return self.core.get_report(report_id)
    
    def get_reports_by_type(self, report_type):
        return self.core.get_reports_by_type(report_type)
    
    def add_insight(self, insight):
        return self.core.add_insight(insight)
    
    def get_insight(self, insight_id):
        return self.core.get_insight(insight_id)
    
    def get_insights_by_type(self, insight_type):
        return self.core.get_insights_by_type(insight_type)
    
    def add_recommendation(self, recommendation):
        return self.core.add_recommendation(recommendation)
    
    def get_recommendation(self, recommendation_id):
        return self.core.get_recommendation(recommendation_id)
    
    def add_agent_metrics(self, metrics):
        return self.core.add_agent_metrics(metrics)
    
    def get_agent_metrics(self, agent_id=None):
        return self.core.get_agent_metrics(agent_id)
    
    def add_coordination_status(self, status):
        return self.core.add_coordination_status(status)
    
    def get_coordination_status(self, status_id):
        return self.core.get_coordination_status(status_id)
    
    def add_mission(self, mission):
        return self.core.add_mission(mission)
    
    def get_mission(self, mission_id):
        return self.core.get_mission(mission_id)
    
    def get_missions_by_status(self, status):
        return self.core.get_missions_by_status(status)
    
    def add_vector_metrics(self, metrics):
        return self.core.add_vector_metrics(metrics)
    
    def get_vector_metrics(self, database_name=None):
        return self.core.get_vector_metrics(database_name)
    
    def add_system_health(self, health):
        return self.core.add_system_health(health)
    
    def get_system_health(self, component=None):
        return self.core.get_system_health(component)
    
    # Delegate service methods
    def generate_comprehensive_report(self, report_type=None):
        return self.services.generate_comprehensive_report(report_type)
    
    def analyze_performance_trends(self, days=7):
        return self.services.analyze_performance_trends(days)
    
    def generate_insights_summary(self):
        return self.services.generate_insights_summary()
    
    def generate_recommendations_summary(self):
        return self.services.generate_recommendations_summary()
    
    def generate_mission_status_summary(self):
        return self.services.generate_mission_status_summary()
    
    def generate_system_health_summary(self):
        return self.services.generate_system_health_summary()
    
    def get_engine_status(self):
        return self.core.get_engine_status()
    
    def cleanup_old_data(self, days=30):
        return self.core.cleanup_old_data(days)
    
    def shutdown(self):
        """Shutdown engine."""
        if not self.is_initialized:
            return
        
        self.services.shutdown()
        self.core.shutdown()
        self.is_initialized = False

# Re-export for backward compatibility
__all__ = [
    'StrategicOversightEngine',
    'StrategicOversightEngineCore',
    'StrategicOversightEngineServices'
]