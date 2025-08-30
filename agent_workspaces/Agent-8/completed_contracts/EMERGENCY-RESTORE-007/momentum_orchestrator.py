#!/usr/bin/env python3
"""
Momentum Orchestrator Module
============================

Main orchestrator for momentum acceleration and contract management.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from .momentum_core import MomentumCore, MomentumStatus, AccelerationPhase, ContractMetrics
from .contract_manager import ContractManager, GeneratedContract


class MomentumOrchestrator:
    """Main orchestrator for momentum acceleration system"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = self._setup_logging()
        self.config_file = config_file
        
        # Initialize core components
        self.momentum_core = MomentumCore()
        self.contract_manager = ContractManager()
        
        # System state
        self.is_running = False
        self.last_cycle_time = datetime.now()
        self.cycle_count = 0
        
        # Load configuration if provided
        if config_file:
            self._load_configuration()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the orchestrator"""
        logger = logging.getLogger("MomentumOrchestrator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[ORCHESTRATOR] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _load_configuration(self) -> None:
        """Load configuration from file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration to components
                if 'momentum_config' in config:
                    self.momentum_core.config = config['momentum_config']
                
                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.logger.warning(f"Configuration file {self.config_file} not found")
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
    
    def start_momentum_system(self) -> bool:
        """Start the momentum acceleration system"""
        try:
            if self.is_running:
                self.logger.warning("Momentum system is already running")
                return True
            
            self.is_running = True
            self.last_cycle_time = datetime.now()
            self.cycle_count = 0
            
            self.logger.info("Momentum acceleration system started")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting momentum system: {e}")
            return False
    
    def stop_momentum_system(self) -> bool:
        """Stop the momentum acceleration system"""
        try:
            if not self.is_running:
                self.logger.warning("Momentum system is not running")
                return True
            
            self.is_running = False
            
            self.logger.info("Momentum acceleration system stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping momentum system: {e}")
            return False
    
    def execute_momentum_cycle(self) -> Dict[str, Any]:
        """Execute a single momentum acceleration cycle"""
        try:
            if not self.is_running:
                return {"error": "Momentum system is not running"}
            
            cycle_start = datetime.now()
            self.cycle_count += 1
            
            self.logger.info(f"Executing momentum cycle {self.cycle_count}")
            
            # Step 1: Assess current state
            current_metrics = self.contract_manager.contract_metrics
            current_status = self.momentum_core.assess_momentum_status(current_metrics)
            current_phase = self.momentum_core.determine_acceleration_phase(current_status)
            momentum_score = self.momentum_core.calculate_momentum_score(current_metrics)
            
            # Step 2: Update momentum history
            self.momentum_core.update_momentum_history(
                current_status, current_phase, current_metrics, momentum_score
            )
            
            # Step 3: Execute phase-specific actions
            phase_actions = self._execute_phase_actions(current_phase, current_status, current_metrics)
            
            # Step 4: Generate contracts if needed
            contracts_generated = self._generate_contracts_for_phase(current_phase, current_metrics)
            
            # Step 5: Update system state
            self.momentum_core.current_status = current_status
            self.momentum_core.current_phase = current_phase
            
            # Calculate cycle duration
            cycle_duration = (datetime.now() - cycle_start).total_seconds()
            
            cycle_results = {
                "cycle_number": self.cycle_count,
                "cycle_start": cycle_start.isoformat(),
                "cycle_duration_seconds": cycle_duration,
                "current_status": current_status.value,
                "current_phase": current_phase.value,
                "momentum_score": momentum_score,
                "phase_actions": phase_actions,
                "contracts_generated": len(contracts_generated),
                "metrics": {
                    "total_contracts": current_metrics.total_contracts,
                    "available_contracts": current_metrics.available_contracts,
                    "completion_rate": current_metrics.completion_rate
                }
            }
            
            self.logger.info(f"Momentum cycle {self.cycle_count} completed in {cycle_duration:.2f}s")
            return cycle_results
            
        except Exception as e:
            self.logger.error(f"Error executing momentum cycle: {e}")
            return {"error": str(e), "cycle_number": self.cycle_count}
    
    def _execute_phase_actions(self, phase: AccelerationPhase, status: MomentumStatus, 
                               metrics: ContractMetrics) -> Dict[str, Any]:
        """Execute actions specific to the current phase"""
        try:
            actions = {
                "phase": phase.value,
                "actions_executed": [],
                "results": {}
            }
            
            if phase == AccelerationPhase.EMERGENCY_RESPONSE:
                # Emergency response actions
                if metrics.available_contracts < 5:
                    emergency_contracts = self.contract_manager.generate_contracts(10, "emergency")
                    actions["actions_executed"].append("emergency_contract_generation")
                    actions["results"]["emergency_contracts"] = len(emergency_contracts)
                
                actions["actions_executed"].append("system_stabilization")
                
            elif phase == AccelerationPhase.SYSTEM_RECOVERY:
                # System recovery actions
                recovery_contracts = self.contract_manager.generate_contracts(15, "optimization")
                actions["actions_executed"].append("recovery_contract_generation")
                actions["results"]["recovery_contracts"] = len(recovery_contracts)
                
            elif phase == AccelerationPhase.MOMENTUM_SUSTAINMENT:
                # Momentum sustainment actions
                sustainment_contracts = self.contract_manager.generate_contracts(20, "momentum")
                actions["actions_executed"].append("sustainment_contract_generation")
                actions["results"]["sustainment_contracts"] = len(sustainment_contracts)
                
            elif phase == AccelerationPhase.CONTINUOUS_OPTIMIZATION:
                # Continuous optimization actions
                optimization_contracts = self.contract_manager.generate_contracts(25, "optimization")
                actions["actions_executed"].append("optimization_contract_generation")
                actions["results"]["optimization_contracts"] = len(optimization_contracts)
            
            return actions
            
        except Exception as e:
            self.logger.error(f"Error executing phase actions: {e}")
            return {"error": str(e), "phase": phase.value}
    
    def _generate_contracts_for_phase(self, phase: AccelerationPhase, 
                                     metrics: ContractMetrics) -> List[GeneratedContract]:
        """Generate contracts appropriate for the current phase"""
        try:
            if metrics.available_contracts >= 30:
                # Sufficient contracts available
                return []
            
            contracts_needed = 30 - metrics.available_contracts
            
            if phase == AccelerationPhase.EMERGENCY_RESPONSE:
                return self.contract_manager.generate_contracts(contracts_needed, "emergency")
            elif phase == AccelerationPhase.SYSTEM_RECOVERY:
                return self.contract_manager.generate_contracts(contracts_needed, "optimization")
            elif phase == AccelerationPhase.MOMENTUM_SUSTAINMENT:
                return self.contract_manager.generate_contracts(contracts_needed, "momentum")
            else:
                return self.contract_manager.generate_contracts(contracts_needed)
                
        except Exception as e:
            self.logger.error(f"Error generating contracts for phase: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            return {
                "system_running": self.is_running,
                "cycle_count": self.cycle_count,
                "last_cycle_time": self.last_cycle_time.isoformat(),
                "momentum_summary": self.momentum_core.get_momentum_summary(),
                "contract_summary": self.contract_manager.get_contract_summary(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def run_continuous_cycles(self, interval_seconds: int = 60, max_cycles: Optional[int] = None) -> None:
        """Run continuous momentum cycles at specified interval"""
        try:
            self.logger.info(f"Starting continuous momentum cycles (interval: {interval_seconds}s)")
            
            cycle_count = 0
            while self.is_running:
                if max_cycles and cycle_count >= max_cycles:
                    self.logger.info(f"Reached maximum cycles: {max_cycles}")
                    break
                
                # Execute cycle
                cycle_results = self.execute_momentum_cycle()
                cycle_count += 1
                
                if "error" in cycle_results:
                    self.logger.error(f"Cycle {cycle_count} failed: {cycle_results['error']}")
                
                # Wait for next cycle
                time.sleep(interval_seconds)
            
            self.logger.info(f"Continuous cycles stopped after {cycle_count} cycles")
            
        except KeyboardInterrupt:
            self.logger.info("Continuous cycles interrupted by user")
        except Exception as e:
            self.logger.error(f"Error in continuous cycles: {e}")
    
    def save_system_state(self, filepath: str) -> bool:
        """Save current system state to file"""
        try:
            state = {
                "timestamp": datetime.now().isoformat(),
                "system_status": self.get_system_status(),
                "momentum_history": self.momentum_core.momentum_history,
                "contracts": [asdict(c) for c in self.contract_manager.generated_contracts]
            }
            
            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2)
            
            self.logger.info(f"System state saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving system state: {e}")
            return False
