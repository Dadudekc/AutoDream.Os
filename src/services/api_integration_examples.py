#!/usr/bin/env python3
"""
V2 API Integration Examples
===========================
Comprehensive examples demonstrating the V2 API integration framework capabilities.
Follows V2 coding standards: 300 target, 350 max LOC.
"""

import json
import time
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add parent directory to path for imports
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the API integration framework
try:
    from services.v2_api_integration_framework import (
        V2APIIntegrationFramework,
        APIEndpoint,
        APIRequest,
        APIResponse,
        HTTPMethod,
        AuthType,
    )
except ImportError:
    from v2_api_integration_framework import (
        V2APIIntegrationFramework,
        APIEndpoint,
        APIRequest,
        APIResponse,
        HTTPMethod,
        AuthType,
    )

logger = logging.getLogger(__name__)


class V2APIIntegrationExamples:
    """Comprehensive examples for V2 API integration framework"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.V2APIIntegrationExamples")
        self.examples_dir = Path("api_examples")
        self.examples_dir.mkdir(exist_ok=True)

        # Example configurations
        self.example_configs = {
            "rest_api": {
                "base_url": "https://jsonplaceholder.typicode.com",
                "endpoints": [
                    {
                        "name": "get_posts",
                        "path": "/posts",
                        "method": "GET",
                        "auth": "none",
                    },
                    {
                        "name": "get_post",
                        "path": "/posts/{id}",
                        "method": "GET",
                        "auth": "none",
                    },
                    {
                        "name": "create_post",
                        "path": "/posts",
                        "method": "POST",
                        "auth": "none",
                    },
                    {
                        "name": "update_post",
                        "path": "/posts/{id}",
                        "method": "PUT",
                        "auth": "none",
                    },
                    {
                        "name": "delete_post",
                        "path": "/posts/{id}",
                        "method": "DELETE",
                        "auth": "none",
                    },
                ],
            },
            "weather_api": {
                "base_url": "https://api.openweathermap.org/data/2.5",
                "endpoints": [
                    {
                        "name": "current_weather",
                        "path": "/weather",
                        "method": "GET",
                        "auth": "api_key",
                    },
                    {
                        "name": "forecast",
                        "path": "/forecast",
                        "method": "GET",
                        "auth": "api_key",
                    },
                ],
            },
            "github_api": {
                "base_url": "https://api.github.com",
                "endpoints": [
                    {
                        "name": "get_user",
                        "path": "/users/{username}",
                        "method": "GET",
                        "auth": "none",
                    },
                    {
                        "name": "get_repos",
                        "path": "/users/{username}/repos",
                        "method": "GET",
                        "auth": "none",
                    },
                    {
                        "name": "create_repo",
                        "path": "/user/repos",
                        "method": "POST",
                        "auth": "bearer",
                    },
                ],
            },
        }

    def create_rest_api_example(self) -> V2APIIntegrationFramework:
        """Create a REST API integration example"""
        self.logger.info("Creating REST API integration example")

        config = self.example_configs["rest_api"]
        framework = V2APIIntegrationFramework(config["base_url"])

        # Register endpoints
        for endpoint_config in config["endpoints"]:
            method = HTTPMethod(endpoint_config["method"])
            auth_type = AuthType.NONE  # JSONPlaceholder doesn't require auth

            framework.register_endpoint(
                name=endpoint_config["name"],
                url=endpoint_config["path"],
                method=method,
                auth_type=auth_type,
                timeout=10.0,
                retry_count=2,
            )

        self.logger.info(
            f"REST API example created with {len(config['endpoints'])} endpoints"
        )
        return framework

    def create_weather_api_example(self) -> V2APIIntegrationFramework:
        """Create a weather API integration example"""
        self.logger.info("Creating Weather API integration example")

        config = self.example_configs["weather_api"]
        framework = V2APIIntegrationFramework(config["base_url"])

        # Register endpoints
        for endpoint_config in config["endpoints"]:
            method = HTTPMethod(endpoint_config["method"])
            auth_type = AuthType.API_KEY

            framework.register_endpoint(
                name=endpoint_config["name"],
                url=endpoint_config["path"],
                method=method,
                auth_type=auth_type,
                timeout=15.0,
                retry_count=3,
                rate_limit=60,  # 60 requests per minute
            )

        # Set API key (demo key - replace with real key for production)
        framework.set_auth_credentials("current_weather", {"api_key": "demo_key_123"})
        framework.set_auth_credentials("forecast", {"api_key": "demo_key_123"})

        self.logger.info(
            f"Weather API example created with {len(config['endpoints'])} endpoints"
        )
        return framework

    def create_github_api_example(self) -> V2APIIntegrationFramework:
        """Create a GitHub API integration example"""
        self.logger.info("Creating GitHub API integration example")

        config = self.example_configs["github_api"]
        framework = V2APIIntegrationFramework(config["base_url"])

        # Register endpoints
        for endpoint_config in config["endpoints"]:
            method = HTTPMethod(endpoint_config["method"])
            auth_type = (
                AuthType.NONE
                if "auth" not in endpoint_config
                else AuthType.BEARER_TOKEN
            )

            framework.register_endpoint(
                name=endpoint_config["name"],
                url=endpoint_config["path"],
                method=method,
                auth_type=auth_type,
                timeout=20.0,
                retry_count=2,
                rate_limit=30,  # GitHub has rate limits
            )

        # Set bearer token for authenticated endpoints
        framework.set_auth_credentials(
            "create_repo", {"bearer_token": "demo_token_123"}
        )

        self.logger.info(
            f"GitHub API example created with {len(config['endpoints'])} endpoints"
        )
        return framework

    def run_rest_api_example(self) -> Dict[str, Any]:
        """Run the REST API integration example"""
        self.logger.info("Running REST API integration example")

        framework = self.create_rest_api_example()
        results = {}

        try:
            # Get posts list
            endpoint = framework._endpoints["get_posts"]
            request = APIRequest(endpoint=endpoint)
            response = framework.execute_request(request)

            results["get_posts"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "data_count": len(response.data) if response.data else 0,
            }

            # Get single post
            endpoint = framework._endpoints["get_post"]
            request = APIRequest(endpoint=endpoint, query_params={"id": "1"})
            response = framework.execute_request(request)

            results["get_post"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "has_data": bool(response.data),
            }

            # Create post
            endpoint = framework._endpoints["create_post"]
            post_data = {
                "title": "Test Post",
                "body": "This is a test post created by V2 API Integration Framework",
                "userId": 1,
            }
            request = APIRequest(endpoint=endpoint, data=post_data)
            response = framework.execute_request(request)

            results["create_post"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "created_id": response.data.get("id") if response.data else None,
            }

        except Exception as e:
            self.logger.error(f"Error running REST API example: {e}")
            results["error"] = str(e)

        return results

    def run_weather_api_example(self) -> Dict[str, Any]:
        """Run the weather API integration example"""
        self.logger.info("Running Weather API integration example")

        framework = self.create_weather_api_example()
        results = {}

        try:
            # Get current weather
            endpoint = framework._endpoints["current_weather"]
            request = APIRequest(
                endpoint=endpoint,
                query_params={
                    "q": "London",
                    "appid": "demo_key_123",
                    "units": "metric",
                },
            )
            response = framework.execute_request(request)

            results["current_weather"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "has_weather_data": bool(response.data),
            }

        except Exception as e:
            self.logger.error(f"Error running Weather API example: {e}")
            results["error"] = str(e)

        return results

    def run_github_api_example(self) -> Dict[str, Any]:
        """Run the GitHub API integration example"""
        self.logger.info("Running GitHub API integration example")

        framework = self.create_github_api_example()
        results = {}

        try:
            # Get user info
            endpoint = framework._endpoints["get_user"]
            request = APIRequest(
                endpoint=endpoint, query_params={"username": "octocat"}
            )
            response = framework.execute_request(request)

            results["get_user"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "username": response.data.get("login") if response.data else None,
            }

            # Get user repos
            endpoint = framework._endpoints["get_repos"]
            request = APIRequest(
                endpoint=endpoint, query_params={"username": "octocat"}
            )
            response = framework.execute_request(request)

            results["get_repos"] = {
                "success": response.success,
                "status_code": response.status_code,
                "response_time": response.response_time,
                "repo_count": len(response.data) if response.data else 0,
            }

        except Exception as e:
            self.logger.error(f"Error running GitHub API example: {e}")
            results["error"] = str(e)

        return results

    def run_all_examples(self) -> Dict[str, Any]:
        """Run all API integration examples"""
        self.logger.info("Running all API integration examples")

        all_results = {"timestamp": time.time(), "examples": {}}

        # Run REST API example
        try:
            rest_results = self.run_rest_api_example()
            all_results["examples"]["rest_api"] = rest_results
        except Exception as e:
            all_results["examples"]["rest_api"] = {"error": str(e)}

        # Run Weather API example
        try:
            weather_results = self.run_weather_api_example()
            all_results["examples"]["weather_api"] = weather_results
        except Exception as e:
            all_results["examples"]["weather_api"] = {"error": str(e)}

        # Run GitHub API example
        try:
            github_results = self.run_github_api_example()
            all_results["examples"]["github_api"] = github_results
        except Exception as e:
            all_results["examples"]["github_api"] = {"error": str(e)}

        # Save results
        results_file = self.examples_dir / "api_integration_results.json"
        with open(results_file, "w") as f:
            json.dump(all_results, f, indent=2)

        self.logger.info(f"All examples completed. Results saved to: {results_file}")
        return all_results

    def get_example_summary(self) -> Dict[str, Any]:
        """Get summary of all examples"""
        summary = {
            "total_examples": len(self.example_configs),
            "example_types": list(self.example_configs.keys()),
            "total_endpoints": sum(
                len(config["endpoints"]) for config in self.example_configs.values()
            ),
            "auth_types": ["none", "api_key", "bearer_token"],
            "supported_methods": [method.value for method in HTTPMethod],
        }

        return summary


def main():
    """CLI interface for V2APIIntegrationExamples"""
    import argparse

    parser = argparse.ArgumentParser(description="V2 API Integration Examples CLI")
    parser.add_argument("--run-all", action="store_true", help="Run all examples")
    parser.add_argument("--run-rest", action="store_true", help="Run REST API example")
    parser.add_argument(
        "--run-weather", action="store_true", help="Run Weather API example"
    )
    parser.add_argument(
        "--run-github", action="store_true", help="Run GitHub API example"
    )
    parser.add_argument("--summary", action="store_true", help="Show examples summary")

    args = parser.parse_args()

    # Initialize examples
    examples = V2APIIntegrationExamples()

    if args.run_all:
        print("🚀 Running all API integration examples...")
        results = examples.run_all_examples()
        print("✅ All examples completed!")
        print(f"Results saved to: api_examples/api_integration_results.json")

    elif args.run_rest:
        print("🚀 Running REST API integration example...")
        results = examples.run_rest_api_example()
        print("✅ REST API example completed!")
        print(f"Results: {json.dumps(results, indent=2)}")

    elif args.run_weather:
        print("🚀 Running Weather API integration example...")
        results = examples.run_weather_api_example()
        print("✅ Weather API example completed!")
        print(f"Results: {json.dumps(results, indent=2)}")

    elif args.run_github:
        print("🚀 Running GitHub API integration example...")
        results = examples.run_github_api_example()
        print("✅ GitHub API example completed!")
        print(f"Results: {json.dumps(results, indent=2)}")

    elif args.summary:
        summary = examples.get_example_summary()
        print("📋 API Integration Examples Summary:")
        print(f"Total Examples: {summary['total_examples']}")
        print(f"Example Types: {', '.join(summary['example_types'])}")
        print(f"Total Endpoints: {summary['total_endpoints']}")
        print(f"Auth Types: {', '.join(summary['auth_types'])}")
        print(f"HTTP Methods: {', '.join(summary['supported_methods'])}")

    else:
        print("V2APIIntegrationExamples ready")
        print("Use --run-all to run all examples")
        print("Use --run-rest to run REST API example")
        print("Use --run-weather to run Weather API example")
        print("Use --run-github to run GitHub API example")
        print("Use --summary to show examples summary")


if __name__ == "__main__":
    main()
