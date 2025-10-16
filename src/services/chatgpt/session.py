"""
ChatGPT Session Manager - V2 Compliant
=====================================

Session management for ChatGPT browser automation.
Handles authentication, cookie management, and context persistence.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Browser Automation Specialist
Mission: DUP-002 SessionManager Consolidation - Refactored to use BaseSessionManager
License: MIT
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Optional dependencies
try:
    from playwright.async_api import BrowserContext, Cookie
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not available - ChatGPT session management disabled")

# V2 Integration imports
try:
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
    from ...core.session.base_session_manager import BaseSessionManager, BaseSessionInfo
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)
    
    # Fallback for BaseSessionManager if import fails
    class BaseSessionManager:
        def __init__(self, config=None, logger_name=None):
            self.config = config or {}
            self.logger = logging.getLogger(logger_name or __name__)
            self.sessions = {}
            
        def session_exists(self, session_id): return False
        def update_session_activity(self, session_id): return False
        def _generate_session_id(self, service_name): return f"{service_name}_{int(time.time())}"


class BrowserSessionManager(BaseSessionManager):
    """
    Browser session management for ChatGPT.
    
    Provides session persistence, cookie management, and authentication
    handling for ChatGPT browser automation.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize browser session manager.
        
        Args:
            config: Configuration dictionary (uses config/chatgpt.yml if None)
        """
        # Initialize base session manager
        super().__init__(config=config, logger_name=__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Session settings (from config or defaults)
        session_config = self.config.get('session', {})
        self.cookie_storage = session_config.get('cookie_storage', 'runtime/browser_profiles/chatgpt/cookies')
        self.cache_enabled = session_config.get('cache_enabled', True)
        self.cache_size = session_config.get('cache_size', 100)
        
        # Override persistent from base if specified in session config
        if 'persistent' in session_config:
            self.persistent = session_config['persistent']
        else:
            self.persistent = True  # Default for browser sessions
        
        # Authentication settings
        auth_config = self.config.get('authentication', {})
        self.auto_login = auth_config.get('auto_login', False)
        self.session_validation_enabled = auth_config.get('session_validation', True)
        self.reauth_on_failure = auth_config.get('reauth_on_failure', True)
        
        # Browser-specific state
        self.session_data = {}
        self.cookie_cache = {}
        self.session_valid = False
        self.last_validation = 0
        
        # Storage paths
        self.session_dir = Path(self.cookie_storage)
        if self.persistent:
            self.session_dir.mkdir(parents=True, exist_ok=True)
        
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("Session management disabled - Playwright not available")

    async def create_session_context(self, browser_context: Optional[BrowserContext] = None) -> Optional[BrowserContext]:
        """
        Create or configure browser context with session data.
        
        Args:
            browser_context: Existing context to configure (creates new if None)
            
        Returns:
            Configured browser context
        """
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("Cannot create session context - Playwright not available")
            return None
        
        try:
            # Load session data
            if self.persistent:
                await self._load_session_data()
            
            # Configure context with session data
            context_options = {
                'viewport': {'width': 1280, 'height': 720},
                'user_agent': self.config.get('browser', {}).get('user_agent')
            }
            
            # Add cookies if available
            if self.cookie_cache:
                context_options['storage_state'] = {
                    'cookies': list(self.cookie_cache.values()),
                    'origins': []
                }
            
            if browser_context:
                # Configure existing context
                await browser_context.add_cookies(list(self.cookie_cache.values()))
            else:
                # Create new context (this would be done by the navigator)
                pass
            
            self.logger.info("Session context configured")
            return browser_context
            
        except Exception as e:
            self.logger.error(f"Failed to create session context: {e}")
            return None

    async def save_session(self, context: BrowserContext) -> bool:
        """
        Save session data from browser context.
        
        Args:
            context: Browser context to save session from
            
        Returns:
            True if successful, False otherwise
        """
        if not PLAYWRIGHT_AVAILABLE:
            return False
        
        try:
            # Get cookies from context
            cookies = await context.cookies()
            
            # Store cookies in cache
            for cookie in cookies:
                self.cookie_cache[cookie['name']] = cookie
            
            # Save to disk if persistent
            if self.persistent:
                await self._save_session_data()
            
            self.logger.info(f"Session saved with {len(cookies)} cookies")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            return False

    async def load_session(self) -> bool:
        """
        Load session data from storage.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.persistent:
                await self._load_session_data()
                self.logger.info(f"Session loaded with {len(self.cookie_cache)} cookies")
                return True
            else:
                self.logger.info("Session persistence disabled")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to load session: {e}")
            return False

    async def validate_session(self, context: BrowserContext) -> bool:
        """
        Validate current session by checking authentication.
        
        Args:
            context: Browser context to validate
            
        Returns:
            True if session is valid, False otherwise
        """
        if not self.session_validation:
            return True
        
        try:
            # Create a page to test session
            page = await context.new_page()
            
            # Navigate to ChatGPT and check for authentication
            await page.goto('https://chat.openai.com/', timeout=30000)
            
            # Check if we're authenticated (look for sign-in button or user menu)
            sign_in_button = await page.query_selector('a[href*="auth"]')
            
            if sign_in_button:
                # Not authenticated
                self.session_valid = False
                self.logger.warning("Session validation failed - not authenticated")
            else:
                # Authenticated
                self.session_valid = True
                self.logger.info("Session validation successful")
            
            await page.close()
            self.last_validation = time.time()
            
            return self.session_valid
            
        except Exception as e:
            self.logger.error(f"Session validation failed: {e}")
            self.session_valid = False
            return False

    async def _load_session_data(self) -> None:
        """Load session data from disk."""
        try:
            cookie_file = self.session_dir / 'cookies.json'
            
            if cookie_file.exists():
                with open(cookie_file, 'r') as f:
                    cookie_data = json.load(f)
                
                self.cookie_cache = cookie_data.get('cookies', {})
                self.session_data = cookie_data.get('session_data', {})
                
                self.logger.info(f"Loaded session data from {cookie_file}")
            else:
                self.logger.info("No existing session data found")
                
        except Exception as e:
            self.logger.error(f"Failed to load session data: {e}")

    async def _save_session_data(self) -> None:
        """Save session data to disk."""
        try:
            cookie_file = self.session_dir / 'cookies.json'
            
            session_data = {
                'cookies': self.cookie_cache,
                'session_data': self.session_data,
                'timestamp': time.time(),
                'version': '2.0.0'
            }
            
            with open(cookie_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.logger.info(f"Session data saved to {cookie_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save session data: {e}")

    def clear_session(self) -> bool:
        """
        Clear all session data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cookie_cache.clear()
            self.session_data.clear()
            self.session_valid = False
            
            # Remove session files
            if self.persistent and self.session_dir.exists():
                cookie_file = self.session_dir / 'cookies.json'
                if cookie_file.exists():
                    cookie_file.unlink()
            
            self.logger.info("Session data cleared")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear session: {e}")
            return False

    def get_session_info(self) -> Dict[str, Any]:
        """Get information about current session."""
        return {
            "playwright_available": PLAYWRIGHT_AVAILABLE,
            "persistent": self.persistent,
            "cookie_storage": self.cookie_storage,
            "cache_enabled": self.cache_enabled,
            "cache_size": self.cache_size,
            "auto_login": self.auto_login,
            "session_validation": self.session_validation,
            "reauth_on_failure": self.reauth_on_failure,
            "session_valid": self.session_valid,
            "last_validation": self.last_validation,
            "cookies_count": len(self.cookie_cache),
            "session_data_keys": list(self.session_data.keys()),
        }

    def is_session_valid(self) -> bool:
        """Check if current session is valid."""
        if not self.session_validation_enabled:
            return True
        
        # Check if validation is recent (within 5 minutes)
        if time.time() - self.last_validation > 300:
            self.logger.warning("Session validation is stale")
            return False
        
        return self.session_valid

    def create_session(self, service_name: str = "chatgpt", **kwargs) -> Optional[str]:
        """
        Create a new browser session.
        
        Implementation of BaseSessionManager abstract method.
        For browser sessions, this creates a session ID but the actual
        browser context is created via create_session_context().
        
        Args:
            service_name: Service name (default: "chatgpt")
            **kwargs: Additional session parameters
            
        Returns:
            Session ID if successful, None otherwise
        """
        try:
            session_id = self._generate_session_id(service_name)
            
            # Create base session info (browser context will be added later)
            session_info = BaseSessionInfo(
                session_id=session_id,
                service_name=service_name,
                status="active"
            )
            
            self.sessions[session_id] = session_info
            self.logger.info(f"✅ Created browser session {session_id}")
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create browser session: {e}")
            return None

    def validate_session(self, session_id: str) -> bool:
        """
        Validate that a browser session exists and is active.
        
        Implementation of BaseSessionManager abstract method.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not self.session_exists(session_id):
            return False
        
        session = self.sessions[session_id]
        
        # Check if session is active
        if session.status != "active":
            return False
        
        # Check timeout
        if time.time() - session.last_activity > self.session_timeout:
            self.logger.warning(f"Browser session {session_id} expired")
            return False
        
        return True
