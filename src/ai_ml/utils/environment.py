import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def create_directory_structure(base_path: str = ".") -> Dict[str, Path]:
    """Create AI/ML directory structure."""
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
        except Exception as e:  # pragma: no cover - filesystem path
            logger.error(f"Error creating directory {path}: {e}")
    return created_dirs


def validate_environment() -> Dict[str, bool]:
    """Validate AI/ML environment setup."""
    validation_results: Dict[str, bool] = {}
    import sys

    python_version = sys.version_info
    validation_results["python_version"] = python_version >= (3, 8)
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
    config_files = ["config/ai_ml/ai_ml.json", ".env.template"]
    for config_file in config_files:
        validation_results[
            f"config_{config_file.replace('/', '_').replace('.', '_')}"
        ] = Path(config_file).exists()
    return validation_results


def generate_environment_report() -> str:
    """Generate comprehensive environment report."""
    validation_results = validate_environment()
    report = "# AI/ML Environment Report\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    total_checks = len(validation_results)
    passed_checks = sum(validation_results.values())
    success_rate = (passed_checks / total_checks) * 100
    report += f"## Summary\n"
    report += f"- **Total Checks:** {total_checks}\n"
    report += f"- **Passed:** {passed_checks}\n"
    report += f"- **Failed:** {total_checks - passed_checks}\n"
    report += f"- **Success Rate:** {success_rate:.1f}%\n\n"
    report += "## Detailed Results\n\n"
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


def cleanup_temp_files(temp_dir: str = "temp") -> int:
    """Clean up temporary files."""
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
                try:
                    file_path.rmdir()
                except OSError:
                    pass
        logger.info(f"Cleaned up {cleaned_count} temporary files")
    except Exception as e:  # pragma: no cover - filesystem path
        logger.error(f"Error cleaning up temporary files: {e}")
    return cleaned_count
