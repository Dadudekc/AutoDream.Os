"""
🎯 AI/ML INTERFACES - CONSOLIDATED
Agent-7 - Interface Systems Consolidation Specialist

Consolidated AI/ML interface definitions.
Sources: 
- src/managers/ai_ml/interfaces/
- agent_workspaces/meeting/src/ai_ml/interfaces/

Agent: Agent-7 (Interface Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Interface System

Author: Agent-7 - Quality Completion Optimization Manager
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    """Agent status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"


class ModelType(Enum):
    """Model type enumeration."""
    AI = "ai"
    ML = "ml"
    OPTIMIZATION = "optimization"
    HYBRID = "hybrid"


class BaseAIInterface(ABC):
    """
    Base interface for all AI systems.
    
    Provides unified AI functionality across all implementations.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the AI system with configuration."""
        pass
    
    @abstractmethod
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """Shutdown the AI system."""
        pass


class AgentInterface(ABC):
    """
    Interface for AI agent management.
    
    Provides unified agent functionality across all implementations.
    """
    
    @abstractmethod
    def create_agent(self, agent_config: Dict[str, Any]) -> str:
        """Create a new AI agent."""
        pass
    
    @abstractmethod
    def destroy_agent(self, agent_id: str) -> bool:
        """Destroy an AI agent."""
        pass
    
    @abstractmethod
    def get_agent_status(self, agent_id: str) -> AgentStatus:
        """Get status of AI agent."""
        pass
    
    @abstractmethod
    def send_message_to_agent(self, agent_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to AI agent."""
        pass
    
    @abstractmethod
    def get_agent_response(self, agent_id: str) -> Dict[str, Any]:
        """Get response from AI agent."""
        pass


class APIKeyInterface(ABC):
    """
    Interface for API key management.
    
    Provides unified API key functionality across all implementations.
    """
    
    @abstractmethod
    def store_api_key(self, service: str, key: str) -> bool:
        """Store API key for service."""
        pass
    
    @abstractmethod
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for service."""
        pass
    
    @abstractmethod
    def validate_api_key(self, service: str, key: str) -> bool:
        """Validate API key for service."""
        pass
    
    @abstractmethod
    def revoke_api_key(self, service: str) -> bool:
        """Revoke API key for service."""
        pass


class ModelInterface(ABC):
    """
    Interface for AI/ML model management.
    
    Provides unified model functionality across all implementations.
    """
    
    @abstractmethod
    def load_model(self, model_path: str, model_type: ModelType) -> str:
        """Load AI/ML model from path."""
        pass
    
    @abstractmethod
    def unload_model(self, model_id: str) -> bool:
        """Unload AI/ML model."""
        pass
    
    @abstractmethod
    def predict(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction using model."""
        pass
    
    @abstractmethod
    def train_model(self, model_id: str, training_data: Dict[str, Any]) -> bool:
        """Train AI/ML model."""
        pass
    
    @abstractmethod
    def get_model_metrics(self, model_id: str) -> Dict[str, float]:
        """Get model performance metrics."""
        pass


class WorkflowAIInterface(ABC):
    """
    Interface for AI workflow management.
    
    Provides unified AI workflow functionality across all implementations.
    """
    
    @abstractmethod
    def create_ai_workflow(self, workflow_config: Dict[str, Any]) -> str:
        """Create new AI workflow."""
        pass
    
    @abstractmethod
    def execute_ai_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI workflow."""
        pass
    
    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get AI workflow status."""
        pass
    
    @abstractmethod
    def stop_ai_workflow(self, workflow_id: str) -> bool:
        """Stop AI workflow."""
        pass


class AIInterface(ABC):
    """
    Interface for general AI operations.
    
    Provides unified AI functionality across all implementations.
    """
    
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text using AI."""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate AI response to prompt."""
        pass
    
    @abstractmethod
    def classify_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Classify content using AI."""
        pass


class MLInterface(ABC):
    """
    Interface for machine learning operations.
    
    Provides unified ML functionality across all implementations.
    """
    
    @abstractmethod
    def train_model(self, training_data: Dict[str, Any], model_config: Dict[str, Any]) -> str:
        """Train ML model."""
        pass
    
    @abstractmethod
    def predict(self, model_id: str, features: List[float]) -> Dict[str, Any]:
        """Make ML prediction."""
        pass
    
    @abstractmethod
    def evaluate_model(self, model_id: str, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate ML model performance."""
        pass


class OptimizationInterface(ABC):
    """
    Interface for optimization operations.
    
    Provides unified optimization functionality across all implementations.
    """
    
    @abstractmethod
    def optimize_parameters(self, objective_function: callable, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize parameters using optimization algorithms."""
        pass
    
    @abstractmethod
    def optimize_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow configuration."""
        pass
    
    @abstractmethod
    def get_optimization_results(self, optimization_id: str) -> Dict[str, Any]:
        """Get optimization results."""
        pass
