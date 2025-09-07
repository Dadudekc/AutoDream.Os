"""Helpers for executing test commands."""
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List


def execute_command(cmd: List[str], cwd: Path, timeout: int = 300) -> Dict[str, Any]:
    """Execute a command and capture result metadata."""
    print(f"🚀 Executing: {' '.join(cmd)}")
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout
        )
        duration = time.time() - start_time
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
            "duration": duration,
            "command": " ".join(cmd),
            "timeout": True,
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Command execution error: {e}",
            "duration": duration,
            "command": " ".join(cmd),
            "error": str(e),
        }
