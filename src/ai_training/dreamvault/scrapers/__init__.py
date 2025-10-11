"""
DreamVault Scrapers - ChatGPT conversation scraping.

V2 Compliance: Ported from DreamVault repository
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from .browser_manager import BrowserManager
from .cookie_manager import CookieManager

# ChatGPTScraper has additional dependencies (conversation_extractor, adaptive_extractor)
# Import only if needed - available but requires additional porting
try:
    from .chatgpt_scraper import ChatGPTScraper
    __all__ = ['BrowserManager', 'ChatGPTScraper', 'CookieManager']
except ImportError:
    __all__ = ['BrowserManager', 'CookieManager']



