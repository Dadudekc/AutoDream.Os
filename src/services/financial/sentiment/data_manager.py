"""
Sentiment Data Manager Module - Sentiment Analysis Package

This module handles data persistence, loading, and management for sentiment analysis.
Extracted from MarketSentimentService to improve maintainability and follow SRP principles.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
from collections import defaultdict

# Configure logging
logger = logging.getLogger(__name__)


class SentimentDataManager:
    """Handles data persistence and management for sentiment analysis"""

    def __init__(self, data_dir: str = "market_sentiment"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Data storage
        self.sentiment_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.sentiment_aggregates: Dict[str, Dict[str, Any]] = {}
        self.news_articles: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.market_psychology: Dict[str, Any] = {}

        # File paths
        self.sentiment_file = self.data_dir / "sentiment_data.json"
        self.aggregates_file = self.data_dir / "sentiment_aggregates.json"
        self.news_file = self.data_dir / "news_articles.json"
        self.psychology_file = self.data_dir / "market_psychology.json"

        # Data retention settings
        self.data_retention_days = 30

    def add_sentiment_data(
        self, symbol: str, sentiment_data: List[Dict[str, Any]]
    ) -> None:
        """Add sentiment data for a symbol"""
        try:
            if symbol not in self.sentiment_data:
                self.sentiment_data[symbol] = []

            # Add new data
            self.sentiment_data[symbol].extend(sentiment_data)

            # Remove old data (older than retention period)
            cutoff_time = datetime.now() - timedelta(days=self.data_retention_days)
            self.sentiment_data[symbol] = [
                data
                for data in self.sentiment_data[symbol]
                if data["timestamp"] >= cutoff_time
            ]

            logger.info(
                f"Added {len(sentiment_data)} sentiment data points for {symbol}"
            )

        except Exception as e:
            logger.error(f"Error adding sentiment data for {symbol}: {e}")

    def add_news_articles(
        self, symbol: str, articles: List[Dict[str, Any]]
    ) -> None:
        """Add news articles for a symbol"""
        try:
            if symbol not in self.news_articles:
                self.news_articles[symbol] = []

            # Add new articles
            self.news_articles[symbol].extend(articles)

            # Remove old articles (older than retention period)
            cutoff_time = datetime.now() - timedelta(days=self.data_retention_days)
            self.news_articles[symbol] = [
                article
                for article in self.news_articles[symbol]
                if article["published_at"] >= cutoff_time
            ]

            logger.info(f"Added {len(articles)} news articles for {symbol}")

        except Exception as e:
            logger.error(f"Error adding news articles for {symbol}: {e}")

    def update_sentiment_aggregate(
        self, symbol: str, aggregate: Dict[str, Any]
    ) -> None:
        """Update sentiment aggregate for a symbol"""
        try:
            self.sentiment_aggregates[symbol] = aggregate
            logger.info(f"Updated sentiment aggregate for {symbol}")

        except Exception as e:
            logger.error(f"Error updating sentiment aggregate for {symbol}: {e}")

    def update_market_psychology(
        self, psychology: Dict[str, Any]
    ) -> None:
        """Update market psychology data"""
        try:
            self.market_psychology = psychology
            logger.info("Updated market psychology data")

        except Exception as e:
            logger.error(f"Error updating market psychology: {e}")

    def get_sentiment_data(
        self, symbol: str, time_window: timedelta = None
    ) -> List[Dict[str, Any]]:
        """Get sentiment data for a symbol with optional time filtering"""
        try:
            if symbol not in self.sentiment_data:
                return []

            if time_window is None:
                return self.sentiment_data[symbol]

            # Filter by time window
            cutoff_time = datetime.now() - time_window
            return [
                data for data in self.sentiment_data[symbol]
                if data["timestamp"] >= cutoff_time
            ]

        except Exception as e:
            logger.error(f"Error getting sentiment data for {symbol}: {e}")
            return []

    def get_news_articles(
        self, symbol: str, time_window: timedelta = None
    ) -> List[Dict[str, Any]]:
        """Get news articles for a symbol with optional time filtering"""
        try:
            if symbol not in self.news_articles:
                return []

            if time_window is None:
                return self.news_articles[symbol]

            # Filter by time window
            cutoff_time = datetime.now() - time_window
            return [
                article for article in self.news_articles[symbol]
                if article["published_at"] >= cutoff_time
            ]

        except Exception as e:
            logger.error(f"Error getting news articles for {symbol}: {e}")
            return []

    def get_sentiment_aggregate(self, symbol: str) -> Dict[str, Any]:
        """Get sentiment aggregate for a symbol"""
        try:
            return self.sentiment_aggregates.get(symbol, {})
        except Exception as e:
            logger.error(f"Error getting sentiment aggregate for {symbol}: {e}")
            return {}

    def get_market_psychology(self) -> Dict[str, Any]:
        """Get market psychology data"""
        try:
            return self.market_psychology
        except Exception as e:
            logger.error(f"Error getting market psychology: {e}")
            return {}

    def save_data(self) -> bool:
        """Save all sentiment data to files"""
        try:
            # Save sentiment data
            sentiment_data = {}
            for symbol, data_list in self.sentiment_data.items():
                sentiment_data[symbol] = data_list

            with open(self.sentiment_file, "w") as f:
                json.dump(sentiment_data, f, indent=2, default=str)

            # Save sentiment aggregates
            with open(self.aggregates_file, "w") as f:
                json.dump(self.sentiment_aggregates, f, indent=2, default=str)

            # Save news articles
            with open(self.news_file, "w") as f:
                json.dump(self.news_articles, f, indent=2, default=str)

            # Save market psychology
            if self.market_psychology:
                with open(self.psychology_file, "w") as f:
                    json.dump(self.market_psychology, f, indent=2, default=str)

            logger.info("Sentiment data saved successfully")
            return True

        except Exception as e:
            logger.error(f"Error saving sentiment data: {e}")
            return False

    def load_data(self) -> bool:
        """Load all sentiment data from files"""
        try:
            # Load sentiment data
            if self.sentiment_file.exists():
                with open(self.sentiment_file, "r") as f:
                    sentiment_data = json.load(f)

                for symbol, data_list in sentiment_data.items():
                    for data_dict in data_list:
                        if "timestamp" in data_dict:
                            data_dict["timestamp"] = datetime.fromisoformat(
                                data_dict["timestamp"]
                            )
                    self.sentiment_data[symbol] = data_list

                logger.info(f"Loaded sentiment data for {len(sentiment_data)} symbols")

            # Load sentiment aggregates
            if self.aggregates_file.exists():
                with open(self.aggregates_file, "r") as f:
                    aggregates_data = json.load(f)

                for symbol, aggregate_dict in aggregates_data.items():
                    if "last_updated" in aggregate_dict:
                        aggregate_dict["last_updated"] = datetime.fromisoformat(
                            aggregate_dict["last_updated"]
                        )
                    self.sentiment_aggregates[symbol] = aggregate_dict

                logger.info(
                    f"Loaded sentiment aggregates for {len(aggregates_data)} symbols"
                )

            # Load news articles
            if self.news_file.exists():
                with open(self.news_file, "r") as f:
                    news_data = json.load(f)

                for symbol, articles_list in news_data.items():
                    for article_dict in articles_list:
                        if "published_at" in article_dict:
                            article_dict["published_at"] = datetime.fromisoformat(
                                article_dict["published_at"]
                            )
                    self.news_articles[symbol] = articles_list

                logger.info(f"Loaded news articles for {len(news_data)} symbols")

            # Load market psychology
            if self.psychology_file.exists():
                with open(self.psychology_file, "r") as f:
                    psychology_dict = json.load(f)

                if "last_updated" in psychology_dict:
                    psychology_dict["last_updated"] = datetime.fromisoformat(
                        psychology_dict["last_updated"]
                    )

                self.market_psychology = psychology_dict
                logger.info("Loaded market psychology data")

            return True

        except Exception as e:
            logger.error(f"Error loading sentiment data: {e}")
            return False

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of stored data"""
        try:
            return {
                "total_symbols": len(self.sentiment_data),
                "total_sentiment_data_points": sum(len(data) for data in self.sentiment_data.values()),
                "total_news_articles": sum(len(articles) for articles in self.news_articles.values()),
                "sentiment_aggregates_count": len(self.sentiment_aggregates),
                "has_market_psychology": bool(self.market_psychology),
                "data_retention_days": self.data_retention_days,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating data summary: {e}")
            return {}

    def cleanup_old_data(self) -> int:
        """Clean up data older than retention period"""
        try:
            cutoff_time = datetime.now() - timedelta(days=self.data_retention_days)
            cleaned_count = 0

            # Clean sentiment data
            for symbol in list(self.sentiment_data.keys()):
                original_count = len(self.sentiment_data[symbol])
                self.sentiment_data[symbol] = [
                    data for data in self.sentiment_data[symbol]
                    if data["timestamp"] >= cutoff_time
                ]
                cleaned_count += original_count - len(self.sentiment_data[symbol])

            # Clean news articles
            for symbol in list(self.news_articles.keys()):
                original_count = len(self.news_articles[symbol])
                self.news_articles[symbol] = [
                    article for article in self.news_articles[symbol]
                    if article["published_at"] >= cutoff_time
                ]
                cleaned_count += original_count - len(self.news_articles[symbol])

            logger.info(f"Cleaned up {cleaned_count} old data points")
            return cleaned_count

        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return 0

    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage information and file sizes"""
        try:
            file_info = {}
            total_size = 0

            for file_path in [self.sentiment_file, self.aggregates_file, 
                            self.news_file, self.psychology_file]:
                if file_path.exists():
                    size = file_path.stat().st_size
                    file_info[file_path.name] = {
                        "size_bytes": size,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "exists": True
                    }
                    total_size += size
                else:
                    file_info[file_path.name] = {
                        "size_bytes": 0,
                        "size_mb": 0,
                        "exists": False
                    }

            return {
                "files": file_info,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "data_directory": str(self.data_dir)
            }

        except Exception as e:
            logger.error(f"Error getting storage info: {e}")
            return {}

