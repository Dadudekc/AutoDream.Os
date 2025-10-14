"""
Import System Mixins - Core Imports
===================================

Core imports mixin for unified import system.
Extracted from unified_import_system.py to reduce complexity.

V2 Compliance: Mixin pattern for modularity
SOLID Principles: Single Responsibility, Composition over Inheritance

Author: Agent-2 (Architecture & Design Specialist) - ROI 10.75 Task
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations


class CoreImportsMixin:
    """Mixin providing core Python imports via delegation.

    Provides access to: os, sys, json, logging, threading, time, re, datetime, Path
    """

    def __init__(self):
        """Initialize core imports mixin."""
        # Import core module for delegation
        from .import_core import ImportSystemCore

        if not hasattr(self, "_core"):
            self._core = ImportSystemCore()

    @property
    def os(self):
        """Get os module."""
        return self._core.os

    @property
    def sys(self):
        """Get sys module."""
        return self._core.sys

    @property
    def json(self):
        """Get json module."""
        return self._core.json

    @property
    def logging(self):
        """Get logging module."""
        return self._core.logging

    @property
    def threading(self):
        """Get threading module."""
        return self._core.threading

    @property
    def time(self):
        """Get time module."""
        return self._core.time

    @property
    def re(self):
        """Get re module."""
        return self._core.re

    @property
    def datetime(self):
        """Get datetime class."""
        return self._core.datetime

    @property
    def Path(self):
        """Get Path class."""
        return self._core.Path


class TypingImportsMixin:
    """Mixin providing typing imports via delegation.

    Provides access to: Any, Dict, List, Optional, Union, Callable, Tuple
    """

    def __init__(self):
        """Initialize typing imports mixin."""
        from .import_core import ImportSystemCore

        if not hasattr(self, "_core"):
            self._core = ImportSystemCore()

    @property
    def Any(self):
        """Get Any type."""
        return self._core.Any

    @property
    def Dict(self):
        """Get Dict type."""
        return self._core.Dict

    @property
    def List(self):
        """Get List type."""
        return self._core.List

    @property
    def Optional(self):
        """Get Optional type."""
        return self._core.Optional

    @property
    def Union(self):
        """Get Union type."""
        return self._core.Union

    @property
    def Callable(self):
        """Get Callable type."""
        return self._core.Callable

    @property
    def Tuple(self):
        """Get Tuple type."""
        return self._core.Tuple


class SpecialImportsMixin:
    """Mixin providing special Python imports via delegation.

    Provides access to: dataclass, field, Enum, ABC, abstractmethod
    """

    def __init__(self):
        """Initialize special imports mixin."""
        from .import_core import ImportSystemCore

        if not hasattr(self, "_core"):
            self._core = ImportSystemCore()

    @property
    def dataclass(self):
        """Get dataclass decorator."""
        return self._core.dataclass

    @property
    def field(self):
        """Get field function."""
        return self._core.field

    @property
    def Enum(self):
        """Get Enum class."""
        return self._core.Enum

    @property
    def ABC(self):
        """Get ABC class."""
        return self._core.ABC

    @property
    def abstractmethod(self):
        """Get abstractmethod decorator."""
        return self._core.abstractmethod


__all__ = [
    "CoreImportsMixin",
    "TypingImportsMixin",
    "SpecialImportsMixin",
]
