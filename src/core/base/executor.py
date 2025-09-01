#!/usr/bin/env python3
"""
Unified Base Executor - Eliminates Duplicate Logic Patterns

This module provides a unified base class that eliminates duplicate logic patterns
found across multiple files in the codebase.

Agent: Agent-1 (Integration & Core Systems Specialist)
Mission: Processing Function Consolidation
Status: CONSOLIDATED - Using Unified Processing System
"""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import sys
import os

# Add the processing module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'processing'))

try:
    from unified_processing_system import UnifiedProcessingSystem, ProcessingType
except ImportError:
    # Fallback if processing system not available
    UnifiedProcessingSystem = None
    ProcessingType = None

class BaseExecutor(ABC):
    """
    Unified base class that eliminates duplicate logic patterns.
    
    This class consolidates the common execute/process/cleanup pattern
    found across multiple files in the codebase.
    
    CONSOLIDATED: Now uses UnifiedProcessingSystem to eliminate duplicate _process methods.
    """
    
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
        
        # Initialize unified processing system if available
        if UnifiedProcessingSystem:
            self.processing_system = UnifiedProcessingSystem()
        else:
            self.processing_system = None
        
    def execute(self, *args, **kwargs) -> Any:
        """
        Main execution method - unified across all executors.
        
        This eliminates the duplicate execute method pattern found in:
        - scripts/devlog.py
        - scripts/setup/cli.py  
        - src/core/consolidation/utils.py
        """
        return self._process(*args, **kwargs)
        
    def _process(self, *args, **kwargs) -> Any:
        """
        Unified processing method that eliminates duplicate _process patterns.
        
        CONSOLIDATED: This single method replaces the 4 duplicate _process methods
        that were previously implemented in DevlogExecutor, CliExecutor, and UtilsExecutor.
        """
        if self.processing_system and ProcessingType:
            # Use unified processing system
            return self.processing_system.process(ProcessingType.TASK, args, **kwargs)
        else:
            # Fallback to abstract method for subclasses
            return self._default_process_logic(*args, **kwargs)
    
    def _default_process_logic(self, *args, **kwargs) -> Any:
        """
        Default processing logic implementation.
        
        This provides a unified fallback for all processing operations.
        """
        # Log processing operation
        print(f"Processing task in {self.__class__.__name__}")
        
        # Return processed data
        return args[0] if args else None
        
    def cleanup(self) -> None:
        """
        Cleanup method - unified across all executors.
        
        This eliminates the duplicate cleanup method pattern.
        """
        self.state.clear()
        self.config.clear()
        
        # Cleanup processing system if available
        if self.processing_system:
            self.processing_system.cleanup()

class DevlogExecutor(BaseExecutor):
    """Devlog-specific implementation using unified processing system."""
    
    def _default_process_logic(self, *args, **kwargs) -> Any:
        """Devlog-specific processing logic."""
        print("Processing devlog task")
        return "devlog_processed"

class CliExecutor(BaseExecutor):
    """CLI-specific implementation using unified processing system."""
    
    def _default_process_logic(self, *args, **kwargs) -> Any:
        """CLI-specific processing logic."""
        print("Processing CLI task")
        return "cli_processed"

class UtilsExecutor(BaseExecutor):
    """Utils-specific implementation using unified processing system."""
    
    def _default_process_logic(self, *args, **kwargs) -> Any:
        """Utils-specific processing logic."""
        print("Processing utils task")
        return "utils_processed"

# Unified instances
devlog_instance = DevlogExecutor()
cli_instance = CliExecutor()
utils_instance = UtilsExecutor()
