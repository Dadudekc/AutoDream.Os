    """Centralized workflow management system."""
    
    def __init__(self):
        self.sequential_engine = SequentialWorkflowEngine()
        self.parallel_engine = ParallelWorkflowEngine()
        self.workflow_registry: Dict[str, Dict[str, Any]] = {}
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask], parallel: bool = False):
        """Register workflow with appropriate engine."""
        if parallel:
            self.parallel_engine.register_workflow(workflow_id, tasks)
        else:
            self.sequential_engine.register_workflow(workflow_id, tasks)
        
        self.workflow_registry[workflow_id] = {
            'tasks': tasks,
            'parallel': parallel,
            'created_at': time.time()
        }
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow using appropriate engine."""
        if workflow_id not in self.workflow_registry:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow_info = self.workflow_registry[workflow_id]
        if workflow_info['parallel']:
            return await self.parallel_engine.execute_workflow(workflow_id, parameters)
        else:
            return await self.sequential_engine.execute_workflow(workflow_id, parameters)
    
    def get_workflow_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution status."""
        execution = self.sequential_engine.executions.get(execution_id)
        if not execution:
            execution = self.parallel_engine.executions.get(execution_id)
        return execution


class ConsolidatedWorkflowSystem:
    """Main consolidated workflow system."""
    
    def __init__(self):
        self.manager = WorkflowManager()
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]):
        """Initialize workflow system with configuration."""
        if self._initialized:
            return
        
        # Register default workflows if specified in config
        if 'default_workflows' in config:
            for workflow_config in config['default_workflows']:
                tasks = [
                    WorkflowTask(**task_config)
                    for task_config in workflow_config['tasks']
                ]
                self.manager.register_workflow(
                    workflow_config['id'],
                    tasks,
                    workflow_config.get('parallel', False)
                )
        
        self._initialized = True
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow."""
        if not self._initialized:
            raise RuntimeError("Workflow system not initialized")
        return await self.manager.execute_workflow(workflow_id, parameters)
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask], parallel: bool = False):
        """Register a new workflow."""
        self.manager.register_workflow(workflow_id, tasks, parallel)
    
    def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution status."""
        return self.manager.get_workflow_status(execution_id)
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        return await self.manager.sequential_engine.cancel_workflow(execution_id) or \
               await self.manager.parallel_engine.cancel_workflow(execution_id)


# Global workflow system instance
workflow_system = ConsolidatedWorkflowSystem()
