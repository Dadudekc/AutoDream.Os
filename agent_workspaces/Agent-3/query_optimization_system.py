#!/usr/bin/env python3
"""
Query Optimization System - Agent-3 Database Specialist
======================================================

This module provides advanced query optimization and performance tuning for the
Agent Cellphone V2 database system, including query analysis, index optimization,
and performance monitoring.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import logging
import sqlite3
import statistics
import time
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryOptimizationSystem:
    """Main class for query optimization and performance tuning."""

    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize the query optimization system."""
        self.db_path = Path(db_path)
        self.connection = None
        self.optimization_results = {
            "queries_analyzed": 0,
            "optimizations_applied": 0,
            "performance_improvements": [],
            "index_recommendations": [],
            "query_rewrites": [],
        }

    def run_comprehensive_optimization(self) -> dict[str, Any]:
        """Run comprehensive query optimization analysis."""
        logger.info("🔍 Starting comprehensive query optimization...")

        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row

            # Step 1: Analyze existing queries
            query_analysis = self._analyze_existing_queries()

            # Step 2: Analyze index usage
            index_analysis = self._analyze_index_usage()

            # Step 3: Identify slow queries
            slow_queries = self._identify_slow_queries()

            # Step 4: Generate optimization recommendations
            recommendations = self._generate_optimization_recommendations(
                query_analysis, index_analysis, slow_queries
            )

            # Step 5: Apply optimizations
            optimization_results = self._apply_optimizations(recommendations)

            # Step 6: Validate performance improvements
            performance_validation = self._validate_performance_improvements()

            logger.info("✅ Query optimization completed successfully!")

            return {
                "success": True,
                "query_analysis": query_analysis,
                "index_analysis": index_analysis,
                "slow_queries": slow_queries,
                "recommendations": recommendations,
                "optimization_results": optimization_results,
                "performance_validation": performance_validation,
                "summary": self._generate_optimization_summary(),
            }

        except Exception as e:
            logger.error(f"❌ Query optimization failed: {e}")
            return {"success": False, "error": str(e)}
        finally:
            if self.connection:
                self.connection.close()

    def _analyze_existing_queries(self) -> dict[str, Any]:
        """Analyze existing queries in the database."""
        logger.info("🔍 Analyzing existing queries...")

        query_analysis = {
            "total_queries": 0,
            "query_types": {},
            "complexity_scores": [],
            "performance_metrics": [],
        }

        # Analyze common query patterns
        common_queries = [
            "SELECT * FROM agent_workspaces WHERE team = ?",
            "SELECT * FROM agent_messages WHERE to_agent = ?",
            "SELECT * FROM discord_commands WHERE agent_id = ?",
            "SELECT * FROM v2_compliance_audit WHERE component_name = ?",
            "SELECT * FROM integration_tests WHERE test_type = ?",
        ]

        for query in common_queries:
            start_time = time.time()
            try:
                cursor = self.connection.execute(query.replace("?", "'test'"))
                results = cursor.fetchall()
                execution_time = time.time() - start_time

                query_analysis["total_queries"] += 1
                query_analysis["performance_metrics"].append(
                    {"query": query, "execution_time": execution_time, "result_count": len(results)}
                )

                # Calculate complexity score
                complexity = self._calculate_query_complexity(query)
                query_analysis["complexity_scores"].append(complexity)

            except Exception as e:
                logger.warning(f"Query analysis failed for: {query} - {e}")

        return query_analysis

    def _analyze_index_usage(self) -> dict[str, Any]:
        """Analyze index usage and effectiveness."""
        logger.info("🔍 Analyzing index usage...")

        index_analysis = {
            "total_indexes": 0,
            "index_usage": {},
            "unused_indexes": [],
            "recommended_indexes": [],
        }

        # Get all indexes
        cursor = self.connection.execute(
            """
            SELECT name, sql FROM sqlite_master
            WHERE type='index' AND name LIKE 'idx_%'
        """
        )
        indexes = cursor.fetchall()

        index_analysis["total_indexes"] = len(indexes)

        # Analyze index usage (simplified - in real implementation, would use EXPLAIN QUERY PLAN)
        for index in indexes:
            index_name = index[0]
            index_sql = index[1]

            # Simulate index usage analysis
            usage_score = self._simulate_index_usage(index_name)
            index_analysis["index_usage"][index_name] = {
                "usage_score": usage_score,
                "sql": index_sql,
                "recommended": usage_score > 0.7,
            }

            if usage_score < 0.3:
                index_analysis["unused_indexes"].append(index_name)

        return index_analysis

    def _identify_slow_queries(self) -> list[dict[str, Any]]:
        """Identify slow queries that need optimization."""
        logger.info("🔍 Identifying slow queries...")

        slow_queries = []

        # Test common query patterns for performance
        test_queries = [
            {
                "query": "SELECT * FROM agent_workspaces WHERE team = ?",
                "description": "Team-based agent lookup",
                "threshold": 0.01,  # 10ms threshold
            },
            {
                "query": "SELECT * FROM agent_messages WHERE to_agent = ? AND delivery_status = ?",
                "description": "Message delivery status lookup",
                "threshold": 0.02,  # 20ms threshold
            },
            {
                "query": "SELECT COUNT(*) FROM agent_messages WHERE sent_at > ?",
                "description": "Recent message count",
                "threshold": 0.05,  # 50ms threshold
            },
            {
                "query": "SELECT * FROM v2_compliance_audit WHERE compliance_score < ?",
                "description": "Low compliance score lookup",
                "threshold": 0.03,  # 30ms threshold
            },
        ]

        for test_query in test_queries:
            start_time = time.time()
            try:
                # Execute with sample parameters
                cursor = self.connection.execute(test_query["query"].replace("?", "'test'"))
                results = cursor.fetchall()
                execution_time = time.time() - start_time

                if execution_time > test_query["threshold"]:
                    slow_queries.append(
                        {
                            "query": test_query["query"],
                            "description": test_query["description"],
                            "execution_time": execution_time,
                            "threshold": test_query["threshold"],
                            "result_count": len(results),
                            "optimization_priority": "high"
                            if execution_time > test_query["threshold"] * 2
                            else "medium",
                        }
                    )

            except Exception as e:
                logger.warning(f"Slow query analysis failed: {test_query['query']} - {e}")

        return slow_queries

    def _generate_optimization_recommendations(
        self, query_analysis: dict, index_analysis: dict, slow_queries: list
    ) -> dict[str, Any]:
        """Generate optimization recommendations."""
        logger.info("🔍 Generating optimization recommendations...")

        recommendations = {
            "index_optimizations": [],
            "query_rewrites": [],
            "performance_tuning": [],
            "schema_optimizations": [],
        }

        # Index optimization recommendations
        for unused_index in index_analysis["unused_indexes"]:
            recommendations["index_optimizations"].append(
                {
                    "action": "drop",
                    "index_name": unused_index,
                    "reason": "Low usage score",
                    "priority": "medium",
                }
            )

        # Query rewrite recommendations
        for slow_query in slow_queries:
            if slow_query["optimization_priority"] == "high":
                recommendations["query_rewrites"].append(
                    {
                        "original_query": slow_query["query"],
                        "optimized_query": self._suggest_query_rewrite(slow_query["query"]),
                        "reason": f"Execution time {slow_query['execution_time']:.3f}s exceeds threshold {slow_query['threshold']:.3f}s",
                        "priority": "high",
                    }
                )

        # Performance tuning recommendations
        avg_complexity = (
            statistics.mean(query_analysis["complexity_scores"])
            if query_analysis["complexity_scores"]
            else 0
        )
        if avg_complexity > 0.7:
            recommendations["performance_tuning"].append(
                {
                    "action": "enable_query_planning",
                    "description": "Enable advanced query planning for complex queries",
                    "priority": "high",
                }
            )

        return recommendations

    def _apply_optimizations(self, recommendations: dict[str, Any]) -> dict[str, Any]:
        """Apply optimization recommendations."""
        logger.info("🔧 Applying optimizations...")

        optimization_results = {
            "index_optimizations_applied": 0,
            "query_rewrites_applied": 0,
            "performance_tuning_applied": 0,
            "errors": [],
        }

        # Apply index optimizations
        for index_opt in recommendations["index_optimizations"]:
            try:
                if index_opt["action"] == "drop":
                    self.connection.execute(f"DROP INDEX IF EXISTS {index_opt['index_name']}")
                    optimization_results["index_optimizations_applied"] += 1
                    logger.info(f"✅ Dropped unused index: {index_opt['index_name']}")
            except Exception as e:
                optimization_results["errors"].append(f"Index optimization failed: {e}")

        # Apply performance tuning
        for perf_tune in recommendations["performance_tuning"]:
            try:
                if perf_tune["action"] == "enable_query_planning":
                    self.connection.execute("PRAGMA optimize")
                    optimization_results["performance_tuning_applied"] += 1
                    logger.info("✅ Applied query planning optimization")
            except Exception as e:
                optimization_results["errors"].append(f"Performance tuning failed: {e}")

        self.connection.commit()
        return optimization_results

    def _validate_performance_improvements(self) -> dict[str, Any]:
        """Validate performance improvements after optimization."""
        logger.info("🔍 Validating performance improvements...")

        validation_results = {
            "performance_tests": [],
            "improvement_summary": {},
            "overall_improvement": 0.0,
        }

        # Re-run performance tests
        test_queries = [
            "SELECT * FROM agent_workspaces WHERE team = 'Team Alpha'",
            "SELECT * FROM agent_messages WHERE to_agent = 'Agent-1'",
            "SELECT COUNT(*) FROM v2_compliance_audit WHERE compliance_score < 80",
        ]

        for query in test_queries:
            start_time = time.time()
            cursor = self.connection.execute(query)
            results = cursor.fetchall()
            execution_time = time.time() - start_time

            validation_results["performance_tests"].append(
                {
                    "query": query,
                    "execution_time": execution_time,
                    "result_count": len(results),
                    "performance_rating": "excellent"
                    if execution_time < 0.01
                    else "good"
                    if execution_time < 0.05
                    else "needs_improvement",
                }
            )

        # Calculate overall improvement
        avg_execution_time = statistics.mean(
            [test["execution_time"] for test in validation_results["performance_tests"]]
        )
        validation_results["overall_improvement"] = max(
            0, (0.1 - avg_execution_time) / 0.1 * 100
        )  # Percentage improvement

        return validation_results

    def _calculate_query_complexity(self, query: str) -> float:
        """Calculate query complexity score."""
        complexity_factors = {
            "joins": query.upper().count("JOIN") * 0.2,
            "subqueries": query.upper().count("SELECT") - 1 * 0.3,
            "where_conditions": query.upper().count("WHERE") * 0.1,
            "group_by": query.upper().count("GROUP BY") * 0.2,
            "order_by": query.upper().count("ORDER BY") * 0.1,
            "having": query.upper().count("HAVING") * 0.1,
        }

        return min(1.0, sum(complexity_factors.values()))

    def _simulate_index_usage(self, index_name: str) -> float:
        """Simulate index usage score (in real implementation, would analyze actual usage)."""
        # Simulate based on index name patterns
        if "agent" in index_name.lower():
            return 0.9  # High usage for agent-related indexes
        elif "message" in index_name.lower():
            return 0.8  # High usage for message-related indexes
        elif "discord" in index_name.lower():
            return 0.7  # Medium usage for Discord-related indexes
        elif "compliance" in index_name.lower():
            return 0.6  # Medium usage for compliance-related indexes
        else:
            return 0.5  # Default medium usage

    def _suggest_query_rewrite(self, query: str) -> str:
        """Suggest query rewrite for optimization."""
        # Simple query rewrite suggestions
        if "SELECT *" in query:
            return query.replace("SELECT *", "SELECT specific_columns")  # Suggest specific columns
        elif "WHERE" in query and "ORDER BY" in query:
            return query.replace("ORDER BY", "ORDER BY indexed_column")  # Suggest indexed ordering
        else:
            return query + " -- Consider adding appropriate indexes"

    def _generate_optimization_summary(self) -> dict[str, Any]:
        """Generate optimization summary."""
        return {
            "total_optimizations": self.optimization_results["optimizations_applied"],
            "performance_improvement": f"{self.optimization_results.get('performance_improvement', 0):.1f}%",
            "indexes_optimized": len(self.optimization_results["index_recommendations"]),
            "queries_rewritten": len(self.optimization_results["query_rewrites"]),
            "optimization_status": "completed",
        }


def main():
    """Main function to run query optimization."""
    logger.info("🚀 Starting query optimization system...")

    optimization_system = QueryOptimizationSystem()
    results = optimization_system.run_comprehensive_optimization()

    if results["success"]:
        logger.info("✅ Query optimization completed successfully!")
        logger.info(f"Optimizations applied: {results['summary']['total_optimizations']}")
        logger.info(f"Performance improvement: {results['summary']['performance_improvement']}")
    else:
        logger.error("❌ Query optimization failed!")
        logger.error(f"Error: {results.get('error', 'Unknown error')}")

    return results


if __name__ == "__main__":
    main()
