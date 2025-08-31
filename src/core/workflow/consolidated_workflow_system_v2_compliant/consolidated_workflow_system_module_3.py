    """Parallel workflow execution engine."""
    
    def __init__(self, max_workers: int = 4):
        self.workflows: Dict[str, List[WorkflowTask]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.max_workers = max_workers
        self._lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask]):
        """Register a workflow definition."""
        with self._lock:
            self.workflows[workflow_id] = tasks
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow with parallel task execution."""
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
            completed_tasks = set()
            failed_tasks = set()
            
            # Execute tasks in parallel where possible
            while len(completed_tasks) + len(failed_tasks) < len(tasks):
                ready_tasks = [
                    task for task in tasks
                    if task.id not in completed_tasks and task.id not in failed_tasks
                    and all(dep in completed_tasks for dep in task.dependencies)
                ]
                
                if not ready_tasks:
                    break
                
                # Execute ready tasks in parallel
                task_futures = []
                for task in ready_tasks:
                    future = asyncio.create_task(self._execute_task(task, parameters))
                    task_futures.append((task.id, future))
                
                # Wait for all tasks to complete
                for task_id, future in task_futures:
                    try:
                        await future
                        completed_tasks.add(task_id)
                        execution.tasks_completed.append(task_id)
                    except Exception as e:
                        failed_tasks.add(task_id)
                        execution.tasks_failed.append(task_id)
            
            execution.status = WorkflowStatus.COMPLETED if not failed_tasks else WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.progress = 100.0
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.error = str(e)
        
        return execution
    
    async def _execute_task(self, task: WorkflowTask, parameters: Dict[str, Any]):
        """Execute individual task with retry logic."""
        for attempt in range(task.retry_count + 1):
            try:
                if asyncio.iscoroutinefunction(task.action):
                    result = await asyncio.wait_for(task.action(**parameters), timeout=task.timeout)
                else:
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, task.action, **parameters
                    )
                return result
            except Exception as e:
                if attempt < task.retry_count:
                    await asyncio.sleep(task.retry_delay)
                else:
                    raise e
    
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


class WorkflowManager: