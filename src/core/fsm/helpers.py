import json
from pathlib import Path
from typing import Any, Dict, Optional

def load_fsm_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Load FSM configuration from a file or return defaults."""
    try:
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {
            "max_concurrent_workflows": 10,
            "default_timeout": 300.0,
            "enable_logging": True,
            "retry_policy": {
                "max_retries": 3,
                "retry_delay": 5.0,
                "exponential_backoff": True,
            },
            "monitoring": {
                "enabled": True,
                "interval": 1.0,
                "metrics_collection": True,
            },
        }
    except Exception as e:
        # If a logger is required, caller should handle logging
        return {}
