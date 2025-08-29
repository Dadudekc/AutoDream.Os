#!/usr/bin/env python3
"""
Integration Test Core - Core Integration Testing Functionality
============================================================

Core integration testing functionality for unified workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from ..base_workflow_engine import BaseWorkflowEngine
from ..specialized.business_process_workflow import BusinessProcessWorkflow
from ..consolidation_migration import WorkflowConsolidationMigrator
from ..learning_integration import LearningWorkflowIntegration


class IntegrationTestCore:
    """
    Core integration testing functionality for workflow system.
    
    Single responsibility: Core integration testing operations
    following V2 standards.
    """
    
    def __init__(self):
        """Initialize integration test core."""
        self.logger = logging.getLogger(f"{__name__}.IntegrationTestCore")
        
        # Initialize workflow components
        self.base_engine = BaseWorkflowEngine()
        self.business_process_workflow = BusinessProcessWorkflow()
        self.consolidation_migrator = WorkflowConsolidationMigrator()
        self.learning_integration = LearningWorkflowIntegration()
        
        # Test results tracking
        self.test_results: Dict[str, Dict[str, Any]] = {}
        self.integration_status: Dict[str, str] = {}
        
        self.logger.info("✅ Integration Test Core initialized")
    
    def load_contract_data(self) -> Dict[str, Any]:
        """Load contract data for integration testing."""
        self.logger.info("📋 Loading contract data...")
        
        contract_data = {}
        try:
            # Load master contract index
            contract_index_path = "contracts/MASTER_CONTRACT_INDEX.json"
            if os.path.exists(contract_index_path):
                with open(contract_index_path, 'r') as f:
                    contract_data["master_index"] = json.load(f)
                self.logger.info("✅ Master contract index loaded")
            
            # Load template
            template_path = "contracts/CONSOLIDATED_CONTRACT_TEMPLATE.json"
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    contract_data["template"] = json.load(f)
                self.logger.info("✅ Contract template loaded")
            
            return contract_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load contract data: {e}")
            return {}
    
    def run_basic_integration_tests(self) -> Dict[str, Any]:
        """Run basic integration tests."""
        self.logger.info("🧪 Running basic integration tests...")
        
        results = {
            "workflow_engine": self._test_workflow_engine(),
            "business_process": self._test_business_process(),
            "learning_integration": self._test_learning_integration()
        }
        
        self.test_results["basic_tests"] = results
        return results
    
    def _test_workflow_engine(self) -> Dict[str, Any]:
        """Test workflow engine functionality."""
        try:
            # Test basic workflow creation
            workflow_def = {
                "name": "Test Workflow",
                "description": "Test workflow for integration testing",
                "steps": [{"step_id": "test", "name": "Test Step"}]
            }
            
            workflow_id = self.base_engine.create_workflow("sequential", workflow_def)
            
            return {
                "status": "PASSED",
                "workflow_id": workflow_id,
                "message": "Workflow engine working correctly"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "message": "Workflow engine test failed"
            }
    
    def _test_business_process(self) -> Dict[str, Any]:
        """Test business process workflow."""
        try:
            business_data = {
                "business_unit": "Testing",
                "priority": "high",
                "compliance_required": True
            }
            
            workflow_id = self.business_process_workflow.create_business_process(
                "approval", business_data
            )
            
            return {
                "status": "PASSED",
                "workflow_id": workflow_id,
                "message": "Business process workflow working correctly"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "message": "Business process workflow test failed"
            }
    
    def _test_learning_integration(self) -> Dict[str, Any]:
        """Test learning integration."""
        try:
            workflow_id = self.learning_integration.create_learning_workflow(
                "Test Learning Goal", "test_agent_001"
            )
            
            return {
                "status": "PASSED",
                "workflow_id": workflow_id,
                "message": "Learning integration working correctly"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "message": "Learning integration test failed"
            }
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get test execution summary."""
        return {
            "total_tests": len(self.test_results),
            "test_results": self.test_results,
            "integration_status": self.integration_status,
            "timestamp": datetime.now().isoformat()
        }
