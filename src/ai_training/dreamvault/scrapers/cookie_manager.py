"""
Cookie Manager for DreamVault ChatGPT Scraper

Handles cookie persistence and session management for ChatGPT login.
Supports optional encryption for secure storage of cookies.
"""

import logging
import json
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
from selenium.webdriver.remote.webdriver import WebDriver

try:
    from cryptography.fernet import Fernet, InvalidToken
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None
    InvalidToken = None

logger = logging.getLogger(__name__)

class CookieManager:
    """Manages cookie persistence and session management."""
    
    def __init__(self, cookie_file: Optional[str] = None):
        """
        Initialize the cookie manager.
        
        Args:
            cookie_file: Path to cookie file for persistence
        """
        self.cookie_file = cookie_file or "data/cookies.json"
        self.cookie_path = Path(self.cookie_file)
        self.cookie_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Encrypted cookie file path
        self.encrypted_cookie_path = Path(f"{self.cookie_file}.enc")
        
        # Get encryption key from environment
        self.encryption_key = os.getenv("COOKIE_ENCRYPTION_KEY", "")
        self._fernet = self._init_fernet()
    
    def save_cookies(self, driver: WebDriver) -> bool:
        """
        Save cookies from the current driver session.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if cookies saved successfully, False otherwise
        """
        try:
            cookies = driver.get_cookies()
            
            with open(self.cookie_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, indent=2)
            
            logger.info(f"✅ Saved {len(cookies)} cookies to {self.cookie_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return False
    
    def load_cookies(self, driver: WebDriver) -> bool:
        """
        Load cookies into the current driver session.
        
        Auto-decrypts encrypted cookies if available and key is set.
        
        Args:
            driver: Selenium webdriver instance
            
        Returns:
            True if cookies loaded successfully, False otherwise
        """
        try:
            # Prefer encrypted cookies if available and we have a key
            if self.encrypted_cookie_path.exists() and self._fernet:
                try:
                    with open(self.encrypted_cookie_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    # Decrypt
                    data = self._decrypt_data(encrypted_data)
                    if data:
                        cookies = json.loads(data.decode('utf-8'))
                        logger.info(f"✅ Loaded encrypted cookies")
                    else:
                        # Decryption failed, fall back to plaintext
                        logger.warning("Decryption failed, falling back to plaintext cookies")
                        if not self.cookie_path.exists():
                            return False
                        with open(self.cookie_path, 'r', encoding='utf-8') as f:
                            cookies = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load encrypted cookies: {e}, falling back to plaintext")
                    if not self.cookie_path.exists():
                        return False
                    with open(self.cookie_path, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
            else:
                # No encrypted cookies or no key, use plaintext
                if not self.cookie_path.exists():
                    logger.warning(f"Cookie file not found: {self.cookie_file}")
                    return False
                
                with open(self.cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
            
            # Add cookies to driver
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    logger.warning(f"Failed to add cookie: {e}")
            
            logger.info(f"✅ Loaded {len(cookies)} cookies")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return False
    
    def has_valid_cookies(self) -> bool:
        """
        Check if valid cookies exist (plaintext or encrypted).
        
        Returns:
            True if cookie file exists and is not empty
        """
        # Check encrypted cookies first
        if self.encrypted_cookie_path.exists() and self._fernet:
            try:
                with open(self.encrypted_cookie_path, 'rb') as f:
                    encrypted_data = f.read()
                data = self._decrypt_data(encrypted_data)
                if data:
                    cookies = json.loads(data.decode('utf-8'))
                    return len(cookies) > 0
            except Exception:
                pass
        
        # Check plaintext cookies
        if not self.cookie_path.exists():
            return False
        
        try:
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            return len(cookies) > 0
        except Exception:
            return False
    
    def clear_cookies(self) -> bool:
        """
        Clear saved cookies.
        
        Returns:
            True if cookies cleared successfully, False otherwise
        """
        try:
            if self.cookie_path.exists():
                self.cookie_path.unlink()
            if self.encrypted_cookie_path.exists():
                self.encrypted_cookie_path.unlink()
            logger.info("✅ Cookies cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear cookies: {e}")
            return False
    
    def _init_fernet(self) -> Optional[Any]:
        """
        Initialize Fernet cipher for encryption/decryption.
        
        Returns:
            Fernet instance if key is available and valid, None otherwise
        """
        if not CRYPTO_AVAILABLE:
            return None
        
        if not self.encryption_key:
            return None
        
        try:
            return Fernet(self.encryption_key.encode())
        except Exception as e:
            logger.warning(f"Failed to initialize encryption: {e}")
            return None
    
    def _encrypt_data(self, data: bytes) -> Optional[bytes]:
        """
        Encrypt data using Fernet.
        
        Args:
            data: Raw bytes to encrypt
            
        Returns:
            Encrypted bytes or None if encryption fails
        """
        if not self._fernet:
            return None
        
        try:
            return self._fernet.encrypt(data)
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return None
    
    def _decrypt_data(self, encrypted_data: bytes) -> Optional[bytes]:
        """
        Decrypt data using Fernet.
        
        Args:
            encrypted_data: Encrypted bytes to decrypt
            
        Returns:
            Decrypted bytes or None if decryption fails
        """
        if not self._fernet:
            return None
        
        try:
            return self._fernet.decrypt(encrypted_data)
        except (InvalidToken, Exception) as e:
            logger.error(f"Decryption failed: {e}")
            return None
    
    def encrypt_cookie_file(self) -> bool:
        """
        Encrypt the plaintext cookie file.
        
        Reads data/cookies.json, encrypts it, and saves to data/cookies.json.enc.
        Removes the plaintext file after successful encryption.
        
        Returns:
            True if encryption successful, False otherwise
        """
        if not self._fernet:
            logger.warning("Encryption not available (no key or cryptography library missing)")
            return False
        
        if not self.cookie_path.exists():
            logger.warning(f"Cookie file not found: {self.cookie_file}")
            return False
        
        try:
            # Read plaintext cookies
            with open(self.cookie_path, 'rb') as f:
                data = f.read()
            
            # Encrypt
            encrypted_data = self._encrypt_data(data)
            if not encrypted_data:
                return False
            
            # Save encrypted cookies
            with open(self.encrypted_cookie_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove plaintext file
            self.cookie_path.unlink()
            
            logger.info(f"✅ Encrypted cookies saved to {self.encrypted_cookie_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to encrypt cookie file: {e}")
            return False
    
    def decrypt_cookie_file(self) -> bool:
        """
        Decrypt the encrypted cookie file.
        
        Reads data/cookies.json.enc, decrypts it, and saves to data/cookies.json.
        
        Returns:
            True if decryption successful, False otherwise
        """
        if not self._fernet:
            logger.warning("Decryption not available (no key or cryptography library missing)")
            return False
        
        if not self.encrypted_cookie_path.exists():
            logger.warning(f"Encrypted cookie file not found: {self.encrypted_cookie_path}")
            return False
        
        try:
            # Read encrypted cookies
            with open(self.encrypted_cookie_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            data = self._decrypt_data(encrypted_data)
            if not data:
                return False
            
            # Save plaintext cookies
            with open(self.cookie_path, 'wb') as f:
                f.write(data)
            
            logger.info(f"✅ Decrypted cookies saved to {self.cookie_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to decrypt cookie file: {e}")
            return False
    
    @staticmethod
    def generate_encryption_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64-encoded encryption key string
        """
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library not available")
        
        return Fernet.generate_key().decode('utf-8') 