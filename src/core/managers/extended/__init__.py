#!/usr/bin/env python3
"""
Extended Managers Package - Consolidates specialized functionality into BaseManager architecture

This package provides extended manager classes that inherit from BaseManager,
consolidating functionality from various duplicate implementations across the codebase.
"""

# Import extended managers from autonomous development
from .autonomous_development.reporting_manager import ExtendedReportingManager
from .autonomous_development.workflow_manager import ExtendedWorkflowManager

# Import extended managers from AI/ML
from .ai_ml.ai_manager import ExtendedAIManager
from .ai_ml.model_manager import ExtendedModelManager
from .ai_ml.api_key_manager import ExtendedAPIKeyManager
from .ai_ml.ai_agent_manager import ExtendedAIAgentManager
from .ai_ml.dev_workflow_manager import ExtendedDevWorkflowManager

# Import extended managers from financial
from .financial.portfolio_manager import ExtendedPortfolioManager
from .financial.risk_manager import ExtendedRiskManager

# Define all available extended managers
__all__ = [
    # Autonomous Development
    "ExtendedReportingManager",
    "ExtendedWorkflowManager",
    
    # AI/ML
    "ExtendedAIManager",
    "ExtendedModelManager", 
    "ExtendedAPIKeyManager",
    "ExtendedAIAgentManager",
    "ExtendedDevWorkflowManager",
    
    # Financial
    "ExtendedPortfolioManager",
    "ExtendedRiskManager",
]

# Convenience functions for creating extended managers
def create_extended_managers(config_base_path: str = "config") -> Dict[str, Any]:
    """Create all extended managers with default configurations"""
    managers = {}
    
    try:
        # Autonomous Development
        managers["reporting"] = ExtendedReportingManager(f"{config_base_path}/autonomous_development/reporting_manager.json")
        managers["workflow"] = ExtendedWorkflowManager(f"{config_base_path}/autonomous_development/workflow_manager.json")
        
        # AI/ML
        managers["ai"] = ExtendedAIManager(f"{config_base_path}/ai_ml/ai_manager.json")
        managers["model"] = ExtendedModelManager(f"{config_base_path}/ai_ml/model_manager.json")
        managers["api_key"] = ExtendedAPIKeyManager(f"{config_base_path}/ai_ml/api_key_manager.json")
        managers["ai_agent"] = ExtendedAIAgentManager(f"{config_base_path}/ai_ml/ai_agent_manager.json")
        managers["dev_workflow"] = ExtendedDevWorkflowManager(f"{config_base_path}/ai_ml/dev_workflow_manager.json")
        
        # Financial
        managers["portfolio"] = ExtendedPortfolioManager(f"{config_base_path}/financial/portfolio_manager.json")
        managers["risk"] = ExtendedRiskManager(f"{config_base_path}/financial/risk_manager.json")
        
        print(f"✅ Created {len(managers)} extended managers")
        return managers
        
    except Exception as e:
        print(f"❌ Error creating extended managers: {e}")
        return {}

def get_reporting_manager(config_path: str = "config/autonomous_development/reporting_manager.json") -> ExtendedReportingManager:
    """Get the extended reporting manager"""
    return ExtendedReportingManager(config_path)

def get_workflow_manager(config_path: str = "config/autonomous_development/workflow_manager.json") -> ExtendedWorkflowManager:
    """Get the extended workflow manager"""
    return ExtendedWorkflowManager(config_path)

def get_ai_manager(config_path: str = "config/ai_ml/ai_manager.json") -> ExtendedAIManager:
    """Get the extended AI manager"""
    return ExtendedAIManager(config_path)

def get_model_manager(config_path: str = "config/ai_ml/model_manager.json") -> ExtendedModelManager:
    """Get the extended model manager"""
    return ExtendedModelManager(config_path)

def get_api_key_manager(config_path: str = "config/ai_ml/api_key_manager.json") -> ExtendedAPIKeyManager:
    """Get the extended API key manager"""
    return ExtendedAPIKeyManager(config_path)

def get_ai_agent_manager(config_path: str = "config/ai_ml/ai_agent_manager.json") -> ExtendedAIAgentManager:
    """Get the extended AI agent manager"""
    return ExtendedAIAgentManager(config_path)

def get_dev_workflow_manager(config_path: str = "config/ai_ml/dev_workflow_manager.json") -> ExtendedDevWorkflowManager:
    """Get the extended dev workflow manager"""
    return ExtendedDevWorkflowManager(config_path)

def get_portfolio_manager(config_path: str = "config/financial/portfolio_manager.json") -> ExtendedPortfolioManager:
    """Get the extended portfolio manager"""
    return ExtendedPortfolioManager(config_path)

def get_risk_manager(config_path: str = "config/financial/risk_manager.json") -> ExtendedRiskManager:
    """Get the extended risk manager"""
    return ExtendedRiskManager(config_path)

def get_manager_by_type(manager_type: str, config_base_path: str = "config") -> Any:
    """Get a specific manager by type"""
    manager_map = {
        "reporting": get_reporting_manager,
        "workflow": get_workflow_manager,
        "ai": get_ai_manager,
        "model": get_model_manager,
        "api_key": get_api_key_manager,
        "ai_agent": get_ai_agent_manager,
        "dev_workflow": get_dev_workflow_manager,
        "portfolio": get_portfolio_manager,
        "risk": get_risk_manager,
    }
    
    if manager_type in manager_map:
        try:
            config_path = f"{config_base_path}/{manager_type}_manager.json"
            return manager_map[manager_type](config_path)
        except Exception as e:
            print(f"❌ Error creating {manager_type} manager: {e}")
            return None
    else:
        print(f"❌ Unknown manager type: {manager_type}")
        return None

def list_available_managers() -> List[str]:
    """List all available manager types"""
    return list(__all__)

def get_manager_status_summary() -> Dict[str, Dict[str, Any]]:
    """Get status summary for all extended managers"""
    try:
        managers = create_extended_managers()
        status_summary = {}
        
        for name, manager in managers.items():
            try:
                status_summary[name] = {
                    "status": manager.status.value if hasattr(manager, 'status') else "unknown",
                    "uptime": manager.get_uptime() if hasattr(manager, 'get_uptime') else 0.0,
                    "last_activity": manager.last_activity.isoformat() if hasattr(manager, 'last_activity') and manager.last_activity else None,
                    "manager_name": manager.manager_name if hasattr(manager, 'manager_name') else name
                }
            except Exception as e:
                status_summary[name] = {"error": str(e)}
        
        return status_summary
        
    except Exception as e:
        print(f"❌ Error getting manager status summary: {e}")
        return {}

# Version information
__version__ = "2.0.0"
__author__ = "V2_SWARM_CAPTAIN"
__description__ = "Extended Managers Package - V2-compliant manager consolidation"
