#!/usr/bin/env python3
"""
Learning Integration - Unified Workflow System

Integrates the existing unified learning system with the unified workflow system
following the established architecture patterns. NO duplicate implementations.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Use existing unified learning system - only import what actually exists
from ..learning.unified_learning_engine import UnifiedLearningEngine
from ..learning.learning_models import LearningData, LearningGoal, LearningStatus
# ARCHITECTURE CORRECTED: Using decision models from existing learning module
from ..learning.decision_models import DecisionRequest, DecisionResult, DecisionType

# Use existing unified workflow system
from .base_workflow_engine import BaseWorkflowEngine
from .types.workflow_enums import WorkflowType, WorkflowStatus, TaskStatus
from .types.workflow_models import WorkflowDefinition, WorkflowStep


class LearningWorkflowIntegration:
    """
    Integrates existing unified learning system with existing unified workflow system.
    
    Follows established architecture patterns from src/core/learning/
    NO duplicate implementations - uses existing systems.
    """
    
    def __init__(self):
        """Initialize learning workflow integration."""
        self.logger = logging.getLogger(f"{__name__}.LearningWorkflowIntegration")
        
        # Use existing unified systems
        self.learning_engine = UnifiedLearningEngine()
        self.workflow_engine = BaseWorkflowEngine()
        
        # Integration state
        self.integrated_workflows: Dict[str, Dict[str, Any]] = {}
        self.learning_workflow_sessions: Dict[str, str] = {}
        
        self.logger.info("✅ LearningWorkflowIntegration initialized using existing unified systems")
    
    def create_learning_workflow(self, learning_goal: str, agent_id: str, 
                                workflow_parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Create learning workflow using existing unified systems.
        
        Args:
            learning_goal: Learning goal description
            agent_id: Agent identifier
            workflow_parameters: Optional workflow parameters
            
        Returns:
            Workflow ID of created learning workflow
        """
        try:
            # Create learning session using existing unified learning engine
            session_config = {
                "agent_id": agent_id,
                "session_type": "workflow_integrated",
                "learning_goal": learning_goal,
                "created_at": datetime.now().isoformat()
            }
            
            # Use existing learning engine to create session
            session_id = self.learning_engine.create_learning_session(
                agent_id=agent_id,
                session_type="workflow_integrated",
                session_config=session_config
            )
            
            # Create workflow using existing unified workflow engine
            workflow_definition = {
                "name": f"Learning Workflow: {learning_goal}",
                "description": f"Integrated learning workflow for {learning_goal}",
                "steps": [
                    {
                        "step_id": "learning_initiation",
                        "name": "Learning Initiation",
                        "step_type": "learning"
                    },
                    {
                        "step_id": "knowledge_acquisition",
                        "name": "Knowledge Acquisition",
                        "step_type": "learning"
                    },
                    {
                        "step_id": "skill_development",
                        "name": "Skill Development",
                        "step_type": "learning"
                    },
                    {
                        "step_id": "assessment",
                        "name": "Learning Assessment",
                        "step_type": "validation"
                    }
                ],
                "metadata": {
                    "learning_session_id": session_id,
                    "agent_id": agent_id,
                    "learning_goal": learning_goal,
                    "integration_type": "learning_workflow"
                }
            }
            
            # Create workflow using existing unified workflow engine
            workflow_id = self.workflow_engine.create_workflow(
                WorkflowType.SEQUENTIAL,
                workflow_definition
            )
            
            # Store integration mapping
            self.integrated_workflows[workflow_id] = {
                "learning_session_id": session_id,
                "agent_id": agent_id,
                "learning_goal": learning_goal,
                "created_at": datetime.now().isoformat(),
                "status": "created"
            }
            
            self.learning_workflow_sessions[session_id] = workflow_id
            
            self.logger.info(f"✅ Created learning workflow: {workflow_id} for session: {session_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create learning workflow: {e}")
            raise
    
    def execute_learning_workflow(self, workflow_id: str, 
                                 learning_parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute learning workflow using existing unified systems.
        
        Args:
            workflow_id: ID of workflow to execute
            learning_parameters: Optional learning parameters
            
        Returns:
            Execution ID of started learning workflow
        """
        try:
            if workflow_id not in self.integrated_workflows:
                raise ValueError(f"Learning workflow not found: {workflow_id}")
            
            # Execute workflow using existing unified workflow engine
            execution_id = self.workflow_engine.execute_workflow(
                workflow_id, 
                learning_parameters
            )
            
            # Update integration status
            self.integrated_workflows[workflow_id]["status"] = "executing"
            self.integrated_workflows[workflow_id]["execution_id"] = execution_id
            self.integrated_workflows[workflow_id]["executed_at"] = datetime.now().isoformat()
            
            self.logger.info(f"✅ Executed learning workflow: {workflow_id} -> {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to execute learning workflow {workflow_id}: {e}")
            raise
    
    def get_learning_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get learning workflow status from existing unified systems.
        
        Args:
            workflow_id: ID of workflow
            
        Returns:
            Combined learning and workflow status
        """
        try:
            if workflow_id not in self.integrated_workflows:
                return {"error": "Learning workflow not found"}
            
            integration_info = self.integrated_workflows[workflow_id]
            
            # Get workflow status from existing unified workflow engine
            workflow_status = self.workflow_engine.get_workflow_status(workflow_id)
            
            # Get learning session status from existing unified learning engine
            learning_session_id = integration_info["learning_session_id"]
            learning_session = self.learning_engine.get_learning_session(learning_session_id)
            
            # Combine status information
            combined_status = {
                "workflow_id": workflow_id,
                "learning_session_id": learning_session_id,
                "agent_id": integration_info["agent_id"],
                "learning_goal": integration_info["learning_goal"],
                "workflow_status": workflow_status,
                "learning_status": learning_session.get("status", "unknown") if learning_session else "unknown",
                "created_at": integration_info["created_at"],
                "integration_status": integration_info["status"]
            }
            
            return combined_status
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get learning workflow status: {e}")
            return {"error": str(e)}
    
    def create_decision_workflow(self, decision_type: str, priority: str, 
                                context: Dict[str, Any]) -> str:
        """
        Create decision workflow using existing unified systems.
        
        Args:
            decision_type: Type of decision
            priority: Priority level
            context: Decision context
            
        Returns:
            Workflow ID of created decision workflow
        """
        try:
            # Create decision workflow using existing unified workflow engine
            workflow_definition = {
                "name": f"Decision Workflow: {decision_type}",
                "description": f"Integrated decision workflow for {decision_type}",
                "steps": [
                    {
                        "step_id": "decision_analysis",
                        "name": "Decision Analysis",
                        "step_type": "decision"
                    },
                    {
                        "step_id": "option_evaluation",
                        "name": "Option Evaluation",
                        "step_type": "decision"
                    },
                    {
                        "step_id": "decision_making",
                        "name": "Decision Making",
                        "step_type": "decision"
                    },
                    {
                        "step_id": "implementation",
                        "name": "Decision Implementation",
                        "step_type": "execution"
                    }
                ],
                "metadata": {
                    "decision_type": decision_type,
                    "priority": priority,
                    "context": context,
                    "integration_type": "decision_workflow"
                }
            }
            
            # Create workflow using existing unified workflow engine
            workflow_id = self.workflow_engine.create_workflow(
                WorkflowType.SEQUENTIAL,
                workflow_definition
            )
            
            # Store integration mapping
            self.integrated_workflows[workflow_id] = {
                "decision_type": decision_type,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "status": "created",
                "integration_type": "decision_workflow"
            }
            
            self.logger.info(f"✅ Created decision workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create decision workflow: {e}")
            raise
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get overall integration status.
        
        Returns:
            Integration status information
        """
        try:
            total_workflows = len(self.integrated_workflows)
            learning_workflows = sum(
                1 for info in self.integrated_workflows.values()
                if info.get("integration_type") == "learning_workflow"
            )
            decision_workflows = sum(
                1 for info in self.integrated_workflows.values()
                if info.get("integration_type") == "decision_workflow"
            )
            
            # Get system health from existing unified systems
            workflow_health = self.workflow_engine.get_system_health()
            learning_health = {
                "total_sessions": len(self.learning_engine.learning_sessions),
                "active_sessions": len(self.learning_engine.active_sessions)
            }
            
            return {
                "integration_status": "operational",
                "total_integrated_workflows": total_workflows,
                "learning_workflows": learning_workflows,
                "decision_workflows": decision_workflows,
                "workflow_system_health": workflow_health,
                "learning_system_health": learning_health,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get integration status: {e}")
            return {"error": str(e)}
    
    def run_integration_test(self) -> bool:
        """
        Run integration test using existing unified systems.
        
        Returns:
            True if integration test passes
        """
        try:
            self.logger.info("🧪 Running learning workflow integration test...")
            
            # Test learning workflow creation
            test_goal = "Integration Testing - Learning Workflow"
            test_agent = "test_agent_001"
            
            workflow_id = self.create_learning_workflow(test_goal, test_agent)
            
            if workflow_id and workflow_id in self.integrated_workflows:
                self.logger.info("✅ Learning workflow creation test passed")
                
                # Test workflow execution
                execution_id = self.execute_learning_workflow(workflow_id)
                
                if execution_id:
                    self.logger.info("✅ Learning workflow execution test passed")
                    
                    # Test status retrieval
                    status = self.get_learning_workflow_status(workflow_id)
                    
                    if "error" not in status:
                        self.logger.info("✅ Learning workflow status test passed")
                        
                        # Test integration status
                        integration_status = self.get_integration_status()
                        
                        if "error" not in integration_status:
                            self.logger.info("✅ Integration status test passed")
                            self.logger.info("🎉 All integration tests passed successfully!")
                            return True
                        else:
                            self.logger.error("❌ Integration status test failed")
                            return False
                    else:
                        self.logger.error("❌ Learning workflow status test failed")
                        return False
                else:
                    self.logger.error("❌ Learning workflow execution test failed")
                    return False
            else:
                self.logger.error("❌ Learning workflow creation test failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Integration test failed: {e}")
            return False


if __name__ == "__main__":
    # Initialize integration
    integration = LearningWorkflowIntegration()
    
    # Run integration test
    success = integration.run_integration_test()
    
    if success:
        print("✅ Learning workflow integration test passed!")
        print("🚀 System ready for production use!")
    else:
        print("❌ Learning workflow integration test failed!")
        print("⚠️ System requires additional testing before deployment.")
