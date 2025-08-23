#!/usr/bin/env python3
"""
Test Suite for Entertainment Core System
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- Content management system
- Social media integration
- User engagement analytics
- Database operations
- System coordination
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path to import entertainment modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from entertainment_apps.entertainment_core_system import (
    EntertainmentCoreSystem,
    ContentManager,
    SocialMediaIntegration,
    UserEngagementAnalytics,
    ContentItem,
    ContentType,
    ContentStatus,
    UserEngagement,
)


class TestContentItem(unittest.TestCase):
    """Test ContentItem data class"""

    def test_default_initialization(self):
        """Test ContentItem with default values"""
        content = ContentItem(
            id="test_001",
            title="Test Content",
            description="Test description",
            content_type=ContentType.GAME,
            status=ContentStatus.DRAFT,
        )

        self.assertEqual(content.id, "test_001")
        self.assertEqual(content.title, "Test Content")
        self.assertEqual(content.description, "Test description")
        self.assertEqual(content.content_type, ContentType.GAME)
        self.assertEqual(content.status, ContentStatus.DRAFT)
        self.assertEqual(content.views, 0)
        self.assertEqual(content.likes, 0)
        self.assertEqual(content.shares, 0)
        self.assertIsInstance(content.created_at, datetime)
        self.assertIsInstance(content.updated_at, datetime)
        self.assertEqual(content.tags, [])
        self.assertEqual(content.metadata, {})

    def test_custom_initialization(self):
        """Test ContentItem with custom values"""
        custom_time = datetime.now()
        content = ContentItem(
            id="custom_001",
            title="Custom Content",
            description="Custom description",
            content_type=ContentType.VIDEO,
            status=ContentStatus.PUBLISHED,
            tags=["action", "adventure"],
            metadata={"genre": "Action", "rating": "PG-13"},
            created_at=custom_time,
            updated_at=custom_time,
            views=100,
            likes=50,
            shares=25,
        )

        self.assertEqual(content.tags, ["action", "adventure"])
        self.assertEqual(content.metadata["genre"], "Action")
        self.assertEqual(content.metadata["rating"], "PG-13")
        self.assertEqual(content.views, 100)
        self.assertEqual(content.likes, 50)
        self.assertEqual(content.shares, 25)

    def test_to_dict_conversion(self):
        """Test ContentItem to dictionary conversion"""
        content = ContentItem(
            id="dict_test_001",
            title="Dict Test",
            description="Test for dict conversion",
            content_type=ContentType.AUDIO,
            status=ContentStatus.PUBLISHED,
        )

        content_dict = content.to_dict()

        self.assertIsInstance(content_dict, dict)
        self.assertEqual(content_dict["id"], "dict_test_001")
        self.assertEqual(content_dict["content_type"], "audio")
        self.assertEqual(content_dict["status"], "published")
        self.assertIn("created_at", content_dict)
        self.assertIn("updated_at", content_dict)


class TestUserEngagement(unittest.TestCase):
    """Test UserEngagement data class"""

    def test_default_initialization(self):
        """Test UserEngagement with default values"""
        engagement = UserEngagement(
            user_id="user_001", content_id="content_001", action_type="view"
        )

        self.assertEqual(engagement.user_id, "user_001")
        self.assertEqual(engagement.content_id, "content_001")
        self.assertEqual(engagement.action_type, "view")
        self.assertIsInstance(engagement.timestamp, datetime)
        self.assertEqual(engagement.metadata, {})

    def test_custom_initialization(self):
        """Test UserEngagement with custom values"""
        custom_time = datetime.now()
        custom_metadata = {"device": "mobile", "location": "US"}

        engagement = UserEngagement(
            user_id="user_002",
            content_id="content_002",
            action_type="like",
            timestamp=custom_time,
            metadata=custom_metadata,
        )

        self.assertEqual(engagement.timestamp, custom_time)
        self.assertEqual(engagement.metadata, custom_metadata)

    def test_to_dict_conversion(self):
        """Test UserEngagement to dictionary conversion"""
        engagement = UserEngagement(
            user_id="user_003", content_id="content_003", action_type="share"
        )

        engagement_dict = engagement.to_dict()

        self.assertIsInstance(engagement_dict, dict)
        self.assertEqual(engagement_dict["user_id"], "user_003")
        self.assertEqual(engagement_dict["action_type"], "share")
        self.assertIn("timestamp", engagement_dict)


class TestContentManager(unittest.TestCase):
    """Test ContentManager class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_entertainment.db")
        self.content_manager = ContentManager(self.db_path)

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        shutil.rmtree(self.temp_dir)

    def test_database_initialization(self):
        """Test database initialization"""
        # Database should be created in setUp
        self.assertTrue(os.path.exists(self.db_path))

        # Check if tables exist
        with sqlite3.connect(self.content_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            self.assertIn("content", tables)
            self.assertIn("engagement", tables)

    def test_add_content(self):
        """Test adding content to database"""
        content = ContentItem(
            id="test_add_001",
            title="Test Add Content",
            description="Test for adding content",
            content_type=ContentType.GAME,
            status=ContentStatus.DRAFT,
        )

        success = self.content_manager.add_content(content)
        self.assertTrue(success)

        # Verify content was added
        retrieved_content = self.content_manager.get_content("test_add_001")
        self.assertIsNotNone(retrieved_content)
        self.assertEqual(retrieved_content.title, "Test Add Content")

    def test_get_content(self):
        """Test retrieving content by ID"""
        # Add test content
        content = ContentItem(
            id="test_get_001",
            title="Test Get Content",
            description="Test for getting content",
            content_type=ContentType.VIDEO,
            status=ContentStatus.PUBLISHED,
        )

        self.content_manager.add_content(content)

        # Retrieve content
        retrieved_content = self.content_manager.get_content("test_get_001")
        self.assertIsNotNone(retrieved_content)
        self.assertEqual(retrieved_content.id, "test_get_001")
        self.assertEqual(retrieved_content.content_type, ContentType.VIDEO)

    def test_get_nonexistent_content(self):
        """Test retrieving non-existent content"""
        retrieved_content = self.content_manager.get_content("nonexistent_001")
        self.assertIsNone(retrieved_content)

    def test_get_content_by_type(self):
        """Test retrieving content by type"""
        # Add different types of content
        game_content = ContentItem(
            id="game_001",
            title="Test Game",
            description="A test game",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        video_content = ContentItem(
            id="video_001",
            title="Test Video",
            description="A test video",
            content_type=ContentType.VIDEO,
            status=ContentStatus.PUBLISHED,
        )

        self.content_manager.add_content(game_content)
        self.content_manager.add_content(video_content)

        # Get game content
        game_contents = self.content_manager.get_content_by_type(ContentType.GAME)
        self.assertEqual(len(game_contents), 1)
        self.assertEqual(game_contents[0].content_type, ContentType.GAME)

        # Get video content
        video_contents = self.content_manager.get_content_by_type(ContentType.VIDEO)
        self.assertEqual(len(video_contents), 1)
        self.assertEqual(video_contents[0].content_type, ContentType.VIDEO)

    def test_search_content(self):
        """Test content search functionality"""
        # Add content with searchable terms
        content = ContentItem(
            id="search_test_001",
            title="Amazing Adventure Game",
            description="An epic adventure game with stunning graphics",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
            tags=["adventure", "rpg", "fantasy"],
        )

        self.content_manager.add_content(content)

        # Search by title
        results = self.content_manager.search_content("Amazing")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "search_test_001")

        # Search by description
        results = self.content_manager.search_content("epic")
        self.assertEqual(len(results), 1)

        # Search by tags
        results = self.content_manager.search_content("fantasy")
        self.assertEqual(len(results), 1)

    def test_update_content_status(self):
        """Test updating content status"""
        content = ContentItem(
            id="status_test_001",
            title="Status Test Content",
            description="Test for status updates",
            content_type=ContentType.GAME,
            status=ContentStatus.DRAFT,
        )

        self.content_manager.add_content(content)

        # Update status
        success = self.content_manager.update_content_status(
            "status_test_001", ContentStatus.PUBLISHED
        )
        self.assertTrue(success)

        # Verify status was updated
        updated_content = self.content_manager.get_content("status_test_001")
        self.assertEqual(updated_content.status, ContentStatus.PUBLISHED)


class TestSocialMediaIntegration(unittest.TestCase):
    """Test SocialMediaIntegration class"""

    def setUp(self):
        """Set up test fixtures"""
        self.social_media = SocialMediaIntegration()

    def test_add_platform(self):
        """Test adding social media platforms"""
        self.social_media.add_platform("twitter", "test_key_1", 100)
        self.social_media.add_platform("facebook", "test_key_2", 200)

        self.assertIn("twitter", self.social_media.platforms)
        self.assertIn("facebook", self.social_media.platforms)

        self.assertEqual(self.social_media.platforms["twitter"]["rate_limit"], 100)
        self.assertEqual(self.social_media.platforms["facebook"]["rate_limit"], 200)

    def test_post_content_success(self):
        """Test successful content posting"""
        self.social_media.add_platform("twitter", "test_key", 100)

        content = ContentItem(
            id="post_test_001",
            title="Test Post",
            description="Test content for posting",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        success = self.social_media.post_content("twitter", content, "Check this out!")
        self.assertTrue(success)

        # Check rate limit counter
        self.assertEqual(self.social_media.platforms["twitter"]["requests_made"], 1)

    def test_post_content_platform_not_configured(self):
        """Test posting to non-configured platform"""
        content = ContentItem(
            id="post_test_002",
            title="Test Post",
            description="Test content for posting",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        success = self.social_media.post_content("instagram", content)
        self.assertFalse(success)

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        self.social_media.add_platform("test_platform", "test_key", 2)

        content = ContentItem(
            id="rate_test_001",
            title="Rate Test",
            description="Test for rate limiting",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        # First two posts should succeed
        self.assertTrue(self.social_media.post_content("test_platform", content))
        self.assertTrue(self.social_media.post_content("test_platform", content))

        # Third post should fail due to rate limiting
        self.assertFalse(self.social_media.post_content("test_platform", content))

    def test_get_platform_stats(self):
        """Test getting platform statistics"""
        self.social_media.add_platform("test_platform", "test_key", 100)

        stats = self.social_media.get_platform_stats("test_platform")

        self.assertEqual(stats["platform"], "test_platform")
        self.assertEqual(stats["rate_limit"], 100)
        self.assertEqual(stats["requests_made"], 0)
        self.assertEqual(stats["requests_remaining"], 100)

    def test_get_nonexistent_platform_stats(self):
        """Test getting stats for non-existent platform"""
        stats = self.social_media.get_platform_stats("nonexistent")
        self.assertEqual(stats, {})


class TestUserEngagementAnalytics(unittest.TestCase):
    """Test UserEngagementAnalytics class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_analytics.db")
        self.content_manager = ContentManager(self.db_path)
        self.analytics = UserEngagementAnalytics(self.content_manager)

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        shutil.rmtree(self.temp_dir)

    def test_track_engagement(self):
        """Test tracking user engagement"""
        # Add test content first
        content = ContentItem(
            id="engagement_test_001",
            title="Engagement Test",
            description="Test for engagement tracking",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        self.content_manager.add_content(content)

        # Track engagement
        self.analytics.track_engagement("user_001", "engagement_test_001", "view")
        self.analytics.track_engagement("user_002", "engagement_test_001", "like")

        # Verify content metrics were updated
        updated_content = self.content_manager.get_content("engagement_test_001")
        self.assertEqual(updated_content.views, 1)
        self.assertEqual(updated_content.likes, 1)

    def test_get_content_analytics(self):
        """Test getting content analytics"""
        # Add test content
        content = ContentItem(
            id="analytics_test_001",
            title="Analytics Test",
            description="Test for analytics",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        self.content_manager.add_content(content)

        # Track various engagements
        self.analytics.track_engagement("user_001", "analytics_test_001", "view")
        self.analytics.track_engagement("user_002", "analytics_test_001", "view")
        self.analytics.track_engagement("user_003", "analytics_test_001", "like")
        self.analytics.track_engagement("user_004", "analytics_test_001", "share")

        # Get analytics
        analytics = self.analytics.get_content_analytics("analytics_test_001")

        self.assertEqual(analytics["content_id"], "analytics_test_001")
        self.assertEqual(analytics["views"], 2)
        self.assertEqual(analytics["likes"], 1)
        self.assertEqual(analytics["shares"], 1)
        self.assertEqual(analytics["total_engagement"], 4)
        self.assertIn("engagement_breakdown", analytics)

    def test_get_popular_content(self):
        """Test getting popular content"""
        # Add multiple content items with different engagement levels
        content1 = ContentItem(
            id="popular_001",
            title="Popular Content 1",
            description="High engagement content",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
            views=100,
            likes=50,
            shares=25,
        )

        content2 = ContentItem(
            id="popular_002",
            title="Popular Content 2",
            description="Medium engagement content",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
            views=50,
            likes=25,
            shares=10,
        )

        self.content_manager.add_content(content1)
        self.content_manager.add_content(content2)

        # Get popular content
        popular_content = self.analytics.get_popular_content(limit=5)

        self.assertEqual(len(popular_content), 2)
        # First item should have higher engagement
        self.assertEqual(popular_content[0]["id"], "popular_001")
        self.assertEqual(popular_content[0]["total_engagement"], 175)
        self.assertEqual(popular_content[1]["id"], "popular_002")
        self.assertEqual(popular_content[1]["total_engagement"], 85)


class TestEntertainmentCoreSystem(unittest.TestCase):
    """Test EntertainmentCoreSystem main class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_entertainment_system.db")
        self.entertainment_system = EntertainmentCoreSystem(self.db_path)

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        shutil.rmtree(self.temp_dir)

    def test_system_initialization(self):
        """Test system initialization"""
        self.assertIsNotNone(self.entertainment_system.content_manager)
        self.assertIsNotNone(self.entertainment_system.social_media)
        self.assertIsNotNone(self.entertainment_system.analytics)
        self.assertFalse(self.entertainment_system.running)

    def test_add_content(self):
        """Test adding content through the main system"""
        content = ContentItem(
            id="system_test_001",
            title="System Test Content",
            description="Test content for main system",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        success = self.entertainment_system.add_content(content)
        self.assertTrue(success)

        # Verify content was added
        retrieved_content = self.entertainment_system.content_manager.get_content(
            "system_test_001"
        )
        self.assertIsNotNone(retrieved_content)

    def test_social_media_integration(self):
        """Test social media integration through main system"""
        # Add platform
        self.entertainment_system.social_media.add_platform("twitter", "test_key", 100)

        # Create content
        content = ContentItem(
            id="social_test_001",
            title="Social Media Test",
            description="Test for social media integration",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        # Post to social media
        success = self.entertainment_system.post_to_social_media(
            "twitter", content, "Check this out!"
        )
        self.assertTrue(success)

    def test_user_engagement_tracking(self):
        """Test user engagement tracking through main system"""
        # Add content
        content = ContentItem(
            id="engagement_system_test_001",
            title="Engagement System Test",
            description="Test for engagement tracking in main system",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        self.entertainment_system.add_content(content)

        # Track engagement
        self.entertainment_system.track_user_engagement(
            "user_001", "engagement_system_test_001", "view"
        )
        self.entertainment_system.track_user_engagement(
            "user_002", "engagement_system_test_001", "like"
        )

        # Get analytics
        analytics = self.entertainment_system.get_content_analytics(
            "engagement_system_test_001"
        )
        self.assertEqual(analytics["views"], 1)
        self.assertEqual(analytics["likes"], 1)

    def test_content_search(self):
        """Test content search through main system"""
        # Add content
        content = ContentItem(
            id="search_system_test_001",
            title="Search System Test",
            description="Test for search functionality in main system",
            content_type=ContentType.GAME,
            status=ContentStatus.PUBLISHED,
        )

        self.entertainment_system.add_content(content)

        # Search content
        results = self.entertainment_system.search_content("Search System")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "search_system_test_001")

    def test_get_system_status(self):
        """Test getting system status"""
        status = self.entertainment_system.get_system_status()

        self.assertIn("content_count", status)
        self.assertIn("social_platforms", status)
        self.assertIn("database_path", status)
        self.assertIn("system_running", status)

        self.assertEqual(status["content_count"], 0)
        self.assertEqual(status["social_platforms"], [])
        self.assertEqual(status["database_path"], self.db_path)
        self.assertFalse(status["system_running"])


def run_entertainment_tests():
    """Run all entertainment tests"""
    print("🎭 Running Entertainment Core System Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestContentItem,
        TestUserEngagement,
        TestContentManager,
        TestSocialMediaIntegration,
        TestUserEngagementAnalytics,
        TestEntertainmentCoreSystem,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 ENTERTAINMENT CORE SYSTEM TEST RESULTS:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\n🎉 ALL ENTERTAINMENT TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME ENTERTAINMENT TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_entertainment_tests()
    sys.exit(0 if success else 1)
