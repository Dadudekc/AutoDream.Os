"""
ChatGPT Scraper for DreamVault

Integrated scraper with cookies, manual login, rate limits, and model selection.
"""

import logging
import json
import time
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path

from .browser_manager import BrowserManager
from .cookie_manager import CookieManager
from .login_handler import LoginHandler
from .conversation_extractor import ConversationExtractor
from .adaptive_extractor import AdaptiveExtractor

# Selenium imports
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class ChatGPTScraper:
    """
    Integrated ChatGPT scraper with all essential features.
    
    Features:
    - Cookie persistence
    - Manual login support
    - Rate limiting
    - Model selection
    - Conversation extraction
    - Resume functionality
    """
    
    def __init__(self, 
                 headless: bool = False,
                 use_undetected: bool = True,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 totp_secret: Optional[str] = None,
                 cookie_file: Optional[str] = None,
                 rate_limit_delay: float = 2.0,
                 progress_file: str = "data/scraper_progress.json"):
        """
        Initialize the ChatGPT scraper.
        
        Args:
            headless: Run browser in headless mode
            use_undetected: Use undetected-chromedriver
            username: ChatGPT username/email
            password: ChatGPT password
            totp_secret: TOTP secret for 2FA
            cookie_file: Path to cookie file
            rate_limit_delay: Delay between requests (seconds)
            progress_file: Path to progress tracking file
        """
        # Initialize components
        self.browser_manager = BrowserManager(headless=headless, use_undetected=use_undetected)
        self.cookie_manager = CookieManager(cookie_file)
        self.login_handler = LoginHandler(username, password, totp_secret)
        self.conversation_extractor = ConversationExtractor()
        self.adaptive_extractor = AdaptiveExtractor()
        
        # Configuration
        self.rate_limit_delay = rate_limit_delay
        self.driver = None
        self.progress_file = progress_file
        
        # Rate limiting state
        self.last_request_time = 0
        self.request_count = 0
        
        # Progress tracking
        self.processed_conversations = self._load_progress()
        
        logger.info("✅ ChatGPT Scraper initialized")
    
    def __enter__(self):
        """Context manager entry."""
        self.start_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()
    
    def start_driver(self) -> bool:
        """Start the web driver."""
        try:
            self.driver = self.browser_manager.create_driver()
            if self.driver:
                logger.info("✅ Driver started successfully")
                # Navigate to ChatGPT to initialize the driver properly
                self.driver.get("https://chat.openai.com")
                time.sleep(2)  # Give driver time to fully initialize
                logger.info("✅ Driver initialized and navigated to ChatGPT")
                return True
            else:
                logger.error("❌ Failed to start driver")
                return False
        except Exception as e:
            logger.error(f"Failed to start driver: {e}")
            return False
    
    def close_driver(self):
        """Close the web driver."""
        if self.driver:
            self.browser_manager.close_driver()
            self.driver = None
            logger.info("✅ Driver closed")
    
    def ensure_login(self, allow_manual: bool = True, manual_timeout: int = 60) -> bool:
        """
        Ensure user is logged into ChatGPT.
        
        Args:
            allow_manual: Allow manual login if automated fails
            manual_timeout: Timeout for manual login
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            # Ensure we're on the ChatGPT domain before loading cookies
            if not self.driver.current_url.startswith("https://chat.openai.com"):
                logger.info("🌐 Navigating to ChatGPT before loading cookies...")
                self.driver.get("https://chat.openai.com")
                time.sleep(3)  # Wait for page to load
            
            # Try to load cookies first
            if self.cookie_manager.has_valid_cookies():
                logger.info("🍪 Found saved cookies, attempting auto-login...")
                self.cookie_manager.load_cookies(self.driver)
                time.sleep(3)  # Give page time to process cookies
                
                # Refresh page to apply cookies
                logger.info("🔄 Refreshing page to apply cookies...")
                self.driver.refresh()
                time.sleep(3)
                
                # Check if cookies are still valid
                logger.info("🔍 Testing if cookies still work...")
                if self.login_handler._is_logged_in(self.driver):
                    logger.info("✅ ✨ SUCCESS! Cookies work! Auto-login successful!")
                    
                    # Handle workspace selection modal if it appears
                    if self._handle_workspace_selection():
                        logger.info("✅ Workspace selection handled")
                    
                    logger.info("⚡ Skipping manual login - proceeding directly to scraping...")
                    return True
                else:
                    logger.warning("⚠️ Cookies expired or invalid")
                    logger.info("🔄 Falling back to manual login...")
            else:
                logger.info("📝 No saved cookies found")
                logger.info("👤 Will need manual login this time...")
            
            # Perform manual login
            logger.info("🔐 Starting manual login process...")
            if self.login_handler.ensure_login(self.driver, allow_manual, manual_timeout):
                # Save cookies after successful login
                self.cookie_manager.save_cookies(self.driver)
                logger.info("✅ Login successful! Cookies saved for next time.")
                logger.info("💡 Next run will auto-login with these cookies!")
                return True
            else:
                logger.error("❌ Login failed")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def _rate_limit(self):
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def select_model(self, model: str = "") -> bool:
        """
        Select a specific ChatGPT model.
        
        Args:
            model: Model to select (e.g., "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo")
            
        Returns:
            True if model selection successful, False otherwise
        """
        if not model:
            logger.info("No specific model selected, using default")
            return True
        
        try:
            logger.info(f"🤖 Selecting model: {model}")
            
            # Navigate to ChatGPT
            self.driver.get("https://chat.openai.com")
            time.sleep(3)
            
            # Look for model selector
            model_selectors = [
                f"//button[contains(text(), '{model}')]",
                f"//div[contains(text(), '{model}')]",
                "//button[contains(@data-testid, 'model-selector')]"
            ]
            
            for selector in model_selectors:
                try:
                    element = self.driver.find_element_by_xpath(selector)
                    if element.is_displayed():
                        element.click()
                        time.sleep(2)
                        logger.info(f"✅ Model {model} selected")
                        return True
                except:
                    continue
            
            logger.warning(f"⚠️ Could not select model {model}, using default")
            return False
            
        except Exception as e:
            logger.error(f"Model selection error: {e}")
            return False
    
    def _handle_workspace_selection(self) -> bool:
        """
        Handle the workspace selection modal that appears after login.
        
        Returns:
            True if handled successfully or not needed, False if failed
        """
        try:
            logger.info("🔍 Checking for workspace selection modal...")
            
            # Wait a moment for modal to appear
            time.sleep(2)
            
            # Look for workspace selection modal
            workspace_selectors = [
                "//button[contains(text(), 'Personal account')]",
                "//button[contains(@class, '__menu-item') and contains(text(), 'Personal account')]",
                "//div[contains(text(), 'Select a workspace')]//following-sibling::*//button[contains(text(), 'Personal account')]",
                "//button[@data-state='off'][@role='radio'][contains(@class, '__menu-item')]"
            ]
            
            for selector in workspace_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        logger.info(f"✅ Found workspace selection button with selector: {selector}")
                        button = elements[0]
                        
                        # Click the Personal account button
                        logger.info("🖱️ Clicking 'Personal account' button...")
                        self.driver.execute_script("arguments[0].click();", button)
                        time.sleep(3)  # Wait for modal to close
                        
                        logger.info("✅ Workspace selection completed")
                        return True
                        
                except Exception as e:
                    logger.debug(f"Selector failed: {selector} - {e}")
                    continue
            
            logger.info("ℹ️ No workspace selection modal found (or already handled)")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to handle workspace selection: {e}")
            return False
    
    def get_conversation_list(self, progress_callback: Optional[Callable] = None) -> List[Dict[str, str]]:
        """
        Get list of available conversations with self-healing.
        
        Args:
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of conversation dictionaries
        """
        try:
            self._rate_limit()
            
            # Try adaptive extractor first (self-healing)
            logger.info("🔄 Using adaptive extractor for self-healing...")
            conversations = self.adaptive_extractor.get_conversation_list(self.driver, progress_callback)
            
            if conversations:
                logger.info(f"✅ Adaptive extractor found {len(conversations)} conversations")
                return conversations
            
            # Fallback to original extractor
            logger.warning("🔄 Adaptive extractor failed, trying original extractor...")
            return self.conversation_extractor.get_conversation_list(self.driver, progress_callback)
            
        except Exception as e:
            logger.error(f"Failed to get conversation list: {e}")
            return []
    
    def extract_conversation(self, conversation_url: str, output_dir: str = "data/raw", chronological_number: Optional[int] = None) -> bool:
        """
        Extract a single conversation.
        
        Args:
            conversation_url: URL of the conversation to extract
            output_dir: Directory to save extracted conversation
            chronological_number: Chronological number for this conversation (1 = oldest, N = newest)
            
        Returns:
            True if extraction successful, False otherwise
        """
        try:
            self._rate_limit()
            
            # Create output directory
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Enter conversation
            if not self.conversation_extractor.enter_conversation(self.driver, conversation_url):
                return False
            
            # Extract content
            conversation_data = self.conversation_extractor.get_conversation_content(self.driver)
            
            # Generate filename with chronological number
            if chronological_number:
                filename = f"conversation_{chronological_number}.json"
                logger.info(f"📅 Saving as conversation #{chronological_number} chronologically")
            else:
                # Fallback to original method if no chronological number provided
                conversation_id = conversation_url.split("/c/")[-1] if "/c/" in conversation_url else f"conv_{int(time.time())}"
                filename = f"{conversation_id}.json"
            
            output_file = Path(output_dir) / filename
            
            # Save conversation
            if self.conversation_extractor.save_conversation(conversation_data, str(output_file)):
                logger.info(f"✅ Extracted conversation: {filename}")
                return True
            else:
                logger.error(f"❌ Failed to save conversation: {filename}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to extract conversation: {e}")
            return False
    
    def extract_all_conversations_smart(self, limit: Optional[int] = None, 
                                       output_dir: str = "data/raw",
                                       progress_callback: Optional[Callable] = None,
                                       skip_processed: bool = True) -> Dict[str, int]:
        """
        SMART extraction: Count first, extract as we go, reverse numbering at end.
        
        This is much faster than the old method because we don't scroll through
        all conversations first - we extract them as we discover them.
        
        Args:
            limit: Maximum number of conversations to extract
            output_dir: Directory to save extracted conversations
            progress_callback: Optional callback for progress updates
            skip_processed: Skip already processed conversations
            
        Returns:
            Dictionary with extraction statistics
        """
        try:
            logger.info("🧠 Starting SMART conversation extraction...")
            logger.info("   Strategy: Count first → Extract as we go → Reverse numbering")
            
            # Create output directory
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Step 1: Quick count of total conversations (fast scroll)
            logger.info("📊 Step 1: Counting total conversations...")
            total_count = self._count_total_conversations()
            logger.info(f"✅ Found {total_count} total conversations")
            
            if limit:
                total_count = min(total_count, limit)
                logger.info(f"🔢 Limited to {total_count} conversations")
            
            # Step 2: Extract conversations as we scroll (much faster)
            logger.info("📝 Step 2: Extracting conversations as we discover them...")
            extracted_files = []
            stats = {
                "total": total_count,
                "extracted": 0,
                "failed": 0,
                "skipped": 0,
                "errors": []
            }
            
            # Get conversation list with smart extraction
            conversations = self._get_conversations_with_smart_extraction(
                total_count, output_dir, progress_callback, skip_processed
            )
            
            # Update stats with actual results
            stats['extracted'] = len([f for f in Path(output_dir).glob("conversation_*.json") if f.exists()])
            
            # Step 3: Reverse file numbering (conversation_1 = oldest)
            logger.info("🔄 Step 3: Reversing file numbering for chronological order...")
            self._reverse_file_numbering(output_dir, total_count)
            
            logger.info(f"✅ SMART extraction complete: {stats['extracted']}/{stats['total']} successful")
            return stats
            
        except Exception as e:
            logger.error(f"Failed SMART extraction: {e}")
            return {"total": 0, "extracted": 0, "failed": 0, "errors": [str(e)]}
    
    def _count_total_conversations(self) -> int:
        """Quickly count total conversations with fast scrolling."""
        try:
            logger.info("🔍 Fast counting conversations...")
            
            # Use adaptive extractor for fast counting
            conversations = self.adaptive_extractor.get_conversation_list(self.driver)
            total_count = len(conversations)
            
            logger.info(f"📊 Fast count complete: {total_count} conversations")
            return total_count
            
        except Exception as e:
            logger.error(f"Failed to count conversations: {e}")
            return 0
    
    def _get_conversations_with_smart_extraction(self, total_count: int, 
                                               output_dir: str,
                                               progress_callback: Optional[Callable],
                                               skip_processed: bool) -> List[Dict]:
        """Extract conversations as we discover them (much faster)."""
        try:
            logger.info("⚡ Smart extraction: processing conversations as we find them...")
            
            # Get conversation list (this will scroll and find all)
            conversations = self.adaptive_extractor.get_conversation_list(self.driver)
            
            if not conversations:
                logger.warning("No conversations found")
                return []
            
            # Limit if specified
            if total_count and len(conversations) > total_count:
                conversations = conversations[:total_count]
            
            logger.info(f"📋 Processing {len(conversations)} conversations...")
            
            # Extract each conversation immediately
            extracted_count = 0
            for i, conversation in enumerate(conversations):
                try:
                    # Skip if already processed
                    if skip_processed and self._is_conversation_processed(conversation):
                        continue
                    
                    # Extract immediately (no waiting)
                    logger.info(f"📝 Extracting conversation {i+1}/{len(conversations)}: {conversation.get('title', 'Unknown')}")
                    
                    if self.extract_conversation(conversation['url'], output_dir, i + 1):
                        extracted_count += 1
                        self._mark_conversation_processed(conversation, success=True)
                    else:
                        self._mark_conversation_processed(conversation, success=False)
                    
                    if progress_callback:
                        progress_callback(i + 1, len(conversations))
                        
                except Exception as e:
                    logger.error(f"Error extracting conversation {i+1}: {e}")
                    self._mark_conversation_processed(conversation, success=False)
            
            logger.info(f"✅ Smart extraction complete: {extracted_count} conversations extracted")
            return conversations
            
        except Exception as e:
            logger.error(f"Smart extraction failed: {e}")
            return []
    
    def _reverse_file_numbering(self, output_dir: str, total_count: int):
        """Reverse file numbering so conversation_1 = oldest, conversation_N = newest."""
        try:
            logger.info("🔄 Reversing file numbering for chronological order...")
            
            raw_dir = Path(output_dir)
            if not raw_dir.exists():
                logger.warning("Output directory doesn't exist")
                return
            
            # Find all conversation files and sort them
            all_files = list(raw_dir.glob("conversation_*.json"))
            if not all_files:
                logger.warning("No conversation files found to rename")
                return
            
            # Sort files by modification time (newest first)
            all_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Take only the most recent files (from this extraction)
            new_files = all_files[:total_count]
            
            logger.info(f"📁 Found {len(new_files)} NEW conversation files to rename")
            
            # Create temporary directory for renaming
            temp_dir = raw_dir / "temp_rename"
            temp_dir.mkdir(exist_ok=True)
            
            # Move files to temp directory with reversed names
            for i, file_path in enumerate(new_files):
                try:
                    # New chronological number (oldest = 1, newest = N)
                    # Reverse the order: first extracted becomes newest
                    chronological_number = total_count - i
                    new_name = f"conversation_{chronological_number}.json"
                    temp_file = temp_dir / new_name
                    
                    # Copy file to temp location
                    import shutil
                    shutil.copy2(file_path, temp_file)
                    
                except Exception as e:
                    logger.error(f"Failed to rename {file_path}: {e}")
            
            # Remove original files
            for file_path in new_files:
                try:
                    file_path.unlink()
                except Exception as e:
                    logger.error(f"Failed to remove original {file_path}: {e}")
            
            # Move files back from temp directory
            temp_files = list(temp_dir.glob("conversation_*.json"))
            for temp_file in temp_files:
                try:
                    final_file = raw_dir / temp_file.name
                    temp_file.rename(final_file)
                except Exception as e:
                    logger.error(f"Failed to move {temp_file}: {e}")
            
            # Remove temp directory
            try:
                temp_dir.rmdir()
            except:
                pass
            
            logger.info("✅ File numbering reversed successfully")
            logger.info(f"   conversation_1.json = oldest conversation")
            logger.info(f"   conversation_{total_count}.json = newest conversation")
            
        except Exception as e:
            logger.error(f"Failed to reverse file numbering: {e}")
    
    def extract_all_conversations(self, limit: Optional[int] = None, 
                                output_dir: str = "data/raw",
                                progress_callback: Optional[Callable] = None,
                                skip_processed: bool = True) -> Dict[str, int]:
        """
        Extract all available conversations with resume functionality.
        
        Args:
            limit: Maximum number of conversations to extract
            output_dir: Directory to save extracted conversations
            progress_callback: Optional callback for progress updates
            skip_processed: Skip already processed conversations
            
        Returns:
            Dictionary with extraction statistics
        """
        try:
            logger.info("🚀 Starting conversation extraction...")
            
            # Get progress stats
            progress_stats = self.get_progress_stats()
            if progress_stats["total_processed"] > 0:
                logger.info(f"📊 Resume mode: {progress_stats['successful']} conversations already processed")
            
            # Get conversation list
            conversations = self.get_conversation_list(progress_callback)
            
            if limit:
                conversations = conversations[:limit]
            
            # Filter out already processed conversations
            if skip_processed:
                original_count = len(conversations)
                conversations = [conv for conv in conversations if not self._is_conversation_processed(conv)]
                skipped_count = original_count - len(conversations)
                if skipped_count > 0:
                    logger.info(f"⏭️ Skipping {skipped_count} already processed conversations")
            
            logger.info(f"📋 Found {len(conversations)} conversations to extract")
            
            if len(conversations) == 0:
                logger.info("✅ All conversations already processed!")
                return {
                    "total": 0,
                    "extracted": 0,
                    "failed": 0,
                    "skipped": progress_stats["total_processed"],
                    "errors": []
                }
            
            stats = {
                "total": len(conversations),
                "extracted": 0,
                "failed": 0,
                "skipped": progress_stats["total_processed"],
                "errors": []
            }
            
            # Number conversations in reverse chronological order
            # conversation_1 = oldest (first ever), conversation_N = newest (most recent)
            total_conversations = len(conversations)
            
            for i, conversation in enumerate(conversations):
                try:
                    # Calculate reverse chronological number
                    chronological_number = total_conversations - i
                    
                    logger.info(f"📝 Extracting conversation {i+1}/{total_conversations} (will be #{chronological_number} chronologically): {conversation.get('title', 'Unknown')}")
                    logger.info(f"   📅 This is conversation #{chronological_number} chronologically (oldest = #1, newest = #{total_conversations})")
                    
                    if self.extract_conversation(conversation['url'], output_dir, chronological_number):
                        stats["extracted"] += 1
                        self._mark_conversation_processed(conversation, success=True)
                    else:
                        stats["failed"] += 1
                        self._mark_conversation_processed(conversation, success=False)
                        stats["errors"].append(f"Failed to extract {conversation.get('id', 'unknown')}")
                    
                    if progress_callback:
                        progress_callback(i + 1, total_conversations)
                        
                except Exception as e:
                    stats["failed"] += 1
                    self._mark_conversation_processed(conversation, success=False)
                    stats["errors"].append(f"Error extracting {conversation.get('id', 'unknown')}: {e}")
                    logger.error(f"Error extracting conversation: {e}")
            
            logger.info(f"✅ Extraction complete: {stats['extracted']}/{stats['total']} successful")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to extract conversations: {e}")
            return {"total": 0, "extracted": 0, "failed": 0, "errors": [str(e)]}
    
    def get_rate_limit_info(self) -> Dict[str, any]:
        """Get current rate limiting information."""
        return {
            "request_count": self.request_count,
            "rate_limit_delay": self.rate_limit_delay,
            "last_request_time": self.last_request_time
        }
    
    def get_adaptive_health_status(self) -> Dict[str, any]:
        """Get health status of the adaptive extractor."""
        return self.adaptive_extractor.get_health_status() 

    def _load_progress(self) -> Dict[str, Dict]:
        """Load progress from file."""
        try:
            if Path(self.progress_file).exists():
                with open(self.progress_file, 'r') as f:
                    progress = json.load(f)
                    logger.info(f"📊 Loaded progress: {len(progress)} conversations already processed")
                    return progress
        except Exception as e:
            logger.warning(f"Failed to load progress: {e}")
        return {}
    
    def _save_progress(self):
        """Save progress to file."""
        try:
            Path(self.progress_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.progress_file, 'w') as f:
                json.dump(self.processed_conversations, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
    
    def _get_conversation_hash(self, conversation: Dict) -> str:
        """Generate hash for conversation identification."""
        content = f"{conversation.get('id', '')}{conversation.get('title', '')}{conversation.get('url', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _is_conversation_processed(self, conversation: Dict) -> bool:
        """Check if conversation has already been processed."""
        conv_hash = self._get_conversation_hash(conversation)
        return conv_hash in self.processed_conversations
    
    def _mark_conversation_processed(self, conversation: Dict, success: bool = True):
        """Mark conversation as processed."""
        conv_hash = self._get_conversation_hash(conversation)
        self.processed_conversations[conv_hash] = {
            "id": conversation.get('id'),
            "title": conversation.get('title'),
            "url": conversation.get('url'),
            "processed_at": datetime.now().isoformat(),
            "success": success
        }
        self._save_progress()
    
    def reset_progress(self):
        """Reset progress tracking."""
        self.processed_conversations = {}
        if Path(self.progress_file).exists():
            Path(self.progress_file).unlink()
        logger.info("🔄 Progress reset - will process all conversations")
    
    def get_progress_stats(self) -> Dict[str, any]:
        """Get progress statistics."""
        total_processed = len(self.processed_conversations)
        successful = sum(1 for conv in self.processed_conversations.values() if conv.get('success', False))
        failed = total_processed - successful
        
        return {
            "total_processed": total_processed,
            "successful": successful,
            "failed": failed,
            "progress_file": self.progress_file
        } 