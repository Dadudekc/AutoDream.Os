#!/usr/bin/env python3
"""
Integrated Onboarding & Coordination System - Modularized Version

This system provides comprehensive agent onboarding, contract management, 
FSM state tracking, and cycle coordination for the swarm agent system.

Features:
- Agent onboarding and status tracking
- Contract system for task commitments
- FSM (Finite State Machine) for state management
- Enhanced cycle coordination with PyAutoGUI automation
- CLI interface for system management

Usage:
    python integrated_onboarding_coordination_system_modular.py [options]

Author: Agent-2 (Architecture & Design Specialist)
"""

import argparse
import logging
import sys
import os
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('coordination_system.log')
    ]
)
logger = logging.getLogger(__name__)

# Import modularized components
from src.core.coordination import IntegratedOnboardingCoordinationSystem


def main():
    """Main entry point for the coordination system."""
    parser = argparse.ArgumentParser(
        description="Integrated Onboarding & Coordination System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Status commands
    parser.add_argument('--status', action='store_true', 
                      help='Show overall system status')
    parser.add_argument('--onboarding-status', action='store_true',
                      help='Show agent onboarding status')
    parser.add_argument('--contract-status', action='store_true',
                      help='Show active contracts status')
    parser.add_argument('--fsm-status', action='store_true',
                      help='Show FSM status for all agents')
    
    # Action commands
    parser.add_argument('--cycle', action='store_true',
                      help='Run enhanced coordination cycle')
    parser.add_argument('--create-contract', type=str,
                      help='Create contract: agent_id:type:description:cycles')
    parser.add_argument('--onboard-agent', type=str,
                      help='Onboard agent: agent_id:role or just agent_id')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize coordination system
    try:
        coordination_system = IntegratedOnboardingCoordinationSystem()
        logger.info("✅ Integrated Onboarding & Coordination System initialized")
        
        # Run CLI with parsed arguments
        coordination_system.run_cli(sys.argv[1:])
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize coordination system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()