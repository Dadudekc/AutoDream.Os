"""Utility helpers consolidated into a single module.

These utilities are shared across systems and re-exported through the
``src.core.consolidation`` package as the SSOT.
"""

from __future__ import annotations

import json
import logging
import hashlib
import os
import platform
import shutil
import psutil
from typing import Any, Dict, List, Optional


class FileSystemUtils:
    """Unified file system utilities."""

    def ensure_directory(self, path: str) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False

    def safe_remove(self, path: str) -> bool:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except Exception:
            return False

    def get_file_hash(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None


class StringUtils:
    """Unified string utilities."""

    def sanitize_filename(self, filename: str) -> str:
        import re
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return sanitized.strip()

    def truncate_with_ellipsis(self, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    def normalize_whitespace(self, text: str) -> str:
        import re
        return re.sub(r"\s+", " ", text).strip()


class MathUtils:
    """Unified math utilities."""

    def calculate_percentage(self, part: float, total: float) -> float:
        if total == 0:
            return 0.0
        return (part / total) * 100.0

    def round_to_decimal(self, value: float, decimal_places: int) -> float:
        return round(value, decimal_places)

    def clamp_value(self, value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(value, max_val))


class IOUtils:
    """Unified IO utilities."""

    def read_json_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def write_json_file(self, file_path: str, data: Dict[str, Any]) -> bool:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def read_text_file(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None


class SystemUtils:
    """Unified system utilities."""

    def get_system_info(self) -> Dict[str, Any]:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count(),
            "memory_usage": psutil.virtual_memory().percent,
        }

    def get_process_info(self) -> Dict[str, Any]:
        process = psutil.Process()
        return {
            "pid": process.pid,
            "memory_usage": process.memory_info().rss,
            "cpu_percent": process.cpu_percent(),
        }

    def is_system_healthy(self) -> bool:
        try:
            memory = psutil.virtual_memory()
            return memory.percent < 90
        except Exception:
            return False


class ValidationUtils:
    """Unified validation utilities."""

    def validate_file_exists(self, file_path: str) -> bool:
        return os.path.isfile(file_path)

    def validate_directory_exists(self, dir_path: str) -> bool:
        return os.path.isdir(dir_path)

    def validate_json_structure(self, data: Dict[str, Any], required_keys: List[str]) -> bool:
        return all(key in data for key in required_keys)


class LoggingUtils:
    """Unified logging utilities."""

    def setup_logging(self, log_level: str = "INFO") -> None:
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("consolidated_utils.log"),
            ],
        )

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)


class ConfigUtils(IOUtils):
    """Unified configuration utilities built on top of IO utilities."""

    def load_config_file(self, config_path: str) -> Optional[Dict[str, Any]]:
        return self.read_json_file(config_path)

    def save_config_file(self, config_path: str, config_data: Dict[str, Any]) -> bool:
        return self.write_json_file(config_path, config_data)

    def merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        merged = base_config.copy()
        merged.update(override_config)
        return merged
