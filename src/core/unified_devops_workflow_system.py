#!/usr/bin/env python3
"""
Unified DevOps Workflow System - Agent Cellphone V2
===================================================

Consolidated DevOps workflow system eliminating DRY violations.
Replaces duplicate CI/CD pipeline configurations with unified interface.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import os
import sys
import yaml
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

# Unified system imports
from .unified_logging_system import get_logger
from .unified_configuration_system import get_unified_config
from .unified_utility_system import get_unified_utility


class WorkflowType(Enum):
    """Workflow type enumeration."""
    CI_CD = "ci_cd"
    CI_BASIC = "ci_basic"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    SECURITY = "security"


class WorkflowStatus(Enum):
    """Workflow status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


@dataclass
class WorkflowStep:
    """Workflow step data structure."""
    name: str
    type: str
    command: str
    timeout_minutes: int = 15
    condition: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class WorkflowJob:
    """Workflow job data structure."""
    name: str
    runs_on: str
    timeout_minutes: int = 15
    steps: List[WorkflowStep] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)
    if_condition: Optional[str] = None


@dataclass
class WorkflowConfiguration:
    """Workflow configuration data structure."""
    name: str
    workflow_type: WorkflowType
    status: WorkflowStatus
    triggers: Dict[str, Any]
    environment: Dict[str, str]
    jobs: List[WorkflowJob] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class UnifiedDevOpsWorkflowSystem:
    """
    Unified DevOps Workflow System.
    
    Consolidates workflow functionality from:
    - .github/workflows/ci-cd.yml (303 lines)
    - .github/workflows/ci.yml (31 lines)
    - .cursor/rules/workflow.mdc
    
    DRY COMPLIANCE: Single unified interface for all DevOps workflows.
    """
    
    def __init__(self):
        """Initialize unified DevOps workflow system."""
        self.logger = get_logger(__name__)
        self.config = get_unified_config()
        self.utility = get_unified_utility()
        
        # Workflow configurations
        self.workflows: Dict[str, WorkflowConfiguration] = {}
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}
        
        # Initialize standard workflows
        self._initialize_standard_workflows()
    
    def _initialize_standard_workflows(self):
        """Initialize standard workflow configurations."""
        # CI/CD Pipeline Configuration
        ci_cd_config = WorkflowConfiguration(
            name="CI/CD Pipeline - V2 Standards Compliance",
            workflow_type=WorkflowType.CI_CD,
            status=WorkflowStatus.ACTIVE,
            triggers={
                "push": {"branches": ["main", "develop", "feature/*", "hotfix/*"]},
                "pull_request": {"branches": ["main", "develop"]},
                "schedule": [{"cron": "0 2 * * 1"}],  # Weekly security scans
                "workflow_dispatch": {
                    "inputs": {
                        "test_category": {
                            "description": "Test category to run",
                            "required": False,
                            "default": "all",
                            "type": "choice",
                            "options": ["all", "smoke", "unit", "integration", "performance", "security", "v2-standards"]
                        }
                    }
                }
            },
            environment={
                "PYTHON_VERSION": "3.9",
                "PIP_CACHE_DIR": "~/.cache/pip",
                "COVERAGE_THRESHOLD": "80",
                "V2_LOC_LIMIT": "300",
                "V2_CORE_LOC_LIMIT": "200",
                "V2_GUI_LOC_LIMIT": "500"
            }
        )
        
        # Code Quality Job
        code_quality_job = WorkflowJob(
            name="🔍 Code Quality & V2 Standards",
            runs_on="ubuntu-latest",
            timeout_minutes=15,
            steps=[
                WorkflowStep("📥 Checkout code", "checkout", "actions/checkout@v4"),
                WorkflowStep("🐍 Set up Python", "setup_python", "actions/setup-python@v4"),
                WorkflowStep("📦 Install dependencies", "run", "python -m pip install --upgrade pip"),
                WorkflowStep("🔧 Install pre-commit hooks", "run", "pre-commit install"),
                WorkflowStep("🔍 Run pre-commit", "run", "pre-commit run --all-files"),
                WorkflowStep("📊 V2 Standards Check", "run", "python -m src.core.v2_standards_checker"),
                WorkflowStep("📏 LOC Analysis", "run", "python -m src.core.loc_analyzer")
            ]
        )
        
        # Testing Job
        testing_job = WorkflowJob(
            name="🧪 Testing Suite",
            runs_on="ubuntu-latest",
            timeout_minutes=20,
            needs=["code-quality"],
            steps=[
                WorkflowStep("📥 Checkout code", "checkout", "actions/checkout@v4"),
                WorkflowStep("🐍 Set up Python", "setup_python", "actions/setup-python@v4"),
                WorkflowStep("📦 Install dependencies", "run", "pip install -r requirements-testing.txt"),
                WorkflowStep("🧪 Run unit tests", "run", "python -m pytest tests/unit/ -v --cov=src"),
                WorkflowStep("🔗 Run integration tests", "run", "python -m pytest tests/integration/ -v"),
                WorkflowStep("📊 Generate coverage", "run", "coverage xml -o coverage.xml"),
                WorkflowStep("📤 Upload coverage", "upload_artifact", "coverage-*")
            ]
        )
        
        # Integration Job
        integration_job = WorkflowJob(
            name="🔗 Integration Testing",
            runs_on="ubuntu-latest",
            timeout_minutes=25,
            needs=["testing"],
            steps=[
                WorkflowStep("📥 Checkout code", "checkout", "actions/checkout@v4"),
                WorkflowStep("🐍 Set up Python", "setup_python", "actions/setup-python@v4"),
                WorkflowStep("📦 Install dependencies", "run", "pip install -r requirements.txt"),
                WorkflowStep("🔗 Run integration tests", "run", "python -m pytest tests/integration/ -v"),
                WorkflowStep("📊 Performance tests", "run", "python -m pytest tests/performance/ -v"),
                WorkflowStep("🔒 Security tests", "run", "python -m pytest tests/security/ -v")
            ]
        )
        
        # Coverage Quality Job
        coverage_job = WorkflowJob(
            name="📈 Coverage & Quality Metrics",
            runs_on="ubuntu-latest",
            timeout_minutes=15,
            needs=["testing", "integration"],
            if_condition="always()",
            steps=[
                WorkflowStep("📥 Checkout code", "checkout", "actions/checkout@v4"),
                WorkflowStep("🐍 Set up Python", "setup_python", "actions/setup-python@v4"),
                WorkflowStep("📦 Install dependencies", "run", "pip install -r requirements-testing.txt"),
                WorkflowStep("📊 Download coverage artifacts", "download_artifact", "coverage-*"),
                WorkflowStep("📈 Generate combined coverage", "run", "coverage combine coverage-*/coverage.xml"),
                WorkflowStep("📊 Coverage report", "run", "coverage report --show-missing"),
                WorkflowStep("📈 HTML coverage", "run", "coverage html --title='Agent_Cellphone_V2 Coverage Report'"),
                WorkflowStep("📤 Upload coverage", "upload_artifact", "combined-coverage-report")
            ]
        )
        
        # Deployment Job
        deployment_job = WorkflowJob(
            name="🚀 Deployment",
            runs_on="ubuntu-latest",
            timeout_minutes=20,
            needs=["code-quality", "testing", "integration", "coverage-quality"],
            if_condition="github.ref == 'refs/heads/main' && github.event_name == 'push'",
            steps=[
                WorkflowStep("📥 Checkout code", "checkout", "actions/checkout@v4"),
                WorkflowStep("🐍 Set up Python", "setup_python", "actions/setup-python@v4"),
                WorkflowStep("📦 Install dependencies", "run", "pip install -r requirements.txt"),
                WorkflowStep("🚀 Deploy to production", "run", "python -m src.deployment.deploy_production"),
                WorkflowStep("✅ Verify deployment", "run", "python -m src.deployment.verify_deployment")
            ]
        )
        
        # Add jobs to CI/CD configuration
        ci_cd_config.jobs = [code_quality_job, testing_job, integration_job, coverage_job, deployment_job]
        self.workflows["ci_cd_pipeline"] = ci_cd_config
        
        # Basic CI Configuration
        basic_ci_config = WorkflowConfiguration(
            name="Basic CI Pipeline",
            workflow_type=WorkflowType.CI_BASIC,
            status=WorkflowStatus.ACTIVE,
            triggers={
                "push": {"branches": ["**"]},
                "pull_request": {"branches": ["**"]}
            },
            environment={
                "PYTHON_VERSION": "3.11"
            }
        )
        
        # Basic CI Job
        basic_ci_job = WorkflowJob(
            name="test",
            runs_on="ubuntu-latest",
            steps=[
                WorkflowStep("Checkout", "checkout", "actions/checkout@v4"),
                WorkflowStep("Set up Python", "setup_python", "actions/setup-python@v5"),
                WorkflowStep("Install system deps", "run", "sudo apt-get update"),
                WorkflowStep("Install Python deps", "run", "python -m pip install --upgrade pip"),
                WorkflowStep("Install requirements", "run", "pip install -r requirements.txt"),
                WorkflowStep("Install pytest", "run", "pip install pytest"),
                WorkflowStep("Lint check", "run", "ruff check src"),
                WorkflowStep("Run tests", "run", "python -m src --test"),
                WorkflowStep("Status snapshot", "run", "python -m src --status")
            ]
        )
        
        basic_ci_config.jobs = [basic_ci_job]
        self.workflows["basic_ci"] = basic_ci_config
    
    def generate_workflow_yaml(self, workflow_name: str) -> str:
        """Generate YAML configuration for workflow."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow {workflow_name} not found")
        
        workflow = self.workflows[workflow_name]
        
        # Build YAML structure
        yaml_config = {
            "name": workflow.name,
            "on": workflow.triggers,
            "env": workflow.environment,
            "jobs": {}
        }
        
        for job in workflow.jobs:
            job_config = {
                "runs-on": job.runs_on,
                "timeout-minutes": job.timeout_minutes,
                "steps": []
            }
            
            if job.needs:
                job_config["needs"] = job.needs
            
            if job.if_condition:
                job_config["if"] = job.if_condition
            
            for step in job.steps:
                step_config = {"name": step.name}
                
                if step.type == "checkout":
                    step_config["uses"] = step.command
                elif step.type == "setup_python":
                    step_config["uses"] = step.command
                    step_config["with"] = {"python-version": workflow.environment.get("PYTHON_VERSION", "3.9")}
                elif step.type == "run":
                    step_config["run"] = step.command
                elif step.type == "download_artifact":
                    step_config["uses"] = "actions/download-artifact@v3"
                    step_config["with"] = {"name": step.command}
                elif step.type == "upload_artifact":
                    step_config["uses"] = "actions/upload-artifact@v3"
                    step_config["with"] = {"name": step.command}
                
                if step.condition:
                    step_config["if"] = step.condition
                
                job_config["steps"].append(step_config)
            
            yaml_config["jobs"][job.name] = job_config
        
        return yaml.dump(yaml_config, default_flow_style=False, sort_keys=False)
    
    def create_workflow_file(self, workflow_name: str, output_path: str) -> bool:
        """Create workflow file from configuration."""
        try:
            yaml_content = self.generate_workflow_yaml(workflow_name)
            
            # Ensure directory exists
            output_dir = self.utility.Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(output_path, 'w') as f:
                f.write(yaml_content)
            
            self.logger.info(f"Created workflow file: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow file {output_path}: {e}")
            return False
    
    def validate_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Validate workflow configuration."""
        if workflow_name not in self.workflows:
            return {"valid": False, "error": f"Workflow {workflow_name} not found"}
        
        workflow = self.workflows[workflow_name]
        validation_result = {
            "valid": True,
            "workflow_name": workflow.name,
            "workflow_type": workflow.workflow_type.value,
            "status": workflow.status.value,
            "jobs_count": len(workflow.jobs),
            "total_steps": sum(len(job.steps) for job in workflow.jobs),
            "issues": []
        }
        
        # Validate jobs
        for job in workflow.jobs:
            if not job.steps:
                validation_result["issues"].append(f"Job {job.name} has no steps")
            
            for step in job.steps:
                if not step.name or not step.type or not step.command:
                    validation_result["issues"].append(f"Invalid step in job {job.name}")
        
        if validation_result["issues"]:
            validation_result["valid"] = False
        
        return validation_result
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get status of all workflows."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_workflows": len(self.workflows),
            "active_workflows": sum(1 for w in self.workflows.values() if w.status == WorkflowStatus.ACTIVE),
            "workflows": {
                name: {
                    "name": workflow.name,
                    "type": workflow.type.value,
                    "status": workflow.status.value,
                    "jobs_count": len(workflow.jobs),
                    "created_at": workflow.created_at.isoformat(),
                    "updated_at": workflow.updated_at.isoformat()
                }
                for name, workflow in self.workflows.items()
            }
        }
    
    def update_workflow(self, workflow_name: str, updates: Dict[str, Any]) -> bool:
        """Update workflow configuration."""
        if workflow_name not in self.workflows:
            return False
        
        workflow = self.workflows[workflow_name]
        
        try:
            if "name" in updates:
                workflow.name = updates["name"]
            if "status" in updates:
                workflow.status = WorkflowStatus(updates["status"])
            if "environment" in updates:
                workflow.environment.update(updates["environment"])
            
            workflow.updated_at = datetime.utcnow()
            self.logger.info(f"Updated workflow {workflow_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update workflow {workflow_name}: {e}")
            return False
    
    def deploy_workflows(self, output_directory: str = ".github/workflows") -> Dict[str, bool]:
        """Deploy all workflows to output directory."""
        results = {}
        
        for workflow_name in self.workflows:
            output_path = f"{output_directory}/{workflow_name}.yml"
            results[workflow_name] = self.create_workflow_file(workflow_name, output_path)
        
        return results


# Global instance
_unified_devops_workflow = None

def get_unified_devops_workflow() -> UnifiedDevOpsWorkflowSystem:
    """Get unified DevOps workflow system instance."""
    global _unified_devops_workflow
    if _unified_devops_workflow is None:
        _unified_devops_workflow = UnifiedDevOpsWorkflowSystem()
    return _unified_devops_workflow
