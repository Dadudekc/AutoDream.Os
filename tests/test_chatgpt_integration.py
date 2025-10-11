"""
ChatGPT Integration Tests - V2 Compliant
========================================

Comprehensive test suite for ChatGPT Integration.
Maintains 100% test pass rate and V2 compliance standards.

Author: Agent-1 - Browser Automation Specialist
License: MIT
"""

from services.chatgpt.extractor import ConversationExtractor
from services.chatgpt.navigator import ChatGPTNavigator
from services.chatgpt.session import BrowserSessionManager


class TestChatGPTNavigator:
    """Test ChatGPT navigator."""

    def test_navigator_initialization(self):
        """Test navigator initialization."""
        navigator = ChatGPTNavigator()

        assert navigator.default_url == "https://chat.openai.com/"
        assert navigator.timeout == 60000
        assert navigator.wait_for_selector == "textarea"

    def test_navigation_info(self):
        """Test navigation information retrieval."""
        navigator = ChatGPTNavigator()
        info = navigator.get_navigation_info()

        assert "playwright_available" in info
        assert "default_url" in info
        assert "timeout" in info
        assert "has_active_page" in info


class TestBrowserSessionManager:
    """Test browser session manager."""

    def test_session_manager_initialization(self):
        """Test session manager initialization."""
        session_manager = BrowserSessionManager()

        assert session_manager.persistent
        assert not session_manager.session_valid

    def test_session_info(self):
        """Test session information retrieval."""
        session_manager = BrowserSessionManager()
        info = session_manager.get_session_info()

        assert "playwright_available" in info
        assert "persistent" in info
        assert "session_valid" in info
        assert "cookies_count" in info

    def test_clear_session(self):
        """Test session clearing."""
        session_manager = BrowserSessionManager()
        success = session_manager.clear_session()

        assert success
        assert not session_manager.session_valid
        assert len(session_manager.cookie_cache) == 0


class TestConversationExtractor:
    """Test conversation extractor."""

    def test_extractor_initialization(self):
        """Test extractor initialization."""
        extractor = ConversationExtractor()

        assert extractor.max_messages == 1000
        assert extractor.save_format == "json"

    def test_extraction_info(self):
        """Test extraction information retrieval."""
        extractor = ConversationExtractor()
        info = extractor.get_extraction_info()

        assert "playwright_available" in info
        assert "message_selector" in info
        assert "max_messages" in info
        assert "save_format" in info

    def test_list_conversations(self):
        """Test listing conversations."""
        extractor = ConversationExtractor()
        conversations = extractor.list_conversations()

        # Should return a list (empty or with conversations)
        assert isinstance(conversations, list)

    def test_cleanup_old_conversations(self):
        """Test conversation cleanup."""
        extractor = ConversationExtractor()
        cleaned = extractor.cleanup_old_conversations(max_age_days=0)

        # Should return a number
        assert isinstance(cleaned, int)
        assert cleaned >= 0
