"""
Import System Core - V2 Compliance Module
========================================

Core import functionality for unified import system.

V2 Compliance: < 300 lines, single responsibility, core imports.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import os
import sys
import json
import logging
import threading
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class ImportSystemCore:
    """Core import system functionality."""
    
    def __init__(self):
        """Initialize the core import system."""
        self._imports_cache = {}
        self._logger = None
    
    # ================================
    # CORE IMPORTS
    # ================================
    
    @property
    def os(self):
        """Get os module."""
        return os
    
    @property
    def sys(self):
        """Get sys module."""
        return sys
    
    @property
    def json(self):
        """Get json module."""
        return json
    
    @property
    def logging(self):
        """Get logging module."""
        return logging
    
    @property
    def threading(self):
        """Get threading module."""
        return threading
    
    @property
    def time(self):
        """Get time module."""
        return time
    
    @property
    def re(self):
        """Get re module."""
        return re
    
    @property
    def datetime(self):
        """Get datetime class."""
        return datetime
    
    @property
    def Path(self):
        """Get Path class."""
        return Path
    
    # ================================
    # TYPING IMPORTS
    # ================================
    
    @property
    def Any(self):
        """Get Any type."""
        return Any
    
    @property
    def Dict(self):
        """Get Dict type."""
        return Dict
    
    @property
    def List(self):
        """Get List type."""
        return List
    
    @property
    def Optional(self):
        """Get Optional type."""
        return Optional
    
    @property
    def Union(self):
        """Get Union type."""
        return Union
    
    @property
    def Callable(self):
        """Get Callable type."""
        return Callable
    
    @property
    def Tuple(self):
        """Get Tuple type."""
        return Tuple
    
    # ================================
    # DATACLASS IMPORTS
    # ================================
    
    @property
    def dataclass(self):
        """Get dataclass decorator."""
        return dataclass
    
    @property
    def field(self):
        """Get field function."""
        return field
    
    # ================================
    # ENUM IMPORTS
    # ================================
    
    @property
    def Enum(self):
        """Get Enum class."""
        return Enum
    
    # ================================
    # ABC IMPORTS
    # ================================
    
    @property
    def ABC(self):
        """Get ABC class."""
        return ABC
    
    @property
    def abstractmethod(self):
        """Get abstractmethod decorator."""
        return abstractmethod
