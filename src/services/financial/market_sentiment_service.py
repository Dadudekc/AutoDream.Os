"""
Market Sentiment Analysis Service - Business Intelligence & Trading Systems
Agent-5: Business Intelligence & Trading Specialist
Performance & Health Systems Division

Provides comprehensive market sentiment analysis, news analysis, and market psychology insights.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from collections import defaultdict
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentSource(Enum):
    """Sentiment data sources"""

    NEWS = "NEWS"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    ANALYST_RATINGS = "ANALYST_RATINGS"
    OPTIONS_FLOW = "OPTIONS_FLOW"
    INSIDER_TRADING = "INSIDER_TRADING"
    FUNDAMENTAL_DATA = "FUNDAMENTAL_DATA"
    TECHNICAL_INDICATORS = "TECHNICAL_INDICATORS"


class SentimentType(Enum):
    """Types of sentiment analysis"""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    MIXED = "MIXED"


@dataclass
class SentimentData:
    """Individual sentiment data point"""

    source: SentimentSource
    sentiment_type: SentimentType
    confidence: float  # 0.0 to 1.0
    score: float  # -1.0 to 1.0
    text: str
    timestamp: datetime
    symbol: str = ""
    weight: float = 1.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SentimentAggregate:
    """Aggregated sentiment data"""

    symbol: str
    overall_sentiment: SentimentType
    sentiment_score: float
    confidence: float
    source_breakdown: Dict[SentimentSource, float]
    sentiment_trend: str  # IMPROVING, DETERIORATING, STABLE
    volatility: float
    momentum: float
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class NewsArticle:
    """News article data"""

    title: str
    content: str
    source: str
    url: str
    published_at: datetime
    symbol: str = ""
    sentiment_score: float = 0.0
    impact_score: float = 0.0
    keywords: List[str] = None

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


@dataclass
class MarketPsychology:
    """Market psychology indicators"""

    fear_greed_index: float  # 0-100
    volatility_regime: str  # LOW, MEDIUM, HIGH, EXTREME
    momentum_bias: str  # BULLISH, BEARISH, NEUTRAL
    contrarian_signals: List[str]
    crowd_sentiment: str  # EXTREME_BULLISH, BULLISH, NEUTRAL, BEARISH, EXTREME_BEARISH
    market_regime: str  # TRENDING, RANGING, BREAKOUT, BREAKDOWN
    last_updated: datetime = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


class MarketSentimentService:
    """Advanced market sentiment analysis and psychology service"""

    def __init__(self, market_data_service=None, data_dir: str = "market_sentiment"):
        self.market_data_service = market_data_service
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.sentiment_data: Dict[str, List[SentimentData]] = defaultdict(list)
        self.sentiment_aggregates: Dict[str, SentimentAggregate] = {}
        self.news_articles: Dict[str, List[NewsArticle]] = defaultdict(list)
        self.market_psychology: MarketPsychology = None

        self.sentiment_file = self.data_dir / "sentiment_data.json"
        self.aggregates_file = self.data_dir / "sentiment_aggregates.json"
        self.news_file = self.data_dir / "news_articles.json"
        self.psychology_file = self.data_dir / "market_psychology.json"

        # Sentiment analysis parameters
        self.sentiment_params = {
            "textblob_threshold": 0.1,
            "confidence_threshold": 0.6,
            "source_weights": {
                SentimentSource.NEWS: 0.3,
                SentimentSource.SOCIAL_MEDIA: 0.2,
                SentimentSource.ANALYST_RATINGS: 0.25,
                SentimentSource.OPTIONS_FLOW: 0.15,
                SentimentSource.INSIDER_TRADING: 0.1,
            },
            "decay_factor": 0.95,  # Sentiment decay over time
            "min_data_points": 5,  # Minimum data points for reliable sentiment
        }

        # Keywords for sentiment analysis
        self.bullish_keywords = [
            "bullish",
            "positive",
            "growth",
            "recovery",
            "rally",
            "surge",
            "gain",
            "strong",
            "improve",
            "beat",
            "exceed",
            "upgrade",
            "buy",
            "outperform",
        ]

        self.bearish_keywords = [
            "bearish",
            "negative",
            "decline",
            "fall",
            "drop",
            "crash",
            "loss",
            "weak",
            "worsen",
            "miss",
            "downgrade",
            "sell",
            "underperform",
        ]

        self.load_data()

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
        self, articles: List[NewsArticle]
    ) -> List[SentimentData]:
        """Analyze sentiment from news articles"""
        try:
            sentiment_data = []

            for article in articles:
                # Analyze article title and content
                title_score, title_confidence = self.analyze_text_sentiment(
                    article.title
                )
                content_score, content_confidence = self.analyze_text_sentiment(
                    article.content
                )

                # Combined sentiment score
                combined_score = (title_score * 0.4) + (content_score * 0.6)
                combined_confidence = (title_confidence * 0.3) + (
                    content_confidence * 0.7
                )

                # Determine sentiment type
                if combined_score > self.sentiment_params["textblob_threshold"]:
                    sentiment_type = SentimentType.BULLISH
                elif combined_score < -self.sentiment_params["textblob_threshold"]:
                    sentiment_type = SentimentType.BEARISH
                else:
                    sentiment_type = SentimentType.NEUTRAL

                # Calculate impact score based on source credibility and content length
                impact_score = self.calculate_news_impact(article)

                # Create sentiment data
                sentiment_data.append(
                    SentimentData(
                        source=SentimentSource.NEWS,
                        sentiment_type=sentiment_type,
                        confidence=combined_confidence,
                        score=combined_score,
                        text=f"{article.title}: {article.content[:200]}...",
                        timestamp=article.published_at,
                        symbol=article.symbol,
                        weight=impact_score,
                        metadata={
                            "source": article.source,
                            "url": article.url,
                            "impact_score": impact_score,
                        },
                    )
                )

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {e}")
            return []

    def calculate_news_impact(self, article: NewsArticle) -> float:
        """Calculate news impact score"""
        try:
            impact_score = 1.0

            # Source credibility
            credible_sources = [
                "reuters",
                "bloomberg",
                "cnbc",
                "wsj",
                "ft",
                "yahoo finance",
            ]
            if any(source in article.source.lower() for source in credible_sources):
                impact_score *= 1.2

            # Content length
            content_length = len(article.content)
            if content_length > 1000:
                impact_score *= 1.1
            elif content_length < 200:
                impact_score *= 0.8

            # Keywords presence
            keyword_count = sum(
                1
                for keyword in self.bullish_keywords + self.bearish_keywords
                if keyword in article.content.lower()
            )
            if keyword_count > 5:
                impact_score *= 1.15

            # Recency (newer articles have higher impact)
            age_hours = (datetime.now() - article.published_at).total_seconds() / 3600
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
    ) -> List[SentimentData]:
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
                    sentiment_type = SentimentType.BULLISH
                elif score < -self.sentiment_params["textblob_threshold"]:
                    sentiment_type = SentimentType.BEARISH
                else:
                    sentiment_type = SentimentType.NEUTRAL

                # Calculate weight based on engagement
                engagement = (
                    post.get("likes", 0)
                    + post.get("retweets", 0)
                    + post.get("replies", 0)
                )
                weight = min(2.0, 1.0 + (engagement / 1000))

                sentiment_data.append(
                    SentimentData(
                        source=SentimentSource.SOCIAL_MEDIA,
                        sentiment_type=sentiment_type,
                        confidence=confidence,
                        score=score,
                        text=text[:200] + "..." if len(text) > 200 else text,
                        timestamp=datetime.fromisoformat(
                            post.get("timestamp", datetime.now().isoformat())
                        ),
                        symbol=post.get("symbol", ""),
                        weight=weight,
                        metadata={
                            "platform": post.get("platform", "unknown"),
                            "engagement": engagement,
                            "author_followers": post.get("author_followers", 0),
                        },
                    )
                )

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing social media sentiment: {e}")
            return []

    def analyze_analyst_ratings(
        self, ratings_data: List[Dict[str, Any]]
    ) -> List[SentimentData]:
        """Analyze sentiment from analyst ratings"""
        try:
            sentiment_data = []

            rating_scores = {
                "strong_buy": 1.0,
                "buy": 0.7,
                "hold": 0.0,
                "sell": -0.7,
                "strong_sell": -1.0,
            }

            for rating in ratings_data:
                rating_type = rating.get("rating", "hold").lower()
                score = rating_scores.get(rating_type, 0.0)

                # Determine sentiment type
                if score > 0.5:
                    sentiment_type = SentimentType.BULLISH
                elif score < -0.5:
                    sentiment_type = SentimentType.BEARISH
                else:
                    sentiment_type = SentimentType.NEUTRAL

                # Calculate confidence based on analyst track record
                track_record = rating.get("analyst_track_record", 0.5)
                confidence = min(1.0, 0.6 + (track_record * 0.4))

                # Calculate weight based on price target and current price
                current_price = rating.get("current_price", 0)
                price_target = rating.get("price_target", 0)

                if current_price > 0 and price_target > 0:
                    price_change_pct = (price_target - current_price) / current_price
                    weight = 1.0 + abs(price_change_pct) * 2
                else:
                    weight = 1.0

                sentiment_data.append(
                    SentimentData(
                        source=SentimentSource.ANALYST_RATINGS,
                        sentiment_type=sentiment_type,
                        confidence=confidence,
                        score=score,
                        text=f"Analyst {rating.get('analyst', 'Unknown')}: {rating_type.upper()} - Target: ${price_target}",
                        timestamp=datetime.fromisoformat(
                            rating.get("timestamp", datetime.now().isoformat())
                        ),
                        symbol=rating.get("symbol", ""),
                        weight=weight,
                        metadata={
                            "analyst": rating.get("analyst", "Unknown"),
                            "firm": rating.get("firm", "Unknown"),
                            "price_target": price_target,
                            "track_record": track_record,
                        },
                    )
                )

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing analyst ratings: {e}")
            return []

    def analyze_options_flow_sentiment(
        self, options_data: List[Dict[str, Any]]
    ) -> List[SentimentData]:
        """Analyze sentiment from options flow data"""
        try:
            sentiment_data = []

            for option in options_data:
                # Calculate sentiment based on options flow
                call_volume = option.get("call_volume", 0)
                put_volume = option.get("put_volume", 0)
                total_volume = call_volume + put_volume

                if total_volume == 0:
                    continue

                # Calculate put-call ratio sentiment
                put_call_ratio = (
                    put_volume / call_volume if call_volume > 0 else float("inf")
                )

                # Lower put-call ratio indicates bullish sentiment
                if put_call_ratio < 0.5:
                    sentiment_type = SentimentType.BULLISH
                    score = 0.8
                elif put_call_ratio > 2.0:
                    sentiment_type = SentimentType.BEARISH
                    score = -0.8
                else:
                    sentiment_type = SentimentType.NEUTRAL
                    score = 0.0

                # Calculate confidence based on volume
                confidence = min(1.0, total_volume / 10000)

                # Calculate weight based on unusual activity
                unusual_activity = option.get("unusual_activity", False)
                weight = 1.5 if unusual_activity else 1.0

                sentiment_data.append(
                    SentimentData(
                        source=SentimentSource.OPTIONS_FLOW,
                        sentiment_type=sentiment_type,
                        confidence=confidence,
                        score=score,
                        text=f"Options Flow: Call Volume: {call_volume}, Put Volume: {put_volume}, PCR: {put_call_ratio:.2f}",
                        timestamp=datetime.fromisoformat(
                            option.get("timestamp", datetime.now().isoformat())
                        ),
                        symbol=option.get("symbol", ""),
                        weight=weight,
                        metadata={
                            "call_volume": call_volume,
                            "put_volume": put_volume,
                            "put_call_ratio": put_call_ratio,
                            "unusual_activity": unusual_activity,
                            "strike": option.get("strike", 0),
                            "expiration": option.get("expiration", ""),
                        },
                    )
                )

            return sentiment_data

        except Exception as e:
            logger.error(f"Error analyzing options flow sentiment: {e}")
            return []

    def aggregate_sentiment(
        self, symbol: str, time_window: timedelta = timedelta(days=7)
    ) -> SentimentAggregate:
        """Aggregate sentiment data for a symbol"""
        try:
            if symbol not in self.sentiment_data:
                return None

            # Filter data by time window
            cutoff_time = datetime.now() - time_window
            recent_data = [
                data
                for data in self.sentiment_data[symbol]
                if data.timestamp >= cutoff_time
            ]

            if len(recent_data) < self.sentiment_params["min_data_points"]:
                return None

            # Calculate weighted sentiment scores by source
            source_scores = defaultdict(list)
            source_weights = self.sentiment_params["source_weights"]

            for data in recent_data:
                source_scores[data.source].append(data.score * data.weight)

            # Calculate aggregate scores by source
            source_breakdown = {}
            total_weighted_score = 0.0
            total_weight = 0.0

            for source, scores in source_scores.items():
                if scores:
                    avg_score = np.mean(scores)
                    source_breakdown[source] = avg_score

                    weight = source_weights.get(source, 0.1)
                    total_weighted_score += avg_score * weight
                    total_weight += weight

            # Calculate overall sentiment score
            overall_score = (
                total_weighted_score / total_weight if total_weight > 0 else 0.0
            )

            # Determine sentiment type
            if overall_score > 0.2:
                overall_sentiment = SentimentType.BULLISH
            elif overall_score < -0.2:
                overall_sentiment = SentimentType.BEARISH
            else:
                overall_sentiment = SentimentType.NEUTRAL

            # Calculate confidence
            confidence = min(1.0, len(recent_data) / 20)

            # Calculate sentiment trend
            if len(recent_data) >= 10:
                recent_scores = [data.score for data in recent_data[-10:]]
                trend_slope = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]

                if trend_slope > 0.01:
                    sentiment_trend = "IMPROVING"
                elif trend_slope < -0.01:
                    sentiment_trend = "DETERIORATING"
                else:
                    sentiment_trend = "STABLE"
            else:
                sentiment_trend = "STABLE"

            # Calculate volatility and momentum
            scores = [data.score for data in recent_data]
            volatility = np.std(scores) if len(scores) > 1 else 0.0

            if len(scores) >= 5:
                momentum = np.mean(scores[-5:]) - np.mean(scores[:5])
            else:
                momentum = 0.0

            aggregate = SentimentAggregate(
                symbol=symbol,
                overall_sentiment=overall_sentiment,
                sentiment_score=overall_score,
                confidence=confidence,
                source_breakdown=source_breakdown,
                sentiment_trend=sentiment_trend,
                volatility=volatility,
                momentum=momentum,
            )

            # Store aggregate
            self.sentiment_aggregates[symbol] = aggregate

            return aggregate

        except Exception as e:
            logger.error(f"Error aggregating sentiment for {symbol}: {e}")
            return None

    def calculate_market_psychology(self, symbols: List[str]) -> MarketPsychology:
        """Calculate overall market psychology indicators"""
        try:
            if not symbols:
                return None

            # Get sentiment aggregates for all symbols
            sentiment_scores = []
            volatility_scores = []
            momentum_scores = []

            for symbol in symbols:
                aggregate = self.sentiment_aggregates.get(symbol)
                if aggregate:
                    sentiment_scores.append(aggregate.sentiment_score)
                    volatility_scores.append(aggregate.volatility)
                    momentum_scores.append(aggregate.momentum)

            if not sentiment_scores:
                return None

            # Calculate fear-greed index
            avg_sentiment = np.mean(sentiment_scores)
            fear_greed_index = 50 + (
                avg_sentiment * 50
            )  # Convert -1 to 1 range to 0-100

            # Determine volatility regime
            avg_volatility = np.mean(volatility_scores)
            if avg_volatility < 0.1:
                volatility_regime = "LOW"
            elif avg_volatility < 0.3:
                volatility_regime = "MEDIUM"
            elif avg_volatility < 0.5:
                volatility_regime = "HIGH"
            else:
                volatility_regime = "EXTREME"

            # Determine momentum bias
            avg_momentum = np.mean(momentum_scores)
            if avg_momentum > 0.1:
                momentum_bias = "BULLISH"
            elif avg_momentum < -0.1:
                momentum_bias = "BEARISH"
            else:
                momentum_bias = "NEUTRAL"

            # Identify contrarian signals
            contrarian_signals = []
            if fear_greed_index > 80:
                contrarian_signals.append("EXTREME_BULLISH - Consider taking profits")
            elif fear_greed_index < 20:
                contrarian_signals.append(
                    "EXTREME_FEAR - Consider buying opportunities"
                )

            if volatility_regime == "EXTREME":
                contrarian_signals.append(
                    "HIGH_VOLATILITY - Market stress, potential reversal"
                )

            # Determine crowd sentiment
            if fear_greed_index > 70:
                crowd_sentiment = "EXTREME_BULLISH"
            elif fear_greed_index > 60:
                crowd_sentiment = "BULLISH"
            elif fear_greed_index > 40:
                crowd_sentiment = "NEUTRAL"
            elif fear_greed_index > 30:
                crowd_sentiment = "BEARISH"
            else:
                crowd_sentiment = "EXTREME_BEARISH"

            # Determine market regime
            if abs(avg_momentum) > 0.2 and avg_volatility < 0.3:
                market_regime = "TRENDING"
            elif avg_volatility > 0.4:
                market_regime = "BREAKOUT"
            elif avg_volatility < 0.2:
                market_regime = "RANGING"
            else:
                market_regime = "MIXED"

            psychology = MarketPsychology(
                fear_greed_index=fear_greed_index,
                volatility_regime=volatility_regime,
                momentum_bias=momentum_bias,
                contrarian_signals=contrarian_signals,
                crowd_sentiment=crowd_sentiment,
                market_regime=market_regime,
            )

            self.market_psychology = psychology
            return psychology

        except Exception as e:
            logger.error(f"Error calculating market psychology: {e}")
            return None

    def get_sentiment_signals(self, symbol: str) -> List[Dict[str, Any]]:
        """Get trading signals based on sentiment analysis"""
        try:
            aggregate = self.sentiment_aggregates.get(symbol)
            if not aggregate:
                return []

            signals = []

            # Strong sentiment signals
            if aggregate.confidence > 0.8:
                if (
                    aggregate.overall_sentiment == SentimentType.BULLISH
                    and aggregate.sentiment_score > 0.5
                ):
                    signals.append(
                        {
                            "type": "STRONG_BULLISH_SENTIMENT",
                            "confidence": aggregate.confidence,
                            "score": aggregate.sentiment_score,
                            "reasoning": f"Strong bullish sentiment across {len(aggregate.source_breakdown)} sources",
                        }
                    )
                elif (
                    aggregate.overall_sentiment == SentimentType.BEARISH
                    and aggregate.sentiment_score < -0.5
                ):
                    signals.append(
                        {
                            "type": "STRONG_BEARISH_SENTIMENT",
                            "confidence": aggregate.confidence,
                            "score": aggregate.sentiment_score,
                            "reasoning": f"Strong bearish sentiment across {len(aggregate.source_breakdown)} sources",
                        }
                    )

            # Sentiment trend signals
            if aggregate.sentiment_trend == "IMPROVING" and aggregate.momentum > 0.2:
                signals.append(
                    {
                        "type": "SENTIMENT_IMPROVING",
                        "confidence": aggregate.confidence,
                        "score": aggregate.momentum,
                        "reasoning": "Sentiment improving with positive momentum",
                    }
                )
            elif (
                aggregate.sentiment_trend == "DETERIORATING"
                and aggregate.momentum < -0.2
            ):
                signals.append(
                    {
                        "type": "SENTIMENT_DETERIORATING",
                        "confidence": aggregate.confidence,
                        "score": aggregate.momentum,
                        "reasoning": "Sentiment deteriorating with negative momentum",
                    }
                )

            # Volatility signals
            if aggregate.volatility > 0.4:
                signals.append(
                    {
                        "type": "HIGH_SENTIMENT_VOLATILITY",
                        "confidence": aggregate.confidence,
                        "score": aggregate.volatility,
                        "reasoning": "High sentiment volatility indicates market uncertainty",
                    }
                )

            return signals

        except Exception as e:
            logger.error(f"Error getting sentiment signals for {symbol}: {e}")
            return []

    def add_sentiment_data(
        self, symbol: str, sentiment_data: List[SentimentData]
    ) -> None:
        """Add sentiment data for a symbol"""
        try:
            if symbol not in self.sentiment_data:
                self.sentiment_data[symbol] = []

            # Add new data
            self.sentiment_data[symbol].extend(sentiment_data)

            # Remove old data (older than 30 days)
            cutoff_time = datetime.now() - timedelta(days=30)
            self.sentiment_data[symbol] = [
                data
                for data in self.sentiment_data[symbol]
                if data.timestamp >= cutoff_time
            ]

            # Recalculate aggregate
            self.aggregate_sentiment(symbol)

            logger.info(
                f"Added {len(sentiment_data)} sentiment data points for {symbol}"
            )

        except Exception as e:
            logger.error(f"Error adding sentiment data for {symbol}: {e}")

    def save_data(self):
        """Save sentiment data"""
        try:
            # Save sentiment data
            sentiment_data = {}
            for symbol, data_list in self.sentiment_data.items():
                sentiment_data[symbol] = [asdict(data) for data in data_list]

            with open(self.sentiment_file, "w") as f:
                json.dump(sentiment_data, f, indent=2, default=str)

            # Save sentiment aggregates
            aggregates_data = {
                symbol: asdict(aggregate)
                for symbol, aggregate in self.sentiment_aggregates.items()
            }

            with open(self.aggregates_file, "w") as f:
                json.dump(aggregates_data, f, indent=2, default=str)

            # Save news articles
            news_data = {
                symbol: [asdict(article) for article in articles]
                for symbol, articles in self.news_articles.items()
            }

            with open(self.news_file, "w") as f:
                json.dump(news_data, f, indent=2, default=str)

            # Save market psychology
            if self.market_psychology:
                with open(self.psychology_file, "w") as f:
                    json.dump(asdict(self.market_psychology), f, indent=2, default=str)

            logger.info("Sentiment data saved successfully")

        except Exception as e:
            logger.error(f"Error saving sentiment data: {e}")

    def load_data(self):
        """Load sentiment data"""
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

                        sentiment_data_obj = SentimentData(**data_dict)
                        self.sentiment_data[symbol].append(sentiment_data_obj)

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

                    aggregate_obj = SentimentAggregate(**aggregate_dict)
                    self.sentiment_aggregates[symbol] = aggregate_obj

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

                        article_obj = NewsArticle(**article_dict)
                        self.news_articles[symbol].append(article_obj)

                logger.info(f"Loaded news articles for {len(news_data)} symbols")

            # Load market psychology
            if self.psychology_file.exists():
                with open(self.psychology_file, "r") as f:
                    psychology_dict = json.load(f)

                if "last_updated" in psychology_dict:
                    psychology_dict["last_updated"] = datetime.fromisoformat(
                        psychology_dict["last_updated"]
                    )

                self.market_psychology = MarketPsychology(**psychology_dict)
                logger.info("Loaded market psychology data")

        except Exception as e:
            logger.error(f"Error loading sentiment data: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create market sentiment service
    mss = MarketSentimentService()

    # Test text sentiment analysis
    test_text = (
        "The company reported strong earnings growth and exceeded analyst expectations."
    )
    score, confidence = mss.analyze_text_sentiment(test_text)

    print(f"Sentiment Score: {score:.3f}")
    print(f"Confidence: {confidence:.3f}")

    # Test news sentiment analysis
    test_article = NewsArticle(
        title="Company Beats Earnings Expectations",
        content="The company reported quarterly earnings that exceeded analyst estimates by 15%.",
        source="Financial News",
        url="https://example.com",
        published_at=datetime.now(),
        symbol="TEST",
    )

    sentiment_data = mss.analyze_news_sentiment([test_article])
    print(f"News Sentiment: {sentiment_data[0].sentiment_type.value}")

    print("Market Sentiment Service initialized successfully")
