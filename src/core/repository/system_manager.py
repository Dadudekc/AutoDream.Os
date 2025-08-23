#!/usr/bin/env python3
"""
System Manager
=============

Handles system-level operations including cache, history, and status.
Keeps the main scanner focused on scanning operations.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

from .discovery_engine import RepositoryDiscoveryEngine
from .report_generator import RepositoryReportGenerator

logger = logging.getLogger(__name__)


class SystemManager:
    """Handles system-level operations and state management"""
    
    def __init__(self, discovery_engine: RepositoryDiscoveryEngine,
                 report_generator: RepositoryReportGenerator):
        """Initialize the system manager"""
        self.discovery_engine = discovery_engine
        self.report_generator = report_generator
        
        # Internal state
        self.scan_cache: Dict[str, Any] = {}
        self.scan_history: List[Dict[str, Any]] = []
        
        logger.info("System Manager initialized")

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            discovery_summary = self.discovery_engine.get_discovery_summary()
            report_stats = self.report_generator.get_report_statistics()
            
            return {
                "scanner_status": "active",
                "components": {
                    "discovery_engine": "active",
                    "technology_detector": "active",
                    "analysis_engine": "active",
                    "report_generator": "active",
                },
                "discovery_summary": discovery_summary,
                "report_statistics": report_stats,
                "scan_cache_size": len(self.scan_cache),
                "scan_history_count": len(self.scan_history),
            }
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}

    def add_scan_history(self, repository_id: str, scan_type: str, duration: float):
        """Add a scan to the history"""
        try:
            self.scan_history.append({
                "timestamp": datetime.now().isoformat(),
                "repository_id": repository_id,
                "scan_type": scan_type,
                "duration": duration,
            })
            logger.debug(f"Added scan to history: {repository_id}")
        except Exception as e:
            logger.error(f"Failed to add scan to history: {e}")

    def clear_cache(self):
        """Clear scan cache"""
        self.scan_cache.clear()
        logger.info("Scan cache cleared")

    def clear_history(self):
        """Clear scan history"""
        self.scan_history.clear()
        self.report_generator.clear_history()
        logger.info("Scan history cleared")

    def reset_system(self):
        """Reset the entire system"""
        self.clear_cache()
        self.clear_history()
        self.discovery_engine.clear_discovery_cache()
        self.report_generator.clear_repositories()
        logger.info("System reset completed")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the cache"""
        return {
            "cache_size": len(self.scan_cache),
            "history_count": len(self.scan_history)
        }

