#!/usr/bin/env python3
"""
System Info Module - System Information Gathering

This module provides system information functions.
Follows Single Responsibility Principle - only system info gathering.
Architecture: Single Responsibility Principle - system info only
LOC: 120 lines (under 200 limit)
"""

import os
import sys
import psutil
import logging
from typing import Dict, Any
from pathlib import Path


class SystemInfo:
    """System information gathering utilities"""

    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            info = {
                "platform": sys.platform,
                "python_version": sys.version,
                "python_executable": sys.executable,
                "current_working_directory": os.getcwd(),
                "user_home": str(Path.home()),
                "environment_variables": dict(os.environ),
            }
            return info
        except Exception as e:
            logging.error(f"Failed to get system info: {e}")
            return {}

    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get memory usage information"""
        try:
            memory = psutil.virtual_memory()
            return {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent,
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
            }
        except Exception as e:
            logging.error(f"Failed to get memory info: {e}")
            return {}

    @staticmethod
    def get_disk_info(path: str = ".") -> Dict[str, Any]:
        """Get disk usage information for a path"""
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
            }
        except Exception as e:
            logging.error(f"Failed to get disk info for {path}: {e}")
            return {}

    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get CPU information"""
        try:
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()

            return {
                "cpu_count": cpu_count,
                "cpu_percent": cpu_percent,
                "cpu_freq_current": cpu_freq.current if cpu_freq else None,
                "cpu_freq_min": cpu_freq.min if cpu_freq else None,
                "cpu_freq_max": cpu_freq.max if cpu_freq else None,
            }
        except Exception as e:
            logging.error(f"Failed to get CPU info: {e}")
            return {}

    @staticmethod
    def get_environment_info() -> Dict[str, str]:
        """Get environment-specific information"""
        try:
            env_info = {
                "os_name": os.name,
                "os_environ": dict(os.environ),
                "python_path": sys.path,
                "executable": sys.executable,
                "version": sys.version,
            }
            return env_info
        except Exception as e:
            logging.error(f"Failed to get environment info: {e}")
            return {}


def run_smoke_test():
    """Run basic functionality test for SystemInfo"""
    print("🧪 Running SystemInfo Smoke Test...")

    try:
        # Test system info
        sys_info = SystemInfo.get_system_info()
        assert "platform" in sys_info
        assert "python_version" in sys_info

        # Test memory info
        mem_info = SystemInfo.get_memory_info()
        assert "total" in mem_info
        assert "percent" in mem_info

        # Test disk info
        disk_info = SystemInfo.get_disk_info()
        assert "total" in disk_info
        assert "free" in disk_info

        # Test CPU info
        cpu_info = SystemInfo.get_cpu_info()
        assert "cpu_count" in cpu_info

        print("✅ SystemInfo Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ SystemInfo Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for SystemInfo testing"""
    import argparse

    parser = argparse.ArgumentParser(description="System Info CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--system", action="store_true", help="Get system information")
    parser.add_argument("--memory", action="store_true", help="Get memory information")
    parser.add_argument("--disk", help="Get disk information for path")
    parser.add_argument("--cpu", action="store_true", help="Get CPU information")
    parser.add_argument(
        "--environment", action="store_true", help="Get environment info"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    if args.system:
        info = SystemInfo.get_system_info()
        print("System Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    elif args.memory:
        memory = SystemInfo.get_memory_info()
        print("Memory Information:")
        for key, value in memory.items():
            print(f"  {key}: {value}")
    elif args.disk:
        disk = SystemInfo.get_disk_info(args.disk)
        print(f"Disk Information for {args.disk}:")
        for key, value in disk.items():
            print(f"  {key}: {value}")
    elif args.cpu:
        cpu = SystemInfo.get_cpu_info()
        print("CPU Information:")
        for key, value in cpu.items():
            print(f"  {key}: {value}")
    elif args.environment:
        env = SystemInfo.get_environment_info()
        print("Environment Information:")
        for key, value in env.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
