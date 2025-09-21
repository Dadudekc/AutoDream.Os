"""
Test Suite for GitHub Agent Client
==================================

Tests for GitHub API client functionality and authentication.
"""

import pytest
import json
from unittest.mock import Mock, patch, mock_open
from tools.github_agent_client import (
    GitHubConfig, GitHubRepository, GitHubAgentClient
)

# ---------- Test Data ----------

SAMPLE_CONFIG_DATA = {
    "username": "testuser",
    "token": "ghp_test_token_12345",
    "setup_date": "2025-01-17T19:00:00Z",
    "wizard_version": "1.0"
}

SAMPLE_USER_DATA = {
    "login": "testuser",
    "name": "Test User",
    "email": "test@example.com",
    "public_repos": 10,
    "total_private_repos": 5
}

SAMPLE_REPO_DATA = {
    "name": "test-repo",
    "full_name": "testuser/test-repo",
    "description": "A test repository",
    "html_url": "https://github.com/testuser/test-repo",
    "clone_url": "https://github.com/testuser/test-repo.git",
    "language": "Python",
    "stargazers_count": 42,
    "forks_count": 7,
    "size": 1024,
    "updated_at": "2025-01-17T19:00:00Z",
    "private": False
}

# ---------- GitHubConfig Tests ----------

class TestGitHubConfig:
    """Test GitHub configuration data class."""
    
    def test_config_creation(self):
        """Test GitHubConfig creation."""
        config = GitHubConfig(
            username="testuser",
            token="test_token",
            setup_date="2025-01-17T19:00:00Z",
            wizard_version="1.0"
        )
        
        assert config.username == "testuser"
        assert config.token == "test_token"
        assert config.setup_date == "2025-01-17T19:00:00Z"
        assert config.wizard_version == "1.0"

# ---------- GitHubRepository Tests ----------

class TestGitHubRepository:
    """Test GitHub repository data class."""
    
    def test_repository_creation(self):
        """Test GitHubRepository creation."""
        repo = GitHubRepository(
            name="test-repo",
            full_name="testuser/test-repo",
            description="A test repository",
            url="https://github.com/testuser/test-repo",
            clone_url="https://github.com/testuser/test-repo.git",
            language="Python",
            stars=42,
            forks=7,
            size=1024,
            updated_at="2025-01-17T19:00:00Z",
            private=False
        )
        
        assert repo.name == "test-repo"
        assert repo.full_name == "testuser/test-repo"
        assert repo.description == "A test repository"
        assert repo.language == "Python"
        assert repo.stars == 42
        assert repo.forks == 7
        assert repo.private is False

# ---------- GitHubAgentClient Tests ----------

class TestGitHubAgentClient:
    """Test GitHub Agent Client functionality."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_client_initialization(self, mock_json_load, mock_file):
        """Test client initialization with config file."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        client = GitHubAgentClient("test_config.json")
        
        assert client.config.username == "testuser"
        assert client.config.token == "ghp_test_token_12345"
        assert client.base_url == "https://api.github.com"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "token ghp_test_token_12345"
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_config_loading_default_paths(self, mock_json_load, mock_file):
        """Test config loading with default paths."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock Path.exists to return True for the first path
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            client = GitHubAgentClient()
            
            assert client.config.username == "testuser"
            assert client.config.token == "ghp_test_token_12345"
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_test_connection_success(self, mock_get, mock_json_load, mock_file):
        """Test successful connection test."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_USER_DATA
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        result = client.test_connection()
        
        assert result["status"] == "success"
        assert result["authenticated"] is True
        assert result["username"] == "testuser"
        assert result["name"] == "Test User"
        assert result["public_repos"] == 10
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_test_connection_failure(self, mock_get, mock_json_load, mock_file):
        """Test failed connection test."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        result = client.test_connection()
        
        assert result["status"] == "error"
        assert result["authenticated"] is False
        assert "401" in result["error"]
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_get_repositories(self, mock_get, mock_json_load, mock_file):
        """Test getting repositories."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [SAMPLE_REPO_DATA]
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        repos = client.get_repositories("testuser")
        
        assert len(repos) == 1
        assert repos[0].name == "test-repo"
        assert repos[0].full_name == "testuser/test-repo"
        assert repos[0].stars == 42
        assert repos[0].language == "Python"
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_get_repository_info(self, mock_get, mock_json_load, mock_file):
        """Test getting repository information."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_REPO_DATA
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        repo_info = client.get_repository_info("testuser", "test-repo")
        
        assert repo_info["name"] == "test-repo"
        assert repo_info["full_name"] == "testuser/test-repo"
        assert repo_info["language"] == "Python"
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_get_file_content(self, mock_get, mock_json_load, mock_file):
        """Test getting file content."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response with base64 encoded content
        import base64
        test_content = "print('Hello, World!')"
        encoded_content = base64.b64encode(test_content.encode()).decode()
        
        file_data = {
            "type": "file",
            "content": encoded_content,
            "name": "test.py"
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = file_data
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        content = client.get_file_content("testuser", "test-repo", "test.py")
        
        assert content == test_content
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_search_repositories(self, mock_get, mock_json_load, mock_file):
        """Test searching repositories."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response
        search_response = {
            "items": [SAMPLE_REPO_DATA]
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = search_response
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        repos = client.search_repositories("python test")
        
        assert len(repos) == 1
        assert repos[0].name == "test-repo"
        assert repos[0].full_name == "testuser/test-repo"
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_get_user_info(self, mock_get, mock_json_load, mock_file):
        """Test getting user information."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_USER_DATA
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        user_info = client.get_user_info("testuser")
        
        assert user_info["login"] == "testuser"
        assert user_info["name"] == "Test User"
        assert user_info["public_repos"] == 10
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_get_rate_limit(self, mock_get, mock_json_load, mock_file):
        """Test getting rate limit information."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API response
        rate_limit_data = {
            "rate": {
                "limit": 5000,
                "remaining": 4999,
                "reset": 1640995200
            }
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = rate_limit_data
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        rate_limit = client.get_rate_limit()
        
        assert rate_limit["rate"]["limit"] == 5000
        assert rate_limit["rate"]["remaining"] == 4999
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_api_error_handling(self, mock_get, mock_json_load, mock_file):
        """Test API error handling."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        client = GitHubAgentClient("test_config.json")
        
        with pytest.raises(Exception) as exc_info:
            client.get_repositories("nonexistent")
        
        assert "404" in str(exc_info.value)
        assert "Not Found" in str(exc_info.value)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_config_file_not_found(self, mock_json_load, mock_file):
        """Test handling of missing config file."""
        mock_file.side_effect = FileNotFoundError()
        
        with pytest.raises(FileNotFoundError):
            GitHubAgentClient("nonexistent_config.json")

# ---------- Integration Tests ----------

class TestIntegration:
    """Integration tests for GitHub client."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('requests.get')
    def test_full_workflow(self, mock_get, mock_json_load, mock_file):
        """Test complete workflow from connection to data retrieval."""
        mock_json_load.return_value = SAMPLE_CONFIG_DATA
        
        # Mock multiple API responses
        def mock_get_side_effect(url, **kwargs):
            mock_response = Mock()
            
            if "/user" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = SAMPLE_USER_DATA
            elif "/repos" in url and "contents" not in url:
                mock_response.status_code = 200
                mock_response.json.return_value = [SAMPLE_REPO_DATA]
            elif "/rate_limit" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "rate": {"limit": 5000, "remaining": 4999, "reset": 1640995200}
                }
            else:
                mock_response.status_code = 404
                mock_response.text = "Not Found"
            
            return mock_response
        
        mock_get.side_effect = mock_get_side_effect
        
        client = GitHubAgentClient("test_config.json")
        
        # Test connection
        connection_result = client.test_connection()
        assert connection_result["status"] == "success"
        
        # Test getting repositories
        repos = client.get_repositories("testuser")
        assert len(repos) == 1
        assert repos[0].name == "test-repo"
        
        # Test rate limit
        rate_limit = client.get_rate_limit()
        assert rate_limit["rate"]["remaining"] == 4999

if __name__ == "__main__":
    pytest.main([__file__, "-v"])


