"""
Overnight Orchestrator - V2 Compliant
=====================================

Main orchestrator for 24/7 autonomous agent operations.
Extends V2's core orchestration with cycle-based scheduling and agent coordination.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
import logging

# V2 Integration imports
try:
    from ...core.orchestration.core_orchestrator import CoreOrchestrator
    from ...core.messaging_pyautogui import send_message_to_agent
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
    from ...workflows import WorkflowEngine
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    class CoreOrchestrator:
        pass
    
    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True
    
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)
    
    class WorkflowEngine:
        pass

from .scheduler import TaskScheduler
from .monitor import ProgressMonitor
from .recovery import RecoverySystem


class OvernightOrchestrator(CoreOrchestrator):
    """
    Main orchestrator for overnight autonomous operations.
    
    Extends V2's core orchestration with:
    - 24/7 autonomous execution
    - Cycle-based scheduling (V2 requirement)
    - Agent task distribution
    - Workflow integration
    - Recovery and monitoring
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize overnight orchestrator.
        
        Args:
            config: Configuration dictionary (uses config/orchestration.yml if None)
        """
        super().__init__()
        
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Overnight settings
        overnight_config = self.config.get('overnight', {})
        self.enabled = overnight_config.get('enabled', True)
        self.cycle_interval = overnight_config.get('cycle_interval', 10)  # minutes (V2 cycle-based)
        self.max_cycles = overnight_config.get('max_cycles', 60)  # 10 hours
        self.auto_restart = overnight_config.get('auto_restart', True)
        
        # Initialize components
        self.scheduler = TaskScheduler(self.config)
        self.monitor = ProgressMonitor(self.config)
        self.recovery = RecoverySystem(self.config)
        
        # State
        self.is_running = False
        self.current_cycle = 0
        self.start_time = 0
        self.active_agents = []
        self.workflow_engine = None
        
        # Integration flags
        self.workflow_integration = overnight_config.get('integration', {}).get('workflow_engine', True)
        self.vision_integration = overnight_config.get('integration', {}).get('vision_system', False)
        self.messaging_integration = overnight_config.get('integration', {}).get('messaging_system', True)
        self.coordinate_integration = overnight_config.get('integration', {}).get('coordinate_system', True)
        
        self.logger.info("Overnight Orchestrator initialized")

    async def start(self) -> None:
        """Start overnight autonomous operations."""
        if not self.enabled:
            self.logger.warning("Overnight operations disabled")
            return
        
        if self.is_running:
            self.logger.warning("Overnight orchestrator already running")
            return
        
        self.is_running = True
        self.current_cycle = 0
        self.start_time = time.time()
        
        self.logger.info("Starting overnight autonomous operations")
        
        try:
            # Initialize components
            await self._initialize_components()
            
            # Start monitoring
            self.monitor.start_monitoring()
            
            # Main execution loop
            await self._execute_overnight_loop()
            
        except Exception as e:
            self.logger.error(f"Overnight operations failed: {e}")
            raise
        finally:
            self.is_running = False
            self.monitor.stop_monitoring()
            self.logger.info("Overnight operations stopped")

    async def stop(self) -> None:
        """Stop overnight operations gracefully."""
        self.logger.info("Stopping overnight operations")
        self.is_running = False

    async def _initialize_components(self) -> None:
        """Initialize orchestrator components."""
        try:
            # Initialize scheduler
            await self.scheduler.initialize()
            
            # Initialize recovery system
            await self.recovery.initialize()
            
            # Initialize workflow engine if enabled
            if self.workflow_integration:
                self.workflow_engine = WorkflowEngine("overnight_operations")
                self.logger.info("Workflow engine initialized")
            
            # Get active agents
            self.active_agents = await self._get_active_agents()
            self.logger.info(f"Found {len(self.active_agents)} active agents")
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            raise

    async def _execute_overnight_loop(self) -> None:
        """Main overnight execution loop with cycle-based scheduling."""
        self.logger.info(f"Starting overnight loop: {self.max_cycles} cycles, {self.cycle_interval} min intervals")
        
        while self.is_running and self.current_cycle < self.max_cycles:
            try:
                self.current_cycle += 1
                cycle_start_time = time.time()
                
                self.logger.info(f"Starting cycle {self.current_cycle}/{self.max_cycles}")
                
                # Execute cycle
                await self._execute_cycle()
                
                # Update monitoring
                self.monitor.update_cycle(self.current_cycle, cycle_start_time)
                
                # Check for recovery needs
                await self._check_recovery()
                
                # Calculate sleep time for cycle interval
                cycle_duration = time.time() - cycle_start_time
                sleep_time = max(0, (self.cycle_interval * 60) - cycle_duration)
                
                if sleep_time > 0:
                    self.logger.info(f"Cycle {self.current_cycle} completed, sleeping {sleep_time:.1f}s")
                    await asyncio.sleep(sleep_time)
                else:
                    self.logger.warning(f"Cycle {self.current_cycle} took longer than interval")
                
            except Exception as e:
                self.logger.error(f"Cycle {self.current_cycle} failed: {e}")
                
                # Attempt recovery
                if self.auto_restart:
                    await self.recovery.handle_cycle_failure(self.current_cycle, str(e))
                
                # Continue to next cycle
                continue
        
        self.logger.info(f"Overnight loop completed after {self.current_cycle} cycles")

    async def _execute_cycle(self) -> None:
        """Execute a single cycle of autonomous operations."""
        try:
            # Get tasks for this cycle
            tasks = await self.scheduler.get_cycle_tasks(self.current_cycle)
            
            if not tasks:
                self.logger.info(f"No tasks scheduled for cycle {self.current_cycle}")
                return
            
            self.logger.info(f"Executing {len(tasks)} tasks in cycle {self.current_cycle}")
            
            # Distribute tasks to agents
            for task in tasks:
                await self._distribute_task(task)
            
            # Execute workflow if available
            if self.workflow_engine:
                await self._execute_workflow_cycle()
            
            # Update progress
            self.monitor.update_tasks(tasks)
            
        except Exception as e:
            self.logger.error(f"Cycle execution failed: {e}")
            raise

    async def _distribute_task(self, task: Dict[str, Any]) -> None:
        """Distribute a task to an agent."""
        try:
            agent_id = task.get('agent_id')
            task_type = task.get('type')
            task_data = task.get('data', {})
            
            if not agent_id:
                self.logger.warning("Task missing agent_id, skipping")
                return
            
            # Create task message
            message = self._create_task_message(task_type, task_data)
            
            # Send to agent
            if self.messaging_integration:
                success = await asyncio.get_event_loop().run_in_executor(
                    None,
                    send_message_to_agent,
                    agent_id,
                    message
                )
                
                if success:
                    self.logger.info(f"Task distributed to {agent_id}: {task_type}")
                else:
                    self.logger.error(f"Failed to distribute task to {agent_id}")
            
        except Exception as e:
            self.logger.error(f"Task distribution failed: {e}")

    def _create_task_message(self, task_type: str, task_data: Dict[str, Any]) -> str:
        """Create task message for agent."""
        return f"""
[OVERNIGHT TASK] Cycle {self.current_cycle}
Type: {task_type}
Data: {task_data}
Timestamp: {time.time()}

Execute this task autonomously. Report completion or issues.
"""

    async def _execute_workflow_cycle(self) -> None:
        """Execute workflow for current cycle."""
        try:
            if not self.workflow_engine:
                return
            
            # Create cycle-specific workflow
            await self._create_cycle_workflow()
            
            # Execute workflow (simplified)
            self.logger.info("Executing cycle workflow")
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")

    async def _create_cycle_workflow(self) -> None:
        """Create workflow for current cycle."""
        # This would integrate with the workflow system
        # For now, just log the intention
        self.logger.info(f"Creating workflow for cycle {self.current_cycle}")

    async def _get_active_agents(self) -> List[str]:
        """Get list of active agents."""
        # Default agent list - would integrate with agent registry
        return [f"Agent-{i}" for i in range(1, 9)]

    async def _check_recovery(self) -> None:
        """Check if recovery actions are needed."""
        try:
            # Check for stalled agents
            stalled_agents = await self.monitor.get_stalled_agents()
            
            if stalled_agents:
                self.logger.warning(f"Found {len(stalled_agents)} stalled agents")
                await self.recovery.handle_stalled_agents(stalled_agents)
            
            # Check system health
            health_status = await self.monitor.get_health_status()
            
            if not health_status.get('healthy', True):
                self.logger.warning("System health issues detected")
                await self.recovery.handle_health_issues(health_status)
                
        except Exception as e:
            self.logger.error(f"Recovery check failed: {e}")

    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get current orchestrator status."""
        return {
            "enabled": self.enabled,
            "is_running": self.is_running,
            "current_cycle": self.current_cycle,
            "max_cycles": self.max_cycles,
            "cycle_interval": self.cycle_interval,
            "start_time": self.start_time,
            "active_agents": len(self.active_agents),
            "workflow_integration": self.workflow_integration,
            "vision_integration": self.vision_integration,
            "messaging_integration": self.messaging_integration,
            "coordinate_integration": self.coordinate_integration,
            "auto_restart": self.auto_restart,
        }
