"""
Text Analyzer Module - Sentiment Analysis Package

This module handles text-based sentiment analysis including news articles,
social media posts, and general text content. Extracted from MarketSentimentService
to improve maintainability and follow SRP principles.
"""

import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any
from textblob import TextBlob

# Configure logging
logger = logging.getLogger(__name__)


class TextAnalyzer:
    """Handles text-based sentiment analysis for various content types"""

    def __init__(self):
        # Keywords for sentiment analysis
        self.bullish_keywords = [
            "bullish", "positive", "growth", "recovery", "rally", "surge",
            "gain", "strong", "improve", "beat", "exceed", "upgrade",
            "buy", "outperform"
        ]

        self.bearish_keywords = [
            "bearish", "negative", "decline", "fall", "drop", "crash",
            "loss", "weak", "worsen", "miss", "downgrade", "sell",
            "underperform"
        ]

        # Sentiment analysis parameters
        self.sentiment_params = {
            "textblob_threshold": 0.1,
            "confidence_threshold": 0.6,
        }

    def analyze_text_sentiment(self, text: str) -> Tuple[float, float]:
        """Analyze text sentiment using TextBlob and keyword analysis"""
        try:
            if not text or len(text.strip()) < 10:
                return 0.0, 0.0

            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_score = blob.sentiment.polarity

            # Keyword-based sentiment analysis
            text_lower = text.lower()
            bullish_count = sum(
                1 for keyword in self.bullish_keywords if keyword in text_lower
            )
            bearish_count = sum(
                1 for keyword in self.bearish_keywords if keyword in text_lower
            )

            # Calculate keyword score
            total_keywords = bullish_count + bearish_count
            if total_keywords > 0:
                keyword_score = (bullish_count - bearish_count) / total_keywords
            else:
                keyword_score = 0.0

            # Combine scores (weighted average)
            combined_score = (textblob_score * 0.6) + (keyword_score * 0.4)

            # Calculate confidence based on text length and keyword presence
            confidence = min(1.0, (len(text) / 1000) + (total_keywords / 10))

            return combined_score, confidence

        except Exception as e:
            logger.error(f"Error analyzing text sentiment: {e}")
            return 0.0, 0.0

    def analyze_news_sentiment(
        self, articles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from news articles"""
        try:
            sentiment_data = []

            for article in articles:
                # Analyze article title and content
                title_score, title_confidence = self.analyze_text_sentiment(
                    article["title"]
                )
                content_score, content_confidence = self.analyze_text_sentiment(
                    article["content"]
                )

                # Combined sentiment score
                combined_score = (title_score * 0.4) + (content_score * 0.6)
                combined_confidence = (title_confidence * 0.3) + (
                    content_confidence * 0.7
                )

                # Determine sentiment type
                if combined_score > self.sentiment_params["textblob_threshold"]:
                    sentiment_type = "BULLISH"
                elif combined_score < -self.sentiment_params["textblob_threshold"]:
                    sentiment_type = "BEARISH"
                else:
                    sentiment_type = "NEUTRAL"

                # Calculate impact score based on source credibility and content length
                impact_score = self.calculate_news_impact(article)

                # Create sentiment data
                sentiment_data.append({
                    "source": "NEWS",
                    "sentiment_type": sentiment_type,
                    "confidence": combined_confidence,
                    "score": combined_score,
                    "text": f"{article['title']}: {article['content'][:200]}...",
                    "timestamp": article["published_at"],
                    "symbol": article["symbol"],
                    "weight": impact_score,
                    "metadata": {
                        "source": article["source"],
                        "url": article["url"],
                        "impact_score": impact_score,
                    },
                })

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {e}")
            return []

    def calculate_news_impact(self, article: Dict[str, Any]) -> float:
        """Calculate news impact score"""
        try:
            impact_score = 1.0

            # Source credibility
            credible_sources = [
                "reuters", "bloomberg", "cnbc", "wsj", "ft", "yahoo finance"
            ]
            if any(source in article["source"].lower() for source in credible_sources):
                impact_score *= 1.2

            # Content length
            content_length = len(article["content"])
            if content_length > 1000:
                impact_score *= 1.1
            elif content_length < 200:
                impact_score *= 0.8

            # Keywords presence
            keyword_count = sum(
                1
                for keyword in self.bullish_keywords + self.bearish_keywords
                if keyword in article["content"].lower()
            )
            if keyword_count > 5:
                impact_score *= 1.15

            # Recency (newer articles have higher impact)
            age_hours = (datetime.now() - article["published_at"]).total_seconds() / 3600
            if age_hours < 24:
                impact_score *= 1.1
            elif age_hours > 168:  # 1 week
                impact_score *= 0.9

            return min(2.0, max(0.1, impact_score))

        except Exception as e:
            logger.error(f"Error calculating news impact: {e}")
            return 1.0

    def analyze_social_media_sentiment(
        self, social_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment from social media data"""
        try:
            sentiment_data = []

            for post in social_data:
                text = post.get("text", "")
                if not text:
                    continue

                # Analyze sentiment
                score, confidence = self.analyze_text_sentiment(text)

                # Determine sentiment type
                if score > self.sentiment_params["textblob_threshold"]:
                    sentiment_type = "BULLISH"
                elif score < -self.sentiment_params["textblob_threshold"]:
                    sentiment_type = "BEARISH"
                else:
                    sentiment_type = "NEUTRAL"

                # Calculate weight based on engagement
                engagement = (
                    post.get("likes", 0)
                    + post.get("retweets", 0)
                    + post.get("replies", 0)
                )
                weight = min(2.0, 1.0 + (engagement / 1000))

                sentiment_data.append({
                    "source": "SOCIAL_MEDIA",
                    "sentiment_type": sentiment_type,
                    "confidence": confidence,
                    "score": score,
                    "text": text[:200] + "..." if len(text) > 200 else text,
                    "timestamp": datetime.fromisoformat(
                        post.get("timestamp", datetime.now().isoformat())
                    ),
                    "symbol": post.get("symbol", ""),
                    "weight": weight,
                    "metadata": {
                        "platform": post.get("platform", "unknown"),
                        "engagement": engagement,
                        "author_followers": post.get("author_followers", 0),
                    },
                })

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing social media sentiment: {e}")
            return []

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of text analysis capabilities"""
        return {
            "supported_content_types": ["news", "social_media", "general_text"],
            "analysis_methods": ["textblob", "keyword_based", "hybrid"],
            "bullish_keywords_count": len(self.bullish_keywords),
            "bearish_keywords_count": len(self.bearish_keywords),
            "sentiment_threshold": self.sentiment_params["textblob_threshold"],
            "confidence_threshold": self.sentiment_params["confidence_threshold"]
        }
