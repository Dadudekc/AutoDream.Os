"""
Utilities Module
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Utility functions for configuration, logging, and performance monitoring
"""

import os
import json
import logging
import time
import functools
from typing import Dict, List, Optional, Any, Union, Callable
from pathlib import Path
from datetime import datetime
import traceback

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def config_loader(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from JSON file

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = "config/ai_ml/ai_ml_config.json"

    config_file = Path(config_path)

    if not config_file.exists():
        logger.warning(f"Configuration file not found: {config_path}")
        return {}

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from: {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration from {config_path}: {e}")
        return {}


def logger_setup(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """
    Setup logging configuration

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Optional custom log format

    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create logger
    logger_instance = logging.getLogger("ai_ml")
    logger_instance.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger_instance.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger_instance.addHandler(console_handler)

    # Create file handler if specified
    if log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            logger_instance.addHandler(file_handler)

            logger.info(f"File logging enabled: {log_file}")
        except Exception as e:
            logger.warning(f"Could not setup file logging: {e}")

    return logger_instance


def performance_monitor(func: Callable) -> Callable:
    """
    Decorator to monitor function performance

    Args:
        func: Function to monitor

    Returns:
        Wrapped function with performance monitoring
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = _get_memory_usage()

        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            logger.error(f"Function {func.__name__} failed: {e}")

        end_time = time.time()
        end_memory = _get_memory_usage()

        execution_time = end_time - start_time
        memory_delta = end_memory - start_memory

        # Log performance metrics
        logger.info(
            f"Performance: {func.__name__} - "
            f"Time: {execution_time:.4f}s, "
            f"Memory: {memory_delta:+d} bytes, "
            f"Success: {success}"
        )

        # Store performance data for analysis
        _store_performance_data(
            func.__name__, execution_time, memory_delta, success, error
        )

        if not success:
            raise Exception(error)

        return result

    return wrapper


def _get_memory_usage() -> int:
    """Get current memory usage in bytes"""
    try:
        import psutil

        process = psutil.Process()
        return process.memory_info().rss
    except ImportError:
        return 0


def _store_performance_data(
    func_name: str,
    execution_time: float,
    memory_delta: int,
    success: bool,
    error: Optional[str],
):
    """Store performance data for analysis"""
    try:
        performance_file = Path("workflow_data/ai_ml/performance_log.json")
        performance_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing data
        if performance_file.exists():
            with open(performance_file, "r") as f:
                performance_data = json.load(f)
        else:
            performance_data = {"functions": {}}

        # Add new data
        if func_name not in performance_data["functions"]:
            performance_data["functions"][func_name] = []

        performance_data["functions"][func_name].append(
            {
                "timestamp": datetime.now().isoformat(),
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "success": success,
                "error": error,
            }
        )

        # Keep only last 100 entries per function
        if len(performance_data["functions"][func_name]) > 100:
            performance_data["functions"][func_name] = performance_data["functions"][
                func_name
            ][-100:]

        # Save updated data
        with open(performance_file, "w") as f:
            json.dump(performance_data, f, indent=2)

    except Exception as e:
        logger.warning(f"Could not store performance data: {e}")


def create_directory_structure(base_path: str = ".") -> Dict[str, Path]:
    """
    Create AI/ML directory structure

    Args:
        base_path: Base path for directory creation

    Returns:
        Dictionary of created directories
    """
    base_path = Path(base_path)
    directories = {
        "config": base_path / "config" / "ai_ml",
        "examples": base_path / "examples" / "ai_ml",
        "tests": base_path / "tests" / "ai_ml",
        "src": base_path / "src" / "ai_ml",
        "docs": base_path / "docs" / "ai_ml",
        "workflow_data": base_path / "workflow_data" / "ai_ml",
        "models": base_path / "models",
        "logs": base_path / "logs",
        "cache": base_path / "cache" / "ai_ml",
    }

    created_dirs = {}
    for name, path in directories.items():
        try:
            path.mkdir(parents=True, exist_ok=True)
            created_dirs[name] = path
            logger.info(f"Created directory: {path}")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")

    return created_dirs


def validate_environment() -> Dict[str, bool]:
    """
    Validate AI/ML environment setup

    Returns:
        Dictionary of validation results
    """
    validation_results = {}

    # Check Python version
    import sys

    python_version = sys.version_info
    validation_results["python_version"] = python_version >= (3, 8)

    # Check required packages
    required_packages = [
        "openai",
        "anthropic",
        "torch",
        "transformers",
        "scikit-learn",
        "numpy",
        "pandas",
    ]

    for package in required_packages:
        try:
            __import__(package)
            validation_results[package] = True
        except ImportError:
            validation_results[package] = False

    # Check directory structure
    required_dirs = [
        "config/ai_ml",
        "examples/ai_ml",
        "tests/ai_ml",
        "src/ai_ml",
        "docs/ai_ml",
        "workflow_data/ai_ml",
    ]

    for dir_path in required_dirs:
        validation_results[f"dir_{dir_path.replace('/', '_')}"] = Path(
            dir_path
        ).exists()

    # Check configuration files
    config_files = ["config/ai_ml/ai_ml_config.json", ".env.template"]

    for config_file in config_files:
        validation_results[
            f"config_{config_file.replace('/', '_').replace('.', '_')}"
        ] = Path(config_file).exists()

    return validation_results


def generate_environment_report() -> str:
    """
    Generate comprehensive environment report

    Returns:
        Formatted environment report
    """
    validation_results = validate_environment()

    report = "# AI/ML Environment Report\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # Summary
    total_checks = len(validation_results)
    passed_checks = sum(validation_results.values())
    success_rate = (passed_checks / total_checks) * 100

    report += f"## Summary\n"
    report += f"- **Total Checks:** {total_checks}\n"
    report += f"- **Passed:** {passed_checks}\n"
    report += f"- **Failed:** {total_checks - passed_checks}\n"
    report += f"- **Success Rate:** {success_rate:.1f}%\n\n"

    # Detailed Results
    report += "## Detailed Results\n\n"

    # Group results by category
    categories = {
        "Python Environment": ["python_version"],
        "Required Packages": [
            k
            for k in validation_results.keys()
            if k not in ["python_version"]
            and not k.startswith("dir_")
            and not k.startswith("config_")
        ],
        "Directory Structure": [
            k for k in validation_results.keys() if k.startswith("dir_")
        ],
        "Configuration Files": [
            k for k in validation_results.keys() if k.startswith("config_")
        ],
    }

    for category, checks in categories.items():
        report += f"### {category}\n"
        for check in checks:
            status = "✅" if validation_results[check] else "❌"
            check_name = check.replace("_", " ").title()
            report += f"- {status} {check_name}\n"
        report += "\n"

    # Recommendations
    report += "## Recommendations\n\n"

    if success_rate < 100:
        failed_checks = [k for k, v in validation_results.items() if not v]
        report += "### Issues to Address:\n"
        for check in failed_checks:
            if check == "python_version":
                report += "- Upgrade Python to version 3.8 or higher\n"
            elif check in [
                "openai",
                "anthropic",
                "torch",
                "transformers",
                "scikit-learn",
                "numpy",
                "pandas",
            ]:
                report += f"- Install {check} package: `pip install {check}`\n"
            elif check.startswith("dir_"):
                dir_name = check.replace("dir_", "").replace("_", "/")
                report += f"- Create directory: `{dir_name}`\n"
            elif check.startswith("config_"):
                config_name = (
                    check.replace("config_", "").replace("_", "/").replace("_", ".")
                )
                report += f"- Create configuration file: `{config_name}`\n"
    else:
        report += (
            "✅ All checks passed! Your AI/ML environment is properly configured.\n"
        )

    return report


def setup_environment_variables() -> bool:
    """
    Setup environment variables from .env file

    Returns:
        True if successful, False otherwise
    """
    try:
        from dotenv import load_dotenv

        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("Environment variables loaded from .env file")
            return True
        else:
            logger.warning(".env file not found. Using system environment variables.")
            return False

    except ImportError:
        logger.warning("python-dotenv not installed. Cannot load .env file.")
        return False


def get_api_keys() -> Dict[str, Optional[str]]:
    """
    Get API keys from environment variables

    Returns:
        Dictionary of API keys
    """
    api_keys = {
        "openai": os.getenv("OPENAI_API_KEY"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "organization": os.getenv("OPENAI_ORGANIZATION"),
    }

    # Log which keys are available (without exposing the actual keys)
    for service, key in api_keys.items():
        if key:
            logger.info(f"{service.title()} API key configured")
        else:
            logger.warning(f"{service.title()} API key not configured")

    return api_keys


def cleanup_temp_files(temp_dir: str = "temp") -> int:
    """
    Clean up temporary files

    Args:
        temp_dir: Temporary directory path

    Returns:
        Number of files cleaned up
    """
    temp_path = Path(temp_dir)
    if not temp_path.exists():
        return 0

    cleaned_count = 0
    try:
        for file_path in temp_path.rglob("*"):
            if file_path.is_file():
                file_path.unlink()
                cleaned_count += 1
            elif file_path.is_dir():
                # Remove empty directories
                try:
                    file_path.rmdir()
                except OSError:
                    pass  # Directory not empty

        logger.info(f"Cleaned up {cleaned_count} temporary files")

    except Exception as e:
        logger.error(f"Error cleaning up temporary files: {e}")

    return cleaned_count
