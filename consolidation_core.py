#!/usr/bin/env python3
"""
Core Logic Consolidation - Logic Consolidation System
==================================================

Core consolidation functionality for the logic consolidation system.

Author: Agent-8 (Integration Enhancement Optimization Manager)
License: MIT
"""

import logging
from typing import Dict, List, Any

from logic_pattern_scanner import LogicPatternScanner
from logic_consolidator import LogicConsolidator
from logic_report_generator import LogicReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LogicConsolidatorCore:
    """Core system for consolidating duplicate logic patterns."""

    def __init__(self):
        self.scanner = LogicPatternScanner()
        self.consolidator = LogicConsolidator()
        self.report_generator = LogicReportGenerator()
        self.total_duplicates_found = 0
        self.total_duplicates_eliminated = 0

    def run_logic_consolidation_mission(self) -> Dict[str, Any]:
        """Run the complete logic consolidation mission."""
        logger.info("🚀 Starting logic consolidation mission...")

        try:
            # Step 1: Scan for logic patterns
            logic_patterns = self.scanner.scan_for_logic_patterns()
            self.total_duplicates_found = self.scanner.total_duplicates_found

            # Step 2: Identify duplicates
            duplicates = self.scanner.get_duplicate_logic()

            # Step 3: Create consolidated logic systems
            consolidated_files = self.consolidator.create_consolidated_logic_system(logic_patterns)
            self.total_duplicates_eliminated = self.consolidator.total_duplicates_eliminated

            # Step 4: Generate logic report
            report = self.report_generator.generate_logic_report(
                logic_patterns, 
                consolidated_files, 
                self.total_duplicates_found, 
                self.total_duplicates_eliminated
            )

            logger.info("🎯 Logic consolidation mission completed successfully!")
            return {
                'success': True,
                'logic_pattern_types_found': len(logic_patterns),
                'total_duplicates_found': self.total_duplicates_found,
                'total_duplicates_eliminated': self.total_duplicates_eliminated,
                'consolidated_logic_systems_created': len(consolidated_files),
                'logic_report': report
            }

        except Exception as e:
            logger.error(f"Error during logic consolidation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
