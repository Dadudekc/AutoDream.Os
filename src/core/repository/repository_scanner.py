#!/usr/bin/env python3
"""
Repository Scanner - Main Orchestrator
======================================

Main orchestrator for repository scanning operations.
Delegates specific responsibilities to focused components.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import our refactored components
from .discovery_engine import RepositoryDiscoveryEngine, DiscoveryConfig
from .technology_detector import TechnologyDetector
from .analysis_engine import RepositoryAnalysisEngine
from .report_generator import RepositoryReportGenerator
from .scanner_orchestrator import ScannerOrchestrator
from .parallel_processor import ParallelProcessor
from .system_manager import SystemManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RepositoryScanner:
    """
    Main repository scanner orchestrator
    
    Features:
    - High-level coordination of all components
    - Delegates specific operations to focused components
    - Provides unified interface for repository scanning
    """

    def __init__(self, config: Optional[DiscoveryConfig] = None):
        """Initialize the repository scanner"""
        self.config = config or DiscoveryConfig()
        
        # Initialize all components
        self.discovery_engine = RepositoryDiscoveryEngine(config)
        self.technology_detector = TechnologyDetector()
        self.analysis_engine = RepositoryAnalysisEngine()
        self.report_generator = RepositoryReportGenerator()
        
        # Initialize specialized components
        self.orchestrator = ScannerOrchestrator(
            self.discovery_engine,
            self.technology_detector,
            self.analysis_engine,
            self.report_generator
        )
        
        self.parallel_processor = ParallelProcessor()
        self.system_manager = SystemManager(
            self.discovery_engine,
            self.report_generator
        )
        
        logger.info("Repository Scanner initialized")

    def scan_repository(self, repository_path: str, deep_scan: bool = False):
        """Scan a single repository for comprehensive analysis"""
        return self.orchestrator.scan_repository(
            repository_path, 
            deep_scan, 
            self.system_manager.scan_cache
        )

    def scan_multiple_repositories(self, repository_paths: List[str], max_workers: int = 4):
        """Scan multiple repositories in parallel"""
        self.parallel_processor.set_max_workers(max_workers)
        return self.parallel_processor.process_repositories(
            repository_paths, 
            lambda path: self.scan_repository(path, deep_scan=True)
        )

    def discover_and_scan(self, root_path: str, recursive: bool = True):
        """Discover repositories and scan them automatically"""
        return self.orchestrator.discover_and_scan(root_path, recursive)

    def get_system_status(self):
        """Get comprehensive system status"""
        return self.system_manager.get_system_status()

    def export_comprehensive_report(self, output_path: Optional[str] = None):
        """Export a comprehensive report of all scanned repositories"""
        return self.report_generator.export_discovery_report(output_path)

    def clear_cache(self):
        """Clear scan cache"""
        self.system_manager.clear_cache()

    def clear_history(self):
        """Clear scan history"""
        self.system_manager.clear_history()

    def reset_system(self):
        """Reset the entire system"""
        self.system_manager.reset_system()


def main():
    """Main function for standalone testing"""
    from .cli_interface import CLIInterface
    
    scanner = RepositoryScanner()
    cli = CLIInterface(scanner)
    cli.run()


if __name__ == "__main__":
    main()
