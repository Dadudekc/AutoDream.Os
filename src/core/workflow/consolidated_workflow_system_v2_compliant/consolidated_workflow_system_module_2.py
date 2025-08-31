    """Workflow execution instance."""
    id: str
    workflow_id: str
    status: WorkflowStatus
    start_time: float
    end_time: Optional[float] = None
    tasks_completed: List[str] = field(default_factory=list)
    tasks_failed: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowEngine(ABC):
    """Abstract workflow execution engine."""
    
    @abstractmethod
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow."""
        pass
    
    @abstractmethod
    async def cancel_workflow(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        pass
    
    @abstractmethod
    async def pause_workflow(self, execution_id: str) -> bool:
        """Pause workflow execution."""
        pass
    
    @abstractmethod
    async def resume_workflow(self, execution_id: str) -> bool:
        """Resume workflow execution."""
        pass


class SequentialWorkflowEngine(WorkflowEngine):
    """Sequential workflow execution engine."""
    
    def __init__(self):
        self.workflows: Dict[str, List[WorkflowTask]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self._lock = threading.Lock()
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask]):
        """Register a workflow definition."""
        with self._lock:
            self.workflows[workflow_id] = tasks
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow sequentially."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution = WorkflowExecution(
            id=f"{workflow_id}_{int(time.time())}",
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            start_time=time.time()
        )
        
        self.executions[execution.id] = execution
        
        try:
            tasks = self.workflows[workflow_id]
            total_tasks = len(tasks)
            
            for i, task in enumerate(tasks):
                execution.current_task = task.id
                execution.progress = (i / total_tasks) * 100
                
                # Check dependencies
                if not all(dep in execution.tasks_completed for dep in task.dependencies):
                    raise Exception(f"Task {task.id} dependencies not met")
                
                # Execute task with retry logic
                success = False
                for attempt in range(task.retry_count + 1):
                    try:
                        if asyncio.iscoroutinefunction(task.action):
                            result = await asyncio.wait_for(task.action(**parameters), timeout=task.timeout)
                        else:
                            result = task.action(**parameters)
                        
                        execution.tasks_completed.append(task.id)
                        success = True
                        break
                    except Exception as e:
                        if attempt < task.retry_count:
                            await asyncio.sleep(task.retry_delay)
                        else:
                            execution.tasks_failed.append(task.id)
                            raise e
                
                if not success:
                    break
            
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = time.time()
            execution.progress = 100.0
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.error = str(e)
        
        return execution
    
    async def cancel_workflow(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.CANCELLED
                execution.end_time = time.time()
                return True
        return False
    
    async def pause_workflow(self, execution_id: str) -> bool:
        """Pause workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.PAUSED
                return True
        return False
    
    async def resume_workflow(self, execution_id: str) -> bool:
        """Resume workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.PAUSED:
                execution.status = WorkflowStatus.RUNNING
                return True
        return False


class ParallelWorkflowEngine(WorkflowEngine):