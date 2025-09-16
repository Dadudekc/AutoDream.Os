"""
Advanced Data Analysis Engine - V2 Compliant
Advanced data analysis engine with statistical analysis and pattern recognition
V2 COMPLIANT: Under 400 lines, single responsibility.
Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    def __init__(self):
        self.analysis_cache = {}
        self.analysis_stats = {"total_analyses": 0, "cache_hits": 0, "statistical_tests": 0}

    def analyze_distribution(self, data: list[float]) -> dict[str, Any]:
        if not data:
            return {"error": "No data provided"}
        try:
            mean_val = statistics.mean(data)
            median_val = statistics.median(data)
            mode_val = statistics.mode(data) if len(set(data)) < len(data) else None
            std_dev = statistics.stdev(data) if len(data) > 1 else 0.0
            variance = statistics.variance(data) if len(data) > 1 else 0.0
            percentiles = {}
            for p in [25, 50, 75, 90, 95, 99]:
                percentiles[f"p{p}"] = self._calculate_percentile(data, p)
            skewness = self._calculate_skewness(data, mean_val, std_dev)
            kurtosis = self._calculate_kurtosis(data, mean_val, std_dev)
            outliers = self._detect_outliers(data, mean_val, std_dev)
            self.analysis_stats["total_analyses"] += 1
            return {
                "basic_stats": {
                    "count": len(data),
                    "mean": round(mean_val, 4),
                    "median": round(median_val, 4),
                    "mode": mode_val,
                    "std_dev": round(std_dev, 4),
                    "variance": round(variance, 4),
                },
                "percentiles": {k: round(v, 4) for k, v in percentiles.items()},
                "distribution": {
                    "skewness": round(skewness, 4),
                    "kurtosis": round(kurtosis, 4),
                    "outliers_count": len(outliers),
                    "outliers": outliers[:10],
                },
            }
        except Exception as e:
            logger.error(f"Error in distribution analysis: {e}")
            return {"error": str(e)}

    def _calculate_percentile(self, data: list[float], percentile: int) -> float:
        sorted_data = sorted(data)
        index = percentile / 100 * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

    def _calculate_skewness(self, data: list[float], mean_val: float, std_dev: float) -> float:
        if std_dev == 0 or len(data) < 3:
            return 0.0
        n = len(data)
        skew_sum = sum(((x - mean_val) / std_dev) ** 3 for x in data)
        return n / ((n - 1) * (n - 2)) * skew_sum

    def _calculate_kurtosis(self, data: list[float], mean_val: float, std_dev: float) -> float:
        if std_dev == 0 or len(data) < 4:
            return 0.0
        n = len(data)
        kurt_sum = sum(((x - mean_val) / std_dev) ** 4 for x in data)
        return n * (n + 1) / ((n - 1) * (n - 2) * (n - 3)) * kurt_sum - 3 * (n - 1) ** 2 / (
            (n - 2) * (n - 3)
        )

    def _detect_outliers(self, data: list[float], mean_val: float, std_dev: float) -> list[float]:
        if len(data) < 4:
            return []
        q1 = self._calculate_percentile(data, 25)
        q3 = self._calculate_percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return [x for x in data if x < lower_bound or x > upper_bound]


class PatternRecognizer:
    def __init__(self):
        self.pattern_cache = {}
        self.recognition_stats = {
            "patterns_identified": 0,
            "trend_analyses": 0,
            "seasonality_detected": 0,
        }

    def identify_trends(self, time_series: list[tuple[datetime, float]]) -> dict[str, Any]:
        if len(time_series) < 2:
            return {"error": "Insufficient data for trend analysis"}
        try:
            timestamps = [ts[0] for ts in time_series]
            values = [ts[1] for ts in time_series]
            trend_slope, trend_intercept, r_squared = self._linear_regression(timestamps, values)
            if abs(trend_slope) < 0.001:
                trend_direction = "stable"
            elif trend_slope > 0:
                trend_direction = "increasing"
            else:
                trend_direction = "decreasing"
            trend_strength = abs(r_squared)
            seasonality = self._detect_seasonality(time_series)
            self.recognition_stats["trend_analyses"] += 1
            if seasonality["detected"]:
                self.recognition_stats["seasonality_detected"] += 1
            return {
                "trend": {
                    "direction": trend_direction,
                    "slope": round(trend_slope, 6),
                    "strength": round(trend_strength, 4),
                    "r_squared": round(r_squared, 4),
                },
                "seasonality": seasonality,
                "data_points": len(time_series),
            }
        except Exception as e:
            logger.error(f"Error in trend identification: {e}")
            return {"error": str(e)}

    def _linear_regression(
        self, x_data: list[datetime], y_data: list[float]
    ) -> tuple[float, float, float]:
        first_timestamp = x_data[0]
        x_numeric = [(ts - first_timestamp).total_seconds() for ts in x_data]
        n = len(x_numeric)
        sum_x = sum(x_numeric)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_numeric, y_data, strict=False))
        sum_x2 = sum(x * x for x in x_numeric)
        sum_y2 = sum(y * y for y in y_data)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean) ** 2 for y in y_data)
        ss_res = sum(
            (y - (slope * x + intercept)) ** 2 for x, y in zip(x_numeric, y_data, strict=False)
        )
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return slope, intercept, r_squared

    def _detect_seasonality(self, time_series: list[tuple[datetime, float]]) -> dict[str, Any]:
        if len(time_series) < 24:
            return {"detected": False, "reason": "Insufficient data"}
        try:
            hourly_data = defaultdict(list)
            for timestamp, value in time_series:
                hour = timestamp.hour
                hourly_data[hour].append(value)
            hourly_averages = {}
            for hour, values in hourly_data.items():
                if values:
                    hourly_averages[hour] = statistics.mean(values)
            if len(hourly_averages) > 1:
                overall_mean = statistics.mean(hourly_averages.values())
                variance = statistics.variance(hourly_averages.values())
                seasonality_strength = variance / overall_mean**2 if overall_mean != 0 else 0
                detected = seasonality_strength > 0.1
                return {
                    "detected": detected,
                    "strength": round(seasonality_strength, 4),
                    "hourly_pattern": {str(h): round(avg, 4) for h, avg in hourly_averages.items()},
                    "peak_hour": (
                        max(hourly_averages.items(), key=lambda x: x[1])[0]
                        if hourly_averages
                        else None
                    ),
                }
            else:
                return {"detected": False, "reason": "Insufficient hourly data"}
        except Exception as e:
            logger.error(f"Error in seasonality detection: {e}")
            return {"detected": False, "error": str(e)}


class InsightsGenerator:
    def __init__(self):
        self.insights_cache = {}
        self.generation_stats = {
            "insights_generated": 0,
            "actionable_insights": 0,
            "predictive_insights": 0,
        }

    def generate_insights(self, analysis_data: dict[str, Any]) -> dict[str, Any]:
        try:
            insights = {"summary": [], "recommendations": [], "alerts": [], "predictions": []}
            if "basic_stats" in analysis_data:
                insights["summary"].extend(
                    self._generate_statistical_insights(analysis_data["basic_stats"])
                )
            if "distribution" in analysis_data:
                insights["alerts"].extend(
                    self._generate_distribution_alerts(analysis_data["distribution"])
                )
            if "trend" in analysis_data:
                insights["recommendations"].extend(
                    self._generate_trend_recommendations(analysis_data["trend"])
                )
                insights["predictions"].extend(
                    self._generate_trend_predictions(analysis_data["trend"])
                )
            if "seasonality" in analysis_data:
                insights["recommendations"].extend(
                    self._generate_seasonality_recommendations(analysis_data["seasonality"])
                )
            self.generation_stats["insights_generated"] += 1
            if insights["recommendations"]:
                self.generation_stats["actionable_insights"] += 1
            if insights["predictions"]:
                self.generation_stats["predictive_insights"] += 1
            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {"error": str(e)}

    def _generate_statistical_insights(self, stats: dict[str, Any]) -> list[str]:
        insights = []
        if stats.get("std_dev", 0) > stats.get("mean", 0) * 0.5:
            insights.append("High variability detected - data shows significant spread")
        if stats.get("count", 0) < 30:
            insights.append(
                "Small sample size - consider collecting more data for reliable analysis"
            )
        return insights

    def _generate_distribution_alerts(self, distribution: dict[str, Any]) -> list[str]:
        alerts = []
        if distribution.get("outliers_count", 0) > 0:
            alerts.append(
                f"Outliers detected: {distribution['outliers_count']} values outside normal range"
            )
        if abs(distribution.get("skewness", 0)) > 1:
            alerts.append("Highly skewed distribution - data may not be normally distributed")
        return alerts

    def _generate_trend_recommendations(self, trend: dict[str, Any]) -> list[str]:
        recommendations = []
        direction = trend.get("direction", "stable")
        strength = trend.get("strength", 0)
        if direction == "increasing" and strength > 0.7:
            recommendations.append("Strong upward trend detected - consider scaling resources")
        elif direction == "decreasing" and strength > 0.7:
            recommendations.append("Strong downward trend detected - investigate potential issues")
        elif strength < 0.3:
            recommendations.append("Weak trend - data may be too noisy for reliable predictions")
        return recommendations

    def _generate_trend_predictions(self, trend: dict[str, Any]) -> list[str]:
        """Generate predictions from trend analysis."""
        predictions = []
        direction = trend.get("direction", "stable")
        strength = trend.get("strength", 0)
        if strength > 0.5:
            if direction == "increasing":
                predictions.append("Trend suggests continued growth in next period")
            elif direction == "decreasing":
                predictions.append("Trend suggests continued decline in next period")
        return predictions

    def _generate_seasonality_recommendations(self, seasonality: dict[str, Any]) -> list[str]:
        """Generate recommendations from seasonality analysis."""
        recommendations = []
        if seasonality.get("detected", False):
            peak_hour = seasonality.get("peak_hour")
            if peak_hour is not None:
                recommendations.append(
                    f"Peak activity detected at hour {peak_hour} - optimize resources accordingly"
                )
            strength = seasonality.get("strength", 0)
            if strength > 0.2:
                recommendations.append(
                    "Strong seasonality pattern - consider time-based optimization strategies"
                )
        return recommendations


class AdvancedDataAnalysisEngine:
    """Main advanced data analysis engine."""

    def __init__(self):
        self.statistical_analyzer = StatisticalAnalyzer()
        self.pattern_recognizer = PatternRecognizer()
        self.insights_generator = InsightsGenerator()
        self.engine_stats = {"total_analyses": 0, "successful_analyses": 0, "failed_analyses": 0}

    def analyze_data(
        self, data: list[float] | list[tuple[datetime, float]], analysis_type: str = "comprehensive"
    ) -> dict[str, Any]:
        """Perform comprehensive data analysis."""
        try:
            self.engine_stats["total_analyses"] += 1
            result = {
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "data_points": len(data),
            }
            if isinstance(data[0], (int, float)):
                stats_result = self.statistical_analyzer.analyze_distribution(data)
                result["statistical_analysis"] = stats_result
                insights = self.insights_generator.generate_insights(stats_result)
                result["insights"] = insights
            elif isinstance(data[0], tuple) and len(data[0]) == 2:
                values = [item[1] for item in data]
                stats_result = self.statistical_analyzer.analyze_distribution(values)
                result["statistical_analysis"] = stats_result
                trend_result = self.pattern_recognizer.identify_trends(data)
                result["trend_analysis"] = trend_result
                combined_analysis = {**stats_result, **trend_result}
                insights = self.insights_generator.generate_insights(combined_analysis)
                result["insights"] = insights
            self.engine_stats["successful_analyses"] += 1
            return result
        except Exception as e:
            logger.error(f"Error in data analysis: {e}")
            self.engine_stats["failed_analyses"] += 1
            return {"error": str(e)}

    def get_engine_stats(self) -> dict[str, Any]:
        """Get engine statistics."""
        return {
            "engine_stats": self.engine_stats,
            "statistical_analyzer": self.statistical_analyzer.analysis_stats,
            "pattern_recognizer": self.pattern_recognizer.recognition_stats,
            "insights_generator": self.insights_generator.generation_stats,
        }


_global_analysis_engine = None


def get_advanced_data_analysis_engine() -> AdvancedDataAnalysisEngine:
    """Get global advanced data analysis engine."""
    global _global_analysis_engine
    if _global_analysis_engine is None:
        _global_analysis_engine = AdvancedDataAnalysisEngine()
    return _global_analysis_engine


if __name__ == "__main__":
    engine = get_advanced_data_analysis_engine()
    numeric_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 100]
    result = engine.analyze_data(numeric_data)
    logger.info(f"Numeric analysis result: {result}")
    now = datetime.now()
    time_series_data = [(now + timedelta(hours=i), 10 + i * 2 + i % 3 * 5) for i in range(24)]
    result = engine.analyze_data(time_series_data)
    logger.info(f"Time series analysis result: {result}")
    stats = engine.get_engine_stats()
    logger.info(f"Engine stats: {stats}")
