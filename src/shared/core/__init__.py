#!/usr/bin/env python3
"""
Shared Core Components
======================

Unified core functionality for Agent Cellphone V2 project.
Consolidates common core patterns from multiple modules.

V2 Compliance: ≤400 lines, single responsibility, type hints
Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BaseConfig:
    """Base configuration class for shared components."""
    
    project_root: str = "."
    log_level: str = "INFO"
    debug: bool = False
    
    def __post_init__(self):
        """Initialize configuration after dataclass creation."""
        if isinstance(self.project_root, str):
            self.project_root = Path(self.project_root).resolve()


@dataclass
class WorkflowStep:
    """Represents a single step in a workflow."""
    
    name: str
    action: str
    status: str = "pending"
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseScanner:
    """Base scanner class with common functionality."""
    
    def __init__(self, config: BaseConfig):
        """Initialize scanner with configuration."""
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def scan_directory(self, path: Path) -> List[Path]:
        """Scan directory for files matching criteria."""
        files = []
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    files.append(item)
        except Exception as e:
            self.logger.error(f"Error scanning directory {path}: {e}")
        return files
    
    def load_json_file(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load JSON file safely."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading JSON file {path}: {e}")
            return None
    
    def save_json_file(self, path: Path, data: Dict[str, Any]) -> bool:
        """Save data to JSON file safely."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Error saving JSON file {path}: {e}")
            return False


class BaseWorkflow:
    """Base workflow class with common workflow functionality."""
    
    def __init__(self, config: BaseConfig):
        """Initialize workflow with configuration."""
        self.config = config
        self.steps: List[WorkflowStep] = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def add_step(self, name: str, action: str, metadata: Optional[Dict[str, Any]] = None) -> WorkflowStep:
        """Add a new step to the workflow."""
        step = WorkflowStep(name=name, action=action, metadata=metadata)
        self.steps.append(step)
        return step
    
    def execute_step(self, step: WorkflowStep) -> bool:
        """Execute a workflow step."""
        try:
            step.status = "running"
            step.timestamp = datetime.now()
            self.logger.info(f"Executing step: {step.name}")
            
            # Step execution logic would go here
            step.status = "completed"
            return True
        except Exception as e:
            step.status = "failed"
            self.logger.error(f"Step {step.name} failed: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get workflow status."""
        return {
            "total_steps": len(self.steps),
            "completed": len([s for s in self.steps if s.status == "completed"]),
            "failed": len([s for s in self.steps if s.status == "failed"]),
            "pending": len([s for s in self.steps if s.status == "pending"]),
            "steps": [{"name": s.name, "status": s.status, "timestamp": s.timestamp} for s in self.steps]
        }


class BaseDiscordComponent:
    """Base Discord component with common Discord functionality."""
    
    def __init__(self, config: BaseConfig):
        """Initialize Discord component with configuration."""
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.is_connected = False
    
    def validate_discord_config(self) -> bool:
        """Validate Discord configuration."""
        required_vars = ["DISCORD_BOT_TOKEN", "DISCORD_CHANNEL_ID"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self.logger.error(f"Missing Discord environment variables: {missing_vars}")
            return False
        
        return True
    
    def log_discord_event(self, event: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Log Discord event."""
        log_data = {"event": event, "timestamp": datetime.now()}
        if data:
            log_data.update(data)
        self.logger.info(f"Discord event: {json.dumps(log_data, default=str)}")


# Utility functions
def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).resolve().parents[3]


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def ensure_directory(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def safe_file_operation(operation, *args, **kwargs):
    """Safely execute file operation with error handling."""
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        logger.error(f"File operation failed: {e}")
        return None

