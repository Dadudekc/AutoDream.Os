#!/usr/bin/env python3
"""
Logging Configuration
=====================

Centralized logging configuration for Discord bot.
"""

import logging
import logging.handlers
import os
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import TextIO


class TerminalLogHandler(logging.StreamHandler):
    """Custom handler to capture terminal output and log it to Discord logs."""
    
    def __init__(self, target_logger_name: str):
        super().__init__()
        self.target_logger_name = target_logger_name
        self.buffer = io.StringIO()
        
    def emit(self, record):
        """Emit a log record to the target logger."""
        try:
            # Format the message
            msg = self.format(record)
            
            # Get the target logger and log the message
            target_logger = logging.getLogger(self.target_logger_name)
            target_logger.info(f"[TERMINAL] {msg}")
            
        except Exception:
            self.handleError(record)


class TeeOutput:
    """Tee output to both original stream and Discord logs."""
    
    def __init__(self, original_stream: TextIO, target_logger_name: str):
        self.original_stream = original_stream
        self.target_logger = logging.getLogger(target_logger_name)
        self.buffer = io.StringIO()
        
    def write(self, text: str):
        """Write to both original stream and Discord logs."""
        # Write to original stream
        self.original_stream.write(text)
        self.original_stream.flush()
        
        # Log to Discord logs (strip newlines for cleaner logging)
        if text.strip():
            try:
                # Clean text to avoid encoding issues - replace Unicode with safe alternatives
                clean_text = text.strip()
                # Replace common problematic Unicode characters
                replacements = {
                    '🚨': '[ALERT]',
                    '📢': '[NOTIFY]', 
                    '❌': '[ERROR]',
                    '✅': '[SUCCESS]',
                    '⚠️': '[WARNING]',
                    '🎓': '[ONBOARD]',
                    '🔄': '[RESTART]',
                    '⏹️': '[SHUTDOWN]',
                    '👥': '[AGENTS]',
                    '📝': '[DEVLOG]',
                    '📊': '[STATUS]'
                }
                for unicode_char, replacement in replacements.items():
                    clean_text = clean_text.replace(unicode_char, replacement)
                
                # Final safety: encode to ASCII with replacement
                clean_text = clean_text.encode('ascii', 'replace').decode('ascii')
                self.target_logger.info(f"[STDOUT] {clean_text}")
            except Exception:
                # If logging fails, just continue without crashing
                pass
    
    def flush(self):
        """Flush the original stream."""
        self.original_stream.flush()
    
    def __getattr__(self, name):
        """Delegate other attributes to original stream."""
        return getattr(self.original_stream, name)


def setup_discord_logging():
    """Setup comprehensive logging for Discord bot."""
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    # Set encoding to UTF-8 to handle Unicode characters
    if hasattr(console_handler.stream, 'reconfigure'):
        console_handler.stream.reconfigure(encoding='utf-8')
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "discord_bot.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Command-specific log file
    command_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "discord_commands.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding="utf-8"
    )
    command_handler.setLevel(logging.INFO)
    command_handler.setFormatter(detailed_formatter)
    
    # Add command handler to command logger
    command_logger = logging.getLogger('src.services.discord_bot.core.command_logger')
    command_logger.addHandler(command_handler)
    command_logger.setLevel(logging.INFO)
    
    # Error-specific log file
    error_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "discord_errors.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Discord library logger
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.WARNING)
    
    # Suppress some noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    
    # Setup terminal output capture
    setup_terminal_output_capture()
    
    # Log startup
    logger = logging.getLogger(__name__)
    logger.info("Discord bot logging system initialized")
    logger.info(f"Log files: {logs_dir.absolute()}")
    
    return logger


def setup_terminal_output_capture():
    """Setup terminal output capture to Discord logs."""
    try:
        # Create a logger for terminal output
        terminal_logger = logging.getLogger('src.services.discord_bot.terminal')
        terminal_logger.setLevel(logging.INFO)
        
        # Add handler to main Discord bot log
        terminal_handler = logging.handlers.RotatingFileHandler(
            Path("logs") / "discord_bot.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        terminal_handler.setLevel(logging.INFO)
        terminal_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        terminal_logger.addHandler(terminal_handler)
        
        # Tee stdout to Discord logs
        original_stdout = sys.stdout
        sys.stdout = TeeOutput(original_stdout, 'src.services.discord_bot.terminal')
        
        # Tee stderr to Discord logs
        original_stderr = sys.stderr
        sys.stderr = TeeOutput(original_stderr, 'src.services.discord_bot.terminal')
        
        # Log that terminal capture is active
        terminal_logger.info("Terminal output capture activated - stdout/stderr will be logged to Discord logs")
        
    except Exception as e:
        # If terminal capture fails, log the error but don't crash
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to setup terminal output capture: {e}")


def disable_terminal_output_capture():
    """Disable terminal output capture (restore original streams)."""
    try:
        # Restore original streams if they were replaced
        if hasattr(sys.stdout, 'original_stream'):
            sys.stdout = sys.stdout.original_stream
        if hasattr(sys.stderr, 'original_stream'):
            sys.stderr = sys.stderr.original_stream
            
        logger = logging.getLogger('src.services.discord_bot.terminal')
        logger.info("Terminal output capture disabled")
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to disable terminal output capture: {e}")


def get_command_logger():
    """Get the command-specific logger."""
    return logging.getLogger('src.services.discord_bot.core.command_logger')


def log_command_execution(command_name: str, user_name: str, success: bool, execution_time: float, error_msg: str = None):
    """Log command execution to command log file."""
    logger = get_command_logger()
    
    status = "SUCCESS" if success else "FAILED"
    log_msg = f"COMMAND: {command_name} | USER: {user_name} | STATUS: {status} | TIME: {execution_time:.2f}s"
    
    if error_msg:
        log_msg += f" | ERROR: {error_msg}"
    
    if success:
        logger.info(log_msg)
    else:
        logger.error(log_msg)


def log_security_event(event_type: str, user_id: int, details: str):
    """Log security events."""
    logger = logging.getLogger('src.services.discord_bot.core.security_manager')
    logger.warning(f"SECURITY: {event_type} | USER: {user_id} | DETAILS: {details}")


def log_performance_metric(metric_name: str, value: float, unit: str = ""):
    """Log performance metrics."""
    logger = logging.getLogger('src.services.discord_bot.core.performance')
    logger.info(f"PERFORMANCE: {metric_name} = {value} {unit}")


if __name__ == "__main__":
    # Test logging setup
    setup_discord_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("[SUCCESS] Logging system test successful")
    
    # Test command logging
    log_command_execution("test", "TestUser", True, 0.5)
    log_command_execution("test", "TestUser", False, 1.2, "Test error")
    
    print("🔧 Logging system initialized successfully!")
