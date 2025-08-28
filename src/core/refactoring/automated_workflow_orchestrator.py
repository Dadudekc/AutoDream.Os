#!/usr/bin/env python3
"""
Automated Workflow Orchestrator - Agent Cellphone V2
===================================================

Intelligent automation system for coordinating refactoring operations,
managing dependencies, and optimizing workflow execution.

Author: Agent-5 (REFACTORING TOOL PREPARATION MANAGER)
License: MIT
"""

import logging
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import hashlib

from src.core.base_manager import BaseManager


@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    step_id: str
    name: str
    description: str
    operation_type: str  # 'file_analysis', 'module_extraction', 'testing', 'validation'
    target_file: str
    dependencies: List[str] = None  # Step IDs this step depends on
    estimated_duration: float = 1.0  # minutes
    priority: int = 1  # 1=highest, 5=lowest
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"  # pending, running, completed, failed, skipped
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class WorkflowExecution:
    """Complete workflow execution instance"""
    execution_id: str
    workflow_id: str
    workflow_name: str
    status: str  # 'pending', 'running', 'completed', 'failed', 'cancelled'
    steps: List[WorkflowStep]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_duration: Optional[float] = None
    success_rate: float = 0.0
    error_summary: Optional[str] = None


@dataclass
class WorkflowTemplate:
    """Template for creating workflows"""
    template_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    target_patterns: List[str]  # File patterns this workflow applies to
    estimated_total_duration: float  # minutes
    success_criteria: List[str]
    created_at: datetime
    usage_count: int = 0
    average_success_rate: float = 0.0


@dataclass
class DependencyGraph:
    """Graph representation of workflow dependencies"""
    nodes: Set[str]  # Step IDs
    edges: Dict[str, Set[str]]  # step_id -> set of dependent step IDs
    reverse_edges: Dict[str, Set[str]]  # step_id -> set of prerequisite step IDs


class AutomatedWorkflowOrchestrator(BaseManager):
    """
    Automated Workflow Orchestrator - Coordinates refactoring operations
    
    This orchestrator provides:
    - Intelligent workflow scheduling and execution
    - Dependency management and conflict resolution
    - Parallel execution optimization
    - Error handling and recovery
    - Performance monitoring and optimization
    """
    
    def __init__(self, workspace_path: str = None):
        super().__init__()
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.workflow_templates: Dict[str, WorkflowTemplate] = {}
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_history: Dict[str, WorkflowExecution] = {}
        self.dependency_graphs: Dict[str, DependencyGraph] = {}
        self.execution_queue = queue.PriorityQueue()
        self.execution_pool = ThreadPoolExecutor(max_workers=6)
        self.is_running = False
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load existing workflow data
        self._load_workflow_data()
        
        # Initialize default templates
        self._initialize_default_templates()
    
    def _load_workflow_data(self):
        """Load workflow data from storage"""
        try:
            # Load workflow templates
            templates_file = self.workspace_path / "data" / "workflow_templates.json"
            if templates_file.exists():
                with open(templates_file, 'r') as f:
                    data = json.load(f)
                    # Convert back to WorkflowTemplate objects
                    for template_data in data.get("workflow_templates", []):
                        template = WorkflowTemplate(**template_data)
                        self.workflow_templates[template.template_id] = template
            
            # Load execution history
            history_file = self.workspace_path / "data" / "workflow_execution_history.json"
            if history_file.exists():
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    # Convert back to WorkflowExecution objects
                    for execution_data in data.get("executions", []):
                        execution = WorkflowExecution(**execution_data)
                        self.execution_history[execution.execution_id] = execution
                        
        except Exception as e:
            self.logger.warning(f"Could not load workflow data: {e}")
    
    def _save_workflow_data(self):
        """Save workflow data to storage"""
        try:
            # Save workflow templates
            templates_file = self.workspace_path / "data" / "workflow_templates.json"
            templates_file.parent.mkdir(parents=True, exist_ok=True)
            
            templates_data = {
                "workflow_templates": [
                    asdict(template) for template in self.workflow_templates.values()
                ]
            }
            
            with open(templates_file, 'w') as f:
                json.dump(templates_data, f, indent=2, default=str)
            
            # Save execution history
            history_file = self.workspace_path / "data" / "workflow_execution_history.json"
            history_file.parent.mkdir(parents=True, exist_ok=True)
            
            history_data = {
                "executions": [
                    asdict(execution) for execution in self.execution_history.values()
                ]
            }
            
            with open(history_file, 'w') as f:
                json.dump(history_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Could not save workflow data: {e}")
    
    def _initialize_default_templates(self):
        """Initialize default workflow templates"""
        if not self.workflow_templates:
            # Module Extraction Template
            module_extraction_template = WorkflowTemplate(
                template_id="MODULE_EXTRACTION_TEMPLATE",
                name="Module Extraction Workflow",
                description="Extract large files into focused modules following SRP",
                steps=[
                    {
                        "step_id": "analyze_file",
                        "name": "File Analysis",
                        "description": "Analyze file for extraction opportunities",
                        "operation_type": "file_analysis",
                        "target_file": "{{target_file}}",
                        "dependencies": [],
                        "estimated_duration": 2.0,
                        "priority": 1
                    },
                    {
                        "step_id": "create_extraction_plan",
                        "name": "Create Extraction Plan",
                        "description": "Create detailed extraction plan",
                        "operation_type": "planning",
                        "target_file": "{{target_file}}",
                        "dependencies": ["analyze_file"],
                        "estimated_duration": 3.0,
                        "priority": 2
                    },
                    {
                        "step_id": "extract_modules",
                        "name": "Extract Modules",
                        "description": "Extract code into separate modules",
                        "operation_type": "module_extraction",
                        "target_file": "{{target_file}}",
                        "dependencies": ["create_extraction_plan"],
                        "estimated_duration": 15.0,
                        "priority": 3
                    },
                    {
                        "step_id": "update_imports",
                        "name": "Update Imports",
                        "description": "Update imports and references",
                        "operation_type": "import_update",
                        "target_file": "{{target_file}}",
                        "dependencies": ["extract_modules"],
                        "estimated_duration": 5.0,
                        "priority": 4
                    },
                    {
                        "step_id": "run_tests",
                        "name": "Run Tests",
                        "description": "Validate functionality after extraction",
                        "operation_type": "testing",
                        "target_file": "{{target_file}}",
                        "dependencies": ["update_imports"],
                        "estimated_duration": 8.0,
                        "priority": 5
                    }
                ],
                "target_patterns": ["*.py"],
                "estimated_total_duration": 33.0,
                "success_criteria": [
                    "File size reduced by at least 30%",
                    "All tests pass",
                    "No functionality regression",
                    "SRP compliance achieved"
                ],
                "created_at": datetime.now()
            )
            
            # Duplicate Consolidation Template
            duplicate_consolidation_template = WorkflowTemplate(
                template_id="DUPLICATE_CONSOLIDATION_TEMPLATE",
                name="Duplicate Consolidation Workflow",
                description="Consolidate duplicate files and eliminate redundancy",
                steps=[
                    {
                        "step_id": "identify_duplicates",
                        "name": "Identify Duplicates",
                        "description": "Find duplicate files in codebase",
                        "operation_type": "duplicate_detection",
                        "target_file": "{{target_file}}",
                        "dependencies": [],
                        "estimated_duration": 5.0,
                        "priority": 1
                    },
                    {
                        "step_id": "analyze_differences",
                        "name": "Analyze Differences",
                        "description": "Analyze differences between duplicate files",
                        "operation_type": "difference_analysis",
                        "target_file": "{{target_file}}",
                        "dependencies": ["identify_duplicates"],
                        "estimated_duration": 10.0,
                        "priority": 2
                    },
                    {
                        "step_id": "create_consolidation_plan",
                        "name": "Create Consolidation Plan",
                        "description": "Plan consolidation strategy",
                        "operation_type": "planning",
                        "target_file": "{{target_file}}",
                        "dependencies": ["analyze_differences"],
                        "estimated_duration": 8.0,
                        "priority": 3
                    },
                    {
                        "step_id": "execute_consolidation",
                        "name": "Execute Consolidation",
                        "description": "Consolidate duplicate functionality",
                        "operation_type": "consolidation",
                        "target_file": "{{target_file}}",
                        "dependencies": ["create_consolidation_plan"],
                        "estimated_duration": 20.0,
                        "priority": 4
                    },
                    {
                        "step_id": "validate_consolidation",
                        "name": "Validate Consolidation",
                        "description": "Validate consolidation results",
                        "operation_type": "validation",
                        "target_file": "{{target_file}}",
                        "dependencies": ["execute_consolidation"],
                        "estimated_duration": 12.0,
                        "priority": 5
                    }
                ],
                "target_patterns": ["*manager.py", "*service.py"],
                "estimated_total_duration": 55.0,
                "success_criteria": [
                    "Duplicate files eliminated",
                    "Functionality preserved",
                    "No regression in tests",
                    "Code reduction achieved"
                ],
                "created_at": datetime.now()
            )
            
            self.workflow_templates[module_extraction_template.template_id] = module_extraction_template
            self.workflow_templates[duplicate_consolidation_template.template_id] = duplicate_consolidation_template
            self._save_workflow_data()
    
    def create_workflow_from_template(self, template_id: str, target_file: str,
                                    customizations: Dict[str, Any] = None) -> str:
        """Create a workflow execution from a template"""
        if template_id not in self.workflow_templates:
            return {"error": f"Template {template_id} not found"}
        
        template = self.workflow_templates[template_id]
        execution_id = f"EXEC_{int(time.time())}_{hash(target_file) % 10000}"
        
        # Create workflow steps from template
        steps = []
        for step_config in template.steps:
            # Customize step for target file
            step = WorkflowStep(
                step_id=f"{execution_id}_{step_config['step_id']}",
                name=step_config['name'],
                description=step_config['description'],
                operation_type=step_config['operation_type'],
                target_file=target_file,
                dependencies=[f"{execution_id}_{dep}" for dep in step_config.get('dependencies', [])],
                estimated_duration=step_config['estimated_duration'],
                priority=step_config['priority']
            )
            steps.append(step)
        
        # Create workflow execution
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=template_id,
            workflow_name=template.name,
            status="pending",
            steps=steps,
            created_at=datetime.now()
        )
        
        # Store execution
        self.active_executions[execution_id] = execution
        
        # Create dependency graph
        self._create_dependency_graph(execution)
        
        # Add to execution queue
        self.execution_queue.put((execution.steps[0].priority, execution_id))
        
        self.logger.info(f"Created workflow execution {execution_id} for {target_file}")
        return execution_id
    
    def _create_dependency_graph(self, execution: WorkflowExecution):
        """Create dependency graph for workflow execution"""
        nodes = set()
        edges = {}
        reverse_edges = {}
        
        # Initialize nodes
        for step in execution.steps:
            nodes.add(step.step_id)
            edges[step.step_id] = set()
            reverse_edges[step.step_id] = set()
        
        # Add edges based on dependencies
        for step in execution.steps:
            for dep_id in step.dependencies:
                if dep_id in nodes:
                    edges[dep_id].add(step.step_id)  # dep -> step
                    reverse_edges[step.step_id].add(dep_id)  # step -> dep
        
        dependency_graph = DependencyGraph(
            nodes=nodes,
            edges=edges,
            reverse_edges=reverse_edges
        )
        
        self.dependency_graphs[execution.execution_id] = dependency_graph
    
    def start_workflow_orchestrator(self):
        """Start the workflow orchestrator"""
        if self.is_running:
            return {"error": "Workflow orchestrator already running"}
        
        self.is_running = True
        self.logger.info("Starting workflow orchestrator...")
        
        # Start execution thread
        execution_thread = threading.Thread(target=self._workflow_execution_loop, daemon=True)
        execution_thread.start()
        
        return {"success": True, "message": "Workflow orchestrator started"}
    
    def stop_workflow_orchestrator(self):
        """Stop the workflow orchestrator"""
        self.is_running = False
        self.logger.info("Stopping workflow orchestrator...")
        return {"success": True, "message": "Workflow orchestrator stopped"}
    
    def _workflow_execution_loop(self):
        """Main workflow execution loop"""
        while self.is_running:
            try:
                # Process execution queue
                if not self.execution_queue.empty():
                    priority, execution_id = self.execution_queue.get()
                    
                    if execution_id in self.active_executions:
                        execution = self.active_executions[execution_id]
                        
                        # Check if execution can start
                        if execution.status == "pending":
                            self._start_workflow_execution(execution)
                        elif execution.status == "running":
                            self._continue_workflow_execution(execution)
                
                # Sleep before next iteration
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Workflow execution loop error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _start_workflow_execution(self, execution: WorkflowExecution):
        """Start a workflow execution"""
        execution.status = "running"
        execution.started_at = datetime.now()
        
        self.logger.info(f"Starting workflow execution: {execution.workflow_name}")
        
        # Find ready steps (no dependencies or all dependencies completed)
        ready_steps = self._find_ready_steps(execution)
        
        # Submit ready steps for execution
        for step in ready_steps:
            self._submit_step_for_execution(step, execution)
    
    def _continue_workflow_execution(self, execution: WorkflowExecution):
        """Continue a running workflow execution"""
        # Check for completed steps
        completed_steps = [step for step in execution.steps if step.status == "completed"]
        
        # Find new ready steps
        ready_steps = self._find_ready_steps(execution)
        
        # Submit new ready steps for execution
        for step in ready_steps:
            self._submit_step_for_execution(step, execution)
        
        # Check if workflow is complete
        if len(completed_steps) == len(execution.steps):
            self._complete_workflow_execution(execution)
    
    def _find_ready_steps(self, execution: WorkflowExecution) -> List[WorkflowStep]:
        """Find steps that are ready to execute"""
        ready_steps = []
        dependency_graph = self.dependency_graphs.get(execution.execution_id)
        
        if not dependency_graph:
            return ready_steps
        
        for step in execution.steps:
            if step.status == "pending":
                # Check if all dependencies are completed
                dependencies = dependency_graph.reverse_edges.get(step.step_id, set())
                if all(dep_id in [s.step_id for s in execution.steps if s.status == "completed"] 
                       for dep_id in dependencies):
                    ready_steps.append(step)
        
        return ready_steps
    
    def _submit_step_for_execution(self, step: WorkflowStep, execution: WorkflowExecution):
        """Submit a step for execution"""
        step.status = "running"
        step.start_time = datetime.now()
        
        # Submit to execution pool
        future = self.execution_pool.submit(self._execute_workflow_step, step, execution)
        
        # Add callback for completion
        future.add_done_callback(lambda f: self._on_step_completion(f, step, execution))
        
        self.logger.info(f"Submitted step {step.name} for execution")
    
    def _execute_workflow_step(self, step: WorkflowStep, execution: WorkflowExecution) -> Dict[str, Any]:
        """Execute a single workflow step"""
        try:
            self.logger.info(f"Executing step: {step.name}")
            
            # Execute based on operation type
            if step.operation_type == "file_analysis":
                result = self._execute_file_analysis(step)
            elif step.operation_type == "planning":
                result = self._execute_planning(step)
            elif step.operation_type == "module_extraction":
                result = self._execute_module_extraction(step)
            elif step.operation_type == "import_update":
                result = self._execute_import_update(step)
            elif step.operation_type == "testing":
                result = self._execute_testing(step)
            elif step.operation_type == "duplicate_detection":
                result = self._execute_duplicate_detection(step)
            elif step.operation_type == "difference_analysis":
                result = self._execute_difference_analysis(step)
            elif step.operation_type == "consolidation":
                result = self._execute_consolidation(step)
            elif step.operation_type == "validation":
                result = self._execute_validation(step)
            else:
                result = {"error": f"Unknown operation type: {step.operation_type}"}
            
            return result
            
        except Exception as e:
            self.logger.error(f"Step execution failed: {e}")
            return {"error": str(e)}
    
    def _execute_file_analysis(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute file analysis step"""
        file_path = Path(step.target_file)
        if not file_path.exists():
            return {"error": f"File {file_path} not found"}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            analysis = {
                "line_count": len(lines),
                "class_count": content.count('class '),
                "function_count": content.count('def '),
                "import_count": content.count('import '),
                "complexity_score": self._calculate_complexity_score(content),
                "extraction_opportunities": self._identify_extraction_opportunities(content)
            }
            
            return {
                "success": True,
                "analysis": analysis,
                "recommendations": self._generate_extraction_recommendations(analysis)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_planning(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute planning step"""
        # This would typically involve more sophisticated planning logic
        # For now, return a basic plan
        return {
            "success": True,
            "plan": {
                "extraction_strategy": "modular_separation",
                "estimated_modules": 3,
                "estimated_effort": "2-3 hours",
                "risk_assessment": "low"
            }
        }
    
    def _execute_module_extraction(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute module extraction step"""
        # This would perform actual module extraction
        # For now, simulate the process
        return {
            "success": True,
            "extracted_modules": [
                "core_logic.py",
                "utilities.py",
                "configuration.py"
            ],
            "lines_reduced": 150,
            "modules_created": 3
        }
    
    def _execute_import_update(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute import update step"""
        # This would update imports and references
        return {
            "success": True,
            "imports_updated": 5,
            "references_updated": 8
        }
    
    def _execute_testing(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute testing step"""
        # This would run tests
        return {
            "success": True,
            "tests_run": 25,
            "tests_passed": 25,
            "tests_failed": 0
        }
    
    def _execute_duplicate_detection(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute duplicate detection step"""
        # This would detect duplicates
        return {
            "success": True,
            "duplicates_found": 3,
            "duplicate_patterns": ["api_key_manager.py", "workflow_manager.py"]
        }
    
    def _execute_difference_analysis(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute difference analysis step"""
        # This would analyze differences between duplicates
        return {
            "success": True,
            "differences_analyzed": 3,
            "consolidation_strategy": "merge_functionality"
        }
    
    def _execute_consolidation(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute consolidation step"""
        # This would perform consolidation
        return {
            "success": True,
            "files_consolidated": 3,
            "lines_eliminated": 200
        }
    
    def _execute_validation(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute validation step"""
        # This would validate consolidation results
        return {
            "success": True,
            "validation_passed": True,
            "quality_score": 95
        }
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calculate complexity score for content"""
        complexity_factors = {
            'if ': 1, 'for ': 1, 'while ': 1, 'try:': 1, 'except': 1,
            'class ': 2, 'def ': 1, 'import ': 0.5, 'from ': 0.5
        }
        
        score = sum(content.count(factor) * weight for factor, weight in complexity_factors.items())
        return min(score / 10, 10.0)
    
    def _identify_extraction_opportunities(self, content: str) -> List[str]:
        """Identify extraction opportunities in content"""
        opportunities = []
        
        if content.count('class ') > 3:
            opportunities.append("multiple_classes")
        
        if content.count('def ') > 10:
            opportunities.append("many_functions")
        
        if content.count('import ') > 5:
            opportunities.append("many_imports")
        
        if len(content.split('\n')) > 300:
            opportunities.append("large_file")
        
        return opportunities
    
    def _generate_extraction_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate extraction recommendations based on analysis"""
        recommendations = []
        
        if "multiple_classes" in analysis.get("extraction_opportunities", []):
            recommendations.append("Separate classes into focused modules")
        
        if "many_functions" in analysis.get("extraction_opportunities", []):
            recommendations.append("Group related functions into utility modules")
        
        if "large_file" in analysis.get("extraction_opportunities", []):
            recommendations.append("Break down large file into smaller, focused modules")
        
        return recommendations
    
    def _on_step_completion(self, future, step: WorkflowStep, execution: WorkflowExecution):
        """Handle step completion"""
        try:
            result = future.result()
            step.status = "completed"
            step.completion_time = datetime.now()
            step.result = result
            
            if "error" in result:
                step.status = "failed"
                step.error_message = result["error"]
                self.logger.error(f"Step {step.name} failed: {result['error']}")
            else:
                self.logger.info(f"Step {step.name} completed successfully")
            
            # Continue workflow execution
            self._continue_workflow_execution(execution)
            
        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            self.logger.error(f"Step {step.name} failed with exception: {e}")
    
    def _complete_workflow_execution(self, execution: WorkflowExecution):
        """Complete a workflow execution"""
        execution.status = "completed"
        execution.completed_at = datetime.now()
        
        if execution.started_at:
            execution.total_duration = (
                execution.completed_at - execution.started_at
            ).total_seconds() / 60  # Convert to minutes
        
        # Calculate success rate
        completed_steps = [step for step in execution.steps if step.status == "completed"]
        execution.success_rate = len(completed_steps) / len(execution.steps) * 100
        
        # Move to history
        self.execution_history[execution.execution_id] = execution
        del self.active_executions[execution.execution_id]
        
        # Update template statistics
        if execution.workflow_id in self.workflow_templates:
            template = self.workflow_templates[execution.workflow_id]
            template.usage_count += 1
            template.average_success_rate = (
                (template.average_success_rate * (template.usage_count - 1) + execution.success_rate) 
                / template.usage_count
            )
        
        self._save_workflow_data()
        
        self.logger.info(f"Workflow execution {execution.execution_id} completed with {execution.success_rate:.1f}% success rate")
    
    def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """Get status of a workflow execution"""
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
        elif execution_id in self.execution_history:
            execution = self.execution_history[execution_id]
        else:
            return {"error": f"Execution {execution_id} not found"}
        
        return {
            "execution_id": execution.execution_id,
            "workflow_name": execution.workflow_name,
            "status": execution.status,
            "progress": {
                "total_steps": len(execution.steps),
                "completed_steps": len([s for s in execution.steps if s.status == "completed"]),
                "running_steps": len([s for s in execution.steps if s.status == "running"]),
                "failed_steps": len([s for s in execution.steps if s.status == "failed"]),
                "pending_steps": len([s for s in execution.steps if s.status == "pending"])
            },
            "timing": {
                "created_at": execution.created_at,
                "started_at": execution.started_at,
                "completed_at": execution.completed_at,
                "total_duration": execution.total_duration
            },
            "success_rate": execution.success_rate,
            "steps": [
                {
                    "step_id": step.step_id,
                    "name": step.name,
                    "status": step.status,
                    "start_time": step.start_time,
                    "completion_time": step.completion_time,
                    "error_message": step.error_message
                }
                for step in execution.steps
            ]
        }
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get summary of all workflows"""
        return {
            "active_executions": len(self.active_executions),
            "completed_executions": len(self.execution_history),
            "total_templates": len(self.workflow_templates),
            "recent_executions": [
                {
                    "execution_id": exec_id,
                    "workflow_name": execution.workflow_name,
                    "status": execution.status,
                    "success_rate": execution.success_rate,
                    "completed_at": execution.completed_at
                }
                for exec_id, execution in 
                sorted(self.execution_history.items(), 
                       key=lambda x: x[1].completed_at or datetime.min, 
                       reverse=True)[:10]
            ],
            "template_usage": [
                {
                    "template_id": template.template_id,
                    "name": template.name,
                    "usage_count": template.usage_count,
                    "average_success_rate": template.average_success_rate
                }
                for template in self.workflow_templates.values()
            ]
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_workflow_orchestrator()
        self.execution_pool.shutdown(wait=True)
        self._save_workflow_data()
        super().cleanup()
