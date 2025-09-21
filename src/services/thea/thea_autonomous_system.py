#!/usr/bin/env python3
"""
Thea Autonomous System - Fully Agent-Friendly Thea Communication
================================================================

A completely autonomous Thea communication system that requires no human intervention.
Designed for 24/7 agent operation with robust error handling and recovery.

Features:
- Fully automated browser management
- Autonomous cookie and session handling
- Automatic message sending and response detection
- Robust error recovery and retry mechanisms
- Comprehensive logging and monitoring
- No human interaction required

Usage:
    from src.services.thea.thea_autonomous_system import TheaAutonomousSystem
    
    thea = TheaAutonomousSystem()
    response = thea.send_message_autonomous("Hello Thea!")
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from .thea_browser_manager import TheaBrowserManager
from .thea_cookie_manager import TheaCookieManager
from .thea_communication_core import TheaCommunicationCore

logger = logging.getLogger(__name__)


class TheaAutonomousSystem:
    """Fully autonomous Thea communication system for agent use."""
    
    def __init__(self, 
                 headless: bool = True,
                 cookie_file: str = "thea_cookies.json",
                 responses_dir: str = "thea_responses",
                 max_retries: int = 3,
                 retry_delay: int = 5):
        """
        Initialize the autonomous Thea system.
        
        Args:
            headless: Run browser in headless mode (recommended for agents)
            cookie_file: Path to cookie persistence file
            responses_dir: Directory for storing responses and logs
            max_retries: Maximum retry attempts for failed operations
            retry_delay: Delay between retry attempts (seconds)
        """
        self.headless = headless
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize components
        self.browser_manager = TheaBrowserManager(headless=headless)
        self.cookie_manager = TheaCookieManager(cookie_file)
        self.communication_core = TheaCommunicationCore(responses_dir)
        
        # System state
        self.driver = None
        self.is_initialized = False
        self.last_activity = None
        
        # Logging setup
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup comprehensive logging for autonomous operation."""
        log_dir = Path("logs/thea_autonomous")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"thea_autonomous_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        logger.info("🤖 Thea Autonomous System initialized")
        
    def initialize(self) -> bool:
        """
        Initialize the autonomous system.
        
        Returns:
            True if initialization successful, False otherwise
        """
        logger.info("🚀 Initializing Thea Autonomous System...")
        
        for attempt in range(self.max_retries):
            try:
                # Initialize browser
                self.driver = self.browser_manager.initialize_driver()
                if not self.driver:
                    raise Exception("Failed to initialize browser driver")
                
                # Navigate to Thea first
                thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
                logger.info(f"🌐 Navigating to Thea: {thea_url}")
                self.driver.get(thea_url)
                time.sleep(3)
                
                # Load cookies after navigation (when domain is correct)
                if self.cookie_manager.has_valid_cookies():
                    logger.info("🍪 Loading existing cookies after navigation...")
                    self.cookie_manager.load_cookies(self.driver)
                else:
                    logger.info("🍪 No valid cookies found - will need fresh session")
                
                # Save cookies after navigation
                self.cookie_manager.save_cookies(self.driver)
                
                self.is_initialized = True
                self.last_activity = datetime.now()
                logger.info("✅ Thea Autonomous System initialized successfully")
                return True
                
            except Exception as e:
                logger.error(f"❌ Initialization attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"⏳ Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("❌ All initialization attempts failed")
                    return False
        
        return False
    
    def send_message_autonomous(self, message: str, timeout: int = 120) -> Optional[str]:
        """
        Send a message to Thea and get response autonomously.
        
        Args:
            message: Message to send to Thea
            timeout: Maximum time to wait for response (seconds)
            
        Returns:
            Thea's response text, or None if failed
        """
        if not self.is_initialized:
            logger.error("❌ System not initialized - call initialize() first")
            return None
        
        logger.info(f"📤 Sending autonomous message to Thea: {len(message)} characters")
        
        for attempt in range(self.max_retries):
            try:
                # Prepare message
                message_path = self.communication_core.prepare_message(message)
                
                # Send message via Selenium
                success = self.communication_core.send_message_selenium(self.driver, message)
                if not success:
                    raise Exception("Failed to send message via Selenium")
                
                # Wait for response
                response_received = self.communication_core.wait_for_response(self.driver, timeout)
                if not response_received:
                    raise Exception("Failed to receive response from Thea")
                
                # Extract response text
                response_text = self.communication_core.extract_response_text(self.driver)
                
                # Capture screenshot
                screenshot_path = self.communication_core.capture_screenshot()
                
                # Save metadata
                if screenshot_path:
                    self.communication_core.save_metadata(
                        screenshot_path, message_path, response_text
                    )
                
                # Create conversation log
                self.communication_core.create_conversation_log(
                    message, message_path, screenshot_path, response_text
                )
                
                # Update activity timestamp
                self.last_activity = datetime.now()
                
                # Save cookies after successful interaction
                self.cookie_manager.save_cookies(self.driver)
                
                logger.info(f"✅ Autonomous message exchange completed successfully")
                return response_text
                
            except Exception as e:
                logger.error(f"❌ Message attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"⏳ Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    
                    # Try to recover by reinitializing
                    if not self._recover_session():
                        logger.error("❌ Session recovery failed")
                        return None
                else:
                    logger.error("❌ All message attempts failed")
                    return None
        
        return None
    
    def _recover_session(self) -> bool:
        """
        Attempt to recover from a failed session.
        
        Returns:
            True if recovery successful, False otherwise
        """
        logger.info("🔄 Attempting session recovery...")
        
        try:
            # Clean up current driver
            if self.driver:
                self.browser_manager.cleanup_driver(self.driver)
                self.driver = None
            
            # Reinitialize
            return self.initialize()
            
        except Exception as e:
            logger.error(f"❌ Session recovery failed: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status.
        
        Returns:
            Dictionary containing system status information
        """
        return {
            "initialized": self.is_initialized,
            "headless_mode": self.headless,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "has_valid_cookies": self.cookie_manager.has_valid_cookies(),
            "browser_available": self.browser_manager.is_selenium_available(),
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        }
    
    def cleanup(self):
        """Clean up system resources."""
        logger.info("🧹 Cleaning up Thea Autonomous System...")
        
        try:
            if self.driver:
                self.browser_manager.cleanup_driver(self.driver)
                self.driver = None
            
            self.is_initialized = False
            logger.info("✅ Cleanup completed")
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        if not self.initialize():
            raise Exception("Failed to initialize Thea Autonomous System")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


# Convenience functions for easy integration
def create_autonomous_thea(headless: bool = True, **kwargs) -> TheaAutonomousSystem:
    """
    Create an autonomous Thea system with default settings.
    
    Args:
        headless: Run in headless mode (recommended for agents)
        **kwargs: Additional configuration options
        
    Returns:
        TheaAutonomousSystem instance
    """
    return TheaAutonomousSystem(headless=headless, **kwargs)


def send_thea_message_autonomous(message: str, headless: bool = True) -> Optional[str]:
    """
    Send a message to Thea autonomously (convenience function).
    
    Args:
        message: Message to send to Thea
        headless: Run in headless mode
        
    Returns:
        Thea's response text, or None if failed
    """
    with create_autonomous_thea(headless=headless) as thea:
        return thea.send_message_autonomous(message)


if __name__ == "__main__":
    # Example usage
    print("🤖 V2_SWARM Thea Autonomous System")
    print("=" * 50)
    
    # Test autonomous operation
    test_message = "Hello Thea! This is an autonomous test message from Agent-2."
    
    print(f"📤 Sending test message: {test_message}")
    response = send_thea_message_autonomous(test_message, headless=True)
    
    if response:
        print(f"✅ Received response: {len(response)} characters")
        print(f"📝 Response preview: {response[:200]}...")
    else:
        print("❌ Failed to get response from Thea")
