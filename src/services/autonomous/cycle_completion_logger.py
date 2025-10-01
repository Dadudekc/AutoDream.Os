"""
Cycle Completion Logger - High-Efficiency Protocol
==================================================

Logs agent cycle completions to status.json for tracking and accountability.
Implements Captain's High-Efficiency Protocol completion tracking.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, KISS principle
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CycleCompletionLogger:
    """Log cycle completions to agent status.json files"""
    
    def __init__(self, agent_id: str):
        """Initialize cycle completion logger"""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.status_file = self.workspace_path / "status.json"
    
    def log_completion(
        self,
        cycle_number: int,
        deliverables: List[Dict[str, Any]],
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Log cycle completion to status.json
        
        Args:
            cycle_number: Current cycle number
            deliverables: List of completed deliverables with details
            metrics: Optional metrics (files created, issues fixed, etc)
        
        Returns:
            bool: Success status
        """
        try:
            # Read current status
            status = self._read_status()
            
            # Initialize cycle_completions if not exists
            if 'cycle_completions' not in status:
                status['cycle_completions'] = []
            
            # Create completion entry
            completion_entry = {
                'cycle': cycle_number,
                'timestamp': datetime.now().isoformat(),
                'agent_id': self.agent_id,
                'deliverables': deliverables,
                'metrics': metrics or {},
                'status': 'completed'
            }
            
            # Add to cycle completions
            status['cycle_completions'].append(completion_entry)
            
            # Update summary metrics
            status = self._update_summary_metrics(status, completion_entry)
            
            # Update last_updated timestamp
            status['last_updated'] = datetime.now().isoformat()
            
            # Write back to file
            self._write_status(status)
            
            logger.info(f"Cycle {cycle_number} completion logged for {self.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging cycle completion: {e}")
            return False
    
    def _read_status(self) -> Dict[str, Any]:
        """Read current status.json"""
        if not self.status_file.exists():
            return {'agent_id': self.agent_id}
        
        try:
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading status.json: {e}")
            return {'agent_id': self.agent_id}
    
    def _write_status(self, status: Dict[str, Any]) -> None:
        """Write status.json"""
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def _update_summary_metrics(
        self,
        status: Dict[str, Any],
        completion: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update summary metrics based on completion"""
        # Initialize summary if not exists
        if 'total_metrics' not in status:
            status['total_metrics'] = {
                'total_cycles_completed': 0,
                'total_deliverables': 0,
                'total_issues_fixed': 0,
                'total_files_created': 0,
                'total_files_deleted': 0,
                'total_files_modified': 0,
            }
        
        # Update totals
        metrics = completion.get('metrics', {})
        status['total_metrics']['total_cycles_completed'] += 1
        status['total_metrics']['total_deliverables'] += len(completion.get('deliverables', []))
        status['total_metrics']['total_issues_fixed'] += metrics.get('issues_fixed', 0)
        status['total_metrics']['total_files_created'] += metrics.get('files_created', 0)
        status['total_metrics']['total_files_deleted'] += metrics.get('files_deleted', 0)
        status['total_metrics']['total_files_modified'] += metrics.get('files_modified', 0)
        
        return status
    
    def get_completion_summary(self) -> Dict[str, Any]:
        """Get summary of all cycle completions"""
        status = self._read_status()
        
        return {
            'agent_id': self.agent_id,
            'total_cycles': len(status.get('cycle_completions', [])),
            'total_metrics': status.get('total_metrics', {}),
            'last_completion': status.get('cycle_completions', [])[-1] if status.get('cycle_completions') else None
        }


def log_cycle_completion(
    agent_id: str,
    cycle_number: int,
    deliverables: List[Dict[str, Any]],
    metrics: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Helper function to log cycle completion
    
    Usage:
        from src.services.autonomous.cycle_completion_logger import log_cycle_completion
        
        deliverables = [
            {'type': 'file_created', 'name': 'messaging_checks.py', 'lines': 212},
            {'type': 'file_created', 'name': 'report_generator.py', 'lines': 251}
        ]
        
        metrics = {
            'issues_fixed': 3,
            'files_created': 2,
            'files_deleted': 15,
            'quality_score': 100
        }
        
        log_cycle_completion('Agent-7', 1, deliverables, metrics)
    """
    logger_instance = CycleCompletionLogger(agent_id)
    return logger_instance.log_completion(cycle_number, deliverables, metrics)


__all__ = [
    'CycleCompletionLogger',
    'log_cycle_completion',
]

