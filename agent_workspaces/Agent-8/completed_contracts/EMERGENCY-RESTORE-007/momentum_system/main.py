#!/usr/bin/env python3
"""
🚨 MOMENTUM ACCELERATION SYSTEM - MAIN MODULE 🚨

Main orchestration module for the modularized momentum acceleration system.

Author: Agent-8 (INTEGRATION ENHANCEMENT OPTIMIZATION MANAGER)
Contract: EMERGENCY-RESTORE-007
Status: MODULARIZED
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, Optional

from .models import MomentumAccelerationConfig
from .analytics import MomentumAnalytics
from .implementation import MomentumImplementationEngine
from .acceleration_measures import AccelerationMeasuresManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('momentum_acceleration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MomentumAccelerationSystem:
    """
    🚀 MOMENTUM ACCELERATION SYSTEM 🚀
    
    Modularized system that implements comprehensive acceleration measures to recover and sustain workflow momentum
    """
    
    def __init__(self, config: Optional[MomentumAccelerationConfig] = None):
        if config is None:
            config = MomentumAccelerationConfig()
        
        self.config = config
        self.analytics = MomentumAnalytics()
        self.implementation_engine = MomentumImplementationEngine(config)
        self.acceleration_measures = AccelerationMeasuresManager.get_all_measures()
        
        logger.info("🚀 Momentum Acceleration System initialized successfully")
    
    def run_full_acceleration_cycle(self) -> Dict:
        """
        Run a complete acceleration cycle including analysis and implementation
        
        Returns:
            Dictionary with complete cycle results
        """
        try:
            logger.info("🚀 Starting full momentum acceleration cycle...")
            
            cycle_results = {
                'timestamp': datetime.now().isoformat(),
                'cycle_id': f"CYCLE_{int(time.time())}",
                'analysis_results': {},
                'implementation_results': {},
                'overall_status': 'IN_PROGRESS'
            }
            
            # Step 1: Load and analyze task list data
            task_list_data = self._load_task_list_data()
            if task_list_data:
                contract_metrics = self.analytics.analyze_contract_completion_rates(task_list_data)
                cycle_results['analysis_results']['contract_metrics'] = contract_metrics
                logger.info("✅ Contract analysis completed")
            else:
                logger.warning("⚠️ Could not load task list data")
            
            # Step 2: Load and analyze meeting data
            meeting_data = self._load_meeting_data()
            if meeting_data:
                momentum_analysis = self.analytics.check_momentum_metrics(meeting_data)
                cycle_results['analysis_results']['momentum_analysis'] = momentum_analysis
                logger.info("✅ Momentum analysis completed")
            else:
                logger.warning("⚠️ Could not load meeting data")
            
            # Step 3: Generate productivity report
            if 'contract_metrics' in cycle_results['analysis_results'] and 'momentum_analysis' in cycle_results['analysis_results']:
                productivity_report = self.analytics.generate_productivity_report(
                    cycle_results['analysis_results']['contract_metrics'],
                    cycle_results['analysis_results']['momentum_analysis']
                )
                cycle_results['analysis_results']['productivity_report'] = productivity_report
                logger.info("✅ Productivity report generated")
            
            # Step 4: Implement acceleration measures
            implementation_results = self.implementation_engine.implement_momentum_acceleration_measures()
            cycle_results['implementation_results'] = implementation_results
            logger.info("✅ Acceleration measures implemented")
            
            # Step 5: Update overall status
            if 'error' not in implementation_results:
                cycle_results['overall_status'] = 'COMPLETED_SUCCESSFULLY'
                logger.info("🎉 Full acceleration cycle completed successfully")
            else:
                cycle_results['overall_status'] = 'COMPLETED_WITH_ERRORS'
                logger.error("❌ Acceleration cycle completed with errors")
            
            return cycle_results
            
        except Exception as e:
            logger.error(f"❌ Error in full acceleration cycle: {e}")
            return {'error': str(e), 'overall_status': 'FAILED'}
    
    def _load_task_list_data(self) -> Optional[Dict]:
        """Load task list data from JSON file"""
        try:
            with open('agent_workspaces/meeting/task_list.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("⚠️ task_list.json not found")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parsing task_list.json: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error loading task_list.json: {e}")
            return None
    
    def _load_meeting_data(self) -> Optional[Dict]:
        """Load meeting data from JSON file"""
        try:
            with open('agent_workspaces/meeting/meeting.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("⚠️ meeting.json not found")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parsing meeting.json: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error loading meeting.json: {e}")
            return None
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'current_phase': self.implementation_engine.current_phase.value,
            'current_status': self.implementation_engine.current_status.value,
            'total_measures': len(self.acceleration_measures),
            'emergency_contracts_generated': self.implementation_engine.emergency_contracts_generated,
            'perpetual_motion_contracts_generated': self.implementation_engine.perpetual_motion_contracts_generated,
            'momentum_sustainment_contracts_generated': self.implementation_engine.momentum_sustainment_contracts_generated
        }
    
    def run_continuous_monitoring(self, interval_minutes: int = 5, max_cycles: int = 12):
        """
        Run continuous monitoring with specified interval
        
        Args:
            interval_minutes: Minutes between cycles
            max_cycles: Maximum number of cycles to run
        """
        logger.info(f"🔄 Starting continuous monitoring - {interval_minutes} minute intervals, max {max_cycles} cycles")
        
        cycle_count = 0
        while cycle_count < max_cycles:
            try:
                logger.info(f"🔄 Running cycle {cycle_count + 1}/{max_cycles}")
                
                # Run acceleration cycle
                cycle_results = self.run_full_acceleration_cycle()
                
                if cycle_results.get('overall_status') == 'COMPLETED_SUCCESSFULLY':
                    logger.info(f"✅ Cycle {cycle_count + 1} completed successfully")
                else:
                    logger.warning(f"⚠️ Cycle {cycle_count + 1} completed with issues")
                
                cycle_count += 1
                
                # Wait for next cycle (except for the last one)
                if cycle_count < max_cycles:
                    logger.info(f"⏳ Waiting {interval_minutes} minutes until next cycle...")
                    time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("🛑 Continuous monitoring interrupted by user")
                break
            except Exception as e:
                logger.error(f"❌ Error in continuous monitoring cycle {cycle_count + 1}: {e}")
                cycle_count += 1
        
        logger.info(f"🏁 Continuous monitoring completed after {cycle_count} cycles")

def main():
    """Main entry point for the momentum acceleration system"""
    try:
        logger.info("🚀 Starting Momentum Acceleration System...")
        
        # Initialize system
        system = MomentumAccelerationSystem()
        
        # Run single acceleration cycle
        results = system.run_full_acceleration_cycle()
        
        if results.get('overall_status') == 'COMPLETED_SUCCESSFULLY':
            logger.info("🎉 Momentum acceleration cycle completed successfully")
            logger.info(f"   Contracts Generated: {results['implementation_results'].get('total_contracts_generated', 0)}")
            logger.info(f"   Points Added: {results['implementation_results'].get('total_points_added', 0)}")
        else:
            logger.error("❌ Momentum acceleration cycle failed")
        
        # Display system status
        status = system.get_system_status()
        logger.info(f"📊 System Status: {status['current_phase']} - {status['current_status']}")
        
    except Exception as e:
        logger.error(f"❌ Fatal error in main: {e}")
        raise

if __name__ == "__main__":
    main()
