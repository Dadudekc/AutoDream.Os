#!/usr/bin/env python3
"""
V3 Contract Execution System - V2 Compliant
===========================================

Refactored contract execution system using modular design.
V2 Compliance: ≤100 lines, single responsibility, KISS principle.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable

from .contracts import (
    ContractExecutionCore,
    ContractQualityValidator,
    ContractPerformanceMonitor,
    create_default_contracts,
    calculate_contract_metrics
)

logger = logging.getLogger(__name__)


class V3ContractExecutionSystem:
    """V3 Contract Execution System - Legacy compatibility wrapper."""
    
    def __init__(
        self,
        vector_integration=None,
        kiss_enforcement=None,
        quality_assurance=None,
        performance_optimization=None,
        config: Optional[Dict[str, Any]] = None
    ):
        """Initialize V3 contract execution system."""
        self.config = config or {}
        
        # Initialize modular components
        self.execution_core = ContractExecutionCore(self.config)
        self.quality_validator = ContractQualityValidator(quality_assurance)
        self.performance_monitor = ContractPerformanceMonitor()
        
        # Set up contracts
        default_contracts = create_default_contracts()
        self.execution_core.set_contracts(default_contracts)
        
        # Add quality monitoring callback
        self.execution_core.add_execution_callback(self._execution_callback)
        
        logger.info("V3 Contract Execution System initialized")
    
    def start_execution(self) -> None:
        """Start V3 contract execution system."""
        self.execution_core.start_execution()
    
    def stop_execution(self) -> None:
        """Stop V3 contract execution system."""
        self.execution_core.stop_execution()
    
    def add_execution_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Add execution callback."""
        self.execution_core.add_execution_callback(callback)
    
    def _execution_callback(self, update_data: Dict[str, Any]) -> None:
        """Internal execution callback for monitoring."""
        try:
            # Update performance monitoring
            contracts = self.execution_core.get_contracts()
            self.performance_monitor.update_execution_stats(contracts)
            
            # Validate quality
            quality_results = self.quality_validator.validate_contract_quality(contracts)
            
        except Exception as e:
            logger.error(f"Execution callback error: {e}")
    
    def get_v3_execution_status(self) -> Dict[str, Any]:
        """Get comprehensive V3 execution status."""
        try:
            contracts = self.execution_core.get_contracts()
            performance_metrics = self.performance_monitor.get_performance_metrics()
            contract_metrics = calculate_contract_metrics(contracts)
            
            return {
                'execution_running': self.execution_core._running,
                'contract_statuses': [contract.to_dict() for contract in contracts],
                'execution_stats': performance_metrics.get('execution_stats', {}),
                'contract_metrics': contract_metrics,
                'performance_metrics': performance_metrics,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get V3 execution status: {e}")
            return {'error': str(e)}
    
    def close(self) -> None:
        """Close V3 contract execution system."""
        self.execution_core.close()
