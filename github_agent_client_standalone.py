"""
GitHub Agent Client - Standalone Version
========================================

Simple GitHub API client for agents to access GitHub repositories and data.
Provides authentication and basic GitHub operations.
"""

import json
from github_agent_client_core import GitHubAgentClientCore


class GitHubAgentClient:
    """GitHub API client for agents."""

    def __init__(self, config_path: str = None):
        """Initialize GitHub client with configuration."""
        self.core = GitHubAgentClientCore(config_path)

    def test_connection(self) -> dict[str, Any]:
        """Test GitHub API connection."""
        return self.core.test_connection()

    def get_repositories(self, username: str = None, per_page: int = 30) -> list[GitHubRepository]:
        """Get repositories for a user."""
        return self.core.get_repositories(username, per_page)

    def get_repository_info(self, owner: str, repo: str) -> dict[str, Any]:
        """Get detailed information about a specific repository."""
        return self.core.get_repository_info(owner, repo)

    def get_repository_contents(
        self, owner: str, repo: str, path: str = ""
    ) -> list[dict[str, Any]]:
        """Get contents of a repository directory."""
        return self.core.get_repository_contents(owner, repo, path)

    def get_file_content(self, owner: str, repo: str, path: str) -> str:
        """Get content of a specific file."""
        return self.core.get_file_content(owner, repo, path)

    def search_repositories(self, query: str, per_page: int = 30) -> list[GitHubRepository]:
        """Search for repositories."""
        return self.core.search_repositories(query, per_page)

    def get_user_info(self, username: str = None) -> dict[str, Any]:
        """Get user information."""
        return self.core.get_user_info(username)

    def get_rate_limit(self) -> dict[str, Any]:
        """Get API rate limit information."""
        return self.core.get_rate_limit()


def main():
    """CLI interface for GitHub Agent Client."""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Agent Client")
    parser.add_argument("--config", help="Path to GitHub config file")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--repos", help="Get repositories for username")
    parser.add_argument("--user", help="Get user info")
    parser.add_argument("--search", help="Search repositories")
    parser.add_argument("--rate-limit", action="store_true", help="Check rate limit")

    args = parser.parse_args()

    try:
        client = GitHubAgentClient(args.config)

        if args.test:
            result = client.test_connection()
            print(json.dumps(result, indent=2))

        elif args.repos:
            repos = client.get_repositories(args.repos)
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:10]:  # Show first 10
                print(f"  {repo.full_name} - {repo.stars} stars - {repo.language or 'No language'}")

        elif args.user:
            user_info = client.get_user_info(args.user)
            print(f"User: {user_info['name']} (@{user_info['login']})")
            print(f"Public repos: {user_info['public_repos']}")
            print(f"Followers: {user_info['followers']}")

        elif args.search:
            repos = client.search_repositories(args.search)
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:10]:  # Show first 10
                print(f"  {repo.full_name} - {repo.stars} stars")

        elif args.rate_limit:
            rate_limit = client.get_rate_limit()
            core = rate_limit["rate"]
            print(f"Rate limit: {core['remaining']}/{core['limit']} requests")
            print(f"Resets at: {core['reset']}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())