#!/usr/bin/env python3
"""
Log Rotation System for Agent Cellphone V2 Repository
====================================================

Implements log rotation for coordination_system.log and other log files.
Maintains log history and prevents disk space issues.

Author: Agent-5 (Data Organization Specialist)
Mission: DATA-ORGANIZE-001
License: MIT
"""

import os
import shutil
import gzip
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class LogRotationManager:
    """Manages log rotation for the repository."""
    
    def __init__(self, log_dir: str = ".", max_size_mb: int = 10, keep_rotated: int = 5):
        self.log_dir = Path(log_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.keep_rotated = keep_rotated
        
    def rotate_log(self, log_file: str) -> bool:
        """Rotate a log file if it exceeds size limit."""
        log_path = self.log_dir / log_file
        
        if not log_path.exists():
            return False
            
        # Check if rotation is needed
        if log_path.stat().st_size < self.max_size_bytes:
            return False
            
        # Create rotated filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_name = f"{log_path.stem}_{timestamp}{log_path.suffix}"
        rotated_path = self.log_dir / rotated_name
        
        try:
            # Move current log to rotated name
            shutil.move(str(log_path), str(rotated_path))
            
            # Compress the rotated log
            compressed_path = rotated_path.with_suffix(rotated_path.suffix + '.gz')
            with open(rotated_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed rotated file
            rotated_path.unlink()
            
            # Create new empty log file
            log_path.touch()
            
            logger.info(f"Rotated log file: {log_file} -> {compressed_path.name}")
            
            # Clean up old rotated logs
            self._cleanup_old_logs(log_file)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to rotate log {log_file}: {e}")
            return False
    
    def _cleanup_old_logs(self, log_file: str):
        """Remove old rotated log files beyond the keep limit."""
        log_stem = Path(log_file).stem
        
        # Find all rotated logs for this file
        rotated_logs = []
        for file_path in self.log_dir.glob(f"{log_stem}_*.gz"):
            rotated_logs.append(file_path)
        
        # Sort by modification time (newest first)
        rotated_logs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove logs beyond the keep limit
        for old_log in rotated_logs[self.keep_rotated:]:
            try:
                old_log.unlink()
                logger.info(f"Removed old rotated log: {old_log.name}")
            except Exception as e:
                logger.error(f"Failed to remove old log {old_log.name}: {e}")
    
    def rotate_all_logs(self) -> dict:
        """Rotate all log files in the directory."""
        results = {}
        
        # Find all log files
        log_files = list(self.log_dir.glob("*.log"))
        
        for log_file in log_files:
            results[log_file.name] = self.rotate_log(log_file.name)
        
        return results

def main():
    """Main entry point for log rotation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Log Rotation System")
    parser.add_argument("--log-dir", default=".", help="Directory containing log files")
    parser.add_argument("--max-size", type=int, default=10, help="Maximum log size in MB")
    parser.add_argument("--keep-rotated", type=int, default=5, help="Number of rotated logs to keep")
    parser.add_argument("--log-file", help="Specific log file to rotate")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create log rotation manager
    manager = LogRotationManager(args.log_dir, args.max_size, args.keep_rotated)
    
    if args.log_file:
        # Rotate specific log file
        result = manager.rotate_log(args.log_file)
        print(f"Log rotation for {args.log_file}: {'SUCCESS' if result else 'NO ROTATION NEEDED'}")
    else:
        # Rotate all log files
        results = manager.rotate_all_logs()
        print("Log rotation results:")
        for log_file, rotated in results.items():
            status = "ROTATED" if rotated else "NO ROTATION NEEDED"
            print(f"  {log_file}: {status}")

if __name__ == "__main__":
    main()
