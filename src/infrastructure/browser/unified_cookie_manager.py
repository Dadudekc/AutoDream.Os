"""
Unified Cookie Manager - SSOT for All Cookie Operations
========================================================

Consolidates 3 cookie manager implementations into a single source of truth:
- browser_backup/cookie_manager.py (BrowserAdapter support)
- browser_backup/thea_cookie_manager.py (stub - deprecated)
- ai_training/dreamvault/scrapers/cookie_manager.py (encryption support)

Features:
- Dual interface support: BrowserAdapter + Selenium WebDriver
- Service-based cookie management (multiple services)
- Optional encryption via Fernet cipher
- Auto-save functionality
- Comprehensive error handling

Author: Agent-6 (Quality Gates & VSCode Specialist) - DUP-003 Consolidation
Date: 2025-10-16
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Optional encryption support
try:
    from cryptography.fernet import Fernet, InvalidToken
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None
    InvalidToken = None


class UnifiedCookieManager:
    """
    Unified cookie manager supporting both BrowserAdapter and WebDriver interfaces.
    
    Consolidates:
    - Service-based cookie management
    - Optional encryption support
    - Auto-save functionality
    - Comprehensive error handling
    """

    def __init__(
        self,
        cookie_file: str = "data/cookies.json",
        auto_save: bool = True,
        enable_encryption: bool = False,
        encryption_key: Optional[str] = None
    ):
        """
        Initialize unified cookie manager.
        
        Args:
            cookie_file: Path to cookie file for persistence
            auto_save: Automatically save cookies after operations
            enable_encryption: Enable cookie encryption (requires cryptography)
            encryption_key: Encryption key (uses env COOKIE_ENCRYPTION_KEY if None)
        """
        self.cookie_file = cookie_file
        self.auto_save = auto_save
        self.cookies: dict[str, list[dict]] = {}
        
        # Setup paths
        self.cookie_path = Path(self.cookie_file)
        self.cookie_path.parent.mkdir(parents=True, exist_ok=True)
        self.encrypted_cookie_path = Path(f"{self.cookie_file}.enc")
        
        # Setup encryption if enabled
        self.enable_encryption = enable_encryption and CRYPTO_AVAILABLE
        if self.enable_encryption:
            self._encryption_key = encryption_key or os.getenv("COOKIE_ENCRYPTION_KEY", "")
            self._fernet = self._init_fernet()
        else:
            self._encryption_key = None
            self._fernet = None
            
        # Load persisted cookies
        self._load_persisted_cookies()

    # =====================================================================
    # BrowserAdapter Interface (browser_backup/cookie_manager.py)
    # =====================================================================

    def save_cookies_for_service(self, browser_adapter: Any, service_name: str) -> bool:
        """
        Save cookies for a specific service using BrowserAdapter.
        
        Args:
            browser_adapter: BrowserAdapter instance with get_cookies() method
            service_name: Service identifier (e.g., 'chatgpt', 'discord')
            
        Returns:
            True if cookies saved successfully, False otherwise
        """
        if not hasattr(browser_adapter, 'is_running') or not browser_adapter.is_running():
            logger.warning(f"Browser adapter not running for {service_name}")
            return False

        try:
            cookies = browser_adapter.get_cookies()
            if cookies:
                self.cookies[service_name] = cookies
                logger.info(f"✅ Saved {len(cookies)} cookies for {service_name}")

            if self.auto_save:
                return self._persist_cookies()

            return True

        except Exception as e:
            logger.error(f"❌ Failed to save cookies for {service_name}: {e}")
            return False

    def load_cookies_for_service(self, browser_adapter: Any, service_name: str) -> bool:
        """
        Load cookies for a specific service using BrowserAdapter.
        
        Args:
            browser_adapter: BrowserAdapter instance with add_cookies() method
            service_name: Service identifier
            
        Returns:
            True if cookies loaded successfully, False otherwise
        """
        if not hasattr(browser_adapter, 'is_running') or not browser_adapter.is_running():
            logger.warning(f"Browser adapter not running for {service_name}")
            return False

        try:
            if service_name in self.cookies:
                browser_adapter.add_cookies(self.cookies[service_name])
                logger.info(f"✅ Loaded cookies for {service_name}")
                return True
            else:
                logger.warning(f"No cookies found for {service_name}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to load cookies for {service_name}: {e}")
            return False

    def has_valid_session(self, service_name: str) -> bool:
        """
        Check if there's a valid session for the service.
        
        Args:
            service_name: Service identifier
            
        Returns:
            True if valid cookies exist for service, False otherwise
        """
        return service_name in self.cookies and len(self.cookies[service_name]) > 0

    # =====================================================================
    # WebDriver Interface (ai_training/dreamvault/scrapers/cookie_manager.py)
    # =====================================================================

    def save_cookies(self, driver: Any) -> bool:
        """
        Save cookies from Selenium WebDriver session.
        
        Args:
            driver: Selenium WebDriver instance with get_cookies() method
            
        Returns:
            True if cookies saved successfully, False otherwise
        """
        try:
            cookies = driver.get_cookies()
            
            # Store under 'default' service for WebDriver interface
            self.cookies['default'] = cookies
            
            if self.auto_save:
                success = self._persist_cookies()
                if success:
                    logger.info(f"✅ Saved {len(cookies)} cookies from WebDriver")
                return success
            
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save cookies from WebDriver: {e}")
            return False

    def load_cookies(self, driver: Any) -> bool:
        """
        Load cookies into Selenium WebDriver session.
        
        Auto-decrypts encrypted cookies if available and key is set.
        
        Args:
            driver: Selenium WebDriver instance with add_cookie() method
            
        Returns:
            True if cookies loaded successfully, False otherwise
        """
        try:
            # Check for encrypted cookies first
            if self.enable_encryption and self.encrypted_cookie_path.exists() and self._fernet:
                cookies = self._load_encrypted_cookies()
                if not cookies and 'default' in self.cookies:
                    cookies = self.cookies['default']
            elif 'default' in self.cookies:
                cookies = self.cookies['default']
            else:
                logger.warning("No cookies found to load")
                return False

            # Add cookies to driver
            loaded_count = 0
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                    loaded_count += 1
                except Exception as e:
                    logger.warning(f"Failed to add cookie: {e}")

            logger.info(f"✅ Loaded {loaded_count} cookies into WebDriver")
            return loaded_count > 0

        except Exception as e:
            logger.error(f"❌ Failed to load cookies into WebDriver: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """
        Check if valid cookies exist (for WebDriver interface).
        
        Returns:
            True if default cookies exist and not empty
        """
        # Check encrypted cookies first
        if self.enable_encryption and self.encrypted_cookie_path.exists():
            cookies = self._load_encrypted_cookies()
            if cookies:
                return True
        
        # Check in-memory cookies
        return 'default' in self.cookies and len(self.cookies['default']) > 0

    # =====================================================================
    # Common Operations
    # =====================================================================

    def clear_cookies(self, service_name: Optional[str] = None) -> bool:
        """
        Clear saved cookies.
        
        Args:
            service_name: Service identifier (None = clear all)
            
        Returns:
            True if cookies cleared successfully, False otherwise
        """
        try:
            if service_name:
                if service_name in self.cookies:
                    del self.cookies[service_name]
                    logger.info(f"✅ Cleared cookies for {service_name}")
            else:
                self.cookies = {}
                if self.cookie_path.exists():
                    self.cookie_path.unlink()
                if self.encrypted_cookie_path.exists():
                    self.encrypted_cookie_path.unlink()
                logger.info("✅ All cookies cleared")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to clear cookies: {e}")
            return False

    # =====================================================================
    # Persistence Operations
    # =====================================================================

    def _persist_cookies(self) -> bool:
        """Persist cookies to file (with optional encryption)."""
        try:
            # Save as JSON
            with open(self.cookie_path, "w", encoding="utf-8") as f:
                json.dump(self.cookies, f, indent=2)
            
            # Encrypt if enabled
            if self.enable_encryption and self._fernet:
                self._encrypt_cookie_file()
                
            return True

        except Exception as e:
            logger.error(f"❌ Failed to persist cookies: {e}")
            return False

    def _load_persisted_cookies(self) -> bool:
        """Load persisted cookies from file."""
        try:
            # Try encrypted cookies first
            if self.enable_encryption and self.encrypted_cookie_path.exists() and self._fernet:
                cookies = self._load_encrypted_cookies()
                if cookies:
                    self.cookies['default'] = cookies
                    return True
            
            # Fall back to plaintext
            if self.cookie_path.exists():
                with open(self.cookie_path, encoding="utf-8") as f:
                    self.cookies = json.load(f)
                return True
                
            return False

        except Exception as e:
            logger.error(f"❌ Failed to load persisted cookies: {e}")
            return False

    # =====================================================================
    # Encryption Operations (Optional)
    # =====================================================================

    def _init_fernet(self) -> Optional[Any]:
        """Initialize Fernet cipher for encryption/decryption."""
        if not CRYPTO_AVAILABLE or not self._encryption_key:
            return None

        try:
            return Fernet(self._encryption_key.encode())
        except Exception as e:
            logger.warning(f"Failed to initialize encryption: {e}")
            return None

    def _encrypt_cookie_file(self) -> bool:
        """Encrypt the plaintext cookie file."""
        if not self._fernet or not self.cookie_path.exists():
            return False

        try:
            with open(self.cookie_path, "rb") as f:
                data = f.read()

            encrypted_data = self._fernet.encrypt(data)
            
            with open(self.encrypted_cookie_path, "wb") as f:
                f.write(encrypted_data)

            # Remove plaintext file
            self.cookie_path.unlink()
            logger.info(f"✅ Encrypted cookies saved to {self.encrypted_cookie_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to encrypt cookie file: {e}")
            return False

    def _load_encrypted_cookies(self) -> Optional[list[dict]]:
        """Load and decrypt encrypted cookies."""
        if not self._fernet or not self.encrypted_cookie_path.exists():
            return None

        try:
            with open(self.encrypted_cookie_path, "rb") as f:
                encrypted_data = f.read()

            data = self._fernet.decrypt(encrypted_data)
            cookies_data = json.loads(data.decode("utf-8"))
            
            # Handle both dict (service-based) and list (WebDriver) formats
            if isinstance(cookies_data, dict):
                return cookies_data.get('default', [])
            elif isinstance(cookies_data, list):
                return cookies_data
            
            return None

        except (InvalidToken, Exception) as e:
            logger.warning(f"Failed to load encrypted cookies: {e}")
            return None

    @staticmethod
    def generate_encryption_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64-encoded encryption key string
            
        Raises:
            ImportError: If cryptography library not available
        """
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library not available")

        return Fernet.generate_key().decode("utf-8")

