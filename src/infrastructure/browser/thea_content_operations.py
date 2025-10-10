#!/usr/bin/env python3
"""
Thea Content Operations - V2 Compliance
=======================================

Unified content scraping and response collection for Thea automation.
Consolidates: thea_modules/browser_ops, content_scraper, response_collector, profile

Author: Agent-3 (Infrastructure & DevOps) - Browser Consolidation
License: MIT
"""

import re
import time
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ScrapedContent:
    """Represents scraped content from Thea Manager."""
    content: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 0.0
    processing_time: float = 0.0


class TheaContentOperations:
    """Unified content operations for Thea Manager automation."""

    def __init__(self, driver: Any = None):
        """Initialize content operations."""
        self.driver = driver
        self._response_cache = {}
        self._last_cursor_position = None

    # ========== Response Collection ==========
    
    def collect_response(self, timeout: float = 120.0) -> Optional[str]:
        """Collect full response with DOM polling and cursor detection."""
        if not self.driver:
            logger.error("No driver available for response collection")
            return None

        logger.info("🚀 Starting response collection...")
        start_time = time.time()
        last_length = 0
        stable_count = 0
        
        try:
            while time.time() - start_time < timeout:
                current = self._extract_response_text()
                
                if current:
                    current_len = len(current)
                    if current_len > last_length:
                        last_length = current_len
                        stable_count = 0
                    elif current_len == last_length:
                        stable_count += 1
                        if stable_count >= 3:  # Stable for 3 checks
                            logger.info("✅ Response complete")
                            return current
                
                if self._is_response_complete():
                    return self._extract_response_text()
                
                time.sleep(0.5)
            
            logger.warning(f"⏰ Timeout after {timeout}s")
            return self._extract_response_text()
            
        except Exception as e:
            logger.error(f"❌ Response collection error: {e}")
            return None

    def _extract_response_text(self) -> Optional[str]:
        """Extract current response text from page using proven selectors."""
        if not self.driver:
            return None
        
        from selenium.webdriver.common.by import By
        
        try:
            # Proven working selectors (from thea_automation.py)
            selectors = [
                "[data-message-author-role='assistant']:last-of-type .markdown",
                "[data-testid='conversation-turn']:last-child .markdown",
                ".agent-turn:last-child",
                "article:last-of-type",
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element and element.text.strip():
                        return element.text.strip()
                except:
                    continue
            
            # Fallback: Get all article elements and return last one
            try:
                articles = self.driver.find_elements(By.TAG_NAME, "article")
                if articles and len(articles) > 1:
                    return articles[-1].text.strip()
            except:
                pass
            
            return None
            
        except Exception as e:
            logger.debug(f"Response extraction failed: {e}")
            return None

    def _is_response_complete(self) -> bool:
        """Check if response is complete using indicators."""
        if not self.driver:
            return False
            
        try:
            # Check for completion indicators
            script = """
            return !document.querySelector('.generating-indicator') &&
                   !document.querySelector('.cursor-blink');
            """
            return self.driver.execute_script(script)
        except:
            return False

    # ========== Content Scraping ==========
    
    def scrape_content(self, raw_content: str) -> ScrapedContent:
        """Scrape and process content."""
        start_time = time.time()
        
        try:
            cleaned = self._clean_content(raw_content)
            metadata = self._extract_metadata(cleaned)
            quality = self._calculate_quality(cleaned)
            
            return ScrapedContent(
                content=cleaned,
                timestamp=str(int(time.time())),
                metadata=metadata,
                quality_score=quality,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Content scraping failed: {e}")
            return ScrapedContent(
                content=raw_content,
                timestamp=str(int(time.time())),
                metadata={'error': str(e)},
                quality_score=0.0,
                processing_time=time.time() - start_time
            )

    def _clean_content(self, content: str) -> str:
        """Clean and normalize content."""
        if not content:
            return ""
        
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        # Remove HTML tags
        content = re.sub(r'<.*?>', '', content)
        # Remove URLs
        content = re.sub(r'http[s]?://\S+', '', content)
        
        return content

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from content."""
        return {
            'length': len(content),
            'word_count': len(content.split()),
            'line_count': len(content.splitlines())
        }

    def _calculate_quality(self, content: str) -> float:
        """Calculate content quality score."""
        if not content:
            return 0.0
        
        score = 0.0
        
        # Length factor
        if len(content) > 100:
            score += 0.3
        if len(content) > 500:
            score += 0.2
        
        # Structure factor
        if '\n' in content:
            score += 0.2
        
        # Completeness factor
        if content.strip().endswith(('.', '!', '?')):
            score += 0.3
        
        return min(score, 1.0)

    # ========== Browser Operations ==========
    
    def send_message(self, message: str, use_clipboard: bool = True) -> bool:
        """Send message to Thea Manager (uses PyAutoGUI clipboard method - proven reliable)."""
        if not self.driver:
            return False
        
        try:
            # Method 1: PyAutoGUI clipboard paste (WORKING - from simple_thea_communication.py)
            if use_clipboard:
                try:
                    import pyperclip
                    import pyautogui
                    
                    logger.info(f"📤 Sending message via clipboard: {message[:50]}...")
                    pyperclip.copy(message)
                    time.sleep(0.5)
                    
                    # Paste and send
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(0.5)
                    pyautogui.press("enter")
                    
                    logger.info("✅ Message sent via clipboard")
                    return True
                    
                except ImportError:
                    logger.warning("PyAutoGUI not available, trying selenium method")
                    use_clipboard = False
            
            # Method 2: Direct Selenium (fallback)
            if not use_clipboard:
                input_elem = self._find_input_element()
                if not input_elem:
                    logger.error("❌ Input field not found")
                    return False
                
                input_elem.clear()
                input_elem.send_keys(message)
                time.sleep(1)
                
                send_btn = self._find_send_button()
                if not send_btn:
                    logger.error("❌ Send button not found")
                    return False
                
                send_btn.click()
                time.sleep(2)
                
                logger.info("✅ Message sent via selenium")
                return True
            
        except Exception as e:
            logger.error(f"❌ Send message failed: {e}")
            return False

    def _find_input_element(self) -> Optional[Any]:
        """Find message input element using working selectors."""
        if not self.driver:
            return None
        
        from selenium.webdriver.common.by import By
        
        # Primary selectors (from unified_config.py - working)
        selectors = [
            "textarea[data-testid='prompt-textarea']",  # ChatGPT primary
            "textarea[placeholder*='Message']",
            "textarea[placeholder*='Ask']",
            "textarea",
            "#prompt-textarea",
            "[contenteditable='true']",
        ]
        
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if elem and elem.is_displayed():
                    return elem
            except:
                continue
        
        return None

    def _find_send_button(self) -> Optional[Any]:
        """Find send button element using working selectors."""
        if not self.driver:
            return None
        
        from selenium.webdriver.common.by import By
        
        # Primary selectors (from unified_config.py - working)
        selectors = [
            "button[data-testid='send-button']",  # ChatGPT primary
            "button[type='submit']",
            "button[aria-label*='Send']",
        ]
        
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if elem and elem.is_displayed():
                    return elem
            except:
                continue
        
        return None

    def navigate_to_conversation(self, url: str) -> bool:
        """Navigate to conversation."""
        if not self.driver:
            return False
            
        try:
            self.driver.get(url)
            time.sleep(3)
            logger.info(f"✅ Navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False

    def verify_page_loaded(self) -> bool:
        """Verify page has loaded."""
        if not self.driver:
            return False
            
        try:
            script = "return document.readyState === 'complete';"
            return self.driver.execute_script(script)
        except:
            return False

    def get_page_text(self) -> Optional[str]:
        """Get all text from current page."""
        if not self.driver:
            return None
            
        try:
            return self.driver.find_element_by_tag_name('body').text
        except Exception as e:
            logger.error(f"Failed to get page text: {e}")
            return None

    # ========== Session Management ==========
    
    def wait_with_exponential_backoff(self, attempt: int, max_wait: float = 60.0) -> None:
        """Wait with exponential backoff."""
        wait_time = min(2 ** attempt, max_wait)
        logger.info(f"⏳ Waiting {wait_time:.1f}s (attempt {attempt})")
        time.sleep(wait_time)


# Factory function
def create_thea_content_operations(driver: Any = None) -> TheaContentOperations:
    """Create Thea content operations instance."""
    return TheaContentOperations(driver)


__all__ = ['TheaContentOperations', 'ScrapedContent', 'create_thea_content_operations']


