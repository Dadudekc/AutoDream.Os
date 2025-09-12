#!/usr/bin/env python3
"""
Performance Benchmarking Suite
==============================

Comprehensive benchmarking for database, API, and system performance.
Measures improvements from optimization implementation.

Usage: python performance_benchmark.py [--target {database,api,memory,cache}]
"""

import statistics
import threading
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List

import psutil

from src.domain.entities.task import Task
from src.infrastructure.persistence.optimized_sqlite_task_repo import OptimizedSqliteTaskRepository

# Import optimized components
from src.infrastructure.persistence.sqlite_task_repo import SqliteTaskRepository


class PerformanceBenchmark:
    """Comprehensive performance benchmarking suite."""

    def __init__(self, db_path: str = "data/benchmark.db"):
        self.db_path = db_path
        self.original_repo = SqliteTaskRepository(db_path)
        self.optimized_repo = OptimizedSqliteTaskRepository(db_path)

        # Benchmark results
        self.results = {"database": {}, "api": {}, "memory": {}, "cache": {}}

    def setup_test_data(self, num_tasks: int = 1000) -> List[Task]:
        """Create test data for benchmarking."""
        tasks = []
        for i in range(num_tasks):
            task = Task(
                id=f"task-{i:04d}",
                title=f"Test Task {i}",
                description=f"Description for test task {i}",
                assigned_agent_id=f"Agent-{i % 8}" if i % 3 == 0 else None,
                created_at=f"2025-09-{i%30+1:02d}T{i%24:02d}:00:00",
                priority=i % 5 + 1,
            )
            tasks.append(task)
        return tasks

    def benchmark_database_performance(self, num_tasks: int = 1000) -> Dict[str, Any]:
        """Benchmark database operations performance."""
        print("🔍 Benchmarking Database Performance...")

        # Setup test data
        tasks = self.setup_test_data(num_tasks)

        results = {"original": {}, "optimized": {}}

        # Test INSERT performance
        print("  📝 Testing INSERT operations...")

        # Original repository
        start_time = time.time()
        for task in tasks[:100]:  # Test with subset for speed
            self.original_repo.add(task)
        results["original"]["insert_time"] = time.time() - start_time

        # Clear and recreate for fair comparison
        Path(self.db_path).unlink(missing_ok=True)

        # Optimized repository
        start_time = time.time()
        for task in tasks[:100]:
            self.optimized_repo.add(task)
        results["optimized"]["insert_time"] = time.time() - start_time

        # Test SELECT performance
        print("  📖 Testing SELECT operations...")

        # Original repository
        start_time = time.time()
        list(self.original_repo.get_all(limit=50))
        results["original"]["select_time"] = time.time() - start_time

        # Optimized repository (with cache warming)
        start_time = time.time()
        list(self.optimized_repo.get_all(limit=50))
        first_run = time.time() - start_time

        # Second run should be cached
        start_time = time.time()
        list(self.optimized_repo.get_all(limit=50))
        cached_run = time.time() - start_time

        results["optimized"]["select_time"] = first_run
        results["optimized"]["cached_select_time"] = cached_run

        # Test agent-specific queries
        print("  👤 Testing agent-specific queries...")

        agent_id = "Agent-1"

        # Original
        start_time = time.time()
        list(self.original_repo.get_by_agent(agent_id, limit=20))
        results["original"]["agent_query_time"] = time.time() - start_time

        # Optimized
        start_time = time.time()
        list(self.optimized_repo.get_by_agent(agent_id, limit=20))
        first_agent_run = time.time() - start_time

        start_time = time.time()
        list(self.optimized_repo.get_by_agent(agent_id, limit=20))
        cached_agent_run = time.time() - start_time

        results["optimized"]["agent_query_time"] = first_agent_run
        results["optimized"]["cached_agent_query_time"] = cached_agent_run

        return results

    def benchmark_memory_usage(self) -> Dict[str, Any]:
        """Benchmark memory usage patterns."""
        print("🧠 Benchmarking Memory Usage...")

        tracemalloc.start()
        process = psutil.Process()

        results = {"original": {}, "optimized": {}}

        # Memory test with original repository
        tracemalloc.clear_traces()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        tasks = []
        for i in range(100):
            task = self.original_repo.get(f"task-{i:04d}")
            if task:
                tasks.append(task)

        final_memory = process.memory_info().rss / 1024 / 1024
        current, peak = tracemalloc.get_traced_memory()

        results["original"] = {
            "memory_used_mb": final_memory - initial_memory,
            "tracemalloc_current_mb": current / 1024 / 1024,
            "tracemalloc_peak_mb": peak / 1024 / 1024,
            "objects_processed": len(tasks),
        }

        # Reset for optimized repository test
        tracemalloc.clear_traces()
        initial_memory = process.memory_info().rss / 1024 / 1024

        tasks = []
        for i in range(100):
            task = self.optimized_repo.get(f"task-{i:04d}")
            if task:
                tasks.append(task)

        final_memory = process.memory_info().rss / 1024 / 1024
        current, peak = tracemalloc.get_traced_memory()

        results["optimized"] = {
            "memory_used_mb": final_memory - initial_memory,
            "tracemalloc_current_mb": current / 1024 / 1024,
            "tracemalloc_peak_mb": peak / 1024 / 1024,
            "objects_processed": len(tasks),
        }

        tracemalloc.stop()
        return results

    def benchmark_api_simulation(self) -> Dict[str, Any]:
        """Simulate API load and measure response times."""
        print("🌐 Benchmarking API Simulation...")

        def simulate_api_call(repo, operation: str, *args):
            """Simulate API call with timing."""
            start_time = time.time()
            if operation == "get":
                result = repo.get(*args)
            elif operation == "get_by_agent":
                result = list(repo.get_by_agent(*args))
            elif operation == "get_pending":
                result = list(repo.get_pending(*args))
            end_time = time.time()
            return end_time - start_time

        results = {"original": {"response_times": []}, "optimized": {"response_times": []}}

        # Simulate concurrent API calls
        operations = [
            ("get", "task-0001"),
            ("get_by_agent", "Agent-1", 10),
            ("get_pending", 10),
        ] * 10  # Repeat for statistical significance

        print("  📊 Running concurrent API simulations...")

        # Test original repository
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for op in operations:
                future = executor.submit(simulate_api_call, self.original_repo, *op)
                futures.append(future)

            for future in as_completed(futures):
                results["original"]["response_times"].append(future.result())

        # Test optimized repository
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for op in operations:
                future = executor.submit(simulate_api_call, self.optimized_repo, *op)
                futures.append(future)

            for future in as_completed(futures):
                results["optimized"]["response_times"].append(future.result())

        # Calculate statistics
        for repo_name in ["original", "optimized"]:
            times = results[repo_name]["response_times"]
            if times:
                results[repo_name]["avg_response_time"] = statistics.mean(times)
                results[repo_name]["median_response_time"] = statistics.median(times)
                results[repo_name]["p95_response_time"] = statistics.quantiles(times, n=20)[
                    18
                ]  # 95th percentile
                results[repo_name]["min_response_time"] = min(times)
                results[repo_name]["max_response_time"] = max(times)

        return results

    def benchmark_cache_performance(self) -> Dict[str, Any]:
        """Benchmark caching performance and hit rates."""
        print("💾 Benchmarking Cache Performance...")

        results = {
            "cache_stats": self.optimized_repo.get_cache_stats(),
            "hit_rates": {},
            "invalidation_performance": {},
        }

        # Test cache hit rates
        print("  🎯 Testing cache hit rates...")

        # Warm up cache
        for i in range(50):
            self.optimized_repo.get(f"task-{i:04d}")

        # Measure cache hits
        cache_hits = 0
        cache_misses = 0
        test_iterations = 100

        for _ in range(test_iterations):
            # Mix of cache hits and misses
            task_id = f"task-{(0 if _ % 3 == 0 else 999):04d}"  # 33% hit rate
            task = self.optimized_repo.get(task_id)
            if task:
                cache_hits += 1
            else:
                cache_misses += 1

        results["hit_rates"] = {
            "total_requests": test_iterations,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "hit_rate_percent": (cache_hits / test_iterations) * 100,
        }

        # Test cache invalidation performance
        print("  🗑️ Testing cache invalidation performance...")

        start_time = time.time()
        invalidated = self.optimized_repo._cache.invalidate_pattern("task")
        invalidation_time = time.time() - start_time

        results["invalidation_performance"] = {
            "entries_invalidated": invalidated,
            "invalidation_time_ms": invalidation_time * 1000,
            "avg_time_per_entry_us": (invalidation_time * 1000000) / max(invalidated, 1),
        }

        return results

    def run_full_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmarking suite."""
        print("🚀 Starting Full Performance Benchmark Suite")
        print("=" * 50)

        # Database Performance
        self.results["database"] = self.benchmark_database_performance()

        # Memory Usage
        self.results["memory"] = self.benchmark_memory_usage()

        # API Simulation
        self.results["api"] = self.benchmark_api_simulation()

        # Cache Performance
        self.results["cache"] = self.benchmark_cache_performance()

        return self.results

    def print_results(self):
        """Print formatted benchmark results."""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE BENCHMARK RESULTS")
        print("=" * 60)

        # Database Results
        print("\n🔍 DATABASE PERFORMANCE:")
        db_results = self.results["database"]
        for repo, metrics in db_results.items():
            print(f"  {repo.upper()}:")
            for metric, value in metrics.items():
                print(".4f")

        # API Results
        print("\n🌐 API RESPONSE TIMES:")
        api_results = self.results["api"]
        for repo, metrics in api_results.items():
            if "avg_response_time" in metrics:
                print(f"  {repo.upper()}:")
                print(".4f")
                print(".4f")
                print(".4f")

        # Memory Results
        print("\n🧠 MEMORY USAGE:")
        mem_results = self.results["memory"]
        for repo, metrics in mem_results.items():
            print(f"  {repo.upper()}:")
            print(".2f")
            print(".2f")

        # Cache Results
        print("\n💾 CACHE PERFORMANCE:")
        cache_results = self.results["cache"]
        if "hit_rates" in cache_results:
            hr = cache_results["hit_rates"]
            print(".1f")
            print(f"  Total Requests: {hr['total_requests']}")

        # Performance Summary
        print("\n🏆 OPTIMIZATION IMPACT:")
        try:
            db_improvement = (
                self.results["database"]["original"]["select_time"]
                / self.results["database"]["optimized"]["select_time"]
            )
            print(".2f")

            if "avg_response_time" in self.results["api"]["original"]:
                api_improvement = (
                    self.results["api"]["original"]["avg_response_time"]
                    / self.results["api"]["api"]["optimized"]["avg_response_time"]
                )
                print(".2f")

        except (KeyError, ZeroDivisionError):
            print("  📊 Performance metrics calculated")

        print("\n✅ Benchmark Complete!")


def main():
    """Main benchmark execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Performance Benchmarking Suite")
    parser.add_argument(
        "--target",
        choices=["database", "api", "memory", "cache", "all"],
        default="all",
        help="Specific benchmark target",
    )
    parser.add_argument(
        "--tasks", type=int, default=1000, help="Number of test tasks for database benchmarks"
    )
    parser.add_argument("--output", type=str, help="Output results to JSON file")

    args = parser.parse_args()

    # Initialize benchmark suite
    benchmark = PerformanceBenchmark()

    print("🚀 Agent Cellphone V2 Performance Benchmark Suite")
    print("=" * 55)

    if args.target == "all":
        results = benchmark.run_full_benchmark()
        benchmark.print_results()
    else:
        if args.target == "database":
            results = {"database": benchmark.benchmark_database_performance(args.tasks)}
        elif args.target == "api":
            results = {"api": benchmark.benchmark_api_simulation()}
        elif args.target == "memory":
            results = {"memory": benchmark.benchmark_memory_usage()}
        elif args.target == "cache":
            results = {"cache": benchmark.benchmark_cache_performance()}

        # Print specific results
        print(f"\n📊 {args.target.upper()} BENCHMARK RESULTS:")
        for category, data in results.items():
            print(f"  {category}: {data}")

    # Save results if requested
    if args.output:
        import json

        with open(args.output, "w") as f:
            json.dump(benchmark.results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {args.output}")


if __name__ == "__main__":
    main()
